from utils import *
import matplotlib.pyplot as plt
import matplotlib as m
from pylab import figure
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--files', '-f',
                    help="Throughput timeseries output to one plot",
                    required=True,
                    action="store",
                    nargs='+',
                    dest="files")

parser.add_argument('--out', '-o',
                    help="Output png file for the plot.",
                    default=None, # Will show the plot
                    dest="out")

parser.add_argument('--duration',
                    help="Upper limit of x axis, data after ignored",
                    type=float,
                    default=50)


args = parser.parse_args()
files = args.files
duration = args.duration
output_dir = args.out

legend = []
connection = 0
for file in files:
    legend.append("Connection number {}".format(connection))
    connection += 1

def get_style(i):
    if i == 0:
        return {'color': 'red'}
    else i == 1:
        return {'color': 'blue'}

m.rc('figure', figsize=(34, 12))
fig = figure()
ax = fig.add_subplot(111)
time_btwn_flows = 2.0
for i, f in enumerate(sorted(files)):
    data = read_list(f)
    data = list(map(list, data))

    times = [float(x[0]) for x in data]
    throughput =[float(x[1]) for x in data]
    
    throughput = [t for j, t in enumerate(throughput) if times[j] <= duration]
    times = [x for x in times if x <= duration]

    ax.plot(times, throughput, label=legend[i], **get_style(i))

plt.legend()
    
plt.ylabel("Throughput (Mbits)")
plt.xlabel("Seconds")

print('saving to', output_dir)
plt.savefig(output_dir)
