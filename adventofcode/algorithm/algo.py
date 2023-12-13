import collections as coll


def hamming_distance(first, second):
    # Number of different elements in two iterables.
    assert len(first) == len(second)
    return sum(a != b for a, b in zip(first, second))


def rotate_clockwise(array_2d):
    # Rotate a 2D list clockwise.
    return list(zip(*array_2d[::-1]))


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
