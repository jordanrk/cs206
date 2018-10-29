import pickle, pandas

def main():
	createMaps()

def createMaps():
	df = pandas.read_csv('new_ira.csv')
	tweet_to_total_retweet_count = {}
	tweet_to_bot_retweet_count = {}

	for index, row in df.iterrows():
		retweet_count = row['retweet_count']
		if (retweet_count == 0):
			continue
		tweetid = row['tweetid']
		tweet_to_total_retweet_count[tweetid] = retweet_count
		tweet_to_bot_retweet_count[tweetid] = 0

	for index, row in df.iterrows():
		if (row['is_retweet'] is 'TRUE'):
			original_id = row['retweet_tweetid']
			if (original_id in tweet_to_bot_retweet_count.keys()):
				tweet_to_bot_retweet_count[original_id] += 1

	with open('tweet_to_total_retweet_count.pickle', 'wb') as first:
		with open('tweet_to_bot_retweet_count.pickle', 'wb') as second:
			pickle.dump(tweet_to_total_retweet_count, first, pickle.HIGHEST_PROTOCOL)
			pickle.dump(tweet_to_bot_retweet_count, second, pickle.HIGHEST_PROTOCOL)


main()