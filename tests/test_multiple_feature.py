import os
import pytest
import unittest
import logging
from datetime import date
from dotenv import load_dotenv
from playwright.sync_api import Page, expect

# Load environment variables from the .env file
load_dotenv()
# setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestFeature(unittest.TestCase):
    # Retrieve username and password from environment variables
    username = os.getenv("DEMO_USERNAME")
    password = os.getenv("DEMO_PASSWORD")

    @pytest.fixture(autouse=True)
    def __setup(self, page: Page):
        self.page = page
        self.filename = "sample_images/anger.jpg"

    # # @pytest.mark.skip
    def test_login_and_assert_login(self):
        # Navigate to the page
        self.page.goto("https://practice.expandtesting.com/")
        self.page.get_by_role("link", name="Test Login Page").click()

        # Fill in login form
        self.page.get_by_label("Username").fill(self.username)
        self.page.get_by_label("Password").fill(self.password)
        self.page.get_by_role("button", name="Login").click()

        logger.info("Use Playwright's `expect` for assertions")
        expect(self.page.get_by_text("You logged into a secure area!")).to_be_visible()
        expect(self.page.get_by_role("link", name="Logout")).to_be_visible()

    # @pytest.mark.skip
    def test_logout_and_assert_logout(self):
        # First, call the login test to ensure the user is logged in before attempting to log out
        self.test_login_and_assert_login()
        # Click on the flash message element interact with it
        self.page.locator("#flash").click()
        # Click the Logout link to log the user out
        self.page.get_by_role("link", name="Logout").click()
        logger.info("Assert that the flash message indicating logout is visible")
        expect(self.page.locator("#flash")).to_be_visible()
        logger.info("Assert that the logout confirmation text is visible")
        expect(self.page.get_by_text("You logged out of the secure")).to_be_visible()
        logger.info(
            "Assert that the flash message contains the expected text confirming logout"
        )
        expect(self.page.locator("#flash")).to_contain_text(
            "You logged out of the secure area!"
        )

    # @pytest.mark.skip
    def test_input_type_element(self):
        # Navigate to the practice testing website
        self.page.goto("https://practice.expandtesting.com/")
        # Click on the link to access the "Web inputs" section
        self.page.get_by_role("link", name="Web inputs").click()

        # Define input values for different input types
        input_number = "123"  # Input for number field
        input_text = "abc"  # Input for text field
        input_password = "123abc"  # Input for password field
        # Format today's date to fill in the date input field
        today_date = f"{date.today()}"
        # Interact with the number input field: click and fill it with a number
        self.page.get_by_label("Input: Number").click()
        self.page.get_by_label("Input: Number").fill(input_number)
        # Interact with the text input field: click and fill it with text
        self.page.get_by_label("Input: Text").click()
        self.page.get_by_label("Input: Text").fill(input_text)
        # Interact with the password input field: click and fill it with a password
        self.page.get_by_label("Input: Password").click()
        self.page.get_by_label("Input: Password").fill(input_password)
        # Fill in the date input field with today's date
        self.page.get_by_label("Input: Date").fill(today_date)
        # Click on the button to display the inputs entered
        self.page.get_by_role("button", name="Display Inputs").click()
        # Retrieve the output values displayed on the page after submission
        output_number = self.page.locator(".output-box#output-number").text_content()
        output_text = self.page.locator(".output-box#output-text").text_content()
        logger.info("Verify that the input number is visible on the page")
        expect(self.page.get_by_text(input_number, exact=True)).to_be_visible()
        logger.info("Assert that the output matches the inputs provided")
        assert input_number == output_number
        assert input_text == output_text

    # @pytest.mark.skip
    def test_dynamic_table(self):
        # Navigate to the page containing the table
        self.page.goto(
            "https://practice.expandtesting.com/dynamic-table"
        )  # Replace with your page URL
        # Locate the row containing "Chrome"
        chrome_row = self.page.locator("tbody tr", has_text="Chrome")
        # Extract data from the Chrome row
        entry1 = chrome_row.locator("td:nth-child(2)").text_content()  # Memory column
        entry2 = chrome_row.locator("td:nth-child(3)").text_content()  # Disk column
        entry3 = chrome_row.locator("td:nth-child(4)").text_content()  # CPU column
        entry4 = chrome_row.locator("td:nth-child(5)").text_content()  # Network column
        list_of_entry = [entry1, entry2, entry3, entry4]
        chrome_cpu_element = self.page.locator(
            "p#chrome-cpu.bg-warning.p-1"
        ).text_content()
        for i in list_of_entry:
            if "%" in i:
                cpu_from_table = i
                assert cpu_from_table == chrome_cpu_element.split(":")[-1].strip()

    # @pytest.mark.skip
    def test_radio_buttons(self):
        # Navigate to the radio buttons page
        self.page.goto("https://practice.expandtesting.com/radio-buttons")
        # Wait for the "Red" radio button to be visible before checking it
        self.page.wait_for_selector('label[for="red"]')
        # Check the "Red" radio button
        self.page.get_by_label("Red").check()
        logger.info("Assert that the 'Red' radio button is checked")
        assert self.page.get_by_label("Red").is_checked()
        logger.info("Assert that the 'Blue' radio button is not checked")
        assert not self.page.get_by_label("Blue").is_checked()
        # Locate the "Football" radio button using XPath and check it
        football_locator = self.page.locator(
            "xpath=/html/body/main/div[2]/div/div[2]/div[2]/div/div[2]/div/div/div[2]/label"
        )
        football_locator.check()
        logger.info("Assert that the 'Football' radio button is checked")
        assert football_locator.is_checked()
        ### OR ###
        # expect(self.page.get_by_label("Football")).to_be_checked()

    # @pytest.mark.skip
    def test_drag_and_drop(self):
        # Navigate to the drag-and-drop page
        self.page.goto("https://practice.expandtesting.com/drag-and-drop")
        self.page.wait_for_timeout(200)
        logger.info("Assert that column-a initially contains the text 'A'")
        assert self.page.locator("#column-a").text_content().strip() == "A"
        logger.info("Locate column-a and drag it to column-b")
        self.page.locator("#column-a").drag_to(self.page.locator("#column-b"))
        logger.info(
            "Assert that after the drag, column-a now contains the text 'B', confirming the drop was successful"
        )
        assert self.page.locator("#column-a").text_content().strip() == "B"

    def test_working_with_dropdowns_list(self):
        # Navigate to the main page
        self.page.goto("https://practice.expandtesting.com/")
        # Click on the "Dropdown List" link to navigate to the dropdown page
        self.page.get_by_role("link", name="Dropdown List").click()
        # Select the option with value "2" from the dropdown (assuming "2" corresponds to the desired option)
        self.page.locator("#dropdown").select_option("2")
        # Click on the heading "Simple dropdown" (if required, or to bring it into view)
        self.page.get_by_role("heading", name="Simple dropdown").click()
        # Again select the option with value "2" from the dropdown (if needed)
        self.page.locator("#dropdown").select_option("2")
        # Select "50" as the number of elements per page from the "Elements per Page" dropdown
        self.page.get_by_label("Elements per Page:").select_option("50")
        logger.info(
            "Click on the heading 'Country selection' to bring it into view or interact with it"
        )
        self.page.get_by_role("heading", name="Country selection").click()
        logger.info(
            "Select the country with the code 'IS' (Iceland) from the country dropdown"
        )
        self.page.locator("#country").select_option("IS")
