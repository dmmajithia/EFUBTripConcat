# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import _find_element
# Built-in module imports
from threading import Semaphore
import time
import re
# Local module imports
from threads import threaded as Threaded

# chromedriver = "~/bin/chromedriver"
# chromedriver = "/Users/dhawalmajithia/Desktop/works/test/ef_scrap/EFUBTripConcat/chromedriver"

class class_regex_match(object):
	# Base code from the below url:
	# https://stackoverflow.com/questions/28240342/perform-a-webdriverwait-or-similar-check-on-a-regular-expression-in-python
	# This function is used in ChromeDiver.wait_for_element.
	def __init__(self, get_elements_matching_class, class_str, element_type):
		self.class_str = class_str
		self.element_type = element_type
		self.get_elements_matching_class = get_elements_matching_class

	def __call__(self, driver):
		# return driver.execute_script(f"document.querySelectorAll('div[class^=\"{self.regexp}\"]').length;") > 0
		matching_elements = self.get_elements_matching_class(driver, 
							self.class_str, self.element_type)
		return len(matching_elements) > 0

class ChromeDriver():
	
	def __init__(self, max_drivers, timeout):
		self.semaphore = Semaphore(value=max_drivers)
		self.timeout = timeout

	def get_driver(self, link):
		if self.semaphore.acquire(timeout=self.timeout):
			options = Options()
			options.add_argument('--headless')
			options.add_argument('--no-sandbox')
			options.add_argument('window-size=1920x1080')
			driver = webdriver.Chrome(options=options)
			driver.get(link)
			return driver
		else:
			return None

	def quit_driver(self, driver):
		driver.quit()
		self.semaphore.release()

	def get_elements_matching_class(self, driver, class_str, element_type=''):
		return driver.execute_script(f"return document.querySelectorAll('{element_type}[class^={class_str}]');")

	@Threaded
	def wait_for_element_class_like(self, driver, class_str, element_type=''):
		# Waits till any element class matching the given class_str and optional element_type appear.
		# If found, return element. Else return None.
		# Waiting is subject to timeout.
		if WebDriverWait(driver, self.timeout).until(
			class_regex_match(self.get_elements_matching_class, class_str, element_type)):
			return True
		else:
			return False














		
