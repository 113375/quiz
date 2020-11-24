import os
import sys
import json
import requests


def translation(word, lang):
    json_dict = {
        "folder_id": "b1gknd3qa346b2r17fn6",
        "texts": [f"{word}"],
        "targetLanguageCode": lang
    }

    headers = {
        'Authorization': 'Bearer t1.9euelZqZzs-Uz8yXncrHiZCQm5OTje3rnpWai46Zz5zInYzGzMuam42SnZrl8_cWegsC-u9PWxJD_N3z91YoCQL6709bEkP8.nNbdtd1ELN4vc2apFoe8hCIZNUCRnPgHFaDy6kbER42s-klsEezh9_RvjGVSKNowMQ1HZhe1T3tsr2kCVUZ8CQ',
        'Content-Type': 'application/json'}

    response = requests.post(
        'https://translate.api.cloud.yandex.net/translate/v2/translate',
        json=json_dict,
        headers=headers
    )
    s = json.loads(response.text)
    return s['translations'][0]['text']


def new_token():
    pass