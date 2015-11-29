from google.appengine.ext import ndb

class Participant(ndb.Model):
	name = ndb.StringProperty()
	email = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

	def __str__(self):
		return self.name