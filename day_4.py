from dataclasses import dataclass
from utils import utils
import re

FILENAME: str = "day_4-data.txt"
PATTERN: str = r"(\s{2,})"


@dataclass
class Game:
    """
    Represents a game with a unique ID, winning numbers, and played numbers.
    """

    game_id: int
    winning_numbers: set[int]
    played_numbers: set[int]
    copies: int = 1

    def __init__(
        self, game_id: int, winning_numbers: [int], played_numbers: [int]
    ) -> None:
        """
        Initialize a Game object with the given game ID, winning numbers, and played numbers.

        Parameters:
        game_id (int): The ID of the game.
        winning_numbers (list[int]): The list of winning numbers.
        played_numbers (list[int]): The list of played numbers.
        """
        self.game_id = game_id
        self.winning_numbers = set(winning_numbers)
        self.played_numbers = set(played_numbers)

    @property
    def number_winning_played_games(self) -> int:
        """
        Returns the number of winning played games.

        This method calculates the number of winning played games by finding the intersection
        between the winning numbers and the played numbers, and then returning the length of
        the resulting set.

        Returns:
            The number of winning played games as an integer.
        """
        winning_played_numbers: set[int] = self.winning_numbers.intersection(
            self.played_numbers
        )
        return len(winning_played_numbers)

    @property
    def points(self) -> int:
        """
        Calculates the points earned by the player based on the number of winning played games.

        Returns:
            int: The points earned by the player.
        """
        games_won: int = self.number_winning_played_games
        if games_won:
            return 1 << (games_won - 1)

        return 0

    def add_copy(self, n: int = 1) -> None:
        """
        Adds the specified number of copies to the object.

        Args:
            n (int): The number of copies to add. Defaults to 1.
        """
        self.copies += n


def parse_input(lines: [str]) -> [str]:
    """
    Parses the input lines by removing a specific pattern from each line.

    Args:
        lines: A list of strings representing the input lines.

    Returns:
        A list of strings with the specified pattern removed from each line.
    """

    num_lines: int = len(lines)
    parsed_lines: [str] = lines.copy()

    for i in range(num_lines):
        parsed_lines[i] = re.sub(PATTERN, " ", parsed_lines[i], 0, re.MULTILINE)

    return parsed_lines


def extract_games(lines: [str]) -> [Game]:
    """
    Extracts game information from a list of lines and returns a list of Game objects.

    Parameters:
    lines (list[str]): A list of strings representing the game information.

    Returns:
    list[Game]: A list of Game objects containing the extracted game information.
    """

    card_number: int = 0
    card: str = ""
    card_number_raw: str = ""
    numbers_raw: str = ""

    winning_numbers_raw: str = ""
    winning_numbers: [int] = []

    played_numbers: [int] = []
    played_numbers_raw: str = ""
    games: [Game] = []
    for line in lines:
        card, numbers_raw = line.split(":")
        _, card_number_raw = card.split(" ")
        card_number = int(card_number_raw)

        winning_numbers_raw, played_numbers_raw = numbers_raw.split("|")

        winning_numbers = [int(num) for num in winning_numbers_raw.strip().split(" ")]
        played_numbers = [int(num) for num in played_numbers_raw.strip().split(" ")]

        games.append(Game(card_number, winning_numbers, played_numbers))

    return games


def get_copies(games: [Game]) -> [Game]:
    """
    Returns a copy of the list of games with updated copies count for each game.

    Parameters:
    games (list[Game]): The list of games.

    Returns:
    list[Game]: A copy of the list of games with updated copies count for each game.
    """

    games_copy: [Game] = games.copy()
    for game in games_copy:
        game_id: int = game.game_id
        games_won: int = game.number_winning_played_games
        for i in range(game_id, game_id + games_won):
            games_copy[i].add_copy(game.copies)

    return games_copy


def get_checksum(games: [Game]) -> int:
    """
    Calculates the checksum by summing up the points of all the games.

    Args:
        games (list[Game]): A list of Game objects.

    Returns:
        int: The checksum value.
    """
    return sum(game.points for game in games)


def get_total_copies(games: [Game]) -> int:
    """
    Calculates the total number of copies for a list of games.

    Args:
        games (list[Game]): A list of Game objects representing different games.

    Returns:
        int: The total number of copies for all the games.
    """
    return sum(game.copies for game in games)


if __name__ == "__main__":
    test: bool = False
    lines: [str] = utils.read_lines(FILENAME, test=test)
    parsed_lines: [str] = parse_input(lines)

    games: [Game] = extract_games(parsed_lines)
    games_with_copies: [Game] = get_copies(games)
    checksum_part_1: int = get_checksum(games)
    checksum_part_2: int = get_total_copies(games_with_copies)

    print(f"{checksum_part_1=}")
    print(f"{checksum_part_2=}")
