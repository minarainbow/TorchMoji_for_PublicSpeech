# -*- coding: utf-8 -*-

""" Use torchMoji to score texts for emoji distribution.

The resulting emoji ids (0-63) correspond to the mapping
in emoji_overview.png file at the root of the torchMoji repo.

Writes the result to a csv file..
"""
from __future__ import print_function, division, unicode_literals
import example_helper
import json
import csv
import numpy as np
import emoji
from itertools import islice

from torchmoji.sentence_tokenizer import SentenceTokenizer
from torchmoji.model_def import torchmoji_emojis
from torchmoji.global_variables import PRETRAINED_PATH, VOCAB_PATH


inputfile = csv.reader(open('../kaggle_transcripts.csv','r+'))


# Emoji map in emoji_overview.png
EMOJIS = ":joy: :unamused: :weary: :sob: :heart_eyes: \
:pensive: :ok_hand: :blush: :heart: :smirk: \
:grin: :notes: :flushed: :100: :sleeping: \
:relieved: :relaxed: :raised_hands: :two_hearts: :expressionless: \
:sweat_smile: :pray: :confused: :kissing_heart: :heartbeat: \
:neutral_face: :information_desk_person: :disappointed: :see_no_evil: :tired_face: \
:v: :sunglasses: :rage: :thumbsup: :cry: \
:sleepy: :yum: :triumph: :hand: :mask: \
:clap: :eyes: :gun: :persevere: :smiling_imp: \
:sweat: :broken_heart: :yellow_heart: :musical_note: :speak_no_evil: \
:wink: :skull: :confounded: :smile: :stuck_out_tongue_winking_eye: \
:angry: :no_good: :muscle: :facepunch: :purple_heart: \
:sparkling_heart: :blue_heart: :grimacing: :sparkles:".split(' ')


def top_elements(array, k):
    ind = np.argpartition(array, -k)[-k:]
    return ind[np.argsort(array[ind])][::-1]

maxlen = 30

print('Tokenizing using dictionary from {}'.format(VOCAB_PATH))
with open(VOCAB_PATH, 'r') as f:
    vocabulary = json.load(f)

st = SentenceTokenizer(vocabulary, maxlen)

print('Loading model from {}.'.format(PRETRAINED_PATH))
model = torchmoji_emojis(PRETRAINED_PATH)
# print(model)
print('Running predictions.')


with open('../kaggle_results.csv','a') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Text', 
                    'Emoji_1', 'Emoji_2', 'Emoji_3', 'Emoji_4', 'Emoji_5',
                    'Pct_1', 'Pct_2', 'Pct_3', 'Pct_4', 'Pct_5'])

    print('Writing results to {}'.format(csvfile))
    for r in islice(inputfile, 0, None):
        if len(r) < 1:
            continue
        TEST_SENTENCES = r
        tokenized, _, _ = st.tokenize_sentences(TEST_SENTENCES)
        prob = model(tokenized)
                        
        for prob in [prob]:
            # Find top emojis for each sentence. Emoji ids (0-63)
            # correspond to the mapping in emoji_overview.png
            # at the root of the torchMoji repo.
            scores = []
            for i, t in enumerate(TEST_SENTENCES):
                print(i, t)
                if '(' in t:
                    continue
                t_tokens = tokenized[i]
                t_score = [t]
                t_prob = prob[i]
                ind_top = top_elements(t_prob, 5)
                t_score.extend(ind_top)
                # map to emojis
                emojis = map(lambda x: EMOJIS[x], ind_top)
                t_score.extend(emoji.emojize(''.join(emojis), use_aliases=True))
                scores.append(t_score)

            for i, row in enumerate(scores):
                try:
                    writer.writerow(row)
                except:
                    print("Exception at row {}!".format(i))
