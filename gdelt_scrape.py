import re
import urllib.request as ur

def clean_text(text):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', text)
  return cleantext

def get_text(link):
    page = ur.urlopen(link)
    return page.read() 
