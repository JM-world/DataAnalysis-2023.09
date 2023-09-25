import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def get_fashion_list():
    browser = webdriver.Chrome()
    browser.get('https://www.musinsa.com/ranking/best')
    #url = 'https://www.musinsa.com/ranking/best'
    #res = requests.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    trs = soup.find("ul", class_="snap-article-list boxed-article-list article-list center list goods_small_media8")
    tr = trs.find_all("li", recursive=False)
    
    
    rank = tr[0].find('p', class_="n-label label-default txt_num_rank").get_text().strip()[:3].strip()
    rank_update = tr[10].select_one("p > span").get_text().strip()
    if len(rank_update) != 1:
        rank_update = '[ ' + rank_update[:1] + rank_update[-4:].strip() + ' ]'
    else:
        rank_update = '[ ' + rank_update + ' ]'
    brand = tr[0].select_one(".item_title > a").get_text().strip()
    name = tr[0].select_one(".list_info > a").get_text().strip()
    price = tr[1].select_one(".price").get_text().strip()[-10:].strip()
    like = tr[0].select_one(".txt_cnt_like > span").get_text().strip()
    img = tr[0].select_one("div.li_inner > div.list_img > a > img")['src']
    return price

print(get_fashion_list())