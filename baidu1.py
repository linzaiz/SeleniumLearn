from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import pyquery as pq

option = webdriver.ChromeOptions()
option.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
proxy = '111.217.10.40:80'  # 设置代理。这只是个例子，请换成有效的代理 
option.add_argument(f'--proxy-server={proxy}') 
browser = webdriver.Chrome(r"c:\tools\chromedriver.exe", chrome_options=option)
try:
#if 1==1:
    browser.get('https://www.baidu.com')
    input = browser.find_element_by_id('kw')
    input.send_keys('Python')
    input.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
    print(browser.current_url)
    print(browser.get_cookies())
    print(browser.page_source)
    doc = pq(browser.page_source)
    items = doc('.div')

except Exception as e:
    print(e.message())
finally:
    browser. close()
