import random
import asyncio
import os
from playwright.async_api import async_playwright
from insta_buddy.utilities.constants import list_of_emoji

insta_user = os.environ.get("INSTA_USER")
insta_password = os.environ.get("INSTA_PASSWORD")
storage_state_file = "session_state.json"


# Login function without closing the browser
async def login(playwright):
    # Start a new browser instance
    browser = await playwright.chromium.launch(headless=False)
    context = await browser.new_context(storage_state=storage_state_file)
    page = await context.new_page()
    page.pause()
    # Go to Instagram login page
    await page.goto("https://www.instagram.com/")

    if await page.is_visible("text=Log in"):
        print("Existing session Expired. Logging in...")
        await context.storage_state(storage_state_file)
        print("Loaded existing session.")

        # Fill in the login credentials
        await page.get_by_label("Phone number, username, or email").fill(insta_user)
        await page.get_by_label("Password").fill(insta_password)
        await page.get_by_role("button", name="Log in", exact=True).click()

        # Wait for the page to load after login
        await page.wait_for_load_state("networkidle")
        await page.page_sleep(300)
        await page.wait_for_page_load()
        # Save the storage state after logging in
        await context.storage_state(path=storage_state_file)

    else:
        pass

    # Handle potential notification prompts
    try:
        await page.wait_for_load_state("networkidle")
        element = page.get_by_text("Turn on Notifications")
        # element = page.locator('text=Turn on Notifications')
        # element = page.page.get_by_role("button", name="Not Now")
        if await element.is_visible():
            await element.click()
            await page.get_by_role("button", name="Not Now").click()
            await page.get_by_role("link", name="Home Home").click()

    except Exception as e:
        print(f"Error handling notifications: {e}")

    return browser, page


async def login2(playwright):
    """Log in to Instagram and save the session state."""
    browser = await playwright.chromium.launch(headless=False)
    # Create a new context with storage state if it exists

    context = await browser.new_context()
    # Check if we need to log in
    page = await context.new_page()
    await page.goto("https://www.instagram.com/")

    # Check if we are already logged in by looking for a specific element
    if await page.is_visible("text=Log in"):
        print("No existing session found. Logging in...")
        # Fill in the login credentials
        await page.get_by_label("Phone number, username, or email").fill(insta_user)
        await page.get_by_label("Password").fill(insta_password)
        await page.get_by_role("button", name="Log in", exact=True).click()

        # Wait for the page to load after login
        await page.wait_for_load_state("networkidle")

        # Handle potential notification prompts
        try:
            element = page.locator("text=Turn on Notifications")
            if await element.is_visible():
                await page.get_by_role("button", name="Not Now").click()
        except Exception as e:
            print(f"Error handling notifications: {e}")

        # Save the storage state after logging in
        await context.storage_state(path=storage_state_file)
    else:
        print("Session already exists.")

    return browser, context


async def search_user_and_like_visible_pics(userid: str):
    async with async_playwright() as playwright:
        browser, page = await login(playwright)
        await page.goto(f"https://www.instagram.com/{userid}/")
        await page.wait_for_selector('div[style*="display: flex"]')

        # Locate all the <img> elements
        all_images = page.locator("img")
        count = await all_images.count()
        print("Total images found:", count)

        for i in range(count):
            # for i in range(min(count, number_to_like)):
            await page.wait_for_selector('div[style*="display: flex"]')
            image = all_images.nth(i)
            alt_text = await image.get_attribute("alt")
            if alt_text and "profile" not in alt_text and "highlight" not in alt_text:
                print(f"Image number {i}: {alt_text}")
                # Click on the image to open it
                await image.click()
                await page.wait_for_timeout(1000)  # Wait for the image modal to load
                like_button = (
                    page.locator("section")
                    .filter(has_text="LikeCommentShare PostShare")
                    .get_by_role("button")
                    .first
                )
                # Click the like button (adjust selector as needed)
                await like_button.click()
                print(f"Liked image number {i}")
                # Close the image modal (adjust selector as needed)
                await page.get_by_role("button", name="Close").click()
                await asyncio.sleep(1)  # Wait a moment before proceeding

        await asyncio.sleep(10)  # Optional wait before closing
        await page.close()
        await browser.close()


