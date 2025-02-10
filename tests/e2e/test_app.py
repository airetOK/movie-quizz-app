import os
import re
from dotenv import load_dotenv
from playwright.sync_api import Playwright, Page, expect, Browser


load_dotenv()

BASE_URL = os.getenv('SERVICE_URL')


def open_close_browsers(func):
    def inner(playwright: Playwright):
        chrome_browser = playwright.chromium.launch(
            headless=False,
            slow_mo=1000)
        func(chrome_browser)
        chrome_browser.close()
    return inner


@open_close_browsers
def test_quizz(browser: Browser):
    context = browser.new_context()
    page = context.new_page()
    page.goto(f"{BASE_URL}/quizz")
    expect(page).to_have_url(re.compile(f"{BASE_URL}/quizz"))
