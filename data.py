class cafe:
  def __init__(self, name, stamp_ID, n_stamps, i_stamp):
    self.name = name
    self.stamp_ID = stamp_ID
    self.n_stamps = n_stamps
    self.i_stamp = i_stamp

  def incrimentStampCount():
    self.i_stamp = self.i_stamp + 1
    if i_stamp == n_stamps:
      i_stamp = 0


class stamp_event:
  def __init__(self, stamp_ID, n_stamps, i_stamp, total_stamps, stamp_time):
    self.stamp_ID = stamp_ID
    self.n_stamps = n_stamps
    self.i_stamp = i_stamp
    self.total_stamps = total_stamps
    self.stamp_time = stamp_time

class user:
  def __init__(self, UUID):
    self.UUID = UUID
    self.active_cafes = []
    self.stamp_history = []
  def __contains__(self, x):
    if self.UUID == x:
      return 1
    else:
      return 0