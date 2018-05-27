#!/usr/bin/env python3

import webbrowser
from time import sleep
from datetime import datetime
import requests                   # see
from bs4 import BeautifulSoup     # requirements.txt


LOGIN = '*************'      # login    on  anytask.org
PASSWORD = '**********'      # password on  anytask.org
TARGET = 'Имя Фамилия	дата		дата'  # Just copy line with full name and dates from task
UPDATE_TIME = 300  # update time in seconds
URL = 'https://www.youtube.com/watch?v=HEXWRTEbj1I'  # will open this video and will start to play it


def login():
    session = requests.session()
    session.get("https://anytask.org/course/319")
    login_data = {'csrfmiddlewaretoken': session.cookies.get_dict()['csrftoken'],
                  'username': LOGIN,
                  'password': PASSWORD}
    referer = {'Referer': 'https://anytask.org/accounts/login/?next=/course/319'}
    session.post("https://anytask.org/accounts/login/", data=login_data, headers=referer)
    return session


def get_page(session):
    page = session.get("https://anytask.org/course/319").text
    header = 'УрФУ\n>\npython.task\n|\n2017-2018'
    page = '\n'.join(i.strip() for i in BeautifulSoup(page, 'html.parser').get_text().split())
    if page.startswith(header):  # check if not "login timeout"
        return session, page
    return get_page(login())     # relogin


if __name__ == '__main__':
    try:
        target = '\n'.join(TARGET.split())
        session = login()
        while True:
            session, text = get_page(session)
            if text.find(target) == -1:
                webbrowser.open("https://anytask.org/course/319")  # opens anytask in new tab
                webbrowser.open(URL)  # opens new tab and loads content
                print("ATTENTION!!!")
                break
            else:
                print("Last update:", datetime.now().strftime("%H:%M:%S"), end="\r")
            sleep(UPDATE_TIME)
    except KeyboardInterrupt:
        exit()
