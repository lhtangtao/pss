#!/usr/bin/env python
# encoding: utf-8
import sys

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

reload(sys)
sys.setdefaultencoding('utf-8')
"""
@author: tangtao
@contact: tangtao@lhtangtao.com
@site: http://www.lhtangtao.com
@software: PyCharm
@file: spider_pss.py
@time: 2017/7/21 19:52
"""

from selenium import webdriver
import time
def is_element_exist(driver, xpath):
    """
    输入xpath 判断这个元素存在与否
    :param driver:
    :param xpath:
    :return:
    """
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except NoSuchElementException:
        return False

def open_url():
    driver = webdriver.Chrome()
    driver.get("http://www.pss-system.gov.cn/sipopublicsearch/search-ui/app/searchtools/quote.jsp")
    driver.maximize_window()
    return driver


def key_word(word, driver):
    driver.find_element_by_id("quoteValue").clear()
    driver.find_element_by_id("quoteValue").send_keys(word)


def click_yinzhen(driver):
    driver.find_element_by_id("queryQuoteb").click()


def click_beiyinzhen(driver):
    driver.find_element_by_id("queryQuotedb").click()
    time.sleep(5)


def get_info(driver):
    driver.find_element_by_xpath(".//*[@id='citingLiteratureTable']/table/thead/tr/th[1]/input").click()
    while True:#确保全部选中
        if driver.find_element_by_xpath(".//*[@id='citingLiteratureTable']/table/tbody/tr[1]/td[1]/input").is_selected():
            break
        else:
            driver.find_element_by_xpath(".//*[@id='citingLiteratureTable']/table/thead/tr/th[1]/input").click()
    driver.find_element_by_css_selector("#containerTable2 > div.table-header > div.btn-group > a.btn.btn-view").click() #点击 浏览文献按钮
    driver.switch_to_window(driver.window_handles[1])#切换到当前页
    time.sleep(10)
    driver.find_element_by_xpath("//li[1]/div/span").click() #点击左侧第n条信息
    famin_mingcheng=driver.find_element_by_xpath("//div[@id='tabContent_1_id']/div[2]/table/tbody/tr[3]/td[2]/div").text
    shenqinghao=driver.find_element_by_xpath("//td[2]/div").text
    shenqingri=driver.find_element_by_xpath("//tr[2]/td[2]/div").text
    gongkaihao=driver.find_element_by_xpath("//tr[3]/td[2]/div").text
    gongkairi=driver.find_element_by_xpath("//tr[4]/td[2]/div").text
    ipc=driver.find_element_by_xpath("//tr[5]/td[2]/div").text
    shengqingren=driver.find_element_by_xpath("//tr[6]/td[2]/div").text
    famingren=driver.find_element_by_xpath("//tr[7]/td[2]/div").text
    youxianquanhao=driver.find_element_by_xpath("//tr[8]/td[2]/div").text
    youxianquanri=driver.find_element_by_xpath("//tr[9]/td[2]/div").text
    shenqingrendizhi=driver.find_element_by_xpath("//tr[10]/td[2]/div").text
    driver.close() #关闭爬取到的东西所在的标签页
    print famin_mingcheng
    print shenqinghao
    print shenqingri
    print gongkaihao
    print gongkairi
    print ipc
    print shengqingren
    print famingren
    print youxianquanhao
    print youxianquanri
    print shenqingrendizhi



if __name__ == '__main__':
    src_driver = open_url()
    key_word("CN1283015A", src_driver)
    click_beiyinzhen(src_driver)
    get_info(src_driver)
