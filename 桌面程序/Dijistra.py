import logging
import sys
from collections import defaultdict
from heapq import *
import re


def readData(carPath, crossPath, roadPath):
    carData = []
    crossData = []
    roadData = []
    with open(carPath, 'r') as lines:
        for line in lines:
            line = line.split(',')
            if re.findall("\d+", line[0]) != []:
                line[0] = re.findall("\d+", line[0])[0]
            if re.findall("\d+", line[-1]) != []:
                line[-1] = re.findall("\d+", line[-1])[0]
            # for i in range(len(line)):
            #     line[i] = int(line[i].strip())
            carData.append(line)
    with open(roadPath, 'r') as lines:
        for line in lines:
            line = line.split(',')
            if re.findall("\d+", line[0]) != []:
                line[0] = re.findall("\d+", line[0])[0]
            if re.findall("\d+", line[-1]) != []:
                line[-1] = re.findall("\d+", line[-1])[0]
            roadData.append(line)
    with open(crossPath, 'r') as lines:
        for line in lines:
            line = line.split(',')
            if re.findall("\d+", line[0]) != []:
                line[0] = re.findall("\d+", line[0])[0]
            if re.findall("\d+", line[-1]) != []:
                line[-1] = re.findall("\d+", line[-1])[0]
            crossData.append(line)
    print(crossData)

    carData = carData[1: ]
    for i in range(len(carData)):
        for j in range(len(carData[i])):
            carData[i][j] = int(carData[i][j].strip())
    roadData = roadData[1: ]
    for i in range(len(roadData)):
        for j in range(len(roadData[i])):
            roadData[i][j] = int(roadData[i][j].strip())
    crossData = crossData[1: ]
    for i in range(len(crossData)):
        for j in range(len(crossData[i])):
            crossData[i][j] = int(crossData[i][j].strip())
            if crossData[i][j] == 1:
                crossData[i][j] = -1
    return carData, crossData, roadData

def dijikstra(edges, start, end):
    g = defaultdict(list)
    for l, r, c in edges:      #将edges中的地图变成字典形式，形式：顶点+距离+相邻所有顶点
        g[l].append((c, r))
    # print(g)
    q, seen, mins = [(0, start, ())], set(), {start: 0}

    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == end:
                return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))


def SeekPath(carData, crossData, roadData):

    edges = []

    # 生成道路的地图（双向图）
    for i in range(len(roadData)):
        if (roadData[i][-1] == 1):
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
            edges.append((str(roadData[i][-2]), str(roadData[i][-3]), roadData[i][1]))
        else:
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
    print(edges)
    Car_Road = []
    for Num in range(len(carData)):
        result = dijikstra(edges, str(carData[Num][1]), str(carData[Num][2]))
        # print(result)
        sumarize = []
        while result[1] != ():    #result是个元组(55, ('50', ('42', ('34', ('26', ('18', ()))))))，把里边路口节点取出来
            sumarize.append(int(result[0]))
            if result[1] != ():
                result = result[1]
        sumarize.append(int(result[0]))   #路口的列表形式[55, 50, 42, 34, 26, 18]
        # print(sumarize)
        lengthSumarize = len(sumarize)
        carRouteTmp = [carData[Num][0]]
        carRouteTmp.append(carData[Num][-1]) #这是car的出发时间
        # print(carRouteTmp)
        for i in range(1, lengthSumarize - 1):
            for j in range(len(roadData)):
                if ((roadData[j][-3] == sumarize[lengthSumarize - i] and roadData[j][-2] == sumarize[
                    lengthSumarize - i - 1]) or (
                        roadData[j][-2] == sumarize[lengthSumarize - i] and roadData[j][-3] == sumarize[
                    lengthSumarize - i - 1])):
                    carRouteTmp.append(roadData[j][0])
        Car_Road.append(list(carRouteTmp))
    return Car_Road


if __name__ == "__main__":
    cpath = 'E:/2019华为软件精英挑战赛/2019软挑-初赛-SDK/SDK/SDK_python/CodeCraft-2019/map1/car.txt'
    rpath = 'E:/2019华为软件精英挑战赛/2019软挑-初赛-SDK/SDK/SDK_python/CodeCraft-2019/map1/road.txt'
    crpath = 'E:/2019华为软件精英挑战赛/2019软挑-初赛-SDK/SDK/SDK_python/CodeCraft-2019/map1/cross.txt'
    answerpath = 'E:/2019华为软件精英挑战赛/2019软挑-初赛-SDK/SDK/SDK_python/CodeCraft-2019/answer/answer.txt'
    cardata,crossdata,roaddata = readData(cpath, crpath, rpath)
    # print(crossdata)
    # print(roaddata)
    carRoute = SeekPath(cardata,crossdata,roaddata)
    print(carRoute)
    with open(answerpath,'w') as f:
        idex = 0
        for i in range(len(carRoute)):
            idex+=1
            if idex % 20 == 0:
                print(carRoute[i][1])
                carRoute[i][1] = carRoute[i][1] + 8
                print(carRoute[i][1])

            for j in range(len(carRoute[i])):
                if j == 0:
                    f.write('(')
                f.write(str(carRoute[i][j]))
                if j != len(carRoute[i]) - 1:
                    f.write(', ')
                else:
                    f.write(')')
            if i != len(carRoute) - 1:
                f.write('\n')
        f.close()