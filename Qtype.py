import datetime
import random

import time

import numpy
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


def nextPage(driver):
    driver.find_element(By.CSS_SELECTOR, '#divNext').click()
    time.sleep(0.3)


def single(driver, current, p):
    xpath = f'//*[@id="div{current}"]/div[2]/div'
    a = driver.find_elements(By.XPATH, xpath)
    if p == -1:
        r = random.randint(1, len(a))
    else:
        total = sum(p)
        for i in range(len(p)):
            p[i] = p[i] / total
        r = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=p)
    driver.find_element(By.CSS_SELECTOR,
                        f'#div{current} > div.ui-controlgroup > div:nth-child({r})').click()



def multiple(driver, current, probabilities, n=None):
    #机密代码
    pass



def vacant(driver, current, content):
    driver.find_element(By.CSS_SELECTOR, f'#q{current}').send_keys(random.choice(content))


def droplist(driver, current, p):
    # 先点击“请选择”
    driver.find_element(By.CSS_SELECTOR, f"#select2-q{current}-container").click()
    time.sleep(0.5)
    # 选项数量
    options = driver.find_elements(By.XPATH, f"//*[@id='select2-q{current}-results']/li")
    total = sum(p)
    for i in range(len(p)):
        p[i] = p[i] / total
    r = numpy.random.choice(a=numpy.arange(1, len(options)), p=p)
    driver.find_element(By.XPATH, f"//*[@id='select2-q{current}-results']/li[{r + 1}]").click()


def reorder(driver, current):
    xpath = f'//*[@id="div{current}"]/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    for j in range(1, len(a) + 1):
        b = random.randint(j, len(a))
        driver.find_element(By.CSS_SELECTOR, f'#div{current} > ul > li:nth-child({b})').click()
        time.sleep(0.4)


def scale(driver, current, p):
    xpath = f'//*[@id="div{current}"]/div[2]/div/ul/li'
    a = driver.find_elements(By.XPATH, xpath)
    if p == -1:
        b = random.randint(1, len(a))
    else:
        total = sum(p)
        for i in range(len(p)):
            p[i] = p[i] / total
        b = numpy.random.choice(a=numpy.arange(1, len(a) + 1), p=p)
    driver.find_element(By.CSS_SELECTOR,
                        f"#div{current} > div.scale-div > div > ul > li:nth-child({b})").click()


def matrix(driver, current, ps):
    xpath1 = f'//*[@id="divRefTab{current}"]/tbody/tr'
    a = driver.find_elements(By.XPATH, xpath1)
    q_num = 0  # 矩阵的题数量
    for tr in a:
        if tr.get_attribute("rowindex") is not None:
            q_num += 1
    # 选项数量
    xpath2 = f'//*[@id="drv{current}_1"]/td'
    b = driver.find_elements(By.XPATH, xpath2)  # 题的选项数量+1 = 6
    # 遍历每一道小题
    for i in range(1, q_num + 1):
        p = ps[i - 1]  # 获取当前小题概率参数
        if p == -1:
            opt = random.randint(2, len(b))
        else:
            total = sum(p)
            for j in range(len(p)):
                p[j] = p[j] / total
            opt = numpy.random.choice(a=numpy.arange(2, len(b) + 1), p=p)
        driver.find_element(By.CSS_SELECTOR, f'#drv{current}_{i} > td:nth-child({opt})').click()


# average, variance表示均值和方差
def slide(driver, current, average, variance):
    samples = numpy.random.normal(average, variance, 1)  # 正态随机数
    target = numpy.maximum(0, numpy.round(samples)).astype(int)  # 转非负整
    driver.find_element(By.CSS_SELECTOR, f'#q{current}').send_keys(str(target))


def submit(driver):
    driver.find_element(By.XPATH, '//*[@id="ctlNext"]').click()
    try:
        intell = WebDriverWait(driver, 4).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="layui-layer1"]/div[3]/a')))
        intell.click()
    except:
        pass
    xpath_dict = {'//*[@id="layui-layer2"]/div[3]/a': 1,
                  '//*[@id="SM_BTN_1"]': 3}
    for xpath, delay in xpath_dict.items():
        try:
            element = driver.find_element(By.XPATH, xpath)
            element.click()
            time.sleep(delay)
        except NoSuchElementException:
            pass
    # 滑块验证
    try:
        slider = driver.find_element(By.XPATH, '//*[@id="nc_1__scale_text"]/span')
        if str(slider.text).startswith("请按住滑块"):
            width = slider.size.get('width')
            ActionChains(driver).drag_and_drop_by_offset(slider, width, 0).perform()
    except:
        pass


def shift(driver, a, b):
    # 机密代码
    pass 
