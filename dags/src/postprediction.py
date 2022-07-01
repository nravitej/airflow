import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from random import randint
from datetime import datetime
import json
import pandas as pd

url='http://127.0.0.1:8000/prediction/'

def process(file, server_url: str):
    m = MultipartEncoder(fields={"file": ("filename", file, "text/json")})
    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
        )
    #print(r.json())
    #print(r.content)
    tab=pd.read_json(r.json())
    print(tab)
    return tab

def fetchdata():
    bulk=pd.read_csv("true_car_listings.csv")
    inference_sample=bulk.sample(n = 100)
    inference_sample.drop(['Price'],axis=1,inplace=True)
    dfjson =inference_sample.to_json(orient='index')
    m=process(dfjson,url)
    return m
    
fetchdata()