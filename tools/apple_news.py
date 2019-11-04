# -*- coding: utf-8 -*-
import requests
import re
import os
import random
from bs4 import BeautifulSoup
from flask import Flask, request, abort
#from imgurpython import ImgurClient
from argparse import ArgumentParser

def apple_newss():

    target_url = 'http://www.appledaily.com.tw/realtimenews/section/new/'
    print('Start parsing appleNews....')
    rs = requests.session()
    res = rs.get(target_url, verify=True)
    soup = BeautifulSoup(res.text, 'html.parser')

    list_links = [] # Create empty list

    for a in soup.select("div[class='abdominis rlby clearmen']")[0].findAll(href=True): # find links based on div
            if a['href']!= None and a['href'].startswith('https://'):
                    list_links.append(a['href']) #append to the list
                    print(a['href']) #Check links

#for l in list_links: # print list to screen (2nd check)
#    print(l)


    print("\n")

    random_list = [] #create random list if needed..
    random.shuffle(list_links) #random shuffle the list
    apple_newss_content0 = ''
    apple_newss_content1 = ''
    apple_newss_content2 = ''
    for i in range(3): # specify range (5 items in this instance)
        res = list_links.pop(random.randint(1, len(list_links)-1)) # pop of each item randomly based on the size of the list
        random_list.append(res)
    #print(res)
    #print(random_list)
    print("\n")
    apple_newss_content0=random_list[0]
    apple_newss_content1=random_list[1]
    apple_newss_content2=random_list[2]
    
    print(apple_newss_content0)
    print(apple_newss_content1)
    print(apple_newss_content2)
    
    return apple_newss_content0, apple_newss_content1, apple_newss_content2
