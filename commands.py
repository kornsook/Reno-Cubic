import random
import sys
import numpy as np
from subprocess import Popen, PIPE
from multiprocessing import Process 
import sched
from mininetTopology import *
from time import sleep, time
import sys

def runner(popen):
    def execute_command(command, background=False, daemon=True):
        def initial_command():
            popen(command, shell=True).wait()
        process = Process(target=initial_command)
        process.daemon = daemon
        process.start()
        if not background:
            process.join()
        return process
    return execute_command

def iperf_server_side(client, server, ports, runners):
    server.popen("killall iperf3", shell=True).wait()
    sleep(1)
    for port in ports:
        cmd = "iperf3 -s -p {} -f m -i 1 -1".format(port)
        runners['server'](cmd, background=True)
    sleep(min(10, len(ports)))

def iperf_client_side(index, client, server, port, cong, duration, outdir, experiment, delay=0, runners={}):
    cmd = "iperf3 -c {} -f m -i 1 -p {} {} -C {} -t {} > {}".format(
        server.IP(), port, '', cong, duration, "{}/iperf{}.txt".format(outdir, index)
    )
    runners['client'](cmd, background=True)