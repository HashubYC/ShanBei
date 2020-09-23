from selenium import webdriver
import time
import requests
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait


driver = webdriver.Chrome(executable_path="E:/WebDrivers/chromedriver.exe")
driver.maximize_window()  # 窗口最大化
timeout = WebDriverWait(driver, 7)  # 设置等待上限7秒


def get_read_url():
    news_url = "https://www.shanbay.com/api/v2/news/articles/?ipp=10&page=1"
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


def login_in(url):
    driver.get(url)
    time.sleep(2)
    js1 = '''Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) '''
    js2 = '''window.navigator.chrome = { runtime: {},  }; '''
    js3 = '''Object.defineProperty(navigator, 'languages', { get: () => ['en-US', 'en'] }); '''
    js4 = '''Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); '''
    driver.execute_script(js1)
    driver.execute_script(js2)
    driver.execute_script(js3)
    driver.execute_script(js4)
    time.sleep(2)
    try:
        driver.find_element_by_id("input-account").send_keys("15703704272")
        driver.find_element_by_id("input-password").send_keys("19990919")
        time.sleep(2)
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
    # 将页面滚动条拖到底部
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    time.sleep(3)
    print("=====到底了=====")

    try:
        finish = driver.find_element_by_class_name("finish-button")
        for i in range(1, 6):  # 循环放在外面
            time.sleep(50)
            finish.click()
    except:
        pass
    finally:
        driver.find_element_by_class_name("load-more")
        print("已经看过了=_=")


def main():
    read_url_list = get_read_url()
    for url in read_url_list:
        login_in(url)
        check_in()


if __name__ == '__main__':
    main()
