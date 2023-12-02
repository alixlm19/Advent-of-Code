"""
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

Your puzzle answer was 54304.

The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".

Equipped with this new information, you now need to find the real first and last digit on each line. For example:
"""

def read_input():
    """
    Read the input file and return a list of lines.

    Returns:
        list: A list of strings representing each line in the input file.
    """
    lines: [str] = []
    with open('./data/day_1-data.txt', 'r') as f:
        lines = f.readlines()

    return lines

def get_first_matching_digit(
        string: str,
        right_to_left: bool = False,
        include_cardinal_digits: bool = False
    ) -> int:
    """
    Returns the first matching digit found in the given string.
    
    Args:
        string (str): The input string to search for a matching digit.
        right_to_left (bool, optional): Specifies whether to search the string from right to left. Defaults to False.
        include_cardinal_digits (bool, optional): Specifies whether to include cardinal digits (one, two, three, etc.) in the search. Defaults to False.
    
    Returns:
        int: The first matching digit found in the string. Returns 0 if no matching digit is found.
    """
    
    num: int = 0

    if right_to_left:
        iterator = reversed(string)
    else:
        iterator = iter(string)

    for i, char in enumerate(iterator):
        if char.isnumeric():
            num = int(char)
        elif include_cardinal_digits:

            index: int = i
            if right_to_left:
                index = len(string) - index - 1

            match char:
                case 'o':
                    if index + 3 <= len(string) and string[index:index+3] == "one":
                        num = 1
                case 't':
                    if index + 3 <= len(string) and string[index:index+3] == "two":
                        num = 2
                    elif index + 5 <= len(string) and string[index:index+5] == "three":
                        num = 3
                case 'f':
                    if index + 4 <= len(string):
                        if string[index:index+4] == "four":
                            num = 4
                        elif string[index:index+4] == "five":
                            num = 5
                case 's':
                    if index + 3 <= len(string) and string[index:index+3] == "six":
                        num = 6
                    elif index + 5 <= len(string) and string[index:index+5] == "seven":
                        num = 7
                case 'e':
                    if index + 5 <= len(string) and string[index:index+5] == "eight":
                        num = 8
                case 'n':
                    if index + 4 <= len(string) and string[index:index+4] == "nine":
                        num = 9
        
        if num:
            break

    return num

def get_calibration_value(lines: [str], include_cardinal_digits = False):
    """
    Calculate the calibration value based on the given lines of digits.

    Args:
        lines (list[str]): A list of strings representing the lines of digits.
        include_cardinal_digits (bool, optional): Whether to include cardinal digits in the calculation. Defaults to False.

    Returns:
        int: The calibration value.
    """
    sum_: int = 0

    for line in lines:
        num_1: int = 0
        num_2: int = 0

        num_1 = get_first_matching_digit(line, False, include_cardinal_digits)
        num_2 = get_first_matching_digit(line, True, include_cardinal_digits)

        sum_ += num_1 * 10 + num_2


    print("The Calibration value " + 
          f"with{'' if include_cardinal_digits else 'out'} cardinal digits is: {sum_}")
    return sum_

if __name__ == "__main__":
    lines = read_input()

    # Part 1
    assert get_calibration_value(lines) == 54304
    # Part 2
    assert get_calibration_value(lines, include_cardinal_digits=True) == 54418