'''
--- Day 10: Pipe Maze ---
You use the hang glider to ride the hot air from Desert Island all the way up to the floating metal island. This island is surprisingly cold and there definitely aren't any thermals to glide on, so you leave your hang glider behind.

You wander around for a while, but you don't find any people or animals. However, you do occasionally find signposts labeled "Hot Springs" pointing in a seemingly consistent direction; maybe you can find someone at the hot springs and ask them where the desert-machine parts are made.

The landscape here is alien; even the flowers and trees are made of metal. As you stop to admire some metal grass, you notice something metallic scurry away in your peripheral vision and jump into a big pipe! It didn't look like any animal you've ever seen; if you want a better look, you'll need to get ahead of it.

Scanning the area, you discover that the entire field you're standing on is densely packed with pipes; it was hard to tell at first because they're the same metallic silver color as the "ground". You make a quick sketch of all of the surface pipes you can see (your puzzle input).

The pipes are arranged in a two-dimensional grid of tiles:

| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
Based on the acoustics of the animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop.

For example, here is a square loop of pipe:

.....
.F-7.
.|.|.
.L-J.
.....
If the animal had entered this loop in the northwest corner, the sketch would instead look like this:

.....
.S-7.
.|.|.
.L-J.
.....
In the above diagram, the S tile is still a 90-degree F bend: you can tell because of how the adjacent pipes connect to it.

Unfortunately, there are also many pipes that aren't connected to the loop! This sketch shows the same loop as above:

-L|F7
7S-7|
L|7||
-L-J|
L|-JF
In the above diagram, you can still figure out which pipes form the main loop: they're the ones connected to S, pipes those pipes connect to, pipes those pipes connect to, and so on. Every pipe in the main loop connects to its two neighbors (including S, which will have exactly two pipes connecting to it, and which is assumed to connect back to those two pipes).

Here is a sketch that contains a slightly more complex main loop:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here's the same example sketch with the extra, non-main-loop pipe tiles also shown:

7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
If you want to get out ahead of the animal, you should find the tile in the loop that is farthest from the starting position. Because the animal is in the pipe, it doesn't make sense to measure this by direct distance. Instead, you need to find the tile that would take the longest number of steps along the loop to reach from the starting point - regardless of which way around the loop the animal went.

In the first example with the square loop:

.....
.S-7.
.|.|.
.L-J.
.....
You can count the distance each tile in the loop is from the starting point like this:

.....
.012.
.1.3.
.234.
.....
In this example, the farthest point from the start is 4 steps away.

Here's the more complex loop again:

..F7.
.FJ|.
SJ.L7
|F--J
LJ...
Here are the distances for each tile on that loop:

..45.
.236.
01.78
14567
23...
Find the single giant loop starting at S. How many steps along the loop does it take to get from the starting position to the point farthest from the starting position?

Your puzzle answer was 6947.
'''

PIPES_ADJ = {
    'down': ['J', '|', 'L'],
    'up': ['|', 'F', '7'],
    'right': ['-', '7', 'J'],
    'left': ['-', 'L', 'F'],
}

PIPES_TO = {
    'right': {
    'F': ['-', 'J', '7'],
    '-': ['-', 'J', '7'],
    'J': [],
    '7': [],
    '|': [],
    'L': ['-', 'J', '7'],
    'S': ['-', '7', 'J'],
},
    'left': {
    'F': [],
    '-': ['-', 'L', 'F'],
    'J': ['-', 'L', 'F'],
    '7': ['-', 'L', 'F'],
    '|': [],
    'L': [],
    'S': ['-', 'L', 'F']
},
    'up': {
    'S': ['|', 'F', '7'],
    'F': [],
    '-': [],
    'J': ['|', 'F', '7'],
    '7': [],
    '|': ['|', 'F', '7'],
    'L': ['|', 'F', '7'],
},
    'down': {
    'F': ['|', 'J', 'L'],
    '-': [],
    'J': [],
    '7': ['|', 'J', 'L'],
    '|': ['|', 'J', 'L'],
    'L': [],
    'S': ['J', '|', 'L']
}
}

def parse_input(data: str) -> list[list[str]]:
    return list(list(line) for line in data.split('\n'))

def get_starting_pos(matrix: list[list[str]]) -> tuple[int, int]:
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 'S':
                return (i, j)
    return (-1, -1)
    
def get_adjacent_pipes(pos: tuple[int, int], matrix: list[list[str]], exclude: tuple[int, int] = None) -> list[tuple[str, int, int]]:
    rows = len(matrix)
    cols = len(matrix[0])
    
    x, y = pos
    next_positions = [('up', -1, 0), ('right', 0, 1), ('down', 1, 0), ('left', 0, -1)]
    pipes = []

    for name, i, j in next_positions:
        i = x + i
        j = y + j
        
        if exclude is not None:
            if (i, j) == exclude:
                continue

        if (0 <= i < rows) and (0 <= j < cols):
            if matrix[i][j] in PIPES_TO[name][matrix[x][y]]:
                pipes.append((matrix[i][j], i, j))
    return pipes

