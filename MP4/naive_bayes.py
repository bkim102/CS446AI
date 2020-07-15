# naive_bayes.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 09/28/2018

"""
This is the main entry point for MP4. You should only modify code
within this file -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np
import math

"""
BAYES RULE:  P(H | e) =  P(e | H) * P(H)
                            ______________
                                P(e)

"""


def naiveBayes(train_set, train_labels, dev_set, smoothing_parameter):
    """
    train_set - List of list of words corresponding with each email
    example: suppose I had two emails 'i like pie' and 'i like cake' in my training set
    Then train_set := [['i','like','pie'], ['i','like','cake']]

    train_labels - List of labels corresponding with train_set
    example: Suppose I had two emails, first one was spam and second one was ham.
    Then train_labels := [0,1]

    dev_set - List of list of words corresponding with each email that we are testing on
              It follows the same format as train_set

    smoothing_parameter - The smoothing parameter you provided with --laplace (1.0 by default)
    """
    # TODO: Write your code here
    lambda_val = 1              #values close to 1 for unigram, close to 0 for bigram!!
    #smoothing_parameter = .0001 #COMMENT THIS OUT for final code!

    print(f"Laplace smoothing parameter: {smoothing_parameter}")
    bagOfWords_spam = {} #store word and number of occurrences in dictionary
    bagOfWords_ham = {}

    bagOfWords_spam_big = {}
    bagOfWords_ham_big = {}

    stop_words = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there',
    'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an',
    'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself',
    'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves',
    'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her',
    'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'than', 'here', 'was',
    'how', 'further', 'it', 'a', 'by', 'doing', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at',
    'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does',
    'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not',
    'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself',
    'which', 'those', 'i', 'after', 'few', 'whom', 'being', 'if', 'theirs', 'my', 'against'
    ]

    ##########  TRAINING SET  ###########
    numWordsinSpam = 0
    numWordsinHam = 0
    for i in range(0, len(train_set)):
        curr_set = train_set[i]
        curr_label = train_labels[i]
        if curr_label == 0: #### SPAM ####
            for word in curr_set:
                if word not in stop_words:
                    numWordsinSpam += 1
                    lword = word.casefold()
                    if lword not in bagOfWords_spam:
                        bagOfWords_spam[lword] = smoothing_parameter
                    else:
                        if bagOfWords_spam[lword] == smoothing_parameter:
                            bagOfWords_spam[lword] = smoothing_parameter
                        bagOfWords_spam[lword] += 1

        else: #### HAM ####
            for word in curr_set:
                if word not in stop_words:
                    numWordsinHam += 1
                    lword = word.casefold()
                    if lword not in bagOfWords_ham:
                        bagOfWords_ham[lword] = smoothing_parameter
                    else:
                        if bagOfWords_ham[lword] == smoothing_parameter:
                            bagOfWords_ham[lword] = smoothing_parameter
                        bagOfWords_ham[lword] += 1

    ###############bigram set ################
    numWordsinSpam_big = 0
    numWordsinHam_big = 0
    for i in range(0, len(train_set)):
        curr_set_big = train_set[i]
        curr_label_big = train_labels[i]
        if curr_label_big == 0: #### SPAM ####
            for index in range(len(curr_set_big)):
                if index+1 >= len(curr_set_big):
                    continue
                numWordsinSpam_big += 1
                bigram = curr_set_big[index]+curr_set_big[index + 1]
                bigram = bigram.casefold()
                if bigram not in bagOfWords_spam_big:
                    bagOfWords_spam_big[bigram] = smoothing_parameter
                else:
                    if bagOfWords_spam_big[bigram] == smoothing_parameter:
                        bagOfWords_spam_big[bigram] = smoothing_parameter
                    bagOfWords_spam_big[bigram] += 1

        else: #### HAM ####
            for index in range(len(curr_set_big)):
                if index+1 >= len(curr_set_big):
                    continue
                numWordsinHam_big += 1
                bigram = curr_set_big[index]+ curr_set_big[index + 1]
                bigram = bigram.casefold()
                if bigram not in bagOfWords_ham_big:
                    bagOfWords_ham_big[bigram] = smoothing_parameter
                else:
                    if bagOfWords_ham_big[bigram] == smoothing_parameter:
                        bagOfWords_ham_big[bigram] = smoothing_parameter
                    bagOfWords_ham_big[bigram] += 1



    #vocabularySpam = len(bagOfWords_spam) #numDistinctWords_SPAM
    #vocabularyHam = len(bagOfWords_ham)  #numDistinctWords_HAM

    ###########  DEVELOPMENT SET  ############
    dev_labels = []
    for i in range(0, len(dev_set)):
        curr_set = dev_set[i]
        probability_spam = 0.0
        probability_ham = 0.0


        for word in curr_set:
            if word in bagOfWords_spam and word in bagOfWords_ham:
                prob_word_in_spam = float(bagOfWords_spam[word]) / float(numWordsinSpam)
                prob_word_in_ham = float(bagOfWords_ham[word]) / float(numWordsinHam)
                probability_spam += math.log(prob_word_in_spam)
                probability_ham += math.log(prob_word_in_ham)

        curr_set_big = dev_set[i]
        probability_ham_big = 0.0
        probability_spam_big = 0.0
        for index in range(len(curr_set_big)):
            if index + 1 >= len(curr_set_big):
                continue
            bigram = curr_set_big[index]+ curr_set_big[index + 1]
            bigram = bigram.casefold()
            if bigram in bagOfWords_ham_big and bigram in bagOfWords_spam_big:
                prob_big_in_spam = float(bagOfWords_spam_big[bigram]) / float(numWordsinSpam_big)
                prob_big_in_ham = float(bagOfWords_ham_big[bigram]) / float(numWordsinHam_big)
                probability_spam_big += math.log(prob_big_in_spam)
                probability_ham_big += math.log(prob_big_in_ham)

        #print(f"spam confidence: {probability_spam}")
        #print(f"ham confidence: {probability_ham}")
        if (lambda_val) * probability_spam + (1 - lambda_val)*probability_spam_big <= (lambda_val)*probability_ham + (1 - lambda_val)*probability_ham_big:
            dev_labels.append(1)
        else:
            dev_labels.append(0)

    # return predicted labels of development set
    return dev_labels
