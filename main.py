from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re
from itertools import product

''' TO STORE COURSES FOUND INFO '''
class ClassSection:
  def __init__(self, course, status, time, professor, room, days):
    self.course = course
    self.status = status
    self.time = time
    self.professor = professor
    self.room = room
    self.days = days

allSections = []
daysOfTheWeek = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

''' ID INFORMATION '''
# For main search page
courseNumberFieldID = "SSR_CLSRCH_WRK_CATALOG_NBR$1"
classSearchFieldID = "SSR_CLSRCH_WRK_SUBJECT$0"
showOpenClassesCheckboxID = "SSR_CLSRCH_WRK_SSR_OPEN_ONLY$3"
searchBtnID = "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"

# For list of courses page
courseID = "^trSSR_CLSRCH_MTG1"
instructorID = "^MTG_INSTR"
meetingInfoID = "^MTG_DAYTIME"
roomID = "^MTG_ROOM"
newSearchBtnID = "CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH$3$"
statusID = "^win10divDERIVED_CLSRCH_SSR_STATUS_LONG"

''' FUNCTIONS '''
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

# Function to type text in given element field slowly
def typeInField(inputElement, text):
  text = str(text)

  inputElement.clear()

  for char in text:
    inputElement.send_keys(char)
    time.sleep(0.5)

# Function that returns an element with a given ID
def getElementByID(ID, purposeOfElement):
  # Wait for 10 seconds for the element to exist before crashing program
  try: 
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
      (By.ID, ID)
    ))
  except:
    print(f"Couldn't work on {purposeOfElement}")

  print(f"✅ Working on {purposeOfElement}...")

  # Return the input field
  return driver.find_element(By.ID, ID)

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

# Prints out the schedules of a list, where i is a schedule and each element[i] is a list of ClassSections
def printSchedules(schedules):
  for i, sched in enumerate(schedules):
    print(f"\nSchedule {i + 1}: ")
    for section in sched:
      print(f"{section.days} {section.course}: {section.professor} {section.time} in {section.room} | {section.status}")

# Writes out the schedules of a list, where i is a schedule and each element[i] is a list of ClassSections
def writeSchedules(title, schedules):
  with open("output.txt", "a") as f:
    f.write(title)
    for i, sched in enumerate(schedules):
      f.write(f"\nSchedule {i + 1}: \n")
      for section in sched:
        f.write(f"{section.days} {section.course}: {section.professor} {section.time} in {section.room} | {section.status}\n")

''' MAIN PROGRAM '''
# Gather the class info before searching
userCourses = input("Enter the courses you wish to enroll in comma-seperated (e.g. CS 219, GEOL 102)\n")
userCourses = [course.strip() for course in userCourses.split(",")]     # Remove commas/whitespace
userCourses = [course.split() for course in userCourses]                 # create pairs : ["COURSE NAME", "COURSE NUMBER"]

# Ask for days of the week that would not want classes
rawUnwantedDays = input("\nEnter days of the week you do not want classes comma-seperated (e.g. Monday, Tuesday). Enter if any day is fine.\n")
rawUnwantedDays = [day.strip().lower() for day in rawUnwantedDays.split(",")]
unwantedDays = []

# Input validation
for day in rawUnwantedDays:
  if day in daysOfTheWeek:
    unwantedDays.append(abbreviateDay(day))
  elif day:
    print(f"{day} is not a valid day of the week. Removed {day}.")

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://my.unlv.nevada.edu/psp/lvporprd_10/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL")

# Wait for main search page to load
try:
  WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.TAG_NAME, "iframe")
  ))
except:
  print("Couldn't load webpage")

# Switch to the iframe the input fields are in
iframes = driver.find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframes[0])

