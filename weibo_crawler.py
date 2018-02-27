#!/usr/bin/path python3
# encoding:utf-8
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from configparser import ConfigParser
import time

weibo_url = "https://weibo.com"
class WeiboCrawler():
    def __init__(self, file_="config.private"):
        with open(file_) as f:
            cfg = ConfigParser()
            cfg.read(file_)
            self.account = cfg.get('account', 'account')
            self.passwd = cfg.get('account', 'passwd')
        self.cookie = None
        self.driver = webdriver.Chrome("./chromedriver")
        self.driver.maximize_window()

    def login(self):
        self.driver.get(weibo_url)
        self.wait_find_element(By.ID, "loginname").send_keys(self.account)
        self.wait_find_element(By.NAME, "password").send_keys(self.passwd)
        self.wait_find_element(By.XPATH, "//a[@node-type='submitBtn']").click()
        self.cookie = self.driver.get_cookies()
        for x in range(len(self.cookie)):
            print(self.cookie[x])

    def star(self):
        #zhangluyi = "https://weibo.com/u/1905283013"
        #handle = self.driver.current_window_handle
        self.wait_find_element(By.XPATH, "//a/strong[@node-type='follow']").click()
        self.wait_find_element(By.XPATH, "//a[@usercard='id=1905283013']").click()
        all_handles = self.driver.window_handles
        #print(all_handles)
        self.driver.switch_to_window(all_handles[-1])
        self.wait_find_element(By.XPATH, "//*[@id='Pl_Core_T8CustomTriColumn__3']/div/div/div/table/tbody/tr/td[2]/a/span").click()
        
    def wait_find_element(self, type_, value):
        element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((type_, value)))
        return element

if __name__ == "__main__":
    wbc = WeiboCrawler()
    wbc.login()
    wbc.star()
