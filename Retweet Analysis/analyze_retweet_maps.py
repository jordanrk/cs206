# Jordan Rosen-Kaplan
# 9 December 2018
# This program writes the bot tweets most or least retweeted by humans

import pickle, operator, math, pandas, csv

NUM_TO_WRITE = 100000
IN_FILENAME = 'ira.csv'

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

# \brief: This function returns a list of all tweets sorted by how many humans
#			retweeted them, over the number of total retweets
# @param 'total': type->map, associating tweetids with total number of 
#			retweets
# @param 'bot': type->map, associating tweetids with total number of retweets
#			by other bots
def analyzeMaps(total, bot):
	percentages = {}
	for i, item in enumerate(total.items()):
		tweet, total_rts = item
		if math.isnan(total_rts):
			continue
		percentages[tweet] = float(bot[tweet]) / total_rts

	return sorted(percentages.items(), key=operator.itemgetter(1))

# \brief: This function loads a DataFrame and returns a map associating
#			tweetid's with text, retweet count, and usernames
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

	df = pandas.read_csv(IN_FILENAME, dtype=dtypes)
	
	tweetid_to_tweet = {}

	for index, row in df.iterrows():
		tweetid_to_tweet[row['tweetid']] = [row['tweet_text'], row['user_screen_name'], row['retweet_count']]

	return tweetid_to_tweet

# \brief: This function creates a row to write to a csv
# @param 'tweet': type->tuple, association of tweetid to 
#			percentage retweets by other bots
# @param 'tweetid_to_tweet': type->map, associates tweetid to text, username
#			and retweet count
def createRow(tweet, tweetid_to_tweet):
	tweetid, percentage_retweets_by_bots = tweet[0], tweet[1]
	row = tweetid
	assert tweetid_to_tweet.get(tweetid) != None
	for field in tweetid_to_tweet[tweetid]:
		row += ',' + str(field)
	row += ',' + str(percentage_retweets_by_bots) + '\n'
	return row

# \brief: This function writes retweet analysis to a csv
# @param 'tweetid_to_tweet': type->map, associates tweetid to text, username
#			and retweet count
# @param 'percentages_sorted': type->list, tweets and percentages of tweets
#			by other bots (list of tuples)
# @param 'best': type->boolean, whether the user wants this function to
#			write the most retweeted tweets by humans (True) or the least
#			retweeted tweets by humans (False)
def writeRetweets(tweetid_to_tweet, percentages_sorted, best):
	filename = ''
	if best:
		filename = 'best_' + str(NUM_TO_WRITE) + '.csv'
		percentages_sorted = percentages_sorted[:NUM_TO_WRITE]
	else:
		filename = 'worst_' + str(NUM_TO_WRITE) + '.csv'
		percentages_sorted = percentages_sorted[-NUM_TO_WRITE:]

	with open(filename, 'w') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerow('tweetid,text,screen_name,retweet_count,percentage_retweets_by_bots\n')
		for tweet in percentages_sorted:
			writer.writerow(createRow(tweet, tweetid_to_tweet))

def main():
	tweet_to_total_retweet_count, tweet_to_bot_retweet_count = rehydrateMaps()
	tweetid_to_tweet = getTweets()
	percentages_sorted = analyzeMaps(tweet_to_total_retweet_count, tweet_to_bot_retweet_count)
	writeRetweets(tweetid_to_tweet, percentages_sorted, True)
	writeRetweets(tweetid_to_tweet, percentages_sorted, False)

if __name__ == '__main__':
	main()