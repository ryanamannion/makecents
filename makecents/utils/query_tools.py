#!/usr/bin/env python3
from regex_patterns import *


def fold_denoms(query_str):
    denominations_mapping = {
        # key is PCGS denomination
        r'1/2C': r'1? ?(and a )?half cents?',  # half cent
        r'1C': r'((1 cent|penny)',  # 1 cent
        # r'Cent': ['1C'],
        # r' C ': ['1C'],   # TODO: Change in price guide, fold these denoms
        r'2C': r'2 cents? (silver)?',  # 2 cent
        r'3CS': r'3 cents? silver',  # flag this and ask if they mean silver or nickel
        r'3CN': r'3 cents? nickel',  # 3 cent nickel
        r'5C': r'((?<!cent )nickel|5 cents?)',  # 5 cent (nickel)
        r'H10C': r'half dime',  # half Dime
        r'10C': '(dime|10 cents?)',  # dime
        r'20C': r'20 cents?',  # 20 cent
        r'25C': r'(quarter|25 cents?)',  # quarter
        r'50C': r'(half dollar|50 cents?)',  # half dollar
        r'\$1': r'(1 )?dollar',  # dollar coin
        r'\$2.50': r'(2 and a half dollars?|2\.50)',  # $2.50 gold
        r'\$3': r'3',  # $3 gold    # TODO: make these not match with year
        r'\$4': [''],  # $4 gold
        r'\$5': [''],  # $4 gold
        r'\$10': [''],  # $10 gold
        r'\$20': [''],  # $20 St. Gaudens Double Eagle
        r'\$25': [''],  # Gold Eagle
        r'\$50': [''],  # Gold Eagle
        # Colonials and special cases
        r'\'?Penny\'?': [''],
        r'1P': [''],
        r'1/2 ?P': [''],
        r'3Pence': [''],
        r'2Pence': [''],
        r'6Pence': [''],
        r'Shilling': [''],
        r'Shilng': [''],  # Special case, see PCGS#249
        r'1/24RL': [''],  # see PCGS#49
        r'9 Den': [''],  # French colonies, Deniers
        r'15 Den': [''],
        r'30 Den': [''],
        r'Farth': [''],  # e.g. PCGS#256
        r'Sou': [''],  # French Colonies
        r'Sol': [''],  # French Colonies, see PCGS#167113
        r'1/2 Db': [''],  # see PCGS#489
        r'1/2 R': [''],  # see PCGS#600506
        r'1/2 RL': [''],
        r'Rial': ['']
    }