# Search for courses
for subject, courseNum in userCourses:
  print(f"\n== Finding {subject} {courseNum} ==")

  ''' --------- ENTER THE CLASS SUBJECT ---------------- '''
  classInputElement = getElementByID(classSearchFieldID, "class name")                # Get the input field
  typeInField(classInputElement, subject)                                             # Enter class slowly

  ''' --------- ENTER THE COURSE NUMBER ---------------- '''
  courseNumInputElement = getElementByID(courseNumberFieldID, "course number")
  typeInField(courseNumInputElement, courseNum)

  # Uncheck the open classes field
  openClassesCheckbox = getElementByID(showOpenClassesCheckboxID, "unchecking open classes checkbox")
  openClassesCheckbox.click()

  ''' --------- SEARCHING FOR CLASSES ---------------- '''
  searchBtn = getElementByID(searchBtnID, "search button")
  searchBtn.click()

  print("✅ Searching for courses...")

  # Wait for search results
  time.sleep(10)

  html_text = driver.page_source
  soup = BeautifulSoup(html_text, "lxml")

  # Find the courses by searching for the divs with starting with this class name
  courses = soup.find_all("tr", id=re.compile(courseID))

  if not courses:
    print("No courses found")
  else:  
    for course in courses:
      instructor = course.find("span", id=re.compile(instructorID)).text
      meetingInfo = course.find("span", id=re.compile(meetingInfoID)).text
      room = course.find("span", id=re.compile(roomID)).text
      status = course.find("div", id=re.compile(statusID)).img["alt"]

      # In case meeting info is not available 
      if meetingInfo == "TBA":
        days, timeBlock = "TBA", "TBA"

      # Split meeting info into its days and time at the first space
      else:
        days, timeBlock = meetingInfo.split(" ", 1) 

      # Add to list
      allSections.append(ClassSection(f"{subject} {courseNum}", status, timeBlock, instructor, room, days))

    newSearchBtn = getElementByID(newSearchBtnID, "new search")
    newSearchBtn.click()

    time.sleep(5)

# 2D array, where element[i] is all the sections for a specific course
coursesList = [[] for _ in range(len(userCourses))] 

# Output in file all the available sections for each user course
with open("output.txt", "w") as file:
  file.write("***************** SCHEDULE BUILDER *****************\n")

  for i, course in enumerate(userCourses):            
    fullCourseName = course[0] + " " + course[1]
    file.write(f"\n=== All Sections for {fullCourseName.upper()}: ===\n") 
    for section in allSections:       # [ClassSection(), ClassSection()]
      if section.course == fullCourseName:    
        file.write(f"{section.days}: {section.professor} {section.time} in {section.room} | {section.status} \n")
        coursesList[i].append(section)

# Create different combinations of the courses
tupleSchedules = list(product(*coursesList))
schedules = [list(tupl) for tupl in tupleSchedules]   # Convert to lists
validSchedules = [] # Schedules without time conflicts

# Go through 2D array of schedules (each index is a list of a possible schedule)
for k, sched in enumerate(schedules):
  # Check for all combinations of the classes to see if there's a conflict
  validSched = True
  for i in range(len(sched)):
    for j in range(i + 1, len(sched)):
      if isOverlapping(sched[i], sched[j]):
        validSched = False
  # if no overlapping sections, add it to valid schedules
  if validSched:
    validSchedules.append(sched)

# Filter out schedules that are on unwanted days of the week, if there are any
preferredDaysSchedules, notOnPreferredDaysSchedules = [], []

if unwantedDays:
  for i, sched in enumerate(validSchedules):
    onPreferredDays = True
    for section in sched:
      for day in unwantedDays:
        if day in section.days:
          onPreferredDays = False
    if onPreferredDays:
      preferredDaysSchedules.append(sched)
    else:
      notOnPreferredDaysSchedules.append(sched)
# No need to filter if there's no schedule limitations
else: 
  preferredDaysSchedules = validSchedules

writeSchedules("""
 _.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._
          Schedules Matching Your Preferred Days
 ,'_.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._.-._`.
""", preferredDaysSchedules)


# check if it outputs properly to output.txt

'''
23 VALID for: CS 302, GRC 380, CS 219
class ClassSection:
  def __init__(self):
    self.course
    self.status
    self.time
    self.professor
    self.room
'''

print("Done!")


