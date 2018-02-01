import re
import urllib.request as ur
import string
import codecs 

from timeout import timeout

def grab_links(filename):
  lines = open(filename).readlines()
  links = []

  for l in lines:
    link = l.split('\t')[-1][:-1] # remove newline
    links.append(link)
	
  return links


def clean_text(text):
  cleantext = codecs.getdecoder("unicode_escape")(text)[0]

  # clean html
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', cleantext)

  # clean braket
  cleanr = re.compile('{.*?}')
  cleantext = re.sub(cleanr, ' ', cleantext)

  cleantext = ' '.join(cleantext.split('\n'))
  return cleantext


@timeout(3)
def get_text(link):
  try:
    page = ur.urlopen(link)
    return str(page.read()) 
  except:
    return ''
