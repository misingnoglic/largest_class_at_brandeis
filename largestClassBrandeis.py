from selenium import webdriver
import time

driver = webdriver.Chrome()
driver.get("https://brandeis.schdl.net/term/Spring_2017")
already_visited = set([])

classes_section = []
for i in range(3): # for each column (there are three)
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
				time.sleep(.2)
				spans = driver.find_elements_by_tag_name("span")
				people = [x for x in spans if x.get_attribute("ng:show")=="exists(enrolled)"]
				for p in people:
					try:
						n = int(p.text.split()[1])
						classes_section.append( (n,driver.current_url) )
					except:
						pass
	driver.get("https://brandeis.schdl.net/term/Spring_2017")
driver.close()
print(sorted(classes_section, key=lambda x:x[0]))