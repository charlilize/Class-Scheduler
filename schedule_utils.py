''' Functions to help build schedules '''

# Abbreviates day of the week to the format of the website
def abbreviateDay(day):
  if day == "monday":
    return "Mo"
  elif day == "tuesday":
    return "Tu"
  elif day == "wednesday":
    return "We"
  elif day == "thursday":
    return "Th"
  elif day == "friday":
    return "Fr"
  elif day == "saturday":
    return "Sa"
  else:
    return "Su"

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

# Takes in two classes and returns True if the sections have conflicting times
def isOverlapping(section1, section2):

  # Edge case if they're on different days
  if section1.days != section2.days:
    return False
  
  # Edge case if one of the section's days are unknown
  if section1.days == "TBA" or section2.days == "TBA":
    return False
  
  # Convert the sections' time range to military time
  section1Times = [part.strip() for part in section1.time.split("-")]
  section2Times = [part.strip() for part in section2.time.split("-")]
  startSection1, endSection1 = convertToMilitaryTime(section1Times[0]), convertToMilitaryTime(section1Times[1])
  startSection2, endSection2 = convertToMilitaryTime(section2Times[0]), convertToMilitaryTime(section2Times[1])

  # Make sure that the end of the first class + 15 is less than the start of the second class 
  return not (endSection1 + 15 <= startSection2 or endSection2 + 15 <= startSection1)

# Writes out the schedules of a list, where i is a schedule and each element[i] is a list of ClassSections
def writeSchedules(title, schedules):
  with open("output.txt", "a") as f:
    f.write(title)
    for i, sched in enumerate(schedules):
      f.write(f"\nSchedule {i + 1}: \n")
      for section in sched:
        f.write(f"{section.days} {section.course}: {section.professor} {section.time} in {section.room} | {section.status}\n")
