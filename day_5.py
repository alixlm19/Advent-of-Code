"""
--- Day 5: If You Give A Seed A Fertilizer ---
You take the boat and find the gardener right where you were told he would be: managing a giant "garden" that looks more to you like a farm.

"A water source? Island Island is the water source!" You point out that Snow Island isn't receiving any water.

"Oh, we had to stop the water because we ran out of sand to filter it with! Can't make snow with dirty water. Don't worry, I'm sure we'll get more sand soon; we only turned off the water a few days... weeks... oh no." His face sinks into a look of horrified realization.

"I've been so busy making sure everyone here has food that I completely forgot to check why we stopped getting more sand! There's a ferry leaving soon that is headed over in that direction - it's much faster than your boat. Could you please go check it out?"

You barely have time to agree to this request when he brings up another. "While you wait for the ferry, maybe you can help us with our food production problem. The latest Island Island Almanac just arrived and we're having trouble making sense of it."

The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use with each kind of seed, what type of fertilizer to use with each kind of soil, what type of water to use with each kind of fertilizer, and so on. Every type of seed, soil, fertilizer and so on is identified with a number, but numbers are reused by each category - that is, soil 123 and fertilizer 123 aren't necessarily related to each other.

For example:

seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
The almanac starts by listing which seeds need to be planted: seeds 79, 14, 55, and 13.

The rest of the almanac contains a list of maps which describe how to convert numbers from a source category into numbers in a destination category. That is, the section that starts with seed-to-soil map: describes how to convert a seed number (the source) to a soil number (the destination). This lets the gardener and his team know which soil to use with which seeds, which water to use with which fertilizer, and so on.

Rather than list every source number and its corresponding destination number one by one, the maps describe entire ranges of numbers that can be converted. Each line within a map contains three numbers: the destination range start, the source range start, and the range length.

Consider again the example seed-to-soil map:

50 98 2
52 50 48
The first line has a destination range start of 50, a source range start of 98, and a range length of 2. This line means that the source range starts at 98 and contains two values: 98 and 99. The destination range is the same length, but it starts at 50, so its two values are 50 and 51. With this information, you know that seed number 98 corresponds to soil number 50 and that seed number 99 corresponds to soil number 51.

The second line means that the source range starts at 50 and contains 48 values: 50, 51, ..., 96, 97. This corresponds to a destination range starting at 52 and also containing 48 values: 52, 53, ..., 98, 99. So, seed number 53 corresponds to soil number 55.

Any source numbers that aren't mapped correspond to the same destination number. So, seed number 10 corresponds to soil number 10.

So, the entire list of seed numbers and their corresponding soil numbers looks like this:

seed  soil
0     0
1     1
...   ...
48    48
49    49
50    52
51    53
...   ...
96    98
97    99
98    50
99    51
With this map, you can look up the soil number required for each initial seed number:

Seed number 79 corresponds to soil number 81.
Seed number 14 corresponds to soil number 14.
Seed number 55 corresponds to soil number 57.
Seed number 13 corresponds to soil number 13.
The gardener and his team want to get started as soon as possible, so they'd like to know the closest location that needs a seed. Using these maps, find the lowest location number that corresponds to any of the initial seeds. To do this, you'll need to convert each seed number through other categories until you can find its corresponding location number. In this example, the corresponding types are:

Seed 79, soil 81, fertilizer 81, water 81, light 74, temperature 78, humidity 78, location 82.
Seed 14, soil 14, fertilizer 53, water 49, light 42, temperature 42, humidity 43, location 43.
Seed 55, soil 57, fertilizer 57, water 53, light 46, temperature 82, humidity 82, location 86.
Seed 13, soil 13, fertilizer 52, water 41, light 34, temperature 34, humidity 35, location 35.
So, the lowest location number in this example is 35.

What is the lowest location number that corresponds to any of the initial seed numbers?
"""

from utils import utils

