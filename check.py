#!/bin/python
import json;
import re;

def msg(s):
    print('\033[1m\033[91m' + s + '\033[0m\033[0m');

f_out = "./workdir/a.out";
f_json = "./workdir/a.json";
pattern = re.compile(r"Error type (\d+) at Line (\d+): .*\.");

ref_list = json.load(open(f_json));
out = open(f_out);

require = {};
allow = {};

if "require" in ref_list:
    for x, y in ref_list["require"]:
        require[(x, y)] = 0;

if "allow" in ref_list:
    for x, y in ref_list["allow"]:
        allow[(x, y)] = True;

while True:
    l = out.readline();
    if(l == ""):
        break;

    m = pattern.match(l);
    if(not m):
        msg("Wrong output format!")
        exit(1);
    x, y = m.groups();
    pos = (int(x), int(y))

    if pos in require:
        require[pos] = 1;
    elif pos in allow:
        pass;
    else:
        exit(1);

exit(0);
