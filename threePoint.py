import shapefile as shp
import numpy as np
from collections import defaultdict
import json


def geo(ans):
    # 总字典
    # ***************************读取文件*********************************
    g = defaultdict(list)
    g["type"] = "FeatureCollection"

    for i in range(len(ans)):
        geometry = defaultdict(list)
        geometry["type"] = "Polygon"
        geometry["coordinates"].append(ans[i])

        properties = defaultdict(list)
        properties["value"] = i
        # properties属性的字典
        object = {
            'type': "Feature",
            'properties': properties,
            'geometry': geometry
        }
        # objects.append(object)
        g["features"].append(object)
    # geometry属性的字典

    json_str = json.dumps(g, indent=2)  # 注意这个indent参数

    with open('./gridFile/POLYGON.geojson', 'w') as json_file:
        json_file.write(json_str)



# 已知平行四边形三个点，求第四个点
# 计算两点之间的距离
def CalcEuclideanDistance(point1, point2):
    vec1 = np.array(point1)
    vec2 = np.array(point2)
    distance = np.linalg.norm(vec1 - vec2)
    return distance


# 计算第四个点
def CalcFourthPoint(point1, point2, point3):  # pint3为A点
    D = (point1[0] + point2[0] - point3[0], point1[1] + point2[1] - point3[1])
    return D


# 三点构成一个三角形，利用两点之间的距离，判断邻边AB和AC,利用向量法以及平行四边形法则，可以求得第四个点D
def JudgeBeveling(point1, point2, point3):
    dist1 = CalcEuclideanDistance(point1, point2)
    dist2 = CalcEuclideanDistance(point1, point3)
    dist3 = CalcEuclideanDistance(point2, point3)
    dist = [dist1, dist2, dist3]
    max_dist = dist.index(max(dist))
    if max_dist == 0:
        D = CalcFourthPoint(point1, point2, point3)
    elif max_dist == 1:
        D = CalcFourthPoint(point1, point3, point2)
    else:
        D = CalcFourthPoint(point2, point3, point1)
    return D



def threePoint(point3, point1, point2, d_x, d_y):
    point4 = (point1[0] + point2[0] - point3[0], point1[1] + point2[1] - point3[1])
    l1 = [point1, point2, point3, point4]
    origin = point1#point1为原点
    for i in range(1, 4):
        if l1[i][0] < origin[0]:
            origin = l1[i]
        elif l1[i][0] == origin[0]:
            if l1[i][1] < origin[1]:
                origin = l1[i]
    l1.remove(origin)
    farthest = l1[0]
    for i in range(1, 3):
        len1 = (farthest[0] - origin[0]) * (farthest[0] - origin[0]) + (farthest[1] - origin[1]) * (
                farthest[1] - origin[1])
        len2 = (l1[i][0] - origin[0]) * (l1[i][0] - origin[0]) + (l1[i][1] - origin[1]) * (l1[i][1] - origin[1])
        if len1 < len2:
            farthest = l1[i]
    l1.remove(farthest)

    if l1[0][0] - origin[0] == 0:
        up = l1[0]
        down = l1[1]
    elif l1[1][0] - origin[0] == 0:
        up = l1[1]
        down = l1[0]
    else:
        k1 = (l1[0][1] - origin[1]) / (l1[0][0] - origin[0])
        k2 = (l1[1][1] - origin[1]) / (l1[1][0] - origin[0])
        if (k1 > k2):
            up = l1[0]
            down = l1[1]
        else:
            up = l1[1]
            down = l1[0]

    # lenUP = (up[0] - origin[0]) * (up[0] - origin[0]) + (up[1] - origin[1]) * (up[1] - origin[1])
    # lenDown = (down[0] - origin[0]) * (down[0] - origin[0]) + (down[1] - origin[1]) * (down[1] - origin[1])
    # lenUP = pow(lenUP, 0.5)
    # lenDown = pow(lenDown, 0.5)

    Dy = 1 / d_y
    Dx = 1 / d_x

    nx = d_x
    ny = d_y

    #生成shp文件
    w = shp.Writer("POLYGON")
    w.autoBalance = 1
    w.field("ID")
    id = 0

    ans = []
    for i in range(ny):
        for j in range(nx):
            id += 1
            vertices = []
            parts = []

            vertices.append([origin[0] + (down[0] - origin[0]) * Dx * j + (up[0] - origin[0]) * Dy * i,
                             origin[1] + (down[1] - origin[1]) * Dx * j + (up[1] - origin[1]) * Dy * i])

            vertices.append([origin[0] + (down[0] - origin[0]) * Dx * (j + 1) + (up[0] - origin[0]) * Dy * i,
                             origin[1] + (down[1] - origin[1]) * Dx * (j + 1) + (up[1] - origin[1]) * Dy * i])

            vertices.append([origin[0] + (down[0] - origin[0]) * Dx * (j + 1) + (up[0] - origin[0]) * Dy * (i + 1),
                             origin[1] + (down[1] - origin[1]) * Dx * (j + 1) + (up[1] - origin[1]) * Dy * (i + 1)])

            vertices.append([origin[0] + (down[0] - origin[0]) * Dx * j + (up[0] - origin[0]) * Dy * (i + 1),
                             origin[1] + (down[1] - origin[1]) * Dx * j + (up[1] - origin[1]) * Dy * (i + 1)])

            parts.append(vertices)
            w.poly(parts)
            w.record(id)
            ans.append(vertices)
    #生成geojson文件
    geo(ans)


# threePoint((-74.0315102,40.7062855), (-73.9871323,40.6937655), (-73.9985950,40.7738362), 8, 16)
threePoint((0,0), (1,2), (2,1), 1, 2)
# point1 = (30, 10)
# point2 = (10, 20)
# point3 = (0,0)

# d_x = 4
# d_y = 5

# w.save('polygon_grid')
