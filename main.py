import webapp2
import json
import jinja2
import os
import boilerplate

import google.appengine.api.images
import logging



class MainHandler(boilerplate.BlogHandler):
  def get(self):
    logging.info("MainHandler")
    self.render("index.html")

class requestCardHTMLForUUIDAndStampID(boilerplate.BlogHandler):
  def get(self, UUID, stampID):
    logging.info("requesting card HTML, UUID = " + UUID + ", stampID = " + stampID)
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