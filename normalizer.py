import io
import sys
import random
import argparse
import matplotlib
import datetime as dt
import itertools as it

def get_key(d):
    # group by 1 minute
    d = dt.datetime.fromtimestamp(float(d))
    k = d - dt.timedelta(seconds=d.second % 60)
    return dt.datetime(k.year, k.month, k.day, k.hour, k.minute, k.second)

def normizer(fin,fout, factor):
    data = open(fin, "r").readlines()
    g = it.groupby(sorted([i.split()[1].strip() for i in data]), key=get_key)
    timestamps = []
    for key, items in g:
        _i = list(items)
        ch = int(len(_i)*factor)
        timestamps += random.sample(_i,ch )

    print(len(timestamps))
    lines = [ line for line in data if line.split()[1].strip() in timestamps ]
    with open(fout, "w") as f:
        for line in lines:
            f.write(line)




if __name__=="__main__":
    fin = sys.argv[1]
    fout = sys.argv[2]
    factor = float(sys.argv[3])
    normizer(fin,fout,factor)
