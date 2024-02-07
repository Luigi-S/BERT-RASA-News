# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
urlcountry = os.getenv("url")
apikey=os.getenv("apiKey")
urlsource=os.getenv("urlsources")
urltop=os.getenv("urltopic")


""" = = = UTILITY FUNCTIONS = = = """

# GET request to server
def queryServer(url, body):
    pass

# plot a single article
def plotArticle(article):
    # analize article: title, snippet, image, author, source, link, category, topics
    pass

# plot article list
def plotArticleList(list):
    for article in list:
        plotArticle(article)




#    - - - HOTTEST NEWS - - -
class ActionHottestNews(Action):
    def name(self) -> Text:
         return "action_hottest_news"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # query a server per una notizia del momento
        # ricevuta, scrive titolo e snippet(se esiste)
        # la linka
        # richiesta cosa posso fare -> TODO lo cambierei

        dispatcher.utter_message(text="...HOTTEST TITLE")
        dispatcher.utter_message(image="link to image")
        dispatcher.utter_message(text="...HOTTEST SNIPPET")
        dispatcher.utter_message(text="...HOW CAN I HELP YOU")
        return []

class ActionQueryNews(Action):
    def name(self) -> Text:
         return "action_query_news"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # FORM!
        # query a server per una notizia + TOPIC, CATEGORY, AUTHOR, SOURCE, WHEN-> ANNO/MESE

        # SORRY O PLOT_LIST
        dispatcher.utter_message(text="...SORRY O LIST")
        # nuovo FORM
        dispatcher.utter_message(text="...FORM")
        return []


#    - - - WEATHER - - -
class ActionWeather(Action):
    def name(self) -> Text:
        return "action_wheater"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # query a server per il meteo con LUOGO
        # ricevuta, riporta
        # vuoi altro?

        dispatcher.utter_message(text="...WEATHER")
        dispatcher.utter_message(text="...WANT SOME MORE?")
        return []

class ActionWeatherMore(Action):
    def name(self) -> Text:
        return "action-more_wheater"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # query a server per il meteo con LUOGO + DATA
        # ricevuta, troppo? YES: error NO: riporta + vuoi altro?

        dispatcher.utter_message(text="...WEATHER")
        dispatcher.utter_message(text="...OPTIONAL BEHAVIOR")
        return []




#    - - - CATEGORY - - -
class ActionCategoryNews(Action):
    def name(self) -> Text:
         return "action_category_news"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # query a server per una notizia del momento con ARGOMENTO
        # ricevuta, scrive titolo e snippet(se esiste)
        # la linka
        # richiesta cosa posso fare

        #LISTA DI
        dispatcher.utter_message(text="...TITLE")
        dispatcher.utter_message(image="OPT: link to image")
        dispatcher.utter_message(text="...OPT: SNIPPET")
        #
        dispatcher.utter_message(text="...MORE?")
        return []


class ActionCategoryNewsMore(Action):
    def name(self) -> Text:
         return "action_category_more"


    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # query a server per una notizia del momento con ARGOMENTO+PAGINATION
        # ricevuta, scrive titolo e snippet(se esiste)
        # la linka
        # richiesta cosa posso fare

        #LISTA DI
        dispatcher.utter_message(text="...TITLE")
        dispatcher.utter_message(image="OPT: link to image")
        dispatcher.utter_message(text="...OPT: SNIPPET")
        #
        dispatcher.utter_message(text="...MORE?")
        return []



#    - - - SOURCE - - -
class ActionSourceNews(Action):
    def name(self) -> Text:
        return "action_source_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # query a server per una notizia del momento con SOURCE
        # ricevuta, scrive titolo e snippet(se esiste)
        # la linka
        # richiesta cosa posso fare

        # LISTA DI
        dispatcher.utter_message(text="...TITLE")
        dispatcher.utter_message(image="OPT: link to image")
        dispatcher.utter_message(text="...OPT: SNIPPET")
        #
        dispatcher.utter_message(text="...MORE?")
        return []


class ActionSourceNewsMore(Action):
    def name(self) -> Text:
        return "action_source_more"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # query a server per una notizia del momento con SOURCE+PAGINATION
        # ricevuta, scrive titolo e snippet(se esiste)
        # la linka
        # richiesta cosa posso fare

        # LISTA DI
        dispatcher.utter_message(text="...TITLE")
        dispatcher.utter_message(image="OPT: link to image")
        dispatcher.utter_message(text="...OPT: SNIPPET")
        #
        dispatcher.utter_message(text="...MORE?")
        return []



#    - - - MORE INFO - - -
class ActionAuthorInfo(Action):
    def name(self) -> Text:
        return "action_info_author"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # query a server per info su source
        # ricevuta, null? YES -> sorry NO-> plot

        dispatcher.utter_message(text="...SORRY O PLOT")
        return []

class ActionSourceInfo(Action):
    def name(self) -> Text:
        return "action_info_source"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # query a server per info su source
        # ricevuta, null? YES -> sorry NO-> plot

        dispatcher.utter_message(text="...SORRY O PLOT")
        return []


#      - - - FEEDBACK - - -
class ActionBrokenLink(Action):
    def name(self) -> Text:
        return "action_broken_link"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # post a server per link malfunction
        # sorry
        dispatcher.utter_message(text="...SORRY")

        cal_serSize = tracker.latest_message['entities'][0]['value']
        query = f'SELECT name, servin_size, energy_kcal_value FROM mulino_bianco WHERE energy_kcal_value<({cal_serSize}*100)/servin_size'

        #cursor.execute(query) # accesso a db
        result = [] #cursor.fetchall() ROBA DA DB
        if len(result) == 0:
            dispatcher.utter_message("Non ci sono prodotti che rispettano questa condizione!")
        else:
            pl = f"I prodotti con meno di {cal_serSize} a porzione sono: \n"
            for elem in result:
                if not elem[0] in pl:
                    pl = pl + f' - {elem[0]}, porzione: {elem[1]}, kcal per porzione: {(elem[1] * elem[2]) / 100}\n'
            dispatcher.utter_message(text=pl)
        # dispatcher.utter_message(text=nome_brand)

        #return []
        return [{"name": "calorie_slot", "event": "slot", "value": None}]


class ActionNewsScore(Action):
    def name(self) -> Text:
        return "action_news_score"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO
        # post a server score news
        # Thank U

        dispatcher.utter_message(text="...THANK U")
        return []



