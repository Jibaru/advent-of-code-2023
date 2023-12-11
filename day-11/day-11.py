from itertools import combinations

'''
--- Day 11: Cosmic Expansion ---
You continue following signs for "Hot Springs" and eventually come across an observatory. The Elf within turns out to be a researcher studying cosmic expansion using the giant telescope here.

He doesn't know anything about the missing machine parts; he's only visiting for this research project. However, he confirms that the hot springs are the next-closest area likely to have people; he'll even take you straight there once he's done with today's observation analysis.

Maybe you can help him with the analysis to speed things up?

The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input). The image includes empty space (.) and galaxies (#). For example:

...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
The researcher is trying to figure out the sum of the lengths of the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took the light from those galaxies to reach the observatory.

Due to something involving gravitational effects, only some space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice as big.

In the above example, three columns and two rows contain no galaxies:

   v  v  v
 ...#......
 .......#..
 #.........
>..........<
 ......#...
 .#........
 .........#
>..........<
 .......#..
 #...#.....
   ^  ^  ^
These rows and columns need to be twice as big; the result of cosmic expansion therefore looks like this:

....#........
.........#...
#............
.............
.............
........#....
.#...........
............#
.............
.............
.........#...
#....#.......
Equipped with this expanded universe, the shortest path between every pair of galaxies can be found. It can help to assign every galaxy a unique number:

....1........
.........2...
3............
.............
.............
........4....
.5...........
............6
.............
.............
.........7...
8....9.......
In these 9 galaxies, there are 36 pairs. Only count each pair once; order within the pair doesn't matter. For each pair, find any shortest path between the two galaxies using only steps that move up, down, left, or right exactly one . or # at a time. (The shortest path between two galaxies is allowed to pass through another galaxy.)

For example, here is one of the shortest paths between galaxies 5 and 9:

....1........
.........2...
3............
.............
.............
........4....
.5...........
.##.........6
..##.........
...##........
....##...7...
8....9.......
This path has length 9 because it takes a minimum of nine steps to get from galaxy 5 to galaxy 9 (the eight locations marked # plus the step onto galaxy 9 itself). Here are some other example shortest path lengths:

Between galaxy 1 and galaxy 7: 15
Between galaxy 3 and galaxy 6: 17
Between galaxy 8 and galaxy 9: 5
In this example, after expanding the universe, the sum of the shortest path between all 36 pairs of galaxies is 374.

Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

Your puzzle answer was 9647174.
'''

def shortest_path_lenght(a: tuple[int, int], b: tuple[int, int]) -> int:
    x1, y1 = a
    x2, y2 = b

    m = max(x2, x1) - min(x2, x1)
    n = max(y2, y1) - min(y1, y2)

    return m + n

def calculate_sum_of_distances(data: str, constant: int) -> int:
    matrix = list(list(line) for line in data.split('\n'))
    cols = {}
    rows = {}
    
    total_rows = len(matrix)
    total_cols = len(matrix[0])
    
    for i in range(total_rows):
        for j in range(total_cols):
            if matrix[i][j] == '.':
                if i not in rows:
                    rows[i] = 0
                if j not in cols:
                    cols[j] = 0
                rows[i] += 1
                cols[j] += 1
    
    expanded_rows = []
    expanded_cols = []
    for i in rows:
        if rows[i] == total_cols:
            expanded_rows.append(i)
    
    for i in cols:
        if cols[i] == total_rows:
            expanded_cols.append(i)

    points = []
    
    for i in range(total_rows):
        for j in range(total_cols):
            if matrix[i][j] == '#':
                points.append((i, j))

    combinations_of_two = list(combinations(points, 2))

    ans = 0
    constant = constant if constant == 1 else constant - 1

    for a, b in combinations_of_two:
        x1, y1 = a
        x2, y2 = b
        
        new_x1, new_x2, new_y1, new_y2 = x1, x2, y1, y2
        
        for row in expanded_rows:
            if row <= x1:
                new_x1 += constant
            if row <= x2:
                new_x2 += constant
                
        for col in expanded_cols:
            if col <= y1:
                new_y1 += constant
            if col <= y2:
                new_y2 += constant

        ans += shortest_path_lenght((new_x1, new_y1), (new_x2, new_y2))
    
    return ans

def solve01(data: str) -> int:
    return calculate_sum_of_distances(data, 1)

'''
--- Part Two ---
The galaxies are much older (and thus much farther apart) than the researcher initially estimated.

Now, instead of the expansion you did before, make each empty row or column one million times larger. That is, each empty row should be replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.

(In the example above, if each empty row or column were merely 10 times larger, the sum of the shortest paths between every pair of galaxies would be 1030. If each empty row or column were merely 100 times larger, the sum of the shortest paths between every pair of galaxies would be 8410. However, your universe will need to expand far beyond these values.)

Starting with the same initial image, expand the universe according to these new rules, then find the length of the shortest path between every pair of galaxies. What is the sum of these lengths?

Your puzzle answer was 377318892554.
'''

def solve02(data: str) -> int:
    return calculate_sum_of_distances(data, 1_000_000)

if __name__ == "__main__":
    # data = open('day-11-input.test.txt', 'r').read()
    data = open('day-11-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
