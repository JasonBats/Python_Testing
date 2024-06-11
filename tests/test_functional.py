import multiprocessing
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

from server import app


def run_server():
    app.run(host="127.0.0.1", port=5000)


@pytest.fixture(scope='module')
def start_server():
    p = multiprocessing.Process(target=run_server)
    p.start()
    time.sleep(1)  # Donne le temps au serveur de démarrer
    yield
    p.terminate()
    p.join()


def test_home(start_server):
    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install())
    )
    driver.get("http://127.0.0.1:5000/")
    assert "GUDLFT Registration" == driver.title

    # Login
    form = driver.find_element(by=By.TAG_NAME, value="form")
    input_form = form.find_element(by=By.TAG_NAME, value="input")
    input_form.send_keys("john@simplylift.co")
    input_form.send_keys(Keys.ENTER)
    title = driver.find_element(by=By.TAG_NAME, value="h2").text
    assert "Welcome, john@simplylift.co" == title

    # Access book view
    book_places_urls = driver.find_elements(by=By.TAG_NAME, value="a")
    book_places_urls[1].click()
    assert driver.current_url == "http://127.0.0.1:5000/book/Spring%20Festival/Simply%20Lift"

    # Book 6 places
    places_input = driver.find_elements(
        by=By.TAG_NAME,
        value="input"
    )[2]
    places_input.send_keys("6")
    places_input.send_keys(Keys.ENTER)
    assert "Great-booking complete!" in driver.page_source

    # Try to book another 7 places > cannot
    book_places_urls = driver.find_elements(by=By.TAG_NAME, value="a")
    book_places_urls[1].click()
    assert driver.current_url == "http://127.0.0.1:5000/book/Spring%20Festival/Simply%20Lift"

    places_input = driver.find_elements(
        by=By.TAG_NAME,
        value="input"
    )[2]
    places_input.send_keys("7")
    places_input.send_keys(Keys.ENTER)
    assert "You can not book more than 12 places" in driver.page_source

    # Book one more place
    places_input = driver.find_elements(
        by=By.TAG_NAME,
        value="input"
    )[2]
    places_input.send_keys("1")
    places_input.send_keys(Keys.ENTER)
    assert "Great-booking complete!" in driver.page_source

    # Try to access past event > cannot
    book_places_urls = driver.find_elements(by=By.TAG_NAME, value="a")
    book_places_urls[2].click()
    assert "This competition is past" in driver.page_source

    # Log out and access newly implemented display_club_points view.
    # Club points should be (13-points spent) = 6.
    logout_button = driver.find_elements(by=By.TAG_NAME, value="a")[0]
    logout_button.click()  # Logged out
    assert driver.current_url == "http://127.0.0.1:5000/"

    # Display club points
    driver.get("http://127.0.0.1:5000/display_club_points")
    assert "Club : Simply Lift | Points : 6" in driver.page_source

    driver.quit()
