import sys
import math
import random

class Point:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

    def __repr__(self):
        return "(" + str(int(self.num)) + ")"

def printProblems(board):
    retStr = ""
    for i in range(0, len(board)):
        retStr += "["
        for x in range(0, len(board[i])):
            retStr += "["
            for y in range(0, len(board[i][x])):
                if y != len(board[i][x]) - 1:
                    retStr += (str(board[i][x][y]) + ",");
                else:
                    retStr += str(board[i][x][y])
            if(x != len(board[i]) - 1):
                retStr += "],"
            else:
                retStr += "]"
        if(i != len(board) - 1):
            retStr += "],"
        else:
            retStr += "]"
    print(retStr)

def printGen(gen):
    retStr = "["
    for i in range (0, len(gen)):
        retStr += "["
        for x in range(0, len(gen[i])):
            if x != len(gen[i]) - 1:
                retStr += str(gen[i][x]) + ","
            else:
                retStr += str(gen[i][x])
        if i != len(gen) - 1:
            retStr += "],"
        else:
            retStr += "]"
    retStr += "]"
    print(retStr)


def return_fitness(gen):
    distances = []
    for i in gen:
        distance = 0
        for x in range(0, len(i) - 1):
            distance += math.sqrt((i[x].x - i[x+1].x)**2 + (i[x].y - i[x+1].y)**2)
        distance += math.sqrt((i[0].x - i[len(i)-1].x)**2 + (i[0].y - i[len(i) - 1].y)**2)
        distances.append(distance)
    prString = ""
    for i in distances:
        i = 1/i
        prString += str(i) + "|"
    return distances

def shuffle(plist):
    random.shuffle(plist)
    return plist



if __name__ == "__main__":
    a = sys.argv
    readFile = open(a[1], 'r')
    writeFile = open(a[2], 'w')
    trials = int(a[3])
    linelist = readFile.readlines()
    problems = []
    tempArr = []
    for line in linelist:
        check = line.split(",")
        check[len(check) - 1] = check[len(check) - 1].replace("\n","")
        for i in check:
            if(type(i) != str):
                i = float(i)
        if line == '\n':
            problems.append(tempArr)
            tempArr = []
        else:
            tempArr.append(check)
        line = readFile.readline()
    #Begin running algorithm for each problem
    #printProblems(problems)
    for problem in problems:
        name = problem[0][0]
        leastVal = problem[0][1]
        #print("name: " + str(name) + " least dist: " + str(leastVal))
        trial = 0
        ##INITIALIZE NEW_GEN###
        new_gen = []
        csv_points = []
        orig_csv_points = []
        generation = []
        trial += 1
        #Create points.
        print("Problem " + name)
        for i in range(0, len(problem[1])):
            csv_points.append(Point(float(problem[1][i]), float(problem[2][i]), float(problem[3][i])))
            orig_csv_points = csv_points
        copy = shuffle(csv_points)
        while (len(new_gen) < 3):
            generation = []
            for i in range(0, 3):
                copy = shuffle(copy)
                generation.append(copy)
            #printGen(generation)
            fitness = return_fitness(generation)
            #Create two paths.
            two_gens = []
            while(len(fitness) > 1):
                index = fitness.index(max(fitness))
                two_gens.append(generation[index])
                fitness.pop(index)


            ##Choosing a random segment of random length.
            randLength = random.randint(1,len(two_gens[0]))
            randStart = random.randint(1,len(two_gens[0]))
            one_gen = []
            while(len(one_gen) < len(two_gens[0])):
                one_gen.append(-1)
            #Reset counter
            i = 0
            while(i < randLength + 1):
                one_gen[(randStart + i) % len(two_gens[0])] = two_gens[0][(randStart + i) % len(two_gens[0])]
                i += 1
            startIndex = (randStart + i) % len(two_gens[0])
            otherIndex = startIndex
            while(-1 in one_gen):
                if(one_gen[startIndex] == -1 and not(two_gens[1][otherIndex % len(two_gens[1])] in one_gen)):
                    one_gen[startIndex] = two_gens[1][otherIndex]
                    startIndex = (startIndex + 1) % len(two_gens[0])
                elif(one_gen[startIndex] != -1):
                    startIndex = (startIndex + 1) % len(two_gens[0])
                else:
                    otherIndex = (otherIndex + 1) % len(two_gens[0])

            new_gen.append(one_gen)
        ##Reset generation##
        generation = new_gen
        new_gen = []
        ##Begin trial iterating.
        trial += 1
        while(trial < trials):
            while (len(new_gen) <= 3):
                fitness = return_fitness(generation)
                #Create two paths.
                two_gens = []
                while(len(fitness) > 1):
                    index = fitness.index(max(fitness))
                    two_gens.append(generation[index])
                    fitness.pop(index)

                ##Choosing a random segment of random length.
                randLength = random.randint(1,len(two_gens[0]))
                randStart = random.randint(1,len(two_gens[0]))
                one_gen = []
                while(len(one_gen) < len(two_gens[0])):
                    one_gen.append(-1)
                #Reset counter
                i = 0
                while(i < randLength + 1):
                    one_gen[(randStart + i) % len(two_gens[0])] = two_gens[0][(randStart + i) % len(two_gens[0])]
                    i += 1
                startIndex = (randStart + i) % len(two_gens[0])
                otherIndex = startIndex
                while(-1 in one_gen):
                    if(one_gen[startIndex] == -1 and not(two_gens[1][otherIndex] in one_gen)):
                        one_gen[startIndex] = two_gens[1][otherIndex % len(two_gens[1])]
                        startIndex = (startIndex + 1) % len(two_gens[0])
                    elif(one_gen[startIndex] != -1):
                        startIndex = (startIndex + 1) % len(two_gens[0])
                    else:
                        otherIndex = (otherIndex + 1) % len(two_gens[0])

                new_gen.append(one_gen)
            generation = new_gen
            new_gen = []
            trial += 1
        printGen(generation)











