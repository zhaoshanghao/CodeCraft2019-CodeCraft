import logging
import sys
import random
from heapq import *
from collections import defaultdict

random.seed(7)
def ReadData(car_path, cross_path, road_path):
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

def Dijkstra(Map, start_point, end_point):
    dict = defaultdict(list)
    for StartPoint,EndPoint,RoadLength in Map:
        dict[StartPoint].append((RoadLength,EndPoint))
    q, seen, dist = [(0, start_point, ())], set(), {start_point: 0}
    while q:
        (cost,v1,path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == end_point:
                break;
            for RoadLength, v2 in dict.get(v1, ()):
                if v2 in seen: continue
                prev = dist.get(v2, None)
                next = cost + RoadLength
                if prev is None or next < prev:
                    dist[v2] = next
                    heappush(q, (next, v2, path))
    return cost,path

def ConstructionMap(RoadList):
    Map = []
    for each_road in range(len(RoadList)):
        if (RoadList[each_road][-1] == 1):
            Map.append((str(RoadList[each_road][-3]), str(RoadList[each_road][-2]), RoadList[each_road][1]))
            Map.append((str(RoadList[each_road][-2]), str(RoadList[each_road][-3]), RoadList[each_road][1]))
        else:
            Map.append((str(RoadList[each_road][-3]), str(RoadList[each_road][-2]), RoadList[each_road][1]))
    return Map

def FindRoute(CarList, RoadList, Map):
    carRoute = []
    Flag = 0
    for carNum in range(len(CarList)):
        ShortestRoute_theory = Dijkstra(Map, str(CarList[carNum][1]), str(CarList[carNum][2]))
        ShortestRoute_list = []
        while len(ShortestRoute_theory[1]):
            ShortestRoute_list.append(int(ShortestRoute_theory[0]))
            ShortestRoute_theory = ShortestRoute_theory[1]
        ShortestRoute_list.append(int(ShortestRoute_theory[0]))
        route_info_tmp = [CarList[carNum][0]]
        route_info_tmp.append(CarList[carNum][-1] + random.randint(0, 3500))
        for i in range(1, len(ShortestRoute_list) - 1):
            for j in range(len(RoadList)):
                if ((RoadList[j][-3] == ShortestRoute_list[len(ShortestRoute_list) - i] and RoadList[j][-2] == ShortestRoute_list[len(ShortestRoute_list) - i - 1]) or (RoadList[j][-2] == ShortestRoute_list[len(ShortestRoute_list) - i] and RoadList[j][-3] == ShortestRoute_list[len(ShortestRoute_list) - i - 1])):
                    route_info_tmp.append(RoadList[j][0])
        carRoute.append(tuple(route_info_tmp))
    return carRoute

def SaveResult(answer_path,Route):
    with open(answer_path, 'w') as f:
        for each_route in Route:
            f.write("(" + str(each_route)[1:-1] + ")" + "\n")
        f.close()


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
    CarList, CrossList, RoadList = ReadData(car_path, cross_path, road_path)

    # process
    Route = FindRoute(CarList, RoadList, ConstructionMap(RoadList))

    # to write output file
    SaveResult(answer_path, Route)


if __name__ == "__main__":
    main()