from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from functools import partial
from mininet.log import setLogLevel


class VirtualNetwork(object):
    def __init__(self):
        self.net = Mininet(controller=partial(RemoteController, ip='192.168.255.7', port=6633), switch=OVSSwitch)
        self.controller = self.net.addController('controller', port=6633)

    def get_net(self):
        return self.net

    def init_topo(self):
        print "*** Creating switches"
        s1 = self.net.addSwitch('s1')
        s2 = self.net.addSwitch('s2')
        s3 = self.net.addSwitch('s3')

        print "*** Creating hosts"
        hosts1 = [self.net.addHost('h%d' % n) for n in 1, 2]
        hosts2 = [self.net.addHost('h%d' % n) for n in 3, 4]

        print "*** Creating links"
        for h in hosts1:
            self.net.addLink(s2, h)
        for h in hosts2:
            self.net.addLink(s3, h)
        self.net.addLink(s1, s2)
        self.net.addLink(s1, s3)

        print "*** Starting network"
        self.net.build()
        self.controller.start()
        s1.start([self.controller])
        s2.start([self.controller])
        s3.start([self.controller])

        print "*** Testing network"
        self.net.pingAll()

    def add_switch(self, name):
        print "*** Add switch"
        s = self.net.addSwitch(name)
        s.start([self.controller])
        return s

    def add_host(self, name):
        print "*** Add host"
        return self.net.addHost(name)

    def add_link(self, node1, node2):
        print "*** Add link"
        self.net.addLink(node1, node2)

    def ping_all(self):
        self.net.pingAll()

    def ping_between_hosts(self, node1, node2):
        hosts = [node1, node2]
        self.net.ping(hosts)
    
    def start_net(self):
        self.net.build()
        self.net.start()

if __name__ == '__main__':
    setLogLevel( 'info' )  # for CLI output
    topology = VirtualNetwork()
    topology.init_topo()
    s4 = topology.add_switch('s4')
    h5 = topology.add_host('h5')
    h6 = topology.add_host('h6')
    topology.add_link(s4, topology.switch)
    topology.add_link(s4, h5)
    topology.add_link(s4, h6)
    print topology.switch
    topology.start_net()
    
    s5 = topology.add_switch('s5')
    topology.add_link(s5, topology.get_net().get('s3'))
    h7 = topology.add_host('h7')
    h8 = topology.add_host('h8')
    topology.add_link(s5, h7)
    topology.add_link(s5, h8)
    topology.start_net()
    topology.ping_all()
    topology.ping_between_hosts(h5, h6)

