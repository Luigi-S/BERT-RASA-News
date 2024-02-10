from datetime import datetime

from flask import Flask, request, jsonify

from Category import NewsCategory

app = Flask(__name__)

ARTICLE = {
    "id": 0,
    "title": "Donald Trump's failed immunity appeal is still a win for his delay strategy",  # MUST HAVE
    "content": """
    Donald Trump has been handed a defeat in court - but one that comes with a generous helping of 
    victory. An appeals court ruled that Mr Trump is not immune from criminal prosecution for acts committed while he 
    was president. The time it took to issue that decision, however, has indefinitely delayed Mr Trump's federal 
    trial related to the 6 January 2021 attack on the US Capitol. So while Mr Trump did not successfully assert 
    sweeping new presidential powers to act with impunity while in office, the tentative 4 March start date in 
    Washington DC has been removed from the federal court's calendar. And there is no indication of when it might 
    reappear. This is in keeping with the former president's strategy of throwing sand in the gears of the judicial 
    process whenever possible, according to Neama Rahmani, a former federal prosecutor. "It's in Trump's interest to 
    delay the case until after the November election," Mr Rahmani said. "If he wins control of the White House, 
    a sitting president can't be prosecuted." If delay is the goal, there are a few steps Mr Trump's legal team could 
    now follow. They might request that the full 11-judge DC Circuit Court of Appeals review and reconsider this 
    case. That is unlikely to succeed, however, as six of the eight remaining judges would have to back that decision 
    and obliging such a request is rare. The appeals court, meanwhile, has ruled that the 6 January case can proceed 
    while such a request is considered. Perhaps in the hope of avoiding further delay.
    """,  # MUST HAVE
    "author": ["Anthony Zurcher", "Matt Murphy"],
    "source": "BBC News",
    "img": "https://ichef.bbci.co.uk/news/976/cpsprodpb/16799/production/_132575029_gettyimages-1918188009-2.jpg.webp",
    "link": "https://www.bbc.com/news/world-us-canada-68061183",  # MUST HAVE
    "date": datetime.strptime('07/02/2024 13:55:26', '%m/%d/%Y %H:%M:%S'),
    "topic": ["Donald Trump", "United States Court of Appeals for the District of Columbia Circuit",
              "White House", "United States Capitol", "President of the United States", "USA"],
    "category": NewsCategory.POLITICS.name
}


@app.route('/get-example/<int:user_id>', methods=['GET'])
def get_example(user_id):
    # Access the path variable user_id
    # For example, you can use it to fetch user data from a database
    user_data = {
        'id': user_id,
        'name': 'John Doe',
        'email': 'john@example.com'
    }

    # Access the request body (if it exists)
    request_data = request.json

    # Return a JSON response with user data and request body
    return jsonify({
        'user_data': user_data,
        'request_data': request_data
    })


@app.route('/weather', methods=['GET'])
def get_weather():
    try:
        request_data = request.headers
        print(request_data)
        if is_valid_key(request_data['apikey']):  # .get('apikey')
            # body = request_data.get('body')
            # Return a JSON response with user data and request body
            where = request_data['where']
            when = request_data['when']
            return jsonify({
                'where': where,
                'when': when,
                'weather_txt': 'SUNNY_DUMMY',
                'weather_icon': 'https://icon-park.com/imagefiles/simple_weather_icons_sunny.png'
            }), 200
        else:
            return "Unauthourized", 401
    except Exception:
        return "BadRequest", 400


@app.route('/hottest', methods=['GET'])
def get_hottest():
    try:
        request_data = request.headers
        if is_valid_key(request_data['apikey']):
            return jsonify([ARTICLE for i in range(2)]), 200
        else:
            return "Unauthourized", 401
    except Exception as e:
        print(e.args)
        return "BadRequest", 400


@app.route('/category', methods=['GET'])
def get_category():
    try:
        request_data = request.headers
        if is_valid_key(request_data['apikey']):
            # TODO cambia i dummy
            page = 0 if 'page' not in request_data else request_data['page']
            return jsonify({
                "category": request_data['category'],
                "news": [ARTICLE for i in range(2)],
                "page": page
            }), 200
        else:
            return "Unauthourized", 401
    except Exception as e:
        print(e.args)
        return "BadRequest", 400


@app.route('/topics', methods=['GET'])
def get_topics():
    try:
        request_data = request.headers
        if is_valid_key(request_data['apikey']):
            # TODO cambia i dummy
            page = 0 if 'page' not in request_data else request_data['page']
            # ranking delle notizie in base a hotness e pertinenza con il topic...
            topics = request_data['topics']
            return jsonify({
                "topics": topics,
                "news": [ARTICLE for i in range(2)],
                "page": page
            }), 200
        else:
            return "Unauthourized", 401
    except Exception as e:
        print(e.args)
        return "BadRequest", 400


@app.route('/source', methods=['GET'])
def get_source():
    try:
        request_data = request.headers
        if is_valid_key(request_data['apikey']):
            # TODO cambia i dummy
            page = 0 if 'page' not in request_data else request_data['page']
            return jsonify({
                "source": request_data['source'],
                "news": [ARTICLE for i in range(2)],
                "page": page
            }), 200
        else:
            return "Unauthourized", 401
    except Exception as e:
        print(e.args)
        return "BadRequest", 400


@app.route('/feedback', methods=['POST'])
def post_feed():
    try:
        request_data = request.headers
        if is_valid_key(request_data['apikey']):
            # based on 'good' and 'article_id'? update article hotness...
            # (True = buono, False, abbassa hotness)
            return "Success", 200
        else:
            return "Unauthourized", 401
    except Exception as e:
        print(e.args)
        return "BadRequest", 400


def is_valid_key(k):
    print(f'KEY CHECK OF: {k}')
    return True


if __name__ == '__main__':
    app.run(debug=True)
