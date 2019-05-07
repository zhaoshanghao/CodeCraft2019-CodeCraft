import logging
import sys
from collections import defaultdict
from heapq import *

def readData(car_path, cross_path, road_path):
    car_queue = []
    cross_queue = []
    road_queue = []
    data_car = []
    data_cross = []
    data_road = []

    with open(cross_path, "r") as f_cross:
        lines_cross = f_cross.readlines()
        for line in lines_cross:
            if (len(line) != 0 and line.isspace() == False and line.startswith("#") != True):
                for str in line.strip().lstrip("(").rstrip(")").replace(" ", "").split(","):
                    data_cross.append(int(str))
                cross_queue.append(data_cross)
                data_cross = []


    with open(road_path, "r") as f_road:
        lines_road = f_road.readlines()
        for line in lines_road:
            if (len(line) != 0 and line.isspace() == False and line.startswith("#") != True):
                for str in line.strip().lstrip("(").rstrip(")").replace(" ", "").split(","):
                    data_road.append(int(str))
                road_queue.append(data_road)
                data_road = []

    with open(car_path, "r") as f_car:
        lines_car = f_car.readlines()
        for line in lines_car:
            if (len(line) != 0 and line.isspace() == False and line.startswith("#") != True):
                for str in line.strip().lstrip("(").rstrip(")").replace(" ", "").split(","):
                    data_car.append(int(str))
                car_queue.append(data_car)
                data_car = []
    return car_queue, cross_queue, road_queue

def dijkstra(edges, f, t):
    g = defaultdict(list)
    for l,r,c in edges:
        g[l].append((c,r))

    q, seen, mins = [(0,f,())], set(), {f: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == t:

                return (cost, path)

            for c, v2 in g.get(v1, ()):
                if v2 in seen: continue
                prev = mins.get(v2, None)
                next = cost + c
                if prev is None or next < prev:
                    mins[v2] = next
                    heappush(q, (next, v2, path))



    return float("inf")


def Seek(carData, crossData, roadData):

    edges = []

    for i in range(len(roadData)):
        if (roadData[i][-1] == 1):
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
            edges.append((str(roadData[i][-2]), str(roadData[i][-3]), roadData[i][1]))
        else:
            edges.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))



    carRoute = []
    for carNum in range(len(carData)):

        result = dijkstra(edges, str(carData[carNum][1]), str(carData[carNum][2]))
        sumarize = []
        while result[1] != ():
            sumarize.append(int(result[0]))
            if result[1] != ():
                result = result[1]
        sumarize.append(int(result[0]))


        lengthSumarize = len(sumarize)
        carRouteTmp = [carData[carNum][0]]
        carRouteTmp.append(carData[carNum][-1])
        for i in range(1, lengthSumarize - 1):
            for j in range(len(roadData)):
                if ((roadData[j][-3] == sumarize[lengthSumarize - i] and roadData[j][-2] == sumarize[lengthSumarize - i -1]) or (roadData[j][-2] == sumarize[lengthSumarize - i] and roadData[j][-3] == sumarize[lengthSumarize - i -1])):
                    carRouteTmp.append(roadData[j][0])
        carRoute.append(tuple(carRouteTmp))


    return carRoute


def main():


    if len(sys.argv) != 5:
         logging.info('please input args: car_path, road_path, cross_path, answerPath')
         exit(1)

    car_path = sys.argv[1]
    road_path = sys.argv[2]
    cross_path = sys.argv[3]
    answer_path = sys.argv[4]

    logging.info("car_path is %s" % (car_path))
    logging.info("road_path is %s" % (road_path))
    logging.info("cross_path is %s" % (cross_path))
    logging.info("answer_path is %s" % (answer_path))

    # to read input file

    carData, crossData, roadData = readData(car_path, cross_path, road_path)

    # process

    carRoute = Seek(carData, crossData, roadData)

    # to write output file

    with open(answer_path, 'w') as f:
        f.write('#(carId,StartTime,RoadId...)')
        f.write('\n')
        for i in range(len(carRoute)):
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


if __name__ == "__main__":
    main()