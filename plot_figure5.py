from utils import *
import matplotlib.pyplot as plt
import matplotlib as m
from pylab import figure
import sys

bbr_file = sys.argv[1]
cubic_file = sys.argv[2]
files = [bbr_file, cubic_file]

duration = float(sys.argv[3])
output_dir = sys.argv[4]

m.rc('figure', figsize=(30, 12))
fig = figure()
ax = fig.add_subplot(111)
for i, f in enumerate(files):
    data = read_list(f)
    data = list(map(list, data))
    
    times = [float(x[0]) for x in data]
    rtts =[float(x[1]) for x in data]

    times = [x - times[0] for x in times]
    rtts = [r * 1000 for j, r in enumerate(rtts) if times[j] <= duration]
    times = [x for x in times if x <= duration]

    if(i == 0):
	    name = "bbr"
    else:
	    name = "cubic"

    ax.plot(times, rtts, label=name)
    plt.legend()

plt.ylabel("RTT (ms)")
plt.xlabel("Seconds")
plt.grid(True)

plt.savefig(output_dir)
