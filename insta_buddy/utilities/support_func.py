import os
from playwright.async_api import async_playwright

insta_user = os.environ.get("INSTA_USER")
insta_password = os.environ.get("INSTA_PASSWORD")


async def login():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False, slow_mo=2000)
        page = await browser.new_page()
        await page.goto("https://www.instagram.com/")
        await page.get_by_label("Phone number, username, or").fill(insta_user)
        await page.get_by_label("Password").fill("Shashwat@123")
        await page.get_by_label("Password").fill(insta_password)
        await page.get_by_role("button", name="Log in", exact=True).click()
        # Wait for the user profile to load
        await page.wait_for_load_state("networkidle")

        return browser, page


# asyncio.run(login())
