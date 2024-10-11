import pytest
import unittest
import logging

from jinja2.runtime import Context
from playwright.sync_api import Page

# setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestMultiplePages(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __setup(self, page: Page, context: Context):
        self.page = page
        self.context = context

    def test_page(self):
        # Navigating to Google's homepage
        self.page.goto("http://google.com")
        # Clicking on the search bar
        logger.info("Clicking on the search bar using aria-label locator")
        self.page.locator('[aria-label="Search"]').click()
        # Filling the search bar with "Python"
        logger.info("Filling the search bar with the query 'Python'")
        self.page.locator('[aria-label="Search"]').fill("Python")
        # Clicking on the first search result
        logger.info("Clicking on the first search result")
        self.page.locator('xpath=//*[@id="Alh6id"]/div[1]').first.click()
        # Logging the current URL after navigation
        logger.info(f"Current URL: {self.page.url}")
        # Waiting for 3 seconds to simulate loading time
        self.page.wait_for_timeout(3000)
        # Closing the page
        logger.info("Closing the page")
        self.page.close()

    def test_page2(self):
        # Opening two new pages in the same context
        page = self.context.new_page()
        page1 = self.context.new_page()
        # Navigating both pages to Google's homepage
        logger.info("Navigating to Google's homepage on both pages")
        page.goto("http://google.com")
        page1.goto("http://google.com")
        # Interacting with the search bar on the second page (page1)
        logger.info("Clicking on the search bar on page1 and filling it with 'Python'")
        page1.locator('[aria-label="Search"]').click()
        page1.locator('[aria-label="Search"]').fill("Python")
        # Clicking the first result on page1
        logger.info("Clicking on the first search result on page1")
        page1.locator('xpath=//*[@id="Alh6id"]/div[1]').first.click()
        # Waiting for 3 seconds to simulate loading time
        self.page.wait_for_timeout(3000)
        # Closing the first page
        logger.info("Closing page1")
        self.page.close()

    def test_working_with_popup(self):
        # Opening a new page and navigating to the popup test site
        page = self.context.new_page()
        logger.info("Navigating to the Texas GIS Popup Blocker Test site")
        page.goto(
            "https://www.rrc.texas.gov/resource-center/"
            "research/gis-viewer/gis-popup-blocker-test/#"
        )
        # Expecting a popup window to appear after clicking the button
        logger.info("Expecting a popup after clicking the 'RUN POPUP TEST' button")
        with page.expect_popup() as popup_info:
            page.locator("text=RUN POPUP TEST").click()
        # Storing the popup page object
        page1 = popup_info.value
        # Waiting for the original page to load the correct URL
        logger.info("Waiting for the URL to match the expected URL after popup")
        page.wait_for_url(
            "https://www.rrc.texas.gov/resource-center/"
            "research/gis-viewer/gis-popup-blocker-test/#"
        )
        # Closing the popup page
        logger.info("Closing the popup page")
        page1.close()
        # Logging the final URL of the main page
        logger.info(f"Final URL of the main page: {page.url}")