def solve01(data: str):
    matrix = parse_input(data)
    start_pos = get_starting_pos(matrix)
    starting_pipes = get_adjacent_pipes(start_pos, matrix)

    pipes = {}
    idx = 0
    for pipe, i, j in starting_pipes:
        pipes[idx] = (pipe, i, j, 1)
        idx += 1
    
    prevs = {}

    while len(set(pipes.values())) != 1:
        to_delete = []

        for idx in pipes.keys():
            pipe, i, j, count = pipes[idx]

            prev = None
            if idx in prevs:
                prev = prevs[idx]

            next = get_adjacent_pipes((i, j), matrix, prev)
            if len(next) == 1:
               p, x, y = next[0]
               pipes[idx] = (p, x, y, count + 1)
               prevs[idx] = (i, j)
            if len(next) == 0:
               to_delete.append(idx)

        for idx in to_delete:
            del pipes[idx]
            if idx in prevs:
                del prevs[idx]

    _, _, _, count = set(pipes.values()).pop()

    return count

'''
--- Part Two ---
You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area enclosed by the loop?

To determine whether it's even worth taking the time to search for such a nest, you should calculate how many tiles are contained within the loop. For example:

...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
The above loop encloses merely four tiles - the two pairs of . in the southwest and southeast (marked I below). The middle . tiles (marked O below) are not in the loop. Here is the same loop again with those regions marked:

...........
.S-------7.
.|F-----7|.
.||OOOOO||.
.||OOOOO||.
.|L-7OF-J|.
.|II|O|II|.
.L--JOL--J.
.....O.....
In fact, there doesn't even need to be a full tile path to the outside for tiles to count as outside the loop - squeezing between pipes is also allowed! Here, I is still within the loop and O is still outside the loop:

..........
.S------7.
.|F----7|.
.||OOOO||.
.||OOOO||.
.|L-7F-J|.
.|II||II|.
.L--JL--J.
..........
In both of the above examples, 4 tiles are enclosed by the loop.

Here's a larger example:

.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
The above sketch has many random bits of ground, some of which are in the loop (I) and some of which are outside it (O):

OF----7F7F7F7F-7OOOO
O|F--7||||||||FJOOOO
O||OFJ||||||||L7OOOO
FJL7L7LJLJ||LJIL-7OO
L--JOL7IIILJS7F-7L7O
OOOOF-JIIF7FJ|L7L7L7
OOOOL7IF7||L7|IL7L7|
OOOOO|FJLJ|FJ|F7|OLJ
OOOOFJL-7O||O||||OOO
OOOOL---JOLJOLJLJOOO
In this larger example, 8 tiles are enclosed by the loop.

Any tile that isn't part of the main loop can count as being enclosed by the loop. Here's another example with many bits of junk pipe lying around that aren't connected to the main loop at all:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
Here are just the tiles that are enclosed by the loop marked with I:

FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJIF7FJ-
L---JF-JLJIIIIFJLJJ7
|F|F-JF---7IIIL7L|7|
|FFJF7L7F-JF7IIL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
In this last example, 10 tiles are enclosed by the loop.

Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are enclosed by the loop?

Your puzzle answer was 273.
'''

def solve02(data: str):
    def area_by_shoelace(points_in_clock_order: list[tuple[int, int]]) -> float:
        size = len(points_in_clock_order)
        area = 0
    
        for i in range(size):
            x1, y1 = points_in_clock_order[i]
            x2, y2 = points_in_clock_order[(i + 1) % size]
    
            area += (x1 * y2 - x2 * y1)
    
        return abs(area) / 2.0
    
    def points_inside_by_picks_theorem(area: float, number_of_points: int) -> int:
        return int(area + 1 - (number_of_points / 2))

    matrix = parse_input(data)
    start_pos = get_starting_pos(matrix)
    starting_pipes = get_adjacent_pipes(start_pos, matrix)

    _, x, y = starting_pipes[0]

    curr = (x, y)
    prev = None
    border_points_in_clock_order = []

    while curr != start_pos:
        next = get_adjacent_pipes(curr, matrix, prev)
        if len(next) == 1:
            p, x, y = next[0]
            border_points_in_clock_order.append((x, y))
            prev = curr
            curr = (x, y)
        elif len(next) == 0:
            curr = start_pos
            prev = curr
            break

    area = area_by_shoelace(border_points_in_clock_order)
    return points_inside_by_picks_theorem(area, len(border_points_in_clock_order))

if __name__ == "__main__":
    # data = open('day-10-input.test.txt', 'r').read()
    data = open('day-10-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
