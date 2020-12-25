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
		tour_year_elements = self.get_year_elements(driver)
		self.chromedriver.quit_driver(driver)
		dates_info_futures = [self.get_dates_info(year, el_id) 
								for year,el_id in tour_year_elements.items()]
		self.dates_info = []
		for f in dates_info_futures:
			self.dates_info += f.result()
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
			print(f'Tour Error: Could not load NAME for link:\n {self.link}')
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

	
	def get_year_elements(self, driver):
		# returns dictionary {year:element_id}
		self.chromedriver.flush_popups(driver)

		if self.chromedriver.wait_for_element_class_like(driver, 
			Constants.tour_year_radio_input, element_type='input').result():

			self.chromedriver.flush_popups(driver)
			tour_year_radio_inputs = self.chromedriver.get_elements_matching_class(driver, 
								Constants.tour_year_radio_input, 'input')
			return {i.get_attribute('value'):i.get_attribute('id') for i in tour_year_radio_inputs}
		else:
			print(f'Tour Error: Could not load YEAR elements for link:\n {self.link}')
			self.error = True
			return {'Error':'Error'}

	@Threaded
	def get_dates_info(self, year, year_input_element_id):
		year = str(year)
		driver = self.chromedriver.get_driver(self.link)
		self.chromedriver.flush_popups(driver)
		if self.chromedriver.wait_for_element_class_like(driver, 
			Constants.tour_year_radio_input, element_type='input').result():
			self.chromedriver.flush_popups(driver)
			# self.chromedriver.click_element_id(year_input_element_id)
			driver.execute_script(f"return document.querySelector('input[id^={year_input_element_id}]')"+".click({});")
			if not self.chromedriver.wait_for_element_class_like(driver, 
					Constants.tour_flight_option_class, element_type='option').result():
				print('Flights Error: Could not find No Flights Included option.')
			gateways = self.chromedriver.get_elements_matching_class(driver, 
								Constants.tour_flight_option_class, 'option')
			_ = [option.click() for option in gateways if option.get_attribute('value') == Constants.tour_no_flight_option_value]
			if not self.chromedriver.wait_for_element_class_like(driver, 
					Constants.tour_date_div, element_type='div').result():
				print('Dates Error: Could not find Dates div.')
			dates = self.chromedriver.get_elements_matching_class(driver, 
								Constants.tour_date_div, 'div')
			prices = self.chromedriver.get_elements_matching_class(driver, 
								Constants.tour_price_div, 'div')
			addl_info = self.chromedriver.get_elements_matching_class(driver, 
								Constants.tour_addl_info_div, 'div')
			dates = [d.get_attribute('textContent') for d in dates]
			dates = [{'start':' '.join([dates[i*2][:3], dates[i*2][3:], year]), 'end':' '.join([dates[i*2+1][:3], dates[i*2+1][3:], year])} 
						for i in range(int(len(dates)/2))]
			prices = [int(p.get_attribute('textContent').split('$')[-1]) for p in prices]
			addl_info = [i.get_attribute('textContent') for i in addl_info]
			year_dates_info = []
			for i in range(len(dates)):
				year_dates_info.append({'dates': dates[i],
										'price': prices[i],
										'addl_info': addl_info[i]})
			self.chromedriver.quit_driver(driver)
			return year_dates_info

		else:
			print(f'Tour Error: Could not load DATES INFO for {year} for link:\n {self.link}')
			self.error = True
		self.chromedriver.quit_driver(driver)
		return []

	# def parse_date_wrapper(self, date_wrapper_element):


	# def get_tour_fast_facts(self, driver):
	# 	self.chromedriver.flush_popups(driver)
	# 	if self.chromedriver.wait_for_element_class_like(driver, 
	# 		Constants.tour_fast_facts_div, element_type='div').result():
	# 		self.chromedriver.flush_popups(driver)
	# 		tour_fast_facts_element = self.chromedriver.get_elements_matching_class(driver, 
	# 							Constants.tour_fast_facts_div, 'div')
	# 		return tour_fast_facts_element[0].get_attribute('textContent')
	# 	else:
	# 		print(f'Tour Error: Could not load fast facts for link:\n {self.link}')
	# 		self.error = True
	# 		return 'Error'