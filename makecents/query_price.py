#!/usr/bin/env python3
"""
query_price.py

query the price guide given some user input string, return most likely coins

Author: Ryan A. Mannion, 2020
github: ryanamannion
twitter: @ryanamannion
"""
import ft
import sys
import pickle
import argparse

from utils import regex_patterns


def validate_query(query_str):
    """

    :param query_str:
    :param coin_ft:
    :return:
    """

    # pre-compiled regex patterns
    year_regex = regex_patterns.year_regex
    denom_regex = regex_patterns.denom_regex_ci     # case insensitive

    # change common references
    query_str.replace('penny')

    # Required for every query: Year and Denomination
    query_year = year_regex.search(query_str)
    query_denom = denom_regex.search(query_str)
    if query_year is None:
        resp = 'I could not detect a year in your query, please make sure you' \
               ' include a year! e.g. 1997-P 25c'
        sys.exit(resp)
    if query_denom is None:
        resp = 'I could not detect an acceptable denomination in your query, ' \
               'please make sure you include one! e.g. 1997-P 25c'
        sys.exit(resp)

    query_year_match = query_year.group(0)
    query_denom_match = query_denom.group(0)

    try:
        matched_year = coin_by_year[query_year_match]
    except KeyError:
        resp = f'I could not find a coin with the year {query_year_match}, ' \
               f"please try again. Remember, I know US and some colonial " \
               f"coin prices"
        sys.exit(resp)

    print('acceptable query')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--price_guide', '-p', action='store',
                        help='path to binary for price guide created with '
                             'pcgs_scraper package, link at '
                             'https://github.com/ryanamannion/pcgs_scraper.git '
                             '\nDefaults to 30-11-2020',
                        default='pcgs_price_guide-30-11-2020.pkl'
                        )
    parser.add_argument('--query', '-q', action='store',
                        help='Coin to get price for, in format: \n '
                             '\tYYYY(-M) DNM...\n'
                             'where YYYY is the year, -M the optional mint mark'
                             ' and DNM the denomination (dime, penny, 25c, $1),'
                             ' any details may follow to give more information'
                             ' about the coin')
    args = parser.parse_args()

    price_guide = pickle.load(open(args.price_guide, 'rb'))

    query = validate_query(args.query)
