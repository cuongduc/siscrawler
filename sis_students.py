import sys
import time
import codecs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException

"""
init_driver: initialize selenium webdriver
"""
def init_driver():
    driver = webdriver.Firefox()
    driver.wait = WebDriverWait(driver, 5)
    return driver

"""
Class Student
"""
class Student():
	def __init__(self, id, fn, md, ln, bd, cla, pro, status):
		self.id 		 = id
		self.first_name  = fn
		self.middle_name = md
		self.last_name 	 = ln
		self.birth_date  = bd
		self.clas 		 = cla
		self.program     = pro
		self.status      = status

"""
make_id_prefix: create prefix for student id
according to the cohort
"""
def make_id_prefix(cohort):
    prefix = 0
    cohort = int(cohort)
    if cohort == 56:
    	prefix = 2011
    elif cohort == 57:
    	prefix = 2012
    elif cohort == 58:
    	prefix = 2013
    elif cohort == 59:
    	prefix = 2014
    elif cohort == 60:
    	prefix = 2015
    else:
    	prefix = 2010

    return prefix

"""
make_id_list: create a list of student ids
to crawl information about students
"""
def make_id_list(cohort, start, end):
	prefix = make_id_prefix(cohort)
	id_list = []

	for index in range(int(start), int(end) + 1):
		if index < 10:
			index = '000' + str(index)
		elif index >= 10 and index < 100:
			index = '00' + str(index)
		elif index >= 100 and index < 1000:
			index = '0' + str(index)
		elif index >= 1000:
			index = str(index)

		id = str(prefix) + str(index)
		id_list.append(id);

	return id_list

"""
get_student: retrieve student information from sis
"""
def get_student(driver, cohort, start, end):
    driver.get("http://sis.hust.edu.vn/ModuleSearch/GroupList.aspx")
    queries = make_id_list(cohort, start, end)
    
    f = codecs.open('data/' + str(cohort)+'.csv', 'a', 'utf-8')
    try:
    	# The student id input field
        input = driver.wait.until(EC.presence_of_element_located((By.NAME, "ctl00$MainContent$tbStudentID")))
        # Get student's info for each id created in make_id_list
        for query in queries:
	        input.send_keys(query)
	        input.send_keys(Keys.RETURN)
	        time.sleep(1.5)
        	# result_field = driver.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "tr.dxgvDataRow_SisTheme td")))
        	try:
        		row = driver.find_element_by_xpath('//*[@id="MainContent_gvStudents_DXDataRow0"]')
        		cells = row.find_elements(By.CLASS_NAME, "dxgv")
        		f.write(cells[0].text + "," + cells[1].text + "," +
        			  cells[2].text + "," + cells[3].text + "," +
        			  cells[4].text + "," + cells[5].text + "," +
        			  cells[6].text + "," + cells[7].text + "," + str(cohort))
        		f.write('\n')
        		print(cells[0].text)
        	except NoSuchElementException:
        		print("No data to display")
	        input.clear()
    except TimeoutException:
        print("Box or Button not found in google.com")
 
def main(argv):
	driver = init_driver()
	cohort = argv[0]
	start  = argv[1]
	end    = argv[2]
	get_student(driver, cohort, start, end)
	time.sleep(5)
	driver.quit()

if __name__ == "__main__":
    main(sys.argv[1:])
