import requests
import re


def remove_html_tags(text):
    """Remove html tags from a string"""
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def fetch_word(word):
    url = "https://api.pons.com/v1/dictionary"
    headers = {
        "X-Secret": "2b860670742155949e9e65d44bc6e5991c953e1b560db5b2c5670aab67fb671b",
    }
    params = {
        "q": word,
        "l": "deru",
        "in": "de",
        "language": "ru",

    }
    response = requests.get(url=url, headers=headers, params=params)
    response.raise_for_status()
    if response.status_code == 200:
        results = []
        for lang in response.json():
            if lang['lang'] == 'de':
                for hit in lang['hits']:
                    if hit['type'] == 'entry':
                        for rom in hit['roms']:
                            for arab in rom['arabs']:
                                for translation in arab['translations']:
                                    key = remove_html_tags(translation['source'])
                                    value = remove_html_tags(translation['target'])
                                    results.append({key: value})
                    elif hit['type'] == 'translation':
                        key = remove_html_tags(hit['source'])
                        value = remove_html_tags(hit['target'])
                        results.append({key: value})

        return results


    return "Nothing found"


# print(fetch_word('sich erinnern an'))
print(fetch_word('gehen'))
