import pytest
import logging
import random

# setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestCustomFixture:
    @pytest.fixture(autouse=True)
    def __setup(self, context_for_hindi_language):
        # Initialize the page from the Hindi language context
        self.page = context_for_hindi_language.new_page()

    # @pytest.mark.skip
    def test_using_hindi_lan_browser_context(self, context_for_hindi_language):
        all_videos_title = []
        # Navigate to the page
        self.page.goto("https://youtube.com/")
        # self.page.pause()
        self.page.wait_for_timeout(2000)  # Wait for 2 seconds to inspect
        self.page.get_by_role("button", name="खोजें", exact=True).click()
        self.page.get_by_placeholder("खोजें").fill("wheels on the bus")
        self.page.get_by_placeholder("खोजें").press("Enter")
        self.page.wait_for_timeout(2000)
        # Get all video titles from the page
        video_titles = self.page.locator('//a[@id="video-title"]')
        # Loop through the titles and print them
        for i in range(video_titles.count()):
            title = video_titles.nth(i).get_attribute(
                "title"
            )  # Extract the title attribute
            all_videos_title.append(title)
        # open and play random video
        self.page.get_by_role("link", name=f"{random.choice(all_videos_title)}").click()
        self.page.wait_for_timeout(20000)  # Wait for 2 seconds to inspect


class TestCustomFixture2:
    @pytest.fixture(autouse=True)
    def __setup(self, browser_context_mobile_iphone_14):
        # Create a page within the iPhone 14 mobile emulation context
        self.page = browser_context_mobile_iphone_14.new_page()

    @pytest.mark.skip
    def test_for_mobile_support(self):
        # Navigate to YouTube on a mobile device emulated as iPhone 14 Pro
        links_for_videos = []
        links_for_shorts = []
        self.page.goto("https://youtube.com/")
        self.page.wait_for_timeout(2000)  # Wait for 2 seconds to inspect
        self.page.locator("#header-bar").get_by_label("Search YouTube").click()
        self.page.get_by_placeholder("Search").fill("baby shark")
        self.page.get_by_placeholder("Search").press("Enter")
        self.page.wait_for_timeout(2000)
        # Locate all the <a> elements
        a_tags = self.page.locator("a")
        count = a_tags.count()
        for i in range(count):
            # self.page.wait_for_selector('#thumbnail')
            href = a_tags.nth(i)
            href_links = href.get_attribute("href")
            if "/watch" in href_links:
                links_for_videos.append(href_links)
                print(href_links)
            elif "/shorts" in href_links:
                links_for_shorts.append(href_links)
        logger.info("Got all links from the page")
