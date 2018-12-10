# Jordan Rosen-Kaplan
# 9 December 2018
# This program finds all instances of bots retweeting other IRA bots

import pickle, pandas, math, operator
IN_FILENAME = 'ira.csv'

# \brief: This function loads a pickle mapping tweets to total retweet counts
#			by other bots in this dataset
def rehydrateMap():
	with open('tweet_to_bot_retweet_count.pickle', 'rb') as file:
		return pickle.load(file)

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

# \brief: This function iterates over all tweets which are retweets, and
#			increments a counter associated with an original tweet if it
#			finds an instance of another tweet retweeting the original
# @param 'df': type->pandas.DataFrame, loaded from the IRA csv
# @param 'bots': type->map, associating tweetids with total number of retweets
#			by other bots
def findBotRetweetCount(df, bots)
	for index, row in df.iterrows():
		if (row['is_retweet']):
			if (not bots.get(row['retweet_tweetid']) == None):
				bots[row['retweet_tweetid']] += 1
	return bots

# \brief: This function serializes a maps and writes it to disk
# @param 'bots': type->map, associating tweetids with total number of retweets
#			by other bots
def rewriteBotRetweetCount(bots):
	with open('tweet_to_bot_retweet_count.pickle', 'wb') as file:
		pickle.dump(bots, file, pickle.HIGHEST_PROTOCOL)

def main():
	bots = rehydrateMap()
	df = getTweets()
	bots = findBotRetweetCount(df, bots)
	rewriteBotRetweetCount(bots)

if __name__ == '__main__':
	main()
