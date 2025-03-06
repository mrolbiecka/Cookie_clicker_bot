from selenium import webdriver
from selenium.webdriver.common.by import By
import threading
import time

TIMEOUT = 300
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get("http://orteil.dashnet.org/experiments/cookie/")
search = driver.find_element(By.CSS_SELECTOR, "#cookie")


def check_money():
    money_amount = driver.find_element(By.CSS_SELECTOR, "#money").text
    money_amount_new = money_amount.replace(",", "")
    return int(money_amount_new)


def decide_what_to_buy():
    search_store = driver.find_element(By.CSS_SELECTOR, "#store")
    list1 = search_store.text.split("\n")
    list2 = [item for item in list1 if "-" in item]
    numbers_list = [int(item.split(' - ')[1].replace(',', '')) for item in list2]
    print(numbers_list)
    available_price = check_money()
    affordable_item = [i for i in numbers_list if i <= available_price]
    if affordable_item:
        max_aff_item = max(affordable_item)
        print(max_aff_item)
        item_dict = {
            numbers_list[0]: "Cursor",
            numbers_list[1]: "Grandma",
            numbers_list[2]: "Factory",
            numbers_list[3]: "Mine",
            numbers_list[4]: "Shipment",
            numbers_list[5]: "Alchemy lab",
            numbers_list[6]: "Portal",
            numbers_list[7]: "Time machine"
        }
        if max_aff_item in item_dict:
            value = item_dict[max_aff_item]
        else:
            value = "Cursor"
        search_max_aff_item = driver.find_element(By.XPATH, f"//*[contains(text(), '{value}')]")
        search_max_aff_item.click()
    else:
        print("No affordable items right now")


def periodic_task():
    while time.time() < timeout_start + TIMEOUT:
        decide_what_to_buy()
        time.sleep(5)


def check_how_many_cookies():
    cookies = driver.find_element(By.CSS_SELECTOR, "#cps")
    cookies_text = cookies.text
    return cookies_text


timeout_start = time.time()
thread = threading.Thread(target=periodic_task)
thread.start()

while time.time() < timeout_start + TIMEOUT:
    search.click()
    time.sleep(0.01)

driver.quit()
