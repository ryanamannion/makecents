# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import glob
from typing import Any, Text, Dict, List

from pcgs_scraper import pcgs_query
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionReturnPrice(Action):

    # def __init__(self):
    #     if os.path.isfile('')

    def name(self) -> Text:
        return "action_return_price"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        coin_query = tracker.get_latest_entity_values("coin")

        validated_query = next(pcgs_query.validate_query(coin_query, verbose=False), None)

        # cant query the price guide because it needs to load the table first,
        # and I need to make the file system better for that
        # TODO:
        #   - use glob to get pcgs_price_guide files and write a function to
        #     pick out the latest one using datetime

        dispatcher.utter_message(text="Hello World!")

        return []
