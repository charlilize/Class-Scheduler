from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Gather the class info before searching
subject = input("Enter the subject abbreviation you wish to find: ")

service = Service(executable_path="./chromedriver")
driver = webdriver.Chrome(service=service)

driver.get("https://my.unlv.nevada.edu/psp/lvporprd_10/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.CLASS_SEARCH.GBL")

WebDriverWait(driver, 10).until(EC.presence_of_element_located(
  (By.TAG_NAME, "iframe")
))

# Switch to the iframe the input fields are in
iframes = driver.find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframes[0])

# ENTER THE CLASS 
# Wait for 5 seconds for the element to exist before crashing program
WebDriverWait(driver, 10).until(EC.presence_of_element_located(
  (By.ID, "SSR_CLSRCH_WRK_SUBJECT$0")
))

if "SSR_CLSRCH_WRK_SUBJECT$0" in driver.page_source:
  print("✅ Entering class name...")

  # Get the class input field and clear it
  input_class_element = driver.find_element(By.ID, "SSR_CLSRCH_WRK_SUBJECT$0")
  input_class_element.clear()

  # Enter class slowly
  for char in subject:
      input_class_element.send_keys(char)
      time.sleep(0.5)
