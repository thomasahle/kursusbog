from google.appengine.ext import ndb

class Course(ndb.Model):
  """Models an individual Guestbook entry with content and date."""
  page = ndb.StringProperty()
  name = ndb.StringProperty()
  code = ndb.StringProperty()
  grade = ndb.StringProperty()
  lang = ndb.StringProperty()
  mpoint = ndb.IntegerProperty()

  @classmethod
  def query_book(cls, ancestor_key):
    return cls.query(ancestor=ancestor_key).order(-cls.date)
