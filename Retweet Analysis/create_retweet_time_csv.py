import pickle, operator, math, pandas, pdb

IN_FILENAME = 'ira.csv'

def main():
	tweet_to_total_retweet_count, tweet_to_bot_retweet_count = rehydrateMaps()
	tweet_to_bot_retweet_count = pruneBotRetweets(tweet_to_bot_retweet_count)
	df = getTweets()
	tweet_to_times = mapRetweetsToTime(tweet_to_bot_retweet_count, df)
	outputMap(tweet_to_times)

def outputMap(tweet_to_times):
	path = filename + '_retweet_times.csv'
	with open(path, 'w') as file:
		file.write('tweetid,is_original,day,time\n')
		for v in tweet_to_times:
			for index, tweet in enumerate(tweet_to_times[v]):
				if not index:
					continue
				is_original = 'False'
				if index == 1:
					is_original = 'True'
				value_list = tweet.items()
				assert len(value_list) == 1
				tweetid = value_list[0][0]
				assert len(value_list[0][1]) == 2
				day, time = value_list[0][1][0], value_list[0][1][1]
				to_write = tweetid + ','\
							+ is_original + ','\
							+ day + ','\
							+ time + '\n'
				file.write(to_write)

def mapRetweetsToTime(tweet_to_bot_retweet_count, df):
	tweet_to_bot_retweet_times = {}
	i = 0
	for k, v in tweet_to_bot_retweet_count.items():
		i += 1
		print i
		tweet_to_bot_retweet_times[k] = [{}]
		original_tweet = df.loc[df['tweetid'] == k]
		assert len(original_tweet.index) == 1
		storeTimes(original_tweet, tweet_to_bot_retweet_times, k)
		bot_retweets = df.loc[df['retweet_tweetid'] == k]
		assert len(bot_retweets.index) == int(v)
		storeTimes(bot_retweets, tweet_to_bot_retweet_times, k)
	return tweet_to_bot_retweet_times

def storeTimes(tweets, tweet_to_bot_retweet_times, k):
	for index, tweet in tweets.iterrows():
		tweetid = tweet['tweetid']
		timeList = tweet['tweet_time'].split(' ')
		if len(timeList) != 2:
			continue
		day, time = timeList[0], timeList[1]
		curr_tweet = {tweetid: (day, time)}
		tweet_to_bot_retweet_times[k].append(curr_tweet)

def pruneBotRetweets(tweet_to_bot_retweet_count):
	tweet_to_bot_retweet_count_pruned = {}
	i = 0
	for k, v in tweet_to_bot_retweet_count.items():
		i += 1
		if not v or i % 10 != 0: 
			continue
		tweet_to_bot_retweet_count_pruned[k] = v
	return tweet_to_bot_retweet_count_pruned

def rehydrateMaps():
	with open('tweet_to_total_retweet_count.pickle', 'rb') as first:
		with open('tweet_to_bot_retweet_count.pickle', 'rb') as second:
			tweet_to_total_retweet_count = pickle.load(first)
			tweet_to_bot_retweet_count = pickle.load(second)
			return tweet_to_total_retweet_count, \
				   tweet_to_bot_retweet_count

def getTweets():
	dtypes = { \
		'tweetid':str, \
		'userid':str, \
		'user_display_name':str, \
		'user_screen_name':str, \
		'user_reported_location':str, \
		'user_profile_description':str, \
		'user_profile_url':str, \
		'follower_count':str, \
		'following_count':str, \
		'account_creation_date':str, \
		'account_language':str, \
		'tweet_language':str, \
		'tweet_text':str, \
		'tweet_time':str, \
		'tweet_client_name':str, \
		'in_reply_to_tweetid':str, \
		'in_reply_to_userid':str, \
		'quoted_tweet_tweetid':str, \
		'is_retweet':bool, \
		'retweet_userid':str, \
		'retweet_tweetid':str, \
		'latitude':str, \
		'longitude':str, \
		'quote_count':str, \
		'reply_count':str, \
		'like_count':str, \
		'retweet_count':str, \
		'hashtags':str, \
		'urls':str, \
		'user_mentions':str, \
		'poll_choices':str\
		}

	return pandas.read_csv(IN_FILENAME, dtype=dtypes)


main()