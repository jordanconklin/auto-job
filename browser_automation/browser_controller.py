from playwright.sync_api import sync_playwright, TimeoutError
import time
import os

class BrowserController:
    def __init__(self):
        # Initialize playwright with proper environment
        os.environ['PLAYWRIGHT_BROWSERS_PATH'] = '0'  # Force browser download in the project directory
        
        self.playwright = sync_playwright().start()
        # Launch browser with additional options for better compatibility
        self.browser = self.playwright.chromium.launch(
            headless=False,  # Show the browser
            args=[
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu'
            ]
        )
        self.context = self.browser.new_context()

    def new_page(self):
        return self.context.new_page()

    def start_browser(self):
        if not self.browser:
            self.browser = self.playwright.chromium.launch(headless=False)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
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
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()