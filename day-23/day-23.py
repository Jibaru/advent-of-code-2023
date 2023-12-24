'''
--- Day 23: A Long Walk ---
The Elves resume water filtering operations! Clean water starts flowing over the edge of Island Island.

They offer to help you go over the edge of Island Island, too! Just hold on tight to one end of this impossibly long rope and they'll lower you down a safe distance from the massive waterfall you just created.

As you finally reach Snow Island, you see that the water isn't really reaching the ground: it's being absorbed by the air itself. It looks like you'll finally have a little downtime while the moisture builds up to snow-producing levels. Snow Island is pretty scenic, even without any snow; why not take a walk?

There's a map of nearby hiking trails (your puzzle input) that indicates paths (.), forest (#), and steep slopes (^, >, v, and <).

For example:

#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
You're currently on the single path tile in the top row; your goal is to reach the single path tile in the bottom row. Because of all the mist from the waterfall, the slopes are probably quite icy; if you step onto a slope tile, your next step must be downhill (in the direction the arrow is pointing). To make sure you have the most scenic hike possible, never step onto the same tile twice. What is the longest hike you can take?

In the example above, the longest hike you can take is marked with O, and your starting position is marked S:

#S#####################
#OOOOOOO#########...###
#######O#########.#.###
###OOOOO#OOO>.###.#.###
###O#####O#O#.###.#.###
###OOOOO#O#O#.....#...#
###v###O#O#O#########.#
###...#O#O#OOOOOOO#...#
#####.#O#O#######O#.###
#.....#O#O#OOOOOOO#...#
#.#####O#O#O#########v#
#.#...#OOO#OOO###OOOOO#
#.#.#v#######O###O###O#
#...#.>.#...>OOO#O###O#
#####v#.#.###v#O#O###O#
#.....#...#...#O#O#OOO#
#.#########.###O#O#O###
#...###...#...#OOO#O###
###.###.#.###v#####O###
#...#...#.#.>.>.#.>O###
#.###.###.#.###.#.#O###
#.....###...###...#OOO#
#####################O#
This hike contains 94 steps. (The other possible hikes you could have taken were 90, 86, 82, 82, and 74 steps long.)

Find the longest hike you can take through the hiking trails listed on your map. How many steps long is the longest hike?

Your puzzle answer was 2386.
'''

def in_bounds(i: int, j: int, matrix: list[str]) -> bool:
    return i >= 0 and j >= 0 and i < len(matrix) and j < len(matrix[0])

def make_weighted_graph(
    matrix: list[list[str]],
    start_node: tuple[int, int],
    end_node: tuple[int, int],
    use_all_directions: bool = False
) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    NEIGHBOR_DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    DIRS = {
        '^': [(-1, 0)],
        'v': [(1, 0)],
        '<': [(0, -1)],
        '>': [(0, 1)],
        '.': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    }

    points = [start_node, end_node]

    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == '#':
                continue

            neighbors = 0
            for di, dj in NEIGHBOR_DIRECTIONS:
                ni = di + i
                nj = dj + j
                if in_bounds(ni, nj, matrix) and matrix[ni][nj] != '#':
                    neighbors += 1

            if neighbors >= 3:
                points.append((i, j))
    
    graph = {pt: {} for pt in points}

    for i, j in points:
        stack = [(0, i, j)]
        visited = {(i, j)}
    
        while stack:
            weight, r, c = stack.pop()
            
            if weight != 0 and (r, c) in points:
                graph[(i, j)][(r, c)] = weight
                continue
    
            dirs = DIRS[matrix[r][c]]
            if use_all_directions:
                dirs = NEIGHBOR_DIRECTIONS
    
            for di, dj in dirs:
                ni = r + di
                nj = c + dj
                if in_bounds(ni, nj, matrix) and matrix[ni][nj] != '#' and (ni, nj) not in visited:
                    stack.append((weight + 1, ni, nj))
                    visited.add((ni, nj))

    return graph

def dfs(
    node: tuple[int, int],
    graph: dict[tuple[int, int], dict[tuple[int, int], int]],
    visited: set[tuple[int, int]],
    end_node: tuple[int, int]
) -> int:
    if node == end_node:
        return 0

    ans = -float("inf")

    visited.add(node)
    for next_node in graph[node]:
        if next_node not in visited:
            weight = graph[node][next_node]
            ans = max(ans, dfs(next_node, graph, visited, end_node) + weight)
    visited.remove(node)

    return ans

def find_longest_path(data: str, use_all_directions: bool) -> int:
    matrix = list(line for line in data.split('\n'))

    start_node = (0, 1)
    end_node = (len(matrix) - 1, len(matrix[0]) - 2)
    graph = make_weighted_graph(matrix, start_node, end_node, use_all_directions)

    return dfs(start_node, graph, set(), end_node)

def solve01(data: str) -> int:
    return find_longest_path(data, use_all_directions=False)

'''
--- Part Two ---
As you reach the trailhead, you realize that the ground isn't as slippery as you expected; you'll have no problem climbing up the steep slopes.

Now, treat all slopes as if they were normal paths (.). You still want to make sure you have the most scenic hike possible, so continue to ensure that you never step onto the same tile twice. What is the longest hike you can take?

In the example above, this increases the longest hike to 154 steps:

#S#####################
#OOOOOOO#########OOO###
#######O#########O#O###
###OOOOO#.>OOO###O#O###
###O#####.#O#O###O#O###
###O>...#.#O#OOOOO#OOO#
###O###.#.#O#########O#
###OOO#.#.#OOOOOOO#OOO#
#####O#.#.#######O#O###
#OOOOO#.#.#OOOOOOO#OOO#
#O#####.#.#O#########O#
#O#OOO#...#OOO###...>O#
#O#O#O#######O###.###O#
#OOO#O>.#...>O>.#.###O#
#####O#.#.###O#.#.###O#
#OOOOO#...#OOO#.#.#OOO#
#O#########O###.#.#O###
#OOO###OOO#OOO#...#O###
###O###O#O###O#####O###
#OOO#OOO#O#OOO>.#.>O###
#O###O###O#O###.#.#O###
#OOOOO###OOO###...#OOO#
#####################O#
Find the longest hike you can take through the surprisingly dry hiking trails listed on your map. How many steps long is the longest hike?

Your puzzle answer was 6246.
'''

def solve02(data: str) -> int:
    return find_longest_path(data, use_all_directions=True)

if __name__ == "__main__":
    data = open('day-23-input.test.txt', 'r').read()
    data = open('day-23-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
