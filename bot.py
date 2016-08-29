from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

closedClassIcon = "https://www.beartracks.ualberta.ca/cs/uahebprd/cache/PS_CS_COURSE_ENROLLED_ICN_1.gif"
openClassIcon = "https://www.beartracks.ualberta.ca/cs/uahebprd/cache/PS_CS_STATUS_OPEN_ICN_1.gif"

def enrollClass():
	#select course and enroll
	driver.implicitly_wait(5) # seconds
	driver.find_element_by_xpath("//tr[@id='trSSR_REGFORM_VW$0_row1']/td/div/input[@id='P_SELECT$0']").click()
	driver.find_element_by_xpath("//a[@id='DERIVED_REGFRM1_LINK_ADD_ENRL']").click()
	driver.find_element_by_xpath("//a[@id='DERIVED_REGFRM1_SSR_PB_SUBMIT']").click()

def takeScreenshot(driver, path):
	print("taking screenshot")
	driver.get_screenshot_as_file(path+str(round(time.time()))) 

def refreshPage(driver):
	driver.refresh()

#get username and password
usernameCred = input("username: ")
passwordCred = input("password: ")

#setup selenium
driver = webdriver.Firefox()

# Sign in to bear tracks
driver.get("https://www.beartracks.ualberta.ca/")
signinButton = driver.find_element_by_css_selector('img#button')
signinButton.click()

usernameField = driver.find_element_by_css_selector('input#username.form-control')
usernameField.send_keys(usernameCred)

passwordField = driver.find_element_by_css_selector('input#user_pass.form-control')
passwordField.send_keys(passwordCred)

driver.find_element_by_css_selector('input.btn.btn-default').click()

# Go to schedule builer
driver.implicitly_wait(10) # seconds
driver.switch_to_frame("NAV")
driver.find_element_by_link_text("Schedule Builder").click()

while(1 == 1):
	# Go to semester
	driver.switch_to_frame("TargetContent")
	driver.find_element_by_xpath("//tr[@id='trSSR_DUMMY_RECV1$0_row2']/td[1]/div[@id='win0divSSR_DUMMY_RECV1$sels$0']").click()
	driver.find_element_by_css_selector("a.SSSBUTTON_CONFIRMLINK").click()

	#check for open class
	icon1 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$0']/div/img[@class='SSSIMAGECENTER']")
	icon2 = driver.find_element_by_xpath("//div[@id='win0divDERIVED_REGFRM1_SSR_STATUS_LONG$1']/div/img[@class='SSSIMAGECENTER']")

	if icon1.get_attribute("src") == closedClassIcon and icon2.get_attribute("src") == closedClassIcon:
		time.sleep(30) # seconds
		refreshPage(driver)
	elif icon1.get_attribute("src") == openClassIcon and icon2.get_attribute("src") == openClassIcon:
		print("Enrolling in class")
		enrollClass()
		break
	else:
		print("Something went wrong")
		driver.maximize_window()
		driver.execute_script("window.scrollTo(0, 700);")
		takeScreenshot(driver, "Images/")
		refreshPage(driver)


