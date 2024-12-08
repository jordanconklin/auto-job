from playwright.sync_api import sync_playwright, TimeoutError
import time

class BrowserController:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None

    def start_browser(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        # Set default timeout
        self.page.set_default_timeout(10000)  # 10 seconds

    def navigate_to(self, url):
        try:
            print(f"\nNavigating to: {url}")
            self.page.goto(url)
            time.sleep(2)  # Allow page to load
            print(f"Current page URL: {self.page.url}")
            return self.page
        except Exception as e:
            print(f"Navigation error: {e}")
            return None

    def close(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()