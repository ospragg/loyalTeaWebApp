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
    cafes.append(data.cafe("dose espresso", 217, 10, 0))
    cafes.append(data.cafe("cafe nero", 101, 10, 0))
    self.render("index.html")

class requestCardHTMLForUUIDAndStampID(boilerplate.BlogHandler):
    header_key = ndb.Key(ImageModel, "header")
    header_path = header_key.get().path

    template_values = {
      "header_path": header_path
    }
    self.response.out.write(template.render("templates/index.html", template_values))

class CafeTableHandler(boilderplate.BlogHandler):
  def get(self):
    pass

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
   ('/requestHeaderHTMLForUUID/(.*)', requestHeaderHTMLForUUID),
   ('/first_time_setup', FirstTimeHandler),
   ('/pageStampedRedirectToCardImageURL/(.*)/(.*)', pageStampedRedirectToCardImageURL),
   ('/new_user', NewUserHandler)
  ], debug=True)
