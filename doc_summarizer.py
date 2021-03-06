from urllib import request
from bs4 import BeautifulSoup as bs
import re
import nltk
import heapq
import docx2txt


def doc_summarizer(text, max_sentences):
    # extract text
    #text = docx2txt.process(input)
    sentences_original = nltk.sent_tokenize(text)
    if (max_sentences > len(sentences_original)):
        print("Error, number of requested sentences exceeds number of sentences inputted")
    allParagraphContent_cleanerData = re.sub(r'\[[0-9]*\]', ' ', text)
    allParagraphContent_cleaningData = re.sub(r'\s+', ' ', allParagraphContent_cleanerData)
    # allParagraphContent_cleanData.replace("The Portrait of Mr. W. H. By Oscar Wilde CHAPTER I","")

    allParagraphContent_cleaningData = re.sub(r'[^.a-zA-Z]', ' ', allParagraphContent_cleaningData)
    allParagraphContent_cleaningData = re.sub(r'\s+', ' ', allParagraphContent_cleaningData)

    allParagraphContent_cleaningData = allParagraphContent_cleaningData.replace(
        "The Portrait of Mr. W. H. By Oscar Wilde CHAPTER I", "")
    #print(allParagraphContent_cleaningData)
    sentences_tokens = nltk.sent_tokenize(allParagraphContent_cleaningData)

    # print("text:::   ", allParagraphContent_cleaningData)
    allParagraphContent_cleanedData = re.sub(r'[^a-zA-Z]', ' ', allParagraphContent_cleaningData)
    allParagraphContent_cleanData = re.sub(r'\s+', ' ', allParagraphContent_cleanedData)
    #print(allParagraphContent_cleanData)

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
    return (summary_MachineLearning)
