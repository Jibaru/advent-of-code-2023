'''
--- Day 13: Point of Incidence ---
With your help, the hot springs team locates an appropriate spring which launches you neatly and precisely up to the edge of Lava Island.

There's just one problem: you don't see any lava.

You do see a lot of ash and igneous rock; there are even what look like gray mountains scattered around. After a while, you make your way to a nearby cluster of mountains only to discover that the valley between them is completely full of large mirrors. Most of the mirrors seem to be aligned in a consistent way; perhaps you should head in that direction?

As you move through the valley of mirrors, you find that several of them have fallen from the large metal frames keeping them in place. The mirrors are extremely flat and shiny, and many of the fallen mirrors have lodged into the ash at strange angles. Because the terrain is all one color, it's hard to tell where it's safe to walk or where you're about to run into a mirror.

You note down the patterns of ash (.) and rocks (#) that you see as you walk (your puzzle input); perhaps by carefully analyzing these patterns, you can figure out where the mirrors are!

For example:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
To find the reflection in each pattern, you need to find a perfect reflection across either a horizontal line between two rows or across a vertical line between two columns.

In the first pattern, the reflection is across a vertical line between two columns; arrows on each of the two columns point at the line between the columns:

123456789
    ><   
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><   
123456789
In this pattern, the line of reflection is the vertical line between columns 5 and 6. Because the vertical line is not perfectly in the middle of the pattern, part of the pattern (column 1) has nowhere to reflect onto and can be ignored; every other column has a reflected column within the pattern and must match exactly: column 2 matches column 9, column 3 matches 8, 4 matches 7, and 5 matches 6.

The second pattern reflects across a horizontal line instead:

1 #...##..# 1
2 #....#..# 2
3 ..##..### 3
4v#####.##.v4
5^#####.##.^5
6 ..##..### 6
7 #....#..# 7
This pattern reflects across the horizontal line between rows 4 and 5. Row 1 would reflect with a hypothetical row 8, but since that's not in the pattern, row 1 doesn't need to match anything. The remaining rows match: row 2 matches row 7, row 3 matches row 6, and row 4 matches row 5.

To summarize your pattern notes, add up the number of columns to the left of each vertical line of reflection; to that, also add 100 multiplied by the number of rows above each horizontal line of reflection. In the above example, the first pattern's vertical line has 5 columns to its left and the second pattern's horizontal line has 4 rows above it, a total of 405.

Find the line of reflection in each of the patterns in your notes. What number do you get after summarizing all of your notes?

Your puzzle answer was 37975.
'''

TYPE_ROW = 'row'
TYPE_COL = 'col'

def summarize(val: tuple[str, int]) -> int:
    type, idx = val

    if type == TYPE_COL:
        return idx + 1

    if type == TYPE_ROW:
        return (idx + 1) * 100

    return -1

def are_equals(matrix, j, k):
    a = tuple(matrix[j])
    b = tuple(matrix[k])

    return a == b

def are_similar(matrix, j, k):
    a = matrix[j]
    b = matrix[k]
    counts = 0

    for i in range(len(a)):
        if a[i] == b[i]:
            counts += 1

    return counts == (len(a) - 1)

def find_reflection_index(matrix: list[list[str]]) -> int:
    nrows = len(matrix)
    
    for i in range(nrows - 1):
        j = i
        k = i + 1
        found = True
        while j >= 0 and k < nrows:
            if not are_equals(matrix, j, k):
                found = False
                break
                    
            j = j - 1
            k = k + 1
        if found:
            return i
    return -1
    
def find_reflection_index_with_smug(matrix: list[list[str]]) -> int:
    nrows = len(matrix)
    
    for i in range(nrows - 1):
        j = i
        k = i + 1
        found = True
        smug_found = False
        while j >= 0 and k < nrows:
            equals = are_equals(matrix, j, k)
            if not equals:
                if not smug_found:
                    if are_similar(matrix, j, k):
                        smug_found = True
                    else:
                        found = False
                        break
                else:
                    found = False
                    break
            j = j - 1
            k = k + 1
        if found and smug_found:
            return i
    return -1
    
    
def get_reflection_idx(matrix: list[list[str]], solution: int) -> tuple[str, int]:
    idx = find_reflection_index(matrix) if solution == 1 else find_reflection_index_with_smug(matrix)
    
    if idx != -1:
        return ('row', idx)
    
    transposed = list(zip(*matrix))
    idx = find_reflection_index(transposed) if solution == 1 else find_reflection_index_with_smug(transposed)
    if idx != -1:
        return ('col', idx)

    return (None, -1)

def solve(data: str, solution: int) -> int:
    matrixes = data.split('\n\n')
    
    ans = 0
    for mtrx in matrixes:
        matrix = list(list(line) for line in mtrx.split('\n'))
        val = get_reflection_idx(matrix, solution)
        ans += summarize(val)

    return ans

def solve01(data: str) -> int:
    return solve(data, 1)
    
'''
--- Part Two ---
You resume walking through the valley of mirrors and - SMACK! - run directly into one. Hopefully nobody was watching, because that must have been pretty embarrassing.

Upon closer inspection, you discover that every mirror has exactly one smudge: exactly one . or # should be the opposite type.

In each pattern, you'll need to locate and fix the smudge that causes a different reflection line to be valid. (The old reflection line won't necessarily continue being valid after the smudge is fixed.)

Here's the above example again:

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
The first pattern's smudge is in the top-left corner. If the top-left # were instead ., it would have a different, horizontal line of reflection:

1 ..##..##. 1
2 ..#.##.#. 2
3v##......#v3
4^##......#^4
5 ..#.##.#. 5
6 ..##..##. 6
7 #.#.##.#. 7
With the smudge in the top-left corner repaired, a new horizontal line of reflection between rows 3 and 4 now exists. Row 7 has no corresponding reflected row and can be ignored, but every other row matches exactly: row 1 matches row 6, row 2 matches row 5, and row 3 matches row 4.

In the second pattern, the smudge can be fixed by changing the fifth symbol on row 2 from . to #:

1v#...##..#v1
2^#...##..#^2
3 ..##..### 3
4 #####.##. 4
5 #####.##. 5
6 ..##..### 6
7 #....#..# 7
Now, the pattern has a different horizontal line of reflection between rows 1 and 2.

Summarize your notes as before, but instead use the new different reflection lines. In this example, the first pattern's new horizontal line has 3 rows above it and the second pattern's new horizontal line has 1 row above it, summarizing to the value 400.

In each pattern, fix the smudge and find the different line of reflection. What number do you get after summarizing the new reflection line in each pattern in your notes?

Your puzzle answer was 32497.
'''

def solve02(data: str) -> int:
    return solve(data, 2)

if __name__ == "__main__":
    # data = open('day-13-input.test.txt', 'r').read()
    data = open('day-13-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
