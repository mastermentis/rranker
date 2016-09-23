#!/usr/bin/python
import sys
sys.path.append('/Users/sayantand/project/resumeranker')
from keywords import PDFKeywords

kw = PDFKeywords('SayantanDas.pdf')
kw.generateKeywords()
keys = kw.getKeywords() 
for key in keys:
    print key

