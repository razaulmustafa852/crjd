#!/usr/bin/python                                                                            
                                                                                             
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import dumpNodeConnections
from mininet.log import setLogLevel
from mininet.cli import CLI
from threading import Thread
import multiprocessing
from multiprocessing import Process
from mininet.node import Node,Controller, OVSKernelSwitch, RemoteController
import os
from argparse import ArgumentParser
import os
import datetime
from subprocess import Popen
#from urls.mpdURL import *
from random import randint


class SingleSwitchTopo( Topo ):

    def build( self, n,bandwidth, delay, packetloss ):
    # define the name of the directory to be created
	pathpcaps = "p/"+str(bandwidth)+ '_' + str(delay)+ '_' + str(packetloss)+ '_' + str(n)
	pathdash  = "d/"+str(bandwidth)+ '_' + str(delay)+ '_' + str(packetloss)+ '_' + str(n)
	try:  
            os.mkdir(pathpcaps)
            os.chmod(pathpcaps,0o777)
            os.mkdir(pathdash)
            os.chmod(pathdash,0o777)
	except OSError:  
    	    print ("Creation of the directory %s failed" % pathpcaps)
	else:  
    	    print ("Successfully created the directory %s " % pathpcaps)
	s1 = self.addSwitch( 's1' )
	for h in range(n):
	    
	    host = self.addHost( 'h%s' % (h + 1))

	    self.addLink( host, s1 )
        h101 = self.addHost( 'h101',  ip='10.0.0.101')
       
        if packetloss > 0 and delay > 0:
            self.addLink(h101, s1, bw=bandwidth, delay=str(delay)+'ms', loss=packetloss )
        elif delay > 0 and packetloss == 0:
            self.addLink(h101, s1, bw=bandwidth, delay=str(delay)+'ms')
        elif packetloss > 0 and delay == 0:
            self.addLink(h101, s1, bw=bandwidth, loss=packetloss)
        else:
            self.addLink(h101, s1, bw=bandwidth)                  
### capture pacp 
def cap(val,bandwidth, delay, packetloss,h):
    os.system('sudo tcpdump -i s1-eth' + str(val) + ' -w  p/'+str(bandwidth)+ '_' + str(delay)+ '_' + str(packetloss)+ '_' + str(h)+'/s1-eth' + str(val)+ '_' + str(bandwidth)+ '_' + str(delay)+ '_' + str(packetloss)+ '_' + str(h))
    


def dashcf(num,h,bandwidth, delay, packetloss,h1):

    cwd = os.getcwd()
    print num.cmd('./goDASH --config ../config/configure.json > d/'+str(bandwidth)+ '_' + str(delay)+ '_' + str(packetloss)+ '_' + str(h1)+'/user_' + str(num)+ '_' +str(bandwidth) +'_'+ str(delay)+ '_' + str(packetloss)+ '_' + str(h1)+'.txt')




def simpleTest(h,bandwidth, delay, packetloss):
    "Create and test a simple network"
    topo = SingleSwitchTopo( h,bandwidth, delay, packetloss)

    net  = Mininet(topo=topo, host=CPULimitedHost,  link=TCLink)
    net.start()
    CLI(net)
    nodes=[]
    for m1 in net.hosts:
     nodes.insert(h, m1)	
    s=net.get('s1')
    return nodes, s
    
    #net.stop()
if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    h 			= int(input("How many Hosts :  "))
    bandwidth 		= int(input("Bandwidth : "))
    delay 		= int(input("Delay : "))
    packetloss 		= int(input("Loss : "))

    l,s= simpleTest(h,bandwidth, delay, packetloss)
    tcpdDump = []
    dashC    = []
    a = 1
    b = 0
    #print l[1]
   
    if a==1:
     for i in range(h+1):
      p = Process(target=cap,args=(i+1, bandwidth, delay, packetloss,h))       
      
      p.start()
     
      b=1 

    if b==1:
     print 'goDash'
     for k in range(h):
     #print 'value is ',l[k] 
      q = Process(target=dashcf, args=(l[k],k+1,bandwidth, delay, packetloss,h))  ## run dashc for multiple user
      dashC.append(q)
      q.start()
  

