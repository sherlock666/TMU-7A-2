# -*- coding: utf-8 -*-
import requests
import re
import os
import random
from bs4 import BeautifulSoup


def yande_res(num):
    #num=random.randint(100000,500000)
    ## 目前限制100000 (之前的常常有砍圖會導致爬蟲錯誤) ~ 500000 (目前更新最新是這數字，正常每天都會增加)
    print(num)
    target_url = 'https://yande.re/post/show/'+str(num)
    print('Start parsing yande.re....')
    rs = requests.session()
    res = rs.get(target_url, verify=True)
    soup = BeautifulSoup(res.text, 'html.parser')
    
    
    #list_links = [] # Create empty list
    
    #for a in soup.select("div[class='note-container']")[0].findAll(href=True): # find links based on div
    #        if a['href']!= None and a['href'].startswith('https://'):
    #                #list_links.append(a['href']) #append to the list
    #                print(a['href']) #Check links
                    
    yande_link = soup.select("div[id='content']")[0].find('img').get('src')
    return yande_link

