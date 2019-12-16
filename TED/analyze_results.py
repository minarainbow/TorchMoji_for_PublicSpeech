import csv 
import collections
import json
from collections import Counter


columns = collections.defaultdict(list) # each value in each column is appended to a list
emoji_scores = collections.defaultdict(int)# each value

with open('results/cheering_results.csv') as f:
    reader = csv.DictReader(f) # read rows into a dictionary format
    for row in reader: # read a row as {column1: value1, column2: value2,...}
        for (k,v) in row.items(): # go over each column name and value 
            columns[k].append(v) # append the value into the appropriate list
                                 # based on column name k

Emoji_1 = columns['Emoji_1']
Emoji_2 = columns['Emoji_2']
Emoji_3 = columns['Emoji_3']
Emoji_4 = columns['Emoji_4']
Emoji_5 = columns['Emoji_5']
Pct_1 = columns['Pct_1']
Pct_2 = columns['Pct_2']
Pct_3 = columns['Pct_3']
Pct_4 = columns['Pct_4']
Pct_5 = columns['Pct_5']

for emoji in Pct_1:
    emoji_scores[emoji] += 10
for emoji in Pct_2:
    emoji_scores[emoji] += 9
for emoji in Pct_3:
    emoji_scores[emoji] += 8
for emoji in Pct_4:
    emoji_scores[emoji] += 7
for emoji in Pct_5:
    emoji_scores[emoji] += 6
sorted_emoji_scores = collections.OrderedDict(sorted(emoji_scores.items(), key=lambda kv: kv[1], reverse=True))
# print(columns)
print(sorted_emoji_scores)
labels = sorted_emoji_scores.keys()
scores = sorted_emoji_scores.values()