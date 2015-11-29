#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import utils

from participant import Participant
from result import DrawResult
from google.appengine.api import users

class MainHandler(webapp2.RequestHandler):
    def get(self):
		user = users.get_current_user()
		if user:
			user_query = Participant.query(Participant.email == user.email())
			saved_user = user_query.fetch(1)
			participants_query = Participant.query().order(-Participant.date)
			participants = participants_query.fetch()
			template_values = {
				'participants': participants
			}
			
			if len(saved_user) > 0:
				template = 'joined.html'
				result_query = DrawResult.query(DrawResult.email == user.email())
				result = result_query.fetch(1)
				if len(result) > 0:
					template_values['result'] = '<h6>Your giftee is <b>%s</b></h6>' % result[0].giftee
				
			else:
				template = 'index.html'
				template_values['name'] = user.nickname()
				template_values['email'] = user.email()

			utils.fillTemplate(self.response, template, template_values)
		else:
			self.redirect(users.create_login_url(self.request.uri))

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
