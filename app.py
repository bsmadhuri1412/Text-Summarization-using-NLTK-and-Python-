import flask
from flask import Flask, render_template, request,url_for, redirect, flash
import os
import urllib
from urllib import request
from bs4 import BeautifulSoup as bs
import re
import nltk
import heapq
import docx2txt
import slate3k as slate
import cv2
from PIL import Image
import PIL.Image

from pytesseract import image_to_string
import pytesseract
import PyPDF2

from werkzeug.utils import secure_filename
from text_summarizer import text_summarizer
from link_summarizer import link_summarzier
from doc_summarizer import doc_summarizer
from pdf_summarizer import pdf_summarizer
from image_summarizer import image_summarizer
from textfile_suummarizer import textfile_summarizer

app =Flask(__name__)

@app.route('/')
def homepage():
	title = "Text Summarizer"
	return render_template("index.html", title = title)

@app.route('/templates', methods=['GET','POST'])
def get_text():
    title = "Text Summarizer"
    text = flask.request.form['input_text']  # Get text from html
    num_sent = float(flask.request.form['num_sentences'])
    print("num_sney -", num_sent)
    sentences_original = nltk.sent_tokenize(text)
    n= len(sentences_original)
    #print("n:", n)
    num_senten = (int)((num_sent * n) / 100)
    print(num_senten)
    summary = text_summarizer(text, num_senten)
    #textsum = ' '.join(summary)
    return render_template("text.html", title=title, original_text=text, output_summary=summary, total = num_senten)
    #return render_template("text.html")

@app.route('/textsummary')
def get_html():
    title = "Text Summarizer"
    return render_template("text.html", title = title)

@app.route('/urlsummary')
def get_htmlurl():
    title = "Text Summarizer"
    return render_template("link.html", title = title)

@app.route('/url', methods=['GET','POST'])
def get_url():
    title = "Text Summarizer"
    text = flask.request.form['input_text']  # Get text from html

    if text == '':
        flask.flash('you should enter a url')
        return redirect(flask.request.base_url)
    else:
        num_sent = float(flask.request.form['num_sentences'])
        allParagraphContent = ""
        htmlDoc = urllib.request.urlopen(text)
        soupObject = bs(htmlDoc, 'html.parser')

        paragraphContents = soupObject.findAll('p')
        # print(paragraphContents)

        for paragraphContent in paragraphContents:
            allParagraphContent += paragraphContent.text

        sentences_original = nltk.sent_tokenize(allParagraphContent)
        n= len(sentences_original)
        num_senten = (int)((num_sent * n) / 100)
        print(num_senten)
        textsum = link_summarzier(allParagraphContent, num_senten)

    return render_template("link.html", title=title, original_text=allParagraphContent, output_summary=textsum, total = num_senten)

ALLOWED_EXTEN  =  {'txt'}
def allowic_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTEN


@app.route('/txtsummary')
def get_txturl():
    title = "Text Summarizer"
    return render_template("txt.html", title = title)

@app.route('/txtupload', methods=['GET','POST'])
def get_txt():
    title = "Text Summarizer"
    textsumm = " "
    newinput = " "

    if flask.request.method == "POST":
        if 'file' not in flask.request.files:
            message = "No file is attached in request"
            flask.flash(message, category='notice')
            # return redirect(url_for('get_doc'))
            return redirect(flask.request.base_url)
        file = flask.request.files['file']
        if file.filename == '':
            message = "no file selected"
            flask.flash(message, category='notice')
            # return redirect(url_for('get_doc'))
            return redirect(flask.request.base_url)
        if file and allowic_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            num_sent = float(flask.request.form['num_sentences'])
            # text = docx2txt.process(input)
            input = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            filein = open(input, "r",encoding="utf8")
            filedata = filein.readlines()  # returns a list contains each lines in a file as a list item
            article = filedata[0].split(". ")
            sentences = []
            for sentence in article:
                #print("i", sentence)
                sentences.append(sentence)
            # sentences.pop()

            #print(sentences)

            article_text = '. '.join([str(elem) for elem in sentences])
            sentences_original = nltk.sent_tokenize(article_text)
            n = len(sentences_original)
            num_senten = (int)((num_sent * n) / 100)

            textsumm = textfile_summarizer(article_text, num_senten)
            # print("text:", textsumm)

    return render_template("txt.html", title=title, original_text=article_text, output_summary=textsumm, total = num_senten)


@app.route('/getdocupload')
def get_doc():
    title = "Text Summarizer"
    return render_template('doc.html',title = title)

ALLOWED_EXTENSIONS  =  {'docx'}
def allowed_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads/'
ALLOWED_EXTENSION  =  {'pdf'}
def allow_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSION

@app.route('/docupload', methods = ['GET', 'POST'])
def upload_file():
    title = "Text Summarizer"
    textsumm = " "
    newinput = " "
    num_senten=0

    if flask.request.method == "POST":
        if 'file' not in flask.request.files:
            message = "No file is attached in request"
            flask.flash(message,category='notice')
            #return redirect(url_for('get_doc'))
            return redirect(flask.request.base_url)
        file = flask.request.files['file']
        if file.filename == '':
            message = "no file selected"
            flask.flash(message,category='notice')
            #return redirect(url_for('get_doc'))
            return redirect(flask.request.base_url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            num_sent = float(flask.request.form['num_sentences'])
            #text = docx2txt.process(input)
            input = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            newinput = docx2txt.process(input)
            sentences_original = nltk.sent_tokenize(newinput)
            n = len(sentences_original)
            num_senten = (int)((num_sent * n) / 100)
            #print(num_senten)
            textsumm = doc_summarizer(newinput, num_senten)
            #print("text:", textsumm)

    return render_template("doc.html", title=title, original_text=newinput, output_summary=textsumm, total = num_senten)


UPLOAD_FOLDER = './uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route('/docupload', methods = ['GET', 'POST'])
# def upload_doc():
#     title = "Text Summarizer"
#     file = request.files['file']
#     newfile = secure_filename(file.filename)
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfile))
#     textsumm = doc_summarizer(os.path.join(app.config['UPLOAD_FOLDER'], newfile))
#     return render_template("doc.html", title=title, original_text=file, output_summary=textsumm)


