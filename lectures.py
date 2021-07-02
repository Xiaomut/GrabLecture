#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   lectures.py
@Time    :   2021/04/22 10:02:53
@Author  :   小木 
@Contact :   hunt_hak@outlook.com
'''

import threading
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import tkinter as tk
import tkinter.messagebox 


class GrabLecture(object):

    def __init__(self, name, number, url):

        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')

        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.url = url
        self.name = name
        self.number = number

    def send_message(self):
        self.browser.get(self.url)
        try:
            # name_btn = self.browser.find_element_by_xpath('//div[contains(@class, "input")][1]//input')
            name_btn = WebDriverWait(self.browser, 1, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "input")][1]//input'))
            )
            name_btn.send_keys(self.name)


            # number_btn = self.browser.find_element_by_xpath('//div[contains(@class, "input")][2]//input')
            number_btn = WebDriverWait(self.browser, 1, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "input")][2]//input'))
            )
            number_btn.send_keys(self.number)

            # click_btn = self.browser.find_element_by_xpath('//div[@class="submitWrapper"]//a').click()
            # self.browser.find_element_by_xpath('//div[@class="submitWrapper"]//a').click()
            
            click_btn = WebDriverWait(self.browser, 1, 0.1).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="submitWrapper"]//a'))
            )
            click_btn.click()
        except:
            self.browser.close()
            return False

        return True


class Gui:
    def __init__(self, times=1000):

        self.times = times
        self.start = 1

        self.root = tk.Tk()
        self.root.title('抢讲座专用v1.0 —— 作者: LittleMu')

        self.root.geometry("+700+400")
        # define the two frames
        self.top_frame = tk.Frame(self.root,  width=1280, height=960)
        self.top_frame.grid(column=0, row=0, rowspan=30, padx=20, pady=20)

        self.bottom_frame = tk.Frame(self.root, width=1280, height=960)
        self.bottom_frame.grid(column=0, row=30, rowspan=30, padx=20, pady=20)

        # define the activities
        self.num_label = tk.Label(self.top_frame, text='学号')
        self.num_label.grid(row=0, column=0)
        self.num_entry = tk.Entry(self.top_frame, width=50, textvariable='number')
        self.num_entry.grid(row=1, column=0, padx=8, pady=8, sticky=tk.W)

        self.name_label = tk.Label(self.top_frame, text='姓名')
        self.name_label.grid(row=2, column=0)
        self.name_entry = tk.Entry(self.top_frame, width=50, textvariable='name')
        self.name_entry.grid(row=3, column=0, padx=8, pady=8, sticky=tk.W) 
        
        self.link_label = tk.Label(self.top_frame, text='讲座链接')
        self.link_label.grid(row=4, column=0)
        self.link_entry = tk.Entry(self.top_frame, width=50, textvariable='link')
        self.link_entry.grid(row=5, column=0, padx=8, pady=8, sticky=tk.W)

        # self.scrollBar = tk.Scrollbar(self.root)
        # self.scrollBar.pack(side="right", fill="y")
        # self.scrollBar.config(command=self.edittext.yview)

        self.info_label = tk.Label(self.top_frame, text='输出信息')
        self.info_label.grid(row=6, column=0)
        self.edittext = tk.Text(self.top_frame, width=50, height=10)
        # self.edittext.pack(side="top", fill=BOTH, padx=10, pady=10)
        self.edittext.grid(row=7, column=0)

        self.run_button = tk.Button(self.bottom_frame, text='Start Runing', command=self.spider)
        self.run_button.grid(row=1, column=0, padx=10, pady=8)
        
        # self.root.after(self.times, self._spider)
        self.root.mainloop()

    def _spider(self):
        number = self.num_entry.get().strip()
        name = self.name_entry.get().strip()
        url = self.link_entry.get().strip()
        for i in range(self.times):
            spider = GrabLecture(name=name, number=number, url=url)
            flag = spider.send_message()
            if flag:
                self.edittext.insert(1.0, 'Success!')
                tkinter.messagebox.showinfo(message='Success!')
                return True
            else:
                self._print_info()

    def spider(self):
        t = threading.Thread(target=self._spider, args=())
        t.start()
        # t.join()

    def _print_info(self):
        self.edittext.insert(1.0, f'{self.start}. Runing {self.start}/{self.times} times...\n')
        self.start += 1

    def print_info(self):
        t = threading.Thread(target=self._print_info, args=(self,))
        t.start()
        # t.join()


if __name__ == "__main__":

    gui = Gui()
