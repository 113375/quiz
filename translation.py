import os
import sys
import json
#import requests


def translation(word, lang):
    json_dict = {
        "folder_id": "b1gknd3qa346b2r17fn6",
        "texts": [f"{word}"],
        "targetLanguageCode": lang
    }

    headers = {
        'Authorization': 'Bearer t1.9euelZrJm4zLz8iQmImej5qXipWQnO3rnpWai46Zz5zInYzGzMuam42SnZrl8_cyXQcC-u9_S0Iz_N3z93ILBQL6739LQjP8.kscbwZcJTM-MmjkQxRmzDnH51tKasKC8yfdh5H9sJHxgHN8HlA2nwW_dL87U8b1_BoyUTU-99CRfL6ZXiIcOBg',
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