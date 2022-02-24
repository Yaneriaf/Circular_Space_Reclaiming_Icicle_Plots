degree = 5
depth = 4
randomDegree = True
degenerated = False
symmetric = False
selfSimilar = False

import random
random.seed(0)

if degenerated and selfSimilar:
    print("Warning: degnerated and selfSimilar cannot be applied together")

idCounter = 0
outNewick = ""
outTxt = ""
fileName = "hierarchy_degree"+str(degree)+"_depth"+str(depth)
if randomDegree:
    fileName += "_randomDegree"
if degenerated:
    fileName += "_degenerated"
if symmetric:
    fileName += "_symmetric"
if selfSimilar:
    fileName += "_selfSimilar"
fNewick = open(fileName+".tre","w")
fTxt = open(fileName+".txt","w")

def printTree(depth, path):
    global idCounter, outNewick, outTxt
    id = idCounter
    path += "/"+str(id)
    idCounter = idCounter + 1
    if (depth > 0):
        outNewick += "("
        currentDegree = degree
        if randomDegree:
            currentDegree = random.randint(2,degree)
        for i in range(0,currentDegree-1):
            if degenerated:
                printTree(min(1,depth-1),path)
            else:
                if selfSimilar:
                    printTree(depth-2-i,path)
                else:
                    printTree(random.randint(0,depth-1),path)
            outNewick += ","
        printTree(depth-1,path)
        outNewick += ")"
    else:
        if symmetric:
            outTxt += " 0/a/"+path[3:]+ " +1"
            outTxt += " 0/b/"+path[3:]+ " +1"
        else:
            outTxt += " "+path[1:]+ " +1"
    outNewick += str(id)
    
if symmetric:
    depth = depth - 1

printTree(depth,"")

if symmetric:
    outNewick = "(" +outNewick[:len(outNewick)-1] +"a,"+ outNewick[:len(outNewick)-1] +"b)0"
outNewick+=";"

fNewick.write("newick;\n"+outNewick)
fTxt.write("2000-01-01 00:00:00"+outTxt)

fNewick.close()
fTxt.close()


