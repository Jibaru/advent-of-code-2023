from collections import Counter
from functools import cmp_to_key

'''
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

Your puzzle answer was 253638586.
'''

FIVE_OF_A_KIND = 7
FOUR_OF_A_KIND = 6
FULL_HOUSE = 5
THREE_OF_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1

CARD_STRENGHTS = {
    '2': 1,
    '3': 2,
    '4': 3,
    '5': 4,
    '6': 5,
    '7': 6,
    '8': 7,
    '9': 8,
    'T': 9,
    'J': 10,
    'Q': 11,
    'K': 12,
    'A': 13
}

def get_type(card: str) -> int:
    if len(set(card)) == 1:
        return FIVE_OF_A_KIND

    counts = dict(Counter(card).items())

    lenght = len(counts)

    if lenght == 2:
        for s in counts:
            if counts[s] == 4:
                return FOUR_OF_A_KIND
            if counts[s] == 3:
                return FULL_HOUSE
    
    if lenght == 3:
        for s in counts:
            if counts[s] == 3:
                return THREE_OF_A_KIND
            if counts[s] == 2:
                return TWO_PAIR
    
    if lenght == 4:
        return ONE_PAIR

    return HIGH_CARD

def is_chr_greater_than(a: str, b: str):
    v1 = CARD_STRENGHTS[a]
    v2 = CARD_STRENGHTS[b]

    if v1 > v2:
        return -1
    elif v1 < v2:
        return 1
    return 0

def is_greater_than(first: (str, int), second: (str, int)) -> int:
    first_card, _ = first
    second_card, _ = second

    first_type = get_type(first_card)
    second_type = get_type(second_card)

    if first_type > second_type:
        return -1
    elif first_type < second_type:
        return 1
    
    lenght = len(first_card)
    for i in range(lenght):
        val = is_chr_greater_than(first_card[i], second_card[i])
        if val != 0:
            return val

    return 0

def solve01(data: str):
    values = []
    for line in data.split('\n'):
        card, val = line.split(' ')
        values.append((card, int(val)))

    values = sorted(values, key=cmp_to_key(is_greater_than))

    lenght = len(values)
    ans = 0
    for i in range(lenght):
        _, val = values[i]
        x = val * (lenght - i)

        ans += x

    return ans

'''
--- Part Two ---
To make things a little more interesting, the Elf introduces one additional rule. Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.

To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.

J cards can pretend to be whatever card is best for the purpose of determining hand type; for example, QJJQ2 is now considered four of a kind. However, for the purpose of breaking ties between two hands of the same type, J is always treated as J, not the card it's pretending to be: JKKK2 is weaker than QQQQ2 because J is weaker than Q.

Now, the above example goes very differently:

32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
32T3K is still the only one pair; it doesn't contain any jokers, so its strength doesn't increase.
KK677 is now the only two pair, making it the second-weakest hand.
T55J5, KTJJT, and QQQJA are now all four of a kind! T55J5 gets rank 3, QQQJA gets rank 4, and KTJJT gets rank 5.
With the new joker rule, the total winnings in this example are 5905.

Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

Your puzzle answer was 253253225.
'''

def get_type_with_joker(card: str) -> int:
    most_common_chars = Counter(card).most_common()

    for char, _ in most_common_chars:
        if char != 'J':
            return get_type(card.replace('J', char))

    return get_type(card)

def is_greater_than_joker(first: (str, int), second: (str, int)) -> int:
    first_card, _ = first
    second_card, _ = second

    first_type = get_type_with_joker(first_card)
    second_type = get_type_with_joker(second_card)

    if first_type > second_type:
        return -1
    elif first_type < second_type:
        return 1
    
    lenght = len(first_card)
    for i in range(lenght):
        val = is_chr_greater_than(first_card[i], second_card[i])
        if val != 0:
            return val

    return 0

def solve02(data):
    values = []
    for line in data.split('\n'):
        card, val = line.split(' ')
        values.append((card, int(val)))
    
    CARD_STRENGHTS['J'] = 0

    values = sorted(values, key=cmp_to_key(is_greater_than_joker))

    lenght = len(values)
    ans = 0
    for i in range(lenght):
        _, val = values[i]
        x = val * (lenght - i)

        ans += x

    return ans

if __name__ == "__main__":
    # data = open('day-7-input.test.txt', 'r').read()
    data = open('day-7-input.txt', 'r').read()

    print(solve01(data))
    print(solve02(data))