@app.route('/getpdf')
def get_pdf():
    title = "Text Summarizer"
    return render_template('pdf.html',title = title)

# @app.route('/pdfupload', methods = ['GET', 'POST'])
# def upload_pdf():
#     title = "Text Summarizer"
#     file = request.files['file']
#     num_sent = int(flask.request.form['num_sentences'])
#     newfile = secure_filename(file.filename)
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfile))
#     textsumm = pdf_summarizer(os.path.join(app.config['UPLOAD_FOLDER'], newfile), num_sent)
#     return render_template("pdf.html", title=title, original_text=file, output_summary=textsumm)

@app.route('/pdfupload', methods = ['GET', 'POST'])
def upload_pdf():
    title = "Text Summarizer"
    textsumm = " "
    article_text = " "
    num_senten=0

    if flask.request.method == "POST":
        if 'file' not in flask.request.files:
            message = "No file is attached in request"
            #return redirect(url_for('get_doc'))
            return redirect(flask.request.base_url)
        file = flask.request.files['file']
        if file.filename == '':
            message = "no file selected"
            #return redirect(url_for('get_doc'))
            return redirect(flask.request.base_url)
        if file and allow_file(file.filename):
            newfile = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfile))
            num_sent = float(flask.request.form['num_sentences'])
            input = os.path.join(app.config['UPLOAD_FOLDER'], newfile)
            with open(input, 'rb') as f:
                extracted_text = slate.PDF(f)
            extracted_text = [x.replace("\t", " ") for x in extracted_text]
            extracted_text = [x.replace("\n", " ") for x in extracted_text]
            extracted_text = [
                x.replace("Liked This Book?  For More FREE e-Books visit Freeditorial.com              \x0c", "")
                for x in extracted_text]
            # print(extracted_text)

            article_text = '. '.join([str(elem) for elem in extracted_text])
            sentences_original = nltk.sent_tokenize(article_text)
            n = len(sentences_original)
            num_senten = (int)((num_sent * n) / 100)
            textsumm = pdf_summarizer(article_text, num_senten)
            #print("text:", textsumm)

    return render_template("pdf.html", title=title, original_text=article_text, output_summary=textsumm, total = num_senten)

ALLOWED_EXTENT  =  {'png', 'jpg', 'jpeg', 'gif'}
#ALLOWED_EXTENT  = {'jpg'}
def allowable_file(filename):
   return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENT

@app.route('/getimg')
def get_img():
    title = "Text Summarizer"
    return render_template('image.html',title = title)

# @app.route('/imgupload', methods = ['GET', 'POST'])
# def upload_img():
#     title = "Text Summarizer"
#     file = request.files['image']
#     num_sent = int(flask.request.form['num_sentences'])
#     newfile = secure_filename(file.filename)
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfile))
#     textsumm = image_summarizer(os.path.join(app.config['UPLOAD_FOLDER'], newfile), num_sent)
#     return render_template("image.html", title=title, original_text=file, output_summary=textsumm)

@app.route('/imgupload', methods = ['GET', 'POST'])
def upload_img():
    title = "Text Summarizer"
    textsumm = " "
    output = " "
    num_senten=0

    if flask.request.method == "POST":
        if 'file' not in flask.request.files:
            message = "No file is attached in request"
            print(message)
            #return redirect(url_for('get_doc'))
            return redirect(flask.request.base_url)
        file = flask.request.files['file']
        if file.filename == '':
            message = "no file selected"
            #return redirect(url_for('get_doc'))
            print(message)
            return redirect(flask.request.base_url)
        if file and allowable_file(file.filename):
            newfile = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], newfile))
            num_sent = float(flask.request.form['num_sentences'])

            input= os.path.join(app.config['UPLOAD_FOLDER'], newfile)
            filename = input
            W = 1000.
            oriimg = cv2.imread(filename, cv2.IMREAD_COLOR)
            print("image",oriimg)
            height, width, depth = oriimg.shape
            imgScale = W / width
            newX, newY = oriimg.shape[1] * imgScale, oriimg.shape[0] * imgScale
            newimg = cv2.resize(oriimg, (int(newX), int(newY)))
            # cv2.imshow("Show by CV2",newimg)
            cv2.waitKey(0)
            cv2.imwrite(filename, newimg)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], resizeimg.jpg))

            tessdata_dir_config = '--tessdata-dir "C:/Users/sitamadhuri/AppData/Local/Tesseract-OCR/tessdata"'
            output = pytesseract.image_to_string(PIL.Image.open(filename).convert("RGB"), lang='eng',
                                                 config=tessdata_dir_config)
            sentences_original = nltk.sent_tokenize(output)
            n = len(sentences_original)
            num_senten = (int)((num_sent * n) / 100)
            textsumm = image_summarizer(output, num_senten)
            #print("text:", textsumm)

    return render_template("image.html", title=title, original_text=output, output_summary=textsumm, total = num_senten)



if __name__ == "__main__":
	app.debug = True
	app.run()