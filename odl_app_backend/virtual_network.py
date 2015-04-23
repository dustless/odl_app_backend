from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from functools import partial
from mininet.log import setLogLevel


class VirtualNetwork(object):
    instance = None
    def __init__(self):
        self.net = Mininet(controller=partial(RemoteController, ip='192.168.255.7', port=6633), switch=OVSSwitch)
        self.controller = self.net.addController('controller', port=6633)
        self.initialized = False

    def get_net(self):
        return self.net

    @staticmethod
    def get_instance():
        if VirtualNetwork.instance == None:
            VirtualNetwork.instance = VirtualNetwork()
        return VirtualNetwork.instance

    def init_topo(self):
        if self.initialized:
            return
        self.initialized = True
        print "*** Creating switches"
        s1 = self.net.addSwitch('s1')
        s2 = self.net.addSwitch('s2')
        s3 = self.net.addSwitch('s3')
        self.switch = s2

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
        #self.start_net()
        return s

    def remove_switch(self, name):
        print "*** Remove switch"
        print self.net.switches
        to_be_removed = []
        for index in range(len(self.net.links)):
            linkinfo = self.net.links[index].intf1.name.split('-')
            linkinfo.extend(self.net.links[index].intf2.name.split('-'))
            print "%s, %s, %s" % (self.net.links[index].intf1.name, self.net.links[index].intf2.name, linkinfo)
            if name in linkinfo:
                self.net.links[index].stop()
                to_be_removed.append(self.net.links[index])

        print "to_be_removed %s" % to_be_removed
        for index in range(len(to_be_removed)):
            print "index is %s, %s" % (index, to_be_removed[index])
            self.net.links.remove(to_be_removed[index])

        for index in range(len(self.net.switches)):
            if self.net.switches[index].name == name:
                self.net.switches[index].stop()
        self.net.switches = filter(lambda x:x.name != name, self.net.switches)
        print self.net.switches

    def add_host(self, name):
        print "*** Add host"
        host = self.net.addHost(name)
        #self.start_net()
        return host

    def remove_host(self, name):
        print "*** Remove host"
        print self.net.hosts
        to_be_removed = []
        for index in range(len(self.net.links)):
            linkinfo = self.net.links[index].intf1.name.split('-')
            linkinfo.extend(self.net.links[index].intf2.name.split('-'))
            print "%s, %s, %s" % (self.net.links[index].intf1.name, self.net.links[index].intf2.name, linkinfo)
            if name in linkinfo:
                print "remove link %s" % self.net.links[index]
                self.net.links[index].stop()
                to_be_removed.append(self.net.links[index])
        print "to_be_removed %s" % to_be_removed
        for index in range(len(to_be_removed)):
            print "index is %s, %s" % (index, to_be_removed[index])
            self.net.links.remove(to_be_removed[index])

        for index in range(len(self.net.hosts)):
            if self.net.hosts[index].name == name:
                print "remove host: %s" % self.net.hosts[index].name
                self.net.hosts[index].stop()
        print self.net.hosts
        self.net.hosts = filter(lambda x:x.name != name, self.net.hosts)
        print self.net.hosts

    def add_link(self, node1, node2):
        print "*** Add link"
        self.net.addLink(node1, node2)
        #self.start_net()

    def remove_link(self, node1, node2, port1, port2):
        print "*** Remove link"
        name = "%s-%s<->%s-%s" % (node1, port1, node2, port2)
        to_be_removed = []
        for index in range(len(self.net.links)):
            link_name = "%s<->%s" % (self.net.links[index].intf1.name, self.net.links[index].intf2.name)
            reverse_link_name = "%s<->%s" % (self.net.links[index].intf2.name, self.net.links[index].intf1.name)
            if name == link_name or name == reverse_link_name:
                self.net.links[index].stop()
                to_be_removed.append(self.net.links[index])
                break

        print "to_be_removed %s" % to_be_removed
        for index in range(len(to_be_removed)):
            print "index is %s, %s" % (index, to_be_removed[index])
            self.net.links.remove(to_be_removed[index])

    def ping_all(self):
        self.net.pingAll()

    def ping_between_hosts(self, node1, node2):
        hosts = [node1, node2]
        self.net.ping(hosts)

    def start_net(self):
        self.net.build()
        self.net.start()

