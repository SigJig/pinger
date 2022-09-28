
import re
import csv
import time
import subprocess
import matplotlib.pyplot as pyplot
from pathlib import Path

PATH = Path.cwd().joinpath('out.csv')

def ping():
    with open(PATH, 'w') as fp:
        writer = csv.writer(fp)

        while 1:
            try:
                out, err = subprocess.Popen(["ping", "-c", "5", "vg.no"],
                                            stderr=subprocess.PIPE,
                                            stdout=subprocess.PIPE).communicate()
                if err:
                    print(err)
                else:
                    groups = list(map(float, re.search(r'round-trip min/avg/max/stddev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)',
                                out.decode('utf-8')).groups()))

                    writer.writerow(groups + [time.time()])
                    print(groups)
            except KeyboardInterrupt:
                print('Interrupted')
                return

def main():
    ping()

    #pyplot.plot([1,2,3])
    #pyplot.show()

    with open(PATH) as fp:
        reader = csv.reader(fp)
        #rows = [float(x) for x in row for row in reader]

        maxs = []
        mins = []
        avgs = []
        times = []

        for row in reader:
            vals = [float(x) for x in row]
            mins.append(vals[0])
            avgs.append(vals[1])
            maxs.append(vals[2])
            times.append(vals[3])

        pyplot.plot(mins, label="min")
        pyplot.plot(avgs, label="avg")
        pyplot.plot(maxs, label="max")
        pyplot.show()


if __name__ == '__main__':
    main()
