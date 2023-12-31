#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import warnings
warnings.filterwarnings("ignore")
import numpy as np
import argparse
import math 
from Bio import SeqIO
from itertools import product


def header(foutput, ksize):
    file = open(foutput, 'a')
    file.write("nameseq,")
    for i in range(1, ksize+1):
        file.write("k" + str(i) + ",")
    file.write("label")
    file.write("\n")
    return


def chunks(seq, win, step):
    seqlen = len(seq)
    for i in range(0,seqlen,step):
        j = seqlen if i+win>seqlen else i+win
        yield seq[i:j]
        if j==seqlen: break
    return        
    

def chunks_two(seq, win):
    seqlen = len(seq)
    for i in range(seqlen):
        j = seqlen if i+win>seqlen else i+win
        yield seq[i:j]
        if j==seqlen: break
    return

            
def file_record(foutput, label_dataset):
    file = open(foutput, 'a')
    file.write("%s," % (name_seq))
    for data in information_entropy:
        file.write("%s," % (str(data)))
    file.write(label_dataset)
    file.write("\n")
    print ("Recorded Sequence: %s" % (name_seq))
    return
    

def entropy_equation():
    header(foutput, ksize)
    global name_seq, information_entropy
    for seq_record in SeqIO.parse(finput, "fasta"):
        seq = seq_record.seq
        seq = seq.upper()
        name_seq = seq_record.name
        information_entropy = []
        for k in range(1, ksize+1):
            probabilities = []
            kmer = {}
            total_windows = (len(seq) - k) + 1 # (L - k + 1)
            for subseq in chunks_two(seq, k):
                if subseq in kmer:
                    # print(subseq)
                    kmer[subseq] = kmer[subseq] + 1
                else:
                    kmer[subseq] = 1
            for key, value in kmer.items():
                # print(key)
                # print(value)
                probabilities.append(value/total_windows)
            entropy_equation = [(p ** q) for p in probabilities]
            entropy =  (1/(q - 1)) * (1 - sum(entropy_equation))
            information_entropy.append(entropy)
        file_record(foutput, str(label_dataset))
    return

        
#############################################################################    
if __name__ == "__main__":
    print("\n")
    print("###################################################################################")
    print("######################## Feature Extraction: Entropy  #############################")
    print("######   Arguments: -i input -o output -l label -k kmer -q entropic parameter  ####")
    print("##########               Author: Robson Parmezan Bonidia                ###########")
    print("###################################################################################")
    print("\n")
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', help='Fasta format file, E.g., test.fasta')
    parser.add_argument('-o', '--output', help='CSV format file, E.g., test.csv')
    parser.add_argument('-l', '--label', help='Dataset Label, E.g., lncRNA, mRNA, sncRNA ...')
    parser.add_argument('-k', '--kmer', help='Range of k-mer, E.g., 1-mer (1) or 2-mer (1, 2) ...')
    parser.add_argument('-q', '--parameter', help='Tsallis - entropic parameter q')
    args = parser.parse_args()
    finput = str(args.input)
    foutput = str(args.output)
    label_dataset = str(args.label)
    ksize = int(args.kmer)
    q = float(args.parameter)
    stepw = 1
    entropy_equation()   
#############################################################################