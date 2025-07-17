from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re
from collections import defaultdict
from itertools import product

''' TO STORE COURSES FOUND INFO '''
# Example:
# week = {
#   MoWe: [ClassSection(), ClassSection()]
#   TuTh:[]
#   Fri: [ClassSection()]
# }

class ClassSection:
  def __init__(self, course, status, time, professor, room, days):
    self.course = course
    self.status = status
    self.time = time
    self.professor = professor
    self.room = room
    self.days = days

week = defaultdict(list)
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

''' MAIN PROGRAM '''
# Gather the class info before searching
userCourses = input("Enter the courses you wish to enroll in comma-seperated (e.g. CS 219, GEOL 102)\n")
userCourses = [course.strip() for course in userCourses.split(",")]     # Remove commas/whitespace
userCourses = [course.split() for course in userCourses]                 # create pairs : ["COURSE NAME", "COURSE NUMBER"]

# Ask for days of the week that would not want classes
unwantedDays = input("\nEnter days of the week you do not want classes comma-seperated (e.g. Monday, Tuesday). Enter if any day is fine.\n")
unwantedDays = [day.strip().lower() for day in unwantedDays.split(",")]
filteredUnwantedDays = []

# Input validation
for day in unwantedDays:
  if day == "":
    break
  if day in daysOfTheWeek:
    filteredUnwantedDays.append(day)
  else:
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

      # Add to dictionary
      week[days].append(ClassSection(f"{subject} {courseNum}", status, timeBlock, instructor, room, days))

    newSearchBtn = getElementByID(newSearchBtnID, "new search")
    newSearchBtn.click()

    time.sleep(5)

with open("output.txt", "w") as file:
    file.write("Test line\n")  # <- add this


# Store each courses' sections in its own list
coursesList = [[] for _ in range(len(userCourses))] # 2D array, where element[i] is all the sections for a specific course

# Output in file all the available sections for each user course
with open("output.txt", "w") as file:
  file.write("***************** SCHEDULE BUILDER *****************\n")

  for i, course in enumerate(userCourses):             # [["CS", "219"], ["CS", "302"]]
    fullCourseName = course[0] + " " + course[1]
    file.write(f"\n=== All Sections for {fullCourseName.upper()}: ===\n") 
    for dayKey in week:                  # ["MoWe", "TuTh"]
      for section in week[dayKey]:       # [ClassSection(), ClassSection()]
        if section.course == fullCourseName:    
          file.write(f"{dayKey}: {section.professor} {section.time} in {section.room} | {section.status} \n")
          coursesList[i].append(section)

# Create different combinations of the courses
tupleSchedules = list(product(*coursesList))
schedules = [list(tupl) for tupl in tupleSchedules]   # Convert to lists

print(len(schedules))

for i, sched in enumerate(schedules):
  print("")
  print(f"Schedule {i + 1}: ")
  for section in sched:
    print(f"{section.days} {section.course}: {section.professor} {section.time} in {section.room} | {section.status}")


'''


class ClassSection:
  def __init__(self):
    self.course
    self.status
    self.time
    self.professor
    self.room

sections = {
  MoWe: [ClassSection("CS 219"), ClassSection("CS 302")]
  TuTh: []
  Fri: [ClassSection("CS 219")]
}
'''

print("Done!")


