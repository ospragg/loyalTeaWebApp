import webapp2
import json
import jinja2
import os
import boilerplate

import google.appengine.api.images
import logging

import data
users = []
cafes = []

class MainHandler(boilerplate.BlogHandler):
  def get(self):
    logging.info("MainHandler")
    cafes.append(data.cafe("dose espresso", 217, 10, 0))
    cafes.append(data.cafe("cafe nero", 101, 10, 0))
    self.render("index.html")

class requestCardHTMLForUUIDAndStampID(boilerplate.BlogHandler):
  def get(self, UUID, stampID):
    logging.info("requesting card HTML, UUID = " + UUID + ", stampID = " + stampID)
    if any(UUID in data.user.UUID for data.user.UUID in users):
      logging.info("     UUID = " + UUID + ", i_stamps = " + users[0].active_cafes[0].i_stamps)
    else:
      logging.info("matching UUID not found. Adding user:")
      users.append(data.user(UUID))
      users.active_cafes.append(stampID in data.cafe.stamp_ID for data.cafe.stamp_ID in cafes)
      logging.info("   user UUID = " + users[0].UUID)
    self.response.write("<img src = '" + "/static/images/Cafe_data/dose_espresso/6.jpg" + "' style = '" + "width:320px" + "'>")

class requestCafeTableHTMLForUUID(boilerplate.BlogHandler):
  def get(self, UUID):
    logging.info("requesting cafe table HTML, UUID = " + UUID)
    self.response.write("<img src = '" + "/static/images/Cafe_data/dose_espresso/0_cell.jpg' style = 'width:320px'><br>")
    
class requestHeaderHTMLForUUID(boilerplate.BlogHandler):
  def get(self, UUID):
    logging.info("requesting header HTML, UUID = " + UUID)
    self.response.write("<img src = '" + "/static/images/header.jpg" + "' style = '" + "width:320px" + "'>")

application = webapp2.WSGIApplication(
  [('/', MainHandler),
  ('/requestCardHTMLForUUIDAndStampID/(.*)/(.*)', requestCardHTMLForUUIDAndStampID),
  ('/requestCafeTableHTMLForUUID/(.*)', requestCafeTableHTMLForUUID),
  ('/requestHeaderHTMLForUUID/(.*)', requestHeaderHTMLForUUID)
  ], debug=True)
