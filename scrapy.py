# -*- coding:utf-8 -*-
import sys
import importlib
importlib.reload(sys)
import re
from lxml import etree
import requests
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#header = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; .NET4.0E)'}
#url="http://bi.jr.tuniu.org" 
url="http://forex.hexun.com/rmbhl/"
#url="http://www.boc.cn/sourcedb/whpj/index.html"  
#html=requests.get(url).content.decode("utf8")  
#html=requests.get(url, headers=header).content.decode("gbk")

#driver = webdriver.PhantomJS(executable_path='C:/Users/zhangxun/scrapy/phantomjs-1.9.7-windows/phantomjs.exe')
driver = webdriver.Firefox()
driver.get(url)
#print ("get content:")
print (driver.current_url)
#print (driver.body)
#print (driver.find_element_by_xpath('//table[@cellpadeleniuming="0"]/tr[8]/td/text()'))



#try:
#    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID,"DefaultMain")))
#finally:
#    driver.quit()
#try:
#    element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//*[@id='BankData']")))
#finally:
#    driver.quit()
    

#.replace(u'\xa9', u''))

#bankData = driver.find_elements_by_xpath("/body/BankData")
#print (bankData)
 
bankNameList = driver.find_elements_by_xpath('//table[@id="BankNameList"]/tbody/td')
print (bankNameList.text)

#print (element.text.replace(u'\xa9', u''))


driver.quit()

#print html.status_code
#print (html)




