import webapp2
import json
import jinja2
import os
import boilerplate

import google.appengine.api.images
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
import logging

class ImageModel(ndb.Model):
  path = ndb.StringProperty()

class MainHandler(boilerplate.BlogHandler):
  def get(self):
    logging.info("MainHandler")
    header_key = ndb.Key(ImageModel, "header")
    header_path = header_key.get().path
    print header_path
    template_values = {
      "header_path": header_path
    }
    self.response.out.write(template.render("templates/index.html", template_values))

class FirstTimeHandler(boilerplate.BlogHandler):
  def get(self):
    header_entitity = ImageModel(id="header", path="/static/images/header.jpg")
    header_entitity.put()

class pageStampedRedirectToCardImageURL(boilerplate.BlogHandler):
  def get(self, UUID, stampID):
    logging.info("pageStamped, UUID = " + UUID + ", stampID = " + stampID)
    self.response.write("<img src = '" + "/static/images/Cafe_data/dose_espresso/6.jpg" + "' style = '" + "width:320px" + "'>")
    #self.redirect("<img src = '" + "/static/images/Cafe_data/dose_espresso/6.jpg" + "' style = '" + "width:320px" + "'>")
    #self.redirect("<img src = '" + "/static/images/Cafe_data/dose_espresso/6.jpg" + "' style = '" + "width:320px" + "'>")
    #self.redirect("/static/images/Cafe_data/dose_espresso/6.jpg")
    #self.redirect("http://idoenjoyanicecupoftea.appspot.com/static/images/Cafe_data/dose_espresso/6.jpg")
    #self.redirect("http://localhost:8080/static/images/Cafe_data/dose_espresso/6.jpg")
    #self.redirect("http://idoenjoyanicecupoftea.appspot.com/static/images/Cafe_data/dose_espresso/6.jpg")


application = webapp2.WSGIApplication(
  [('/', MainHandler),
   ('/first_time_setup', FirstTimeHandler),
   ('/pageStampedRedirectToCardImageURL/(.*)/(.*)', pageStampedRedirectToCardImageURL)
  ], debug=True)
