import csv
import json
import time

import psutil
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from fake_useragent import UserAgent

ITER_TIME = 2
SCROLL_TIME = 1.5
btn_nst_xth = '//*[@id="action-menu"]/ul/li[2]'  # button newest xpath
btn_srt_xth = '//button[normalize-space()="Sort"]'  # button newest xpath
btn_rw_xth = '//*[contains(text(), "More reviews")]'  # button reviews xpath
scrl_mn_xth = '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]'  # sidebar main xpath
scrl_rw_xth = '/html/body/div[3]/div[9]/div[9]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]'  # sidebar review xpath


def create_driver() -> WebDriver:
    useragent = UserAgent()
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--lang=en")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('ignore-certificate-errors')
    chrome_options.add_argument(f"user-agent={useragent.random}")
    chrome_options.add_argument("--disable-site-isolation-trials")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def timed(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        duration = "[{name}]: finished in {elapsed:.2f}s".format(
            name=func.__name__.upper(),
            elapsed=time.time() - start
        )
        logger.info(duration)
        return result

    return wrapper


def kill_by_process():
    process_names = ['chromedriver.exe']
    try:
        for proc in psutil.process_iter():
            for process_name in process_names:

                if proc.name() == process_name:
                    proc.kill()
    except Exception as ex:
        print(str(ex))
        # logger.warning(f"Session isn't closed [{str(ex)}]")
        # os.system("taskkill /f /im " + PROCESS_NAME)
        # logger.info('[KILL BY PROCESS SHELL]')


def save_json(data: dict) -> None:
    with open('db/reviews-test.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=3)
    return logger.success(f'[SAVE SCV]')


def open_scv(file_name: str) -> list:
    with open(f'{file_name}', "r") as fp:
        reader = csv.reader(fp, delimiter=",", quotechar='"')
        return [row for row in reader]


def create_companies_list(db_file_name: str) -> list:
    return [f"{company[8].split('?hl')[0]}?hl=en" for company in open_scv(db_file_name)]

