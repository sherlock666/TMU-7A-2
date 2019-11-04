import requests
import re
import os
import random
from bs4 import BeautifulSoup
from flask import Flask, request, abort
#from imgurpython import ImgurClient
from argparse import ArgumentParser
import pandas as pd

def exchange_rates(L):

    res = requests.get("http://rate.bot.com.tw/xrt?Lang=zh-TW")
    soup = BeautifulSoup(res.text,'html.parser')

    ratecash=pd.Series()
    ratespot=pd.Series()

    for i in soup.select("td[data-table='本行現金賣出']"):
        ratecash = ratecash.append(pd.Series([i][0].string)).reset_index(drop=True)  
    for i in soup.select("td[data-table='本行即期賣出']"):
        ratespot = ratespot.append(pd.Series([i][0].string)).reset_index(drop=True) 
    
    df=pd.DataFrame({'ratecash':ratecash,'ratespot':ratespot})

   
    Country=L

    content="現金匯率為 : "+df.at[Country,'ratecash']+"\n"+"即期匯率為 : "+df.at[Country,'ratespot']
    #content_ratecash=df.at[Country,'ratecash']
    #content_ratespot=df.at[Country,'ratespot']

    #print(content)


    return content