async def search_user_and_leave_comment_on_first_three_pics(userid: str):
    breaker = 0
    async with async_playwright() as playwright:
        browser, page = await login(playwright)
        await page.goto(f"https://www.instagram.com/{userid}/")
        await page.wait_for_selector('div[style*="display: flex"]')
        # Locate all the <img> elements
        all_images = page.locator("img")
        count = await all_images.count()
        for i in range(count):
            await page.wait_for_selector('div[style*="display: flex"]')
            image = all_images.nth(i)
            alt_text = await image.get_attribute("alt")
            if alt_text and "profile" not in alt_text and "highlight" not in alt_text:
                # Click on the image to open it
                await page.get_by_role("link", name=f"{alt_text}").click()
                await page.wait_for_timeout(1000)  # Wait for the image modal to load
                # await page.get_by_role("button", name="Comment", exact=True).click()
                random_emoji_to_comment = random.choice(list_of_emoji)
                print(f"Commented on image {i} with {random_emoji_to_comment}")
                comment_box = page.get_by_role("textbox", name="Add a comment…")
                await comment_box.click()
                await comment_box.fill(f"{random_emoji_to_comment}")
                await comment_box.press("Enter")
                await page.get_by_role("button", name="Close").click()
                await asyncio.sleep(1)  # Wait a moment before proceeding
                breaker += 1
                if breaker == 3:
                    break
        await asyncio.sleep(10)  # Optional wait before closing
        await page.close()
        await browser.close()


# async def search_user_and_leave_comment_on_first_three_pics(userid: str):
#     async with async_playwright() as playwright:
#         browser, page = await login(playwright)
#         await page.goto(f"https://www.instagram.com/{userid}/")
#         await page.wait_for_selector('div[style*="display: flex"]')
#         # Locate all the <img> elements
#         all_images = page.locator('img')
#         count = await all_images.count()
#         for i in range(count):
#             await page.wait_for_selector('div[style*="display: flex"]')
#             image = all_images.nth(i)
#             alt_text = await image.get_attribute('alt')
#             if alt_text and "profile" not in alt_text and "highlight" not in alt_text:
#                 # Click on the image to open it
#                 await page.get_by_role("link", name=f"{alt_text}").click()
#                 await page.wait_for_timeout(1000)  # Wait for the image modal to load
#                 # await page.get_by_role("button", name="Comment", exact=True).click()
#                 random_emoji_to_comment = random.choice(list_of_emoji)
#                 print(f"Commented on image {i} with {random_emoji_to_comment}")
#                 comment_box = page.get_by_role("textbox", name="Add a comment…")
#                 await comment_box.click()
#                 await comment_box.fill(f"{random_emoji_to_comment}")
#                 await comment_box.press("Enter")
#                 await page.get_by_role("button", name="Close").click()
#                 await asyncio.sleep(1)  # Wait a moment before proceeding
#                 breaker += 1
#                 if breaker == 3:
#                     break
#         await asyncio.sleep(10)  # Optional wait before closing
#         await page.close()
#         await browser.close()


async def like_visible_feed():
    async with async_playwright() as playwright:
        browser, page = await login(playwright)
        await page.wait_for_load_state("networkidle")

        # Locate the main feed container
        feed_locator = page.locator(".xw7yly9 > div:nth-child(2)")

        # Locate all <article> elements within the main feed
        articles = feed_locator.locator("article")

        # Get count of articles found
        count = await articles.count()
        print(f"Total articles found: {count}")

        # Loop through each article and like it
        for i in range(count):
            article = articles.nth(i)
            # Click on the article to open it (if necessary)
            await article.click()
            await page.wait_for_timeout(1000)  # Wait for modal to load
            # Click the like button (adjust selector as needed)
            like_button = page.locator('svg[aria-label="Like"]')
            await like_button.click()
            print(f"Liked article {i + 1}")
            # Close the modal (adjust selector as needed)
            close_button = page.locator('button[aria-label="Close"]')
            await close_button.click()
            await asyncio.sleep(1)  # Wait a moment before proceeding
        await asyncio.sleep(10)  # Optional wait before closing
        await page.close()
        await browser.close()


async def upload_a_picture(file_path: str):
    async with async_playwright() as playwright:
        browser, page = await login(playwright)
        # Wait until the page has fully loaded
        await page.wait_for_load_state("networkidle")
        # Click on "New post Create" button
        await page.get_by_role("link", name="New post Create").click()
        # # Wait for the file input to appear
        # input_locator = page.locator('//input[@class="_ac69" and @type="file"]')
        # await input_locator.wait_for(state="visible", timeout=5000)  # Adjust the timeout if needed
        # # Upload the file
        # await input_locator.set_input_files(file_path)
        # await page.locator('input[accept="file"]._ac69').set_input_files(file_path)

        page.on("filechooser", lambda file_chooser: file_chooser.set_files(file_path))
        await page.click("button#upload")
        # Wait for some time to ensure the upload completes (adjust timeout if needed)
        await page.wait_for_timeout(10000)

        # Optionally, wait for any specific action post-upload if required
        await page.wait_for_load_state("load")


# Running the async function
if __name__ == "__main__":
    # asyncio.run(search_user_and_like_visible_pics(userid="vanessac_69"))
    # asyncio.run(like_visible_feed())
    asyncio.run(upload_a_picture(file_path="images/20240527_015250.jpg"))
