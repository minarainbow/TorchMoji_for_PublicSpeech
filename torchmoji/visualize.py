# -*- coding: utf-8 -*-
from __future__ import absolute_import
 
import numpy
import matplotlib
import matplotlib.pyplot as plt
import json
import argparse
 
 
# input:
#  alignment matrix - numpy array
#  shape (target tokens + eos, number of hidden source states = source tokens +eos)
# one line correpsonds to one decoding step producing one target token
# each line has the attention model weights corresponding to that decoding step
# each float on a line is the attention model weight for a corresponding source state.
# plot: a heat map of the alignment matrix
# x axis are the source tokens (alignment is to source hidden state that roughly corresponds to a source token)
# y axis are the target tokens
 
def plot_head_map(mma, target_labels, source_labels):
    fig, ax = plt.subplots()
    heatmap = ax.pcolor(mma, cmap=plt.cm.Blues)
    # put the major ticks at the middle of each cell
    ax.set_xticks(numpy.arange(mma.shape[1]) + 0.5, minor=False) # mma.shape[1] = target seq 길이
    ax.set_yticks(numpy.arange(mma.shape[0]) + 0.5, minor=False) # mma.shape[0] = input seq 길이
 
    ax.set_xlim(0, int(mma.shape[1]))
    ax.set_ylim(0, int(mma.shape[0]))
 
    # want a more natural, table-like display
    ax.invert_yaxis()
    ax.xaxis.tick_top()
 
    # source words -> column labels
    ax.set_xticklabels(source_labels, minor=False)
    # target words -> row labels
    ax.set_yticklabels(target_labels, minor=False)
 
    plt.xticks(rotation=45)
 
    # plt.tight_layout()
    plt.show()
 
 
def read_plot_alignment_matrices(source_labels, target_labels, alpha):
 
    mma = alpha.cpu().data.numpy()
 
    plot_head_map(mma, target_labels, source_labels)