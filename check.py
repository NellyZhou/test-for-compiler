import json;
from os import system, pipe, close, fdopen

def msg(s):
    print('\033[1m\033[91m' + s + '\033[0m\033[0m');
def err(data_in, s):
    msg("Wrong on input " + str(data_in) + "\n" + s)
    exit(1)

f_ir   = "./workdir/a.ir";
f_json = "./workdir/a.json";
program = "irsim/build/irsim"
irsim_in  = './workdir/irsim_in'
irsim_out = './workdir/irsim_out'

for data_in, data_out, ret_val in json.load(open(f_json)):
    with open(irsim_in, 'w') as to_irsim_w:
        for i in data_in:
            to_irsim_w.write(str(i) + '\n')

    ret = system("%s %s < %s > %s 2>/dev/null"%(program, f_ir , irsim_in , irsim_out))
    # Suppose irsim is compiled by run.sh
    if ret != 0:
        with open(irsim_out, 'r') as from_irsim_r:
            err(data_in,
                "runtime error occured when running your IR code\n"
                + from_irsim_r.read().splitlines()[-1]);
    with open(irsim_out, 'r') as from_irsim_r:
        from_irsim_r.readline()
        # Filter out the first line "load ./workdir/a.ir"
        try:
            for i in range(len(data_out)):
                expected = int(from_irsim_r.readline());
                if data_out[i] != expected:
                    err(data_in, "Output mismatch! expected %d, found %d at line %d" % (expected, data_out[i], i));
            else:
                if "ret with 0, reason 0\n" != from_irsim_r.readline():
                    err(data_in, "Output mismatch!(you output more than supposed?)")
                cnt = int(from_irsim_r.readline())
                with open("./workdir/count", "r") as f:
                    cnt = cnt + int(f.read())
                with open("./workdir/count", "w") as f:
                    f.write(str(cnt))
        except ValueError:
            err(data_in, "Output mismatch!(you output less than supposed?)")

exit(0);
