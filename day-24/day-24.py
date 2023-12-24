import numpy as np

'''
--- Day 24: Never Tell Me The Odds ---
It seems like something is going wrong with the snow-making process. Instead of forming snow, the water that's been absorbed into the air seems to be forming hail!

Maybe there's something you can do to break up the hailstones?

Due to strong, probably-magical winds, the hailstones are all flying through the air in perfectly linear trajectories. You make a note of each hailstone's position and velocity (your puzzle input). For example:

19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
Each line of text corresponds to the position and velocity of a single hailstone. The positions indicate where the hailstones are right now (at time 0). The velocities are constant and indicate exactly how far each hailstone will move in one nanosecond.

Each line of text uses the format px py pz @ vx vy vz. For instance, the hailstone specified by 20, 19, 15 @ 1, -5, -3 has initial X position 20, Y position 19, Z position 15, X velocity 1, Y velocity -5, and Z velocity -3. After one nanosecond, the hailstone would be at 21, 14, 12.

Perhaps you won't have to do anything. How likely are the hailstones to collide with each other and smash into tiny ice crystals?

To estimate this, consider only the X and Y axes; ignore the Z axis. Looking forward in time, how many of the hailstones' paths will intersect within a test area? (The hailstones themselves don't have to collide, just test for intersections between the paths they will trace.)

In this example, look for intersections that happen with an X and Y position each at least 7 and at most 27; in your actual data, you'll need to check a much larger test area. Comparing all pairs of hailstones' future paths produces the following results:

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 18, 19, 22 @ -1, -1, -2
Hailstones' paths will cross inside the test area (at x=14.333, y=15.333).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths will cross inside the test area (at x=11.667, y=16.667).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=6.2, y=19.4).

Hailstone A: 19, 13, 30 @ -2, 1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone A.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 25, 34 @ -2, -2, -4
Hailstones' paths are parallel; they never intersect.

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-6, y=-5).

Hailstone A: 18, 19, 22 @ -1, -1, -2
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 12, 31, 28 @ -1, -2, -1
Hailstones' paths will cross outside the test area (at x=-2, y=3).

Hailstone A: 20, 25, 34 @ -2, -2, -4
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for hailstone B.

Hailstone A: 12, 31, 28 @ -1, -2, -1
Hailstone B: 20, 19, 15 @ 1, -5, -3
Hailstones' paths crossed in the past for both hailstones.
So, in this example, 2 hailstones' future paths cross inside the boundaries of the test area.

However, you'll need to search a much larger test area if you want to see if any hailstones might collide. Look for intersections that happen with an X and Y position each at least 200000000000000 and at most 400000000000000. Disregard the Z axis entirely.

Considering only the X and Y axes, check all pairs of hailstones' future paths for intersections. How many of these intersections occur within the test area?

Your puzzle answer was 17776.
'''

def parse_input(data: str):
    hailstones = []

    for line in data.split('\n'):
        pos, vel = line.split(' @ ')
        x, y, z = pos.split(', ')
        vx, vy, vz = vel.split(', ')

        hailstones.append((
            (int(x), int(y), int(z)),
            (int(vx), int(vy), int(vz))
        ))

    return hailstones

def calculate_slope_and_intersection(a: tuple[int, int], b: tuple[int, int]):
    slope = (b[1] - a[1]) / (b[0] - a[0])
    intersection = a[1] - slope * a[0]

    return slope, intersection

def find_intersection(
    vector_1: tuple[tuple[int, int], tuple[int, int]],
    vector_2: tuple[tuple[int, int], tuple[int, int]]
) -> tuple[int, int]|None:
    slope_1, intersection_1 = calculate_slope_and_intersection(vector_1[0], vector_1[1])
    slope_2, intersection_2 = calculate_slope_and_intersection(vector_2[0], vector_2[1])

    if slope_1 != slope_2:
        x = (intersection_2 - intersection_1) / (slope_1 - slope_2)
        y = slope_1 * x + intersection_1

        vel_x_i = vector_1[1][0] - vector_1[0][0]
        vel_y_i = vector_1[1][1] - vector_1[0][1]

        vel_x_j = vector_2[1][0] - vector_2[0][0]
        vel_y_j = vector_2[1][1] - vector_2[0][1]

        if vel_x_i >= 0:
            if not x >= vector_1[0][0]:
                return None
        else:
            if not x <= vector_1[0][0]:
                return None

        if vel_y_i >= 0:
            if not y >= vector_1[0][1]:
                return None
        else:
            if not y <= vector_1[0][1]:
                return None

        if vel_x_j >= 0:
            if not x >= vector_2[0][0]:
                return None
        else:
            if not x <= vector_2[0][0]:
                return None

        if vel_y_j >= 0:
            if not y >= vector_2[0][1]:
                return None
        else:
            if not y <= vector_2[0][1]:
                return None

        return x, y

    return None

