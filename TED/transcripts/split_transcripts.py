#!/usr/bin/env python

from __future__ import unicode_literals
import csv
import os
import logging.handlers
import multiprocessing_logging
import re

def split_sentences(st):
    sentences = re.split(r'[.?!()]\s*', st)
    if sentences[-1]:
        return sentences
    else:
        return sentences[:-1]

line_end_chars = '!', '?', '.', '(', ')', ',,,'
regexPattern = '|'.join(map(re.escape, line_end_chars))



inputfile = csv.reader(open('transcripts.csv','r+'))
outputfile = open('transcripts_split.csv','a')

for r in inputfile:
    transcript = r[0]
    url = r[1]
    example = "Welcome to SOF! (Applause) This website securely stores U.S. data for the user? I don't know. naver.com is the url! (Applause and Cheers) hmm... Hi!"
    # handle in-speech urls
    example = re.sub('\.com', ',com', transcript)
    # remove quote mark
    example = re.sub('\"', '', example)
    # handle acronyms with dots
    example = re.sub(r'(?<!\w)([A-Z])\.', r'\1', example)
    # handle multiple dots
    example = re.sub(r'\.(?=\.)|(?<=\.)\.', ",", example)
    #split with line-end characters
    line_list = re.findall('.*?[\.!\?)]', example)
    # line_list should look like this:
    # ['Welcome to SOF!', '(Applause)', ' This website securely stores U.S. data for the user?','I don't know.', 'naver,com is the url!', (Applause and Cheers)', 'hmm,,, Hi!']
    # Now we just need to see which lines have our keyword
    for i in range(len(line_list)):
        line = line_list[i]
        # print('line:' + line)
        if '(' in line:
            keyword = line
            if 'Applause' in line:
                outputfile = open('applause.csv','a')
            elif 'Cheer'in line:
                outputfile = open('cheering.csv', 'a')
            elif 'Laughter' in line:
                outputfile = open('laughter.csv', 'a')
            else:
                outputfile = open('transcripts_split.csv', 'a')
            if i>=4:
                row_list = line_list[i-4:i]
            else:
                row_list = line_list[0:i]
            writer = csv.writer(outputfile)
            first_col = [keyword]
            writer.writerow(first_col+row_list)
        

        
            
 