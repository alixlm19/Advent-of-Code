"""
--- Day 7: Camel Cards ---
Your all-expenses-paid trip turns out to be a one-way, five-minute ride in an airship. (At least it's a cool airship!) It drops you off at the edge of a vast desert and descends back to Island Island.

"Did you bring the parts?"

You turn around to see an Elf completely covered in white clothing, wearing goggles, and riding a large camel.

"Did you bring the parts?" she asks again, louder this time. You aren't sure what parts she's looking for; you're here to figure out why the sand stopped.

"The parts! For the sand, yes! Come with me; I will show you." She beckons you onto the camel.

After riding a bit across the sands of Desert Island, you can see what look like very large rocks covering half of the horizon. The Elf explains that the rocks are all along the part of Desert Island that is directly above Island Island, making it hard to even get there. Normally, they use big machines to move the rocks and filter the sand, but the machines have broken down because Desert Island recently stopped receiving the parts they need to fix the machines.

You've already assumed it'll be your job to figure out why the parts stopped when she asks if you can help. You agree automatically.

Because the journey will take a few days, she offers to teach you the game of Camel Cards. Camel Cards is sort of similar to poker except it's designed to be easier to play while riding a camel.

In Camel Cards, you get a list of hands, and your goal is to order them based on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2. The relative strength of each card follows this order, where A is the highest and 2 is the lowest.

Every hand is exactly one type. From strongest to weakest, they are:

Five of a kind, where all five cards have the same label: AAAAA
Four of a kind, where four cards have the same label and one card has a different label: AA8AA
Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
High card, where all cards' labels are distinct: 23456
Hands are primarily ordered based on type; for example, every full house is stronger than any three of a kind.

If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand. If these cards are different, the hand with the stronger first card is considered stronger. If the first card in each hand have the same label, however, then move on to considering the second card in each hand. If they differ, the hand with the higher second card wins; otherwise, continue with the third card in each hand, then the fourth, then the fifth.

So, 33332 and 2AAAA are both four of a kind hands, but 33332 is stronger because its first card is stronger. Similarly, 77888 and 77788 are both a full house, but 77888 is stronger because its third card is stronger (and both hands have the same first and second card).

To play Camel Cards, you are given a list of hands and their corresponding bid (your puzzle input). For example:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
This example shows five hands; each hand is followed by its bid amount. Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1, the second-weakest hand gets rank 2, and so on up to the strongest hand. Because there are five hands in this example, the strongest hand will have rank 5 and its bid will be multiplied by 5.

So, the first step is to put the hands in order of strength:

32T3K is the only one pair and the other hands are all a stronger type, so it gets rank 1.
KK677 and KTJJT are both two pair. Their first cards both have the same label, but the second card of KK677 is stronger (K vs T), so KTJJT gets rank 2 and KK677 gets rank 3.
T55J5 and QQQJA are both three of a kind. QQQJA has a stronger first card, so it gets rank 5 and T55J5 gets rank 4.
Now, you can determine the total winnings of this set of hands by adding up the result of multiplying each hand's bid with its rank (765 * 1 + 220 * 2 + 28 * 3 + 684 * 4 + 483 * 5). So the total winnings in this example are 6440.

Find the rank of every hand in your set. What are the total winnings?
"""

from utils import utils
from enum import IntEnum, auto

CARD_MAP: str = dict(zip("23456789TJQKA", range(13)))
CARD_MAP_WITH_WILDCARD: str = dict(zip("J23456789TQKA", range(13)))

class HandRank(IntEnum):
    """
    Enumeration representing the rank of a poker hand.
    
    The possible values are:
    - HIGH_CARD: Represents a high card hand.
    - ONE_PAIR: Represents a hand with one pair.
    - TWO_PAIR: Represents a hand with two pairs.
    - THREE_OF_KIND: Represents a hand with three of a kind.
    - FULL_HOUSE: Represents a hand with a full house.
    - FOUR_OF_KIND: Represents a hand with four of a kind.
    - FIVE_OF_KIND: Represents a hand with five of a kind.
    """
    
    HIGH_CARD: int = auto()
    ONE_PAIR: int = auto()
    TWO_PAIR: int = auto()
    THREE_OF_KIND: int = auto()
    FULL_HOUSE: int = auto()
    FOUR_OF_KIND: int = auto()
    FIVE_OF_KIND: int = auto()

def get_card_value(card: str, wildcard: bool = False) -> int:
    """
    Get the value of a card.

    Args:
        card (str): The card to get the value of.
        wildcard (bool, optional): Whether to use wildcard mapping. Defaults to False.

    Returns:
        int: The value of the card.
    """
    if wildcard:
        return CARD_MAP_WITH_WILDCARD[card]
    
    return CARD_MAP[card]

