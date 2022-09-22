import requests
from loguru import logger
from bs4 import BeautifulSoup


def replace_smbls_schedule(string: str) -> str:
    string = string.replace('[', '').replace(']', '').replace('"', '').replace('\\', '')
    return string.replace('–', ' - ').replace('AM', ' AM').replace('PM', ' PM')


def get_schedule(response: str, url: str):
    schedule_dict = {}
    try:
        soup = BeautifulSoup(response, features="html.parser")
        days_list = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']
        schedule_script = [str(item).split(',') for item in soup.find_all('script') if days_list[0] in str(item)]
        if schedule_script:
            schedule_script = schedule_script[0][:len(schedule_script[0]) // 2]
            for day in days_list:
                for idx, item in enumerate(schedule_script):
                    if day in item:
                        day = replace_smbls_schedule(item)
                        hour = replace_smbls_schedule(schedule_script[idx + 1])
                        if len(day) < 15 and len(hour) < 15:
                            schedule_dict[day] = hour
            return schedule_dict

        else:
            logger.warning(f'[NO SCHEDULE]: {url} |')
            return 'no_schedule'
    except Exception as ex:
        logger.warning(f'ERROR]: {str(ex)} | {url} |')
