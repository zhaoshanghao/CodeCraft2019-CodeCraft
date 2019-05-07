def ConstructionMap(roadData):
    Map = []
    for i in range(len(roadData)):
        if (roadData[i][-1] == 1):
            Map.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
            Map.append((str(roadData[i][-2]), str(roadData[i][-3]), roadData[i][1]))
        else:
            Map.append((str(roadData[i][-3]), str(roadData[i][-2]), roadData[i][1]))
    return Map

def FindRoute(CarList, RoadList, Map):
    carRoute = []
    for carNum in range(len(CarList)):
        ShortestRoute_theory = Dijkstra(Map, str(CarList[carNum][1]), str(CarList[carNum][2]))
        ShortestRoute_list = []
        while ShortestRoute_theory[1] != ():
            ShortestRoute_list.append(int(ShortestRoute_theory[0]))
            if ShortestRoute_theory[1] != ():
                ShortestRoute_theory = ShortestRoute_theory[1]
        ShortestRoute_list.append(int(ShortestRoute_theory[0]))
        lengthSumarize = len(ShortestRoute_list)
        carRouteTmp = [CarList[carNum][0]]
        carRouteTmp.append(CarList[carNum][-1]+random.randint(0,3000))
        for i in range(1, lengthSumarize - 1):
            for j in range(len(RoadList)):
                if ((RoadList[j][-3] == ShortestRoute_list[lengthSumarize - i] and RoadList[j][-2] == ShortestRoute_list[lengthSumarize - i - 1]) or (RoadList[j][-2] == ShortestRoute_list[lengthSumarize - i] and RoadList[j][-3] == ShortestRoute_list[lengthSumarize - i - 1])):
                    carRouteTmp.append(RoadList[j][0])
        carRoute.append(tuple(carRouteTmp))
    return carRoute
