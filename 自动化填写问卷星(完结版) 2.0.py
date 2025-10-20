# ==========  配置区  ==========
DRIVER_PATH = r"D:\EdgeDriver\edgedriver_win64(1)\msedgedriver.exe"
QUESTION_URL = "https://www.wjx.cn/vm/PKzq0IS.aspx"
SUBMIT_TIMES = 100          # 总份数
LOOP_DELAY = 2              # 每份间隔秒
# ==============================
import random
import time
import traceback
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
# ----------- 浏览器初始化 ----------
def build_driver():
    opt = webdriver.EdgeOptions()
    opt.add_experimental_option("excludeSwitches", ["enable-automation"])
    opt.add_experimental_option('useAutomationExtension', False)
    opt.add_experimental_option("detach", True)
    # 无头可打开下面一行
    # opt.add_argument("--headless")
    ser = Service(DRIVER_PATH)
    driver = webdriver.Edge(service=ser, options=opt)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
    })
    return driver

# ----------- 工具函数 --------------
def safe_click_multi(driver, css, at_least=2):
    """多选题：随机点 2~3 个，不重复点"""
    els = driver.find_elements(By.CSS_SELECTOR, css)
    if not els:
        print(f'警告：未找到 {css}，跳过')
        return
    k = min(random.randint(2, 3), len(els))   # 最多不超过实际选项数
    for el in random.sample(els, k):
        el.click()
def safe_click_random(driver, css):
    """找到元素列表后随机点一个；空列表则跳过"""
    els = driver.find_elements(By.CSS_SELECTOR, css)
    if els:
        random.choice(els).click()
    else:
        print(f'警告：未找到 {css}，跳过')

def renzheng(driver):
    """智能认证按钮"""
    try:
        btn = driver.find_element(By.ID, 'SM_BTN_1')
        if btn.is_displayed():
            btn.click()
            time.sleep(5)
    except Exception:
        pass

# ----------- 单份问卷填写 ----------
def fill_one(driver, idx):
    driver.get(QUESTION_URL)
    time.sleep(1)

    # 1-10 单选
    for div in range(1,11):
        safe_click_random(driver, f'div#div{div} .jqradiowrapper a.jqradio')

    # 11-12 多选
    safe_click_multi(driver, 'div#div11 .jqcheckwrapper a.jqcheck')
    safe_click_multi(driver, 'div#div12 a.jqcheck')

    # 提交
    submit = driver.find_element(By.ID, 'ctlNext')
    driver.execute_script("arguments[0].click();", submit)
    time.sleep(2)
    renzheng(driver)

# ----------- 主循环（单浏览器复用） ----------
def main():
    driver = build_driver()
    try:
        for i in range(1, SUBMIT_TIMES + 1):
            print(f'>>> 第 {i}/{SUBMIT_TIMES} 份')
            try:
                fill_one(driver, i)
                print('    提交成功')
            except Exception as e:
                print('    异常：', traceback.format_exc())
            time.sleep(LOOP_DELAY)
    finally:
        driver.quit()

if __name__ == '__main__':
    main()




