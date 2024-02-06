import asyncio
import time
import json
import random
from playwright.async_api import async_playwright


# This method get random name and surname for registration
# And returns randomly received data from data.json file
def get_random_data() -> list:
    file = open('data.json')
    data = json.load(file)
    file.close()
    return [
        data['names'][random.randint(0, len(data['names']) - 1)],
        data['surnames'][random.randint(0, len(data['surnames']) - 1)]
    ]


# Main method
async def main():
    try:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto("http://gmail.com")
            print("On Gmail.com")
            data = get_random_data()
            print(data)
            time.sleep(5)
            await browser.close()
            await playwright.stop()
    except:
        print("Something went wrong")


# Calling the main method
asyncio.run(main())
