from utils import utils


def get_symbol_and_number_positions(
    lines: [str], include_all_symbols: bool = True, token="*"
) -> dict:
    """
    Get the positions of symbols and numbers in the given lines.

    Args:
        lines (list[str]): The lines of text.
        include_all_symbols (bool, optional): Whether to include all symbols or only the specified token. Defaults to True.
        token (str, optional): The symbol token to include. Defaults to "*".

    Returns:
        dict: A dictionary containing the positions of numbers and symbols.

    Example:
        lines = [
            "1..2..3",
            "4..5..6",
            "7..8..9",
        ]
        positions = get_symbol_and_number_positions(lines, include_all_symbols=False, token=".")
        print(positions)
        # Output: {'number_positions': [(0, 0, 1), (0, 3, 1), (0, 6, 1), (1, 0, 1), (1, 3, 1), (1, 6, 1), (2, 0, 1), (2, 3, 1), (2, 6, 1)], 'symbol_positions': [(0, 1), (0, 2), (0, 4), (0, 5), (1, 1), (1, 2), (1, 4), (1, 5), (2, 1), (2, 2), (2, 4), (2, 5)]}
    """

    num_lines: int = len(lines)
    num_chars: int = len(lines[0])

    number_positions: [[int, int, int]] = []
    symbol_positions: [[int, int]] = []

    for i in range(num_lines):
        num_length: int = 0
        for j in range(num_chars):
            char: str = lines[i][j]
            if char.isnumeric():
                num_length += 1

                # Add number to list if end of line reached
                if j + 1 == num_chars:
                    number_positions.append((i, j - num_length + 1, num_length))
                    num_length = 0
            else:
                if num_length:
                    number_positions.append((i, j - num_length, num_length))
                    num_length = 0
                if include_all_symbols:
                    if char != ".":
                        symbol_positions.append((i, j))
                elif char == token:
                    symbol_positions.append((i, j))

    positions: dict = dict(
        number_positions=number_positions, symbol_positions=symbol_positions
    )

    return positions


def filter_number_with_adjacent_symbols(symbol_and_number_positions: dict):
    """
    Filter number positions that have adjacent symbols.

    Args:
        symbol_and_number_positions (dict): A dictionary containing the positions of symbols and numbers.

    Returns:
        list: A list of filtered number positions that have adjacent symbols.
    """
    number_positions: [[int, int, int]] = symbol_and_number_positions[
        "number_positions"
    ]
    symbol_positions: [[int, int]] = symbol_and_number_positions["symbol_positions"]

    filtered_number_positions: [[int, int, int]] = []
    for num in number_positions:
        num_row, num_col, num_len = num
        for sym in symbol_positions:
            sym_row, sym_col = sym

            if (
                num_row - 1 <= sym_row <= num_row + 1
                and num_col - 1 <= sym_col <= num_col + num_len
            ):
                filtered_number_positions.append(num)
                break

    return filtered_number_positions


def get_number_powers(symbol_and_number_positions: dict):
    """
    Calculate the powers of adjacent numbers based on their positions.

    Args:
        symbol_and_number_positions (dict): A dictionary containing the positions of symbols and numbers.

    Returns:
        list: A list of powers calculated from adjacent numbers.
    """

    number_positions: [[int, int, int]] = symbol_and_number_positions[
        "number_positions"
    ]
    symbol_positions: [[int, int]] = symbol_and_number_positions["symbol_positions"]
    powers: [int] = []

    number_positions_length: int = len(number_positions)
    for sym in symbol_positions:
        sym_row, sym_col = sym

        for i in range(number_positions_length):
            num_prev: [int, int, int] = number_positions[i]
            num_row_prev, num_col_prev, num_len_prev = num_prev
            left_prev: int = num_col_prev
            right_prev: int = num_col_prev + num_len_prev
            num_prev_int: int = int(get_numbers_from_positions([num_prev])[0])

            # Ignore numbers too far up
            if (
                (num_row_prev < sym_row and sym_row - num_row_prev > 1)
                or (right_prev < sym_col and sym_col - right_prev >= 1)
                or (sym_col < left_prev and left_prev - sym_col > 1)
            ):
                continue

            for j in range(i + 1, number_positions_length):
                num_curr: [int, int, int] = number_positions[j]
                num_row_curr, num_col_curr, num_len_curr = num_curr
                left_curr: int = num_col_curr
                right_curr: int = num_col_curr + num_len_curr

                # Ignore numbers too far up
                if (
                    (num_row_curr < sym_row and sym_row - num_row_curr > 1)
                    or (right_curr < sym_col and sym_col - right_curr >= 1)
                    or (sym_col < left_curr and left_curr - sym_col > 1)
                ):
                    continue
                # Remaining numbers are outside the area of adjacent numbers
                elif num_row_curr > sym_row and num_row_curr - sym_row > 1:
                    break

                num_curr_int: int = int(get_numbers_from_positions([num_curr])[0])
                powers.append(num_prev_int * num_curr_int)

    return powers


def get_symbols_from_positions(symbol_positions: [[int, int, int]]) -> [int]:
    """
    Get symbols from the given positions in a 2D list.

    Args:
        symbol_positions: A list of symbol positions, where each position is represented as a tuple (row, column).

    Returns:
        A list of symbols corresponding to the given positions.
    """
    symbols: [str] = set()
    for sym in symbol_positions:
        sym_row, sym_col = sym
        symbols.add(lines[sym_row][sym_col])

    return list(symbols)


def get_numbers_from_positions(number_positions: [[int, int, int]]) -> [int]:
    """
    Extracts numbers from specified positions in a 2D list of lines.

    Args:
        number_positions: A list of number positions, where each position is represented as [row, column, length].

    Returns:
        A list of extracted numbers.

    """
    numbers: [int] = []
    for num in number_positions:
        num_row, num_col, num_len = num
        numbers.append(int(lines[num_row][num_col : num_col + num_len]))

    return numbers


def get_checksum(
    lines: [str], include_all_symbols: bool = True, token: str = "*"
) -> int:
    """
    Calculate the checksum of a list of lines.

    Args:
        lines: A list of strings representing the lines.
        include_all_symbols: A boolean indicating whether to include all symbols in the calculation.
        token: A string representing the token to be used as a symbol.

    Returns:
        The checksum as an integer.
    """

    symbol_and_number_positions = get_symbol_and_number_positions(
        lines, include_all_symbols, token
    )
    filtered_number_positions = filter_number_with_adjacent_symbols(
        symbol_and_number_positions
    )

    valid_part_numbers: [int] = []
    if include_all_symbols:
        valid_part_numbers = get_numbers_from_positions(filtered_number_positions)
    else:
        valid_part_numbers = get_number_powers(symbol_and_number_positions)

    symbols: [int] = get_symbols_from_positions(
        symbol_and_number_positions["symbol_positions"]
    )
    print(f"{symbols=}")

    checksum: int = sum(valid_part_numbers)

    return checksum


if __name__ == "__main__":
    test: bool = False
    lines: [str] = utils.read_lines("day_3-data.txt", test=test)

    checksum_part_1: int = get_checksum(lines)
    print(f"{checksum_part_1=}")

    checksum_part_2: int = get_checksum(lines, include_all_symbols=False, token="*")
    print(f"{checksum_part_2=}")

    if test:
        assert checksum_part_1 == 4361
        assert checksum_part_2 == 87287096
