import re
import urllib.request as ur
import string
import codecs 
from timeout import timeout
from datetime import timedelta, date
import zipfile
import wget


def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def generate_links(start, end, template='http://data.gdeltproject.org/events/%s.export.CSV.zip'):
    """
    Generates a list of web pages to grab.
    :param start: the beginning date in the YYYY-MM-DD format (str)
    :param end: the ending date in the YYYY-MM-DD format (str)
    :returns: list of links to get
    """
    links = []
    year1, month1, day1 = start.split("-")
    year2, month2, day2 = end.split("-")                                                  

    start_dt = date(int(year1), int(month1), int(day1))
    end_dt = date(int(year2), int(month2), int(day2))

    for dt in daterange(start_dt, end_dt):
        date_string = dt.strftime("%Y%m%d")
        link = template % date_string
        links.append(link)

    return links


def grab_csv_data(filename):
  lines = open(filename).readlines()
  data = []

  for line_id, l in enumerate(lines):
    comps = l.split('\t')
    link = l.split('\t')[-1][:-1] # remove newline
    data.append([line_id, comps[-2], link])
	
  return data


def extract_csv(link, path=''):
    zip_file = wget.download(link, out=path)
    zip_ref = zipfile.ZipFile(zip_file, 'r')
    zip_ref.extractall(path)
    zip_ref.close()
    csv_file = zip_ref.filename[:zip_ref.filename.index('.zip')]
    zip_ref.close()
    return csv_file


def clean_text(text):
  cleantext = codecs.getdecoder("unicode_escape")(text)[0]
  """
  # clean html
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, ' ', cleantext)

  # clean braket
  cleanr = re.compile('{.*?}')
  cleantext = re.sub(cleanr, ' ', cleantext)

  cleantext = ' '.join(cleantext.split('\n'))
  cleantext.replace('\t', ' ')
  cleantext = cleantext.lower()
  """
  return cleantext


@timeout(3)
def get_text(link):
  try:
    page = ur.urlopen(link)
    raw = page.read() 
    clean = clean_text(raw)
    clean = clean_text(clean)
    return clean
  except:
    return ''
