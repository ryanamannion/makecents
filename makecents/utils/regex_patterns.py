#!/usr/bin/env python3
"""
regex_pattern.py

contains regex patterns for parsing coin descriptions

Author: Ryan A. Mannion, 2020
github: ryanamannion
twitter: @ryanamannion
"""
import re

# TODO: I want to put pcgs_scraper on PyPi and then I can just import these
# for now they are the exact same patterns I use in pcgs_scraper

# ci = case insensitive

year_regex = re.compile(r'\(?(\d\d\d\d)\)?(/\(?\d+\)?)*')
# notes on year:   #93924: 1914/(3) 5C
#   #3939: 1918/7-D 5C
#   #38975: 1825/4/(2) 25C Browning 2
#   #715594: (2019) 1C Blank Planchet Explore & Discover Set, RD

mint_pattern = r'-((P|D|S|CC|O|W|M|A|H)(/(P|D|S|CC|O|W|M|A|H)))'
mint_regex = re.compile(mint_pattern)
mint_regex_ci = re.compile(mint_pattern, re.IGNORECASE)
# mint mark reference: en.wikipedia.org/wiki/Historical_United_States_mints
# can have slash with two mints: e.g. #3985: 1938-D/S 5C Buffalo

denominations = [
    # US Coins
    r'1/2C',     # half cent
    r'1C',       # 1 cent
    r'Cent',
    r' C ',
    r'2C',       # 2 cent
    r'3CS',      # 3 cent silver
    r'3CN',      # 3 cent nickel
    r'5C',       # 5 cent (nickel)
    r'H10C',     # half Dime
    r'10C',      # dime
    r'20C',      # 20 cent
    r'25C',      # quarter
    r'50C',      # half dollar
    r'\$1',       # dollar coin
    r'\$2.50',    # $2.50 gold
    r'\$3',       # $3 gold
    r'\$4',       # $4 gold
    r'\$5',       # $4 gold
    r'\$10',      # $10 gold
    r'\$20',      # $20 St. Gaudens Double Eagle
    r'\$25',      # Gold Eagle
    r'\$50',      # Gold Eagle
    # Colonials and special cases
    r'\'?Penny\'?',
    r'1P',
    r'1/2 ?P',
    r'3Pence',
    r'2Pence',
    r'6Pence',
    r'Shilling',
    r'Shilng',    # Special case, see PCGS#249
    r'1/24RL',    # see PCGS#49
    r'9 Den',     # French colonies, Deniers
    r'15 Den',
    r'30 Den',
    r'Farth',     # e.g. PCGS#256
    r'Sou',       # French Colonies
    r'Sol',       # French Colonies, see PCGS#167113
    r'1/2 Db',    # see PCGS#489
    r'1/2 R',      # see PCGS#600506
    r'1/2 RL',
    r'Rial'
]
denom_option = r'(' + r'|'.join(denominations) + r')'
denom_regex = re.compile(denom_option)
denom_regex_ci = re.compile(denom_option, re.IGNORECASE)
# !Cannot just do contains() for denomination:
#       #4282: 1835 H10C Large Date, Large 5C
# re.search handles this for us since it just matches the first one

# Detail is just everything after the denom
#   #5063: 1945-S 10C Micro S, FB
#   #802036: 1814 10C STATESOF S.S. Central America #2 (with Pinch)
# Search algorithm will handle this by calculating edit distance between the
# multiple options and ranking them