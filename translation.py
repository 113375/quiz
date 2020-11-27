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
        'Authorization': 'Bearer t1.9euelZqelJGKzsiMyMmSlovLzZSXje3rnpWai46Zz5zInYzGzMuam42SnZrl8_dpCX4B-u93eWcz_t3z9yk4ewH673d5ZzP-.WL9IIYcDvnO4xj7hNIGCDSKsxldkrm3v_CQDYJjn8thZogR9xzO5XSdlYv3dMWw2qwqDvLjlw_t_gdcRXrLhCA',
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