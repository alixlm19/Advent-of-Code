"""
The ferry quickly brings you across Island Island. After asking around, you discover that there is indeed normally a large pile of sand somewhere near here, but you don't see anything besides lots of water and the small island where the ferry has docked.

As you try to figure out what to do next, you notice a poster on a wall near the ferry dock. "Boat races! Open to the public! Grand prize is an all-expenses-paid trip to Desert Island!" That must be where the sand comes from! Best of all, the boat races are starting in just a few minutes.

You manage to sign up as a competitor in the boat races just in time. The organizer explains that it's not really a traditional race - instead, you will get a fixed amount of time during which your boat has to travel as far as it can, and you win if your boat goes the farthest.

As part of signing up, you get a sheet of paper (your puzzle input) that lists the time allowed for each race and also the best distance ever recorded in that race. To guarantee you win the grand prize, you need to make sure you go farther in each race than the current record holder.

The organizer brings you over to the area where the boat races are held. The boats are much smaller than you expected - they're actually toy boats, each with a big button on top. Holding down the button charges the boat, and releasing the button allows the boat to move. Boats move faster if their button was held longer, but time spent holding the button counts against the total race time. You can only hold the button at the start of the race, and boats don't move until the button is released.

For example:

Time:      7  15   30
Distance:  9  40  200
This document describes three races:

The first race lasts 7 milliseconds. The record distance in this race is 9 millimeters.
The second race lasts 15 milliseconds. The record distance in this race is 40 millimeters.
The third race lasts 30 milliseconds. The record distance in this race is 200 millimeters.
Your toy boat has a starting speed of zero millimeters per millisecond. For each whole millisecond you spend at the beginning of the race holding down the button, the boat's speed increases by one millimeter per millisecond.

So, because the first race lasts 7 milliseconds, you only have a few options:

Don't hold the button at all (that is, hold it for 0 milliseconds) at the start of the race. The boat won't move; it will have traveled 0 millimeters by the end of the race.
Hold the button for 1 millisecond at the start of the race. Then, the boat will travel at a speed of 1 millimeter per millisecond for 6 milliseconds, reaching a total distance traveled of 6 millimeters.
Hold the button for 2 milliseconds, giving the boat a speed of 2 millimeters per millisecond. It will then get 5 milliseconds to move, reaching a total distance of 10 millimeters.
Hold the button for 3 milliseconds. After its remaining 4 milliseconds of travel time, the boat will have gone 12 millimeters.
Hold the button for 4 milliseconds. After its remaining 3 milliseconds of travel time, the boat will have gone 12 millimeters.
Hold the button for 5 milliseconds, causing the boat to travel a total of 10 millimeters.
Hold the button for 6 milliseconds, causing the boat to travel a total of 6 millimeters.
Hold the button for 7 milliseconds. That's the entire duration of the race. You never let go of the button. The boat can't move until you let go of the button. Please make sure you let go of the button so the boat gets to move. 0 millimeters.
Since the current record for this race is 9 millimeters, there are actually 4 different ways you could win: you could hold the button for 2, 3, 4, or 5 milliseconds at the start of the race.

In the second race, you could hold the button for at least 4 milliseconds and at most 11 milliseconds and beat the record, a total of 8 different ways to win.

In the third race, you could hold the button for at least 11 milliseconds and no more than 19 milliseconds and still beat the record, a total of 9 ways you could win.

To see how much margin of error you have, determine the number of ways you can beat the record in each race; in this example, if you multiply these values together, you get 288 (4 * 8 * 9).

Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers together?
"""
from utils import utils
from math import floor, ceil
import re


def solve_quadratic_equation(a: int, b: int, c: int) -> float:
    """
    Solves a quadratic equation of the form ax^2 + bx + c = 0.

    Args:
        a (int): Coefficient of x^2.
        b (int): Coefficient of x.
        c (int): Constant term.

    Returns:
        Tuple[float, float]: The two solutions of the quadratic equation.
    """

    # Discriminant
    d: float = (b**2) - (4 * a * c)

    x_0: float = (-b + (d**0.5)) / (2 * a)
    x_1: float = (-b - (d**0.5)) / (2 * a)

    return x_0, x_1


def calculate_displacement_bounds(
    max_time: int, target_displacement: int, epsilon: float = 1e-3
) -> int:
    """
    Calculates the minimum and maximum bounds of displacement for a given maximum time and target displacement.

    Args:
        max_time (int): The maximum time.
        target_displacement (int): The target displacement.
        epsilon (float, optional): The tolerance value for solving quadratic equations. Defaults to 1e-3.

    Returns:
        Tuple[int, int]: A tuple containing the minimum and maximum bounds of displacement.
    """

    min_bound_1: int = 0
    max_bound_1: int = 0
    min_bound_1, max_bound_1 = solve_quadratic_equation(
        1, max_time, target_displacement - epsilon
    )

    min_bound_1 = abs(floor(min_bound_1))
    max_bound_1 = abs(ceil(max_bound_1))

    min_bound_2, max_bound_2 = solve_quadratic_equation(
        1, max_time, target_displacement + epsilon
    )

    min_bound_2 = abs(floor(min_bound_2))
    max_bound_2 = abs(ceil(max_bound_2))

    min_bound: int = max(min_bound_1, min_bound_2)
    max_bound: int = min(max_bound_1, max_bound_2)

    return min_bound, max_bound


def calculate_margin_of_error(races: [[int, int]]):
    """
    Calculates the margin of error for a list of races.

    Args:
        races (list): A list of tuples representing the maximum time and target displacement for each race.

    Returns:
        int: The calculated margin of error.
    """

    margin_of_error: int = 1

    for max_time, target_displacement in races:
        bounds: [int, int] = calculate_displacement_bounds(
            max_time, target_displacement
        )
        bound_width: int = bounds[1] - bounds[0] + 1

        margin_of_error *= bound_width

    return margin_of_error


def parse_lines(lines: [str], adjusted_for_bad_kerning=False) -> [[int, int]]:
    """
    Parses the lines of input and returns a list of tuples containing the parsed values.

    Args:
        lines (list[str]): The lines of input to parse.
        adjusted_for_bad_kerning (bool, optional): Flag indicating whether the input has been adjusted for bad kerning. Defaults to False.

    Returns:
        list[list[int, int]]: A list of tuples containing the parsed values.
    """
    times_raw: str = re.findall(r"\d+", lines[0])
    distances_raw: str = re.findall(r"\d+", lines[1])

    if adjusted_for_bad_kerning:
        times_raw = ["".join(times_raw)]
        distances_raw = ["".join(distances_raw)]

    times: [int] = [int(time) for time in times_raw]
    distances: [int] = [int(dist) for dist in distances_raw]

    return list(zip(times, distances))


if __name__ == "__main__":
    test: bool = False
    lines: [str] = utils.read_lines("day_6-data.txt", test=test)

    races_with_bad_kerning: [[int, int]] = parse_lines(lines)
    print(f"{races_with_bad_kerning=}")
    races_without_bad_kerning: [[int, int]] = parse_lines(
        lines, adjusted_for_bad_kerning=True
    )
    print(f"{races_without_bad_kerning=}")

    margin_of_error_with_bad_kerning: int = calculate_margin_of_error(
        races_with_bad_kerning
    )
    margin_of_error_without_bad_kerning: int = calculate_margin_of_error(
        races_without_bad_kerning
    )

    print(f"{margin_of_error_with_bad_kerning=}")
    print(f"{margin_of_error_without_bad_kerning=}")
