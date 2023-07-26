import requests
import os
import argparse
from dotenv import load_dotenv

# .envファイルをロードします
load_dotenv()

API_VERSION = os.getenv('API_VERSION')
SERVICE_NAME = os.getenv('COGNITIVE_SEARCH_NAME')
INDEX_NAME = os.getenv('COGNITIVE_SEARCH_INDEX_NAME')
COGNITIVE_SEARCH_API_KEY = os.getenv('COGNITIVE_SEARCH_API_KEY')

url = F"https://{SERVICE_NAME}.search.windows.net/indexes/{INDEX_NAME}/analyze?api-version={API_VERSION}"
headers = {"api-key": COGNITIVE_SEARCH_API_KEY}

analyzers = [
    "ja.microsoft",
    "ja.lucene"
]


class Color:
    RED = '\033[31m'
    END = '\033[0m'


def print_red(target):
    print(Color.RED + str(target) + Color.END)


def _get_tokens(word, analyzer):
    r = requests.post(url, json={"text": word, 'analyzer': analyzer}, headers=headers)
    return [token['token'] for token in r.json()['tokens']]


def main(word):
    ms_tokens = _get_tokens(word, "ja.microsoft")
    lucene_tokens = _get_tokens(word, "ja.lucene")
    if ms_tokens != lucene_tokens:
        print_red({"word": word, "ja.microsoft_tokens": ms_tokens, "ja.lucene_tokens": lucene_tokens})
    else:
        print({"word": word, "ja.microsoft_tokens": ms_tokens, "ja.lucene_tokens": lucene_tokens})


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('word', help='Word to be analyzed.')
    args = parser.parse_args()
    main(args.word)
