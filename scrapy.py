# -*- coding:utf-8 -*-
import sys
import importlib
import datetime
import time

importlib.reload(sys)
import pymysql
from selenium import webdriver

url = "http://forex.hexun.com/rmbhl/"

# while 1:
driver = webdriver.Firefox()
driver.get(url)
print(driver.current_url)

currName = driver.find_element_by_id("BankNameList").text.replace(u'\xa9', u'')
bankData = driver.find_element_by_id("BankData").text.replace(u'\xa9', u'')

tmpBankDataList = bankData.split("\n")
bankDataList = []
i = 0
while i < len(tmpBankDataList):
    bankDataList.append(tmpBankDataList[i].replace(" ", ","))
    i += 1

tmpCurrNameInfoList = currName.split("/汇卖价\n")
tmpRefRateInfoList = currName.split("/参考价\n")
currNameList = []
currRefRateList = []

now = datetime.datetime.now()
batch_no = now.strftime("%Y%m%d") + str(now.hour * 12 + int(now.minute / 5))

for tmpCurrNameList in tmpCurrNameInfoList:
    tmpCurrNameList1 = tmpCurrNameList.split("/人民币")
    currNameList.append(tmpCurrNameList1[0])
    tmp1 = tmpCurrNameList1[1].split("\n参考价:")
    tmp2 = tmp1[1].split("\n")
    currRefRateList.append(tmp2[0])

driver.quit()

# 持久化
conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='', db='scrapy', charset="utf8")
cursor = conn.cursor()

# conn.set_character_set('utf8')
cursor.execute('SET NAMES utf8;')
cursor.execute('SET CHARACTER SET utf8;')
cursor.execute('SET character_set_connection=utf8;')

for index in range(len(currNameList)):
    if index == 0:
        jIndex = 0
    else:
        jIndex = index * 4

    cnt = 0
    while (((index + 1) * 4) <= len(bankDataList) and cnt < 4):
        if (jIndex + 1) % 4 == 1:
            rate_type = "中间价"
        elif (jIndex + 1) % 4 == 2:
            rate_type = "钞买价"
        elif (jIndex + 1) % 4 == 3:
            rate_type = "汇买价"
        elif (jIndex + 1) % 4 == 0:
            rate_type = "钞/汇卖价"
        sql = 'insert into currency_rate(batch_no, curr_name, ref_rate,bank_rate_list, rate_type, add_time) values ("%s", "%s", "%s", "%s", "%s", now())' \
                % (batch_no, currNameList[index], currRefRateList[index], bankDataList[jIndex], rate_type)

        cursor.execute(sql)
        jIndex = jIndex + 1
        cnt = cnt + 1  # 提交

conn.commit()
# 关闭游标
cursor.close()
# 关闭连接
conn.close()

#  time.sleep(300)
