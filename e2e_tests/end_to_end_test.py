import os
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pytest
from dotenv import find_dotenv, load_dotenv
import logging

from app import create_app
from db_client.index import get_db_collection
from entity.status import Status
from helpers.index import generate_random_string

log = logging.getLogger('app')


@pytest.fixture(scope='module')
def test_app():
    file_path = find_dotenv()
    load_dotenv(file_path, override=True)

    os.environ['LOGIN_DISABLED'] = 'True'

    # Set up a temporary test collection
    os.environ['MONGO_DB_DATABASE_NAME'] = 'test-table-' + generate_random_string(10)
    collection = get_db_collection()

    # Clear the collection in case it already contains data
    collection.drop()

    # Construct the new application
    application = create_app()

    # Start the app in its own thread.
    thread = Thread(target=lambda: application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application

    # Tear down, including wiping test collection
    thread.join(1)
    collection.drop()


@pytest.fixture(scope="module")
def driver():
    opts = webdriver.ChromeOptions()
    opts.add_argument('--headless')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    with webdriver.Chrome('./chromedriver', options=opts) as driver:
        yield driver


def test_task_journey(driver, test_app):
    driver.implicitly_wait(3)
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

    new_item_title_input = driver.find_element_by_name("title")
    new_item_title_input.send_keys("New element")
    new_item_title_input.send_keys(Keys.RETURN)

    driver.implicitly_wait(3)

    to_do_item = driver.find_element_by_class_name("to-do-item")
    assert to_do_item.text == "New element"

    mark_done_button = driver.find_element_by_class_name("mark-done")
    mark_done_button.click()

    done_item = driver.find_element_by_class_name("done-item")
    assert done_item.text == "New element"
