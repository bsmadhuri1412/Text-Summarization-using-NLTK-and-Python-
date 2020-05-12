import cv2
from PIL import Image
import PIL.Image

from pytesseract import image_to_string
import pytesseract

import nltk
import heapq
import bs4 as bs
import PyPDF2
import re
import os


#UPLOAD_FOLDER = './uploads/'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def image_summarizer(output, max_sentences):
    # filename = input
    # W = 1000.
    # oriimg = cv2.imread(filename, cv2.IMREAD_COLOR)
    # height, width, depth = oriimg.shape
    # imgScale = W / width
    # newX, newY = oriimg.shape[1] * imgScale, oriimg.shape[0] * imgScale
    # newimg = cv2.resize(oriimg, (int(newX), int(newY)))
    # # cv2.imshow("Show by CV2",newimg)
    # cv2.waitKey(0)
    # cv2.imwrite(filename, newimg)
    # #file.save(os.path.join(app.config['UPLOAD_FOLDER'], resizeimg.jpg))
    #
    #
    # tessdata_dir_config = '--tessdata-dir "C:/Users/sitamadhuri/AppData/Local/Tesseract-OCR/tessdata"'


    # pytesseract.pytesseract.tesseract_cmd = 'C:/Users/sitamadhuri/AppData/Local/Tesseract-OCR/tesseract.exe'
    # TESSDATA_PREFIX = 'C:/Users/sitamadhuri/AppData/Local/Tesseract-OCR/tessdata'
    # tessdata_dir_config = '--tessdata-dir "C:\Users\sitamadhuri\AppData\Local\Tesseract-OCR\tesseract"'
    # pytesseract.pytesseract.tesseract_cmd =  r"C:\Users\sitamadhuri\AppData\Local\Tesseract-OCR\tesseract"
    # TESSDATA_PREFIX =  r"C:\Users\sitamadhuri\AppData\Local\Tesseract-OCR\tessdata"

    # output = pytesseract.image_to_string(PIL.Image.open(filename).convert("RGB"), lang='eng',
    #                                      config=tessdata_dir_config)
    #print("output", output)
    sentences_original = nltk.sent_tokenize(output)
    if (max_sentences > len(sentences_original)):
        print("Error, number of requested sentences exceeds number of sentences inputted")

    allParagraphContent_cleanerData = re.sub(r'\[[0-9]*\]', ' ', output)
    allParagraphContent_cleanData = re.sub(r'\s+', ' ', allParagraphContent_cleanerData)

    allParagraphContent_cleaningData = re.sub(r'[^.a-zA-Z]', ' ', allParagraphContent_cleanData)
    # print(allParagraphContent_cleanedData)
    allParagraphContent_cleaningData = re.sub(r'\s+', ' ', allParagraphContent_cleaningData)

    sentences_tokens = nltk.sent_tokenize(allParagraphContent_cleaningData)

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
    #print(word_frequencies)
    # stopwords=nltk.corpus.stopwords.words('english')
    maximum_frequency_word = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequency_word)

    sentences_scores = {}

    for sentence in sentences_tokens:
        for word in nltk.word_tokenize(sentence.lower()):
            if word in word_frequencies.keys():
                if (len(sentence.split(' '))) < 30:
                    if sentence not in sentences_scores.keys():
                        sentences_scores[sentence] = word_frequencies[word]
                    else:
                        sentences_scores[sentence] += word_frequencies[word]
    #print(sentences_scores)

    summary_sentences = heapq.nlargest(max_sentences, sentences_scores, key=sentences_scores.get)
    return summary_sentences
