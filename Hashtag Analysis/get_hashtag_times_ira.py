# Jordan Rosen-Kaplan
# 9 December 2018
# This program digests the Twitter IRA dataset, 
# released @ https://about.twitter.com/en_us/values/elections-integrity.html#data
# and outputs a csv of hashtags, their date, time, and unique identifiers

import math, pandas, string, csv

LANGUAGE = 'en'
OUT_FILENAME = 'hashtags_by_time.csv'
IN_FILENAME = 'ira.csv'

# \brief: This function strips the hashtag list of its brackets
# @param 'hashtag_list': type->list, list of hashtags
def digestHashtags(hashtag_list):
	iter_list = hashtag_list.split()

	# remove opening bracket
	iter_list[0] = iter_list[0][1:]
	# remove closing bracket
	iter_list[len(iter_list)-1] = iter_list[len(iter_list)-1][:-1]

	return iter_list

# \brief: This function strips a string of its punctuation
# @param 'hashtag': type->str, any string
def removePunctuation(hashtag):
	return hashtag.translate(None, string.punctuation)

# \brief: This function strips the hashtag list of its brackets
# @param 'hashtag_list': type->list, list of hashtags
def getDayTime(row):
	time_list = row['tweet_time'].split(' ')
	assert len(time_list) == 2
	return time_list

# \brief: This function finds all English hashtags and associates
#			them with the time and date they were tweeted
# @param 'df': type->pandas.DataFrame, IRA dataset, linked above
def getHashtags(df):
	hashtag_times = {}

	for index, row in df.iterrows():

		if row['tweet_language'] != LANGUAGE:
			continue

		hashtag_list = row['hashtags']
		# continue if empty
		if type(hashtag_list) is float and math.isnan(hashtag_list):
			continue

		hashtags = digestHashtags(hashtag_list)

		for hashtag in hashtags:
			if not hashtag:
				continue

			hashtag = removePunctuation(hashtag)
			day, time = getDayTime(row)
			hashtag_times[row['tweetid']] = [hashtag, day, time, row['tweet_text'], row['user_screen_name']]

	return hashtag_times

# \brief: This function return a DataFrame of IRA dataset, linked above
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

# \brief: This function manipulates the list of fields and
#			associated key into a comma seperated row 
#			for csv export
# @param 'tweetid': type->str, key from hashtag_times map
# @param 'field_list': type->list, all associated values from
#			'tweetid'
def createRow(tweetid, field_list):
	row = str(tweetid)
	for field in field_list:
		x = ',' + str(field)
		row += x
	row += '\n'
	return row

# \brief: This function writes a csv of hashtags, times, and unique IDs
# @param 'hashtag_times': type->map, tweetid to hashtag, day, time, text,
#			and user_screen_name 
def writeHashtags(hashtag_times):
	with open(OUT_FILENAME, 'w') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerow('tweetid,hashtag,day,time,text,user_screen_name\n')
		for tweetid, field_list in hashtag_times.items():
			writer.writerow(createRow(tweetid, field_list))

def main():
	df = getTweets()
	hashtag_times = findHashtags(df)
	writeHashtags(hashtag_times)

if __name__ == '__main__':
	main()
