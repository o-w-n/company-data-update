from bs4 import BeautifulSoup
from datetime import datetime, timedelta


def clear_user_rating(string: str) -> str:
    return string.replace(' stars', '').replace(' star', '').strip()


def clear_user_date(string: str) -> str:
    return string.replace(' ago', '').replace('a ', '').strip()


def convert_to_timestamp(string: str) -> str:
    if 'second' in string:
        return str(datetime.now()).split()[0]
    elif 'minutes' in string:
        return str(datetime.now()).split()[0]
    elif 'hour' in string:
        return str(datetime.now()).split()[0]
    elif 'day' in string:
        if (string.split()[0]).isdigit():
            user_date = int(string.split()[0])
            return str((datetime.now()).date() - timedelta(days=user_date * 7))
        else:
            user_date = 1
            return str((datetime.now()).date() - timedelta(days=user_date * 7))
    elif 'week' in string:
        if (string.split()[0]).isdigit():
            user_date = int(string.split()[0])
            return str((datetime.now()).date() - timedelta(days=user_date * 7))
        else:
            user_date = 1
            return str((datetime.now()).date() - timedelta(days=user_date * 7))
    elif 'month' in string:
        if (string.split()[0]).isdigit():
            user_date = int(string.split()[0])
            return str((datetime.now()).date() - timedelta(days=user_date * 30))
        else:
            user_date = 1
            return str((datetime.now()).date() - timedelta(days=user_date * 30))
    elif 'year' in string:
        if (string.split()[0]).isdigit():
            user_date = int(string.split()[0])
            return str((datetime.now()).date() - timedelta(days=user_date * 365))
        else:
            user_date = 1
            return str((datetime.now()).date() - timedelta(days=user_date * 365))


def get_reviews(response: str) -> dict:
    review_dict = {}
    soup = BeautifulSoup(response, features="html.parser")
    blocks_review = soup.find_all('div', class_='jJc9Ad')
    for count_review, value in enumerate(blocks_review[:len(blocks_review) - 10]):
        # slice 10 last reviews after last scroll, because scroll_reviews load new reviews with "More" buttons
        review_dict.update({count_review: {}})
        review_dict[count_review] = {
            'user_name': value.find('div', class_='d4r55').text.strip(),
            'user_description': value.find('span', class_='rsqaWe').text.replace(' ago', '').strip(),
            'user_rating': clear_user_rating(value.find('span', class_='kvMYJc')['aria-label']),
            'user_text': value.find('div', class_='MyEned').text.split('(Original)')[-1].strip(),
            'user_date': convert_to_timestamp(clear_user_date(value.find('span', class_='rsqaWe').text))
        }
    return review_dict


def get_reviews2(response: str) -> dict:
    review_dict = {}
    soup = BeautifulSoup(response, features="html.parser")
    blocks_review = soup.find_all('div', class_='jJc9Ad')
    for count_review, value in enumerate(blocks_review):
        review_dict.update({count_review: {}})
        review_dict[count_review] = {
            'user_name': value.find('div', class_='d4r55').text.strip(),
            'user_description': value.find('span', class_='rsqaWe').text.replace(' ago', '').strip(),
            'user_rating': clear_user_rating(value.find('span', class_='kvMYJc')['aria-label']),
            'user_text': value.find('div', class_='MyEned').text.split('(Original)')[-1].strip(),
            'user_date': convert_to_timestamp(clear_user_date(value.find('span', class_='rsqaWe').text))
        }
    return review_dict
