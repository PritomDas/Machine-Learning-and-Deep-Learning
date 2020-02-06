import re, sys
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words('english'))

class kmeans_cluster_algo:
    def __init__(self, k_value, tweets, seeds, output):
        self.k_value = k_value
        self.tweets = tweets
        self.seeds = seeds
        self.output = output
        self.centroid = {}
        self.clusters = {}
        self.id_to_index_clusters = {}
        self.id_clusters = {}
        self.id_to_index_cluster = {}
        self.jaccardian_matrix = {}
        self.initial_clusters()
        self.initial_matrix()

    def initial_clusters(self):
        for ID in self.tweets:
            self.id_to_index_clusters[ID.id] = -1

        for k in range(self.k_value):
            self.clusters[k] = set([self.seeds[k]])
            self.id_to_index_clusters[self.seeds[k]] = k

    def JaccardianDistance(self, tweetID_x, tweetID_y):
        X = set(tweetID_x.word)
        Y = set(tweetID_y.word)
        try:
            return 1 - float(len(X.intersection(Y))) \
                       / float(len(X.union(Y)))
        except ZeroDivisionError:
            return 1
        
    def initial_clusters(self):
        for ID in self.tweets:
            self.id_to_index_clusters[ID.id] = -1

        for k in range(self.k_value):
            self.clusters[k] = set([self.seeds[k]])
            self.id_to_index_clusters[self.seeds[k]] = k

    def initial_matrix(self):
        for tweetID_x in self.tweets:
            self.jaccardian_matrix[tweetID_x.id] = {}
            for tweetID_y in self.tweets:
                if tweetID_y.id not in self.jaccardian_matrix:
                    self.jaccardian_matrix[tweetID_y.id] = {}
                distance = self.JaccardianDistance(tweetID_x, tweetID_y)
                self.jaccardian_matrix[tweetID_x.id][tweetID_y.id] = distance
                self.jaccardian_matrix[tweetID_y.id][tweetID_x.id] = distance

    def create_clusters(self):
        for k in range(self.k_value):
            self.id_clusters[k] = set()

        for tweetID_x in self.tweets:
            min_dist = sys.float_info.max
            min_cluster = self.id_to_index_clusters[tweetID_x.id]

            for k in self.clusters:
                dist = 0.0
                seed_count = 0
                for tweetID_y in self.clusters[k]:
                    dist += self.jaccardian_matrix[tweetID_x.id][int(tweetID_y)]
                    seed_count += 1
                if seed_count > 0:
                    avg_dist = dist / float(seed_count)
                    if min_dist > avg_dist:
                        min_dist = avg_dist
                        min_cluster = k
            self.id_clusters[min_cluster].add(tweetID_x.id)
            self.id_to_index_cluster[tweetID_x.id] = min_cluster

        for k in self.id_clusters:
            num_id = len(self.id_clusters[k])
            if num_id != 0:
                min_dist = sys.float_info.max
                centroid_temp = self.id_clusters[k]

                for tweetID_x in self.id_clusters[k]:
                    dist_sum = 0.0
                    for tweetID_y in self.id_clusters[k]:
                        if tweetID_y != tweetID_y:
                            dist_sum += self.jaccardian_matrix[tweetID_x][tweetID_y]
                    if dist_sum < min_dist:
                        min_dist = dist_sum
                        centroid_temp = tweetID_x
                self.centroid[k] = centroid_temp

        report = open(self.output, 'w')
        self.put_results(report)

        sse = self.get_SSE()
        report.write("\nsum of squared error : %f\n"  % sse)

        report.close()

    def put_results(self, res_output=None):
        cluster_index = 1
        clusters_id = []
        for k in range(self.k_value):
            for cluster in self.id_clusters[k]:
                clusters_id.append(cluster)
            res_output.write(str(cluster_index) + "\n")
            res_output.write(str(clusters_id) + "\n")
            res_output.write("size = " + str(len(clusters_id)) + "\n\n")
            clusters_id = []
            cluster_index += 1

    def get_SSE(self):
        SSE = 0.0
        for k in range(self.k_value):
            for ID in self.id_clusters[k]:
                SSE += ((self.jaccardian_matrix[self.centroid[k]][ID])**2)/100
        return SSE

class format_tweet:
    def __init__(self, tweet_id, tweet_text):
        self.id = tweet_id
        self.text = tweet_text
        self.word = self.text.split()
    def __repr__(self):
        return str(self.id) + ":" + self.text

def process_tweet(file):
    dataset = []
    for entry in open(file, encoding="utf-8").read().split("\n")[:-1]:
        tweet = entry[50:].lower()
        tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet)
        tweet = re.sub('^(RT @.+?: )+', '', tweet)
        tweet = re.sub('#\w+', '', tweet)
        tweet = re.sub('@\w+', '', tweet)
        tweet = re.sub("[^\w ]", ' ', tweet)

        tweet = " ".join([word for word in word_tokenize(tweet) if not word in stop_words] )

        dataset.append(format_tweet(int(entry[:18]), tweet))

    return dataset

if __name__ == "__main__":
    #change the value of K as needed, it stands for the number of clusters
    K = 30
    #enter the directory path address of the dummycentroids.txt file
    dummy_centroids = "C:\\Users\\91917\\Desktop\\Thanks GOD Again\\dummycentroids.txt"
    #enter the directory path address of the dataset bbchealth.txt
    input_tweet_file = "C:\\Users\\91917\\Desktop\\Thanks GOD Again\\bbchealth.txt"
    #enter the driectory path address to save the output file as desired
    result_file = "C:\\Users\\91917\\Desktop\\Thanks GOD Again\\k_means_results.txt"

    cleaned_tweets = process_tweet(input_tweet_file)
    seeds = []
    f = open(dummy_centroids, 'r')
    for ID in open(initial_centroids, encoding="utf-8").read().split("\n")[:-1]:
        ID = re.sub('[\s,]+', '', ID)
        seeds.append(ID)
    f.close()
    kmeans_final = kmeans_cluster_algo(K,cleaned_tweets, seeds, result_file)
    kmeans_final.create_clusters()
