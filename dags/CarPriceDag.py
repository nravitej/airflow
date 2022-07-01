from airflow import DAG
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import numpy as np
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from random import randint
from datetime import datetime
from airflow.decorators import dag, task
from pendulum import today
from datetime import datetime
from datetime import timedelta
import json

url='http://127.0.0.1:8000/prediction/'

@dag(
    dag_id="ingest_data",
    description="Ingest data from a file to another DAG",
    tags=["example"],
    default_args={'owner': 'airflow'},
    schedule_interval=timedelta(minutes=1),
    start_date=today().add(hours=-1)
)
def ingest_data():
    @task
    def get_data_to_ingest_from_local_file_task():
        return fetchdata()

    @task
    #Prediction Job
    def save_data_task(data_to_ingest_df):
        process(data_to_ingest_df,url)

    # Task relationships
    data_to_ingest = get_data_to_ingest_from_local_file_task()
    save_data_task(data_to_ingest)


ingest_data_dag = ingest_data()


#####

def process(file, server_url: str):
    m = MultipartEncoder(fields={"file": ("filename", file, "text/json")})
    
    r = requests.post(
        server_url, data=m, headers={"Content-Type": m.content_type}, timeout=8000
        )
    tab=pd.read_json(r.json())
    return tab

def fetchdata():
    bulk=pd.read_csv("true_car_listings.csv")
    #bulk=bulk.iloc[1:,:].copy()
    inference_sample=bulk.sample(n = 100)
    dfjson =inference_sample.to_json(orient='index')
    return dfjson

    


        

        