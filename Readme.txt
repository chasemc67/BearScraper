A bot created using selenium to automate web tasks

Dependencies:
Python 3.4, Selenium

use pip install selenium

Currently bot opens page, refreshes ever 10 - 20 mintues 4 times, closes page, waits 45-75 minutes, then opens page.
sleep times are specified by arguments to executeBottingSession() and the sleep timer inside

Currently checks for both a lab and lecture once on schedule builder page. 
If you class does not have a lecture, modfify bothClassesAreFull() and bothClassesAreOpen() to check whether your class is open of full.
Modify enrollClass() to click appropriate boxes
