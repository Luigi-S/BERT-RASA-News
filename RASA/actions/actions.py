# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
from datetime import datetime
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, AllSlotsReset, UserUtteranceReverted


import requests
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)
URL = os.getenv("URL")
APIKEY = os.getenv("APIKEY")
SNIPPET_CHARS = 200

""" = = = UTILITY FUNCTIONS = = = """


# GET request to server
def queryServer(url, params=None):
    try:
        print(params)
        if params is None:
            params = {'apikey': APIKEY}
        else:
            params['apikey'] = APIKEY
        response = requests.get(url, headers=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Errore: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# POST request to server
def postServer(url, params=None):
    try:
        if params is None:
            params = {'apikey': APIKEY}
        else:
            params['apikey'] = APIKEY
        response = requests.post(url, headers=params)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Errore: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None


# plot a single article
def plotArticle(article, dispatcher):
    # analize article: title, snippet, image, author, source, link, category, topics
    dispatcher.utter_message(text=f"**{article['title']}**")
    if 'img' in article:
        #dispatcher.utter_message(image=article['img'])
        pass
    dispatcher.utter_message(text=truncate_string(article['content']))
    art_infos = ""
    if 'author' in article and len(article['author']) > 0:
        art_infos = "By:"
        for a in article['author']:
            art_infos += f" {a}"
    if art_infos != "":
        dispatcher.utter_message(text=art_infos)
    source_infos = ""
    if 'source' in article:
        source_infos += article['source']
    if 'date' in article:
        source_infos += f" {article['date']}"
    if source_infos != "":
        dispatcher.utter_message(text=source_infos)
    dispatcher.utter_message(text=article['link'])


# plot article list
def plotArticleList(list, dispatcher):
    for article in list:
        plotArticle(article, dispatcher)
        dispatcher.utter_message(text="------------------------")


def truncate_string(str, max_chars=SNIPPET_CHARS):
    if len(str) <= max_chars:
        return str
    # Find the last space before the maximum character limit
    last_space_index = str[:max_chars].rfind(' ')
    truncated_string = str[:last_space_index]
    return truncated_string + "..."


def get_entity_values(msg, name):
    values = []
    for e in msg['entities']:
        if e['entity'] == name:
            values.append(e['value'])
    return values



#    - - - HOTTEST NEWS - - -
class ActionHottestNews(Action):
    def name(self) -> Text:
        return "action_hottest_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        res = queryServer(URL + '/hottest')

        if res is None:
            # TODO: SORRY
            dispatcher.utter_message(text="...SORRY")
        else:
            plotArticleList(res, dispatcher)
        # TODO: buttons!
        dispatcher.utter_message(text="...HOW CAN I HELP YOU")
        return []


#    - - - WEATHER - - -
class ActionWeather(Action):
    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        where = tracker.get_slot('where') #get_entity_values(tracker.latest_message, 'where')
        when = tracker.get_slot('time')   # get_entity_values(tracker.latest_message, 'when')
        if where is not None:
            if when is not None:
                print(f"IL TEMPO RICHIESTO è : {when}")
                response = queryServer(URL + '/weather', {'where': where, 'when': when})
            else:
                response = queryServer(URL + '/weather', {
                    'where': where,
                    'when': datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
                })
            if response is not None:
                dispatcher.utter_message(text=f"The weather in {response['where']}")
                dispatcher.utter_message(image=response['weather_icon'])
                dispatcher.utter_message(text=response['weather_txt'])
                return [SlotSet("time", when), SlotSet("time", where)]
            else:
                dispatcher.utter_message(
                    text='Sorry I couldn\'t get the weather forecasts')  # TODO personalizza i sorry
        else:
            # TODO completare rotta con creazione weather_form
            dispatcher.utter_message(text= "...NOT ENOUGH DATA TO RETRIEVE WEATHER, TRY ASKING AGAIN")
            return []
        return []

#    - - - CATEGORY - - -
class ActionCategoryNews(Action):
    def name(self) -> Text:
        return "action_category_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        category = tracker.get_slot('category')
        res = queryServer(URL+'/category', {"category": category})
        dispatcher.utter_message(text=f"News: {res['category']}")
        plotArticleList(res['news'], dispatcher)

        dispatcher.utter_message(text="...MORE?")
        return [SlotSet("category", category), SlotSet("cat_page", 0)]


class ActionCategoryNewsMore(Action):
    def name(self) -> Text:
        return "action_category_more"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            category = tracker.get_slot('category')
            page = tracker.get_slot('cat_page')+1
            res = queryServer(URL+'/category', {"category": category, "page": str(page)})
            print(f"RES: {res}")
            dispatcher.utter_message(text=f"News: {res['category']}, page: {res['page']}")
            plotArticleList(res['news'], dispatcher)

            dispatcher.utter_message(text="...MORE?")
            return [SlotSet("cat_page", page)]
        except Exception:
            dispatcher.utter_message(text="...SORRY")
            return[]


#    - - - SOURCE - - -
class ActionSourceNews(Action):
    def name(self) -> Text:
        return "action_source_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        source = tracker.get_slot('source') #get_entity_values(tracker.latest_message, 'source')
        res = queryServer(URL + '/source', {"source": source})
        dispatcher.utter_message(text=f"News: {res['source']}")
        plotArticleList(res['news'], dispatcher)

        dispatcher.utter_message(text="...MORE?")
        return [SlotSet("source", source), SlotSet("src_page", 0)]


class ActionSourceNewsMore(Action):
    def name(self) -> Text:
        return "action_source_more"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            source = tracker.get_slot('source')
            page = tracker.get_slot('src_page') + 1
            res = queryServer(URL + '/source', {"source": source, "page": str(page)})
            dispatcher.utter_message(text=f"News: {res['source']}, page: {res['page']}")
            plotArticleList(res['news'], dispatcher)

            dispatcher.utter_message(text="...MORE?")
            return [SlotSet("src_page", page)]
        except Exception:
            dispatcher.utter_message(text="...SORRY")
            return []


#    - - - TOPICS - - -
class ActionTopicsNews(Action):
    def name(self) -> Text:
        return "action_topics_news"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        category = tracker.get_slot('category') # get_entity_values(tracker.latest_message, 'category')
        places = get_entity_values(tracker.latest_message, 'place')
        people = get_entity_values(tracker.latest_message, 'people')
        orgs = get_entity_values(tracker.latest_message, 'organization')
        topics = {
            'category': category,
            'place': places,
            'people': people,
            'organization': orgs
        }
        res = queryServer(URL + '/topics', {"topics":str(topics)})
        cat_res = "Generics" if 'category' not in res else res['category']
        dispatcher.utter_message(text=f"News: {cat_res}")
        plotArticleList(res['news'], dispatcher)

        dispatcher.utter_message(text="...MORE?")
        return [SlotSet("topics", topics), SlotSet("topics_page", 0)]


class ActionTopicsNewsMore(Action):
    def name(self) -> Text:
        return "action_topics_more"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        try:
            topics = tracker.get_slot('topics')
            page = tracker.get_slot('topics_page') + 1
            res = queryServer(URL + '/topics', {"topics": str(topics), "page": str(page)})

            cat_res = "Generics" if 'category' not in res else res['category']
            dispatcher.utter_message(text=f"News: {cat_res}, page: {res['page']}")
            plotArticleList(res['news'], dispatcher)

            dispatcher.utter_message(text="...MORE?")
            return [SlotSet("topics_page", page)]
        except Exception:
            dispatcher.utter_message(text="...SORRY")
            return[]


#    - - - OTHER INFO - - -

class ActionSourceInfo(Action):
    def name(self) -> Text:
        return "action_info_source"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        source = tracker.get_slot('source')
        if source is not None:
            res = queryServer(URL + '/info/source', {'source': source})
            if res is not None:
                dispatcher.utter_message(text=f"{res['source']} is a newspaper")
                return [SlotSet("source", source)]
            else:
                dispatcher.utter_message(
                    text='Sorry I couldn\'t get information about it')
        else:
            dispatcher.utter_message(text="...Sorry i didn't quite get what you want to know about")
        return []


#      - - - FEEDBACK - - -
class ActionBrokenLink(Action):
    def name(self) -> Text:
        return "action_broken_link"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # bad feedback
        id = 0    # TODO get id from slot
        postServer(URL+'/feedback', {'article_id': id, 'good': False})

        dispatcher.utter_message(text="...SORRY")
        return []


class ActionGoodFeed(Action):
    def name(self) -> Text:
        return "action_good_feed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # TODO inserire sentiment analysis??
        id = 0
        postServer(URL+'/feedback', {'article_id': id, 'good': True})
        # ignore errors...

        dispatcher.utter_message(text="...THANK U")
        return []


class ActionBadFeed(Action):
    def name(self) -> Text:
        return "action_bad_feed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # TODO inserire sentiment analysis??
        id = 0
        postServer(URL + '/feedback', {'article_id': id, 'good': False})
        # ignore errors...

        dispatcher.utter_message(text="...SORRY")
        return []


"""
**================================================**
            =  =  =  VALIDATION  =  =  =                        
**================================================**
"""
class ValidateWeatherForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_weather_form"

    async def validate_where(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # Perform any validation if needed
        dispatcher.utter_message(text='Ok, and when?')
        return {"where": slot_value}

    async def validate_time(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        # TODO check date is in the future... convert in datetime
        return {"time": slot_value}



"""
---------------------------------------
        Buttons :>)
---------------------------------------
"""

class ActionUtterStart(Action):
    def name(self) -> Text:
        return "action_utter_start"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {"payload": '/hottest_news', "title": "News Headline", "button_type":"vertical"},
            {"payload": '/news_from_source', "title":  "News from specific source", "button_type":"vertical"},
            {"payload": '/news_categories', "title":  "News Categories", "button_type":"vertical"},
            {"payload": '/weather_no_place', "title": "Weather Forecast", "button_type": "vertical"},
        ]
        msg = "Hi! Welcome to the JournAI bot! To keep reading select one of the buttons or write a message!"
        dispatcher.utter_message(text=msg, buttons=buttons)
        return [AllSlotsReset()]


class ActionCategoryChoice(Action):
    def name(self) -> Text:
        return "action_category_choice"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        buttons = [
            {"payload": '/cat_sel{"category":"sports"}', "title": "Sports", "button_type":"vertical"},
            {"payload": '/cat_sel{"category":"technology"}', "title":  "Technology", "button_type":"vertical"},
            {"payload": '/cat_sel{"category":"politics"}', "title":  "Politics", "button_type":"vertical"},
            {"payload": '/cat_sel{"category":"business"}', "title": "Business", "button_type": "vertical"},
        ]
        msg = "Please, select one of the categories with these buttons"
        dispatcher.utter_message(text=msg, buttons=buttons)
        return []

class ActionRepeat(Action):
    def name(self) -> Text:
        return "action_repeat"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(text='...REPEAT ACTIVATED!')
        user_ignore_count = 2
        count = 0
        tracker_list = []

        while user_ignore_count > 0:
            event = tracker.events[count].get('event')
            if event == 'user':
                user_ignore_count = user_ignore_count - 1
            if event == 'bot':
                tracker_list.append(tracker.events[count])
            count = count - 1

        i = len(tracker_list) - 1
        while i >= 0:
            data = tracker_list[i].get('data')
            print(data)
            if data:
                if ("buttons" in data) and ("image" in data):
                    dispatcher.utter_message(
                        text=tracker_list[i].get('text'), buttons=data["buttons"], image=data["image"])
                elif "buttons" in data:
                    dispatcher.utter_message(text=tracker_list[i].get('text'), buttons=data["buttons"])
                elif "images" in data:
                    dispatcher.utter_message(text=tracker_list[i].get('text'), image=data["image"])
                else:
                    dispatcher.utter_message(text=tracker_list[i].get('text'))
            i -= 1

        return []

