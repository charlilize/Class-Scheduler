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

# ERROR WITH HAVING >= 2 COURSES

# Create all combinations of a schedule containing one of each desired course

# All the available sections in a 1D array for easy iteration
'''
loop through each userCourses
  store fullCourse name
  loop throuch the values in the week hashmap

'''

