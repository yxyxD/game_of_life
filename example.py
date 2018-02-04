import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

gridSize = 10
numberOfGenerations = 10

def getNeighborCount(x, y):
    global generation
    count = 0
    for i in [x-1, x, x+1]:
        for j in [y-1, y, y+1]:
            if (i == x and j == y):
                continue
            if (i != gridSize and j != gridSize):
                count += generation[i][j]
            elif (i == gridSize and j != gridSize):
                count += generation[0][j]
            elif (i != gridSize and j == gridSize):
                count += generation[i][0]
            else:
                count += generation[0][0]
    return count

def applyRules(x, y):
    global newGeneration
    neighborCount = getNeighborCount(x, y)
    if generation[x, y] == 1:
        if neighborCount < 2:
            newGeneration[x, y] = 0
        elif neighborCount == 2 or neighborCount == 3:
            newGeneration[x, y] = 1
        elif neighborCount > 3:
            newGeneration[x, y] = 0
    elif generation[x, y] == 0:
        if neighborCount == 3:
            newGeneration[x, y] = 1
    return

def playGame():
    t = 1
    global generation
    global newGeneration
    global numberOfGenerations
    while t <= numberOfGenerations:
        for x in range(gridSize):
            for y in range(gridSize):
                applyRules(x, y)
        generation = np.copy(newGeneration)
        print("At generation %d" % t)
        print(generation)
        t += 1
    return

def initWithBeacon():
    global generation
    beacon = [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]
    generation[1:5, 1:5] = beacon
    return

def initWithRandom():
    global generation
    randomSeed = np.random.randint(2, size=(gridSize, gridSize))
    generation = randomSeed
    return

if (__name__ == "__main__"):
    generation = np.zeros((gridSize, gridSize), dtype=np.int64)
    #initWithBeacon()
    initWithRandom()
    print(generation)
    newGeneration = np.copy(generation)
    playGame()
    #plt.axis('off')
    #plt.imshow(generation, cmap='binary', interpolation='nearest')
    #plt.show()