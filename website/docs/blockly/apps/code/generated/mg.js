// This file was automatically generated from common.soy.
// Please don't edit this file by hand.

if (typeof apps == 'undefined') { var apps = {}; }


apps.messages = function(opt_data, opt_ignored, opt_ijData) {
  return '<div style="display: none"><span id="subtitle">Tontolo fanoratam-pandaharana ara-pijery</span><span id="blocklyMessage">Blockly</span><span id="codeTooltip">Hijery ny kaody JavaScript namboarina.</span><span id="linkTooltip">Hitahiry ary hampirohy amin\'ny bolongana.</span><span id="runTooltip">Handefa ny fandaharana voafaritry ny bolongana ao amin\'ny erana iasana.</span><span id="runProgram">Handefa ny fandaharana</span><span id="resetProgram">Averina</span><span id="dialogOk">OK</span><span id="dialogCancel">Aoka ihany</span><span id="catLogic">Lôjika</span><span id="catLoops">Tondro mifolaka</span><span id="catMath">Matematika</span><span id="catText">Soratra</span><span id="catLists">Lisitra</span><span id="catColour">Loko</span><span id="catVariables">Ova</span><span id="catProcedures">Paika</span><span id="httpRequestError">Nisy olana tamin\'ilay hataka.</span><span id="linkAlert">Zarao amin\'ity rohy ity ny bolonganao: \n\n%1</span><span id="hashError">Miala tsiny, tsy miady amin\'ny fandaharana notehirizina \'%1\'.</span><span id="xmlError">Tsy nahasokatra ny rakitra voatahirinao. Mety namboarina tamin\'ny versionan\'i Blockly hafa angamba ilay izy?</span><span id="listVariable">lisitra</span><span id="textVariable">soratra</span></div>';
};


apps.dialog = function(opt_data, opt_ignored, opt_ijData) {
  return '<div id="dialogShadow" class="dialogAnimate"></div><div id="dialogBorder"></div><div id="dialog"></div>';
};


apps.codeDialog = function(opt_data, opt_ignored, opt_ijData) {
  return '<div id="dialogCode" class="dialogHiddenContent"><pre id="containerCode"></pre>' + apps.ok(null, null, opt_ijData) + '</div>';
};


apps.storageDialog = function(opt_data, opt_ignored, opt_ijData) {
  return '<div id="dialogStorage" class="dialogHiddenContent"><div id="containerStorage"></div>' + apps.ok(null, null, opt_ijData) + '</div>';
};


apps.ok = function(opt_data, opt_ignored, opt_ijData) {
  return '<div class="farSide" style="padding: 1ex 3ex 0"><button class="secondary" onclick="BlocklyApps.hideDialog(true)">OK</button></div>';
};

;
// This file was automatically generated from template.soy.
// Please don't edit this file by hand.

if (typeof codepage == 'undefined') { var codepage = {}; }


codepage.messages = function(opt_data, opt_ignored, opt_ijData) {
  return apps.messages(null, null, opt_ijData) + '<div style="display: none"><span id="Code_badXml">Hadisoana tam-pamakiana ny XML:\n%1\n\nSafidio \'OK\' raha hamoy ny fiovana, na \'Aoka ihany\' raha mbola hitoy hanova ny XML.</span><span id="Code_badCode">Hadisoam-pandaharana:\n%1</span><span id="Code_timeout">Tafahoatra ny isa ambony indrindra ny isan\'ny fiverimberenana.</span><span id="Code_discard">Hamafa ny bolongana %1?</span></div>';
};


codepage.start = function(opt_data, opt_ignored, opt_ijData) {
  return codepage.messages(null, null, opt_ijData) + '<script type="text/javascript" src="../../blockly_compressed.js"><\/script><script type="text/javascript" src="../../blocks_compressed.js"><\/script><script type="text/javascript" src="../../javascript_compressed.js"><\/script><script type="text/javascript" src="../../python_compressed.js"><\/script><script type="text/javascript" src="../../dart_compressed.js"><\/script><script type="text/javascript" src="../../' + soy.$$escapeHtml(opt_ijData.langSrc) + '"><\/script><table width="100%" height="100%"><tr><td><h1><span id="title"><a href="../index.html?lang=' + soy.$$escapeHtml(opt_ijData.lang) + '">Blockly</a> : Kaody</span></h1></td><td class="farSide"><select id="languageMenu"></select></td></tr><tr><td colspan=2><table width="100%"><tr id="tabRow" height="1em"><td id="tab_blocks" class="tabon">Bolongana</td><td class="tabmin">&nbsp;</td><td id="tab_javascript" class="taboff">JavaScript</td><td class="tabmin">&nbsp;</td><td id="tab_python" class="taboff">Python</td><td class="tabmin">&nbsp;</td><td id="tab_dart" class="taboff">Dart</td><td class="tabmin">&nbsp;</td><td id="tab_xml" class="taboff">XML</td><td class="tabmax"><button id="trashButton" class="notext" title="Hanary ny bolongana rehetra."><img src=\'../../media/1x1.gif\' class="trash icon21"></button> <button id="linkButton" class="notext" title="Hitahiry ary hampirohy amin\'ny bolongana."><img src=\'../../media/1x1.gif\' class="link icon21"></button> <button id="runButton" class="notext primary" title="Handefa ny fandaharana voafaritry ny bolongana ao amin\'ny erana iasana."><img src=\'../../media/1x1.gif\' class="run icon21"></button></td></tr></table></td></tr><tr><td height="99%" colspan=2 id="content_area">' + codepage.toolbox(null, null, opt_ijData) + '</td></tr></table><div id="content_blocks" class="content"></div><pre id="content_javascript" class="content"></pre><pre id="content_python" class="content"></pre><pre id="content_dart" class="content"></pre><textarea id="content_xml" class="content" wrap="off"></textarea>' + apps.dialog(null, null, opt_ijData) + apps.storageDialog(null, null, opt_ijData);
};