def get_hand_type(card_counts: [int]) -> HandRank:
    """
    Determines the hand type based on the counts of cards.

    Args:
        card_counts (list[int]): A list of integers representing the counts of each card.

    Returns:
        HandRank: The hand type based on the card counts.
    """

    card_counts_collapsed: tuple[int] = tuple(sorted(card_counts, reverse=True)[:3])
    hand_type: HandRank = HandRank.HIGH_CARD
    match card_counts_collapsed:
        # FIVE OF A KIND
        case (5, 0, 0): 
            hand_type = HandRank.FIVE_OF_KIND
        # FOUR OF A KIND
        case (4, 1, 0): 
            hand_type = HandRank.FOUR_OF_KIND
        # FULL HOUSE
        case (3, 2, 0): 
            hand_type = HandRank.FULL_HOUSE
       # THREE OF KIND 
        case (3, 1, 1): 
            hand_type =  HandRank.THREE_OF_KIND
        # TWO PAIR
        case (2, 2, 1): 
            hand_type = HandRank.TWO_PAIR
        # ONE PAIR
        case (2, 1, 1): 
            hand_type = HandRank.ONE_PAIR

    return hand_type

def get_hand_rank(hand: str, wildcard = False) -> HandRank:
    """
    Calculates the rank of a hand in a card game.

    Args:
        hand (str): The hand of cards represented as a string.
        wildcard (bool, optional): Indicates whether a wildcard is present. Defaults to False.

    Returns:
        HandRank: The rank of the hand.

    """
    card_counts: [int] = [0] * 13

    for card in hand:
        card_value: int = get_card_value(card, wildcard)
        card_counts[card_value] += 1

    rank: HandRank = get_hand_type(card_counts)
    
    if wildcard:
        card_count_copy: [int] = card_counts.copy()
        max_card_index: int = len(card_counts) - 1
        max_value: int = 0
        
        for i in range(len(card_counts)-1, 0, -1):
            if card_counts[i] > max_value:
                max_value = card_counts[i]
                max_card_index = i

        card_count_copy[max_card_index] += card_counts[0]
        card_count_copy[0] = 0

        tentative_rank: HandRank = get_hand_type(card_count_copy)

        rank = max(rank, tentative_rank)

    return rank



def sort_by_rank(hands: [tuple[str, int]], wildcard: bool = False):
    """
    Sorts a list of hands by their rank.

    Args:
        hands (list[tuple[str, int]]): A list of tuples containing the hand and the bid.
        wildcard (bool, optional): Indicates whether wildcard is enabled. Defaults to False.

    Returns:
        list[tuple[str, int]]: A sorted list of hands by their rank.

    """
    hands_by_rank: [tuple[str, int]] = []

    def get_hand_order(hand_with_bid: tuple[str, int]):
        """
        Get the order of a hand with a bid.

        Args:
            hand_with_bid (tuple[str, int]): A tuple containing the hand and the bid.

        Returns:
            tuple: A tuple containing the hand rank and the card values.

        """
        hand, _ = hand_with_bid
        card_values: tuple[int] = tuple(get_card_value(card, wildcard) for card in hand)

        return (get_hand_rank(hand, wildcard), card_values)
    
    hands_by_rank = sorted(hands, key = get_hand_order)
    return hands_by_rank

def get_total_winnings(hands: [tuple[str, int]], wildcard: bool = False) -> int:
    """
    Calculates the total winnings based on the ranks of the hands.

    Args:
        hands (list[tuple[str, int]]): A list of tuples representing the hands, where each tuple contains a string representing the hand and an integer representing its value.
        wildcard (bool, optional): A flag indicating whether to consider a wildcard. Defaults to False.

    Returns:
        int: The total winnings based on the ranks of the hands.
    """

    hands_by_rank: [tuple[str, int]] = sort_by_rank(hands, wildcard)
    total_winnings: int = 0

    
    for i in range(len(hands_by_rank)):
        rank: int = i + 1
        total_winnings += rank * hands_by_rank[i][1]
    
    return total_winnings

def parse_lines(lines: [str]):
    """
    Parse lines of input and return a list of tuples containing hands and bids.

    Args:
        lines: A list of strings representing each line of input.

    Returns:
        A list of tuples, where each tuple contains a hand and a bid.

    Example:
        >>> lines = ['North 5', 'South 3', 'East 2']
        >>> parse_lines(lines)
        [('North', 5), ('South', 3), ('East', 2)]
    """
    hands: [str] = []
    bids: [int] = []
    for line in lines:
        hand, bid = line.split(' ')
        hands.append(hand)
        bids.append(int(bid))

    return list(zip(hands, bids))

if __name__ == "__main__":
    test = False
    lines: [str] = utils.read_lines("day_7-data.txt", test = test)

    # lines = ["JKKK2 23", "QQQQ2 14"]
    plays: [tuple[str, int]] = parse_lines(lines)
    total_winnings_without_wildcard: int = get_total_winnings(plays)
    print(f"{total_winnings_without_wildcard=}")

    total_winnings_with_wildcard: int = get_total_winnings(plays, wildcard=True)
    print(f"{total_winnings_with_wildcard=}")