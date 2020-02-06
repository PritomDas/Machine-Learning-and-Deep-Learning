import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def JaccardianDistance(x, y):
    intersection = len(list(set(x).intersection(y)))
    union = (len(x) + len(y)) - intersection
    if union == 0: return 1
    return float(intersection) / float(union)


def process_tweet(file):
    tweetID_dictionary = {}
    for entry in open(file, encoding="utf-8").read().split("\n")[:-1]:
        tweet_id = entry[0:18]
        tweet = entry[50:].lower()
        tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet)
        tweet = re.sub('^(RT @.+?: )+', '', tweet)
        tweet = re.sub('#\w+', '', tweet)
        tweet = re.sub('@\w+', '', tweet)
        tweet = re.sub("[^\w ]", ' ', tweet)
        tokens = [word for word in word_tokenize(tweet) if not word in stop_words]
        tweetID_dictionary[tweet_id] = tokens

    return tweetID_dictionary


def get_n_centroids(n, tweetID_dictionary, output):
    x = open(output, "w", encoding="utf-8")
    tweet_id, mean_distance = [], []
    for count, key in enumerate(tweetID_dictionary.keys()):
        print((count + 1)/(len(tweetID_dictionary)) * 100)
        tweet_id.append(key)
        distance = []
        for comp_key in tweetID_dictionary.keys():
            if key == comp_key:
                continue
            distance.append(JaccardianDistance(tweetID_dictionary[key], tweetID_dictionary[comp_key]))
        mean_distance.append(sum(distance)/len(distance))
    mean_distance, tweet_id = zip(*sorted(zip(mean_distance, tweet_id), reverse=True))
    for index in range(n):
        x.write(str(tweet_id[index]))
        if index != n - 1:
            x.write(",\n")
    x.close()
    return


number_of_centroids = 100
#please enter the directory address of the dataset below
tweetID_dictionary = process_tweet("C:\\Users\\91917\\Desktop\\Thanks GOD Again\\bbchealth.txt")
#please enter the directory address where the file containing initial centroids is saved
get_n_centroids(number_of_centroids, tweetID_dictionary, "C:\\Users\\91917\\Desktop\\Thanks GOD Again\\dummycentroids.txt")