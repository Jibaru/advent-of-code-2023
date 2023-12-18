'''
--- Day 18: Lavaduct Lagoon ---
Thanks to your efforts, the machine parts factory is one of the first factories up and running since the lavafall came back. However, to catch up with the large backlog of parts requests, the factory will also need a large supply of lava for a while; the Elves have already started creating a large lagoon nearby for this purpose.

However, they aren't sure the lagoon will be big enough; they've asked you to take a look at the dig plan (your puzzle input). For example:

R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
The digger starts in a 1 meter cube hole in the ground. They then dig the specified number of meters up (U), down (D), left (L), or right (R), clearing full 1 meter cubes as they go. The directions are given as seen from above, so if "up" were north, then "right" would be east, and so on. Each trench is also listed with the color that the edge of the trench should be painted as an RGB hexadecimal color code.

When viewed from above, the above example dig plan would result in the following loop of trench (#) having been dug out from otherwise ground-level terrain (.):

#######
#.....#
###...#
..#...#
..#...#
###.###
#...#..
##..###
.#....#
.######
At this point, the trench could contain 38 cubic meters of lava. However, this is just the edge of the lagoon; the next step is to dig out the interior so that it is one meter deep as well:

#######
#######
#######
..#####
..#####
#######
#####..
#######
.######
.######
Now, the lagoon can contain a much more respectable 62 cubic meters of lava. While the interior is dug out, the edges are also painted according to the color codes in the dig plan.

The Elves are concerned the lagoon won't be large enough; if they follow their dig plan, how many cubic meters of lava could it hold?

Your puzzle answer was 108909.
'''

def area_by_shoelace(points_in_clock_order: list[tuple[int, int]]) -> float:
        size = len(points_in_clock_order)
        area = 0
        i = 0

        while i < size:
            x1, y1 = points_in_clock_order[i]
            x2, y2 = points_in_clock_order[(i + 1) % size]

            area += (x1 * y2 - x2 * y1)
            i += 1

        return abs(area) / 2.0

def points_inside_by_picks_theorem(area: float, number_of_points: int) -> int:
    return int(area + 1 - (number_of_points / 2))

def calculate_cubic_meters(dig_plan: list[tuple[str, int]]) -> int:
    initial = (0, 0)
    current = (0, 0)
    points = [current]
    total_points = 0

    for dir, steps in dig_plan:
        total_points += steps
        if dir == 'U':
            current = (current[0] - steps, current[1])
        elif dir == 'D':
            current = (current[0] + steps, current[1])
        elif dir == 'R':
            current = (current[0], current[1] + steps)
        elif dir == 'L':
            current = (current[0], current[1] - steps)

        if current == initial:
            break

        points.append(current)

    area = area_by_shoelace(points)
    return points_inside_by_picks_theorem(area, total_points) + total_points

def solve01(data: str) -> int:
    dig_plan = list(line.split(' ') for line in data.split('\n'))

    new_dig_plan = []
    for dir, steps, _ in dig_plan:
        new_dig_plan.append((dir, int(steps)))

    return calculate_cubic_meters(new_dig_plan)

'''
--- Part Two ---
The Elves were right to be concerned; the planned lagoon would be much too small.

After a few minutes, someone realizes what happened; someone swapped the color and instruction parameters when producing the dig plan. They don't have time to fix the bug; one of them asks if you can extract the correct instructions from the hexadecimal codes.

Each hexadecimal code is six hexadecimal digits long. The first five hexadecimal digits encode the distance in meters as a five-digit hexadecimal number. The last hexadecimal digit encodes the direction to dig: 0 means R, 1 means D, 2 means L, and 3 means U.

So, in the above example, the hexadecimal codes can be converted into the true instructions:

#70c710 = R 461937
#0dc571 = D 56407
#5713f0 = R 356671
#d2c081 = D 863240
#59c680 = R 367720
#411b91 = D 266681
#8ceee2 = L 577262
#caa173 = U 829975
#1b58a2 = L 112010
#caa171 = D 829975
#7807d2 = L 491645
#a77fa3 = U 686074
#015232 = L 5411
#7a21e3 = U 500254
Digging out this loop and its interior produces a lagoon that can hold an impressive 952408144115 cubic meters of lava.

Convert the hexadecimal color codes into the correct instructions; if the Elves follow this new dig plan, how many cubic meters of lava could the lagoon hold?

Your puzzle answer was 133125706867777.
'''

def solve02(data: str) -> int:
    dig_plan = list(line.split(' ') for line in data.split('\n'))

    DIRS_BY_NUMBER = {
        '0': 'R',
        '1': 'D',
        '2': 'L',
        '3': 'U',
    }

    new_dig_plan = []

    for _, _, color in dig_plan:
        color = color[1:8]

        dir = DIRS_BY_NUMBER[color[6]]
        steps = int(color[1:6], 16)

        new_dig_plan.append((dir, steps))

    return calculate_cubic_meters(new_dig_plan)

if __name__ == "__main__":
    # data = open('day-18-input.test.txt', 'r').read()
    data = open('day-18-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
