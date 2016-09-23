#!/usr/bin/python

import docx
import nltk, re, pprint, string
from nltk import word_tokenize
from nltk.tag import pos_tag
import sets
from sets import Set
from cStringIO import StringIO
from Keywords import Keywords

############################################################################################
# This class generates and stores the keywords read from a
# microsoft docx file. 

class DOCKeywords(Keywords):

    def __init__(self, file_name):
        self._keys = []
        self._fname = file_name

    # Generate Keywords from docx file _fname
    def generateKeywords(self):
        doc = docx.Document(self._fname)
        for para in doc.paragraphs:
            for run in para.runs:
                sent = run.text
                print sent
                empty = re.compile('\s+$')
                if not empty.match(sent):
                    self.getNNP(sent)

############################################################################################
