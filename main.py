from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
import pyautogui as pag
import time as t

# !!!!!!!!!!!!!!IMPORTANT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# You must backspace the '#' at the beginning of
# lines 127 & 128 for it to complete the entire process
# Example lines:
# x, y = pag.locateCenterOnScreen('completepurchase.png', confidence=0.9)
# pag.click(x, y)


# ENTER YOUR INFORMATION HERE --------------------------------------------------------
# the name or keyword to be found in the product (separated by a '-' if more than one
product_attribute = "ass-hat"
# your personal info for checkout
contact_info = ["Firstname", "Lastname", "email@hotmail.com", "phone"]
# your address info for shipping
shipping_info = ["street", "", "city", "state (not abbreviated)", "zip"]
# your paypal login
paypal_info = ["paypal email or phone", "paypal password"]
# ------------------------------------------------------------------------------------

def start_driver():
    # modification to browser
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-extensions")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=1920,1080")
    # Initialize the webdriver, options, and get the password field and error message box
    web_driver = webdriver.Chrome(options=chrome_options)
    web_driver.get("https://glowmandan.bigcartel.com/")

    return web_driver


def add_product_to_cart(web_driver):
    # find the product card in the main store page
    card = web_driver.find_elements(By.XPATH,  f"//*[contains(@href, '{product_attribute}')]")[0]
    if card:
        card.click()
    else:
        driver.quit()
        print(f'Product with "{product_attribute}" not found in store')
    t.sleep(0.3)

    # find the add product button on the product page
    add_cart = web_driver.find_elements(By.XPATH,  "//*[contains(@class, 'add-to-cart')]")[0]
    add_cart.click()

    # Go to the checkout page
    check_out = web_driver.find_elements(By.XPATH, "//*[contains(@class, 'checkout-btn')]")[0]
    check_out.click()


def complete_checkout(web_driver):
    # find personal info fields and populate them
    web_driver.find_elements(By.XPATH, "//*[contains(@name, 'buyer_first_name')]")[0].send_keys(contact_info[0])
    web_driver.find_elements(By.XPATH, "//*[contains(@name, 'buyer_last_name')]")[0].send_keys(contact_info[1])
    web_driver.find_elements(By.XPATH, "//*[contains(@name, 'buyer_email')]")[0].send_keys(contact_info[2])
    web_driver.find_elements(By.XPATH, "//*[contains(@name, 'buyer_phone_number')]")[0].send_keys(contact_info[3])
    next_button = web_driver.find_elements(By.XPATH, "//*[contains(@type, 'submit')]")[0]
    # proceed and wait for animation
    next_button.click()
    t.sleep(2)

    # find shipping info fields and populate them
    web_driver.find_elements(By.XPATH, "//*[contains(@id, 'shipping_address_1')]")[0].send_keys(shipping_info[0])
    web_driver.find_elements(By.XPATH, "//*[contains(@name, 'shipping_address_2')]")[0].send_keys(shipping_info[1])
    web_driver.find_elements(By.XPATH, "//*[contains(@name, 'shipping_city')]")[0].send_keys(shipping_info[2])
    Select(web_driver.find_elements(By.NAME, "shipping_state")[0]).select_by_visible_text(shipping_info[3])
    web_driver.find_elements(By.XPATH, "//*[contains(@name, 'shipping_zip')]")[0].send_keys(shipping_info[4])
    next_button = web_driver.find_elements(By.XPATH, "//*[contains(@type, 'submit')]")[1]
    # proceed and wait for animation
    next_button.click()
    t.sleep(2)

    # continue past the shipping options
    next_button = web_driver.find_elements(By.XPATH, "//*[contains(@type, 'submit')]")[2]
    # proceed and wait for animation
    next_button.click()
    t.sleep(2)

    # switch from CC payment to Paypal
    button_x, button_y = pag.locateCenterOnScreen('paypalbutton.png', confidence=0.9)
    pag.click(button_x, button_y)
    next_button = web_driver.find_elements(By.XPATH, "//*[contains(@type, 'submit')]")[3]
    # proceed and wait for animation
    next_button.click()
    t.sleep(2)

    # visually find the Paypal checkout button and click
    button_x, button_y = pag.locateCenterOnScreen('checkout.png', confidence=0.9)
    pag.click(button_x, button_y)
    t.sleep(3)


def paypal_interact(web_driver):
    # establish main page and determine Paypal window
    main_page = web_driver.current_window_handle
    other_windows = web_driver.window_handles
    paypal_window = None
    for window in other_windows:
        if window != main_page:
            paypal_window = window

    # switch to Paypal popup window
    web_driver.switch_to.window(paypal_window)

    # enter Paypal username
    paypal_user = web_driver.find_elements(By.XPATH, "//*[contains(@placeholder, 'Email or mobile number')]")[0]
    paypal_user.send_keys(paypal_info[0])
    paypal_user.send_keys(Keys.RETURN)
    # wait for load
    t.sleep(2)

    # enter Paypal password
    paypal_pass = web_driver.find_elements(By.XPATH, "//*[contains(@placeholder, 'Password')]")[0]
    paypal_pass.send_keys(paypal_info[1])
    paypal_pass.send_keys(Keys.RETURN)
    t.sleep(15)

    # complete Paypal purchase (using default payment method)
    # x, y = pag.locateCenterOnScreen('completepurchase.png', confidence=0.9)
    # pag.click(x, y)

if __name__ == '__main__':
    # run the each stage
    driver = start_driver()
    add_product_to_cart(driver)
    complete_checkout(driver)
    paypal_interact(driver)

    # wait for manual termination of the webdriver
    terminate_web_driver = str(input("Close the bot? Y/N->"))
    while terminate_web_driver != 'Y':
        print("checking again in 60 seconds...")
        t.sleep(60)
    driver.quit()
