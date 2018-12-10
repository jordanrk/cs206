# Jordan Rosen-Kaplan
# 9 December 2018
# This program digests the Twitter 1% dataset,
# and outputs a csv of hashtags, their date, and time

import pandas, csv, chardet, langdetect

HASHTAG_FILENAME = 'troll_hashtags_by_time.csv'
1_PERCENT_FILENAME = '1_percent_data.csv'
OUT_FILENAME = '1_percent_hashtags_by_time.csv'
LANGUAGE = 'en'
STANDARD_DATE_FORMAT = 'XX-XX-XXXX' # note this is only used for length

# \brief: This function creates a set from a DataFrame of all hashtags
#			used in the IRA dataset
def getHashtagSet():
	dtypes = {\
	'tweetid':str,\
	'hashtag':str,\
	'day':str,\
	'time':str,\
	'text':str,\
	'user_screen_name':str\
	}

	df = pandas.read_csv(HASHTAG_FILENAME, error_bad_lines=False, dtype=dtypes)

	hashtags = set()
	for index, row in df.iterrows():
		hashtags.add(row.__dict__['_name'][1].lower().strip())

	return hashtags

# \brief: This function creates a DataFrame of the 1% dataset
def getTweets():
	dtypes = {\
	'external_author_id':str,\
	'author':str,\
	'content':str,\
	'region':str,\
	'language':str,\
	'publish_date':str,\
	'harvested_date':str,\
	'following':str,\
	'followers':str,\
	'updates':str,\
	'post_type':str,\
	'account_type':str,\
	'retweet':str,\
	'account_category':str,\
	'new_june_2018':str,\
	'alt_external_id':str,\
	'tweet_id':str,\
	'article_url':str,\
	'tco1_step1':str,\
	'tco2_step1':str,\
	'tco3_step1':str\
	}

	return pandas.read_csv(1_PERCENT_FILENAME, dtype=dtypes, error_bad_lines=False)

# \brief: This function returns a boolean if the row contains
#			all the necessary fields to include it in the csv
# @param 'row': type->series, a row in the 1% DataFrame
def isAcceptableTweet(row):
	try:
		content = row['content']
		if not content \
		or langdetect.detect(content) != LANGUAGE \
		or chardet.detect(content)['encoding'] != 'ascii' \
		or row['publish_date'] == '':
			return False
	except:
		return False

	return True

# \brief: This function returns a tuple of the day and time
#			a tweet was published
# @param 'row': type->series, a row in the 1% DataFrame
def getDayTime(row):
	return row['publish_date'][:len(STANDARD_DATE_FORMAT)], \
		row['publish_date'][len(STANDARD_DATE_FORMAT)+1:]

# \brief: This function returns digested, cleaned hashtag
# @param 'content': type->str, the tweet's text
# @param 'first_hash': type->int, the index of the next hashtag
def getNextHashtag(content, first_hash):
	end_of_hash = content.find(" " or "\n", first_hash)
	hashtag = content[first_hash:end_of_hash].lower().strip()
	# remove the '#'
	return hashtag[1:]

# \brief: This function writes hashtags, days, and times to a csv
# @param 'df': type->pandas.DataFrame, the 1%'s csv based df
# @param 'ira_hashtags': type->set, the set of all hashtags that appear
#			in the ira dataset
def writeHashtags(df, ira_hashtags):
	hashtag_times = {}
	
	with open(OUT_FILENAME, 'w') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerow("hashtag,day,time\n")
	
		for index, row in df.iterrows():
			if not isAcceptableTweet(row):
				continue

			content = row['content']		
			day, time = getDayTime(row)
		
			first_hash = content.find("#")
			while first_hash > 0:
				hashtag = getNextHashtag(content, first_hash)
				if hashtag not in ira_hashtags:
					first_hash = content.find("#", first_hash+1)
					continue
				writer.writerow(str(hashtag) + ',' + str(day) + ',' + str(time) + '\n')
				first_hash = content.find("#", first_hash+1)

def main():
	ira_hashtags = getHashtagSet()
	df = getTweets()
	writeHashtags(df, ira_hashtags)

if __name__ == '__main__':
	main()
