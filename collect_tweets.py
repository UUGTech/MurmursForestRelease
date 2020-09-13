import tweet_search
import pandas as pd
import pickle
from datetime import datetime
from tqdm import tqdm
filters = " lang:ja -filter:links -filter:replies -filter:images exclude:retweets"
positive_emoji = " -\"😀\" -\"😁\" -\"😂\" -\"🤣\" -\"😃\" \
                   -\"😄\" -\"😅\" -\"😆\" -\"😉\" -\"😊\" \
                   -\"😋\" -\"😎\" -\"😍\" -\"😘\" -\"🥰\" \
                   -\"😙\" -\"😚\" -\"🙂\" -\"🤩\" -\"🤗\""

negative_emoji = " -\"😫\" -\"😢\" -\"😰\" -\"😱\" -\"😩\" \
                   -\"😤\" -\"😞\" -\"😖\" -\"😟\" -\"😠\" \
                   -\"😡\" -\"🤬\" -\"👎\""

key_emoji = {"😡":0, "😩":0, "😰":0,
             "👍":1, "😘":1, "😆":1}

#---------------------------------------------------------------
# emoji search
#---------------------------------------------------------------
def emoji_search(emoji, label, loop):
    exceptions = [positive_emoji, negative_emoji][label]
    keyword = emoji + filters + exceptions
    df = tweet_search.search(keyword=keyword, loop=loop)
    df = pd.concat([df, pd.DataFrame([label]*len(df), columns=["label"])], axis=1)

    return df


#---------------------------------------------------------------
# main function
#---------------------------------------------------------------
def main():
    df = pd.DataFrame(columns=["time", "tweet", "label"])
    for i, e in enumerate(key_emoji):
        tqdm.write("{}/{}".format(i+1, len(key_emoji)))
        df = pd.concat([df,emoji_search(e, key_emoji[e], 180)], ignore_index=True)
    
    print("Saving tweets data...")
    f = open("tweets_data" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".pkl", "wb")
    pickle.dump(df, f)
    f.close()
    print("Complete!")
    
    return df


if __name__ == "__main__":
    main()