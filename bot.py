from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import getpass
import os
import random

#Globals
closedClassIcon = "https://www.beartracks.ualberta.ca/cs/uahebprd/cache/PS_CS_COURSE_ENROLLED_ICN_1.gif"
openClassIcon = "https://www.beartracks.ualberta.ca/cs/uahebprd/cache/PS_CS_STATUS_OPEN_ICN_1.gif"

#functions
def takeScreenshot(driver, path):
	if not os.path.exists(path):
		os.makedirs(path)
	print("taking screenshot")
	driver.get_screenshot_as_file(path+"/"+str(round(time.time())) + ".png") 

def getRandomRefreshTime():
	return random.randint(600, 1200)

def refreshPage(driver):
	time.sleep(getRandomRefreshTime()) # seconds
	driver.refresh()

def scrollPage(driver):
	driver.maximize_window()
	driver.execute_script("window.scrollTo(0, 700);")

def navigateToLogin(driver):
	# Sign in to bear tracks
	try:
		driver.get("https://www.beartracks.ualberta.ca/")
		signinButton = driver.find_element_by_css_selector('img#button')
		signinButton.click()
	except NoSuchElementException:
		print("Navigate to login error")
		takeScreenshot(driver, "Images")
		return

def submitLogin(username, password, driver):
	try:
		usernameField = driver.find_element_by_css_selector('input#username.form-control')
		usernameField.send_keys(username)

		passwordField = driver.find_element_by_css_selector('input#user_pass.form-control')
		passwordField.send_keys(password)

		driver.find_element_by_css_selector('input.btn.btn-default').click()

	except NoSuchElementException:
		print("Submit login error")
		takeScreenshot(driver, "Images")
		return		

def navigateToScheduleBuilder(driver):
	# Go to schedule builer
	try:
		driver.implicitly_wait(10) # seconds
		driver.switch_to_frame("NAV")
		driver.find_element_by_link_text("Schedule Builder").click()
	except NoSuchElementException:
		print("Navigate to schedule builder error")
		takeScreenshot(driver, "Images")
		return

def navigateToFallSemester(driver):
	# Go to semester
	try:
		driver.switch_to_frame("TargetContent")
		driver.find_element_by_xpath("//tr[@id='trSSR_DUMMY_RECV1$0_row2']/td[1]/div[@id='win0divSSR_DUMMY_RECV1$sels$0']").click()
		driver.find_element_by_css_selector("a.SSSBUTTON_CONFIRMLINK").click()
	except NoSuchElementException:
		print("Navigate to fall semester error")
		takeScreenshot(driver, "Images")
		return

def bothClassesAreFull(driver):
	#determines if the class in schedule builder is open
	# hard coded for 1 class, that contains a lab
	try:
		icon1 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0']/div/img[@class='SSSIMAGECENTER']")
		icon2 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$1']/div/img[@class='SSSIMAGECENTER']")
	except NoSuchElementException:
		print("both classes are full error")
		takeScreenshot(driver, "Images")
		return

	if icon1.get_attribute("src") == closedClassIcon and icon2.get_attribute("src") == closedClassIcon:
		return True
	return False

def bothClassesAreOpen(driver):
	try:
		icon1 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0']/div/img[@class='SSSIMAGECENTER']")
		icon2 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$1']/div/img[@class='SSSIMAGECENTER']")
	except NoSuchElementException:
		print("Both class are open error error")
		takeScreenshot(driver, "Images")
		return

	if icon1.get_attribute("src") == openClassIcon and icon2.get_attribute("src") == openClassIcon:
		return True
	return False

def enrollClass(driver):
	#select course and enroll
	try:
		driver.implicitly_wait(5) # seconds
		driver.find_element_by_xpath("//tr[@id='trSSR_REGFORM_VW$0_row1']/td/div/input[@id='P_SELECT$0']").click()
		driver.find_element_by_xpath("//a[@id='DERIVED_REGFRM1_LINK_ADD_ENRL']").click()
		driver.find_element_by_xpath("//a[@id='DERIVED_REGFRM1_SSR_PB_SUBMIT']").click()
	except NoSuchElementException:
		print("Enroll class error")
		takeScreenshot(driver, "Images")
		return

def main():

	#get username and password
	username = input("username: ")
	password = getpass.getpass('Password:')

	#setup selenium
	driver = webdriver.Firefox()

	navigateToLogin(driver)
	submitLogin(username, password, driver)
	navigateToScheduleBuilder(driver)

	errorCount = 0
	while(1 == 1):
		navigateToFallSemester(driver)
		if bothClassesAreFull(driver):
			errorCount = 0
			print("Both classes are full")
			scrollPage(driver)
			refreshPage(driver)
		elif bothClassesAreOpen(driver):
			print("Congratz bro")
			enrollClass(driver)
			break
		else:
			errorCount += 1
			print("Something went wrong")
			scrollPage(driver)
			takeScreenshot(driver, "Images")
			if errorCount > 3:
				break
			refreshPage(driver)
	#cleanup		
	driver.close()
main()
