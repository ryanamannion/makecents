# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import os
import glob
from datetime import datetime, date, time
import pickle
from typing import Any, Text, Dict, List

from pcgs_scraper import pcgs_query, utils
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


def most_recent_guide():
    pcgs_files = glob.glob('./data/pcgs_price_guide*')

    file_datetimes = []

    for pcgs_file in pcgs_files:
        # file is format: pcgs_price_guide-YYYYMMDD-HHMMSS.pkl
        # .pkl is [-4:]
        date_format = pcgs_file[-19:-4]
        year = int(date_format[:4])
        month = int(date_format[4:6])
        day = int(date_format[6:8])
        # skip hyphen
        hour = int(date_format[9:11])
        minute = int(date_format[11:13])
        second = int(date_format[13:15])
        d = date(year, month, day)
        t = time(hour, minute, second)
        this_file_datetime = datetime.combine(d, t)

        file_datetime = (pcgs_file, this_file_datetime)
        file_datetimes.append(file_datetime)

    most_recent = max(file_datetimes, key=lambda x: x[1])

    price_guide = pickle.load(open(most_recent[0], 'rb'))

    return price_guide


class ActionReturnPrice(Action):

    # def __init__(self):
    #     if os.path.isfile('')

    def name(self) -> Text:
        return "action_return_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        coin_entities = tracker.get_latest_entity_values("coin")
        *_, last = coin_entities

        validated_query = pcgs_query.validate_query(last, verbose=False)
        price_guide = most_recent_guide()

        results = pcgs_query.query_price_guide(validated_query, price_guide)

        if len(results) == 0:
            msg = "I'm sorry, I could not find a coin matching your query."
            dispatcher.utter_message(text=msg)
            dispatcher.utter_message(template='utter_search_help')
        elif len(results) == 1:
            result = results[0]
            prices = utils.price_table(result['desig'], result['prices'])
            dispatcher.utter_message(text=prices)
        elif len(results) > 1:
            """
            User query returns more than one coin result:
                - tell user the results
                - give user buttons
                - buttons return exact description of coin, which should return
                  just that coin with pcgs_query.query_price_guide()
            """
            dispatcher.utter_message("I found multiple results for your query.")
            descriptions = [x['description'] for x in results]
            buttons = []
            for description in descriptions:
                button = {
                    "payload": description,
                    "title": description
                }
                buttons.append(button)
            dispatcher.utter_message("Please select the coin you would like to "
                                     "inspect: ", buttons=buttons)

        return []
