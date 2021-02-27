import argparse
import time
import os
from mininet.topo import Topo
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.net import Mininet
from mininet.log import lg, info
from mininet.util import dumpNodeConnections
from mininet.cli import CLI
from mininet.node import OVSController
from mininet.log import setLogLevel


class BBRTopo(Topo):
    
    def __init__(self, nodes=2, bandw_hosts=1000, bandw_btl=10, link_delay=20, max_q_size=175, **opts):
        Topo.__init__(self, **opts)
        self.buildTopo(nodes,bandw_hosts, bandw_btl, link_delay, max_q_size)
    
    def buildTopo(self, nodes=2, bandw_hosts=1000, bandw_btl=10, link_delay=20, max_q_size=175):

        client = self.addHost('client')
        server = self.addHost('server')
        switch = self.addSwitch('s0')

        link1 = self.addLink(client, switch, bw=bandw_hosts)
        link2 = self.addLink(server, switch, bw=bandw_btl, delay=str(link_delay) + 'ms', max_queue_size=max_q_size)
        return

        

if __name__ == '__main__':
    setLogLevel('info')
    topo = BBRTopo()
    
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()
    dumpNodeConnections(net.hosts)
    net.pingAll()
    net.stop()