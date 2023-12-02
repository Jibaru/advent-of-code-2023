'''
--- Day 1: Trebuchet?! ---
Something is wrong with global snow production, and you've been selected to take a look. The Elves have even given you a map; on it, they've used stars to mark the top fifty locations that are likely to be having problems.

You've been doing this long enough to know that to restore snow operations, you need to check all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

You try to ask why they can't just use a weather machine ("not powerful enough") and where they're even sending you ("the sky") and why your map looks mostly blank ("you sure ask a lot of questions") and hang on did you just say the sky ("of course, where do you think snow comes from") when you realize that the Elves are already loading you into a trebuchet ("please hold still, we need to strap you in").

As they're making the final adjustments, they discover that their calibration document (your puzzle input) has been amended by a very young Elf who was apparently just excited to show off her art skills. Consequently, the Elves are having trouble reading the values on the document.

The newly-improved calibration document consists of lines of text; each line originally contained a specific calibration value that the Elves now need to recover. On each line, the calibration value can be found by combining the first digit and the last digit (in that order) to form a single two-digit number.

For example:

1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
In this example, the calibration values of these four lines are 12, 38, 15, and 77. Adding these together produces 142.

Consider your entire calibration document. What is the sum of all of the calibration values?

Your puzzle answer was 54708.
'''

def solve01(data):
    numbers = ['1','2', '3', '4', '5', '6', '7', '8', '9']
    ans = 0

    for line in data.split('\n'):
        lenght = len(line)

        if lenght == 0:
            continue
        
        num = ''

        for i in range(lenght):
            if line[i] in numbers:
                a = line[i]
                num = a 
                break

        for j in range(lenght - 1, -1, -1):
            if line[j] in numbers:
                b = line[j]
                num = num + b
                break
        ans += int(num)

    return ans
    
'''
--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:

two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
In this example, the calibration values are 29, 83, 13, 24, 42, 14, and 76. Adding these together produces 281.

What is the sum of all of the calibration values?

Your puzzle answer was 54087.
'''

def solve02(data):
    numbers = ['1','2', '3', '4', '5', '6', '7', '8', '9']
    nums_in_letters = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
    }
    
    reversed_num_in_letters = {
        'eno': '1',
        'owt': '2',
        'eerht': '3',
        'ruof': '4',
        'evif': '5',
        'xis': '6',
        'neves': '7',
        'thgie': '8',
        'enin': '9'
    }
    
    ans = 0
    
    for line in data.split('\n'):
        lenght = len(line)
        if lenght == 0:
            continue
        first_idx = 9999999999
        second_idx = 9999999999
        
        first_digit = ''
        second_digit = ''

        for i in range(lenght):
            if line[i] in numbers:
                first_idx = i
                first_digit = line[i]
                break

        for num_in_letter in nums_in_letters:
            idx = line.find(num_in_letter)

            if idx != -1 and idx < first_idx:
                first_digit = nums_in_letters[num_in_letter]
                first_idx = idx

        reverse = ''.join(reversed(line))

        for j in range(lenght):
            if reverse[j] in numbers:
                second_idx = j
                second_digit = reverse[j]
                break

        for num_in_letter in reversed_num_in_letters:
            idx = reverse.find(num_in_letter)

            if idx != -1 and idx < second_idx:
                second_digit = reversed_num_in_letters[num_in_letter]
                second_idx = idx

        ans += int(first_digit + second_digit)

    return ans

if __name__ == "__main__":
    # data = open('day-1-input.test.txt', 'r').read()
    # data = open('day-1-input-2.test.txt', 'r').read()
    data = open('day-1-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
