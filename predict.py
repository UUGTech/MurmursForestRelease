import tensorflow as tf
import numpy as np
import MeCab
import pickle
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import model_from_json
from constant import *
import preprocess
import gc

#---------------------------------------------------------------
# load model and parameters
#---------------------------------------------------------------
def load_model():
    mode_json_str = open(MODEL_FILE_PATH).read()
    model = model_from_json(mode_json_str)
    model.load_weights(PARAMS_PATH)
    return model

#---------------------------------------------------------------
# predict from tweets
#---------------------------------------------------------------
def predict_tweets(tweets):
    model = load_model()


    input_data = preprocess.tweets_digitization_to_predict(tweets)
    input_data = input_data.astype(np.float32)

    results = model.predict(input_data)
    del tweets
    gc.collect()
    return results


