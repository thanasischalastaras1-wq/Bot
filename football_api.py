# football_api.py

import requests
from datetime import datetime

from config import BASE_URL, API_FOOTBALL_KEY


HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}


def api_call(endpoint, params=None):

    url = BASE_URL + endpoint

    response = requests.get(
        url,
        headers=HEADERS,
        params=params
    )

    return response.json()



# Όλοι οι αγώνες της ημέρας

def today_matches():

    today = datetime.now().strftime("%Y-%m-%d")

    data = api_call(
        "/fixtures",
        {
            "date": today
        }
    )

    return data.get("response", [])



# Τελευταία παιχνίδια ομάδας

def last_matches(team_id):

    data = api_call(
        "/fixtures",
        {
            "team": team_id,
            "last": 10
        }
    )

    return data.get("response", [])



# Προϊστορία

def h2h(team1, team2):

    data = api_call(
        "/fixtures/headtohead",
        {
            "h2h": f"{team1}-{team2}",
            "last": 10
        }
    )

    return data.get("response", [])



# Predictions API

def predictions(fixture_id):

    data = api_call(
        "/predictions",
        {
            "fixture": fixture_id
        }
    )

    return data.get("response", [])



# Στατιστικά αγώνα

def fixture_stats(fixture_id):

    data = api_call(
        "/fixtures/statistics",
        {
            "fixture": fixture_id
        }
    )

    return data.get("response", [])
