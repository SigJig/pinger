
import re
import csv
import sys
import time
import subprocess
import matplotlib.pyplot as pyplot
from pathlib import Path

PATH = Path.cwd().joinpath('out.csv')
FORMAT = 'round-trip min/avg/max/stddev'

if sys.platform in ("linux", "linux2"):
    FORMAT = 'rtt min/avg/max/mdev'

def ping(path):
    with open(path, 'w') as fp:
        writer = csv.writer(fp)

        while 1:
            try:
                out, err = subprocess.Popen(["ping", "-c", "5", "vg.no"],
                                            stderr=subprocess.PIPE,
                                            stdout=subprocess.PIPE).communicate()
                if err:
                    print(err)
                    continue

                search = re.search(re.compile(f'{FORMAT} = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)'),
                            out.decode('utf-8'))

                if search is None:
                    print('Search is none')
                    continue

                groups = list(map(float, search.groups()))

                writer.writerow(groups + [time.time()])
                print(groups)

            except KeyboardInterrupt:
                print('Interrupted')
                return

def show(path):
    with open(path) as fp:
        reader = csv.reader(fp)
        plots = ([],[],[],[])

        for row in reader:
            vals = [float(x) for x in row]

            for i in range(4):
                plots[i].append(vals[i])

        for idx, label in enumerate(("min", "avg", "max")):
            pyplot.plot(plots[idx], label=label)

        pyplot.show()

def main(**kwargs):
    file = kwargs.pop('file', PATH)

    if 'p' in kwargs:
        ping(file)
    show(file)

if __name__ == '__main__':
    args = (x for x in sys.argv[1:])
    kwargs = {}

    for arg in args:
        if arg.startswith('--'):
            kwargs[arg.lstrip('-')] = next(args)
        elif arg.startswith('-'):
            kwargs[arg.lstrip('-')] = None

    main(**kwargs)

