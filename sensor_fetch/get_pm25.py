import os
from datetime import datetime
import pymongo
from pymongo import MongoClient
import get_pm25_regular


def get_pm25(Location_name):
    db_url = "127.0.0.1:27017"
    db_name = 'bot'
    client = MongoClient(db_url,  27017)
    db = client[ 'bot']
    collect = db['pm25_data']
    
    now_time = datetime.now()
    now_hour = datetime(now_time.year, now_time.month, now_time.day, now_time.hour, 0, 0, 0)
    item = collect.find_one({'PublishTime': {'$eq': now_hour},'County':Location_name})
    
    if item == None :
        time = get_pm25_regular.save_pm25()
        item = collect.find_one({'PublishTime': {'$eq': time},'County':Location_name})
        pm25 = item['PM25']
    elif item['PM25'] == 'ND':
        now_day = datetime(now_time.year, now_time.month, now_time.day, 0, 0, 0, 0)
        item = collect.find_one({'PublishTime': {'$gt': now_day},'County':Location_name})
        pm25 = item['PM25'] 
    else:
        pm25 = item['PM25']
        
    if item == None:
        pm25 = 0.0
    elif item['PM25'] == 'ND':
        pm25 = 0.0
    
    return pm25
    
def get_pm25_station(SiteName):
    db_url = "127.0.0.1:27017"
    db_name = 'bot'
    client = MongoClient(db_url,  27017)
    db = client[ 'bot']
    collect = db['pm25_data']
    
    now_time = datetime.now()
    now_hour = datetime(now_time.year, now_time.month, now_time.day, now_time.hour, 0, 0, 0)
    item = collect.find_one({'PublishTime': {'$eq': now_hour},'SiteName':SiteName})
    
    if item == None :
        time = get_pm25_regular.save_pm25()
        item = collect.find_one({'PublishTime': {'$eq': time},'SiteName':SiteName})
        pm25 = item['PM25']
    elif item['PM25'] == 'ND':
        now_day = datetime(now_time.year, now_time.month, now_time.day, 0, 0, 0, 0)
        item = collect.find_one({'PublishTime': {'$gt': now_day},'SiteName':SiteName})
        pm25 = item['PM25'] 
    else:
        pm25 = item['PM25']
        
    if item == None:
        pm25 = 0.0
    elif item['PM25'] == 'ND':
        pm25 = 0.0
    
    return pm25
    
if __name__ == "__main__":
    pm25 = get_pm25("新竹市")
    print(pm25)
