import os
import getpass
import random
import time
from time import strftime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

#Globals
closedClassIcon = "https://www.beartracks.ualberta.ca/cs/uahebprd/cache/PS_CS_COURSE_ENROLLED_ICN_1.gif"
openClassIcon = "https://www.beartracks.ualberta.ca/cs/uahebprd/cache/PS_CS_STATUS_OPEN_ICN_1.gif"

#functions
def takeScreenshot(driver, path):
	if not os.path.exists(path):
		os.makedirs(path)
	print("taking screenshot")
	driver.get_screenshot_as_file(path+"/"+str(round(time.time())) + ".png") 

def getRandomTimeFromRange(start, end):
	return random.randint(start, end)

def getTime():
	os.environ['TZ'] = 'US/Mountain'
	time.tzset()
	return strftime("%a, %d %b %Y %Z %X")

#wait in seconds before refreshing the page
def refreshPageAfterWait(wait, driver):
	time.sleep(wait) # seconds
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
	except NoSuchElementException as e:
		takeScreenshot(driver, "Images")
		print("Navigate to login error")
		print(e)
		return

def submitLogin(username, password, driver):
	try:
		usernameField = driver.find_element_by_css_selector('input#username.form-control')
		usernameField.send_keys(username)

		passwordField = driver.find_element_by_css_selector('input#user_pass.form-control')
		passwordField.send_keys(password)

		driver.find_element_by_css_selector('input.btn.btn-default').click()

	except NoSuchElementException as e:
		takeScreenshot(driver, "Images")
		print("Submit login error")
		print(e)
		return		

def navigateToScheduleBuilder(driver):
	# Go to schedule builer
	try:
		driver.implicitly_wait(10) # seconds
		driver.switch_to_frame("NAV")
		driver.find_element_by_link_text("Schedule Builder").click()
	except NoSuchElementException as e:
		takeScreenshot(driver, "Images")
		print("Navigate to schedule builder error")
		print(e)
		return

def navigateToFallSemester(driver):
	# Go to semester
	try:
		driver.switch_to_frame("TargetContent")
		driver.find_element_by_xpath("//tr[@id='trSSR_DUMMY_RECV1$0_row2']/td[1]/div[@id='win0divSSR_DUMMY_RECV1$sels$0']").click()
		driver.find_element_by_css_selector("a.SSSBUTTON_CONFIRMLINK").click()
	except NoSuchElementException as e:
		takeScreenshot(driver, "Images")
		print("Navigate to fall semester error")
		print(e)
		return

def bothClassesAreFull(driver):
	#determines if the class in schedule builder is open
	# hard coded for 1 class, that contains a lab
	try:
		icon1 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0']/div/img[@class='SSSIMAGECENTER']")
		icon2 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$1']/div/img[@class='SSSIMAGECENTER']")
	except NoSuchElementException as e:
		takeScreenshot(driver, "Images")
		print("both classes are full error")
		print(e)
		return

	if icon1.get_attribute("src") == closedClassIcon and icon2.get_attribute("src") == closedClassIcon:
		return True
	return False

def bothClassesAreOpen(driver):
	try:
		icon1 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0']/div/img[@class='SSSIMAGECENTER']")
		icon2 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$1']/div/img[@class='SSSIMAGECENTER']")
	except NoSuchElementException as e:
		takeScreenshot(driver, "Images")
		print("Both class are open error error")
		print(e)
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
	except NoSuchElementException as e:
		takeScreenshot(driver, "Images")
		print("Enroll class error")
		print(e)
		return

#refeshSeconds is the number of seconds we should wait before refreshing the page.
	#refreshMinutes are actually a random number in some interval, where refreshMinutes is the midpoint of the interval.
#refreshIntervalSize is the size of the interval. Some number less than refreshSeconds
#refreshesPerSession is the number of sessions before the function returns control.
def executeBottingSession(refreshSeconds, refreshIntervalSize, refreshesPerSession, username, password):
	print("[ *** ] Executing botting session at " + str(getTime()))
	print("[ ** ] Refresh count: " + str(refreshesPerSession))
	print("[ ** ] Rate of refresh: " + str(refreshSeconds/60) + " +/- " + str(refreshIntervalSize/60) + " minutes" )
	print("[ * ]")

	refreshIntervalStart = refreshSeconds - refreshIntervalSize
	refreshIntervalEnd = refreshSeconds + refreshIntervalSize

	#setup selenium
	driver = webdriver.Firefox()

	navigateToLogin(driver)
	submitLogin(username, password, driver)
	navigateToScheduleBuilder(driver)

	errorCount = 0
	for i in range(refreshesPerSession):
		navigateToFallSemester(driver)
		if bothClassesAreFull(driver):
			errorCount = 0
			print("[ . ] Both classes are full, " + str(i) + " refreshes so far. taken at " + str(getTime()))
			scrollPage(driver)
			refreshPageAfterWait(getRandomTimeFromRange(refreshIntervalStart, refreshIntervalEnd), driver)
		elif bothClassesAreOpen(driver):
			print("[ + ] Congratz bro, you did it")
			enrollClass(driver)
			break
		else:
			errorCount += 1
			print("[ - ] Something went wrong, " + str(i) + " refreshes so far, error count: " + str(errorCount))
			scrollPage(driver)
			takeScreenshot(driver, "Images")
			if errorCount > 3:
				break
			refreshPageAfterWait(getRandomTimeFromRange(refreshIntervalStart, refreshIntervalEnd), driver)
	#cleanup		
	driver.close()
	return
		

def main():
	print("")
	print("")
	print("")
	print("oooooooooo.                                .oooooo..o                                                            ")
	print("`888'   `Y8b                              d8P'    `Y8                                                            ")
	print(" 888     888  .ooooo.   .oooo.   oooo d8b Y88bo.       .ooooo.  oooo d8b  .oooo.   oo.ooooo.   .ooooo.  oooo d8b ")
	print(" 888oooo888' d88' `88b `P  )88b  `888\"\"8P  `\"Y8888o.  d88' `\"Y8 `888\"\"8P `P  )88b   888' `88b d88' `88b `888\"\"8P ")
	print(" 888    `88b 888ooo888  .oP\"888   888          `\"Y88b 888        888      .oP\"888   888   888 888ooo888  888     ")
	print(" 888    .88P 888    .o d8(  888   888     oo     .d8P 888   .o8  888     d8(  888   888   888 888    .o  888     ")
	print("o888bood8P'  `Y8bod8P' `Y888\"\"8o d888b    8\"\"88888P'  `Y8bod8P' d888b    `Y888\"\"8o  888bod8P' `Y8bod8P' d888b    ")
	print("                                                                                    888                          ")
	print("                                                                                   o888o                         ")
	print("")
	print("")
	print("--==      Beginning Campaign      ==--")
	print("")
	print("")

	#get username and password
	username = input("username: ")
	password = getpass.getpass('Password:')

	for i in range(4):
		executeBottingSession(900, 300, 4, username, password)
		print("")
		print("[ ** ] Ending session at " + str(getTime()))
		print("")
		print("")
		print("")
		time.sleep(2700, 4500)
	
	print("")
	print("")
	print("[ * ]")
	print("[ ** ]")
	print("[ **** ] Ending Campaing at " + str(getTime()))

main()
