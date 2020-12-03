#!/usr/bin/env python3
from utils.regex_patterns import *
from nltk.metrics.distance import edit_distance


def word_to_digit(input_string):
    replacement_pairs = [
        ('one', '1'),
        ('two', '2'),
        ('three', '3'),
        ('four', '4'),
        (r'(?<!twenty )five', '5'),
        ('six', '6'),
        ('seven', '7'),
        ('eight', '8'),
        ('nine', '9'),
        ('ten', '10'),
        ('twenty', '20'),
        ('twenty five', '25'),
        ('fifty', '50')
    ]
    for pattern, replacement in replacement_pairs:
        input_string = re.sub(pattern, replacement, input_string)

    return input_string


def fold_denoms(query_str):
    denominations_mapping = [
        # key is PCGS denomination
        (r'1/2C', r'(1 )?half( of (a|one) ?)? cents?'),  # half cent
        (r'1C', r'(1 cent|penny)'),  # 1 cent
        # (r'Cent', ['1C']),
        # (r' C ', ['1C'],
        (r'2C', r'2 cents? (silver)?'),  # 2 cent
        (r'3CS', r'3( ?C| cents?) silver'),  # flag this and ask if they mean silver or nickel
        (r'3CN', r'3 cents? nickel'),  # 3 cent nickel
        (r'5C', r'((?<!cent )nickel|5 cents?)'),  # 5 cent (nickel)
        (r'H10C', r'half dime'),  # half Dime
        (r'10C', '(dime|10 cents?)'),  # dime
        (r'20C', r'20 cents?'),  # 20 cent
        (r'25C', r'(quarter|25 cents?)'),  # quarter
        (r'50C', r'(?<!and a )(half dollar|50 cents?)'),  # half dollar
        (r'$1', r'(?<![02-9] )(?<!half )(1 )?dollar'),  # dollar coin
        (r'$2.50', r'(2 (and a half dollars?|dollars and 50 cents)|\$?2\.50)'),  # $2.50 gold
        (r'$3', r'3 dollars?'),  # $3 gold
        (r'$4', r'4 dollars?'),  # $4 gold
        (r'$5', r'5 dollars?'),  # $4 gold
        (r'$10', r'10 dollars?'),  # $10 gold
        (r'$20', r'20 dollars?'),  # $20 St. Gaudens Double Eagle
        (r'$25', r'25 dollars?'),  # Gold Eagle
        (r'$50', r'50 dollars?'),  # Gold Eagle
        # after all of the main ones are done
        (r'1C', r'(?<![0-9] )(?<!half )cent')     # lincoln cent, wheat cent, etc.
        # Colonials and special cases
        # (r'\'?Penny\'?', ['']),
        # (r'1P', ['']),
        # (r'1/2 ?P', ['']),
        # (r'3Pence', ['']),
        # (r'2Pence', ['']),
        # (r'6Pence', ['']),
        # (r'Shilling', ['']),
        # (r'Shilng', ['']),  # Special case, see PCGS#249
        # (r'1/24RL', ['']),  # see PCGS#49
        # (r'9 Den', ['']),  # French colonies, Deniers
        # (r'15 Den', ['']),
        # (r'30 Den', ['']),
        # (r'Farth', ['']),  # e.g. PCGS#256
        # (r'Sou', ['']),  # French Colonies
        # (r'Sol', ['']),  # French Colonies, see PCGS#167113
        # (r'1/2 Db', ['']),  # see PCGS#489
        # (r'1/2 (R', ['']),  # see PCGS#600506
        # (r'1/2 RL', ['']),
        # (r'Rial', ['']
    ]

    query_str = word_to_digit(query_str)

    for repl, pattern in denominations_mapping:
        query_str = re.sub(pattern, repl, query_str)

    return query_str


def rank_results(normalized_query, results):
    """
    Rank results by lowest-highest Levenshtein Edit Distance

    :param normalized_query: query normalized (denom folded)
    :param results: results list from query_price_guide
    :return sorted_results: results sorted from lowest to highest edit distance
    """
    scores = []
    for result in results:
        score = edit_distance(normalized_query, result['description'])
        scores.append((score, result))
    # sort scores by index 0, aka edit distance
    scores.sort(key=lambda x: x[0])
    sorted_results = [score[1] for score in scores]
    return sorted_results


if __name__ == "__main__":
    # for testing
    print(fold_denoms('lincoln cent'))
    print(fold_denoms('wheat cent'))
    print(fold_denoms('lincoln penny'))
    print(fold_denoms('cent'))
    print(fold_denoms('three cent silver'))
    print(fold_denoms('3 cent silver'))
    print(fold_denoms('3C silver'))
    print(fold_denoms('half dollar'))
    print(fold_denoms('quarter'))
    print(fold_denoms('$50'))
    print(fold_denoms('fifty dollar piece'))
    print(fold_denoms('two and a half dollars'))
    print(fold_denoms('dime'))
