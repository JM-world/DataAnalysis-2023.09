import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def get_bestseller():
    base_url = 'http://book.interpark.com'
    url = f'{base_url}/display/collectlist.do?_method=bestsellerHourNew&bookblockname=b_gnb&booklinkname=%BA%A3%BD%BA%C6%AE%C1%B8&bid1=bgnb_mn&bid2=LiveRanking&bid3=main&bid4=001'
    res = requests.get(url)     # url 가져오기
    soup = BeautifulSoup(res.text, 'html.parser')
    lis = soup.select('.rankBestContentList > ol > li')

    data = []
    for li in lis:
        title = li.select_one('.itemName').get_text().strip()
        author = li.select_one('.author').get_text().strip()
        company = li.select_one('.company').get_text().strip()
        price = li.select_one('.price > em').get_text().strip()
        price = int(price.replace(',', ''))
        rank = li.select_one('.cover').find('div', class_='rankNumber digit2').find_all('span')
        href = li.select_one('.coverImage > label > a')['href'] # 자식 셀렉터
        src =  li.select_one('.coverImage img')['src']  # 꺽새 없으므로 자손 셀렉터
        if len(rank) == 2:
            r1, r2 = str(rank[0]), str(rank[1])
            r1, r2 = r1[-10], r2[-10]
            s = r1+r2
        else:
            s = ''
            s+=str(rank[0])[-10]
            s
        data.append({'제목': title, '저자':author, '출판사':company, '가격':f'{price:7,d}', 
                    '순위':s, 'href': base_url+href, 'src': src})
    return data

def get_melon_chart():
    url = 'https://www.melon.com/chart/index.htm'
    header = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
    res = requests.get(url, headers= header)
    soup = BeautifulSoup(res.text, 'html.parser')
    date_str = soup.select_one('.yyyymmdd').get_text().strip() + \
                soup.select_one('.hhmm').get_text().strip()
    date_str = date_str.replace('.', '').replace(':', '')
    trs = soup.select('.lst50')
    data = []
    for tr in trs:
        rank = int(tr.select_one('.rank').get_text().strip())
        title = tr.select_one('.ellipsis.rank01').get_text().strip()
        artist = tr.select_one('.ellipsis.rank02 > a').get_text().strip()
        album = tr.select_one('.ellipsis.rank03').get_text().strip()
        image = tr.select_one('tr > td:nth-child(4) > div > a > img')['src']
        data.append({'순위': rank, '제목': title, '아티스트':artist, '앨범':album, '이미지': image})

    return data

def get_restaurant_list(keyword):
    url = f'https://www.siksinhot.com/search?keywords={keyword}'
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    trs = soup.select('.localFood_list > li')

    data = []
    for tr in trs:
        atag = tr.select_one('figcaption > a')
        name = atag.select_one('h2').get_text().strip()
        score = atag.select_one('.score').get_text().strip()
        menu = tr.select('.cate > a')[-1].get_text().strip()
        sub_href = atag['href']
        sub_res = requests.get(sub_href)
        sub_soup = BeautifulSoup(sub_res.text, 'html.parser')
        info = sub_soup.select('.pc_only > td')
        addr = info[0].select_one('div').get_text().split('지번')[0].strip()
        tel = info[1].select_one('div').get_text().strip()
        data.append({'가게명':name, '평점':score, '메뉴':menu, '주소':addr, '전화번호':tel})
    
    return data

def get_fashion_list():
    options = Options()
    options.add_experimental_option("detach", True) # 브라우저 꺼짐 방지 옵션

    browser = webdriver.Chrome(options=options)
    browser.maximize_window()   # 창 최대화
    browser.get('https://www.musinsa.com/ranking/best')
    

    body = browser.find_element(By.TAG_NAME, 'body')
    for _ in range(10):
        body.send_keys(Keys.PAGE_DOWN)
        time.sleep(1)
    #url = 'https://www.musinsa.com/ranking/best'
    #res = requests.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    trs = soup.find("ul", class_="snap-article-list boxed-article-list article-list center list goods_small_media8")
    tr = trs.find_all("li", recursive=False)
    
    data = []
    for t in tr:
        rank = t.find('p', class_="n-label label-default txt_num_rank").get_text().strip()[:3].strip()
        rank_update = t.select_one("p > span").get_text().strip()
        if len(rank_update) != 1:
            rank_update = '[ ' + rank_update[:1] + rank_update[-4:].strip() + ' ]'
        else:
            rank_update = '[ ' + rank_update + ' ]'
        brand = t.select_one(".item_title > a").get_text().strip()
        name = t.select_one(".list_info > a").get_text().strip()
        href = t.select_one(".list_info > a")['href']
        price = t.select_one(".price").get_text().strip()[-10:].strip()
        like = t.select_one(".txt_cnt_like > span").get_text().strip()
        img = t.select_one("div.li_inner > div.list_img > a > img")['src']
        data.append({'순위': rank + ' ' + rank_update, '사진': img, '브랜드': brand, '제품명': name,    \
                        '가격': price, '좋아요 수': like, '링크': href })
    return data
