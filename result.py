from google.appengine.ext import ndb

class DrawResult(ndb.Model):
	name = ndb.StringProperty()
	email = ndb.StringProperty()
	giftee = ndb.StringProperty()
	date = ndb.DateTimeProperty(auto_now_add=True)

	def __str__(self):
		return self.name