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
  stamp_id = ndb.IntegerProperty()
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
    header_key = ndb.Key(ImageModel, "header")
    header_path = header_key.get().path

    template_values = {
      "header_path": header_path
    }
    self.response.out.write(template.render("templates/index.html", template_values))

class StampHandler(boilerplate.BlogHandler):
  def get(self):
    uuid = self.request.get('uuid')
    stamp_id = self.request.get('stamp_id')
    user_key = ndb.Key(UserModel, uuid)
    cafe_data = user_key.get()
    if cafe_data.cafe_stamps.get(stamp_id, None) is not None:
      cafe_data.cafe_stamps[stamp_id] += 1
    else:
      cafe_data.cafe_stamps[stamp_id] = 1

    if cafe_data.cafe_stamps[stamp_id] > 9:
      cafe_data.cafe_stamps[stamp_id] = 0

    cafe_data.put()

    num_of_stamps = cafe_data.cafe_stamps[stamp_id]

    cafe_key = ndb.Key(CafeModel, stamp_id)
    cafe = cafe_key.get()

    if num_of_stamps == 0:
      header_path = cafe.stamp_0
    elif num_of_stamps == 1:
      header_path = cafe.stamp_1
    elif num_of_stamps == 2:
      header_path = cafe.stamp_2
    elif num_of_stamps == 3:
      header_path = cafe.stamp_3
    elif num_of_stamps == 4:
      header_path = cafe.stamp_4
    elif num_of_stamps == 5:
      header_path = cafe.stamp_5
    elif num_of_stamps == 6:
      header_path = cafe.stamp_6
    elif num_of_stamps == 7:
      header_path = cafe.stamp_7
    elif num_of_stamps == 8:
      header_path = cafe.stamp_8
    elif num_of_stamps == 9:
      header_path = cafe.stamp_9
    else:
      header_path = cafe.stamp_9

    self.response.out.write('<img src="' + header_path + '" >')

class CafeTableHandler(boilerplate.BlogHandler):
  def get(self):
    uuid = self.request.get('uuid')
    user_key = ndb.Key(UserModel, uuid)
    cafe_data = user_key.get().cafe_stamps

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
    cafe_entity = CafeModel(id="217",
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
   ('/requestCafeTableHTMLForUUID/(.*)', requestCafeTableHTMLForUUID),
   ('/requestHeaderHTMLForUUID/(.*)', requestHeaderHTMLForUUID),
   ('/first_time_setup', FirstTimeHandler),
   ('/pageStampedRedirectToCardImageURL/(.*)/(.*)', pageStampedRedirectToCardImageURL),
   ('/new_user', NewUserHandler),
   ('/cafe_table', CafeTableHandler),
   ('/record_stamp', StampHandler)
  ], debug=True)
