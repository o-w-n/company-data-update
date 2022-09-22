import time

from bs4 import BeautifulSoup
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from reviews import get_reviews, get_reviews2
from schedule import get_schedule
from place_id import get_place_id
from business_status import get_status
from config import SCROLL_TIME, ITER_TIME, btn_nst_xth, btn_srt_xth, scrl_rw_xth, scrl_mn_xth, btn_rw_xth, create_driver

driver = create_driver()


def scroll_main(scroll_element_xpath: str) -> None:
    scrolling_element = driver.find_element(By.XPATH, scroll_element_xpath)
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrolling_element)
    while True:
        driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', scrolling_element)
        time.sleep(SCROLL_TIME)
        # Check if more scrolling required
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrolling_element)
        if new_height == last_height:
            break
        last_height = new_height


def scroll_reviews(scroll_element_xpath: str, scroll_number: int) -> None:
    scrolling_element = driver.find_element(By.XPATH, scroll_element_xpath)
    last_height = driver.execute_script("return arguments[0].scrollHeight", scrolling_element)
    for _ in range(scroll_number):  # 1 scroll_number = 10 reviews
        driver.execute_script('arguments[0].scrollTo(0, arguments[0].scrollHeight)', scrolling_element)
        time.sleep(SCROLL_TIME)
        for bt in driver.find_elements(By.XPATH, '//*[contains(@class,"w8nwRe kyuRq")]'):
            wait = WebDriverWait(driver, 20)
            wait.until(EC.element_to_be_clickable(bt)).click()
        new_height = driver.execute_script("return arguments[0].scrollHeight", scrolling_element)
        if new_height == last_height:
            break
        last_height = new_height


def get_company_data(url: str) -> dict:
    companies_data_dict = {}
    driver.get(url)
    time.sleep(ITER_TIME)
    place_id = get_place_id(driver.page_source, url)
    if place_id:
        business_status = get_status(driver.page_source, url)
        companies_data_dict.update({place_id: {}})
        if business_status == 'Operational':
            companies_data_dict[place_id] = {
                'url': url,
                'business_status': business_status,
                'schedule': get_schedule(driver.page_source, url)
            }
            scroll_main(scroll_element_xpath=scrl_mn_xth)  # scroll to see 'More views' button
            time.sleep(ITER_TIME)
            try:
                more_reviews_element = driver.find_element(By.XPATH, btn_rw_xth) # click 'More reviews' button
                more_reviews_element.click()
                time.sleep(ITER_TIME)
                driver.find_element(By.XPATH, btn_srt_xth).click()  # click 'Sort' button to sort reviews by newest
                time.sleep(ITER_TIME)
                driver.find_element(By.XPATH, btn_nst_xth).click()  # click 'Newest' button to see newest reviews
                time.sleep(ITER_TIME)
                scroll_reviews(scroll_element_xpath=scrl_rw_xth, scroll_number=10)  # scroll down to render reviews
                companies_data_dict[place_id]['reviews'] = get_reviews(driver.page_source)
                logger.info(f'Place ID: {place_id} | Business status: {business_status}\nUrl: {url}')
            except:
                companies_data_dict[place_id]['reviews'] = get_reviews2(driver.page_source)
        else:
            # if company closed, write only business status in main_dict
            companies_data_dict[place_id] = {
                'business_status': business_status,
                'url': url
            }
            logger.warning(f'Place ID: {place_id} | Business status: {business_status}\nUrl: {url}')
    else:
        logger.error(f'[UNDIRECT URL]: EDIT COMPANY IN ADMIN-TG\nUrl: {url}')
    return companies_data_dict
