#!/usr/bin/python

import sys
import lexer_parser

print_int = """void print(int value) {
    char temp_str[11];
    itoa (value, temp_str, 10); 
    print_message(temp_str);
}"""

print_str = """void print(char *value) {
   print_message(value);
}"""


program_template = """\
#include "dal.h"
#include <math.h>

%DECLARATIONS%

void setup()
{
    microbug_setup();
}

void loop()
{
    %STATEMENTS%;
}

int main(void)
{
        init();

#if defined(USBCON)
        USBDevice.attach();
#endif
        setup(); // Switches on "eyes", and switches to bootloader if required
        enable_power_optimisations();
set_eye('L', LOW);  // Switch off eyes if bootloader not required
set_eye('R', LOW);
//        for (;;) {
                loop();
                if (serialEventRun) serialEventRun();
//        }
        return 0;
}


"""

class CodeGenerator(object):
    def __init__(self):
        self.need_print_str = False
        self.need_print_int = False
        self.declarations = []

    def program(self, statementlist):
        statement_lines = self.statementlist(statementlist)
        declarations= []
        if self.need_print_str:
            self.declarations.append(print_str)
        if self.need_print_int:
            self.declarations.append(print_int)

        program_lines = program_template
        program_lines = program_lines.replace("%STATEMENTS%", ";\n".join(statement_lines))
        program_lines = program_lines.replace("%DECLARATIONS%", "\n".join(self.declarations))
        return program_lines

    def statementlist(self, statementlist):
        assert statementlist[0] == "statementlist"
        lines = []
        for statement in statementlist[1]:
            statement_lines = self.statement(statement)
            lines.append(statement_lines)
        return lines

    def statement(self, statement):
        assert statement[0] == "statement"
        the_statement = statement[1]

        if the_statement[0] == "expression":
            gen_result = self.expression(the_statement)
            try:
                expression_type, expression_fragment = gen_result
            except ValueError:
                if not lexer_parser.quiet_mode:
                    print repr(gen_result),gen_result.__class__
                raise
            return expression_fragment

        if the_statement[0] == "assignment_statement":
            gen_result = self.assignment_statement(the_statement)
            return gen_result

        if the_statement[0] == "infix_expression":
            return self.statement(["statement", ["expression", the_statement]]) # Treat infix_expression statement as an expression statement

        if the_statement[0] == "and_expression":
            gen_result = self.and_expression(the_statement)
            return gen_result

        if the_statement[0] == "print_statement":
            print_statement_lines = self.print_statement(the_statement)
            return print_statement_lines

        if the_statement[0] == "pass_statement":
            return "// pass\n"

        if the_statement[0] == "forever_statement":
            return self.forever_statement(the_statement)

        if the_statement[0] == "while_statement":
            return self.while_statement(the_statement)

        if the_statement[0] == "for_statement":
            return self.for_statement(the_statement)

        if the_statement[0] == "if_statement":
            return self.if_statement(the_statement)

        return "//TBD (statement) " + the_statement[0]


    def assignment_statement(self, assignment_statement):
        assert assignment_statement[0] == "assignment_statement"

        # The code generator for blockly generates spurious "i = None" style
        # statements when creating loops. For now we'll intercept them here
        # and remove them
        assigment_type = assignment_statement[1]
        lvalue = assignment_statement[2]
        rvalue = assignment_statement[3]
        if rvalue[0] == "expression":
            if rvalue[1][0] == "literalvalue":
                # print "SKIPPING DECLARATION"
                if rvalue[1][1][0] == "identifier":
                    if rvalue[1][1][1] == "None":
                        return "// SKIPPING" + repr(assignment_statement)
        return "// TBD Assignment statement -- " + repr(assignment_statement)

    def if_statement(self, if_statement):
        assert if_statement[0] == "if_statement"

        main_clause_lines = []
        else_clause_lines = []

        result = "if"

        expression = if_statement[1]

        if expression[0] == "comparison":
            assert len(expression) == 4
            comparator = expression[1]
            if comparator == "<>":
                comparator = "!="

            if comparator == "is":
                comparator = "=="

            if comparator == "is not":
                comparator = "!="

            operand_L = expression[2]
            operand_R = expression[3]

            gen_operand_L = self.expression(operand_L)
            try:
                expression_type_operand_L, expression_fragment_operand_L = gen_operand_L
            except ValueError:
                if not lexer_parser.quiet_mode:
                    print repr(gen_operand_L),gen_operand_L.__class__
                raise

            gen_operand_R = self.expression(operand_R)
            try:
                expression_type_operand_R, expression_fragment_operand_R = gen_operand_R
            except ValueError:
                if not lexer_parser.quiet_mode:
                    print repr(gen_operand_R),gen_operand_R.__class__
                raise

            result += " (" + expression_fragment_operand_L + comparator + expression_fragment_operand_R + " ) "

        if expression[0] == "literalvalue":
            expression = ["expression", expression ]

        if expression[0] == "expression":
            gen_result = self.expression(expression)
            try:
                expression_type, expression_fragment = gen_result
            except ValueError:
                if not lexer_parser.quiet_mode:
                    print repr(gen_result),gen_result.__class__
                raise

            result += " (" + expression_fragment + " ) "


        statements = if_statement[2]
        if statements[0] == "statementlist":
            main_clause_lines = self.statementlist(statements)

        result += "{\n" + ";\n".join(main_clause_lines) + " ; }\n"

        if len(if_statement) == 4:
            result += self.if_trailer(if_statement[3])

        return result

    def elseclause(self, elseclause):
        if elseclause[0] == "else_clause":
            elsestatements = elseclause[1]
            if elsestatements[0] == "statementlist":
                else_clause_lines = self.statementlist(elsestatements)

            return "else {\n " + ";\n".join(else_clause_lines) + "; }\n"

    def if_trailer(self, if_trailer):
        result = ""
        if if_trailer[0] == "else_clause":
            result += self.elseclause(if_trailer)

        if if_trailer[0] == "elif_clause":
            result += " else "
            if_trailer[0] = "if_statement"
            result += self.if_statement(if_trailer)

        if type(if_trailer[0]) == list:
            for if_trailer_clause in if_trailer:
                result += self.if_trailer(if_trailer_clause)

        return result

    def for_statement(self, for_statement):
        assert for_statement[0] == "for_statement"
        identifier_spec = for_statement[1]
        range_spec = for_statement[2] # FIXME: Yes, this is hardcoded here for now
        block = for_statement[3]
        identifier = identifier_spec[1]
        max_iter = 0
        arg_one = 0
        range_args = []
        if range_spec[0] == "expression":
            range_call = range_spec[1]
            if range_call[0] == "func_call":
                if range_call[1] == "range":
                    if range_call[2][0] == "expr_list":
                        range_args_raw = range_call[2]
                        if range_args_raw[1][0] == "expression":
                            if range_args_raw[1][1][0] == "literalvalue":
                                if range_args_raw[1][1][1][0] == "number":
                                    first_arg = str(range_args_raw[1][1][1][1])
                                    range_args.append(first_arg)

                        if len(range_args_raw)>2:
                            # Extract second arg
                            if range_args_raw[2][0] == "expr_list":
                                if range_args_raw[2][1][0] == "expression":
                                    if range_args_raw[2][1][1][0] == "literalvalue":
                                        if range_args_raw[2][1][1][1][0] == "number":
                                            second_arg = str(range_args_raw[2][1][1][1][1])
                                            range_args.append(second_arg)

                            if len(range_args_raw[2])>2:
                                # Extract second arg
                                if range_args_raw[2][2][0] == "expr_list":
                                    if range_args_raw[2][2][1][0] == "expression":
                                        if range_args_raw[2][2][1][1][0] == "literalvalue":
                                            if range_args_raw[2][2][1][1][1][0] == "number":
                                                third_arg = str(range_args_raw[2][2][1][1][1][1])
                                                range_args.append(third_arg)

        init_value = "0"
        end_value = "5"
        step = "1"

        if len(range_args) == 1:
            end_value = range_args[0]

        if len(range_args) == 2:
            init_value = range_args[0]
            end_value = range_args[1]

        if len(range_args) == 3:
            init_value = range_args[0]
            end_value = range_args[1]
            step = range_args[2]

        if int(init_value)<int(end_value):
            comp = "<"
        else:
            comp = ">"
        body_lines = ""
        body_lines = "{\n" + ";\n".join(self.statementlist(block)) + ";\n}"

        return "for(int " + identifier +"="+init_value+"; "+identifier+comp+end_value+"; "+identifier+"= "+identifier+" + "+step+")\n" +body_lines

    def forever_statement(self, forever_statement):
        assert forever_statement[0] == "forever_statement"
        the_statement = forever_statement[1]
        body_lines = ""
        if the_statement[0] == "statementlist":
            body_lines = self.statementlist(the_statement)

        return "while(1) {// Forever\n"+";\n".join(body_lines)+";"+ "\n}\n"

    def while_statement(self, while_statement):
        assert while_statement[0] == "while_statement"
        result = "while"
        expression = while_statement[1]

        if expression[0] == "literalvalue":
            expression = ["expression", expression ]

        if expression[0] == "expression":
            gen_result = self.expression(expression)
            try:
                expression_type, expression_fragment = gen_result
            except ValueError:
                if not lexer_parser.quiet_mode:
                    print repr(gen_result),gen_result.__class__
                raise

            result += " (" + expression_fragment + " ) "

        if expression[0] == "comparison":
            assert len(expression) == 4
            comparator = expression[1]
            if comparator == "<>":
                comparator = "!="

            if comparator == "is":
                comparator = "=="

            if comparator == "is not":
                comparator = "!="

            operand_L = expression[2]
            operand_R = expression[3]

            gen_operand_L = self.expression(operand_L)
            try:
                expression_type_operand_L, expression_fragment_operand_L = gen_operand_L
            except ValueError:
                if not lexer_parser.quiet_mode:
                    print repr(gen_operand_L),gen_operand_L.__class__
                raise

            gen_operand_R = self.expression(operand_R)
            try:
                expression_type_operand_R, expression_fragment_operand_R = gen_operand_R
            except ValueError:
                if not lexer_parser.quiet_mode:
                    print repr(gen_operand_R),gen_operand_R.__class__
                raise

            result += " (" + expression_fragment_operand_L + comparator + expression_fragment_operand_R + " ) "


        statements = while_statement[2]

        body_lines = ""
        if statements[0] == "statementlist":
            body_lines = self.statementlist(statements)

        return result + "{// Normal\n"+";\n".join(body_lines)+";"+ "\n}\n"

    def print_statement(self, print_statement):
        assert print_statement[0] == "print_statement"
        what_to_print = print_statement[1]

        if what_to_print[0] == "expression":
            gen_result = self.expression(what_to_print)
            (expression_type, expression_fragment) = gen_result
            if expression_type == "string":
                self.need_print_str = True

            if expression_type == "int":
                self.need_print_int = True

            print_template = 'print(%WHAT%)'
            return print_template.replace("%WHAT%", expression_fragment)

        return "// TBD print_statemnt " + repr(what_to_print)

    def and_expression(self, and_expression):
        assert and_expression[0] == "and_expression"
        result = ""
        L_expression = and_expression[1]
        R_expression = and_expression[2]
        L_gen_result = self.expression(L_expression)
        (L_expression_type, L_expression_fragment) = L_gen_result

        R_gen_result = self.expression(R_expression)
        (R_expression_type, R_expression_fragment) = R_gen_result
        result += "(" + L_expression_fragment + ")"
        result += " && "
        result += "(" + R_expression_fragment + ")"
        return "(" + result + ")"

    def or_expression(self, or_expression):
        assert or_expression[0] == "or_expression"
        result = ""
        L_expression = or_expression[1]
        R_expression = or_expression[2]
        L_gen_result = self.expression(L_expression)
        (L_expression_type, L_expression_fragment) = L_gen_result

        R_gen_result = self.expression(R_expression)
        (R_expression_type, R_expression_fragment) = R_gen_result
        result += "(" + L_expression_fragment + ")"
        result += " || "
        result += "(" + R_expression_fragment + ")"
        return "(" + result + ")"

    def not_expression(self, not_expression):
        assert not_expression[0] == "not_expression"
        result = ""
        L_expression = not_expression[1]
        L_gen_result = self.expression(L_expression)
        (L_expression_type, L_expression_fragment) = L_gen_result

        result += "! (" + L_expression_fragment + ")"
        return "(" + result + ")"

    def infix_expression(self, infix_expression):
        assert infix_expression[0] == "infix_expression"
        operator = infix_expression[1]
        L_value_expression = ["expression", infix_expression[2] ]
        R_value_expression = ["expression", infix_expression[3] ]

        L_gen_result = self.expression(L_value_expression )
        L_expression_type, L_expression_fragment = L_gen_result

        R_gen_result = self.expression(R_value_expression )
        R_expression_type, R_expression_fragment = R_gen_result

        if L_expression_type != R_expression_type:
            # dunno what to do here really. Types are *wrong*
            # We should fail, but what's the C rules?
            # For the moment, we'll say the L_expression_type win
            # But print a massive warning
            print "************************** WARNING *******************************"
            print "************************** WARNING *******************************"
            print "***                                                            ***"
            print "*** THE TYPES FOR THE EXPRESSION DO NOT MATCH.                 ***"
            print "***                                                            ***"
            print "*** FOR THE MOMENT WE'RE ALLOWING THE LEFT HAND SIDE TO 'WIN'  ***"
            print "***                                                            ***"
            print "*** BUT THIS IS WRONG, AND MAY RESULT IN A FAILURE             ***"
            print "***                                                            ***"
            print "*** The reason for allowing it is because int and bool can be  ***"
            print "*** Interchanged on occasions, as can pointers etc, so this    ***"
            print "*** isn't really quite that clear cut                          ***"
            print "***                                                            ***"
            print "************************** WARNING *******************************"
            print "************************** WARNING *******************************"

        expression_type = L_expression_type
        # Brackets round sub-expressions, and round the expression as a whole.
        if operator == "**":
            result = "( pow((" + L_expression_fragment +  "), " + "(" + R_expression_fragment + ")) )"
        else:
            result = "( (" + L_expression_fragment +  ")" + operator + "(" + R_expression_fragment + ") )"

        return expression_type, result

    def expression(self, expression):
        assert expression[0] == "expression"
        the_expression = expression[1]
        if the_expression[0] == "literalvalue":
            (literalvalue_type, literalvalue_fragment) = self.literalvalue(the_expression)
            return (literalvalue_type, literalvalue_fragment)

        if the_expression[0] == "expression":
            gen_result = self.expression(the_expression)
            expression_type, expression_fragment = gen_result
            return expression_type, expression_fragment

        if the_expression[0] == "infix_expression":
            gen_result = self.infix_expression(the_expression)
            expression_type, expression_fragment = gen_result
            return expression_type, expression_fragment

        if the_expression[0] == "or_expression":
            return "boolean", self.or_expression(the_expression)

        if the_expression[0] == "and_expression":
            return "boolean", self.and_expression(the_expression)

        if the_expression[0] == "not_expression":
            return "boolean", self.not_expression(the_expression)

        if the_expression[0] == "func_call":
            if not lexer_parser.quiet_mode:
                sys.stderr.write("AHA\n")
                sys.stderr.flush()
            gen_result = self.func_call(the_expression)
            func_type, expression_fragment = gen_result
            return func_type, expression_fragment

        if not lexer_parser.quiet_mode:
            sys.stderr.write("TBD::\n")
            sys.stderr.flush()
            sys.stderr.write(repr(expression))
            sys.stderr.flush()
        return ("tbd", repr(expression))

    def func_call(self, func_call):
        # ['func_call', 'scroll_string', ['expr_list', ['expression', ['literalvalue', ['string', 'HELLO WORLD']]]]]

        assert func_call[0] == "func_call"
        if not lexer_parser.quiet_mode:
            sys.stderr.write( repr(func_call) )
            sys.stderr.write("\n")
            sys.stderr.flush()
        function_name = func_call[1]
        if len(func_call)>=3:
            function_arglist = func_call[2]
            gen_function_arglist = self.expr_list(function_arglist)
            gen_function_arglist_ = ",".join(gen_function_arglist)
            assert function_arglist[0] == "expr_list"
        else:
            gen_function_arglist_ = ""
        function_call = function_name + '("HELLO WORLD")'
        function_call = function_name + "( " + gen_function_arglist_ + " )"
        return ("void", function_call)

    def expr_list(self, expr_list):
        assert expr_list[0] == "expr_list"
        list_result = []
        for item in expr_list[1:]:
            if item[0] == "expression":
                gen_result = self.expression(item)
                expression_type, expression_fragment = gen_result
                list_result.append( expression_fragment )
            if item[0] == "expr_list":
                cdr_list = self.expr_list(item)
                list_result = list_result+cdr_list

        return list_result

    def literalvalue(self, literalvalue):
        assert literalvalue[0] == "literalvalue"
        the_literalvalue = literalvalue[1]

        if the_literalvalue[0] == "number":
            # Generated C code for a literal integer  #FIXME, integer size
            # Note that this should be a string!
            return ( "int", str( the_literalvalue[1] ) )

        if the_literalvalue[0] == "string":
            # Generated C code for a literal string
            # FIXME: Do we want to be able to auto flash things?
            # FIXME: Do we want these as predeclared constants?
            py_string = the_literalvalue[1]

            x = repr(py_string)
            x = '"' + x[1:-1] + '"'

            return ("string", x)
            # literalvalue_fragment = self.literalvalue(the_expression)
            # return literalvalue_fragment

        if the_literalvalue[0] == "boolean":
            # Generated C code for a literal integer  #FIXME, integer size
            # Note that this should be a string!
            if the_literalvalue[1] == "True":
                return ( "boolean", "true" )
            if the_literalvalue[1] == "False":
                return ( "boolean", "false" )
            return ( "boolean", "false; /* FAILED PARSE " + repr(the_literalvalue[1]) +"*/ " )

        if the_literalvalue[0] == "identifier":
            # Generated C code for a literal integer  #FIXME, integer size
            # Note that this should be a string!
            return ( "identifier", the_literalvalue[1] )


        return ("tbd", "//TBD "+ repr(literalvalue) )


def gen_code(AST):
    cg = CodeGenerator()
    if not lexer_parser.quiet_mode:
        print repr(AST)
    AST[0] = "program"
    program = cg.program(AST[1])
    return program

