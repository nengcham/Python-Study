from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Solution:
    def __init__(self):
        self.url = "https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com"

    @staticmethod
    def browser_test():
        chrome_options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        browser.get('https://www.naver.com')
        while (True):
            pass

    def auto_login(self):
        url = self.url
        chrome_options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        browser.implicitly_wait(10)
        browser.maximize_window()
        browser.get(url)
        while (True):
            pass


if __name__ == '__main__':
    Solution().browser_test()
