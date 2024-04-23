from PIL import Image
import numpy
from random import *
from math import *




inputs_X,outputs_X = [],[]
for im in train_X:
    input = []
    for row in im:
        for a in row: input.append(a)
    inputs_X.append(input)
print(len(inputs_X[0]))
outputs_X = [[1 if i==x-1 else 0 for i in range(10)] for x in train_y]
print(outputs_X[0])

testIns_X = []
for im in test_X:
    input = []
    for row in im:
        for a in row: input.append(a)
    testIns_X.append(input)
testOuts_y = [[1 if i==x-1 else 0 for i in range(10)] for x in test_y]



def transfer(x):
    #return x if x>0 else 0
    return 1 / (1 + e ** (-1 * x))

layerCounts = [28*28,28,4,10,10]
numLayers = len(layerCounts)

genWeight = lambda: (random()-0.5)*2
weightCounts = []
weights = []


def generateNewWeights():
    weights = []
    weightCounts = []
    for ldx in range(numLayers - 1):
        l, next = layerCounts[ldx], layerCounts[ldx + 1]
        if ldx == numLayers - 2:
            weights.append([genWeight() for i in range(l)])
            weightCounts.append(l)
        else:
            weights.append([genWeight() for i in range(l * next)])
            weightCounts.append(l * next)
    # print(weights,weightCounts)
    return weights, weightCounts


weights, weightCounts = generateNewWeights()

def forward(weights, inputs, layerCounts):
    wdx = 0
    vals = [i for i in inputs]
    Nodes = [vals]

    for i in range(len(layerCounts) - 1):
        nextLayerNodes = []
        for nlndx in range(layerCounts[i + 1]):
            nextLayerNodes.append(0);
            if i == len(layerCounts) - 2:
                nextLayerNodes[nlndx] = vals[nlndx] * weights[i][nlndx]
            else:
                for j, cln in enumerate(vals):
                    nextLayerNodes[nlndx] += cln * weights[i][nlndx * layerCounts[i] + j]
                nextLayerNodes[nlndx] = transfer(nextLayerNodes[nlndx])
        Nodes.append(nextLayerNodes)
        vals = [p for p in nextLayerNodes]

    return Nodes


def backProp(woots, Nodes, expected, alpha):
    weights = woots
    numLayers = len(Nodes)
    errorGradient = []
    errorGradient.append([expected[i] - Nodes[-1][i] for i in range(len(expected))])
    for i in range(numLayers - 2, -1, -1):
        currErr = []
        # print(len(Nodes[i]),len(Nodes[i+1]))
        for n in range(len(Nodes[i])):
            cNode = Nodes[i][n]
            ERROR = 0
            if i < numLayers - 2:
                for f in range(len(Nodes[i + 1])):
                    errorGradient[i + 1 - numLayers][f]
                    weights[i][f * layerCounts[i] + n]
                    ERROR += errorGradient[i + 1 - numLayers][f] * weights[i][f * layerCounts[i] + n]
            else:
                ERROR = errorGradient[i + 1 - numLayers][n] * weights[i][n]
            ERROR *= cNode * (1 - cNode)
            currErr.append(ERROR)
        errorGradient.insert(0, currErr)

    for l in range(len(Nodes) - 2):
        for f in range(len(Nodes[l + 1])):
            for n in range(len(Nodes[l])):
                weights[l][f * len(Nodes[l]) + n] += Nodes[l][n] * errorGradient[l + 1][f] * alpha
    for n in range(len(Nodes[-1])): weights[-1][n] += Nodes[-2][n] * errorGradient[-1][n] * alpha
    return weights


def getError(inList, outList, weights, tf):
    ERROR = 0
    for inputs, outputs in zip(inList, outList):
        ERROR += sum(
            0.5 * (outputs[i] - forward(weights, inputs, layerCounts, tf)[-1][i]) ** 2 for i in range(len(outputs)))
    return ERROR

ct = 0
while True:
    ct += 1
    totalError = 0
    for n in range(len(inputs_X)):
        #print(n)
        nodes = forward(weights, inputs_X[n], layerCounts)
        totalError += sum(0.5 * (nodes[-1][i]-outputs_X[n][i]) ** 2 for i in range(10))
        weights = backProp(weights, nodes, outputs_X[n], 0.01)
    avgErr = totalError / len(inputs_X)
    print(avgErr)
    #if avgErr > 0.2: weights, weightCounts = generateNewWeights()
    if avgErr < 0.005: break

for n in range(len(testIns_X)):
    nodes = forward(weights, testIns_X[n], layerCounts)
    totalError += 0.5 * (nodes[-1][0] - testOuts_y[n]) ** 2
avgErr = totalError / len(inputs_X)
print("AvgErr:",avgErr)