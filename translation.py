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
        'Authorization': 'Bearer t1.9euelZrMz5WUlZmVmovNnJ6Qko3Hie3rnpWai46Zz5zInYzGzMuam42SnZrl8_dCfgAC-u8fBzJ7_N3z9wItfgH67x8HMnv8.zfa3iYbW8F2ou3gHe4Vqu15939AOUbTYxdB3566pfOvICHt7D-35-Izy_ib4yQvInnyTp39gsD_cAnP0YkYhBQ',
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