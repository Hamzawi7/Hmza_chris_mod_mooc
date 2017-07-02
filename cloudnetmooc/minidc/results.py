
import matplotlib.pyplot as plt
#import matplotlib.lines as mlines
import numpy as np
from datetime import datetime

def average(l):
    "returns average of a list of numbers"
    avg=(sum(l)/float(len(l)))
    avg=round(avg, 4)
    return avg

def graphing(static, adaptive, h, fname):
    "take raw data gathered as arguments"    

    for i in range(0, 3):

        avgStatic=[]
        avgAdaptive=[]
        if i == 0: 
            temp = 'none'
            plt.figure(1)
            fnames=fname+'-%s.png' % temp
            fnameNone=fnames
            title='No'
        elif i == 1: 
            temp = 'med'
            plt.figure(2)
            fnames=fname+'-%s.png' % temp
            fnameMed=fnames
            title='Medium'
        elif i == 2: 
            temp = 'high'
            plt.figure(3)
            fnames=fname+'-%s.png' % temp
            fnameHigh=fnames
            title='High'

        

        plt.subplot(111)
        "label axis"
        plt.ylabel('Ping(ms)')
        plt.xlabel('Hosts')
        "Give title"
        plt.title("Average ping times to hosts - %s load" % title)
        "insert hosts along x axis"
        plt.xticks(np.arange(len(h)),h)

        high=0
        for o in range(0,len(h)):

            s=average(static[temp]['times'][h[o]])
            a=average(adaptive[temp]['times'][h[o]])
            if s > high: high=s
            if a > high: high=a

            avgStatic.append(s)
            avgAdaptive.append(a)
        
        
        plt.ylim(0, high+round(float(high/3)))
        staticLine, =plt.plot(range(0,len(h)), avgStatic, 'ro-', label='Static Policy')
        adaptiveLine, =plt.plot(range(0,len(h)), avgAdaptive, 'go-', label='Adaptive Policy')
        plt.legend([staticLine, adaptiveLine], ['Static Policy', 'Adaptive Policy'])
        avgAvgStatic=[]
        avgAvgAdaptive=[]
        s=average(avgStatic)
        a=average(avgAdaptive)
        for i in range(0,len(h)):
            avgAvgStatic.append(s)
            avgAvgAdaptive.append(a)
        plt.plot(range(0, len(h)), avgAvgStatic, 'r--')
        plt.plot(range(0, len(h)), avgAvgAdaptive, 'g--')
        
        plt.savefig(fnames)
    return fnameNone, fnameMed, fnameHigh



def createHTML(figure1, figure2, hosts, it, hostNames):
    print "*** Generating Report"
    now=datetime.now()
    now=now.strftime('%Y_%m_%d-%H_%M_%S')
    fname='results-'+now
    f=open(fname+'.html', 'w+')
    f.write("<!doctype html>\n")
    f.write("<h1>Results - %s</h1>\n" % now)
    for i in range(0,2):
        if i==0: figure=figure1
        elif i==1: figure=figure2

        f.write("<p><b>%s</b></p>\n" % figure['name'])
        f.write("<table>\n")
        f.write("<tr><b><th>Host&nbsp;&nbsp;</th><th>No load&nbsp;&nbsp;&nbsp;     </th><th>Medium load&nbsp;&nbsp;</th><th>High Load     </th></b></tr>\n")
        for i in range(0, len(hosts)):
            f.write("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % ( hosts[i].name, 
                                                                                str(average(figure['none']['times'][hosts[i].name])),
                                                                                str(average(figure['med']['times'][hosts[i].name])), 
                                                                                str(average(figure['high']['times'][hosts[i].name])) ))
            f.write("\n")
        f.write("</table>\n")

        f.write("<p><b>Traffic stats</b></p>\n")
        for i in range(0,3):

            if i == 0: temp='none';
            elif i == 1: temp='med'
            elif i == 2: temp='high'
        
            f.write("<p><b>Load: %s</b></p>\n" % temp)

            pingsSec=round(it*len(hosts)/float(str(figure[temp]['timeTaken'])), 3)
            throughput=pingsSec*128
    
            f.write('<p>Packets Dropped: %s<br>\n' % str(len(figure[temp]['dropped'])))
            f.write('Time elapsed: %ss<br>\n' % str(figure[temp]['timeTaken']))
            f.write('Pings/second: %s<br>\n' % str(pingsSec))
            f.write('Throughput: %sB/s<br></p>\n' % str(throughput))

            if len(figure[temp]['dropped']) != 0:
                f.write("<p>Dropped pings:<br>\n")
                for i in range( 0, len(figure[temp]['dropped']) ):
                    f.write("ah2 -> %s<br>\n" % str(figure[temp]['dropped'][i]))
                f.write("</p>\n")

            f.write("<p>Times:<br>\n")
            for h in hosts:
                f.write("%s: %s<br>\n" % (str(h.name), (figure[temp]['times'][h.name])))
            f.write("</p>\n")

    fnameNone, fnameMed, fnameHigh = graphing(figure1, figure2, hostNames, fname)
    f.write('<p><b>Graphs</b></p>\n')
    f.write('<img src="%s"><br>\n' % fnameNone)
    f.write('<img src="%s"><br>\n' % fnameMed)
    f.write('<img src="%s"><br>\n' % fnameHigh)

    f.write("<p><b>Hardware + software info<b></p>")
    f.write('<img src="%s"><br>\n' % "hardware.png")
    

    print "*** Report created"

    f.close()    
        

def init(hostNames, hosts, static, adaptive, it):
    
    print "*** Results"
    
    createHTML(static, adaptive, hosts, it, hostNames)
    
