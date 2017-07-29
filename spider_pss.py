#!/usr/bin/env python
# encoding: utf-8
import sys

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys

from excel import save_to_excel

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
    # driver = webdriver.Firefox()
    driver.get("http://www.pss-system.gov.cn/sipopublicsearch/search-ui/app/searchtools/quote.jsp")
    driver.maximize_window()
    return driver


def key_word(word, driver):
    driver.find_element_by_id("quoteValue").clear()
    driver.find_element_by_id("quoteValue").send_keys(word)


def click_yinzhen(driver):
    driver.find_element_by_id("queryQuoteb").click()
    while True:
        time.sleep(3)
        if is_element_exist(driver, ".//*[@id='quoteLiteratureTable']/table/tbody/tr[1]/td[2]"):
            time.sleep(1)
            break


def click_beiyinzhen(driver):
    driver.find_element_by_id("queryQuotedb").click()
    while True:
        time.sleep(3)
        if is_element_exist(driver, ".//*[@id='citingLiteratureTable']/table/tbody/tr[1]/td[2]"):
            time.sleep(1)
            break


def record_info(driver, snword):
    """
    记录下所有的新标签页中的信息
    :param driver:
    :param snword:
    :return:
    """
    driver.switch_to_window(driver.window_handles[1])  # 切换到当前页
    while True:  # 此循环的作用是确保能出现有用的数据
        time.sleep(1)
        if is_element_exist(driver, "//tr[2]/td[2]/div"):
            break
    time.sleep(1)
    file_len = len(driver.find_element_by_id('patent_list').find_elements_by_tag_name('li'))
    for i in range(1, file_len):
        if is_element_exist(driver, "//li[" + str(i) + "]/div/span"):
            if i == 6:
                js="document.getElementById('patent_list').setAttribute('style', 'bottom:0');"
                driver.execute_script(js)
            driver.find_element_by_xpath("//li[" + str(i) + "]/div/span").click()  # 点击左侧第n条信息
            while True:
                time.sleep(3)
                if is_element_exist(driver, "//tr[2]/td[2]/div"):
                    break
            time.sleep(1)
            famin_mingcheng = driver.find_element_by_xpath(".//*[@id='patent_list']/li[" + str(i) + "]/div[2]").text
            shenqinghao = driver.find_element_by_xpath("//td[2]/div").text
            shenqingri = driver.find_element_by_xpath("//tr[2]/td[2]/div").text
            gongkaihao = driver.find_element_by_xpath("//tr[3]/td[2]/div").text
            gongkairi = driver.find_element_by_xpath("//tr[4]/td[2]/div").text
            ipc = driver.find_element_by_xpath("//tr[5]/td[2]/div").text
            shengqingren = driver.find_element_by_xpath("//tr[6]/td[2]/div").text
            famingren = driver.find_element_by_xpath("//tr[7]/td[2]/div").text
            youxianquanhao = driver.find_element_by_xpath("//tr[8]/td[2]/div").text
            youxianquanri = driver.find_element_by_xpath("//tr[9]/td[2]/div").text
            info = [snword, famin_mingcheng, shenqinghao, shenqingri, gongkaihao, gongkairi, ipc, shengqingren,
                    famingren,
                    youxianquanhao, youxianquanri]
            if is_element_exist(driver, "//tr[10]/td[2]/div"):
                shenqingrendizhi = driver.find_element_by_xpath("//tr[10]/td[2]/div").text
                info.append(shenqingrendizhi)
            if is_element_exist(driver, "//tr[11]/td[2]/div"):
                youbian = driver.find_element_by_xpath("//tr[11]/td[2]/div").text
                info.append(youbian)
            save_to_excel(info)
    driver.close()  # 关闭爬取到的东西所在的标签页
    driver.switch_to_window(driver.window_handles[0])  # 切换到当前页


def get_info_one_page(driver, sns):
    """
    引证与被引证页面的单个页面全选并且下载
    :param driver:
    :param sns:
    :return:
    """
    while True:
        time.sleep(2)
        if is_element_exist(driver, ".//*[@id='citingLiteratureTable']/table/tbody/tr[1]/td[2]"):
            time.sleep(1)
            break
    driver.find_element_by_xpath(".//*[@id='citingLiteratureTable']/table/thead/tr/th[1]/input").click()  # 点击全选按钮
    while True:  # 确保全部选中
        if driver.find_element_by_xpath(
                ".//*[@id='citingLiteratureTable']/table/tbody/tr[1]/td[1]/input").is_selected():
            break
        else:
            driver.find_element_by_xpath(".//*[@id='citingLiteratureTable']/table/thead/tr/th[1]/input").click()
    driver.find_element_by_css_selector(
        "#containerTable2 > div.table-header > div.btn-group > a.btn.btn-view").click()  # 点击 浏览文献按钮
    record_info(driver, sns)


def get_all_page(driver, sns):
    js = "window.scrollTo(0,document.body.scrollHeight)"
    driver.execute_script(js)
    driver.find_element_by_xpath("//div[3]/div[3]").click()
    page_num = driver.find_element_by_xpath("//div[3]/div[3]").text.replace(" ", "").split(u"共")[1].split(u"条")[
        0]  # 取出一共有多少条
    page_num = int(page_num) / 5 + 1
    get_info_one_page(driver, sns)
    for i in range(2, page_num + 1):
        time.sleep(2)
        # driver.find_element_by_xpath("//div[@id='citingLiteraturePage']/ul/li[" + str(i) + "]/a").click()
        driver.find_element_by_link_text(str(i)).click()
        get_info_one_page(driver, sns)
    driver.quit()


def info_by_sn(sn):
    src_driver = open_url()
    key_word(sn, src_driver)
    click_beiyinzhen(src_driver)
    get_all_page(src_driver, sn)