def solve01(data: str) -> int:
    hailstones = parse_input(data)

    vectors = []

    for hailstone in hailstones:
        (x, y, z), (vx, vy, vz) = hailstone
        vectors.append(((x, y), (x + vx, y + vy)))

    lenght = len(vectors)
    min_area = 200000000000000
    max_area = 400000000000000
    ans = 0
    for i in range(lenght):
        for j in range(i + 1, lenght):
            intersection = find_intersection(vectors[i], vectors[j])
            if intersection is not None:
                x, y = intersection

                if (min_area <= x <= max_area and
                    min_area <= y <= max_area):
                    ans += 1

    return ans

'''
--- Part Two ---
Upon further analysis, it doesn't seem like any hailstones will naturally collide. It's up to you to fix that!

You find a rock on the ground nearby. While it seems extremely unlikely, if you throw it just right, you should be able to hit every hailstone in a single throw!

You can use the probably-magical winds to reach any integer position you like and to propel the rock at any integer velocity. Now including the Z axis in your calculations, if you throw the rock at time 0, where do you need to be so that the rock perfectly collides with every hailstone? Due to probably-magical inertia, the rock won't slow down or change direction when it collides with a hailstone.

In the example above, you can achieve this by moving to position 24, 13, 10 and throwing the rock at velocity -3, 1, 2. If you do this, you will hit every hailstone as follows:

Hailstone: 19, 13, 30 @ -2, 1, -2
Collision time: 5
Collision position: 9, 18, 20

Hailstone: 18, 19, 22 @ -1, -1, -2
Collision time: 3
Collision position: 15, 16, 16

Hailstone: 20, 25, 34 @ -2, -2, -4
Collision time: 4
Collision position: 12, 17, 18

Hailstone: 12, 31, 28 @ -1, -2, -1
Collision time: 6
Collision position: 6, 19, 22

Hailstone: 20, 19, 15 @ 1, -5, -3
Collision time: 1
Collision position: 21, 14, 12
Above, each hailstone is identified by its initial position and its velocity. Then, the time and position of that hailstone's collision with your rock are given.

After 1 nanosecond, the rock has exactly the same position as one of the hailstones, obliterating it into ice dust! Another hailstone is smashed to bits two nanoseconds after that. After a total of 6 nanoseconds, all of the hailstones have been destroyed.

So, at time 0, the rock needs to be at X position 24, Y position 13, and Z position 10. Adding these three coordinates together produces 47. (Don't add any coordinates from the rock's velocity.)

Determine the exact position and velocity the rock needs to have at time 0 so that it perfectly collides with every hailstone. What do you get if you add up the X, Y, and Z coordinates of that initial position?

Your puzzle answer was 948978092202212.
'''

def solve02(data: str) -> int:
    hailstones = parse_input(data)

    # Solution based on:
    # https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect
    (p1, v1), (p2, v2), (p3, v3) = hailstones[:3]

    a = np.array([
        [-(v1[1] - v2[1]), v1[0] - v2[0], 0, p1[1] - p2[1], -(p1[0] - p2[0]), 0],
        [-(v1[1] - v3[1]), v1[0] - v3[0], 0, p1[1] - p3[1], -(p1[0] - p3[0]), 0],

        [0, -(v1[2] - v2[2]), v1[1] - v2[1],  0, p1[2] - p2[2], -(p1[1] - p2[1])],
        [0, -(v1[2] - v3[2]), v1[1] - v3[1],  0, p1[2] - p3[2], -(p1[1] - p3[1])],

        [-(v1[2] - v2[2]), 0, v1[0] - v2[0],  p1[2] - p2[2], 0, -(p1[0] - p2[0])],
        [-(v1[2] - v3[2]), 0, v1[0] - v3[0],  p1[2] - p3[2], 0, -(p1[0] - p3[0])]
    ])

    b = np.array([
        (p1[1] * v1[0] - p2[1] * v2[0]) - (p1[0] * v1[1] - p2[0] * v2[1]),
        (p1[1] * v1[0] - p3[1] * v3[0]) - (p1[0] * v1[1] - p3[0] * v3[1]),

        (p1[2] * v1[1] - p2[2] * v2[1]) - (p1[1] * v1[2] - p2[1] * v2[2]),
        (p1[2] * v1[1] - p3[2] * v3[1]) - (p1[1] * v1[2] - p3[1] * v3[2]),

        (p1[2] * v1[0] - p2[2] * v2[0]) - (p1[0] * v1[2] - p2[0] * v2[2]),
        (p1[2] * v1[0] - p3[2] * v3[0]) - (p1[0] * v1[2] - p3[0] * v3[2])
    ])

    x = np.linalg.solve(a, b)

    return round(sum(x[:3]))

if __name__ == "__main__":
    # data = open('day-24-input.test.txt', 'r').read()
    data = open('day-24-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
