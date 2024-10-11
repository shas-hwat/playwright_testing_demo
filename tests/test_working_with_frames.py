from playwright.sync_api import Page
import logging
import pytest

# setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestFrames:
    @pytest.fixture(autouse=True)
    def __setup(self, page: Page):
        self.page = page

    def test_frame(self):
        # Navigate to the page containing the iframe
        logger.info("Navigating to the page with the iframe")
        self.page.goto("https://practice.expandtesting.com/iframe")
        # Locate the iframe by XPath and click inside the content area
        logger.info(
            "Locating the iframe and clicking on the content area inside the iframe"
        )
        self.page.frame_locator("xpath=//*[@id='mce_0_ifr']").locator(
            "xpath=//*[@id='tinymce']"
        ).click()
        # Fill the content area inside the iframe with a message
        logger.info(
            "Filling the content area inside the iframe with text: 'My favorite tool is Playwright'"
        )
        self.page.frame_locator("xpath=//*[@id='mce_0_ifr']").locator(
            "xpath=//*[@id='tinymce']"
        ).fill("My favorite tool is Playwright")
        # Wait for 60 seconds to observe the changes (useful for manual testing/verification)
        logger.info("Waiting for 6 seconds to observe changes")
        self.page.wait_for_timeout(6000)
        self.page.close()
