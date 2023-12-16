'''
--- Day 16: The Floor Will Be Lava ---
With the beam of light completely focused somewhere, the reindeer leads you deeper still into the Lava Production Facility. At some point, you realize that the steel facility walls have been replaced with cave, and the doorways are just cave, and the floor is cave, and you're pretty sure this is actually just a giant cave.

Finally, as you approach what must be the heart of the mountain, you see a bright light in a cavern up ahead. There, you discover that the beam of light you so carefully focused is emerging from the cavern wall closest to the facility and pouring all of its energy into a contraption on the opposite side.

Upon closer inspection, the contraption appears to be a flat, two-dimensional square grid containing empty space (.), mirrors (/ and \), and splitters (| and -).

The contraption is aligned so that most of the beam bounces around the grid, but each tile on the grid converts some of the beam's light into heat to melt the rock in the cavern.

You note the layout of the contraption (your puzzle input). For example:

.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
The beam enters in the top-left corner from the left and heading to the right. Then, its behavior depends on what it encounters as it moves:

If the beam encounters empty space (.), it continues in the same direction.
If the beam encounters a mirror (/ or \), the beam is reflected 90 degrees depending on the angle of the mirror. For instance, a rightward-moving beam that encounters a / mirror would continue upward in the mirror's column, while a rightward-moving beam that encounters a \ mirror would continue downward from the mirror's column.
If the beam encounters the pointy end of a splitter (| or -), the beam passes through the splitter as if the splitter were empty space. For instance, a rightward-moving beam that encounters a - splitter would continue in the same direction.
If the beam encounters the flat side of a splitter (| or -), the beam is split into two beams going in each of the two directions the splitter's pointy ends are pointing. For instance, a rightward-moving beam that encounters a | splitter would split into two beams: one that continues upward from the splitter's column and one that continues downward from the splitter's column.
Beams do not interact with other beams; a tile can have many beams passing through it at the same time. A tile is energized if that tile has at least one beam pass through it, reflect in it, or split in it.

In the above example, here is how the beam of light bounces around the contraption:

>|<<<\....
|v-.\^....
.v...|->>>
.v...v^.|.
.v...v^...
.v...v^..\
.v../2\\..
<->-/vv|..
.|<<<2-|.\
.v//.|.v..
Beams are only shown on empty tiles; arrows indicate the direction of the beams. If a tile contains beams moving in multiple directions, the number of distinct directions is shown instead. Here is the same diagram but instead only showing whether a tile is energized (#) or not (.):

######....
.#...#....
.#...#####
.#...##...
.#...##...
.#...##...
.#..####..
########..
.#######..
.#...#.#..
Ultimately, in this example, 46 tiles become energized.

The light isn't energizing enough tiles to produce lava; to debug the contraption, you need to start by analyzing the current situation. With the beam starting in the top-left heading right, how many tiles end up being energized?

Your puzzle answer was 7608.
'''

OFFSET_BY_DIR = {
    'right': (0, 1),
    'left': (0, -1),
    'up': (-1, 0),
    'down': (1, 0),
}

NEW_DIRS = {
    'right': {
        '.': ['right'],
        '\\': ['down'],
        '/': ['up'],
        '-': ['right'],
        '|': ['up', 'down']
    },
    'left': {
        '.': ['left'],
        '\\': ['up'],
        '/': ['down'],
        '-': ['left'],
        '|': ['up', 'down']
    },
    'up': {
        '.': ['up'],
        '\\': ['left'],
        '/': ['right'],
        '-': ['left', 'right'],
        '|': ['up']
    },
    'down': {
        '.': ['down'],
        '\\': ['right'],
        '/': ['left'],
        '-': ['left', 'right'],
        '|': ['down']
    },
}

def in_bounds(i: int, j: int, matrix: list[list[str]]) -> bool:
    return i >= 0 and j >= 0 and i < len(matrix) and j < len(matrix[0])

def get_energyzed_tiles(starting_point: tuple[int, int, str], matrix: list[list[str]]) -> set:
    tiles = set()
    visited = set()

    rays = [starting_point]

    while len(rays) > 0:
            i, j, dir = rays.pop(0)
            di, dj = i + OFFSET_BY_DIR[dir][0], j + OFFSET_BY_DIR[dir][1]

            if not in_bounds(di, dj, matrix):
                continue

            tiles.add((di, dj))

            new_dirs = NEW_DIRS[dir][matrix[di][dj]]

            for new_dir in new_dirs:
                n = (di, dj, new_dir)

                if n in visited:
                    continue

                visited.add(n)
                rays.append(n)

    return tiles

def solve01(data: str):
    matrix = list(list(line) for line in data.split('\n'))
    return len(get_energyzed_tiles((0, -1, 'right'), matrix))

'''
--- Part Two ---
As you try to work out what might be wrong, the reindeer tugs on your shirt and leads you to a nearby control panel. There, a collection of buttons lets you align the contraption so that the beam enters from any edge tile and heading away from that edge. (You can choose either of two directions for the beam if it starts on a corner; for instance, if the beam starts in the bottom-right corner, it can start heading either left or upward.)

So, the beam could start on any tile in the top row (heading downward), any tile in the bottom row (heading upward), any tile in the leftmost column (heading right), or any tile in the rightmost column (heading left). To produce lava, you need to find the configuration that energizes as many tiles as possible.

In the above example, this can be achieved by starting the beam in the fourth tile from the left in the top row:

.|<2<\....
|v-v\^....
.v.v.|->>>
.v.v.v^.|.
.v.v.v^...
.v.v.v^..\
.v.v/2\\..
<-2-/vv|..
.|<<<2-|.\
.v//.|.v..
Using this configuration, 51 tiles are energized:

.#####....
.#.#.#....
.#.#.#####
.#.#.##...
.#.#.##...
.#.#.##...
.#.#####..
########..
.#######..
.#...#.#..
Find the initial beam configuration that energizes the largest number of tiles; how many tiles are energized in that configuration?

Your puzzle answer was 8221.
'''

def get_starting_points_with_dirs(matrix: list[list[str]]) -> list[tuple[int, int, str]]:
    starting_points = []
    rows = len(matrix)
    cols = len(matrix[0])

    for i in range(rows):
        starting_points.append((i, -1, 'right'))
        starting_points.append((i, cols, 'left'))

    for j in range(cols):
        starting_points.append((-1, j, 'down'))
        starting_points.append((rows, j, 'up'))

    return starting_points

def solve02(data: str):
    matrix = list(list(line) for line in data.split('\n'))

    ans = -1
    for point in get_starting_points_with_dirs(matrix):
        ans = max(ans, len(get_energyzed_tiles(point, matrix)))    
    return ans

if __name__ == "__main__":
    # data = open('day-16-input.test.txt', 'r').read()
    data = open('day-16-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
