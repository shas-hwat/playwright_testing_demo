import pytest
from typing import Dict
from datetime import datetime
from playwright.sync_api import BrowserType, Playwright, APIRequestContext
from typing import Generator


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "ignore_https_errors": True}


@pytest.fixture(scope="session")
def browser_context_size(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1920,
            "height": 1080,
        },
    }


@pytest.fixture(scope="function")
def browser_context_mobile_iphone_14(playwright, browser_type_launch_args):
    # Get the device settings for iPhone 14 Pro
    iphone_14 = playwright.devices["iPhone 14 Pro"]
    # Launch a new browser with mobile emulation for iPhone 14 Pro
    browser = playwright.chromium.launch(**browser_type_launch_args)
    # Create a new context with the iPhone 14 Pro settings
    context = browser.new_context(**iphone_14)
    yield context
    context.close()


@pytest.fixture(scope="function")
def context_for_hindi_language(
    browser_type: BrowserType,
    browser_type_launch_args: Dict,
    browser_context_args: Dict,
):
    context = browser_type.launch_persistent_context(
        "./browser_hindi",
        **{
            **browser_type_launch_args,
            **browser_context_args,
            "locale": "hi-IN",
        },
    )
    yield context
    context.close()


def pytest_configure(config):
    # Get the current timestamp in the desired format
    report_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Construct the report filename with the timestamp
    report_filename = f"report_{report_time}.html"
    # Set the report path dynamically
    config.option.htmlpath = f"logs/{report_filename}"


@pytest.fixture(scope="session")
def api_request_context(
    playwright: Playwright,
) -> Generator[APIRequestContext, None, None]:
    # Create a new APIRequestContext with the base URL
    request_context = playwright.request.new_context()
    yield request_context  # Yield it for use in tests
    request_context.dispose()  # Ensure it's disposed of after the tests
