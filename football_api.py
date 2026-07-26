# football_api.py

import requests
from config import API_FOOTBALL_KEY, BASE_URL


HEADERS = {
    "x-apisports-key": API_FOOTBALL_KEY
}


def api_request(endpoint, params=None):

    url = BASE_URL + endpoint

    response = requests.get(
        url,
        headers=HEADERS,
        params=params
    )

    return response.json()



# Αναζήτηση ομάδας

def search_team(team_name):

    data = api_request(
        "/teams",
        {
            "search": team_name
        }
    )

    if not data.get("response"):
        return None

    return data["response"][0]["team"]



# Τελευταία παιχνίδια ομάδας

def get_last_matches(team_id, number=10):

    data = api_request(
        "/fixtures",
        {
            "team": team_id,
            "last": number
        }
    )

    return data.get("response", [])



# Προϊστορία μεταξύ ομάδων

def get_h2h(team1_id, team2_id):

    data = api_request(
        "/fixtures/headtohead",
        {
            "h2h": f"{team1_id}-{team2_id}",
            "last": 10
        }
    )

    return data.get("response", [])



# Στατιστικά αγώνα

def get_fixture_statistics(fixture_id):

    data = api_request(
        "/fixtures/statistics",
        {
            "fixture": fixture_id
        }
    )

    return data.get("response", [])



# Predictions API (όπου διαθέσιμο)

def get_prediction(fixture_id):

    data = api_request(
        "/predictions",
        {
            "fixture": fixture_id
        }
    )

    return data.get("response", [])



# Λίστα διοργανώσεων

def get_leagues():

    data = api_request(
        "/leagues"
    )

    return data.get("response", [])



# Σημερινά παιχνίδια

def get_today_fixtures():

    data = api_request(
        "/fixtures",
        {
            "date": "2026-07-27"
        }
    )

    return data.get("response", [])
