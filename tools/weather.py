# -*- coding: utf-8 -*-
import requests
import re
import os
import random
from bs4 import BeautifulSoup
from flask import Flask, request, abort
#from imgurpython import ImgurClient
from argparse import ArgumentParser
import pandas as pd



def weather(L):
    url="http://opendata.cwb.gov.tw/govdownload?dataid=F-C0032-001&authorizationkey=rdec-key-123-45678-011121314"
    res = requests.get(url) 
    soup = BeautifulSoup(res.text,'xml')
    LocationNames = pd.Series()
    Weathers1 = pd.Series()
    Weathers2 = pd.Series()
    Weathers3 = pd.Series()
    MaxT1 = pd.Series()
    MaxT2 = pd.Series()
    MaxT3 = pd.Series()
    MinT1 = pd.Series()
    MinT2 = pd.Series()
    MinT3 = pd.Series()
    Feel1 = pd.Series()
    Feel2 = pd.Series()
    Feel3 = pd.Series()



    for i in soup.select("locationName"):
        LocationNames = LocationNames.append(pd.Series([i][0].string)).reset_index(drop=True)  
    
    for i in soup.select("parameterName")[::15]:
        Weathers1 = Weathers1.append(pd.Series([i][0].string)).reset_index(drop=True) 
    for i in soup.select("parameterName")[1::15]:
        Weathers2 = Weathers2.append(pd.Series([i][0].string)).reset_index(drop=True) 
    for i in soup.select("parameterName")[2::15]:
        Weathers3 = Weathers3.append(pd.Series([i][0].string)).reset_index(drop=True) 
    
    for i in soup.select("parameterName")[3::15]:
        MaxT1 = MaxT1.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("parameterName")[4::15]:
        MaxT2 = MaxT2.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("parameterName")[5::15]:
        MaxT3 = MaxT3.append(pd.Series([i][0].string)).reset_index(drop=True)
    
    for i in soup.select("parameterName")[6::15]:
        MinT1 = MinT1.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("parameterName")[7::15]:
        MinT2 = MinT2.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("parameterName")[8::15]:
        MinT3 = MinT3.append(pd.Series([i][0].string)).reset_index(drop=True)

    for i in soup.select("parameterName")[9::15]:
        Feel1 = Feel1.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("parameterName")[10::15]:
        Feel2 = Feel2.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("parameterName")[11::15]:
        Feel3 = Feel3.append(pd.Series([i][0].string)).reset_index(drop=True)
    
    startTime1 =pd.Series()
    startTime2 =pd.Series()
    startTime3 =pd.Series()
    endTime1 =pd.Series()
    endTime2 =pd.Series()
    endTime3 =pd.Series()

    for i in soup.select("startTime")[0:65:3]:
        startTime1 = startTime1.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("startTime")[1:66:3]:
        startTime2 = startTime2.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("startTime")[2:67:3]:
        startTime3 = startTime3.append(pd.Series([i][0].string)).reset_index(drop=True)
    
    for i in soup.select("endTime")[0:65:3]:
        endTime1 = endTime1.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("endTime")[1:66:3]:
        endTime2 = endTime2.append(pd.Series([i][0].string)).reset_index(drop=True)
    for i in soup.select("endTime")[2:67:3]:
        endTime3 = endTime3.append(pd.Series([i][0].string)).reset_index(drop=True)

    df = pd.DataFrame({'city':LocationNames,'12st':startTime1,'12et':endTime1,'12pr':Weathers1,'12ht':MaxT1,'12lt':MinT1,'12feel':Feel1,'24st':startTime2,'24et':endTime2,'24pr':Weathers2,'24ht':MaxT2,'24lt':MinT2,'24feel':Feel2,'36st':startTime3,'36et':endTime3,'36pr':Weathers3,'36ht':MaxT3,'36lt':MinT3,'36feel':Feel3})
    #df[['city','12st','12et','12pr','12ht','12lt','12feel','24st','24et','24pr','24ht','24lt','24feel','36st','36et','36pr','36ht','36lt','36feel']]




    Location=L
    st12=df.at[Location,'12st'].replace("T"," ").replace("+08:00"," ")
    et12=df.at[Location,'12et'].replace("T"," ").replace("+08:00"," ")

    st24=df.at[Location,'24st'].replace("T"," ").replace("+08:00"," ")
    et24=df.at[Location,'24et'].replace("T"," ").replace("+08:00"," ")

    st36=df.at[Location,'36st'].replace("T"," ").replace("+08:00"," ")
    et36=df.at[Location,'36et'].replace("T"," ").replace("+08:00"," ")

    contentl=("36小時內 "+df.at[Location,'city']+" 天氣預報\n")

    content12=(st12+" ~ \n"+et12
             +"\n天氣狀況: "+df.at[Location,'12pr']
             +"\n最高溫: "+df.at[Location,'12ht']+"℃"+"  最低溫: "+df.at[Location,'12lt']+"℃"+"\n體感指標: "
             +df.at[Location,'12feel'])

    content24=(st24+" ~ \n"+et24
             +"\n天氣狀況: "+df.at[Location,'24pr']
             +"\n最高溫: "+df.at[Location,'24ht']+"℃"+"  最低溫: "+df.at[Location,'24lt']+"℃"+"\n體感指標: "
             +df.at[Location,'24feel'])

    content36=(st36+" ~ \n"+et36
             +"\n天氣狀況: "+df.at[Location,'36pr']
             +"\n最高溫: "+df.at[Location,'36ht']+"℃"+"  最低溫: "+df.at[Location,'36lt']+"℃"+"\n體感指標: "
             +df.at[Location,'36feel'])

    weather_content=(contentl+"\n"+content12+"\n\n"+content24+"\n\n"+content36)

    return weather_content