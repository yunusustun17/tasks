import time
import uuid

import flask
from flask import request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

app = flask.Flask(__name__)


def run(url_list):
    result_list = []
    error_list = []

    for url in url_list:
        browser = None
        try:
            # chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument("--no-sandbox")
            # chrome_options.add_argument("--headless")
            # chrome_options.add_argument("--disable-gpu")
            # browser = webdriver.Chrome(options=chrome_options)
            # browser.maximize_window()

            options = webdriver.ChromeOptions()
            options.add_argument("start-maximized")
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            browser = webdriver.Chrome(options=options)

            stealth(browser,
                    languages=["en-US", "en"],
                    vendor="Google Inc.",
                    platform="Win32",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
                    )

            browser.get(url)
            time.sleep(5)

            try:
                try:
                    price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div[1]/span[2]/span').text
                    if price == '':
                        price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/span[2]/span').text
                except:
                    price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/span[2]/span').text
            except:
                try:
                    price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[3]/div[2]/div/div/div[2]/div[1]/div/div/div[1]/span[2]/span').text
                except:
                    try:
                        price = browser.find_element(By.XPATH, '//*[@id="u146-tabs--14-content-0"]/div/div[3]/div[1]/div/div[2]/div/div/div[1]/span[2]/span').text
                    except:
                        try:
                            price = browser.find_element(By.XPATH, '//*[@id="u147-tabs--140-content-0"]/div/div[3]/div[1]/div/div[2]/div/div/div[1]/span[2]/span').text
                        except:
                            price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[1]/div[1]/div/div/div/div/span[1]/span[1]').text.split(' ')[3]


            try:
                course_name = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[3]/div/div/div[3]/div/h1').text
            except:
                course_name = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[4]/div/div/div[3]/div/h1').text

            old_price = None
            discount = None
            try:
                try:
                    old_price = browser.find_element(By.XPATH, '//*[@id="u147-tabs--140-content-0"]/div/div[3]/div[1]/div/div[2]/div/div/div[2]/div/span[2]/s/span').text
                    if old_price == '':
                        old_price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div[2]/div/span[2]/s/span').text
                    if old_price == '':
                        old_price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/span[2]/s/span').text
                except:
                    old_price = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div[2]/div/span[2]/s/span').text

                discount = browser.find_element(By.XPATH, '//*[@id="udemy"]/div[1]/div[2]/div/div/div[1]/div[2]/div[1]/div/div[1]/div[2]/div/div/div[1]/div/div[2]/div/div/div[3]/span[2]').text
                if discount == '':
                    discount = browser.find_element(By.XPATH, '//*[@id="u147-tabs--140-content-0"]/div/div[3]/div[1]/div/div[2]/div/div/div[3]/span[2]').text
            except:
                pass

            if old_price and discount:
                result_list.append(f"Price: {price} - Old Price: {old_price} - Discount: {discount} - Course Name: {course_name}")
            elif old_price:
                result_list.append(f"Price: {price} - Old Price: {old_price} - Course Name: {course_name}")
            else:
                result_list.append(f"Price: {price} - Course Name: {course_name}")
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
