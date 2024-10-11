import pytest
import unittest
import logging
from playwright.sync_api import Page, expect

# setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestUploadAndDownload(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def __setup(self, page: Page):
        self.page = page
        self.filename = "inputs_outputs/sample_images/anger.jpg"

    def test_upload_a_file(
        self, filename: str = "inputs_outputs/sample_images/anger.jpg"
    ):
        """this function is using set_input_files method"""

        # Navigate to the file upload page
        self.page.goto("https://practice.expandtesting.com/upload")
        # Wait for 200 milliseconds before interacting with the page
        self.page.wait_for_timeout(200)
        # Locate the file input element using XPath and set the file to upload
        input_locator = self.page.locator(
            '//input[@class="form-control" and @id="fileInput"]'
        )
        input_locator.set_input_files(filename)  # Directly upload the file
        # Submit the form by clicking the submit button
        self.page.get_by_test_id("file-submit").click()
        logger.info("Assert that the uploaded file name is displayed correctly")
        assert "anger.jpg" in self.page.locator("#uploaded-files").text_content()
        # Click the "File Uploaded!" heading (if required, otherwise this can be optional)
        self.page.get_by_role("heading", name="File Uploaded!").click()
        logger.info(
            "Verify that the 'File Uploaded!' heading is visible after successful upload"
        )
        expect(self.page.get_by_role("heading", name="File Uploaded!")).to_be_visible()
        # Optionally, wait to visually confirm the result (during development/testing)
        self.page.wait_for_timeout(2000)

    def test_upload_a_file_by_event_listener(self):
        """this function is using event listener to upload a file"""

        # Navigate to the file upload page
        self.page.goto("https://practice.expandtesting.com/upload")
        # Wait for 200 milliseconds before proceeding
        self.page.wait_for_timeout(200)
        # Locate the file input element using XPath
        input_locator = self.page.locator(
            '//input[@class="form-control" and @id="fileInput"]'
        )
        # Set up the file chooser event listener to handle file upload
        self.page.on(
            "filechooser", lambda file_chooser: file_chooser.set_files(self.filename)
        )
        # Simulate a click on the file input element to trigger the file chooser
        input_locator.click()
        # Submit the form by clicking the submit button (assuming there's a data-testid on the button)
        self.page.get_by_test_id("file-submit").click()
        logger.info("Assert that the uploaded file name is displayed correctly")
        assert "anger.jpg" in self.page.locator("#uploaded-files").text_content()
        logger.info(
            "Assert that the 'File Uploaded!' heading is visible after successful upload"
        )
        assert self.page.get_by_role("heading", name="File Uploaded!").is_visible()
        # Optionally, wait for a short duration to visually see the result (if needed)
        self.page.wait_for_timeout(2000)

    def test_download(self):
        self.page.goto("https://www.jetbrains.com/pycharm/download/#section=windows")
        if self.page.get_by_role("button", name="Accept All"):
            self.page.get_by_role("button", name="Accept All").click()
        with self.page.expect_download() as download_info:
            self.page.locator(
                "xpath=//*[@id='download-block']/section[2]/div/div/div[1]/div[2]/div[1]/div/div/div/span/a"
            ).click()
        download = download_info.value
        logger.info(download.path())
        download.save_as("inputs_outputs/download_folder/jetbrains_path.txt")
