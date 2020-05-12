from urllib import request
from bs4 import BeautifulSoup as bs
import re
import nltk
import heapq

def text_summarizer(input, max_sentences):
    sentences_original = nltk.sent_tokenize(input)
    # if (max_sentences > len(sentences_original)):
    #     print("Error, number of requested sentences exceeds number of sentences inputted")
    # input = "Today we know that machines have become smarter than us and can help us with every aspect of life, the technologies have reached to an extent where they can do all the tasks of human beings like household tasks, controlling home devices, making appointments etc. The field which makes these things happen is Machine Learning. Machine Learning train the machines with some data which makes it capable of acting when tested by the similar type of data. The machines have become capable of understanding human languages using Natural Language Processing. " \
    #         "Today researches are being done in the field of text analytics."
    allParagraphContent_cleanerData = re.sub(r'\[[0-9]*\]', ' ', input)
    allParagraphContent_cleanedData = re.sub(r'\s+', ' ', allParagraphContent_cleanerData)

    sentences_tokens = nltk.sent_tokenize(allParagraphContent_cleanedData)

    allParagraphContent_cleanedData = re.sub(r'[^a-zA-Z]', ' ', allParagraphContent_cleanedData)
    allParagraphContent_cleanedData = re.sub(r'\s+', ' ', allParagraphContent_cleanedData)
    # print(allParagraphContent_cleanedData)

    words_tokens = nltk.word_tokenize(allParagraphContent_cleanedData)
    # print(words_tokens)

    ## cal frequency
    stopwords = nltk.corpus.stopwords.words('english')
    # print(stopwords)

    # stopwords=nltk.corpus.stopwords.words('english')
    word_frequencies = {}

    for word in words_tokens:
        if word not in stopwords:
            if word not in word_frequencies.keys():
                word_frequencies[word] = 1
            else:
                word_frequencies[word] += 1
    # print(word_frequencies)

    maximum_frequency_word = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency_word)

    # print(word_frequencies)

    sentences_scores = {}

    for sentence in sentences_tokens:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                if (len(sentence.split(' '))) < 30:
                    if sentence not in sentences_scores.keys():
                        sentences_scores[sentence] = word_frequencies[word]
                    else:
                        sentences_scores[sentence] += word_frequencies[word]
    # print(sentences_scores)

    summary_MachineLearning = heapq.nlargest(max_sentences, sentences_scores, key=sentences_scores.get)
    # print(summary_MachineLearning)
    #summary = ' '.join(summary_MachineLearning)
    return (summary_MachineLearning)




