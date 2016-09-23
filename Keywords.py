#!/usr/bin/python

import nltk, re, pprint, string
from nltk import word_tokenize
from nltk.tag import pos_tag
import sets
from sets import Set
from pdfminer.pdfinterp import PDFResourceManager, process_pdf
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO


class Keywords:
    def __init__(self, file_name):
        self._keys = []
        self._fname = file_name

    def getKeywords(self):
        return self._keys

    def convertToString(self, file_name):    #will be overwritten in derived class
        raise AssertionError

    def generateKeywords(self):
        raise AssertionError

    def strip_non_ascii(self, string):
        stripped = (c for c in string if 0 < ord(c) < 127)
        return ''.join(stripped)

    def createParagraphs(self, f):
        para = []
        para_line = ''
        line = ''
        notempty = re.compile('.*(\w+)\n')
        empty = re.compile('\s+$')
        pageno = re.compile('^Page([0-9])+')
        lines = re.split('\n', f)
        for line in lines  :
            if pageno.match(line):
                continue 
            if not empty.match(line) :
                para_line = para_line + ' ' + self.strip_non_ascii(line.replace('\n',' '))
            else : 
                para.append(para_line)
                para_line = ''
        return para

    def createSentences(self, para):
        sentences = re.split('\.|;|:|,', para)
        return sentences

    def stem(self, word):
        regexp = r'^(.*?)(ing|ly|ed|ious|ies|ive|es|s|ment)?$'
        stem, suffix = re.findall(regexp, word)[0]
        re.sub(r'[\W_]+', '', stem)
        return stem

    def getNNP(self, doc):
        sentence = nltk.sent_tokenize(doc)
        sentence = [nltk.word_tokenize(sent) for sent in sentence]
        sentence = [nltk.pos_tag(sent) for sent in sentence]

        grammar = "KEY: {(<VB.*><IN>*<NN*>|<NNP>)}"
        cp = nltk.RegexpParser(grammar)

        chunked = []
        for s in sentence:
            chunked.append(cp.parse(s))
        for c in chunked:
            for cc in c.subtrees() :
                if cc.label() == 'KEY':
                    for (s,label) in cc :
                        if label == 'NNP' or label == 'NN' or label == 'NNS':
                            key = s.strip().lower()
                            if not key in self._keys:
                                self._keys.append(key)

############################################################################################

'''
# This the new version of convert_pdf

from cStringIO import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

def convert_pdf(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)

    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = file(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close
    return text 

'''
############################################################################################
