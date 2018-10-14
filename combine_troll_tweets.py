import pandas as pd

def main():
	df_out = pd.DataFrame(pd.np.empty((0, 21)))
	for i in range(1, 14):
		filename = "IRAhandle_tweets_" + str(i) + ".csv"
		df = pd.read_csv(filename)
		if i == 1:
			df_out.columns = df.columns
		for index, row in df.iterrows():
			date = row['publish_date'].split(' ')[0].split('/')
			month, year = date[0].strip(), date[2].strip()
			if (month == str(11) and year == str(2017)):
				df_out = df_out.append(row)
		df_out.to_csv('final_bot_tweets.csv')
main()