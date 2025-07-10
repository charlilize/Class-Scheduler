from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re

''' TO STORE COURSES FOUND INFO '''
class ClassSection:
  def __init__(self):
    self.course
    self.status
    self.time
    self.professor
    self.room

week = {}

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
userCourses = [ course.strip() for course in userCourses.split(",")]     # Remove commas/whitespace
userCourses = [course.split() for course in userCourses]                 # create pairs : ["COURSE NAME", "COURSE NUMBER"]

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
  print(f"== Finding {subject} {courseNum} ==")

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

  # Wait for search results
  time.sleep(10)

  print("✅ Searching for courses...")

  html_text = driver.page_source
  soup = BeautifulSoup(html_text, "lxml")

  # Find the courses by searching for the divs with starting with this class name
  courses = soup.find_all("tr", id=re.compile(courseID))

  if not courses:
    print("No courses found")

  for course in courses:
    instructor = course.find("span", id=re.compile(instructorID)).text
    meetingInfo = course.find("span", id=re.compile(meetingInfoID)).text
    room = course.find("span", id=re.compile(roomID)).text
    status = course.find("div", id=re.compile(statusID)).img["alt"]

    # print(f"{instructor} {meetingInfo} in {room} | {status}")

    # In case meeting info is not available 
    if meetingInfo == "TBA":
      days, timeBlock = "TBA", "TBA"
      
    # Split meeting info into its days and time at the first space
    else:
      days, timeBlock = meetingInfo.split(" ", 1) 

    newSearchBtn = getElementByID(newSearchBtnID, "new search")
    newSearchBtn.click()

  time.sleep(10)

print("Done!")


'''

week = {
  MoWe: 
  TuTh:
  Fri:
}
'''
