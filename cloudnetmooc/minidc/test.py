
from mininet.node import Host
import minidc.results as results
import time
import random


def initIperfServer(net, h, targ):
    
    print "*** Initilizing iPerf server on h4"
    "Get h4 object and run an iperf server"
    target = net.get(targ)
    perfServer="iperf -s -u -p 7890 &"
    print "\t%s" % perfServer
    target.cmd(perfServer)


def launchAttack(net, h, load, targ, strength):

    "Get objects"
    target=net.get(targ)
    ah1 = net.get("ah1")
    print "*** Launching Attack"

    "medium or high load"
    if strength == "high":
        perf=("iperf -t 9999 -c %s -p 7890 -b %s &" % (target.IP(), load))
    elif strength == "med":
        load="4800K"
        perf=("iperf -t 9999 -c %s -p 7890 -b %s &" % (target.IP(), load))
    
    "Launch attack against target"
    print "\t%s" % perf
    ah1.cmd(perf)

def stopJobs(net, h):

    print "*** Stopping Jobs"

    "kill all jobs on each host"
    for i in range(0,len(h)):
        h[i].cmd("jobs -p | xargs kill")

    ah1=net.get("ah1")
    ah2=net.get("ah2")
    ah1.cmd("jobs -p | xargs kill")
    ah2.cmd("jobs -p | xargs kill")

def pingTest(net, h, it):
    
    print "*** Testing Ping"
    ah2=net.get("ah2")

    "Create dictionary of hosts"
    pingList={}
    for i in range(0, len(h)):
        pingList[h[i].name]=[]

    p1=time.time()
    "ah2 takes turns pinging each host, appends time(ms) to dictionary. Repeat 50 times for good average."
    dropped=[]
    for i in range(0, it):
        "create list of possible choises of hosts"
        pos=[]
        for y in range(0, len(h)):
            pos.append(y)
        for x in range(0,len(h)):
            
            "pseudo random ping targets - Each round different order."
            target=random.choice(pos)
            "remove when used, cant be targetted again this round."
            pos.remove(target)
            "Ping target host"
            temp1=ah2.cmd("ping %s -c 1 -W 10" % h[target].IP())
            temp=temp1.split("/")

            "don't use results of first round"
            if i == 0:
                continue
            else:
                "append ping time between hosts or record dropped packet."
                try:
                    pingList[h[target].name].append(float(temp[4]))
                except:
                    "Add dropped packets"
                    #print "\t\tDropped packet ah2 -> %s" % h[target].name
                    dropped.append(h[target].name)
                    
        print "\tRun: %s complete" % str(i+1) 
    p2=time.time()
    return pingList, dropped, round(p2-p1,3)

def run(net, h, targ, strength, it, pol, load, wait):
    
    if strength == "none":
        times, dropped, timeTaken =pingTest(net, h, it)
        print "*** Load test completed - %s, %s" % (strength, pol)
        time.sleep(wait/4)
        return times, dropped, timeTaken

    "initilize iperf server"
    initIperfServer(net, h, targ)

    "perform ping test whilst under load"
    launchAttack(net, h, load, targ, strength)

    "wait for traffic to build up"
    print "*** Waiting for traffic"    
    time.sleep(wait)
    
    "perform tests"
    times, dropped, timeTaken=pingTest(net, h, it)
    print "*** Load test completed - %s, %s" % (strength, pol)
    
    "stop jobs"
    stopJobs(net, h)
    
    "wait for traffic to die down"
    time.sleep(wait)

    return times, dropped, timeTaken


def start(net, topo):
    
    "arguments for controlling tests"
    it=30
    wait=20
    load="5M"
    targ="h4"
    
    "create list of passive hosts"
    h=[]
    for host in net.hosts:
        if host.name != "ah1":
            if host.name != "ah2":
                h.append(host)
    

    static={}
    static['name']="Static"
    static['none']={}
    static['med']={}
    static['high']={}

    adaptive={}
    adaptive['name']="Adaptive"
    adaptive['none']={}
    adaptive['med']={}
    adaptive['high']={}

    print "*** Start static policy on controller <ENTER>"
    raw_input()
    pol="static"

    static['none']['times'], static['none']['dropped'], static['none']['timeTaken'] = run(net, h, targ, "none", it, pol, load, wait)
    static['med']['times'], static['med']['dropped'], static['med']['timeTaken'] = run(net, h, targ, "med", it, pol, load, wait)
    static['high']['times'], static['high']['dropped'], static['high']['timeTaken']  = run(net, h, targ, "high", it, pol, load, wait)
    
    print "*** Static policy tests finished"
    time.sleep(wait/4)
    print "*** Start adaptive policy on controller <ENTER>"
    raw_input()
    pol="adaptive"

    adaptive['none']['times'], adaptive['none']['dropped'], adaptive['none']['timeTaken'] = run(net, h, targ, "none", it, pol, load, wait)
    adaptive['med']['times'], adaptive['med']['dropped'], adaptive['med']['timeTaken'] = run(net, h, targ, "med", it, pol, load, wait)
    adaptive['high']['times'], adaptive['high']['dropped'], adaptive['high']['timeTaken'] = run(net, h, targ, "high", it, pol, load, wait)
    print "*** Adaptive policy tests finished"

    "make list of host names"
    x=[]
    for i in range(0,len(h)):
        x.append(h[i].name)
    
    results.init(x, h, static, adaptive, it)
