import collections as coll
import functools
import heapq
import math
import operator


def lcm(numbers):
    # Least-common multiplier for a list of numbers.
    result = 1
    for n in numbers:
        result = binary_lcm(result, n)
    return result


def binary_lcm(a, b):
    # Least-common multiplier for two numbers.
    return int(a * b / math.gcd(a, b))


def lagrange_polynomial(points):
    # Creates a polynomial function of degree <= #points that interpolates the given points.
    def basis_polynomial(j, x):
        return functools.reduce(
            operator.mul,
            (
                (x - p[0]) / (points[j][0] - p[0])
                for i, p in enumerate(points)
                if i != j
            ),
        )

    def f(x):
        return sum(p[1] * basis_polynomial(i, x) for i, p in enumerate(points))

    assert len(set(p[0] for p in points)) == len(points)  # Check that all x are unique.
    return f


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
    # Find the distances from the start node to all other nodes.
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
    # Find the shortest path from the start node to all other nodes.
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


def longest_path(graph, start, end, neighbor_generator, visited=None):
    # Find the longest path from start to end using DFS. Note that this is not feasible for large
    # graphs.
    visited = visited if visited else set()
    visited.add(start)
    if start == end:
        length = 0
    else:
        length = float("-inf")
        # Use -inf to handle invalid paths that does not lead to end in a nice way.
        for node, distance in neighbor_generator(graph, start):
            if node not in visited:
                candidate = longest_path(graph, node, end, neighbor_generator, visited)
                length = max(length, distance + candidate)
    visited.remove(start)
    return length


def compress_maze(maze, start, end, neighbor_generator):
    # Compress a maze to a graph represented as a dict where each node is an intersection:
    #     {node: [(neighbor_node, distance)]}
    def find_neighbor_intersections(start, intersections):
        queue = coll.deque()
        visited = set()
        for n in neighbor_generator(maze, start):
            queue.append((n, 1))
        neighbors = set()
        while queue:
            node, distance = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            if node in intersections:
                neighbors.add((node, distance))
                continue
            for n in neighbor_generator(maze, node):
                queue.append((n, distance + 1))
        return neighbors

    intersections = set(
        node for node in maze if len(list(neighbor_generator(maze, node))) > 2
    )
    intersections.add(start)
    intersections.add(end)
    graph = {c: find_neighbor_intersections(c, intersections) for c in intersections}
    return graph


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