class SourceMap:
    def __init__(
        self,
        map_name_string: str = "",
        source_name: str = "",
        destination_name: str = "",
    ) -> None:
        """
        Initialize a SourceMap object.

        Args:
            map_name_string (str): A string representing the map name.
            source_name (str): The name of the source location.
            destination_name (str): The name of the destination location.
        """
        self.source_name: str = ""
        self.destination_name: str = ""

        self.destination_ranges: list[range] = []
        self.source_ranges: list[range] = []
        self.length: list[int] = []

        self.destination_map: SourceMap = None

        self.__current_iter: self = None
        self._last: self = self

        if source_name and destination_name:
            self.source_name, self.destination_name = source_name, destination_name
        else:
            self.source_name, self.destination_name = SourceMap.__parse_map_name(
                map_name_string
            )

    def add_ranges(self, ranges_string: str):
        """
        Add ranges to the SourceMap object.

        Args:
            ranges_string (str): A string representing the ranges to be added.
        """
        destination_start: int = 0
        source_start: int = 0
        length: int = 0

        destination_start, source_start, length = [
            int(num) for num in ranges_string.strip().split(" ")
        ]
        self._last.destination_ranges.append(
            range(destination_start, destination_start + length + 1)
        )
        self._last.source_ranges.append(range(source_start, source_start + length + 1))

    def add_map(self, map_name_string: str):
        """
        Add a new SourceMap object to the current SourceMap object.

        Args:
            map_name_string (str): A string representing the name of the new SourceMap.
        """
        source_name, destination_name = SourceMap.__parse_map_name(map_name_string)

        this_map = self
        while this_map.destination_name != source_name:
            this_map = this_map.destination_map

            if this_map is None:
                raise

        this_map.destination_map = SourceMap(
            source_name=this_map.destination_name, destination_name=destination_name
        )

        self._last = this_map.destination_map

    def __range_intersection(self, range_1: range, range_2: range) -> range:
        """
        Find the intersection of two ranges.

        Args:
            range_1 (range): The first range.
            range_2 (range): The second range.

        Returns:
            range: The intersection of the two ranges, or None if there is no intersection.
        """
        max_start: int = max(range_1.start, range_2.start)
        min_end: int = min(range_1.stop, range_2.stop)
        return range(max_start, min_end) or None

    def __get_minimum_index_in_range(self, range_start: int, range_length: int):
        """
        Get the minimum index within a given range.

        Args:
            range_start (int): The start of the range.
            range_length (int): The length of the range.

        Returns:
            int: The minimum index within the range, or None if no intersection is found.
        """
        _range: range = range(range_start, range_start + range_length)
        min_index: int = float("inf")

        found_intersection: bool = False
        for source_range in self.source_ranges:
            range_intersection: range = self.__range_intersection(_range, source_range)

            if range_intersection:
                found_intersection = True
                min_index = min(min_index, range_intersection.start)
                break

        if not found_intersection:
            return None

        return min_index

    def __get_location_by_index(self, index: int) -> int:
        """
        Get the location by index.

        Args:
            index (int): The index.

        Returns:
            int: The location corresponding to the index.
        """
        found: bool = False
        output: int = index
        for i, map_range in enumerate(self.source_ranges):
            if index in map_range:
                found = True
                offset: int = index - map_range.start
                output_index = self.destination_ranges[i].start + (offset)
                if self.destination_map:
                    output = self.destination_map[output_index]
                break

        if not found:
            if self.destination_map:
                output = self.destination_map[index]

        if not self.destination_map:
            for i, map_range in enumerate(self.source_ranges):
                if output in map_range:
                    found = True
                    offset: int = output - map_range.start
                    output = self.destination_ranges[i].start + (offset)
                    break

        return output

    def __getitem__(self, key: int) -> int:
        """
        Get the location by index or range.

        Args:
            key (int or slice): The index or range.

        Returns:
            int: The location corresponding to the index or range.
        """
        if isinstance(key, int):
            return self.__get_location_by_index(key)
        elif isinstance(key, slice):
            range_start: int = key.start
            range_length: int = key.stop - 1
            index: int = self.__get_minimum_index_in_range(range_start, range_length)

            if index:
                output: int = self.__getitem__(index)
                return output

    @staticmethod
    def __parse_map_name(map_name_string: str) -> [str, str]:
        """
        Parse the map name string and return the source and destination names.

        Args:
            map_name_string (str): The map name string.

        Returns:
            [str, str]: A list containing the source and destination names.
        """
        if map_name_string.endswith(":"):
            map_name_string = map_name_string[:-5]
        return map_name_string.split("-to-")

    def __iter__(self):
        """
        Initialize the iterator.

        Returns:
            self: The iterator object.
        """
        self.__current_iter = self
        return self.__current_iter

    def __next__(self):
        """
        Get the next SourceMap object in the iteration.

        Returns:
            self: The next SourceMap object.
        """
        if self.__current_iter is None:
            raise StopIteration

        temp = self.__current_iter
        self.__current_iter = self.__current_iter.destination_map
        return temp

    def __repr__(self) -> str:
        """
        Get the string representation of the SourceMap object.

        Returns:
            str: The string representation of the SourceMap object.
        """
        repr_str: str = ""
        for source_map in self.__iter__():
            repr_str += f"{source_map.source_name} --> {source_map.destination_name}\n"
            repr_str += "\tRange maps:\n"
            for source, destination in zip(
                source_map.source_ranges, source_map.destination_ranges
            ):
                repr_str += f"\t\t [{source.start:3}, {source.stop-1:3}]"
                repr_str += "--> "
                repr_str += f"[{destination.start:3}, {destination.stop-1:3}]\n"
        return repr_str

    def __str__(self) -> str:
        """
        Get the string representation of the SourceMap object.

        Returns:
            str: The string representation of the SourceMap object.
        """
        return self.__repr__()

