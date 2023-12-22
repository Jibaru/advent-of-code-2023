'''
--- Day 22: Sand Slabs ---
Enough sand has fallen; it can finally filter water for Snow Island.

Well, almost.

The sand has been falling as large compacted bricks of sand, piling up to form an impressive stack here near the edge of Island Island. In order to make use of the sand to filter water, some of the bricks will need to be broken apart - nay, disintegrated - back into freely flowing sand.

The stack is tall enough that you'll have to be careful about choosing which bricks to disintegrate; if you disintegrate the wrong brick, large portions of the stack could topple, which sounds pretty dangerous.

The Elves responsible for water filtering operations took a snapshot of the bricks while they were still falling (your puzzle input) which should let you work out which bricks are safe to disintegrate. For example:

1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
Each line of text in the snapshot represents the position of a single brick at the time the snapshot was taken. The position is given as two x,y,z coordinates - one for each end of the brick - separated by a tilde (~). Each brick is made up of a single straight line of cubes, and the Elves were even careful to choose a time for the snapshot that had all of the free-falling bricks at integer positions above the ground, so the whole snapshot is aligned to a three-dimensional cube grid.

A line like 2,2,2~2,2,2 means that both ends of the brick are at the same coordinate - in other words, that the brick is a single cube.

Lines like 0,0,10~1,0,10 or 0,0,10~0,1,10 both represent bricks that are two cubes in volume, both oriented horizontally. The first brick extends in the x direction, while the second brick extends in the y direction.

A line like 0,0,1~0,0,10 represents a ten-cube brick which is oriented vertically. One end of the brick is the cube located at 0,0,1, while the other end of the brick is located directly above it at 0,0,10.

The ground is at z=0 and is perfectly flat; the lowest z value a brick can have is therefore 1. So, 5,5,1~5,6,1 and 0,2,1~0,2,5 are both resting on the ground, but 3,3,2~3,3,3 was above the ground at the time of the snapshot.

Because the snapshot was taken while the bricks were still falling, some bricks will still be in the air; you'll need to start by figuring out where they will end up. Bricks are magically stabilized, so they never rotate, even in weird situations like where a long horizontal brick is only supported on one end. Two bricks cannot occupy the same position, so a falling brick will come to rest upon the first other brick it encounters.

Here is the same example again, this time with each brick given a letter so it can be marked in diagrams:

1,0,1~1,2,1   <- A
0,0,2~2,0,2   <- B
0,2,3~2,2,3   <- C
0,0,4~0,2,4   <- D
2,0,5~2,2,5   <- E
0,1,6~2,1,6   <- F
1,1,8~1,1,9   <- G
At the time of the snapshot, from the side so the x axis goes left to right, these bricks are arranged like this:

 x
012
.G. 9
.G. 8
... 7
FFF 6
..E 5 z
D.. 4
CCC 3
BBB 2
.A. 1
--- 0
Rotating the perspective 90 degrees so the y axis now goes left to right, the same bricks are arranged like this:

 y
012
.G. 9
.G. 8
... 7
.F. 6
EEE 5 z
DDD 4
..C 3
B.. 2
AAA 1
--- 0
Once all of the bricks fall downward as far as they can go, the stack looks like this, where ? means bricks are hidden behind other bricks at that location:

 x
012
.G. 6
.G. 5
FFF 4
D.E 3 z
??? 2
.A. 1
--- 0
Again from the side:

 y
012
.G. 6
.G. 5
.F. 4
??? 3 z
B.C 2
AAA 1
--- 0
Now that all of the bricks have settled, it becomes easier to tell which bricks are supporting which other bricks:

Brick A is the only brick supporting bricks B and C.
Brick B is one of two bricks supporting brick D and brick E.
Brick C is the other brick supporting brick D and brick E.
Brick D supports brick F.
Brick E also supports brick F.
Brick F supports brick G.
Brick G isn't supporting any bricks.
Your first task is to figure out which bricks are safe to disintegrate. A brick can be safely disintegrated if, after removing it, no other bricks would fall further directly downward. Don't actually disintegrate any bricks - just determine what would happen if, for each brick, only that brick were disintegrated. Bricks can be disintegrated even if they're completely surrounded by other bricks; you can squeeze between bricks if you need to.

In this example, the bricks can be disintegrated as follows:

Brick A cannot be disintegrated safely; if it were disintegrated, bricks B and C would both fall.
Brick B can be disintegrated; the bricks above it (D and E) would still be supported by brick C.
Brick C can be disintegrated; the bricks above it (D and E) would still be supported by brick B.
Brick D can be disintegrated; the brick above it (F) would still be supported by brick E.
Brick E can be disintegrated; the brick above it (F) would still be supported by brick D.
Brick F cannot be disintegrated; the brick above it (G) would fall.
Brick G can be disintegrated; it does not support any other bricks.
So, in this example, 5 bricks can be safely disintegrated.

Figure how the blocks will settle based on the snapshot. Once they've settled, consider disintegrating a single brick; how many bricks could be safely chosen as the one to get disintegrated?

Your puzzle answer was 505.
'''

X_INDEX = 0
Y_INDEX = 1
Z_INDEX = 2

def orientation(p: tuple[int, int], q: tuple[int, int], r: tuple[int, int]) -> int:
    val = (q[Y_INDEX] - p[Y_INDEX]) * (r[X_INDEX] - q[X_INDEX]) - (q[X_INDEX] - p[X_INDEX]) * (r[Y_INDEX] - q[Y_INDEX])
    if val == 0:
        return 0
    return 1 if val > 0 else -1

