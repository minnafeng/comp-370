import json
import requests
import logging

logger = logging.getLogger(__name__)

SHOW_QUERY_STRING_TEMPLATE = "https://api.tvmaze.com/search/shows?q={}"
EPISODES_QUERY_STRING_TEMPLATE = "https://api.tvmaze.com/shows/{}/episodes"


def collect_episodes(show_name, output_path_json):
    show_id = fetch_show_id(show_name)
    episodes = fetch_episodes(show_id)

    with open(output_path_json, "w") as f:
        json.dump(episodes, f, indent=4)


def fetch_show_id(show_name):
    show_name = show_name.replace(" ", "+")
    url = SHOW_QUERY_STRING_TEMPLATE.format(show_name)

    logger.debug("Fetching show id from {}".format(url))

    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    # grab id of first show
    show_id = data[0]["show"]["id"]
    return show_id


def fetch_episodes(show_id):
    url = EPISODES_QUERY_STRING_TEMPLATE.format(show_id)

    logger.debug("Fetching episodes from {}".format(url))

    response = requests.get(url)
    response.raise_for_status()

    return response.json()
