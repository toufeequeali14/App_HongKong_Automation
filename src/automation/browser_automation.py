import asyncio
import random
import time

from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def randomize_sleep(min_seconds=0.5, max_seconds=1.0):
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

        await asyncio.sleep(await randomize_sleep())

        # xpath to buy button
        buy_btn_xpath = "//a[@data-autom='IPHONE18PRO_MAIN']"
        # click the button
        await page.click(buy_btn_xpath)

        await asyncio.sleep(await randomize_sleep())

        # XPath targeting the label for the 6.3-inch model
        phone_label_xpath = "//label[@for=//input[@data-autom='dimensionScreensize6_3inch']/@id]"
        await page.click(f"xpath={phone_label_xpath}")

        await asyncio.sleep(await randomize_sleep())

        # xpath to phone color.
        color_xpath = "(//ul[contains(@class, 'colornav-items')]/li[contains(@class, 'colornav-item')])[2]//label"
        await page.click(color_xpath)

        await asyncio.sleep(await randomize_sleep())

        # storage selector xpath
        storage_xpath = "//label[@for=//input[@data-autom='dimensionCapacity256gb']/@id]"
        await page.click(storage_xpath)

        await asyncio.sleep(await randomize_sleep())

        # Trade-in xpath
        no_tradein_label = "//label[@for='noTradeIn']"
        # Wait for element to be visible/attached
        await page.wait_for_selector(f"xpath={no_tradein_label}", state="visible", timeout=5000)

        await asyncio.sleep(await randomize_sleep())

        # Click with force=True
        await page.locator(f"xpath={no_tradein_label}").click(force=True)

        await asyncio.sleep(await randomize_sleep())

        # apple coverage xpath
        # Wait until the input is no longer disabled
        # Wait until the input is enabled
        await page.wait_for_selector("input[data-autom='acp']:not([disabled])", state="attached", timeout=5000)

        await asyncio.sleep(await randomize_sleep())

        # Target and click the parent label wrapper
        acp_wrapper = page.locator("div.rf-applecare-option:has(input[data-autom='acp']) .rf-applecare-label")
        await acp_wrapper.click(force=True)

        await asyncio.sleep(await randomize_sleep())

        # add coverage_btn xpath
        add_button = page.locator("button[data-autom='inlineapplecare_overlay_add']")
        await add_button.wait_for(state="visible", timeout=5000)
        await add_button.click()

        await asyncio.sleep(await randomize_sleep())

        # add_to_bag xpath
        # Wait for the button to be fully visible and enabled, then click
        add_to_bag_btn = page.locator("button[data-autom='add-to-cart']")
        await add_to_bag_btn.wait_for(state="visible", timeout=5000)
        await add_to_bag_btn.click()

        await asyncio.sleep(await randomize_sleep())

        # Review Bag xpath
        # Wait for the button to be visible and click it
        # Submit the form directly via JavaScript
        # Trigger Apple's JS click handler directly in the browser
        await page.locator("button[data-autom='proceed']").evaluate("el => el.click()")

        await asyncio.sleep(await randomize_sleep())

        # click check_out button
        await page.click('#shoppingCart\\.actions\\.navCheckoutOtherPayments')

        await asyncio.sleep(await randomize_sleep())

        # continue as guest btn
        await page.locator("button[data-autom='guest-checkout-btn']").click()

        await asyncio.sleep(await randomize_sleep())

        # select delivery method
        await page.locator('button.rc-segmented-control-button:has-text("I’d like it delivered")').click()

        await asyncio.sleep(await randomize_sleep())

        # shipping address button xpath
        # ship_btn_xpath = "//button[@data-autom='fulfillment-continue-button']"
        await page.locator("xpath=//button[@data-autom='fulfillment-continue-button']").click()

        await asyncio.sleep(await randomize_sleep())

        # Fill shipping address
        # First Name
        await page.locator('[data-autom="form-field-firstName"]').fill("John")

        await asyncio.sleep(await randomize_sleep())

        # Last Name
        await page.locator('[data-autom="form-field-lastName"]').fill("Doe")

        await asyncio.sleep(await randomize_sleep())

        # Street Name / District / Region
        await page.locator('[data-autom="form-field-street"]').fill("123 Nathan Road")

        await asyncio.sleep(await randomize_sleep())

        # Room / Unit, Floor, Tower / Block, Estate / Building Name
        await page.locator('[data-autom="form-field-street2"]').fill("Flat A, 10/F, Block 1")

        await asyncio.sleep(await randomize_sleep())

        # # check the check-box
        # Click the visual check mark box directly
        # await page.locator(
        #     'label[for="checkout.shipping.addressSelector.newAddress.address.isBusinessAddress"] .form-checkbox-indicator').click()
        # await asyncio.sleep(await randomize_sleep())

        # 1. Check the business address box
        await page.locator(
            'label[for="checkout.shipping.addressSelector.newAddress.address.isBusinessAddress"] .form-checkbox-indicator'
        ).click()

        await asyncio.sleep(await randomize_sleep())

        email = page.locator(
            'fieldset.rs-shipping-addresscontact input[data-autom="form-field-emailAddress"]'
        )
        # or by id (dots need the attribute form, not #id):
        # email = page.locator('[id="checkout.shipping.addressContactEmail.address.emailAddress"]')

        await email.wait_for(state="visible", timeout=5000)
        await email.click()
        await email.press_sequentially("john.doe@example.com", delay=60)
        await email.press("Tab")

        assert await email.input_value() == "john.doe@example.com"
        await asyncio.sleep(await randomize_sleep())


        # # Mobile Phone Number
        await page.locator('[data-autom="form-field-mobilePhone"]').fill("91234567")

        await asyncio.sleep(await randomize_sleep())

        # # Click "Continue to Payment"
        await page.locator('[data-autom="shipping-continue-button"]').click()

        await asyncio.sleep(await randomize_sleep())

        # select payment method
        await page.locator('label[for="checkout.billing.billingoptions.credit"]').click()

        # enter card number
        await page.locator('[data-autom="card-number-input"]').fill("4111111111111111")

        # enter expiration date
        await page.locator('[data-autom="expiration-input"]').fill("12/28")

        # Enter CVV / Security Code
        await page.locator('[data-autom="security-code-input"]').fill("123")

        # check-box: use my shipping address
        await page.locator('[data-autom="shippingAddressCheckbox"]').check(force=True)

        await asyncio.sleep(await randomize_sleep())

        await asyncio.sleep(6)

        # 2. Wait for any loading spinners to finish fading out
        await page.wait_for_selector('.waitindicator', state="hidden", timeout=5000)

        # 3. Blur the last input to ensure form validation state updates
        await page.locator('[data-autom="security-code-input"]').blur()
        await asyncio.sleep(1)

        # 4. Trigger full event sequence on the Review button
        await page.evaluate("""() => {
            const btn = document.querySelector('[data-autom="continue-button-review"]')
                || document.getElementById('rs-checkout-continue-button-bottom');
            if (btn) {
                btn.dispatchEvent(new MouseEvent('mousedown', {bubbles: true, cancelable: true}));
                btn.dispatchEvent(new MouseEvent('mouseup', {bubbles: true, cancelable: true}));
                btn.click();
            }
        }""")

        await asyncio.sleep(await randomize_sleep())

        # click button 'place your order'
        place_order_btn = page.locator('[data-autom="continue-button-placeOrder"]')

        # Scroll into view and click
        await place_order_btn.scroll_into_view_if_needed()
        await place_order_btn.click()

        await asyncio.sleep(await randomize_sleep())

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())