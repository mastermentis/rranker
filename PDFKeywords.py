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
from Keywords import Keywords

class PDFKeywords(Keywords):

    def __init__(self, file_name):
        self._keys = []
        self._fname = file_name

    def convertToString(self, file_name):
        rsrcmgr = PDFResourceManager()
        retstr = StringIO()
        codec = 'utf-8'
        laparams = LAParams()
        device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)

        fp = file(file_name, 'rb')
        process_pdf(rsrcmgr, device, fp)
        fp.close()
        device.close()

        str = retstr.getvalue()
        retstr.close()
        return str

    def generateKeywords(self):
        str = self.convertToString(self._fname)
        paragraphs = self.createParagraphs(str)
        empty = re.compile('\s+$')
        for para in paragraphs:
            sentences = self.createSentences(para)
            for sent in sentences:
                if not empty.match(sent):
                    self.getNNP(sent)

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
