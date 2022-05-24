from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService

# Start Up Browswer
service = FirefoxService(executable_path="C:/Users/maxpar/dev/experimentation_dev/selenium/geckodriver-v0.30.0-win64/geckodriver")
options = FirefoxOptions()
driver = webdriver.Firefox(service=service, options=options)

# Request Website
driver.get('https://www.weblem.org/Admin/Account/Login')

un = driver.find_element_by_id("UserName")
un.send_keys('113678.shared')
ps = driver.find_element_by_id('Password')
ps.send_keys('11112222')
ps.submit()
sleep(5)
accept = driver.find_element_by_name('accept')
accept.click()
sleep(5)

import random
import itertools

input("any key to continue")

def df(start, fin):
    with open("href-remaining.txt", "r") as file:
        tot = fin-start
        i=0
        for line in itertools.islice(file, start, fin):
            sleep(1+random.randint(1,4))
            link = line.strip()
            print(link)
            try:
                #driver.execute_script(f'''window.open("{link}", "_blank");''')
                driver.get(link[:-4])
                sleep(0.7)
                driver.find_element_by_xpath("//a[@class='pure-button print']").click()
                print(f"{i} of {tot}")
            except:
                with open('log1.1.txt','a') as log:
                    log.write(link)
                    print("logged bad entry")
            i=i+1
            

df(0,12)
driver.quit()


# driver = webdriver.Firefox(service=service)

# driver = webdriver.Chrome()
# driver.get("https://docs.b360.autodesk.com/projects/8455701b-de46-45b3-b2cc-aca09ac6d7ce/folders/urn:adsk.wipprod:fs.folder:co.xTsouL_pRQeBgFfgp8o_MA")

# # Sign In 
# sign_in_id = "sign_in"
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, sign_in_id))
#     )
# finally:
#     print('driver quit!')

# sign_in_but = driver.find_element_by_id(sign_in_id)
# sign_in_but.click()

# # Enter Email and Click Next
# email_field_id = "userName"
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, email_field_id))
#     )
# finally:
#     print('driver quit!')

# email_field = driver.find_element_by_id(email_field_id)
# email_field.clear()
# email_field.send_keys("max.parker@jedunn.com")
# next_but = driver.find_element_by_id("verify_user_btn")
# next_but.click()

# # Enter Password and Click Sign In
# password_id = "password"
# try:
#     element = WebDriverWait(driver, 10).until(
#         EC.presence_of_element_located((By.ID, password_id))
#     )
# finally:
#     print('driver quit!')
# pass_field = driver.find_element_by_id(password_id)
# pass_field.clear()
# pass_field.send_keys("Sealant35^4")
# sign_in_but2 = driver.find_element_by_id("btnSubmit")
# sign_in_but2.click()


# #assert "No results found." not in driver.page_source
# driver.close()