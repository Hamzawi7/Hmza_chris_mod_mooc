
import matplotlib.pyplot as plt
import numpy as np


def average(l):
    avg=(sum(l)/float(len(l)))
    avg=round(avg, 4)
    return avg

def graphing(YesLoad, h):
    "take raw data gathered as arguments"    

    "create figure and plot"
    plt.figure(1)
    plt.subplot(111)

    "label axis"
    plt.ylabel('Ping(ms)')
    plt.xlabel('Hosts')
    plt.ylim(0,2500)
    "Give title"
    plt.title("yoyoyooyoyoyooyooooooo")
    
    "insert hosts along x axis"
    plt.xticks(np.arange(len(h)),h)

    avg=[]
    for o in range(0,len(h)):
        avg.append(average(YesLoad[h[o]]))
        
    plt.plot(range(0,len(h)), avg, 'o-')
    

    "show graph"
    plt.show()

def temp():
    YesLoad={'h1':[1.5,2,1.88,1.334],'h2':[1.5,2,1.88,1.334],'h3':[1.5,2,1.88,1.334],'h4':[1.5,2,1.88,1.334]}
    h=['h1','h2','h3','h4']
    graphing(YesLoad, h)
