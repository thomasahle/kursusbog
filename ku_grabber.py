import urllib, urllib2
import re
import HTMLParser
import model

# http://kurser.ku.dk/cbb/search/StudyProgrammes/en-GB
# http://kurser.ku.dk/search?q=&studyBlockId=null&teachingLanguage=&period=&schedules=&studyId=&openUniversity=-1&programme=&faculty=&departments=&volume=

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

def grab():
    data = urllib.urlencode(args)
    response = urllib2.urlopen(url + '?' + data)
    the_page = response.read()
    h = HTMLParser.HTMLParser()
    l = re.findall('<td>(.*?)</td>'*5, the_page, flags=re.DOTALL)
    for (info, grade, point, lang, tid) in l:
        yield model.Course(
            page = re.search('"(/course/.*?)"', info).group(1),
            name = h.unescape(re.search('>(.*?)</span>', info).group(1),)
            mpoint = int(float(point.strip())*1000),
            grade = grade.strip(),
            lang = lang.strip()
            )

def update():
    for course in grab():
        course.put()

if __name__ == '__main__':
    update()
