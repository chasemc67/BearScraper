### A Bot for Enrolling in University Classes

The University of Alberta has a first-come-first-serve waitlist for classes once they are full.  
When a space opens in a class, their site waits 30 minutes, then sends out an email to everyone on the watch list.  
It is a well known fact, during the first week of classes, refresshing the enroll page with intervals < 30 mins can get you into a class.  
This automates that process.  


<img width="972" alt="screen shot 2018-05-13 at 6 08 19 pm" src="https://user-images.githubusercontent.com/6922982/39973802-ab124142-56d8-11e8-9740-8df4e692641c.png">

#### Dependencies and Installation:  
```
Python 3.4, Selenium
pip install selenium
```

#### Usage: 
```
python BearScraper.py
```


Currently bot opens page, refreshes ever 10 - 20 mintues 4 times, closes page, waits 45-75 minutes, then opens page.
sleep times are specified by arguments to executeBottingSession() and the sleep timer inside

Currently checks for both a lab and lecture once on schedule builder page. 
If you class does not have a lecture, modfify bothClassesAreFull() and bothClassesAreOpen() to check whether your class is open of full.
Modify enrollClass() to click appropriate boxes



It is important to note, that botting was NOT prohibited on the beartracks site when this was written. However, it does now appear to be prohibited. Use at your own risk. 
