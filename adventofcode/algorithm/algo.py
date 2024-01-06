import collections as coll
import heapq
import math


def lcm(numbers):
    # Least-common multiplier for a list of numbers.
    result = 1
    for n in numbers:
        result = binary_lcm(result, n)
    return result


def binary_lcm(a, b):
    # Least-common multiplier for two numbers.
    return int(a * b / math.gcd(a, b))


def flatten_list(array_2d):
    return [e for row in array_2d for e in row]


def hamming_distance(first, second):
    # Number of different elements in two iterables.
    assert len(first) == len(second)
    return sum(a != b for a, b in zip(first, second))


def rotate_clockwise(array_2d):
    # Rotate a 2D list clockwise.
    return list(map(list, zip(*array_2d[::-1])))


def flood_fill(graph, start):
    # Finds the distances from the start node to all other nodes.
    queue = coll.deque([(start, 0)])
    distances = {}
    while queue:
        node, distance = queue.popleft()
        if node in distances:
            assert distance >= distances[node]
            continue
        distances[node] = distance
        for neighbor in graph[node]:
            queue.append((neighbor, distance + 1))
    return distances


def dijkstra(graph, start, neighbor_generator, start_cost=0):
    # Finds the shortest path from the start node to all other nodes.
    queue = [(start_cost, start)]
    costs = {}
    while queue:
        cost, node = heapq.heappop(queue)
        if node in costs:
            assert cost >= costs[node]
            continue
        costs[node] = cost
        for n, c in neighbor_generator(graph, node):
            heapq.heappush(queue, (cost + c, n))
    return costs


def polygon_area(polygon):
    # Find the area of a polygon using the trapezoid version of the Shoelace formula.
    n = len(polygon)
    area = 0
    for i in range(n):
        j = (i + 1) % n
        area += (polygon[i][0] + polygon[j][0]) * (polygon[i][1] - polygon[j][1])
    area = abs(area) // 2
    return area


def polygon_num_border_points(polygon):
    # Find the number of border points of a polygon.
    result = 0
    for a, b in zip(polygon[:-1], polygon[1:]):
        result += math.sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)
    return result


def polygon_internal_points(polygon):
    # Find the number of internal points in a polygon using Pick's theorem:
    #     A = i + b/2 - 1 => i = A - b/2 + 1,
    # where
    #     A: area of the polygon,
    #     i: number of internal points in polygon,
    #     b: number of border points.
    A = polygon_area(polygon)
    b = polygon_num_border_points(polygon)
    i = A - b // 2 + 1
    return i


def get_insides(graph, y_range, x_range):
    # Finds all positions that is inside a loop represented as a graph of
    # connected nodes. The y_range and x_range limits the search space, which
    # can typically be extracted from the min and max positions of the graph.
    # The algorithm is to keep track of whether we are inside or outside the
    # loop by detecting crossings. A crossing is detected by scanning line-wise
    # and for it to be a real crossing we must have encountered the loop both
    # above and below, otherwise it is not a crossing.
    #
    # Example crossings:
    #     #
    #     x
    #     #
    #
    #     #
    #     ####X
    #         #
    #
    # Example non-crossing:
    #
    #     ###X
    #     #  #
    #
    # X represents the current position.
    insides = set()
    for y in range(*y_range):
        is_inside = False
        crossing = set()
        for x in range(*x_range):
            node = (y, x)
            if node not in graph:
                if is_inside:
                    insides.add(node)
                continue
            right = (y, x + 1)
            up = (y - 1, x)
            down = (y + 1, x)
            neighbors = graph[node]
            if up in neighbors:
                crossing.add(-1)
            if down in neighbors:
                crossing.add(1)
            if right not in neighbors:
                if sum(crossing) == 0:
                    is_inside = not is_inside
                crossing.clear()
    return insides
