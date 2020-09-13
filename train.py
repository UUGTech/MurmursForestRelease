import sys
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.model_selection import train_test_split
from constant import *
import preprocess


def main(pklname):
    #---------------------------------------------------------------
    # load data
    #---------------------------------------------------------------
    tweets, labels, vocab_size = preprocess.load_data_with_labels(pklname)
    x_train, x_test, y_train, y_test = train_test_split(tweets, labels, train_size=0.8)

    #---------------------------------------------------------------
    # buid model
    #---------------------------------------------------------------
    embedding_dim = 64
    model = keras.Sequential([
        layers.Embedding(vocab_size, embedding_dim, input_length=MAX_LENGTH_OF_TWEETS),
        layers.Dense(16, activation="relu"),
        layers.GlobalAveragePooling1D(),
        layers.Dense(1, activation="sigmoid")
    ])

    #---------------------------------------------------------------
    # compile and train model
    #---------------------------------------------------------------
    model.compile(optimizer="adam", loss="binary_crossentropy", metrics=["accuracy"])
    print(model.summary())

    batch_size = 1024
    epochs = 15
    history = model.fit(x_train,
                        y_train,
                        validation_data=(x_test, y_test),
                        batch_size=batch_size,
                        epochs=epochs)

    #---------------------------------------------------------------
    # save model and parameters
    #---------------------------------------------------------------
    model_json_str = model.to_json()
    open(MODEL_FILE_PATH, "w").write(model_json_str)
    model.save_weights(PARAMS_PATH)


if __name__ == "__main__":
    args = sys.argv
    pklname = args[1]
    main(pklname)