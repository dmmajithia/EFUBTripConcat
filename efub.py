# Local module imports
from chromedriver import ChromeDriver
from threads import threaded as Threaded
import constants as Constants
from tour import Tour
# Built-in module imports
import time

class EFUltimateBreak():
	def __init__(self, max_drivers=10, timeout=180):
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
		tour_links_infos_futures = [self.get_tour_links_infos_from_page(n) 
								for n in range(self.num_pages)]
		tour_links_infos_by_page = [future.result() for future in tour_links_infos_futures]
		self.tour_links_infos = []
		for page in tour_links_infos_by_page:
			self.tour_links_infos += page
		self.tours = [Tour(tour_link, tour_info, self.chromedriver) for tour_link, tour_info in self.tour_links_infos]
		_ = [tour.start_scrape() for tour in self.tours]

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
	def get_tour_links_infos_from_page(self, page_number):
		# Returns links to tours on page_number'th explore page.
		tour_links = []
		driver = self.chromedriver.get_driver(f'{self.link}?results-page={page_number}')

		if self.chromedriver.wait_for_element_class_like(driver, 
			Constants.tour_tile_links, 'a').result():
			
			tour_link_elements = self.chromedriver.get_elements_matching_class(driver, 
				Constants.tour_tile_links, 'a')
			tour_links = [t.get_attribute('href') for t in tour_link_elements]

			tour_info_elements = self.chromedriver.get_elements_matching_class(driver, 
				Constants.tour_tile_info_p, 'p')
			tour_infos = [t.get_attribute('textContent') for t in tour_info_elements]

		self.chromedriver.quit_driver(driver)
		if len(tour_links) < 1:
			print(f'Tour Links Error: Could not load any links from page {page_number}.')
		if len(tour_infos) < 1:
			print(f'Tour Infos Error: Could not load any infos from page {page_number}.')
		if len(tour_links) != len(tour_infos):
			print(f'Tour Links&Infos Error: # of links and infos do not match on page {page_number}.')
		return list(zip(tour_links, tour_infos))

	def stat_tours_scrape(self):
		return self.num_done_tours()==len(self.tours)

	def num_done_tours(self):
		c = sum([1 for tour in self.tours if tour.done])
		return c



























