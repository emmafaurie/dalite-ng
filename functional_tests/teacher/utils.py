import contextlib
import time

from django.urls import reverse
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from functional_tests.fixtures import *  # noqa

MAX_WAIT = 60


def accept_cookies(browser):
    browser.find_element_by_id("accept-cookies").click()


def go_to_account(browser):
    browser.find_element_by_xpath("//i[contains(text(), 'menu')]").click()

    WebDriverWait(browser, MAX_WAIT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//i[contains(text(), 'account_circle')]")
        )
    ).click()


def login(browser, teacher):
    username = teacher.user.username
    password = "test"

    browser.get(f'{browser.server_url}{reverse("login")}')

    browser.find_element_by_id("login-teachers").click()

    username_input = browser.find_element_by_xpath(
        "//input[@id='id_username']"
    )
    username_input.clear()
    username_input.send_keys(username)

    password_input = browser.find_element_by_xpath(
        "//input[@id='id_password']"
    )
    password_input.clear()
    password_input.send_keys(password)

    submit_button = browser.find_element_by_xpath(
        "//button[@id='submit-btn']"
    ).click()

    assert browser.current_url.endswith("saltise/lobby/")

    browser.find_element_by_xpath("//a[contains(.,'My dashboard')]").click()

    assert browser.current_url.endswith("teacher/dashboard/")


def logout(browser):
    browser.find_element(By.XPATH, "//i[contains(text(), 'menu')]").click()

    WebDriverWait(browser, MAX_WAIT).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//i[contains(text(), 'logout')]")
        )
    ).click()

    assert browser.current_url == f"{browser.server_url}/en/login/"
