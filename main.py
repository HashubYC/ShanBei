from selenium import webdriver
import time
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options

# driver = webdriver.Chrome(executable_path="‪E:\\WebDrivers\\chromedriver.exe")

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome('/usr/local/bin/chromedriver', chrome_options=chrome_options)

driver.maximize_window()  # 窗口最大化


def get_read_url():
    news_url = "https://www.shanbay.com/api/v2/news/articles/?ipp=22&page=1"
    start_url = "https://www.shanbay.com/news/articles/"
    response = requests.get(news_url)
    data = response.json()
    objects = data["data"]["objects"]
    read_url_list = []
    for object in objects:
        # print(object["id"])
        read_url = start_url + object["id"]
        print(read_url)
        read_url_list.append(read_url)
    return read_url_list


def login_in(url, account, password):
    driver.get(url)
    time.sleep(10)
    js1 = '''Object.defineProperties(navigator,{ webdriver:{ get: () => false } })'''
    js2 = '''window.navigator.chrome = { runtime: {},  };'''
    js3 = '''Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] });'''
    js4 = '''Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], });'''
    driver.execute_script(js1)
    driver.execute_script(js2)
    driver.execute_script(js3)
    driver.execute_script(js4)
    time.sleep(5)
    try:
        driver.find_element_by_id("input-account").send_keys(account)
        driver.find_element_by_id("input-password").send_keys(password)
        time.sleep(5)
    except:
        # print("不需要登陆===")
        pass
    try:
        slider = driver.find_element_by_xpath("//*[@id='nc_1__scale_text']")
        if slider.is_displayed():
            ActionChains(driver).click_and_hold(on_element=slider).perform()
            ActionChains(driver).move_by_offset(xoffset=280, yoffset=0).perform()
            ActionChains(driver).pause(0.5).release().perform()
            driver.find_element_by_id("button-login").click()
            print("登陆==========")
            time.sleep(5)
    except:
        pass


def check_in():
    looked = 0
    time.sleep(3)
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)  # 将页面滚动条拖到底部
    print("=====到底了=====")

    try:
        finish = driver.find_element_by_class_name("finish-button")
        for i in range(1, 25):  # 循环放在外面
            time.sleep(15)
            finish.click()
    except:
        print("没有找到finish-button")

    try:
        driver.find_element_by_class_name("load-more")
        print("已经看过了=_=")
        looked += 1
    except:
        print("没有找到load-more")

    if looked > 5:
        exit(1)


def main(account, password):
    read_url_list = get_read_url()
    for url in read_url_list:
        login_in(url, account, password)
        check_in()


if __name__ == '__main__':
    account = input()
    password = input()
    main(account, password)
