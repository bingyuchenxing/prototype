#!/usr/bin/python

#import cgitb
#cgitb.enable()

import json
import sys
from filelock import FileLock

raw_stdin = sys.stdin.read()
myjson = json.loads(raw_stdin)

python_code = myjson["repr"]["code"]

results = {}

myjson = json.dumps(myjson )

if myjson != "''":
    with FileLock("../upload/highest.lock", timeout=2) as lock:
        f = open("../upload/highest")
        r = f.read()
        r = r.strip()
        top_id = int(r)
        f.close()
        top_id += 1
        f = open("../upload/highest","w")
        f.write(str(top_id))
        f.close()
        f = open("../upload/" + str(top_id) + ".json", "w")
        data = { "myjson": myjson, "id": top_id }
        f.write(json.dumps(data))
        f.flush()
        f.close()

        f = open("../python_pending/" + str(top_id) + ".py", "w")
        f.write(str(python_code))
        f.flush()
        f.close()

else:
    myjson = "No data uploaded"
    top_id = ""

result = { "id" : top_id }

print "Content-type: application/json"
print "Length:", len(result)
print
print json.dumps(result)

"""

>>> import json
>>> f = open("../upload/71.json").read()
>>> j = json.loads(f)
>>> mj = json.loads(j["myjson"])

python_code = mj["repr"]["code"]


"""


