# Local module imports
from chromedriver import ChromeDriver
from threads import threaded as Threaded
import constants as Constants
# Built-in module imports
import time

class EFUltimateBreak():
	def __init__(self, max_drivers=5, timeout=10):
		self.max_drivers = max_drivers
		self.timeout = timeout
		self.chromedriver = ChromeDriver(max_drivers=max_drivers, timeout=timeout)


	def start_scrape(self, link='https://www.efultimatebreak.com/explore'):
		self.link = link
		driver = self.chromedriver.get_driver(self.link)
		if driver is None:
			print('ChromeDriver Error: Could not load link.')
			self.chromedriver.quit_driver(driver)
			return
		self.num_pages = self.get_num_pages(driver)
		self.chromedriver.quit_driver(driver)
		tour_links_futures = [self.get_tour_links_from_page(n) 
								for n in range(self.num_pages)]
		self.tour_links = [future.result() for future in tour_links_futures]


	def get_num_pages(self, driver):
		# Returns number of pages available in explore section.
		page_numbers = 0

		if self.chromedriver.wait_for_element_class_like(driver, 
			Constants.page_number_links, 'a').result():

			page_number_elements = self.chromedriver.get_elements_matching_class(driver, 
				Constants.page_number_links, 'a')

			num_pages = len(page_number_elements)-4
			# there are four directional buttons and the rest are page buttons
		print(f'Found {num_pages} pages.')
		return num_pages

	@Threaded
	def get_tour_links_from_page(self, page_number):
		# Returns links to tours on page_number'th explore page.
		tour_links = []
		driver = self.chromedriver.get_driver(f'{self.link}?results-page={page_number}')

		if self.chromedriver.wait_for_element_class_like(driver, 
			Constants.tour_tile_links, 'a').result():
			
			tour_link_elements = self.chromedriver.get_elements_matching_class(driver, 
				Constants.tour_tile_links, 'a')
			tour_links = [t.get_attribute('href') for t in tour_link_elements]

		self.chromedriver.quit_driver(driver)
		if len(tour_links) < 1:
			print(f'Tour Links Error: Could not load any links from page {page_number}')
		return tour_links



























