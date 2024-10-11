import os
import asyncio
from playwright.async_api import async_playwright
from insta_buddy.utilities.support_func import login

insta_user = os.environ.get("INSTA_USER")
insta_password = os.environ.get("INSTA_PASSWORD")


async def search_user_and_like_all_pics(userid: str, number_to_like: int):
    async with async_playwright():
        browser, page = await login()
        await page.get_by_placeholder("Search").fill(userid)
        # Scroll through and like photos
        for i in range(number_to_like):
            # Click on a post
            await page.locator("article div img").nth(i).click()
            await page.wait_for_selector(
                'svg[aria-label="Like"]'
            )  # Wait for the like button
            await page.locator(
                'svg[aria-label="Like"]'
            ).click()  # Click the like button

            # Close the photo modal
            await page.locator('svg[aria-label="Close"]').click()


asyncio.run(search_user_and_like_all_pics(userid="vanessac_69", number_to_like=10))
