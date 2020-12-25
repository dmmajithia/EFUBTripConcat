# Local module imports
from threads import threaded as Threaded
import constants as Constants

class Tour():
	def __init__(self, link, info, chromedriver):
		self.link = link
		self.info = info
		self.chromedriver = chromedriver
		self.done = False
		self.error = False

	@Threaded
	def start_scrape(self):
		driver = self.chromedriver.get_driver(self.link)
		self.tour_name = self.get_tour_name(driver)
		# self.tour_fast_facts = self.get_tour_fast_facts(driver)
		self.num_cities, self.num_days = self.parse_tour_info()
		self.chromedriver.quit_driver(driver)
		self.done = True

	def get_tour_name(self, driver):
		self.chromedriver.flush_popups(driver)
		if self.chromedriver.wait_for_element_class_like(driver, 
			Constants.tour_name_h1, element_type='h1').result():
			self.chromedriver.flush_popups(driver)
			tour_name_element = self.chromedriver.get_elements_matching_class(driver, 
								Constants.tour_name_h1, 'h1')
			return tour_name_element[0].get_attribute('textContent').split('Saved')[0]
		else:
			print(f'Tour Error: Could not load name for link:\n {self.link}')
			self.error = True
			return 'Error'

	def parse_tour_info(self):
		info_split = self.info.split(',')
		num_cities, num_days = 0, 0
		for i in info_split:
			if 'days' in i or 'day' in i:
				num_days = int(i.split()[0])
			elif 'cities' in i or 'city' in i:
				num_cities = int(i.split()[0])
		return num_cities, num_days


	def get_tour_fast_facts(self, driver):
		self.chromedriver.flush_popups(driver)
		if self.chromedriver.wait_for_element_class_like(driver, 
			Constants.tour_fast_facts_div, element_type='div').result():
			self.chromedriver.flush_popups(driver)
			tour_fast_facts_element = self.chromedriver.get_elements_matching_class(driver, 
								Constants.tour_fast_facts_div, 'div')
			return tour_fast_facts_element[0].get_attribute('textContent')
		else:
			print(f'Tour Error: Could not load fast facts for link:\n {self.link}')
			self.error = True
			return 'Error'