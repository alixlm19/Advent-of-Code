from dataclasses import dataclass
from math import prod

@dataclass
class BallDraw:
    """
    A class that tracks the number of balls of different colors in a game.
    """

    num_red: int = 0
    num_green: int = 0
    num_blue: int = 0

    def add_ball(self, game: str) -> None:
        """
        Adds the specified number of balls to the corresponding color count.

        Args:
            game (str): The game string containing the number and color of balls.

        Returns:
            None
        """
        raw_num: str = ""
        color: str = ""

        raw_num, color = game.strip().split(" ")

        num: int = int(raw_num)
        match color:
            case "red":
                self.num_red += num
            case "green":
                self.num_green += num
            case "blue":
                self.num_blue += num


def read_lines(test=False) -> [dict]:
    """
    Read lines from a file and parse them into a list of dictionaries.

    Args:
        test (bool): Flag indicating whether to use test data file.

    Returns:
        list: A list of dictionaries representing the parsed lines.
    """
    filename: str = "./data/day_2-data.txt"
    if test:
        filename = "./data/day_2-data-test.txt"

    lines: [dict] = []
    with open(filename, "r") as f:
        lines = list(map(parse_line, f.readlines()))

    return lines


def parse_line(string: str) -> dict:
    """
    Parses a string and returns a dictionary containing game information.

    Args:
        string (str): The input string to be parsed.

    Returns:
        dict: A dictionary containing the parsed game information.
            - game_id (int): The ID of the game.
            - games (list): A list of GameTracker objects representing the games.
    """
    
    raw_game_id: str = ""
    raw_games: str = ""

    raw_game_id, raw_games = string.split(":")
    game_id: int = int(raw_game_id.split(" ")[1])

    game_draws: [str] = raw_games.split(";")

    games: [BallDraw] = []

    for draw in game_draws:
        ball_draw: BallDraw = BallDraw()
        for ball in draw.split(","):
            ball_draw.add_ball(ball)

        games.append(ball_draw)

    return dict(game_id=game_id, games=games)


def get_games_checksum_and_power(
    games: [dict], max_red: int, max_green: int, max_blue: int
) -> [int, int]:
    """
    Calculates the checksum and power of compatible games based on the maximum
    number of red, green, and blue balls allowed.

    Args:
        games (list[dict]): A list of games, where each game is represented as a dictionary.
        max_red (int): The maximum number of red balls allowed.
        max_green (int): The maximum number of green balls allowed.
        max_blue (int): The maximum number of blue balls allowed.

    Returns:
        list[int, int]: A list containing the checksum and power of compatible games.
    """
    
    compatible_games: [int] = []
    minimum_required_balls: [[int]] = []
    for game in games:
        max_game_red: int = 0
        max_game_green: int = 0
        max_game_blue: int = 0

        for draw in game["games"]:
            max_game_red = max(max_game_red, draw.num_red)
            max_game_green = max(max_game_green, draw.num_green)
            max_game_blue = max(max_game_blue, draw.num_blue)

        minimum_required_balls.append((max_game_red, max_game_green, max_game_blue))
        if (
            max_game_red > max_red
            or max_game_green > max_green
            or max_game_blue > max_blue
        ):
            continue

        compatible_games.append(game["game_id"])

    
    checksum: int = sum(compatible_games)
    power: int = sum(map(prod, minimum_required_balls))
    
    return checksum, power


if __name__ == "__main__":
    games: [dict] = read_lines()

    get_games_checksum_and_power(games, 12, 13, 14)
