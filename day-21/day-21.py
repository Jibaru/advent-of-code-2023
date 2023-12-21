from collections import deque

'''
--- Day 21: Step Counter ---
You manage to catch the airship right as it's dropping someone else off on their all-expenses-paid trip to Desert Island! It even helpfully drops you off near the gardener and his massive farm.

"You got the sand flowing again! Great work! Now we just need to wait until we have enough sand to filter the water for Snow Island and we'll have snow again in no time."

While you wait, one of the Elves that works with the gardener heard how good you are at solving problems and would like your help. He needs to get his steps in for the day, and so he'd like to know which garden plots he can reach with exactly his remaining 64 steps.

He gives you an up-to-date map (your puzzle input) of his starting position (S), garden plots (.), and rocks (#). For example:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
The Elf starts at the starting position (S) which also counts as a garden plot. Then, he can take one step north, south, east, or west, but only onto tiles that are garden plots. This would allow him to reach any of the tiles marked O:

...........
.....###.#.
.###.##..#.
..#.#...#..
....#O#....
.##.OS####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
Then, he takes a second step. Since at this point he could be at either tile marked O, his second step would allow him to reach any garden plot that is one step north, south, east, or west of any tile that he could have reached after the first step:

...........
.....###.#.
.###.##..#.
..#.#O..#..
....#.#....
.##O.O####.
.##.O#...#.
.......##..
.##.#.####.
.##..##.##.
...........
After two steps, he could be at any of the tiles marked O above, including the starting position (either by going north-then-south or by going west-then-east).

A single third step leads to even more possibilities:

...........
.....###.#.
.###.##..#.
..#.#.O.#..
...O#O#....
.##.OS####.
.##O.#...#.
....O..##..
.##.#.####.
.##..##.##.
...........
He will continue like this until his steps for the day have been exhausted. After a total of 6 steps, he could reach any of the garden plots marked O:

...........
.....###.#.
.###.##.O#.
.O#O#O.O#..
O.O.#.#.O..
.##O.O####.
.##.O#O..#.
.O.O.O.##..
.##.#.####.
.##O.##.##.
...........
In this example, if the Elf's goal was to get exactly 6 more steps today, he could use them to reach any of 16 garden plots.

However, the Elf actually needs to get 64 steps today, and the map he's handed you is much larger than the example map.

Starting from the garden plot marked S on your map, how many garden plots could the Elf reach in exactly 64 steps?

Your puzzle answer was 3562.
'''

def in_bounds(i: int, j: int, matrix: list[str]) -> bool:
    return i >= 0 and j >= 0 and i < len(matrix) and j < len(matrix[0])            

def count_garden_plots(start_row: int, start_col: int, steps: int, matrix: list[str]) -> int:
    garden_plots_reached = set()
    visited = {(start_row, start_col)}
    queue = deque([(start_row, start_col, steps)])

    while queue:
        i, j, remaining_steps = queue.popleft()

        if remaining_steps % 2 == 0:
            garden_plots_reached.add((i, j))
        if remaining_steps == 0:
            continue

        for x, y in [(1, 0), (- 1, 0), (0, 1), (0, -1)]:
            di = x + i
            dj = y + j

            if not in_bounds(di, dj, matrix) or matrix[di][dj] == "#" or (di, dj) in visited:
                continue

            visited.add((di, dj))
            queue.append((di, dj, remaining_steps - 1))

    return len(garden_plots_reached)

def find_start(matrix: list[str]) -> tuple[int, int]:
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] == 'S':
                return (i, j)

    return (-1, -1)

def solve01(data: str) -> int:
    matrix = list(list(line) for line in data.split('\n'))
    start_row, start_col = find_start(matrix)
    return count_garden_plots(start_row, start_col, 64, matrix)

'''
--- Part Two ---
The Elf seems confused by your answer until he realizes his mistake: he was reading from a list of his favorite numbers that are both perfect squares and perfect cubes, not his step counter.

The actual number of steps he needs to get today is exactly 26501365.

He also points out that the garden plots and rocks are set up so that the map repeats infinitely in every direction.

So, if you were to look one additional map-width or map-height out from the edge of the example map above, you would find that it keeps repeating:

.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##..S####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
.................................
.....###.#......###.#......###.#.
.###.##..#..###.##..#..###.##..#.
..#.#...#....#.#...#....#.#...#..
....#.#........#.#........#.#....
.##...####..##...####..##...####.
.##..#...#..##..#...#..##..#...#.
.......##.........##.........##..
.##.#.####..##.#.####..##.#.####.
.##..##.##..##..##.##..##..##.##.
.................................
This is just a tiny three-map-by-three-map slice of the inexplicably-infinite farm layout; garden plots and rocks repeat as far as you can see. The Elf still starts on the one middle tile marked S, though - every other repeated S is replaced with a normal garden plot (.).

Here are the number of reachable garden plots in this new infinite version of the example map for different numbers of steps:

In exactly 6 steps, he can still reach 16 garden plots.
In exactly 10 steps, he can reach any of 50 garden plots.
In exactly 50 steps, he can reach 1594 garden plots.
In exactly 100 steps, he can reach 6536 garden plots.
In exactly 500 steps, he can reach 167004 garden plots.
In exactly 1000 steps, he can reach 668697 garden plots.
In exactly 5000 steps, he can reach 16733044 garden plots.
However, the step count the Elf needs is much larger! Starting from the garden plot marked S on your infinite map, how many garden plots could the Elf reach in exactly 26501365 steps?

Your puzzle answer was 592723929260582.
'''

def solve02(data: str) -> int:
    matrix = list(list(line) for line in data.split('\n'))
    start_row, start_col = find_start(matrix)
    
    assert len(matrix) == len(matrix[0])

    size = len(matrix)
    steps = 26501365

    assert start_row == start_col == size // 2
    assert steps % size == size // 2

    grid_width = steps // size - 1

    odd = (grid_width // 2 * 2 + 1) ** 2
    even = ((grid_width + 1) // 2 * 2) ** 2

    odd_points = count_garden_plots(start_row, start_col, size * 2 + 1, matrix)
    even_points = count_garden_plots(start_row, start_col, size * 2, matrix)

    corner_t = count_garden_plots(size - 1, start_col, size - 1, matrix)
    corner_r = count_garden_plots(start_row, 0, size - 1, matrix)
    corner_b = count_garden_plots(0, start_col, size - 1, matrix)
    corner_l = count_garden_plots(start_row, size - 1, size - 1, matrix)

    small_tr = count_garden_plots(size - 1, 0, size // 2 - 1, matrix)
    small_tl = count_garden_plots(size - 1, size - 1, size // 2 - 1, matrix)
    small_br = count_garden_plots(0, 0, size // 2 - 1, matrix)
    small_bl = count_garden_plots(0, size - 1, size // 2 - 1, matrix)

    large_tr = count_garden_plots(size - 1, 0, size * 3 // 2 - 1, matrix)
    large_tl = count_garden_plots(size - 1, size - 1, size * 3 // 2 - 1, matrix)
    large_br = count_garden_plots(0, 0, size * 3 // 2 - 1, matrix)
    large_bl = count_garden_plots(0, size - 1, size * 3 // 2 - 1, matrix)

    return (
        odd * odd_points +
        even * even_points +
        corner_t + corner_r + corner_b + corner_l +
        (grid_width + 1) * (small_tr + small_tl + small_br + small_bl) +
        grid_width * (large_tr + large_tl + large_br + large_bl)
    )

if __name__ == "__main__":
    # data = open('day-21-input.test.txt', 'r').read()
    data = open('day-21-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
