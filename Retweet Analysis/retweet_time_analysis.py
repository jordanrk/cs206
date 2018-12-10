import pandas, pdb
from datetime import datetime, date, time

filename = 'new_ira_retweet_times'

def main():
	df = getData()
	dates = mapRowToDatetime(df)
	analyze(dates, df)

def getData():
	dtypes = {"tweetid":str, "is_original":bool, "day":str, "time":str}

	path = filename + '.csv'
	return pandas.read_csv(path, dtype=dtypes)

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



def analyze(dates, df):
	analyzeFirstRTTime(dates, df)
	analyzeNumRetweets(dates, df)

def analyzeFirstRTTime(dates, df):
	with open("first_RT_to_num_retweets.csv", 'w') as file:
		file.write('time_to_first_RT,num_retweets\n')

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
				file.write(str(t.total_seconds()) + "," + str(num_retweets) + "\n")
				original_tweet_datetime = dates[index]
				num_retweets = 0
				first_retweet_datetime = None
			else:
				num_retweets += 1
				curr_retweet_time = dates[index]
				if not first_retweet_datetime or curr_retweet_time < first_retweet_datetime:
					first_retweet_datetime = curr_retweet_time
		t = first_retweet_datetime - original_tweet_datetime
		file.write(str(t.total_seconds()) + "," + str(num_retweets) + "\n")


def analyzeNumRetweets(dates, df):
	with open("average_time_delta_to_num_retweets.csv", 'w') as file:
		file.write('average_time_delta,num_retweets\n')
		
		num_retweets = 0
		rt_times = []

		for index, row in df.iterrows():

			if index == 0:
				original_tweet_datetime = dates[index]
				continue

			if row['is_original']:
				if len(rt_times) == 1:
					continue
				avg_td = findAverageTD(rt_times)
				file.write(avg_td + "," + str(num_retweets) + "\n")
				num_retweets = 0
				rt_times = []
			else:
				num_retweets += 1
				rt_times.append(dates[index])

def findAverageTD(rt_times):
	all_tds = []
	num_combos = 0
	for i in xrange(len(rt_times)):
		for j in xrange(i+1, len(rt_times)):
			num_combos += 1
			all_tds.append(abs(rt_times[i] - rt_times[j]).total_seconds())
	average = sum(all_tds) / float(num_combos)
	return str(average)

main()