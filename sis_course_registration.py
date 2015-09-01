import sys
import time
import codecs
import pprint
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

def crawl(driver, cohort, start, end):
	driver.get("http://sis.hust.edu.vn/ModuleSearch/StudentRegister.aspx")
	ids = make_id_list(cohort, start, end)
	file = codecs.open(cohort + '_course_registration.csv', 'a', 'utf-8')
	
	for id in ids:
		get_registration(driver, id, file)

	file.close()

def get_registration(driver, id, file):
	try:
		# The student id input field
		input = driver.wait.until(EC.presence_of_element_located((By.NAME, "ctl00$MainContent$tbStudentID")))
		input.send_keys(id)
		input.send_keys(Keys.RETURN)
		time.sleep(2)
		try:
			rows = driver.find_elements(By.CSS_SELECTOR, "tr.dxgvDataRow_SisTheme")
			student = ''

			for row in rows:
				row_height = row.size['height']
				if row_height == 0:
					continue
				cells	     = row.find_elements_by_class_name("dxgv")
				student_id   = cells[1].text
				class_id     = cells[4].text
				course_id    = cells[6].text
				course_title = cells[7].text
				class_type   = cells[8].text
				reg_status   = cells[10].text
				
				str_to_write = student_id + '|' + class_id + '|' + class_type + '|' + course_id + '|' + course_title + '|' reg_status + '\n'
				file.write(str_to_write)
				student = student_id

			print("Get: " + student)

		except NoSuchElementException:
			print("No data to display")

		input.clear()
	except TimeoutException:
		print("Timeout for retrieving student's class registration list")
def main(argv):
	driver = init_driver()
	cohort = argv[0]
	start  = argv[1]
	end    = argv[2]

	crawl(driver, cohort, start, end)

	time.sleep(5)
	driver.quit()

if __name__ == "__main__":
    main(sys.argv[1:])
