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

# Takes in a string: "10:00PM" and returns the military time 2200
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

  return str(time)  


schedule = [
    ClassSection("CS 302", "Wait List", "4:00PM - 5:15PM", "James Andro-Vasko", "HFA 257", "MoWe"),
    ClassSection("CS 302", "Open", "1:00PM - 2:15PM", "Staff", "TBE B-176", "MoWe"),
    ClassSection("CS 302", "Open", "11:30AM - 12:45PM", "Staff", "GUA 2212", "MoWe"),
    ClassSection("CS 302", "Open", "5:30PM - 6:45PM", "James Andro-Vasko", "TBE B-176", "TuTh"),
    ClassSection("CS 302", "Open", "1:00PM - 2:15PM", "Shaikh Arifuzzaman", "BEH 121", "TuTh"),
    ClassSection("CS 219", "Wait List", "8:30AM - 9:45AM", "Sam Black", "BEH 107", "MoWe"),
    ClassSection("CS 219", "Open", "10:00AM - 11:15AM", "Kishore Konda Chidella", "Web live", "TuTh"),
    ClassSection("CS 219", "Open", "1:00PM - 2:15PM", "Kishore Konda Chidella", "BEH 113", "TuTh"),
    ClassSection("GRC 380", "Open", "5:30PM - 8:15PM", "Ryan Almazan", "Web live", "MoWe"),
    ClassSection("GRC 380", "Open", "8:30AM - 11:15AM", "Ashley Doughty", "GRA 239B", "TuTh")
]

print(convertToMilitaryTime("12:00AM"))  # 00:00
print(convertToMilitaryTime("12:01AM"))  # 00:01
print(convertToMilitaryTime("1:00AM"))   # 01:00
print(convertToMilitaryTime("2:30AM"))   # 02:30
print(convertToMilitaryTime("4:15AM"))   # 04:15
print(convertToMilitaryTime("6:45AM"))   # 06:45
print(convertToMilitaryTime("9:15AM"))   # 09:15
print(convertToMilitaryTime("11:59AM"))  # 11:59
print(convertToMilitaryTime("12:00PM"))  # 12:00
print(convertToMilitaryTime("12:01PM"))  # 12:01
print(convertToMilitaryTime("1:00PM"))   # 13:00
print(convertToMilitaryTime("2:30PM"))   # 14:30
print(convertToMilitaryTime("4:45PM"))   # 16:45
print(convertToMilitaryTime("5:30PM"))   # 17:30
print(convertToMilitaryTime("8:30PM"))   # 20:30
print(convertToMilitaryTime("10:45PM"))  # 22:45
print(convertToMilitaryTime("11:59PM"))  # 23:59