def parse_lines(lines: [str]) -> [int, SourceMap]:
    """
    Parses the input lines and returns a tuple containing the seed numbers and the source map.

    Args:
        lines (List[str]): The input lines to parse.

    Returns:
        Tuple[List[int], SourceMap]: A tuple containing the seed numbers and the source map.
    """

    seeds_raw: str = lines[0]
    maps_raw_list: str = [line for line in lines[1:] if line and not line.isspace()]

    seed_numbers_raw: [str] = seeds_raw.split(" ", 1)[1].strip().split(" ")
    seed_numbers: [int] = list(map(int, seed_numbers_raw))

    source_map: SourceMap = None
    for map_raw_string in maps_raw_list:
        if map_raw_string[0].isalpha():
            if not source_map:
                source_map = SourceMap(map_raw_string)
            else:
                source_map.add_map(map_raw_string)
        else:
            source_map.add_ranges(map_raw_string)

    return seed_numbers, source_map


def get_min_location(seeds: [int], source_map: SourceMap, seed_ranges=False) -> int:
    """
    Returns the minimum location value from the given seeds and source map.

    Args:
        seeds (List[int]): A list of seed values.
        source_map (SourceMap): A mapping of locations to values.
        seed_ranges (bool, optional): Indicates whether the seeds represent ranges. Defaults to False.

    Returns:
        int: The minimum location value.

    """
    min_location: int = float("inf")

    if seed_ranges:
        for i in range(1, len(seeds), 2):
            seed_range_start: int = 0
            seed_range_length: int = 0
            seed_range_start, seed_range_length = seeds[i - 1], seeds[i]
            location: int = source_map[seed_range_start:seed_range_length]
            min_location = min(min_location, location)

    else:
        for seed in seeds:
            location: int = source_map[seed]
            min_location = min(min_location, location)

    return min_location


if __name__ == "__main__":
    test: bool = False
    lines: [str] = utils.read_lines("day_5-data.txt", test=test)

    seeds: [int] = None
    source_map: SourceMap = None

    seeds, source_map = parse_lines(lines)
    min_location: int = get_min_location(seeds, source_map)
    min_location: int = get_min_location(seeds, source_map, seed_ranges=True)
