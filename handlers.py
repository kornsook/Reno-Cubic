import random
import sys
import numpy as np
from subprocess import Popen, PIPE
from multiprocessing import Process 
import sched
from mininetTopology import *
from time import sleep, time
import sys


def capture_packets(options="",fname="capture_packets.pcapng", folder='./'):
    if(fname == "capture_packets.pcapng"):
        fname = '%s/{}'.format(fname) % folder
    cmd = "tcpdump -w {} {}".format(fname, options)
    return Popen(cmd, shell=True).wait()

def filter_capture(filt, infile="capture_packets.pcapng", outfile="filter_packets.pcapng", folder="./"):
    handler = Process(target=capture_packets, args=("-r {} {}".format(infile, filt), outfile, folder))
    handler.start()
    return handler

def start_capture(outfile="capture_packets.pcapng", folder='./'):
    handler = Process(target=capture_packets, args=("", outfile, folder))
    handler.start()
    return handler