import glob
import pandas as pd
import re

opened = []
# csv files in the current directory
csvFile = glob.glob("*.csv")
# read files into a list

for files in csvFile:
    frame = pd.read_csv(files, index_col=None, header=0, sep=',')
    opened.append(frame)

frame = pd.concat(opened, axis=0, ignore_index=True)

# remove front and ending spaces
frame = frame.replace({"^\s*|\s*$": ""}, regex=True)

# dates to date type
frame['date'] = pd.to_datetime(frame['date'], errors='coerce')

# replace quotes with space
frame.content = frame.content.str.replace("[\[\'<>{}\"\/;:,~!?@#$%^=&*\"\\\]]|[“”¿§«»ω⊙¤°℃℉€¥£¢¡®©+–-]|"
                                          "(\\xa0)|([0-9])|(^\s*|\s*$)|(\.{2,})|(xa)", '', regex=True)

# drop duplicate rows
frame = frame.drop_duplicates()

# removal of tags
for i in range(len(frame.content)):
    frame.content.iloc[i] = re.sub(r'\\n|\\r|\\t|\\s', '', frame.content.iloc[i])

# rename columns
frame.rename(columns={'content': 'summary'}, inplace=True)

# new dataframe for specific columns
new_df = frame[['date', 'summary']]

# Give the filename you wish to save the file to
filename = 'data1.csv'

# Use this function to search for any files which match your filename
files_present = glob.glob(filename)

# if no matching files, write to csv, if there are matching files, print statement
if not files_present:
    new_df.to_csv(filename, encoding="utf-8", header=True, sep=',')
    print(filename, "file saved successfully")
else:
    print('WARNING: This file already exists!')
