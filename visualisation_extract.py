import pandas as pd
import re
from statistics import mean
import datetime

df = pd.read_csv('merge.csv', header=0, index_col=None, sep=',')

# makes counts column to int type
df['counts'] = df['counts'].astype(int)

# sorting of counts
df = df.sort_values('counts',ascending=False)

# calculating average sentiment score for each keyword
counter = 0
avg_list = []
for i in df['postive_sentiment']:
    print(i)
    if isinstance(i, str):
        i = re.sub(r'[\[\]\s]', '', i)
        if not i:
            text = 0
        else:
            text = i.split(',')
            text = [float(x) for x in text]
    else:
        text = 0
    df['postive_sentiment'][counter] = text
    if text != 0:
        avg = mean(text)
    else:
        avg = 0
    avg_list.append(avg)
    counter = counter + 1

format = '%Y-%m-%d'

# calculating days of occurence betwween the lowest and highest possible dates or else 0
counter = 0
diff_list = []
for i in df['occurance']:
    if isinstance(i, str):
        i = re.sub(r'[\[\]\s]|(nan)|(\')', '', i)
        if not i:
            text = 0
        else:
            text = i.split(',')
            text = list(filter(None, text))
            text = [datetime.datetime.strptime(x, format) for x in text]
        if text != 0:
            newest = max(text)
            oldest = min(text)
            diff = newest - oldest
            diff = diff.days/30
        else:
            diff = 0
            print(diff)
    else:
        diff = 0
    counter = counter + 1
    print(diff)
    diff_list.append(diff)
    print(diff_list)

# new columns with avg sentiment score and occurence count
df['average_sentiment'] = avg_list
df['occurance_difference'] = diff_list
# category may change subject to type of collection of data
df['category'] = 'global'
del df['Unnamed: 0']

# writing of csv file
df.to_csv('merge_sort.csv', encoding="utf-8", header=True, sep=',')
