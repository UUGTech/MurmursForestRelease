import json
import pandas as pd
from time import sleep
from requests_oauthlib import OAuth1Session
from datetime import datetime
from tqdm import tqdm
from api_keys import *      # need api_keys.py including API keys

#---------------------------------------------------------------
# API keys
#---------------------------------------------------------------
Consumer_key = CONSUMER_KEY
Consumer_secret = CONSUMER_SECRET
Access_token = ACCESS_TOKEN
Access_secret = ACCESS_SECRET
twitter = OAuth1Session(Consumer_key, Consumer_secret, Access_token, Access_secret)


#---------------------------------------------------------------
# search function
#---------------------------------------------------------------
def search(keyword = " ", count = 100, loop = 200, log=True):
    cnt=0
    max_id = -1
    url = "https://api.twitter.com/1.1/search/tweets.json"
    columns = ["time", "tweet"]
    df = pd.DataFrame(columns = columns)
    
    if keyword == " ":
        return df
    
    params = {"q" : keyword, "count" : count, "max_id" : max_id}
    if log:
        bar = tqdm(total = loop)
    while True:
        # loop_check
        if cnt >= loop:
            break

        # max_id for the next request
        if max_id != -1:
            params["max_id"] = max_id - 1
        
        # make a request
        req = twitter.get(url, params = params)

        # if the request is accepted
        if req.status_code == 200:
            timeline = json.loads(req.text)

            if timeline["statuses"] == []:
                if log:
                    tqdm.write("no more tweets")
                break

            for tweet in timeline["statuses"]:
                text = tweet["text"]
                time = tweet["created_at"]
                
                df = df.append(pd.DataFrame([[time, text]], columns=columns), ignore_index=True)
            
            max_id = timeline["statuses"][-1]["id"]
            # count
            cnt+=1
            if log:
                bar.update(1)
        
        # wait for 15 min if the request is rejected
        else:
            print("Wait for 15minutes from: " +  datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            sleep(60*15+30)

    twitter.close()
    return df

#---------------------------------------------------------------
# this function gets user timeline
#---------------------------------------------------------------
def get_user_timeline(screen_name=" ", count=200):
    columns = ["time", "tweet"]
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    df = pd.DataFrame(columns = columns)
    if screen_name == " ":
        return df

    params = {"screen_name" : screen_name, "count" : count, "include_rts" : False}
    
    # make a request
    req = twitter.get(url, params = params)

    # if the request is accepted
    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in timeline:
            if(tweet["lang"] != "ja"):
                continue
            text = tweet["text"]
            time = tweet["created_at"]

            df = df.append(pd.DataFrame([[time, text]], columns=columns), ignore_index=True)
        
    # wait for 15 min if the request is rejected
    else:
        return df
        sleep(60*15+30)
    
    twitter.close()
    return df


