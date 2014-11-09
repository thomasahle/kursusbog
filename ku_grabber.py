import urllib, urllib2
import re
import HTMLParser
import model
from google.appengine.ext import ndb


# http://kurser.ku.dk/cbb/search/StudyProgrammes/en-GB
# http://kurser.ku.dk/search?q=&studyBlockId=null&teachingLanguage=&period=&schedules=&studyId=&openUniversity=-1&programme=&faculty=&departments=&volume=

# https://mit.itu.dk/ucs/cb_www/index.sml
# http://www.cbs.dk/uddannelse/enkeltfag-valgfag-supplering/valgfag

url = 'http://kurser.ku.dk'
args = {'departments': '',
 'education': '',
 'faculty': '',
 'openUniversity': '0',
 'period': '',
 'programme': '',
 'q': '',
 'schedules': '',
 'searched': '1',
 'studyBlockId': 'null',
 'studyId': '',
 'teachingLanguage': '',
 'volume': ''}

url = 'http://kurser.ku.dk/search'
args = {'departments': '',
 'faculty': '',
 'openUniversity': '-1',
 'period': '',
 'programme': '',
 'q': '',
 'schedules': '',
 'studyBlockId': 'null',
 'studyId': '',
 'teachingLanguage': '',
'volume': ''}

from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(120)

def parse_point(point):
    try:
        return int(float(point.strip().replace(',','.'))*1000)
    except ValueError:
        return 0

def parse_grade(grade):
    return ' '.join(g.strip() for g in re.split('<.*?>', grade))
    
def grab():
    data = urllib.urlencode(args)
    response = urllib2.urlopen(url + '?' + data)
    the_page = response.read()
    h = HTMLParser.HTMLParser()
    l = re.findall('<td>(.*?)</td>'*5, the_page, flags=re.DOTALL)
    for (info, grade, point, lang, tid) in l:
        yield model.Course(
            parent=ndb.Key('Book', 'all'),
            page = re.search('"(/course/.*?)"', info).group(1),
            name = h.unescape(re.search('>(.*?)</span>', info).group(1)),
            mpoint = parse_point(point),
            grade = parse_grade(grade),
            lang = lang.strip()
            )

def update():
    for course in grab():
        course.put()

if __name__ == '__main__':
    update()
