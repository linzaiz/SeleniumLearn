# Learn https://blog.csdn.net/whjkm/article/details/81056650 Thanks!
import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
# from config import *

KEYWORD = 'Python'

"""
import pymongo

MONGO_URL = 'localhost'
MONGO_DB = 'taobao'
MONGO_TABLE = 'product'

client = pymongo.MongoClient(MONGO_URL)   # 创建一个连接对象 
db = client[MONGO_DB]
"""
# browser = webdriver.Chrome()

# Chrome Headless模式
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless')  # 加入headless则会报告登录错误（需先登录？）； 即便不加，也会在“submit.click()”那一步要求登录！

# browser = webdriver.Chrome(chrome_options=chrome_options)
# Proxy and path
chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
proxy = '10.217.10.40:80'  # 设置代理。这只是个例子，请换成有效的代理 
chrome_options.add_argument(f'--proxy-server={proxy}') 
browser = webdriver.Chrome(r"c:\tools\chromedriver.exe", chrome_options=chrome_options)

wait = WebDriverWait(browser, 10)


# 搜索索引页面，用selenium控制自动搜索
def search():
    if 1 == 1:
    #try:
        browser.get('https://www.taobao.com')
        # 等待元素信息加载完成
        submit = wait.until(EC.element_to_be_clickable( (By.CSS_SELECTOR, '.user-nick > a') ))
        submit.click()
        time.sleep(1)
        browser.switch_to_window(browser.window_handles[-1])
        #login_input = wait.until(EC.presence_of_element_located( (By.CSS_SELECTOR, 'input[name="fm-login-id"') ))
        login_input = wait.until(EC.presence_of_element_located( (By.CSS_SELECTOR, 'div.fm-field > div.input-plain-wrap.input-wrap-loginid > input') ))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.fm-button.fm-submit.password-login')))  # 这种空格隔开的多属性也可以用其中一部分定位或属性定位：button[class="fm-button fm-submit password-login"]
        input_input.send_keys('lozoo')
        pwd_input = wait.until(EC.presence_of_element_located( (By.CSS_SELECTOR, 'input[name="fm-login-password"') ))
        # ################################ ！！！！！！！！！！！！！！！Change before upload to HUB ！！！！！！！！！！
        input_input.send_keys('PASSWORD!!!')  ############################################### !!!!!!!!!!!!!!!!!!!!!!!!!!! ！！！！！！
        submit.click()
        browser.


        # 等待元素信息加载完成
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mq')))  # #q
        #submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        submit = wait.until(EC.element_to_be_clickable( (By.CSS_SELECTOR, 'input[type="submit"]') ))
        input.send_keys(KEYWORD)   # 传入需要搜索的关键词
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total')))
        get_products()
        return total.text
        # except TimeoutException:
        #   return search()

# 跳转到下一个页面
def next_page(page_number):
    try:
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')))
        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)))
        get_products()
    except TimeoutException:
        next_page(page_number)

# 解析商品页
def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source      # 获取页面的源代码
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text().replace('\n', ''),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

# 保存到数据库
def save_to_mongo(result):
    """
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功', result)
    except Exception:
        print('存储到MONGODB失败', result)
    """
    print(result)


def main():
    #try:
        total = search()
        # 通过正则表达式提取页面的总页数
        total = int(re.compile('(\d+)').search(total).group(1))
        # print(total)
        # 遍历所有页面
        for i in range(2, total+1):
            next_page(i)
    #except Exception as e:
    #    print("出错啦! 出错信息：", e.message)
    #finally:
    #    browser.close()

if __name__ == "__main__":
    main()
