import random
import sys
import numpy as np
from subprocess import Popen, PIPE
from multiprocessing import Process 
import sched
from mininetTopology import *
from commands import *
from handlers import *
from time import sleep, time
import sys

folder = sys.argv[1]
duration = int(sys.argv[2])
experiment = sys.argv[3]

class Connection:

    def __init__(self, _id, clientIP, serverIP, port):
        self.id = _id
        self.clientIP = clientIP
        self.serverIP = serverIP
        self.port = port
        self.filter = None

    def set_filter(self, _filter):
        self.filter = _filter
    

class RenoCubicExperiment:

    def __init__(self, client, server, runners):
        self.client = client
        self.server = server
        self.runners = runners
    
    def execute_connections(self, num_connections, time_each_connection, cong):
        
        connections = []
        start_port = 3555
        iperf_server_side(self.client, self.server, [start_port + i for i in range(num_connections)], self.runners)

        def start_connection(connection):

            iperf_client_side(i, self.client, self.server, connection.port, cong[connection.id],
                            duration - (time_each_connection * connection.id),
                            folder, experiment, delay=i*time_each_connection, runners=self.runners)

            filter_client_server = 'src {} and dst {} and dst port {}'.format(connection.clientIP, connection.serverIP, connection.port)
            filter_server_client = 'src {} and dst {} and src port {}'.format(connection.serverIP, connection.clientIP, connection.port)
            connection.set_filter('"({}) or ({})"'.format(filter_client_server, filter_server_client))

            connections.append(connection)

        s = sched.scheduler(time, sleep)
        for i in range(num_connections):
            connection = Connection(i, self.client.IP(), self.server.IP(), start_port + i)
            s.enter(i * time_each_connection, 1, start_connection, [connection])

        s.run()
        return connections

    def run_fig5_experiment(self, cong):
        thread = start_capture("{}/capture_{}.pcapng".format(folder,cong), folder)

        connections = self.execute_connections(1, 0, [cong])
        sleep(duration + 5)

        Popen("killall tcpdump", shell=True)
        thread.join()
        filter_capture(connections[0].filter, "{}/capture_{}.pcapng".format(folder, cong), "{}/connection_{}.pcapng".format(folder, cong), folder)

    def figure5(self):
        self.run_fig5_experiment('bbr')
        self.run_fig5_experiment('cubic')
        
    def figure_throughput(self):
        thread = start_capture("{}/capture_packets.pcapng".format(folder))

        num_connections = 5
        time_each_connection = 0
        cong = ['reno', 'cubic']
        connections = self.execute_connections(num_connections, time_each_connection, cong)

        sleep(duration + 15)

        Popen("killall tcpdump", shell=True)
        thread.join()

        for connection in connections:
            if connection.filter:
                filter_capture(connection.filter, "{}/capture_packets.pcapng".format(folder), "{}/connection{}.pcapng".format(folder, connection.id)) 

    def figure6(self):
        thread = start_capture("{}/capture_packets.pcapng".format(folder))

        num_connections = 5
        time_each_connection = 2
        cong = ['bbr' for x in range(num_connections)]
        connections = self.execute_connections(num_connections, time_each_connection, cong)

        sleep(duration + 15)

        Popen("killall tcpdump", shell=True)
        thread.join()

        for connection in connections:
            if connection.filter:
                filter_capture(connection.filter, "{}/capture_packets.pcapng".format(folder), "{}/connection{}.pcapng".format(folder, connection.id)) 


def launchExperiment():
    setLogLevel('info')

    if(experiment == 'figure5'):
        topo = BBRTopo(nodes=2, bandw_hosts=1000, bandw_btl=10, link_delay=40, max_q_size=210)
    
    elif(experiment == "figure6"):
        topo = BBRTopo(nodes=2, bandw_hosts=1000, bandw_btl=100, link_delay=7, max_q_size=3024)
    
    else:
        topo = BBRTopo(nodes=2, bandw_hosts=1000, bandw_btl=10, link_delay=20, max_q_size=175)

    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()

    instance_client = net.get('client')
    instance_server = net.get('server')
    
    runners = {}
    runners['client'] = runner(instance_client.popen)
    runners['server'] = runner(instance_server.popen)

    runners['client']("tc qdisc del dev client-eth0 root;")
    runners['client']("tc qdisc add dev client-eth0 root fq pacing;")
    runners['client']("sudo ethtool -K client-eth0 gso off tso off gro off;")

    runners['server']("tc qdisc del dev server-eth0 root;")
    runners['server']("tc qdisc add dev server-eth0 root fq pacing;")
    runners['server']("sudo ethtool -K server-eth0 gso off tso off gro off;")

    renocubicExperiment = RenoCubicExperiment(instance_client, instance_server, runners)

    if(experiment == 'figure_throughput'):
        renocubicExperiment.figure_throughput()
    
    elif(experiment == "figure6"):
        renocubicExperiment.figure6()

    net.stop()


launchExperiment()