codepage.toolbox = function(opt_data, opt_ignored, opt_ijData) {
  return '<xml id="toolbox" style="display: none"><category name="Lôjika"><block type="controls_if"></block><block type="logic_compare"></block><block type="logic_operation"></block><block type="logic_negate"></block><block type="logic_boolean"></block><block type="logic_null"></block><block type="logic_ternary"></block></category><category name="Tondro mifolaka"><block type="controls_repeat_ext"><value name="TIMES"><block type="math_number"><field name="NUM">10</field></block></value></block><block type="controls_whileUntil"></block><block type="controls_for"><value name="FROM"><block type="math_number"><field name="NUM">1</field></block></value><value name="TO"><block type="math_number"><field name="NUM">10</field></block></value><value name="BY"><block type="math_number"><field name="NUM">1</field></block></value></block><block type="controls_forEach"></block><block type="controls_flow_statements"></block></category><category name="Matematika"><block type="math_number"></block><block type="math_arithmetic"></block><block type="math_single"></block><block type="math_trig"></block><block type="math_constant"></block><block type="math_number_property"></block><block type="math_change"><value name="DELTA"><block type="math_number"><field name="NUM">1</field></block></value></block><block type="math_round"></block><block type="math_on_list"></block><block type="math_modulo"></block><block type="math_constrain"><value name="LOW"><block type="math_number"><field name="NUM">1</field></block></value><value name="HIGH"><block type="math_number"><field name="NUM">100</field></block></value></block><block type="math_random_int"><value name="FROM"><block type="math_number"><field name="NUM">1</field></block></value><value name="TO"><block type="math_number"><field name="NUM">100</field></block></value></block><block type="math_random_float"></block></category><category name="Soratra"><block type="text"></block><block type="text_join"></block><block type="text_append"><value name="TEXT"><block type="text"></block></value></block><block type="text_length"></block><block type="text_isEmpty"></block><block type="text_indexOf"><value name="VALUE"><block type="variables_get"><field name="VAR">soratra</field></block></value></block><block type="text_charAt"><value name="VALUE"><block type="variables_get"><field name="VAR">soratra</field></block></value></block><block type="text_getSubstring"><value name="STRING"><block type="variables_get"><field name="VAR">soratra</field></block></value></block><block type="text_changeCase"></block><block type="text_trim"></block><block type="text_print"></block><block type="text_prompt_ext"><value name="TEXT"><block type="text"></block></value></block></category><category name="Lisitra"><block type="lists_create_empty"></block><block type="lists_create_with"></block><block type="lists_repeat"><value name="NUM"><block type="math_number"><field name="NUM">5</field></block></value></block><block type="lists_length"></block><block type="lists_isEmpty"></block><block type="lists_indexOf"><value name="VALUE"><block type="variables_get"><field name="VAR">lisitra</field></block></value></block><block type="lists_getIndex"><value name="VALUE"><block type="variables_get"><field name="VAR">lisitra</field></block></value></block><block type="lists_setIndex"><value name="LIST"><block type="variables_get"><field name="VAR">lisitra</field></block></value></block><block type="lists_getSublist"><value name="LIST"><block type="variables_get"><field name="VAR">lisitra</field></block></value></block></category><category name="Loko"><block type="colour_picker"></block><block type="colour_random"></block><block type="colour_rgb"><value name="RED"><block type="math_number"><field name="NUM">100</field></block></value><value name="GREEN"><block type="math_number"><field name="NUM">50</field></block></value><value name="BLUE"><block type="math_number"><field name="NUM">0</field></block></value></block><block type="colour_blend"><value name="COLOUR1"><block type="colour_picker"><field name="COLOUR">#ff0000</field></block></value><value name="COLOUR2"><block type="colour_picker"><field name="COLOUR">#3333ff</field></block></value><value name="RATIO"><block type="math_number"><field name="NUM">0.5</field></block></value></block></category><category name="Ova" custom="VARIABLE"></category><category name="Paika" custom="PROCEDURE"></category></xml>';
};
