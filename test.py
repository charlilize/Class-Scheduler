class ClassSection:
  def __init__(self, course, status, time, professor, room, days):
    self.course = course
    self.status = status
    self.time = time
    self.professor = professor
    self.room = room
    self.days = days

def printSection(section):
  print(f"{section.days} {section.course}: {section.professor} {section.time} in {section.room} | {section.status}")

# Takes in a string: "10:00PM" and returns the military time: 2200
def convertToMilitaryTime(time):
  
  hour, minutes = [part.strip() for part in time.split(":")]  # Remove colon

  # If the time is PM or is during 12AM, convert it
  if "PM" in time or ("12" in time and "AM" in time):          
    # Edge case where 12PM doesn't need to be converted 
    if not ("12" in time and "PM" in time):
      hour = int(hour)
      hour += 12

      # Reset back to 0 if at 24 mark
      if hour == 24:
        hour = 0

      hour = str(hour)

  time = hour + minutes
  time = time[:-2]                                            # Remove AM/PM

  return int(time)  

# Takes in two classes and a boolean
def isOverlapping(section1, section2):

  # Edge case if they're on different days
  if section1.days != section2.days:
    return False
  
  # Convert the sections' time range to military time
  section1Times = [part.strip() for part in section1.time.split("-")]
  section2Times = [part.strip() for part in section2.time.split("-")]
  startSection1, endSection1 = convertToMilitaryTime(section1Times[0]), convertToMilitaryTime(section1Times[1])
  startSection2, endSection2 = convertToMilitaryTime(section2Times[0]), convertToMilitaryTime(section2Times[1])

  # Make sure that the end of the first class + 15 is less than the start of the second class 
  return not (endSection1 + 15 <= startSection2 or endSection2 + 15 <= startSection1)


schedule = [
    ClassSection("CS 302", "Wait List", "4:00PM - 5:15PM", "James Andro-Vasko", "HFA 257", "MoWe"),
    ClassSection("CS 302", "Open", "1:00PM - 2:15PM", "Staff", "TBE B-176", "MoWe"),
    ClassSection("CS 302", "Open", "11:30AM - 12:45PM", "Staff", "GUA 2212", "MoWe"),
    ClassSection("CS 302", "Open", "5:30PM - 6:45PM", "James Andro-Vasko", "TBE B-176", "TuTh"),
]

print()
