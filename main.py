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

class UserModel(ndb.Model):
  cafe_stamps = ndb.JsonProperty()

class CafeModel(ndb.Model):
  name = ndb.StringProperty()
  small_image = ndb.StringProperty()
  stamp_0 = ndb.StringProperty()
  stamp_1 = ndb.StringProperty()
  stamp_2 = ndb.StringProperty()
  stamp_3 = ndb.StringProperty()
  stamp_4 = ndb.StringProperty()
  stamp_5 = ndb.StringProperty()
  stamp_6 = ndb.StringProperty()
  stamp_7 = ndb.StringProperty()
  stamp_8 = ndb.StringProperty()
  stamp_9 = ndb.StringProperty()

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

class NewUserHandler(boilerplate.BlogHandler):
  def get(self):
    uuid = self.request.get('uuid')
    user_entity = UserModel(id=uuid,
                            cafe_stamps = {}
                            )
    user_entity.put()

class FirstTimeHandler(boilerplate.BlogHandler):
  def get(self):
    header_entitity = ImageModel(id="header", path="/static/images/header.jpg")
    header_entitity.put()
    self.register_cafe("dose_espresso")

  def register_cafe(self, cafe_name):
    cafe_entity = CafeModel(id=cafe_name,
                            name = cafe_name,
                            small_image = self.cafe_image_path(cafe_name, "0_cell"),
                            stamp_0 = self.cafe_image_path(cafe_name, "0"),
                            stamp_1 = self.cafe_image_path(cafe_name, "1"),
                            stamp_2 = self.cafe_image_path(cafe_name, "2"),
                            stamp_3 = self.cafe_image_path(cafe_name, "3"),
                            stamp_4 = self.cafe_image_path(cafe_name, "4"),
                            stamp_5 = self.cafe_image_path(cafe_name, "5"),
                            stamp_6 = self.cafe_image_path(cafe_name, "6"),
                            stamp_7 = self.cafe_image_path(cafe_name, "7"),
                            stamp_8 = self.cafe_image_path(cafe_name, "8"),
                            stamp_9 = self.cafe_image_path(cafe_name, "9"),
      )
    cafe_entity.put()

  def cafe_image_path(self, cafe_name, file_name):
    return "/static/images/Cafe_data/" + cafe_name + "/" + file_name + ".jpg"

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
   ('/pageStampedRedirectToCardImageURL/(.*)/(.*)', pageStampedRedirectToCardImageURL),
   ('/new_user', NewUserHandler)
  ], debug=True)
