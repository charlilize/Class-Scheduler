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

week = {
    "TuTh": [
        ClassSection("CS 326", "Wait List", "10:00AM - 11:15AM", "Andreas Stefik", "HFA 257", "TuTh"),
        ClassSection("CS 370", "Open", "1:00PM - 2:15PM", "Benjamin Cisneros Merino", "BEH 104", "TuTh")
    ],
    "MoWe": [
        ClassSection("CS 326", "Open", "10:00AM - 11:15AM", "Benjamin Cisneros Merino", "WRI C144", "MoWe"),
        ClassSection("CS 370", "Closed", "11:30AM - 12:45PM", "Venkata Prashant Modekurthy", "GUA 3217", "MoWe"),
        ClassSection("CS 370", "Open", "2:30PM - 3:45PM", "Chuck Tessler", "CEB 218", "MoWe")
    ],
    "Fri": []
}

userCourses = 2

# Create all combinations of a schedule containing one of each desired course

# All the available sections in a 1D array for easy iteration
sections = [section for sectionsInDay in week.values() for section in sectionsInDay]

schedules = []      # each element is a schedule list
tmpSchedule = []       # temp array to build a schedule

for i in range(len(sections)):

  tmpSchedule = []
  tmpSchedule.append(sections[i])

  for j in range(i + 1, len(sections)):

    # Add the section in the schedule if not already
    if not any(existingSection.course == sections[j].course for existingSection in tmpSchedule):
      tmpSchedule.append(sections[j])

    # Only add schedule if it contains all the desired courses
    if len(tmpSchedule) == userCourses:

      schedules.append(tmpSchedule[:]) # shallow copy of schedule

      # Remove to prepare for other possible combinations
      tmpSchedule.pop(-1)

# printing schedules
for i, schedule in enumerate(schedules):
  print(f"SCHEDULE {i + 1}")
  for section in schedule:
    print(f"{section.days} {section.course}: {section.professor} {section.time} in {section.room} | {section.status}")
