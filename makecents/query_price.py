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
from copy import deepcopy

from utils.regex_patterns import year_regex, denom_regex_ci, mint_regex_ci
from utils.query_tools import fold_denoms, rank_results


def validate_query(query_str):
    """
    Given a query, ensure it has a year and a denomination and extract them

    :param query_str: (str), query input from user
    :return query_params: (tuple)
        year(str),
        denomination(str),
        mint mark(str), str if included, None if not
        original query(str),
        normalized query(str), denomination folded query
    """
    original_query = deepcopy(query_str)

    # normalize query
    query_str = fold_denoms(query_str)      # normalize denominations

    # Required for every query: Year and Denomination
    query_year = year_regex.search(query_str)
    query_denom = denom_regex_ci.search(query_str)      # case insensitive
    if query_year is None:
        resp = 'I could not detect a year in your query, please make sure you' \
               ' include a year! e.g. 1997-P 25c'
        sys.exit(resp)
    if query_denom is None:
        resp = 'I could not detect an acceptable denomination in your query, ' \
               'please make sure you include one! e.g. 1997-P 25c'
        sys.exit(resp)

    year_match = query_year.group(0)
    denom_match = query_denom.group(0)

    # get mint mark if provided, else set to None
    query_mint = mint_regex_ci.search(query_str)
    if query_mint is not None:
        mint_match = query_mint.group(0).strip('-').upper()
    else:
        mint_match = None

    normalized_query = query_str        # alias for clarity

    query_params = (year_match,
                    denom_match,
                    mint_match,
                    original_query,
                    normalized_query)

    return query_params


def query_price_guide(query_tuple, coin_ft):
    """
    With a validated query, return one or more coins from the free table
    matching the description

    :param query_tuple: (tuple) output from validate_query
    :param coin_ft: (list(dict)) free table of coin prices, made with
        pcgs_scraper
    :return :
    """
    query_year, query_denom, query_mint, query_orig, query_norm = query_tuple

    # lots of loops, make life easy
    result_found = False

    # index the ft by year to quick search for year
    coins_by_year = ft.indexBy('year_short', coin_ft)
    for year, year_coins in coins_by_year.items():
        if result_found:
            break
        if year == query_year:
            coins_by_denom = ft.indexBy('denom', year_coins)
            for denom, denom_coins in coins_by_denom.items():
                if result_found:
                    break
                if denom == query_denom:
                    if query_mint is not None:
                        coins_by_mint = ft.indexBy('mint', denom_coins)
                        for mint, mint_coins in coins_by_mint.items():
                            if mint == query_mint:
                                # ding ding ding: year, denom, & mint match
                                results = mint_coins
                                result_found = True
                                break
                        else:
                            # mint loop completed without breaks, means no mint
                            # match was found ... return denomination matches
                            # anyway (max 4-5 coins, user can choose)
                            results = denom_coins
                            result_found = True
                            break
                    else:
                        # query_mint is none, return denominations
                        results = denom_coins
                        result_found = True
                        break
            else:
                # denomination loop completed without breaking, no match found
                # perhaps that denomination was not minted in the specified year
                results = None
                break
    else:
        # year loop completed without breaking, no year match found
        # perhaps the specified year was out of range, or mistyped
        results = None

    # rank results by Levenshtein Edit Distance
    if results is not None:
        if len(results) > 1:
            results = rank_results(query_norm, results)

    return results


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

    if args.query is None:
        sys.exit("Please provide a query with the -q option")

    query = validate_query(args.query)
    print(f"Recognized Query:")
    print(f"\tInput: {query[3]}")
    print(f"\tYear: {query[0]}")
    print(f"\tMint: {query[2]}")
    print(f"\tDenomination: {query[1]}")
    query_results = query_price_guide(query, price_guide)
    if query_results is None:
        print(f"Found 0 results")
        sys.exit()
    print(f"Found {len(query_results)} results:")
    for query_result in query_results:
        print(f"\t{query_result['description']}")
