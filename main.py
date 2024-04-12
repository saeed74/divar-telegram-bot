import requests
import json
import os
#from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

#SEARCH_URL = os.getenv('SEARCH_CONDITIONS')
SEARCH_URL = "mashhad/rent-residential?credit=10000000-150000000&rent=3000000-13000000"

URL = "https://api.divar.ir/v8/web-search/" + SEARCH_URL
TOKENS = list()
BOT_TOKEN = "6468244388:AAHNduXgSMClUSi6An8iRHwNxr8rRDdD-6I"
BOT_CHATID = "-4160354534"


def get_data():
    response = requests.get(URL)
    return response


def parse_data(data):
    return json.loads(data.text)


def get_houses_list(data):
    return data['web_widgets']['post_list']


def extract_each_house(house):
    data = house['data']

    return {
        'title': data['title'],
        'description': data['top_description_text'] + " - " + data['middle_description_text'],
        'district': data['action']['payload']['web_info']['district_persian'],
        'token': data['token'],
    }


def send_telegram_message(house):
    url = 'https://api.telegram.org/bot' + BOT_TOKEN + '/sendMessage'
    text = f"<b>{house['title']}</b>"+"\n"
    text += f"<i>{house['district']}</i>"+"\n"
    text += f"{house['description']}"+"\n\n"
    text += f"https://divar.ir/v/a/{house['token']}"

    body = {
        'chat_id': BOT_CHATID,
        'parse_mode': 'HTML',
        'text': text
    }

    requests.post(url, data=body)


def load_tokens():
    with open("tokens.json", "r") as content:
        if content == "":
            return []
        return json.load(content)


def save_tokns(tokens):
    with open("tokens.json", "w") as outfile:
        json.dump(tokens, outfile)


if __name__ == "__main__":
    tokens = load_tokens()

    data = get_data()
    data = parse_data(data)
    data = get_houses_list(data)

    INCLUDE_DISTRICTS = [
        'آزادشهر',
        'اقبال',
        'اقبال لاهوری',
        'دانشجو',
        'ستاری',
        'شهرآرا',
        'صدف',
        'صیاد شیرازی',
        'فارغ التحصیلان',
        'فرهنگ',
        'نوفل لوشاتو',
        'وکیل‌آباد'
    ]
    
    for house in data:
        house_data = extract_each_house(house)
        if house_data is None:
            continue
        if house_data['token'] in tokens:
            continue
        if house_data['district'] not in INCLUDE_DISTRICTS:
            continue

        tokens.append(house_data['token'])
        send_telegram_message(house_data)

    save_tokns(tokens)
