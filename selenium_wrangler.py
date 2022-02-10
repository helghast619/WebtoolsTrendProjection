import glob
import pandas as pd
import re

csvFile = glob.glob("*.csv")
opened = []

for file in csvFile:
    # you must put header on 0 and index_col as none so you won't damage the
    # indexed later
    df = pd.read_csv(file, index_col=None, header=0)
    opened.append(df)

frame = pd.concat(opened, axis=0, ignore_index=True)
del frame['Unnamed: 0']
frame['summary'] = frame['summary'].apply(''.join)

# remove front and ending spaces
frame = frame.replace({"^\s*|\s*$": ""}, regex=True)

# dates to date type
frame['date'] = pd.to_datetime(frame['date'], errors='coerce')

# replace quotes with space
frame.summary = frame.summary.str.replace("[\[\'<>{}\"\/;:,~!?@#$%^=&*\"\\\]]|[“”¿§«»ω⊙¤°℃℉€¥£¢¡®©+–-]|"
                                          "(\\xa0)|([0-9])|(^\s*|\s*$)|(\.{2,})|(xa)", '', regex=True)
# drop duplicate rows
frame = frame.drop_duplicates()

# removal of tags
for i in range(len(frame.summary)):
    frame.summary.iloc[i] = re.sub(r'\\n|\\r|\\t|\\s', '', frame.summary.iloc[i])

# new dataframe for specific columns
new_df = frame[['date', 'summary']]

# Give the filename you wish to save the file to
filename = 'data2.csv'

# Use this function to search for any files which match your filename
files_present = glob.glob(filename)

# if no matching files, write to csv, if there are matching files, print statement
if not files_present:
    new_df.to_csv(filename, encoding="utf-8", header=True, sep=',')
    print(filename, "file saved successfully")
else:
    print('WARNING: This file already exists!')