def on_segment(p: tuple[int, int], q: tuple[int, int], r: tuple[int, int]) -> bool:
    return (q[X_INDEX] <= max(p[X_INDEX], r[X_INDEX]) and q[X_INDEX] >= min(p[X_INDEX], r[X_INDEX]) and
            q[Y_INDEX] <= max(p[Y_INDEX], r[Y_INDEX]) and q[Y_INDEX] >= min(p[Y_INDEX], r[Y_INDEX]))

class Brick:
    def __init__(self, first: tuple[int, int, int], second: tuple[int, int, int]) -> None:
        self.first = first
        self.second = second
        self.lowest_z = min(first[Z_INDEX], second[Z_INDEX])
        self.highest_z = max(first[Z_INDEX], second[Z_INDEX])
        self.bricks_it_supports = []
        self.base_bricks = []
        self.name = f'{first}~{second}'

    def min_max(self) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
        if self.first[Z_INDEX] < self.second[Z_INDEX]:
            return self.first, self.second
        return self.second, self.first

    def z_units(self) -> int:
        return abs(self.first[Z_INDEX] - self.second[Z_INDEX])

    def __repr__(self) -> str:
        return self.name

    def intersects_in_x_or_y(self, other) -> bool:
        p1, q1 = (self.first, self.second)
        p2, q2 = (other.first, other.second)

        o1 = orientation(p1, q1, p2)
        o2 = orientation(p1, q1, q2)
        o3 = orientation(p2, q2, p1)
        o4 = orientation(p2, q2, q1)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and on_segment(p1, p2, q1):
            return True
        if o2 == 0 and on_segment(p1, q2, q1):
            return True
        if o3 == 0 and on_segment(p2, p1, q2):
            return True
        if o4 == 0 and on_segment(p2, q1, q2):
            return True

        return False

    def add_to_bricks_it_supports(self, brick):
        self.bricks_it_supports.append(brick)

    def add_base_brick(self, brick):
        self.base_bricks.append(brick)

    def total_bricks_it_support(self) -> int:
        return len(self.bricks_it_supports)

def parse_bricks(data: str) -> list[Brick]:
    bricks = []

    for line in data.split('\n'):
        a, b = line.split('~')
        a = a.split(',')
        b = b.split(',')
        
        bricks.append(Brick((int(a[0]), int(a[1]), int(a[2])), (int(b[0]), int(b[1]), int(b[2]))))
    return bricks

def determine_bricks_on_final_state(bricks: list[Brick]) -> list[Brick]:
    sorted_bricks = sorted(bricks, key=lambda brick: brick.lowest_z)
    bricks_on_final_state = []

    for brick in sorted_bricks:
        max_z = 1
        base_bricks = []

        for brick_on_final_state in bricks_on_final_state:
            if brick.intersects_in_x_or_y(brick_on_final_state):
                if brick_on_final_state.highest_z > max_z:
                    max_z = brick_on_final_state.highest_z
                    base_bricks = [brick_on_final_state]
                elif brick_on_final_state.highest_z == max_z:
                    base_bricks.append(brick_on_final_state)

        first, second = brick.min_max()
        max_z = max_z + 1 if len(base_bricks) > 0 else 1

        new_brick_on_final_state = Brick(
            (first[X_INDEX], first[Y_INDEX], max_z),
            (second[X_INDEX], second[Y_INDEX], max_z + brick.z_units())
        )

        for base_brick in base_bricks:
            base_brick.add_to_bricks_it_supports(new_brick_on_final_state)
            new_brick_on_final_state.add_base_brick(base_brick)

        bricks_on_final_state.append(new_brick_on_final_state)

    return bricks_on_final_state

def solve01(data: str) -> int:
    bricks = parse_bricks(data)
    bricks_on_final_state = determine_bricks_on_final_state(bricks)

    ans = 0
    for brick in bricks_on_final_state:
        if brick.total_bricks_it_support() == 0:
            ans += 1
            continue

        total = 1
        for brick_on_top in brick.bricks_it_supports:
            if len(brick_on_top.base_bricks) <= 1:
                total = 0
                break
        ans += total

    return ans

'''
--- Part Two ---
Disintegrating bricks one at a time isn't going to be fast enough. While it might sound dangerous, what you really need is a chain reaction.

You'll need to figure out the best brick to disintegrate. For each brick, determine how many other bricks would fall if that brick were disintegrated.

Using the same example as above:

Disintegrating brick A would cause all 6 other bricks to fall.
Disintegrating brick F would cause only 1 other brick, G, to fall.
Disintegrating any other brick would cause no other bricks to fall. So, in this example, the sum of the number of other bricks that would fall as a result of disintegrating each brick is 7.

For each brick, determine how many other bricks would fall if that brick were disintegrated. What is the sum of the number of other bricks that would fall?

Your puzzle answer was 71002.
'''

def solve02(data: str) -> int:
    bricks = parse_bricks(data)    
    bricks_on_final_state = determine_bricks_on_final_state(bricks)

    def count_fall(brick: Brick, fell_brick_names: set) -> int:
        if brick.total_bricks_it_support() == 0:
            return 0

        total = 0

        for top_brick in brick.bricks_it_supports:
            bricks_fell_count = 0
            for base_brick_of_top in top_brick.base_bricks:
                if base_brick_of_top.name in fell_brick_names:
                    bricks_fell_count += 1

            if len(top_brick.base_bricks) - bricks_fell_count == 1:
                total += count_fall(top_brick, fell_brick_names) + 1
                fell_brick_names.add(top_brick.name)

        return total

    ans = 0
    for brick in bricks_on_final_state:
        ans += count_fall(brick, set())

    return ans

if __name__ == "__main__":
    # data = open('day-22-input.test.txt', 'r').read()
    data = open('day-22-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
