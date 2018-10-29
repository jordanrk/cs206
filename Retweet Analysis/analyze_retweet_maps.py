import pickle, operator

def main():
	tweet_to_total_retweet_count, tweet_to_bot_retweet_count = rehydrateMaps()
	analyzeMaps(tweet_to_total_retweet_count, tweet_to_bot_retweet_count)

def rehydrateMaps():
	with open('tweet_to_total_retweet_count.pickle', 'rb') as first:
		with open('tweet_to_bot_retweet_count.pickle', 'rb') as second:
			tweet_to_total_retweet_count = pickle.load(first)
			tweet_to_bot_retweet_count = pickle.load(second)
			return tweet_to_total_retweet_count, \
				   tweet_to_bot_retweet_count

def analyzeMaps(total, bot):
	percentages = {}
	bot_keys = bot.keys()
	for tweet, total_rts in total.items():
		if tweet not in bot_keys:
			raise Exception("Not existing key should not happen.")

		if str(total_rts) == '0':
			raise Exception("0 retweets should not happen.")

		percentages[tweet] = float(bot[tweet]) / total_rts

	percentages_sorted = sorted(percentages.items(), key=operator.itemgetter(1))

	print "Here are the top 6 tweets with bots retweeting them"
	print percentages_sorted[:5]

	print "Here are the top 6 tweets with humans/unknown bots retweeting them"
	print percentages[-5:]


main()