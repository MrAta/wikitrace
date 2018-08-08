import io
import sys
import argparse
import matplotlib
import datetime as dt
import itertools as it
matplotlib.use("Agg")

parser = argparse.ArgumentParser()
parser.add_argument("files", help="files to be analyzed in a comma seprated format")
parser.add_argument("final_name", help="final name for trace")

def get_key(d):
    # group by 1 minute
    d = dt.datetime.fromtimestamp(float(d))
    k = d - dt.timedelta(seconds=d.second % 60)
    return dt.datetime(k.year, k.month, k.day, k.hour, k.minute, k.second)

def get_data(f):
    data = open(f, "r").readlines()
    g = it.groupby(sorted([i.strip() for i in data]), key=get_key)
    datapoints = []
    for key, items in g:
        print(key, ":", len(list(items)))
        datapoints.append(len(list(items)))
        # for item in items:
        #     print('-', dt.datetime.fromtimestamp(float(item)).second)
    return datapoints
# import matplotlib.pyplot as plt
#
# plt.plot(datapoints[5:])
# plt.show()
def file_names():
    import re
    d = []
    with open("source.log" , "r") as f:
        for line in f.readlines():
            print(line)
            if re.search(r'href="wiki.(.*).gz"', line):
                d.append("wiki."+re.search(r'href="wiki.(.*).gz"', line).group(1)+".gz")
                # print("wiki."+re.search(r'href="wiki.(.*).gz"', line).group(1)+".gz")
    return d

def plot_data(datapoints, f):
    import matplotlib.pyplot as plt
    # fig = plt.figure()
    fig, ax = plt.subplots()
    plt.xlabel('Time(minute)')
    plt.ylabel('Reqs/min')
    plt.title('Request Arrival Rate')
    ax.plot(datapoints[2:])
    fig.savefig(f+'.png')


def concatenate_files(files, final_name,cp):
    for file_name in files:
        import subprocess
        from subprocess import call
        if cp:
            print("Decompressing " + file_name)
            call(["gunzip",file_name])
        print("Extracting timestamps...")
        p1 = subprocess.Popen(["cat", file_name[:-3]], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["awk", "{print $2}"], stdin=p1.stdout, stdout=subprocess.PIPE)
        p1.stdout.close()
        out, err = p2.communicate()
        with open(file_name[:-2]+"log" , "w") as f:
            f.write(out.decode("utf-8") )
        print("Done with "+file_name)
    with open(final_name, "a") as ht:
        for file_name in files:
            with open(file_name[:-2]+"log") as f:
                for line in f.readlines():
                    ht.write(line)
            os.remove(file_name[:-2]+"log")
    print("Concatenating Done!")

if __name__=="__main__":
    import os
    args = parser.parse_args()
    all_files = args.files.split(",")
    final_name = args.final_name
    print("Concatenating following files in to "+ final_name+":")
    for fl in all_files:
        print("-",fl)
    concatenate_files(all_files, final_name, cp=False)
    print("Calculating timestamps...")
    data = get_data(final_name)
    print("Plotting...")
    plot_data(data , final_name)
    print("Done")
