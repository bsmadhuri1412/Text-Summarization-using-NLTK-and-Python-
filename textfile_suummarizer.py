from urllib import request
from bs4 import BeautifulSoup as bs
import re
import nltk
import heapq

def textfile_summarizer(article_text, max_sentences):
    # file = open("demo.txt", "r")
    # filedata = file.readlines()  # returns a list contains each lines in a file as a list item
    # article = filedata[0].split(". ")
    # sentences = []
    # for sentence in article:
    #     print("i", sentence)
    #     sentences.append(sentence)
    # # sentences.pop()
    #
    # print(sentences)
    #
    # article_text = '. '.join([str(elem) for elem in sentences])
    #print(article_text)

    allParagraphContent_cleanerData = re.sub(r'\[[0-9]*\]', ' ', article_text)
    allParagraphContent_cleanData = re.sub(r'\s+', ' ', allParagraphContent_cleanerData)
    # print(allParagraphContent_cleanData)

    # sentences_tokens = nltk.sent_tokenize(allParagraphContent_cleanData)
    # print(sentences_tokens)
    allParagraphContent_cleaningData = re.sub(r'[^.a-zA-Z]', ' ', allParagraphContent_cleanData)
    # print(allParagraphContent_cleanedData)
    allParagraphContent_cleaningData = re.sub(r'\s+', ' ', allParagraphContent_cleaningData)

    sentences_tokens = nltk.sent_tokenize(allParagraphContent_cleaningData)
    # print(sentences_tokens)

    allParagraphContent_cleanedData = re.sub(r'[^a-zA-Z]', ' ', allParagraphContent_cleanData)
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

    summary_sentences = heapq.nlargest(max_sentences, sentences_scores, key=sentences_scores.get)
    return summary_sentences

