import pandas as pd
import numpy as np

data = pd.read_csv('player_data.csv')

data.columns

data.describe()

# check for null values

data.isnull().any()

data.shape

# replace empty row elements with '-' as 0
data = data.replace(['-'], 0)

runs = data.sort_values(by=['Runs'])

# some problem occurs while sorting about runs value being str for some records

# we will find out which records they are

count = 0
for ind in data.index:
    if type(data['Runs'][ind]) == str:
        count += 1
    else:
        print(data['Name'][ind])
print(count)

# see how many values are str 

count = 0
for ind in data.index:
    if type(data['Runs'][ind]) == str:
        count += 1
        data['Runs'][ind] = int(data['Runs'][ind])
print(count)

data.columns

# converting all the data types to what they should be for further processing
data[[
      'Matches', 'Innings', 'Not Outs', 'Runs',
      'Highest', 'BF', 'Matches.1', 'Innings_Bowl',
      'Balls', 'Runs_Given', 'Wickets', '100',
      '200', '50', '4', '6', '5W', '10W'
      ]] = data[[
      'Matches', 'Innings', 'Not Outs', 'Runs',
      'Highest', 'BF', 'Matches.1', 'Innings_Bowl',
      'Balls', 'Runs_Given', 'Wickets', '100',
      '200', '50', '4', '6', '5W', '10W'
      ]].astype(int)
          
data[['Average', 'SR', 'Economy', 'B_Average',
      'BSR']] = data[['Average', 'SR', 'Economy', 'B_Average',
      'BSR']].astype(float)

data2 = data.sort_values(by=['Average'], ascending=False)
data2.iloc[:, :10].head()