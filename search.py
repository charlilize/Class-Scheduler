from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import re

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

# Gather the class info before searching
# courses = input("Enter the courses you wish to enroll in comma-seperated (e.g. CS 219, GEOL 102)\n")
# courses = [ course.strip() for course in courses.split(",")]     # Remove commas/whitespace
# courses = [course.split() for course in courses]                 # create pairs : ["COURSE NAME", "COURSE NUMBER"]

subject = "CS"
courseNumber = 370
courseNumberFieldID = "SSR_CLSRCH_WRK_CATALOG_NBR$1"
classSearchFieldID = "SSR_CLSRCH_WRK_SUBJECT$0"
showOpenClassesCheckboxID = "SSR_CLSRCH_WRK_SSR_OPEN_ONLY$3"
searchBtnID = "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://my.unlv.nevada.edu/psp/lvporprd_10/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL")

# FOR LOOP
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

''' --------- ENTER THE CLASS SUBJECT ---------------- '''
classInputElement = getElementByID(classSearchFieldID, "class name")                # Get the input field
typeInField(classInputElement, subject)                                             # Enter class slowly

''' --------- ENTER THE COURSE NUMBER ---------------- '''
courseNumInputElement = getElementByID(courseNumberFieldID, "course number")
typeInField(courseNumInputElement, courseNumber)

# Uncheck the open classes field
openClassesCheckbox = getElementByID(showOpenClassesCheckboxID, "open classes checkbox")
openClassesCheckbox.click()

''' --------- SEARCHING FOR CLASSES ---------------- '''
searchBtn = getElementByID(searchBtnID, "search button")
searchBtn.click()

# Wait for search results
time.sleep(10)

# Variables for parsing courses information
courseID = "^trSSR_CLSRCH_MTG1"
instructorID = "^MTG_INSTR"
meetingInfoID = "^MTG_DAYTIME"
roomID = "^MTG_ROOM"
newSearchBtnID = "CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH$3$"

html_text = driver.page_source
soup = BeautifulSoup(html_text, "lxml")

# Find the courses by searching for the divs with starting with this class name
courses = soup.find_all("tr", id=re.compile(courseID))

print("✅ Searching for courses...")

for course in courses:
  instructor = course.find("span", id=re.compile(instructorID)).text
  meetingInfo = course.find("span", id=re.compile(meetingInfoID)).text
  room = course.find("span", id=re.compile(roomID)).text

  print(f"{instructor} {meetingInfo} in {room}")

newSearchBtn = getElementByID(newSearchBtnID, "new search")
newSearchBtn.click()

time.sleep(10)


