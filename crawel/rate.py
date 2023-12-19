import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# 查價
chrome = ""


def get_middle_rate():
    datas = []
    try:
        global chrome
        chrome = webdriver.Chrome(service=Service(r"C:\webdriver\chromedriver.exe"))
        chrome.get("https://rate.bot.com.tw/xrt?Lang=zh-TW")
        chrome.maximize_window()
        time.sleep(5)
        chrome.find_element(
            by=By.XPATH, value="/html/body/div[1]/main/div[4]/div/p[1]/a[1]"
        ).click()
        time.sleep(5)
        soup = BeautifulSoup(chrome.page_source, "lxml")
        for tr in soup.find("tbody").find_all("tr"):
            data = []
            for i, td in enumerate(tr.find_all("td")[:5]):
                if i == 0:
                    data.append(
                        td.find(
                            "div", class_="hidden-phone print_show xrt-cur-indent"
                        ).text.strip()
                    )
                else:
                    data.append(td.text.strip())
            if data != []:
                datas.append([data[0], data[3], data[4]])
                datas = [[0 if value == "-" else value for value in i] for i in datas]
                # 把字串轉成浮點數
                datas = [
                    [
                        float(x)
                        if isinstance(x, str) and x.replace(".", "", 1).isdigit()
                        else x
                        for x in row
                    ]
                    for row in datas
                ]
                # 計算每個幣別的平均值
                averages = [round((row[1] + row[2]) / 2, 5) for row in datas]
                # 將平均值附加在各自的第三個位置
                result_data = [row + [avg] for row, avg in zip(datas, averages)]

    except Exception as e:
        print(e)

    return result_data


if __name__ == "__main__":
    result_data = get_middle_rate()
    print(result_data)
