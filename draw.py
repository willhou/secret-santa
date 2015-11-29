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
import random
import utils

from participant import Participant
from result import DrawResult
from google.appengine.api import mail
from google.appengine.ext import ndb

class DrawHandler(webapp2.RequestHandler):
    def get(self):

		template_values = {
			'results': 'NOPE'
    	}

		utils.fillTemplate(self.response, 'draw.html', template_values)

	def draw():

		participants_query = Participant.query()
		participants = participants_query.fetch()

		results = []
		length = len(participants)

		while length > 0:
			index = random.randrange(length)
			results.append(participants[index])
			del participants[index]
			length = len(participants)

		rs = ' -> '.join(str(p) for p in results)

		length = len(results)

		for i in range(0, length):
			result = results[i]
			giftee = ''
			if i == length - 1:
				giftee = results[0].name
			else:
				giftee = results[i+1].name

			draw_result = DrawResult(id=result.email, 
				name=result.name,
				email=result.email,
				giftee=giftee)
			draw_result.put()

			mail.send_mail(sender="satya@secret-santa-1130.appspotmail.com",
				to=result.email,
				subject="#new-york Secret Santya",
				body='Hi %s,\n\nYour secret-santya giftee is %s!\n\nLove,\nSatya' % (result.name, giftee),
				html="""
				<html><body>
				Hi %s,<br><br>
				Your secret-santya giftee is <b>%s</b>!<br><br>
				Love,<br>
				Satya
				</body></html>
				""" % (result.name, giftee))

		template_values = {
			'results': 'OK'
    	}

		utils.fillTemplate(self.response, 'draw.html', template_values)


app = webapp2.WSGIApplication([
    ('/draw', DrawHandler)
], debug=True)
