from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from fake_useragent import UserAgent


class BrowserHelper:

    @staticmethod
    def get_options():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1920x1080")
        ua = UserAgent()
        userAgent = ua.random
        chrome_options.add_argument(f'user-agent={userAgent}')

    @staticmethod
    def get_browser():
        return webdriver.Chrome(chrome_options=BrowserHelper.get_options(), executable_path='./chromedriver')
