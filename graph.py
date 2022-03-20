import math
import random
import os # JUST FOR TESTING REMOVE


def euclid(p,q):
    x = p[0]-q[0]
    y = p[1]-q[1]
    return math.sqrt(x*x+y*y)

class Graph:

    # Complete as described in the specification, taking care of two cases:
    # the -1 case, where we read points in the Euclidean plane, and
    # the n>0 case, where we read a general graph in a different format.
    # self.perm, self.dists, self.n are the key variables to be set up.
    def __init__(self,n,filename):
            self.dists = []
            file = open(filename, 'r')
            allLines = file.readlines()
            points = []
            if n == - 1 :
                lineCount= 0
                for line in allLines:
                    lineSplit = line.split()
                    points.append([int(lineSplit[0]),int(lineSplit[1])])
                    lineCount += 1
                self.n = lineCount
                for pointi in points:
                    listFori = []
                    for otherPoints in points:
                        currDist = euclid(pointi,otherPoints)
                        listFori.append(currDist)
                    self.dists.append(listFori)
            else :
                    self.n = n
                    for line in allLines:
                        lineSplit = line.split()
                        points.append([int(lineSplit[0]),int(lineSplit[1]),int(lineSplit[2])])
                        currList = []
                        #Initialise array with 0 values
                        for i in range(0,n):
                            currList = []
                            for j in range(0,n):
                                currList.append(j)
                            self.dists.append(currList)
                        for pointi in points:
                            self.dists[(pointi[0])][(pointi[1])] = pointi[2]
                            self.dists[(pointi[1])][(pointi[0])] = pointi[2]
            self.perm = []
            for i in range(0,self.n):
                 self.perm.append(i)




# N = -1 case 1 Points are lines of a file in format
 #376  231
 #401  440
 #289  294
 # We need to create an adjecny matrix of points

    # Complete as described in the spec, to calculate the cost of the
    # current tour (as represented by self.perm).
    def tourValue(self):
        tourValue = 0
        for  i in range(0,self.n - 1):
            tourValue += self.dists[(self.perm[i])][(self.perm[i+1])]
        tourValue += self.dists[(self.perm[i+1])][(self.perm[0])]
        return tourValue
    # Attempt the swap of cities i and i+1 in self.perm and commit
    # commit to the swap if it improves the cost of the tour.
    # Return True/False depending on success.
    def trySwap(self,i):
        val1 = self.tourValue()
        temp = self.perm[i]
        self.perm[i] = self.perm[(i+1) % self.n]
        self.perm[(i+1) % self.n] = temp
        val2 = self.tourValue()
        if val2 < val1:
            return True
        else:
            temp = self.perm[i]
            self.perm[i] = self.perm[(i+1) % self.n]
            self.perm[(i+1) % self.n] = temp
            return False






    # Consider the effect of reversiing the segment between
    # self.perm[i] and self.perm[j], and commit to the reversal
    # if it improves the tour value.
    # Return True/False depending on success.
    def tryReverse(self,i,j):
                val1 = self.tourValue()
                self.perm[i:j+1] = self.perm[i:j+1][::-1]
                val2 = self.tourValue()
                if val2 < val1:
                    return True
                else:
                    self.perm[i:j+1] = self.perm[i:j+1][::-1]
                    return False


    def swapHeuristic(self,k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for i in range(self.n):
                if self.trySwap(i):
                    better = True

    def TwoOptHeuristic(self,k):
        better = True
        count = 0
        while better and (count < k or k == -1):
            better = False
            count += 1
            for j in range(self.n-1):
                for i in range(j):
                    if self.tryReverse(i,j):
                        better = True


    # Implement the Greedy heuristic which builds a tour starting
    # from node 0, taking the closest (unused) node as 'next'
    # each time.
    def Greedy(self):
        fullList = []
        for item in self.perm:
            fullList.append(item)
        fullList.remove(0)
        current = 0
        i = 0
        while i < self.n - 1:
            lowest = None
            i = i + 1
            for potential in fullList:
                if potential != current:
                    if lowest == None:
                         lowest = self.dists[current][potential]
                         bestPotential = potential

                    else:
                        if (self.dists[current][potential] < lowest):
                            lowest = self.dists[current][potential]
                            bestPotential = potential
            current = bestPotential
            self.perm[i] = bestPotential
            fullList.remove(bestPotential)

    def nearestInsertion(self):
        lowest = None
        val = None
        subTour = [0]
        remainingChoices = []
        for item in self.perm:
            remainingChoices.append(item)
        remainingChoices.remove(0)
        for i in range(0,self.n):
            if i == 1 :
                lowest = self.dists[0][i]
                val = 1
            else:
                if self.dists[0][i] < lowest :
                    lowest = self.dists[0][i]
                    val = i
        subTour.append(i)
        remainingChoices.remove(i)
        while len(subTour) < len(self.perm):
            currentSelection = remainingChoices[0]
            for nodeInSub in subTour:
                for nodeInRemaining in remainingChoices:
                    if self.dists[nodeInSub][currentSelection] > self.dists[nodeInSub][nodeInRemaining]:
                        currentSelection = nodeInRemaining
            remainingChoices.remove(currentSelection)
            # can it insert at end check ?
            minCurrTour = None
            pos = None
            for k in range(0,len(subTour) - 1 ):
                if k == 0:
                    minCurrTour = self.dists[subTour[k]][currentSelection] + self.dists[currentSelection][subTour[k+1]]
                    pos = k+1
                else:
                    if (minCurrTour > self.dists[subTour[k]][currentSelection] + self.dists[currentSelection][subTour[k+1]]) :
                        minCurrTour = self.dists[subTour[k]][currentSelection] + self.dists[currentSelection][subTour[k+1]]
                        pos = k + 1
            subTour.insert(pos,currentSelection)
        self.perm = subTour




    def valFromStart(self,n):
        fullList = []
        i = 0
        for item in self.perm:
            if (((item -1) % n) == 0):
                i = item
            currentDistance = self.dists[i][item]
            fullList.append((item,currentDistance))

        fullList.remove((0,0))
        fullList.sort(key=lambda x: x[1])
        i = 1
        for cities in fullList:
            self.perm[i] = cities[0]
            i = i + 1
# two optimisation also look at wiki
def main():
    g = Graph(-1,"cities50")
    g.swapHeuristic(25)
    print(g.tourValue())
    #print(g.tourValue())
if __name__ == "__main__":
    main()
