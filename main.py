import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.divar.ir/v8/web-search/{SEARCH_CONDITIONS}".format(**os.environ)
TOKENS = list()
BOT_TOKEN = '{BOT_TOKEN}'.format(**os.environ)
BOT_CHATID = '{BOT_CHATID}'.format(**os.environ)


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
        'description': data['description'],
        'district': data['district'],
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
        'جلال آل احمد',
        'جلال‌آل‌احمد',
        'هاشمیه',
        'کوثر',
        'سیدرضی',
        'سید رضی',
        'وکیل آباد',
        'وکیل‌آباد',
        'اقبال',
        'اقبال لاهوری',
        'اقبال‌لاهوری',
        'لادن',
        'صیاد شیرازی',
        'صیادشیرازی',
        'آزاد شهر',
        'آزادشهر',
        'امامت',
        'امامیه',
        'دانشجو',
        'دانش آموز',
        'دانش‌آموز',
        'فارغ‌التحصیلان',
        'فارغ التحصیلان',
        'دندانپزشکان',
        'پیروزی',
        'فرهنگ',
        'رضاشهر',
        'سرافرازان',
        'نماز',
        'معلم',
        'استقلال',
        'شهرآرا',
        'خاقانی',
        'صدف',
        'چهارچشمه',
        'هنرستان',
        'محله چهارچشمه',
        'هفت تیر',
        'شهرستانی',
        'حافظ',
        'ستاری',
        'آموزگار',
        'شهرک طالقانی',
        'فرامز عباسی',
        'فرامزعباسی',
        'فردوسی',
        'میدان فردوسی',
        'جانباز',
        'میدان جانباز',
        'کوثر جنوبی',
        'کوثرجنوبی',
        'دلاوران',
        'ویلا',
        'محله کوثر',
        'محله‌کوثر',
        'محله جاهدشهر',
        'محله سرافرازان',
        'محله‌سرافرازان',
        'محله‌جاهدشهر',
        'کوه سنگی',
        'کوهسنگی',
        'کلاهدوز',
        'فرامرز عباسی',
        'راهنمایی',
        'دانشگاه فردوسی مشهد',
        'بهشتی',
        'بهاران',
        'بلوار سجاد',
        'باهنر',
        'باغ ملک‌آباد',
        'ارشاد',
        'احمدآباد',
        'احمد آباد',
        'نوفل لوشاتو',
        'نوفل‌لوشاتو',
        'نمایشگاه بین المللی مشهد',
        'حافظیه'
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
