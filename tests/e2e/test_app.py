import os
import re
from dotenv import load_dotenv
from playwright.sync_api import Playwright, expect, Browser


load_dotenv()

BASE_URL = os.getenv('SERVICE_E2E_URL')


def open_close_browsers(func):
    def inner(playwright: Playwright):
        chrome_browser = playwright.chromium.launch(
            headless=True)
        func(chrome_browser)
        chrome_browser.close()
    return inner


@open_close_browsers
def test_quizz(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/quizz")
    expect(page).to_have_url(re.compile(f"{BASE_URL}/quizz"))

    
@open_close_browsers
def test_return_to_main_menu_from_quick_quizz(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/quizz")
    page.locator("#return-to-main-menu").click()
    expect(page).to_have_url(re.compile(f"{BASE_URL}"))


@open_close_browsers
def test_return_to_main_menu_from_game(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/start")
    page.locator("#return-to-main-menu").click()
    expect(page).to_have_url(re.compile(f"{BASE_URL}"))


@open_close_browsers
def test_return_to_main_menu_from_result_page(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/quizz")
    page.locator("div.movies form:first-of-type button").click()
    expect(page).to_have_url(re.compile(f"{BASE_URL}/quizz/.*/verify"))
    page.locator("#return-to-main-menu").click()
    expect(page).to_have_url(re.compile(f"{BASE_URL}"))
