from selenium import webdriver
import time
try:
	import winsound
	sound = True
except ImportError:
	sound = False

import pickle
try:
	from tabulate import tabulate
except ImportError:
	tabulate = lambda *args,**kwargs: args[0]

driver = webdriver.PhantomJS()
link = "https://brandeis.schdl.net/term/Spring_2017"

driver.get(link)
already_visited = set([]) # List of links already visisted, so no duplicates
# This is needed because lots of classes are crosslists - thankfully they have the same URL

classes_section = [] # Store classes by section
classes_total = [] # Store by total number of people in all the sections
for i in range(3): # for each column (there are three - bad that this is hardcoded but eh)
	time.sleep(1) # time for loading

	column = driver.find_elements_by_class_name("col-sm-4")[i] # get that column
	
	# Every link in the major
	major_links = [l.get_attribute("href") for l in column.find_elements_by_tag_name("a") if l]
	for major in major_links:
		driver.get(major) # go to that URL
		time.sleep(1)
		links = driver.find_elements_by_tag_name("a")
		links = [l.get_attribute("href") for l in links]
		#print(links)
		print(driver.current_url)
		for l in links:
			if l and "course" in l and l not in already_visited:
				driver.get(l)
				already_visited.add(l)
				time.sleep(.3)
				spans = driver.find_elements_by_tag_name("span")
				if len(spans)==0: # in case the page didn't load
					driver.refresh()
					time.sleep(3)
					spans = driver.find_elements_by_tag_name("span")
				# All of the span elements that have a section name
				people = [x for x in spans if x.get_attribute("ng:show")=="exists(enrolled)"]
				total_n = 0
				current_class = driver.current_url.split("/")[-1]
				for i,p in enumerate(people):
					try:
						n = int(p.text.split()[1]) # Number of people in class
						# Append a tuple of number of people, class name, and section
						classes_section.append( (n,current_class,i+1) )
						total_n+=n
					except:
						pass
				classes_total.append( (total_n, current_class) )
	driver.get(link)
driver.quit()

sorted_classes_section = sorted(classes_section, key=lambda x:x[0], reverse=True)
print(tabulate(sorted_classes_section[:25], headers=["Number of people", "Course", "Section"]))
sorted_classes_total = sorted(classes_total, key=lambda x:x[0], reverse=True)
#if sound: winsound.MessageBeep()
#input("Press enter to continue")
print(tabulate(sorted_classes_total[:25], headers=["Number of people", "Course"]))

with open("classes_by_section.pickle", "wb") as classes_by_section:
	pickle.dump(sorted_classes_section, classes_by_section)


with open("classes_total.pickle", "wb") as classes_total:
	pickle.dump(sorted_classes_total, classes_total)


