# Jordan Rosen-Kaplan
# 9 December 2018
# This program creates serializations of all IRA bot tweets to the number
# of retweets they receive and a map of all IRA bot tweets to the number
# 0, which gets populated with a value in process_bot_retweets.py

import pickle, pandas, pdb, math

IN_FILENAME = 'ira.csv'
LANGUAGE = 'en'

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

# \brief: This function creates two maps, linking tweets to total retweets
#			and an empty map associating all tweets with 0
# @param 'df': type->pandas.DataFrame, loaded from the IRA csv
def findRetweetCounts(df):
	tweet_to_total_retweet_count = {}
	tweet_to_bot_retweet_count = {}

	for index, row in df.iterrows():
		retweet_count = row['retweet_count']
		tweetid = row['tweetid']
		if (retweet_count == '0' or row['tweet_language'] != LANGUAGE or math.isnan(float(retweet_count))):
			continue
		tweet_to_total_retweet_count[tweetid] = int(retweet_count)
		# tweet_to_bot_rt_count gets filled in process_bot_retweets.py
		tweet_to_bot_retweet_count[tweetid] = 0

	return tweet_to_total_retweet_count, tweet_to_bot_retweet_count

# \brief: This function serializes two maps and writes them to disk
# @param 'tweet_to_total_retweet_count': type->map, linking tweets 
#			to total retweets
# @param 'tweet_to_bot_retweet_count': type->map, an empty map 
#			associating all tweets with 0
def dehydrateMaps(tweet_to_total_retweet_count, tweet_to_bot_retweet_count):
	with open('tweet_to_total_retweet_count.pickle', 'wb') as first:
		with open('tweet_to_bot_retweet_count.pickle', 'wb') as second:
			pickle.dump(tweet_to_total_retweet_count, first, pickle.HIGHEST_PROTOCOL)
			pickle.dump(tweet_to_bot_retweet_count, second, pickle.HIGHEST_PROTOCOL)

def main():
	df = getTweets()
	total, bot = findRetweetCounts(df)
	dehydrateMaps(total, bot)

if __name__ == '__main__':
	main()