"""Custom topology example
Andrew Zhu, Alex Lew
"""

from mininet.topo import Topo
from mininet.log import setLogLevel
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import RemoteController

class MyTopo( Topo ):

    def __init__( self ):
        
        # Initialize topology
        Topo.__init__( self )

        # Add switches Level 3 Core
        sw1 = []
        sw1.append(self.addSwitch('s1_1'))
	sw1.append(self.addSwitch('s1_2'))

	        
        # Add switches Level 2 Aggregation
        sw2 = []
        sw2.append(self.addSwitch('s2_1'))
        sw2.append(self.addSwitch('s2_2'))
	sw2.append(self.addSwitch('s2_3'))
	sw2.append(self.addSwitch('s2_4'))


        # Add switches Level 1 Edge
        sw3 = []
        for i in range(1,14):
            sw3.append(self.addSwitch('s3_%d' % i))

        # Add hosts 
        hosts = []
        for i in range(1,101):
            hosts.append(self.addHost( 'h_%d' % i))

        print sw1
        print sw2
        print sw3
        print hosts
	
	
	# link cost
	linkCost=0
	
        # Add links L3 -- L3
        self.addLink( sw1[0], sw1[1], bw=1000 )
        linkCost += 15

        # Add links L3 -- L2
        self.addLink( sw1[0], sw2[0], bw=1000 )
        self.addLink( sw1[0], sw2[1], bw=1000 )
        self.addLink( sw1[1], sw2[2], bw=1000 )
        self.addLink( sw1[1], sw2[3], bw=1000 )
	linkCost += 60

        # Add links L2 -- L1 (13 links)
        for i in range(0,3):
            self.addLink( sw2[0], sw3[i], bw=100 )
	    linkCost+=1
	for i in range (3,6):
	    self.addLink( sw2[1], sw3[i], bw=100)
	    linkCost+=1
	
	for i in range (6,9):
	    self.addLink( sw2[2], sw3[i], bw=100)
            linkCost+=1

        for i in range(9,13):
            self.addLink( sw2[3], sw3[i], bw=100 )
	    linkCost+=1
       
        # Add links L1 -- hosts (96 links)
        for i in range(0,12):
            # each L3 switch have 8 fanout to connect hosts
            for j in range(8*i, 8*i+8):
                self.addLink( sw3[i], hosts[j], bw=100)
		linkCost+=1

        # Add links L1 -- hosts for last switch and 4 hosts (4 links)
        for j in range(96,100):
            self.addLink( sw3[12], hosts[j], bw=100)
	    linkCost+=1
	
	#How much cost is used 
	sw1Cost=len(sw1) 
	sw2Cost=len(sw2) 
  	sw3Cost= len(sw3) 
	switchCost = 300 * (sw1Cost+sw2Cost+sw3Cost) 
	dollarTotal = switchCost + linkCost
	print 'switch cost is ' + str(switchCost)
	print 'Link cost is ' + str(linkCost)
	print 'Total dollars spent is ' + str(dollarTotal)
	
topos = { 'mytopo': ( lambda: MyTopo() ) }


if __name__ == '__main__':
    setLogLevel('info')
    topo = MyTopo()
    net = Mininet(controller=RemoteController, topo=topo, link=TCLink, autoSetMacs=True, autoStaticArp=True)
    net.start()
    CLI(net)
    net.stop()

