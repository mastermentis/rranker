#!/usr/bin/python
import sys
sys.path.append('/Users/sayantand/project/resumeranker')
from keywords import DOCKeywords

kw = DOCKeywords('aparna.docx')
kw.generateKeywords()
keys = kw.getKeywords() 
for key in keys:
    print key

