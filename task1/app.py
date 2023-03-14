import re

import bs4
import flask
import urllib3
from flask import request

app = flask.Flask(__name__)


def is_letter_non_count(letter):
    return (ord(letter) >= 32 and ord(letter) <= 47) or (ord(letter) >= 58 and ord(letter) <= 64) or (ord(letter) >= 91 and ord(letter) <= 96) or (ord(letter) >= 123 and ord(letter) <= 126) or (ord(letter) >= 161 and ord(letter) <= 191) or (ord(letter) >= 48 and ord(letter) <= 57)


def is_letter_hindi_character(letter):
    return ord(letter) >= 2304 and ord(letter) <= 2431


def all_text_is_hindi_language(text):
    for i in text:
        if is_letter_non_count(i):
            continue

        if ord(i) < 2304 or ord(i) > 2431:
            return False
    return True


def clear_text_from_whitespace_characters_newlines(text):
    return re.sub(r'\s+', ' ', text)


def run(url_list):
    result_list = []
    for url in url_list:
        try:
            http = urllib3.PoolManager()
            user_agent = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'}
            r = http.request('GET', url, headers=user_agent, retries=urllib3.Retry(0))
            source = re.sub(r'<!--.*?-->', '', r.data.decode('utf-8'), flags=re.DOTALL)

            soup = bs4.BeautifulSoup(source, 'html.parser')
            for text in soup.find_all(text=True):
                if text.parent.name not in ['script', 'title', 'style', 'head', 'meta', '[document]'] and text != '\n':
                    if not all_text_is_hindi_language(clear_text_from_whitespace_characters_newlines(text)):
                        result_list.append(f"this text is not in hindi language: '''{text}''' in {url}")
                        break

        except Exception as e:
            result_list.append(f"error: {e} in {url}")

    return result_list


@app.route('/', methods=['GET', 'POST'])
def index():
    result_list = []
    if flask.request.method == 'POST':
        data = request.form
        url_list = list(filter(None, data.get('urls').split('\r\n')))
        result_list = run(url_list)
    return flask.render_template('index.html', result_list=result_list)


if __name__ == "__main__":
    app.run(debug=True)