'''
#通用模板例子，问卷有单选、多选、填空#
option = webdriver.EdgeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
option.add_experimental_option("detach", True)

service = Service(r"D:\EdgeDriver\edgedriver_win64(1)\msedgedriver.exe")
driver = webdriver.Edge(service=service, options=option)   # ✅ 传 options
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument',
                       {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'})
def is_element_visible(driver, by, value):
    try:
        element = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((by, value))
        )
        return element.is_displayed()
    except:
        return False

def click_if_visible(driver, by, value):
    if is_element_visible(driver, by, value):
        driver.find_element(by, value).click()

def renzheng(driver):
    click_if_visible(driver, By.ID, 'SM_BTN_1')
    time.sleep(5)  # 等待一定时间，确保页面加载完成


def st():
    driver.get('https://www.wjx.cn/vm/PKzq0IS.aspx')#替换你的问卷网址
    sleep(1)
    #下面的代码依照题目结构调整


    """
    #单选案例
    radio_containers1 = driver.find_elements(By.CSS_SELECTOR, 'div#div1 .jqradiowrapper a.jqradio')
    random_radio_element1 = random.choice(radio_containers1)   #这个位置是随机选择一个，你可以根据需求设置概率，视频里会说
    a1=radio_containers1[0]
    b1=radio_containers1[1]

    a1.click()
    b1.click()
    random_radio_element1.click()

    #多选案例
    radio_containers2 = driver.find_elements(By.CSS_SELECTOR, 'div#div2 .jqcheckwrapper a.jqcheck')
    random_radio_element2 = random.choice(radio_containers2)  #这个位置是随机选择一个，你可以根据需求设置概率，视频里会说
    a2=radio_containers2[0]
    a2.click()
    random_radio_element2.click()

    #填空案例
    input_element = driver.find_element(By.ID, "q10")
    input_element.send_keys("输入内容")   #输入想输入的内容
    """
    radio_containers1 = driver.find_elements(By.CSS_SELECTOR, 'div#div1 .jqradiowrapper a.jqradio')
    random_radio_element1 = random.choice(radio_containers1)   #这个位置是随机选择一个，你可以根据需求设置概率，视频里会说
    random_radio_element1.click()

    radio_containers2 = driver.find_elements(By.CSS_SELECTOR, 'div#div2 .jqradiowrapper a.jqradio')
    random_radio_element2 = random.choice(radio_containers2)   #这个位置是随机选择一个，你可以根据需求设置概率，视频里会说
    random_radio_element2.click()

    radio_containers3 = driver.find_elements(By.CSS_SELECTOR, 'div#div3 .jqradiowrapper a.jqradio')
    random_radio_element3 = random.choice(radio_containers3)   #这个位置是随机选择一个，你可以根据需求设置概率，视频里会说
    random_radio_element3.click()

    radio_containers4 = driver.find_elements(By.CSS_SELECTOR, 'div#div4 .jqradiowrapper a.jqradio')
    random_radio_element4 = random.choice(radio_containers4)   #这个位置是随机选择一个，你可以根据需求设置概率，视频里会说
    random_radio_element4.click()

    radio_containers5 = driver.find_elements(By.CSS_SELECTOR, 'div#div5 .jqradiowrapper a.jqradio')
    random_radio_element5 = random.choice(radio_containers5)   #这个位置是随机选择一个，你可以根据需求设置概率，视频里会说
    random_radio_element5.click()

    radio_containers6 = driver.find_elements(By.CSS_SELECTOR, 'div#div6 .jqcheckwrapper a.jqcheck')
    random_radio_element6 = random.choice(radio_containers6)  #这个位置是随机选择一个，你可以根据需求设置概率，视频里会说
    random_radio_element6.click()

    radio_containers7 = driver.find_elements(By.CSS_SELECTOR, 'div#div7 .jqradiowrapper a.jqradio')
    random_radio_element7 = random.choice(radio_containers7)   #这个位置是随机选择一个，你可以根据需求设置概率，视频里会说
    random_radio_element7.click()

    # 使用 ActionChains 模拟点击
    # 提交表单（假设有提交按钮）
    submit_button = driver.find_element(By.ID, 'ctlNext')
    driver.execute_script("arguments[0].click();",submit_button)
    sleep(2)
    renzheng(driver)
    # 关闭浏览器
    #driver.quit()
for i in range(1,101):
    print('>>> 第', i, '份')
    driver = webdriver.Edge(service=service, options=option)  # 新建
    try:
        st()
    except Exception as e:
        print('异常：', e)
    finally:
        driver.quit()
    sleep(2)

'''



'''
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.common.action_chains import ActionChains
import time

# 设置Edge浏览器选项，避免自动化检测
option = webdriver.EdgeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
option.add_experimental_option('useAutomationExtension', False)
option.add_experimental_option("detach", True)
option.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Edge(options=option)
# 隐藏WebDriver的标识
driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
    'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'
})

# 定义一个辅助函数，用于检查元素是否可见
def is_element_visible(driver, by, value):
    try:
        # 使用WebDriverWait等待直到元素可见
        element = WebDriverWait(driver, 3).until(
            EC.visibility_of_element_located((by, value))
        )
        # 返回元素是否可见
        return element.is_displayed()
    except:
        # 如果等待过程中出现异常，返回False
        return False

# 定义一个辅助函数，如果元素可见则点击它
def click_if_visible(driver, by, value):
    if is_element_visible(driver, by, value):
        # 如果元素可见，则点击
        driver.find_element(by, value).click()

# 定义一个辅助函数，用于执行认证过程（如果需要）
def renzheng(driver):
    click_if_visible(driver, By.ID, 'SM_BTN_1') 
    time.sleep(5)   # 等待页面加载完成

# 主函数，用于自动化填写问卷
def st():
    # 打开问卷星问卷页面
    driver.get('https://www.wjx.cn/vm/mqTgqR5.aspx#')  # 替换为你的问卷网址
    sleep(1)
    # 下面的代码根据问卷题目结构调整

    # 示例：随机选择单选题答案
    radio_containers1 = driver.find_elements(By.CSS_SELECTOR, 'div#div1 .jqradiowrapper a.jqradio')
    random_radio_element1 = random.choice(radio_containers1)  # 随机选择一个单选按钮
    random_radio_element1.click()

    # 示例：随机选择多选题答案
    radio_containers2 = driver.find_elements(By.CSS_SELECTOR, 'div#div2 .jqradiowrapper a.jqradio')
    random_radio_element2 = random.choice(radio_containers2)  # 随机选择一个单选按钮
    random_radio_element2.click()

    # 示例：填写文本答案
    input_element = driver.find_element(By.ID, "q10")
    input_element.send_keys("输入内容")  # 输入想输入的内容

    # 提交问卷
    submit_button = driver.find_element(By.ID, 'ctlNext')
    driver.execute_script("arguments[0].click();", submit_button)
    sleep(2)
    renzheng(driver)  # 可能的认证过程

    # 关闭浏览器（如果需要）
    # driver.quit()

# 循环执行填写问卷100次
for i in range(100):
    st()
'''