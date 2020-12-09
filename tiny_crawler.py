from __future__ import print_function, unicode_literals

import pkg_resources
import sys

from pyimod03_importers import FrozenImporter

if getattr(sys, 'frozen', False):
   pkg_resources.register_loader_type(
       FrozenImporter, pkg_resources.DefaultProvider
   )

from urllib.request import urlretrieve
from getpass import getpass

from pyfiglet import Figlet
from pyfiglet import fonts

from PyInquirer import prompt
from pprint import pprint

import os
from configparser import ConfigParser

basedir = os.path.abspath(os.path.dirname(__file__)) 

# config_file = os.path.join(basedir, 'config.ini')
# config_file = 'config.ini'
# CONFIG_FILES = [config_file]
config = ConfigParser()
config.read(['config.ini'])

    
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager




# Init config
SITE = config["CRAWL"]["SITE"]
WIDTH = config["CRAWL"]["WIDTH"]
HEIGHT = config["CRAWL"]["HEIGHT"]
ID_XPATH = config["CRAWL"]["ID_XPATH"]
PW_XPATH = config["CRAWL"]["PW_XPATH"]
FORM_CLS_PATH = config["CRAWL"]["FORM_CLS_PATH"]
NOTI_INFO_XPATH = config["CRAWL"]["NOTI_INFO_XPATH"]
LOGIN_INFO_XPATH = config["CRAWL"]["LOGIN_INFO_XPATH"]
POST_TAG_PATH = config["CRAWL"]["POST_TAG_PATH"]
LINK_TAG_PATH = config["CRAWL"]["LINK_TAG_PATH"]
TOTAL_POSTS_XPATH = config["CRAWL"]["TOTAL_POSTS_XPATH"]
POST_DESC_XPATH = config["CRAWL"]["POST_DESC_XPATH"]
LIKE_LIST_XPATH = config["CRAWL"]["LIKE_LIST_XPATH"]

NUMBER_OF_IMAGES = config["CRAWL"]["NUMBER_OF_IMAGES"]

f = Figlet(font='slant')
print (f.renderText('Get Hot Girl !'))

questions = [
    {
        'type': 'input',
        'name': 'MODE',
        'message': '모드를 선택해주세요: (1): 유저, (2)태그',
    },
    {
        'type': 'input',
        'name': 'ID',
        'message': '인스타그램 아이디를 입력해주세요:',
    },
]
tag_answer = {
        'type': 'input',
        'name': 'TAG',
        'message': '태그를 입력해주세요: ',
    },
user_answer = {
        'type': 'input',
        'name': 'TARGET_USER',
        'message': '상대 인스타 아이디를 입력해주세요(ex: https://www.instagram.com/dev.gon.io/): ',
    },
answers = prompt(questions)

MODE = answers['MODE']
mode_set = {
    'target':[]
}
if MODE == '1':
    mode_set['mode'] = MODE
    user_list =[]
    with open('list.txt', 'r') as f:
        data = f.readlines()
    user_list = user_list+data
    if len(user_list) <1:
        print('[INIT]: 유저리스트가 없습니다.')
        target = prompt(user_answer)
        mode_set['target'].append(target['TARGET_USER'])
    else:
        print('[INIT]: 타겟 목록 로드 완료.')
        mode_set['target'] = user_list
    
# elif MODE == '2':
#     target=prompt(tag_answer)
#     print(target)
#     mode_set['mode'] = MODE
#     mode_set['target'] = target['TAG']
else:
    print('[ERROR]: 초기설정실패(모드값 이상)')
    sys.exit()


ID = answers['ID']
PW = getpass('[INIT]: (보안 모드)비밀번호를 입력해주세요:')
print('[INIT]: 설정 로드 완료')
print('[START]: ================ 크롬 브라우저 실행 ================')

# Wait time set
LOAD_TIME = 10
RENDER_TIME = 1


# Implicit wait function
def wait_presence(wait_target, explicit_time, call_by, element_path):
    """
    =Usage=
    wait_target: implicit wait target scope
    implicit_time: wait time
    call_by: find element by element type (ex: By.CLASS_NAME, By.XPATH)
    element_path: target elememnt path(ex: 'a', ''//*[@id="loginForm"]/div/div[1]/div/label/input')

    =Return=
    found web element
    """
    element = WebDriverWait(wait_target, explicit_time).until(
        EC.element_to_be_clickable((call_by, element_path))
    )
    return element


# Initialize browser
browser = webdriver.Chrome(ChromeDriverManager().install())
browser.maximize_window()
browser.get(SITE)

# login
login_form = WebDriverWait(browser, 5).until(
    EC.presence_of_element_located((By.CLASS_NAME, FORM_CLS_PATH))
)
id_form = login_form.find_element_by_xpath(ID_XPATH)
pw_form = login_form.find_element_by_xpath(PW_XPATH)
# send login info
id_form.send_keys(ID)
pw_form.send_keys(PW)
pw_form.send_keys(Keys.ENTER)

# wait and click login info btn
check_btn = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, LOGIN_INFO_XPATH))
)
check_btn.send_keys(Keys.ENTER)

# wait and click noti btn
check2_btn = WebDriverWait(browser, 10).until(
    EC.presence_of_element_located((By.XPATH, NOTI_INFO_XPATH))
)
check2_btn.send_keys(Keys.ENTER)


for target in mode_set['target']:
    print(f'[DONWLOAD]: {target}')
    target = target.rstrip('\n')
    target_name = target.split('/')
    
    cnt=0
    browser.get(target.rstrip('\n'))
    posts_container = browser.find_element(By.TAG_NAME, POST_TAG_PATH)
    top_three_posts = posts_container.find_elements(By.TAG_NAME, LINK_TAG_PATH)
    top_three_posts = top_three_posts[:int(NUMBER_OF_IMAGES)]
    links = [post.get_attribute("href") for post in top_three_posts]
    for link in links:
        browser.get(link)
        img_cont = browser.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div[1]/article/div[2]')
        img = img_cont.find_element(By.TAG_NAME,'img')
        src = img.get_attribute('src')
        urlretrieve(src, f"images/{target_name[3]}-{cnt}.png")
        print(f"[COMPLETE]: images/{target_name[3]}-{cnt}.png")
        cnt+=1

browser.quit()
# download the image
# //*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div/div/div[1]/img
# //*[@id="react-root"]/section/main/div/div[1]/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[3]/div/div/div/div[1]/img
# /html/body/div[5]/div[2]/div/article/div[2]/div/div[1]/div[2]/div/div/div/ul/li[3]/div/div/div/div[1]/img
# urllib.urlretrieve(src, "captcha.png")