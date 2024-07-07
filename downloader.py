# In[1]
import os.path

import requests
from playwright.sync_api import sync_playwright
import shutil
from os import path
from draw_marker import draw_marker
from imgs_join import gen_merge_pages

# In[2]:

url = 'https://www.iyingdi.com/share/deck/deck.html?game=magic&id=973958&lang=SC'
session = requests.session()
cards_group_info = {}

# In[3]:
playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False, channel='msedge')
context = browser.new_context(viewport={'width': 1920, 'height': 1024})
page = context.new_page()
page.goto(url)

# %% cards info
# 卡组名称
query = page.query_selector('.formatName')
card_group_name = ' '.join([query.query_selector('.format').inner_text(), query.query_selector('.name').inner_text()])
cards_group_info.setdefault('name', card_group_name)
del card_group_name, query

# 卡组表图
query = page.query_selector(':text("导出图片")')
with page.expect_popup() as popup_info:
    query.click()
page1 = popup_info.value
group_img_url = page1.url
cards_group_info.setdefault('group_img_url', group_img_url)
page1.close()
del group_img_url, page1

# 卡分类
all_cards = []  # 全部卡的信息
query_type_list = page.query_selector_all('.cardList .cardType')
print(query_type_list)
for card_type in query_type_list:
    card_type_title = card_type.query_selector('.title').inner_text()
    card_list = card_type.query_selector_all('li.card')
    cur_card_type = {}  # 保存当前循环中卡分类信息
    cur_card_type = {'title': card_type_title}  # 卡分类标题
    cur_card_type.setdefault('cards', [])  # 此分类中的卡列表
    for card in card_list:
        card_name = card.query_selector('div.name').inner_text()
        card_count = int(card.query_selector('span.count').inner_text().strip()[1:])
        card_url = card.query_selector('img').get_attribute('src')
        cur_card_type.get('cards').append((card_name, card_count, card_url))
    all_cards.append(cur_card_type)
cards_group_info['card_types'] = all_cards

# 输出结果
print(cards_group_info)

# %% clear:
session.close()
page.close()
context.close()
browser.close()
playwright.stop()


# In[7]:


def download_file(session, addr, save_file_name):
    res = session.get(addr)
    with open(save_file_name, 'wb') as fi:
        fi.write(res.content)


def copy_files(file_name, count):
    for i in range(1, count):
        split_name = path.splitext(file_name)
        new_file_name = '{}_{}{}'.format(split_name[0], i + 1, split_name[1])
        shutil.copyfile(file_name, new_file_name)


# In[9]:


# downloads images
base_dir = 'download'
# 下载并保存总览图
download_file(session, cards_group_info.get('group_img_url'),
              path.join(base_dir, f'{cards_group_info.get("name")}.jpg'))
# 下载并保存全部图
for card_type in cards_group_info.get('card_types'):
    type_title = card_type.get('title')
    for c_name, c_count, c_url in card_type.get('cards'):
        c_name = str(c_name).replace('/', '_')
        c_url = str(c_url).split('?')[0]
        print(c_url)
        ext_name = path.splitext(c_url)[-1]
        save_file = '{}_{}{}'.format(type_title, c_name, ext_name)
        save_file = path.join(base_dir, save_file)
        download_file(session, c_url, save_file)  # 下载并保存图像
        copy_files(save_file, c_count)  # 复制出对应的数量
draw_marker(base_dir)  # 标记备牌

# 生成合并图，目前是3*3第页布局
gen_merge_pages()

for file_name in os.listdir(base_dir):
    os.remove(path.join(base_dir, file_name))