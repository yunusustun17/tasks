import time

import flask
from flask import request
from selenium import webdriver
from selenium.webdriver.common.by import By

app = flask.Flask(__name__)


def run(url_list):
    result_list = []
    error_list = []

    for url in url_list:
        browser = None
        try:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            # chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-gpu")
            browser = webdriver.Chrome(options=chrome_options)
            browser.maximize_window()

            browser.get(url)
            time.sleep(3)

            price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/span[2]/span').text
            course_name = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[3]/div/div/div[3]/div/h1').text

            old_price = None
            discount = None
            try:
                old_price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div/span[2]/s/span').text
                discount = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div[3]/span[2]').text
            except Exception as e:
                pass

            if old_price and discount:
                result_list.append(f"{price} - {old_price} - {discount} - {course_name}")
            else:
                result_list.append(f"{price} - {course_name}")
        except Exception as e:
            error_list.append(f"error: {e} in {url}")
            continue
        finally:
            browser.close()

    return (result_list, error_list)


@app.route('/', methods=['GET', 'POST'])
def index():
    result_list = []
    error_list = []
    if flask.request.method == 'POST':
        data = request.form
        url_list = list(filter(None, data.get('urls').split('\r\n')))
        if len(url_list) > 10:
            error_list.append('10 urls max')
        else:
            (result_list, error_list) = run(url_list)
    return flask.render_template('index.html', result_list=result_list, error_list=error_list)


if __name__ == "__main__":
    app.run(debug=True)
