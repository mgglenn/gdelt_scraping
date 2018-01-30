import re
import urllib.request as ur
import string
import codecs 

def clean_text(text):
  cleantext = codecs.getdecoder("unicode_escape")(text)[0]

  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', cleantext)
  cleantext = ' '.join(cleantext.split('\n'))
  return cleantext

def get_text(link):
    page = ur.urlopen(link)
    return str(page.read()) 
