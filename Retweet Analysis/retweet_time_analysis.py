# Jordan Rosen-Kaplan
# 9 December 2018
# This program outputs a CSV of time between the original tweet and
# the first retweet versus the overall number of retweets a tweet gets

import pandas, csv
from datetime import datetime, date, time

IN_FILENAME = 'ira_retweet_times.csv'

# \brief: This function returns a DataFrame of a csv 
#			associating information about the tweet's id, whether the tweet
#			is an original or a retweet, date, and time
def getData():
	dtypes = {"tweetid":str, "is_original":bool, "day":str, "time":str}

	return pandas.read_csv(IN_FILENAME, dtype=dtypes)

# \brief: This function associates tweets with a datetime object
# @param 'df': type->pandas.DataFrame, loaded from getData()
def mapRowToDatetime(df):
	row_to_datetime = {}
	for index, row in df.iterrows():
		day, time_of_day = row['day'], row['time']
		year, month, day = day.split('-')
		hour, minute = time_of_day.split(':')
		t = time(int(hour), int(minute))
		d = date(int(year), int(month), int(day))
		to_save = datetime.combine(d, t)
		row_to_datetime[index] = to_save
	return row_to_datetime

# \brief: This function writes a csv associating the time difference
#			between a tweet and its first retweet against the number
#			of retweets it ultimately garners
# @param 'dates': type->map, returned from mapRowToDatetime(df)
# @param 'df': type->pandas.DataFrame, loaded from getData()
def analyzeFirstRTTime(dates, df):
	with open("first_RT_to_num_retweets.csv", 'w') as file:
		writer = csv.writer(file, delimiter=',')
		writer.writerow('time_to_first_RT,num_retweets\n')

		new_tweet = True
		original_tweet_datetime = None
		first_retweet_datetime = None
		num_retweets = 0

		for index, row in df.iterrows():

			if index == 0:
				original_tweet_datetime = dates[index]
				continue

			if row['is_original']:
				t = first_retweet_datetime - original_tweet_datetime
				writer.writerow(str(t.total_seconds()) + "," + str(num_retweets) + "\n")
				original_tweet_datetime = dates[index]
				num_retweets = 0
				first_retweet_datetime = None
			else:
				num_retweets += 1
				curr_retweet_time = dates[index]
				if not first_retweet_datetime or curr_retweet_time < first_retweet_datetime:
					first_retweet_datetime = curr_retweet_time
		t = first_retweet_datetime - original_tweet_datetime
		writer.writerow(str(t.total_seconds()) + "," + str(num_retweets) + "\n")

def main():
	df = getData()
	dates = mapRowToDatetime(df)
	analyzeFirstRTTime(dates, df)

if __name__ == '__main__':
	main()