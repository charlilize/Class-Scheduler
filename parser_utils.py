import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

''' Functions to help parse / navigate the websites '''

# Function to type text in given element field slowly
def typeInField(inputElement, text):
  text = str(text)

  inputElement.clear()

  for char in text:
    inputElement.send_keys(char)
    time.sleep(0.5)

# Function that returns an element with a given ID
def getElementByID(driver, ID, purposeOfElement):
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
