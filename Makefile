fivethirtyeight_ncaa_forecasts.csv:
	wget "https://projects.fivethirtyeight.com/march-madness-api/2022/fivethirtyeight_ncaa_forecasts.csv"

# Pre
finishes316.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-03-16

# end of R64D1
finishes317.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-03-17

# end of R64D2
finishes318.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-03-18

# end of R32D1
finishes319.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-03-19

# end of R32D2
finishes320.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-03-20

# end of R16D1
finishes324.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-03-24

# end of R16D2
finishes325.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-03-25

# end of E8D1
finishes326.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-03-26

# end of E8D2
finishes327.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-03-27

# end of F4
finishes402.csv: fivethirtyeight_ncaa_forecasts.csv brackets.csv
	./bracket-handicapper.py -o $@ 2022-04-02

clean:
	rm -f fivethirtyeight*.csv
