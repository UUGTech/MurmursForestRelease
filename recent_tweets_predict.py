import tweet_search
import pandas as pd
import predict
import time
import datetime
import sys
import os
import json
from collections import OrderedDict
from constant import *
from database import session
from timedata import *
from sqlalchemy.sql import func, text

#---------------------------------------------------------------
# return proportions of positive tweets and negative tweets of japan
#---------------------------------------------------------------
def predict_negaposi():
    # search tweets written in Japanese
    keyword = "lang:ja -filter:links -filter:replies -filter:images exclude:retweets"
    df = tweet_search.search(keyword=keyword, loop = 50, log=False)

    tweets = df["tweet"].values

    # predict
    results = predict.predict_tweets(tweets)
    
    # calculate proportions
    return calculate_negaposi(results)


#---------------------------------------------------------------
# return proportions of positive tweets and negative tweets of a user
#---------------------------------------------------------------
def predict_user_negaposi(screen_name=" "):
    if screen_name == " ":
        return
    
    df = tweet_search.get_user_timeline(screen_name)
    # if df is error
    if len(df) == 0 or screen_name[1:]=="" or '@' in screen_name[1:]:
        return -1, -1
    tweets = df["tweet"].values

    # predict
    results = predict.predict_tweets(tweets)

    # calculate proportions
    return calculate_negaposi(results)


#---------------------------------------------------------------
# return proportions of positive tweets and negative tweets including a word
#---------------------------------------------------------------
def predict_word_negaposi(word=" "):
    if word == " ":
        return
    
    word = word + " lang:ja -filter:links -filter:replies -filter:images exclude:retweets"
    # search
    df = tweet_search.search(word, loop=2, log=False)
    tweets = df["tweet"].values

    # predict
    results = predict.predict_tweets(tweets)

    # calculate proportions
    return calculate_negaposi(results)
    

#---------------------------------------------------------------
# calculate proportions of positive tweets and negative tweets
#---------------------------------------------------------------
def calculate_negaposi(results):
    pos_p = 0
    neg_p = 0
    for res in results:
        if res[0] >= 0.6:
            pos_p += 1
        if res[0] < 0.3:
            neg_p += 1
    pos_p = (pos_p / len(results)) * 100
    neg_p = (neg_p / len(results)) * 100

    return pos_p, neg_p


#---------------------------------------------------------------
# update DB
#---------------------------------------------------------------
def update_db(now, pos_now, neg_now):
    p_col = "pos"+"{0:02d}".format(now.minute)
    n_col = "neg"+"{0:02d}".format(now.minute)
    now_id = int(now.strftime("%Y%m%d%H"))
    timedata = session.query(TimeData).filter(TimeData.id==now_id).scalar()
    if timedata is None:
        new_timedata = TimeData()
        new_timedata.id = now_id
        new_timedata.__dict__[p_col] = pos_now
        new_timedata.__dict__[n_col] = neg_now
        session.add(new_timedata)
        session.commit()
    else:
        str_sql_pos = "UPDATE negaposi SET " + p_col + " = " + str(pos_now) + "WHERE id = " + str(now_id)
        str_sql_neg = "UPDATE negaposi SET " + n_col + " = " + str(neg_now) + "WHERE id = " + str(now_id)
        update_pos = text(str_sql_pos)
        update_neg = text(str_sql_neg)
        session.execute(update_pos)
        session.execute(update_neg)
        session.commit()
    return


#---------------------------------------------------------------
# return negaposi data used in index.html
#---------------------------------------------------------------
def get_latest_data():
    latest_id = session.query(func.max(TimeData.id).label("latest")).one().latest
    latest_row = session.query(TimeData).filter(TimeData.id==latest_id).one()
    for i in range(12):
        str_minute = "{0:02d}".format(i*5)
        p_col = "pos"+str_minute
        n_col = "neg"+str_minute
        if(latest_row.__dict__[p_col] != 0.0 and latest_row.__dict__[n_col] != 0.0):
            latest_pos = latest_row.__dict__[p_col]
            latest_neg = latest_row.__dict__[n_col]
            str_data_time = str(latest_id) + str_minute
    return str_data_time, latest_pos, latest_neg


def get_24hours_from(start_id):
    sql = "SELECT * FROM negaposi WHERE id >= " + str(start_id) + " ORDER BY id ASC FETCH FIRST 24 ROWS ONLY"
    rows = session.execute(sql)
    res = json.dumps([(dict(row.items())) for row in rows])
    return res
              

def get_7days_from(start_id):
    sql = "SELECT * FROM negaposi WHERE id >= " + str(start_id) + " ORDER BY id ASC FETCH FIRST 168 ROWS ONLY"
    rows = session.execute(sql)
    res = json.dumps([(dict(row.items())) for row in rows])
    return res


#---------------------------------------------------------------
# retun user data used in tree.html
#---------------------------------------------------------------
def get_user_data(user_name):
    pos, neg = predict_user_negaposi(user_name)
    return pos, neg

#---------------------------------------------------------------
# main function
#---------------------------------------------------------------
def main():
    now = datetime.datetime.now()
    try:
        pos, neg = predict_negaposi()
    except:
        pos = 0
        neg = 0
    update_db(now, pos, neg)
    return

if __name__ == "__main__":
    main()


