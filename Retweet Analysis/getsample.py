def main():
	with open('new_ira.csv', 'rb') as inp:
		with open('new_ira_trimmed.csv', 'wb') as outp:
			lines = inp.readlines()
			for i, line in enumerate(lines):
				if (i % 100000 == 0):
					outp.write(line)
main()