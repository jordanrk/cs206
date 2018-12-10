# Jordan Rosen-Kaplan
# 9 December 2018
# This program creates a csv with rows containing
# information about the tweet's id, whether the tweet
# is an original or a retweet, date, and time

import pickle, pandas, csv

IN_FILENAME = 'ira.csv'
OUT_FILENAME = IN_FILENAME[:IN_FILENAME.find('.')] + '_retweet_times.csv'

# \brief: This function writes a csv with rows containing
# 			information about the tweet's id, whether the tweet
# 			is an original or a retweet, date, and time
# @param 'tweet_to_times': type->map, associates tweetids with 
#			date and time of their posting. Originality is inferred
#			from location.
def outputMap(tweet_to_times):
	with open(OUT_FILENAME, 'w') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerow('tweetid,is_original,day,time\n')
		for v in tweet_to_times:
			for index, tweet in enumerate(tweet_to_times[v]):
				if not index: # first entry is header
					continue
				is_original = 'False'
				if index == 1:
					is_original = 'True'
				value_list = tweet.items()
				assert len(value_list) == 1

				# needs to be cleaned
				tweetid = value_list[0][0]
				assert len(value_list[0][1]) == 2
				day, time = value_list[0][1][0], value_list[0][1][1]

				writer.writerow(tweetid + ',' + is_original + ',' + day + ',' + time + '\n')

# \brief: This function associates all tweet ids with date and time of
#			their retweets
# @param 'tweet_to_bot_retweet_count': type->map, associating tweetids 
#			with total number of retweets by other bots
# @param 'df': type->pandas.DataFrame, loaded from the IRA csv
def mapRetweetsToTime(tweet_to_bot_retweet_count, df):
	tweet_to_bot_retweet_times = {}
	i = 0
	for k, v in tweet_to_bot_retweet_count.items():
		i += 1
		tweet_to_bot_retweet_times[k] = [{}]
		original_tweet = df.loc[df['tweetid'] == k]
		assert len(original_tweet.index) == 1
		storeTimes(original_tweet, tweet_to_bot_retweet_times, k)
		bot_retweets = df.loc[df['retweet_tweetid'] == k]
		assert len(bot_retweets.index) == int(v)
		storeTimes(bot_retweets, tweet_to_bot_retweet_times, k)
	return tweet_to_bot_retweet_times

# \brief: This function associates tweet ids with date and time of
#			their tweet
# @param 'tweets': type->pandas.DataFrame, tweets which are retweets
#			of the original tweet
# @param 'tweet_to_bot_retweet_times': type->map, associates an original
#			tweet with all of its subsequent retweets and their times
# @param 'original_id': type->str, the tweetid of the original tweet,
#			which all tweets in tweets are retweeting
def storeTimes(tweets, tweet_to_bot_retweet_times, original_id):
	for index, tweet in tweets.iterrows():
		tweetid = tweet['tweetid']
		timeList = tweet['tweet_time'].split(' ')
		assert len(timeList) == 2
		day, time = timeList[0], timeList[1]
		curr_tweet = {tweetid: (day, time)}
		tweet_to_bot_retweet_times[original_id].append(curr_tweet)

# \brief: This function returns a randomized sample map
#			of the bot tweets that have >0 retweets
# @param 'tweet_to_bot_retweet_count': type->map, associating tweetids 
#			with total number of retweets by other bots
def pruneBotRetweets(tweet_to_bot_retweet_count):
	tweet_to_bot_retweet_count_pruned = {}
	i = 0
	for k, v in tweet_to_bot_retweet_count.items():
		i += 1
		if not v or i % 10 != 0: 
			continue
		tweet_to_bot_retweet_count_pruned[k] = v
	return tweet_to_bot_retweet_count_pruned

# \brief: This function loads pickles mapping tweets to total
#			retweet counts and tweets to total retweet counts
#			by other bots in this dataset
def rehydrateMaps():
	with open('tweet_to_total_retweet_count.pickle', 'rb') as first:
		with open('tweet_to_bot_retweet_count.pickle', 'rb') as second:
			tweet_to_total_retweet_count = pickle.load(first)
			tweet_to_bot_retweet_count = pickle.load(second)
			return tweet_to_total_retweet_count, \
				   tweet_to_bot_retweet_count

# \brief: This function returns a DataFrame of IRA dataset, linked in README.MD
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

def main():
	tweet_to_total_retweet_count, tweet_to_bot_retweet_count = rehydrateMaps()
	tweet_to_bot_retweet_count = pruneBotRetweets(tweet_to_bot_retweet_count)
	df = getTweets()
	tweet_to_times = mapRetweetsToTime(tweet_to_bot_retweet_count, df)
	outputMap(tweet_to_times)

if __name__ == '__main__':
	main()