import asyncio
import random
import time

from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def randomize_sleep(min_seconds=1.0, max_seconds=2.0):
    """Asynchronously sleeps for a random float duration between min_seconds and max_seconds."""
    duration = random.uniform(min_seconds, max_seconds)
    await asyncio.sleep(duration)
    return duration

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-infobars",
                "--window-position=0,0",
                "--ignore-certificate-errors",
                "--ignore-certificate-errors-spki-list",
            ],
        )

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            device_scale_factor=1,
            locale="en-US",
            timezone_id="Asia/Hong_Kong",
            permissions=["geolocation"],
            geolocation={"latitude": 22.3193, "longitude": 114.1694},
        )

        page = await context.new_page()

        # Apply stealth directly using the Stealth instance
        stealth = Stealth()
        await stealth.apply_stealth_async(page)

        print("Navigating to Apple Hong Kong iPhone Store...")

        response = await page.goto(
            "https://www.apple.com/hk/shop/buy-iphone",
            wait_until="domcontentloaded",
            timeout=60000,
        )

        print(f"Page loaded with status code: {response.status if response else 'N/A'}")
        print(f"Page Title: {await page.title()}")

        await asyncio.sleep(randomize_sleep)

        # xpath to buy button
        buy_btn_xpath = "//a[@data-autom='IPHONE18PRO_MAIN']"
        # click the button
        await page.click(buy_btn_xpath)

        await asyncio.sleep(randomize_sleep)

        # XPath targeting the label for the 6.3-inch model
        phone_label_xpath = "//label[@for=//input[@data-autom='dimensionScreensize6_3inch']/@id]"
        await page.click(f"xpath={phone_label_xpath}")

        await asyncio.sleep(randomize_sleep)

        # xpath to phone color.
        color_xpath = "(//ul[contains(@class, 'colornav-items')]/li[contains(@class, 'colornav-item')])[2]//label"
        await page.click(color_xpath)

        await asyncio.sleep(randomize_sleep)

        # storage selector xpath
        storage_xpath = "//label[@for=//input[@data-autom='dimensionCapacity256gb']/@id]"
        await page.click(storage_xpath)

        await asyncio.sleep(randomize_sleep)

        # Trade-in xpath
        no_tradein_label = "//label[@for='noTradeIn']"
        # Wait for element to be visible/attached
        await page.wait_for_selector(f"xpath={no_tradein_label}", state="visible", timeout=5000)

        await asyncio.sleep(randomize_sleep)

        # Click with force=True
        await page.locator(f"xpath={no_tradein_label}").click(force=True)

        await asyncio.sleep(randomize_sleep)

        # apple coverage xpath
        # Wait until the input is no longer disabled
        # Wait until the input is enabled
        await page.wait_for_selector("input[data-autom='acp']:not([disabled])", state="attached", timeout=5000)

        await asyncio.sleep(randomize_sleep)

        # Target and click the parent label wrapper
        acp_wrapper = page.locator("div.rf-applecare-option:has(input[data-autom='acp']) .rf-applecare-label")
        await acp_wrapper.click(force=True)

        await asyncio.sleep(randomize_sleep)

        # add coverage_btn xpath
        add_button = page.locator("button[data-autom='inlineapplecare_overlay_add']")
        await add_button.wait_for(state="visible", timeout=5000)
        await add_button.click()

        await asyncio.sleep(randomize_sleep)

        # add_to_bag xpath
        # Wait for the button to be fully visible and enabled, then click
        add_to_bag_btn = page.locator("button[data-autom='add-to-cart']")
        await add_to_bag_btn.wait_for(state="visible", timeout=5000)
        await add_to_bag_btn.click()

        await asyncio.sleep(randomize_sleep)

        # Review Bag xpath
        # Wait for the button to be visible and click it
        # Submit the form directly via JavaScript
        # Trigger Apple's JS click handler directly in the browser
        await page.locator("button[data-autom='proceed']").evaluate("el => el.click()")

        await asyncio.sleep(randomize_sleep)

        # click check_out button
        await page.click('#shoppingCart\\.actions\\.navCheckoutOtherPayments');

        await asyncio.sleep(randomize_sleep)

        # continue as guest btn
        await page.locator("button[data-autom='guest-checkout-btn']").click()


        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())