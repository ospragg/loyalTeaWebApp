from google.appengine.ext import ndb

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
