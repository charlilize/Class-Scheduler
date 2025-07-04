from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

def typeInField(inputElement, text):
  for char in text:
    inputElement.send_keys(char)
    time.sleep(0.5)

# Gather the class info before searching
# courses = input("Enter the courses you wish to enroll in comma-seperated (e.g. CS 219, GEOL 102)\n")
# courses = [ course.strip() for course in courses.split(",")]                                                      # Remove commas/whitespace

subject = "CS"
courseNumber = 370
courseNumberFieldID = "SSR_CLSRCH_WRK_CATALOG_NBR$1"
classSearchFieldID = "SSR_CLSRCH_WRK_SUBJECT$0"

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://my.unlv.nevada.edu/psp/lvporprd_10/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL")

# maybe underneath as a for loop for each course
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
(By.TAG_NAME, "iframe")
))

# Switch to the iframe the input fields are in
iframes = driver.find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframes[0])

# --------- ENTER THE CLASS ----------------
# Wait for 5 seconds for the element to exist before crashing program
try: 
  WebDriverWait(driver, 10).until(EC.presence_of_element_located(
  (By.ID, classSearchFieldID)
  ))
except:
   print("Couldn't enter class subject")

print("✅ Entering class name...")

# Get the class input field and clear it
classInputElement = driver.find_element(By.ID, classSearchFieldID)
classInputElement.clear()

# Enter class slowly
for char in subject:
  classInputElement.send_keys(char)
  time.sleep(0.5)

try: 
  WebDriverWait(driver, 10).until(EC.presence_of_element_located(
  (By.ID, courseNumberFieldID)
  ))
except:
   print("Couldn't enter course number")

CourseNumInputElement = driver.find_element(By.ID, courseNumberFieldID)
CourseNumInputElement.clear()

# Enter course number slowly
for char in str(courseNumber):
  CourseNumInputElement.send_keys(char)
  time.sleep(0.5)
