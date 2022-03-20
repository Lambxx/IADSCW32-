import math
from graph import *
import random
import itertools
import timeit
import time
import os

def eucliDeanGraphGenerator(filename,xmin,xmax,ymin,ymax,points):
    f = open(os.getcwd() + filename, "w")
    for i in range(0,points):
        randx = random.randint(xmin,xmax)
        randy = random.randint(ymin,ymax)
        f.write(" " + str(randx) + "  " + str(randy) + "\n")
    f.close()

def nonMetricGraphGenerator(filename,points,min,max):
    f = open(os.getcwd() + filename, "w")
    for i in range(0,points -1 ):
        for x in range(i,points - 1):
            if (i != x):
                randDist = random.randint(min,max)
                f.write( str(i) + " " + str(x) + " " + str(randDist) + "\n")

def evalTablePrinter():

    eucliDeanGraphGenerator("/Euclidean10",0,250,0,250,10)
    nonMetricGraphGenerator("/NonMetric10",11,10,5000)
    f = open(os.getcwd() + "/eval", "w")
    graphs = [[os.getcwd() + "/sixnodes",[6],'sixNodes'],[os.getcwd() + "/twelvenodes",[12],'twelveNodes'],[os.getcwd() + "/Euclidean10",[-1,10] ,'Euclidean10'],[os.getcwd() + "/NonMetric10",[10] ,'Non Metric 10 '],[os.getcwd() +"/xqf131",[-1,131],'xqf131',564]]
    for item in graphs:
        file = item[0]
        nodes = item[1][0]
        if nodes == -1:
            nodesFlag = -1
            nodes = item[1][1]
        else:
            nodesFlag = nodes
        name = item[2]
        half = nodes // 2
        #deafultHuersitcs = [[swapHeuristic(half),'swapHeuristic'],[swapHeuristic(nodes),'swapHeuristic']]
        f.write(name +  "\n")
        f.write("\n")
        currGraph = Graph(nodesFlag,file)
        f.write("Deafult tour value (permuatation for 0 - n): " + str(currGraph.tourValue()) + "\n")
        start = time.time()
        currGraph.swapHeuristic(half)
        timeTaken = ((time.time()- start)  )
        f.write('swapHeuristic k = n//2' + '  tourValue:' + str(currGraph.tourValue()) + ' time taken(s): ' + str(timeTaken) +"\n")

        currGraph1 = Graph(nodesFlag,file)
        start = time.time()
        currGraph1.swapHeuristic(nodes)
        timeTaken = ((time.time()- start)  )
        f.write('swapHeuristic k = n' + '  tourValue:' + str(currGraph1.tourValue()) + ' time taken(s): ' + str(timeTaken) +"\n")

        currGraph2 = Graph(nodesFlag,file)
        start = time.time()
        currGraph2.TwoOptHeuristic(half)
        timeTaken = ((time.time()- start)  )
        f.write('TwoOptHeuristic k = n // 2' + '  tourValue:' + str(currGraph2.tourValue()) + ' time taken(s): ' + str(timeTaken) +"\n")

        currGraph3 = Graph(nodesFlag,file)
        start = time.time()
        currGraph3.TwoOptHeuristic(nodes)
        timeTaken = ((time.time()- start)  )
        f.write('TwoOptHeuristic k = n ' + '  tourValue:' + str(currGraph3.tourValue()) + ' time taken(s): ' + str(timeTaken) +"\n")

        currGraph4 = Graph(nodesFlag,file)
        start = time.time()
        currGraph4.Greedy()
        timeTaken = ((time.time()- start)  )
        f.write('Greedy ' + '  tourValue:' + str(currGraph4.tourValue()) + ' time taken(s): ' + str(timeTaken) +"\n")

        currGraph5 = Graph(nodesFlag,file)
        start = time.time()
        currGraph5.swapHeuristic(nodes)
        currGraph5.TwoOptHeuristic(nodes)
        timeTaken = ((time.time()- start)  )
        f.write('swapHeuristic(n) then TwoOptHeuristic(n) ' + '  tourValue:' + str(currGraph5.tourValue()) + ' time taken(s): ' + str(timeTaken) +"\n")

        currGraph6 = Graph(nodesFlag,file)
        start = time.time()
        currGraph6.nearestInsertion()
        timeTaken = ((time.time()- start)  )
        f.write('nearestInsertion Huerstic ' + '  tourValue:' + str(currGraph6.tourValue()) + ' time taken(s): ' + str(timeTaken) +"\n")


        ### THIS SECTION IS SLOW IF ISSUES RUNNING PLEASE COMMENT OUT ###
        if(nodes <= 12):
            currGraph = Graph(nodesFlag,file)
            start = time.time()
            tourVal = superSlowMethod(currGraph)
            timeTaken = ((time.time()- start)  )
            f.write('Optimal soloution (my method )' + '  tourValue:' + str(tourVal) + ' time taken(s): ' + str(timeTaken) +"\n")
        else:
            knownOptimal = item[3]
            f.write('Optimal soloution (given not claculated )' + '  tourValue:' + str(knownOptimal) +"\n")
        ## END OF SECTION ###

def optimalSoloution(graph):
    # We start at 0
    currentNode = 0
    currentDistance = 0
    numVisitedSoFar = 0
    fullList = []
    for item in graph.perm:
        fullList.append([item,0]) # 0 indicates unvisited
    fullList[0][1] = 1
    return optimalRecursion(graph,numVisitedSoFar,currentNode,currentDistance,fullList)



def optimalRecursion(graph,numVisitedSoFar,currentNode,currentDistance,nodesLeft):
        funcCalls = []
        for item in nodesLeft:
            if item[0] == currentNode:
                item[1] = 1
        if (numVisitedSoFar == (graph.n -1)):
            currentDistance += graph.dists[currentNode][0]
            return currentDistance
        else:
            for nodesAndVisited in nodesLeft:
                if nodesAndVisited[1] == 0:
                    node = nodesAndVisited[0]
                    funcCalls.append(optimalRecursion(graph,(numVisitedSoFar + 1),node,(currentDistance + graph.dists[currentNode][node]),nodesLeft[1:]))
            return min(funcCalls)
def superSlowMethod(graph):
    perms = list (itertools.permutations(graph.perm[1:]))
    tourVals = []
    for lists in perms:
        tourVals.append(tourValueMod(([0] + list (lists) ), graph))
    return min(tourVals)


def tourValueMod(lists,graph):
    tourValue = 0
    for  i in range(0,graph.n - 1):
        tourValue += graph.dists[(lists[i])][(lists[i+1])]
    tourValue += graph.dists[(lists[i+1])][(lists[0])]
    return tourValue


def main():
    # Running this will create the required graphs and create an evaluation file with results
    # Due to the optimal soloution problem being solved it will take a few minutes to run
    # The eval function was run on a DICE machine with no problem however if you have issues testing the Code
    evalTablePrinter()

if __name__ == "__main__":
    main()
