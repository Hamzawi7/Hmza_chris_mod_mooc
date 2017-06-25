
#!/usr/bin/env python

"""
FattreeTopology: creates a simple fattree topology with N edge switches
    connected to N-1 core switches.  Each edge switch connects to 2 hosts.
"""

from mininet.node import CPULimitedHost
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.log import setLogLevel, info
from mininet.node import RemoteController
from mininet.cli import CLI
from mininet.link import TCLink
from subprocess import *
import os

class FatTreeTopology(Topo):

    def build(self, Topo):
        self.numES=3
        self.hostsPerEdge=2
        self.numHosts=self.numES*self.hostsPerEdge
        #self.numCS = self.numES-1
        self.numCS=1
        self.hostIds = range(1, self.numHosts+1)
        self.firstSwitch= max(101, self.numHosts+1)
        self.edgeIds = range(self.firstSwitch, self.numES + self.firstSwitch)
        self.coreIds = range(self.numES + self.firstSwitch,
                            self.numES + self.firstSwitch + self.numCS)        
        self.connect()
        
    def connect(self):

        self.edge=[]
        self.core=[]
        host=[]
        links=[]
        
        for s in self.coreIds:
            node=self.addSwitch('cs%s' % s, protocol="OpenFlow13")
            self.core.append(node)

        for s in self.edgeIds:
            node = self.addSwitch('es%s' % s, protocol="OpenFlow13")
            self.edge.append(node)

        for i in range(0, len(self.core)):
            for x in range(0,len(self.edge)):
                #if self.core[i]=="cs105":continue
                self.addLink( self.core[i], self.edge[x] )
                links.append(self.core[i]+" <-> "+self.edge[x])
        
        for i, h in enumerate(self.hostIds):
            node=self.addHost('h%s' % h)
            host.append(node)

        s=0

        while s <=  self.numHosts:
            if s > self.numES:
                print "error - s out of range " + str(s)
                break
            for h in range(s*self.hostsPerEdge, (s*self.hostsPerEdge)+self.hostsPerEdge):
                if h >= len(host):
                    break
                else:
                    self.addLink( self.edge[s], host[h] )
                    links.append(self.edge[s]+" <-> "+host[h])
            s+=1
        
        for i in range(0,len(links)):
            print links[i]

    def createBridges(self):
        for s in range(0,len(self.core)):
            print "creating bridge for %s..." % self.core[s]
            cmd =  "sudo ovs-vsctl set bridge %s protocols=OpenFlow13" % self.core[s]
            print os.system(cmd)
        for s in range(0,len(self.edge)):
            print "creating bridge for %s..." % self.edge[s]
            cmd =  "sudo ovs-vsctl set bridge %s protocols=OpenFlow13" % self.edge[s]
            os.system(cmd)
            
def runTest(topo):
    ip="127.0.0.1"
    c = RemoteController("c", ip, 6633)
    setLogLevel('info')
    net = Mininet(topo, host=CPULimitedHost, link=TCLink)
    net.addController(c)
    net.build()
    #topo.createBridges()

    #net.pingAll()
    
    CLI(net)
    net.stop()

topo=FatTreeTopology(Topo)
print topo
runTest(topo)