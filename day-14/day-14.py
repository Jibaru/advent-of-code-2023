'''
--- Day 14: Parabolic Reflector Dish ---
You reach the place where all of the mirrors were pointing: a massive parabolic reflector dish attached to the side of another large mountain.

The dish is made up of many small mirrors, but while the mirrors themselves are roughly in the shape of a parabolic reflector dish, each individual mirror seems to be pointing in slightly the wrong direction. If the dish is meant to focus light, all it's doing right now is sending it in a vague direction.

This system must be what provides the energy for the lava! If you focus the reflector dish, maybe you can go where it's pointing and use the light to fix the lava production.

Upon closer inspection, the individual mirrors each appear to be connected via an elaborate system of ropes and pulleys to a large metal platform below the dish. The platform is covered in large rocks of various shapes. Depending on their position, the weight of the rocks deforms the platform, and the shape of the platform controls which ropes move and ultimately the focus of the dish.

In short: if you move the rocks, you can focus the dish. The platform even has a control panel on the side that lets you tilt it in one of four directions! The rounded rocks (O) will roll when the platform is tilted, while the cube-shaped rocks (#) will stay in place. You note the positions of all of the empty spaces (.) and rocks (your puzzle input). For example:

O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
Start by tilting the lever so all of the rocks will slide north as far as they will go:

OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#....
You notice that the support beams along the north side of the platform are damaged; to ensure the platform doesn't collapse, you should calculate the total load on the north support beams.

The amount of load caused by a single rounded rock (O) is equal to the number of rows from the rock to the south edge of the platform, including the row the rock is on. (Cube-shaped rocks (#) don't contribute to load.) So, the amount of load caused by each rock in each row is as follows:

OOOO.#.O.. 10
OO..#....#  9
OO..O##..O  8
O..#.OO...  7
........#.  6
..#....#.#  5
..O..#.O.O  4
..O.......  3
#....###..  2
#....#....  1
The total load is the sum of the load caused by all of the rounded rocks. In this example, the total load is 136.

Tilt the platform so that the rounded rocks all roll north. Afterward, what is the total load on the north support beams?

Your puzzle answer was 112773.
'''

def transpose(matrix: list[list[str]]) -> list[list[str]]:
    transposed = list(zip(*matrix))
    for i in range(len(transposed)):
        transposed[i] = list(transposed[i])
    return transposed

def tilt_north(matrix: list[list[str]]) -> list[list[str]]:
    transposed = transpose(matrix)

    total_rows = len(transposed)
    total_cols = len(transposed[0])

    for i in range(total_rows):
        current_j = -1
        idx = []
        for j in range(total_cols):
            if transposed[i][j] == '#':
                current_j = j
            elif transposed[i][j] == 'O':
                current_j += 1
                idx.append(current_j)

        for j in range(total_cols):
            if j in idx:
                transposed[i][j] = 'O'
            elif transposed[i][j] != '#':
                transposed[i][j] = '.'

    return transpose(transposed)

def summarize(matrix: list[list[str]]) -> int:
    total_rows = len(matrix)
    total_cols = len(matrix[0])
    ans = 0
    for i in range(total_rows):
        for j in range(total_cols):
            if matrix[i][j] == 'O':
                ans += (total_cols - i)
    return ans

def solve01(data: str):
    matrix = list(list(line) for line in data.split('\n'))
    matrix = tilt_north(matrix)
    return summarize(matrix)

'''
--- Part Two ---
The parabolic reflector dish deforms, but not in a way that focuses the beam. To do that, you'll need to move the rocks to the edges of the platform. Fortunately, a button on the side of the control panel labeled "spin cycle" attempts to do just that!

Each cycle tilts the platform four times so that the rounded rocks roll north, then west, then south, then east. After each tilt, the rounded rocks roll as far as they can before the platform tilts in the next direction. After one cycle, the platform will have finished rolling the rounded rocks in those four directions in that order.

Here's what happens in the example above after each of the first few cycles:

After 1 cycle:
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#....

After 2 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O

After 3 cycles:
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O
This process should work if you leave it running long enough, but you're still worried about the north support beams. To make sure they'll survive for a while, you need to calculate the total load on the north support beams after 1000000000 cycles.

In the above example, after 1000000000 cycles, the total load on the north support beams is 64.

Run the spin cycle for 1000000000 cycles. Afterward, what is the total load on the north support beams?

Your puzzle answer was 98894.
'''

def tilt_east(matrix: list[list[str]]) -> list[list[str]]:
    total_rows = len(matrix)
    total_cols = len(matrix[0])

    for i in range(total_rows):
        current_j = total_cols
        idx = []
        for j in range(total_cols - 1, -1, -1):
            if matrix[i][j] == '#':
                current_j = j
            elif matrix[i][j] == 'O':
                current_j -= 1
                idx.append(current_j)

        for j in range(total_cols):
            if j in idx:
                matrix[i][j] = 'O'
            elif matrix[i][j] != '#':
                matrix[i][j] = '.'
    return matrix

def tilt_south(matrix: list[list[str]]) -> list[list[str]]:
    transposed = transpose(matrix)

    total_rows = len(transposed)
    total_cols = len(transposed[0])

    for i in range(total_rows):
        current_j = total_cols
        idx = []
        for j in range(total_cols - 1, -1, -1):
            if transposed[i][j] == '#':
                current_j = j
            elif transposed[i][j] == 'O':
                current_j -= 1
                idx.append(current_j)

        for j in range(total_cols):
            if j in idx:
                transposed[i][j] = 'O'
            elif transposed[i][j] != '#':
                transposed[i][j] = '.'

    return transpose(transposed)

def tilt_west(matrix: list[list[str]]) -> list[list[str]]:
    total_rows = len(matrix)
    total_cols = len(matrix[0])

    for i in range(total_rows):
        current_j = -1
        idx = []
        for j in range(total_cols):
            if matrix[i][j] == '#':
                current_j = j
            elif matrix[i][j] == 'O':
                current_j += 1
                idx.append(current_j)

        for j in range(total_cols):
            if j in idx:
                matrix[i][j] = 'O'
            elif matrix[i][j] != '#':
                matrix[i][j] = '.'
    return matrix

def do_cycle(matrix: list[list[str]]) -> list[list[str]]:
    new_matrix = tilt_north(matrix)
    new_matrix = tilt_west(new_matrix)
    new_matrix = tilt_south(new_matrix)
    new_matrix = tilt_east(new_matrix)
    return new_matrix

def hash(matrix: list[list[str]]) -> str:
    return ''.join(''.join(i) for i in matrix)

def solve02(data: str):
    matrix = list(list(line) for line in data.split('\n'))

    times = {}
    cache = True

    total = 1_000_000_000
    i = 0
    while i < total:
        matrix = do_cycle(matrix)

        if cache:
            key = hash(matrix)

            if key not in times:
                times[key] = {
                    'idx': None,
                    'count': 0
                }
            times[key]['count'] += 1

            if times[key]['count'] == 2:
                repetitive_count = i - times[key]['idx']
                current_total = total - i
                remaining = current_total % repetitive_count
                i = total - remaining
                i += 1
                cache = False
                continue

            times[key]['idx'] = i

        i += 1

    return summarize(matrix)

if __name__ == "__main__":
    # data = open('day-14-input.test.txt', 'r').read()
    data = open('day-14-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
