import webapp2
from google.appengine.ext import ndb
from google.appengine.ext.webapp import template
from models.models import ImageModel, UserModel, CafeModel

class MainHandler(webapp2.RequestHandler):
  def get(self):
    header_key = ndb.Key(ImageModel, "header")
    header_path = header_key.get().path

    template_values = {
      "header_path": header_path
    }
    self.response.out.write(template.render("templates/index.html", template_values))

class StampHandler(webapp2.RequestHandler):
  def get(self):
    uuid = self.request.get('uuid')
    stamp_id = self.request.get('stamp_id')
    record_stamp = int(self.request.get('stamp'))
    user_key = ndb.Key(UserModel, uuid)
    cafe_data = user_key.get()

    if record_stamp:
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

    self.response.out.write(header_path)

class CafeTableHandler(webapp2.RequestHandler):

  def get(self):
    uuid = self.request.get('uuid')
    user_key = ndb.Key(UserModel, uuid)
    cafe_data = user_key.get().cafe_stamps
    cafe_smalls = []

    for cafe_id in cafe_data.keys():
      cafe_key = ndb.Key(CafeModel, cafe_id)
      cafe = cafe_key.get()
      cafe_smalls.append((cafe_id, cafe.small_image))

    template_values = {
      "cafes": cafe_smalls
    }

    self.response.out.write(template.render("templates/cafe_table.html", template_values))

class NewUserHandler(webapp2.RequestHandler):
  def get(self):
    uuid = self.request.get('uuid')
    user_entity = UserModel(id=uuid,
                            cafe_stamps = {}
                            )
    user_entity.put()

class FirstTimeHandler(webapp2.RequestHandler):
  def get(self):
    header_entitity = ImageModel(id="header", path="/static/images/header.jpg")
    header_entitity.put()
    self.register_cafe("dose_espresso")

  def register_cafe(self, cafe_name):
    cafe_entity = CafeModel(
      id="217",
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

application = webapp2.WSGIApplication(
  [('/', MainHandler),
   ('/first_time_setup', FirstTimeHandler),
   ('/new_user', NewUserHandler),
   ('/cafe_table', CafeTableHandler),
   ('/record_stamp', StampHandler)
  ], debug=True)
