import asyncio
import json
from random import randint, choice
from password_generator import generate_password
from playwright.async_api import async_playwright


# This method get random name and surname for registration
# And returns randomly received data from data.json file
def get_random_data() -> list:
    file = open('data.json')
    data = json.load(file)
    file.close()
    return [
        choice(data['names']),
        choice(data['surnames'])
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
            # Create account
            await page.get_by_role("button", name="Создать аккаунт").click()
            await page.locator("text=Для личного использования").click()
            await asyncio.sleep(2)
            # Enter account data
            await page.locator('input[id="firstName"]').fill(data[0])
            await page.locator('input[id="lastName"]').fill(data[1])
            await page.get_by_role("button", name="Далее").click()
            await asyncio.sleep(5)
            # Set BD date
            BDay = [str(randint(1, 25)), str(randint(1, 12)), str(randint(1990, 2000))]
            await page.locator('input[id="day"]').fill(BDay[0])
            await page.select_option('select#month', value=BDay[1])
            await page.locator('input[id="year"]').fill(BDay[2])
            await page.select_option('select#gender', value='3')
            await page.locator('text=Далее').click()
            await asyncio.sleep(2)
            # Choosing the address
            email = (data[0]+data[1]+BDay[0]+BDay[1])[::-1]
            if (await page.text_content('h1#headingText') == 'Выберите адрес Gmail'):
                print("here")
                await page.locator('text=Создать собственный адрес Gmail').click()
            await page.locator('input[name="Username"]').fill(email)
            email += '@gmail.com'
            await page.locator('text=Далее').click()
            await asyncio.sleep(2)
            # Create password
            new_password = generate_password()
            await page.locator('input[name="Passwd"]').fill(new_password)
            await page.locator('input[name="PasswdAgain"]').fill(new_password)
            await page.locator('text=Далее').click()
            # Here's a robot check...
            await asyncio.sleep(10)
            await browser.close()
    except:
        print("Something went wrong")


# Calling the main method
asyncio.run(main())
