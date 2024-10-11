import re
import logging
import pytest
from playwright.async_api import Browser
from playwright.sync_api import Page
from datetime import datetime
from utilities.generate_fake_user import (
    generate_random_phone_number,
)

# setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# setting up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class TestScreenshortAndRecording:
    @pytest.fixture(autouse=True)
    def __setup(self, page: Page, browser: Browser):
        self.page = page
        self.browser = browser
        self.screenshot_path = "inputs_outputs/screenshorts"
        self.video_path = "inputs_outputs/screen_recordings"
        self.traced_object_path = "inputs_outputs/traced_object"

    def create_path_and_name_for_new_file(self, base_path, file_type):
        self.random_no = generate_random_phone_number()
        self.time_now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        new_generated_path = f"{base_path}/{self.random_no}_{self.time_now}{file_type}"
        return new_generated_path

    def test_take_snapshot_instagram(self):
        self.page.goto("https://www.instagram.com")
        self.page.pause()

        # Take first screenshot
        self.page.locator("text=Forgot password?").click()
        self.page.wait_for_url("https://www.instagram.com/accounts/password/reset/")
        self.page.screenshot(
            path=self.create_path_and_name_for_new_file(
                base_path=self.screenshot_path, file_type=".png"
            )
        )

        # Take second screenshot
        self.page.locator("text=Create New Account").click()
        self.page.wait_for_url("https://www.instagram.com/accounts/emailsignup/")
        self.page.locator('[aria-label="Mobile Number or Email"]').click()
        self.page.screenshot(
            path=self.create_path_and_name_for_new_file(
                base_path=self.screenshot_path, file_type=".png"
            )
        )

        # Take third screenshot
        self.page.locator('[aria-label="Mobile Number or Email"]').fill(
            "playwright@gmail.com"
        )
        self.page.locator('[aria-label="Full Name"]').click()
        self.page.locator('[aria-label="Full Name"]').fill("Play")
        self.page.locator('[aria-label="Full Name"]').press("Tab")
        self.page.locator('[aria-label="Username"]').fill("wright3536462")
        self.page.locator('[aria-label="Password"]').click()
        self.page.locator('[aria-label="Password"]').fill("wright1234")
        self.page.screenshot(
            path=self.create_path_and_name_for_new_file(
                base_path=self.screenshot_path, file_type=".png"
            )
        )

        # Proceed with the rest of the test
        self.page.locator('button:has-text("Sign up")').click()
        self.page.close()

    def test_record_video_facebook(self):
        """This test records the registration process on Facebook."""

        # Create a new browser context with video recording enabled
        logger.info("Creating a new browser context with video recording.")
        context = self.browser.new_context(
            record_video_dir=self.video_path,  # Path to save the video
            record_video_size={
                "width": 1920,
                "height": 1080,
            },  # Set the video resolution
        )
        # Open a new page
        logger.info("Opening a new page for Facebook registration.")
        page = context.new_page()
        # Navigate to the Facebook registration page
        logger.info("Navigating to 'https://www.facebook.com/register'.")
        page.goto("https://www.facebook.com/register")
        # Filling out the Facebook registration form
        logger.info("Filling out the registration form with user details.")
        # Enter first name
        page.get_by_label("First name").click()
        page.get_by_label("First name").fill("shashwat")
        logger.info("Filled 'First name' with 'shashwat'.")
        # Enter surname
        page.get_by_label("Surname").click()
        page.get_by_label("Surname").fill("jian")
        logger.info("Filled 'Surname' with 'jian'.")
        # Select date of birth (Day: 3, Month: May, Year: 1997)
        page.get_by_label("Day").select_option("3")
        logger.info("Selected 'Day' as '3'.")
        page.get_by_label("Month").select_option("5")
        logger.info("Selected 'Month' as 'May'.")
        page.get_by_label("Year").select_option("1997")
        logger.info("Selected 'Year' as '1997'.")
        # Select gender as Male
        page.get_by_label("Male", exact=True).check()
        logger.info("Selected 'Male' as gender.")
        # Enter mobile number or email address
        page.get_by_label("Mobile number or email address").click()
        page.get_by_label("Mobile number or email address").fill(
            "shashwat.jain@gmail.com"
        )
        logger.info(
            "Filled 'Mobile number or email address' with 'shashwat.jain@gmail.com'."
        )
        # Enter password
        page.get_by_label("New password").click()
        page.get_by_label("New password").fill("Shashwat@123")
        logger.info("Filled 'New password'.")
        # Click the 'Sign Up' button
        logger.info("Clicking the 'Sign Up' button.")
        page.locator("#reg_form_box div").filter(
            has_text=re.compile(r"^Sign Up$")
        ).click()
        # Close the page and stop video recording
        logger.info("Closing the page and stopping the video recording.")
        page.close()
        # Optionally, you can retrieve the video file path if needed
        video_path = page.video.path()
        logger.info(f"Video recording saved at: {video_path}")

        # Cleanup: Close the context to stop the video recording
        context.close()

    def test_tracing_facebook(self):
        """TO view the trace use 'playwright show-trace {file_path}' on terminal"""
        # Create a new browser context
        context = self.browser.new_context()
        # Start tracing with snapshots and sources enabled
        logger.info("Starting trace for the Facebook registration page.")
        context.tracing.start(snapshots=True, sources=True)
        # Open a new page and navigate to the Facebook registration page
        page = context.new_page()
        logger.info("Navigating to the Facebook registration page.")
        page.goto("https://www.facebook.com/register")
        # Fill the registration form with required details
        logger.info("Filling the registration form.")
        # Enter first name
        page.get_by_label("First name").click()
        page.get_by_label("First name").fill("shashwat")
        logger.info("Filled 'First name' with 'shashwat'.")
        # Enter surname
        page.get_by_label("Surname").click()
        page.get_by_label("Surname").fill("jian")
        logger.info("Filled 'Surname' with 'jian'.")
        # Select the date of birth (Day: 3, Month: May, Year: 1997)
        page.get_by_label("Day").select_option("3")
        logger.info("Selected 'Day' as '3'.")
        page.get_by_label("Month").select_option("5")
        logger.info("Selected 'Month' as 'May'.")
        page.get_by_label("Year").select_option("1997")
        logger.info("Selected 'Year' as '1997'.")
        # Select gender as Male
        page.get_by_label("Male", exact=True).check()
        logger.info("Selected 'Male' as gender.")
        # Enter email address
        page.get_by_label("Mobile number or email address").click()
        page.get_by_label("Mobile number or email address").fill(
            "shashwat.jain@gmail.com"
        )
        logger.info(
            "Filled 'Mobile number or email address' with 'shashwat.jain@gmail.com'."
        )
        # Enter password
        page.get_by_label("New password").click()
        page.get_by_label("New password").fill("Shashwat@123")
        logger.info("Filled 'New password'.")
        # Click the Sign Up button
        logger.info("Clicking the 'Sign Up' button.")
        page.locator("#reg_form_box div").filter(
            has_text=re.compile(r"^Sign Up$")
        ).click()

        # Stop tracing and save the trace file
        trace_file_path = self.create_path_and_name_for_new_file(
            base_path=self.traced_object_path, file_type=".zip"
        )
        context.tracing.stop(path=trace_file_path)
        logger.info(f"Stopped tracing and saved trace file at: {trace_file_path}")
