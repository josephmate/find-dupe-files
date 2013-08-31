from datetime import datetime
from datetime import timedelta
import sys

class timeleft:
  
  def __init__(self, units_of_work):
    self.units_of_work = units_of_work
    self.completed_work = 0
    self.start_dt = datetime.now()


  def complete_unit(self):
    self.completed_work = self.completed_work + 1

  def percent_done(self):
    return float(self.completed_work) / float(self.units_of_work) * 100.0

  # returns the time left in seconds
  # doing simple extrapolation by
  # looking at how much time has passed
  # since we started work, and how much
  # work has been completed so far.
  # That gives us a rate;
  #
  # X seconds
  # ==========
  # 1 work
  #
  # Now we multiply the amount of work left:
  #
  # X seconds     Y work
  # ==========  *
  # 1 work
  #
  # (work units cancel out)
  #
  # = seconds left
  def seconds_left(self):
    if self.completed_work == 0:
      return sys.maxint
    delta = float((datetime.now() - self.start_dt).total_seconds())
    workLeft = self.units_of_work - self.completed_work 
    return delta / float(self.completed_work) * float(workLeft)

  def pretty_string(self):
    soFar = "["
    percent_done = self.percent_done()
    for j in [float(i) for i in range(5, 100, 5)]:
      if percent_done >= j :
        soFar += "="
      else:
        soFar += " "
    soFar += "]"
    soFar += " " + str(percent_done) + "%" + " " + str(self.seconds_left()) + " seconds left"

    return soFar


    

