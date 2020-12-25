#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from threading import Thread
from concurrent.futures import Future
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONSTANTS
dests_class = "tour-tile__TileContainer-henuwi-3"
dest_title_class = "itinerary-header__Title-wtfiof-5"
year_buttons_class = "iYkdPv"
date_li_class = "departure-selector__DepartureListItem-vtvk14-3"
date_start_end_class = "departure-date__InnerDateDiv-sc-1a35nt3-7"
date_avail_class = "departure-date__Availability-sc-1a35nt3-2"
# chromedriver = "/Users/dhawalmajithia/Desktop/works/test/ef_scrap/EFUBTripConcat/chromedriver"
chromedriver = "~/bin/chromedriver"

# threading related source from - 
# https://stackoverflow.com/questions/19846332/python-threading-inside-a-class
def call_with_future(fn, future, args, kwargs):
	try:
		result = fn(*args, **kwargs)
		future.set_result(result)
	except Exception as exc:
		future.set_exception(exc)

def threaded(fn):
	def wrapper(*args, **kwargs):
		future = Future()
		Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
		return future
	return wrapper


def get_driver(link):
	options = Options()
	options.add_argument('--headless')
	options.add_argument('--no-sandbox')
	options.add_argument('window-size=1920x1080')
	driver = webdriver.Chrome(options=options)
	driver.get(link)
	time.sleep(5)
	return driver

class TripDate():
	def __init__(self,date_list_item,year):
		x = date_list_item.find_elements_by_class_name(date_start_end_class)
		self.start = x[0].get_attribute('textContent')
		self.end = x[1].get_attribute('textContent')
		self.avail = date_list_item.find_element_by_class_name(date_avail_class).get_attribute('textContent')
		self.year = year
	def print(self):
		print(self.year + ' ' + self.start + ' - ' + self.end + '    ' + self.avail)

class Destination():
	def __init__(self,dlink,t):
		self.url = dlink
		self.name = ""
		self.years = set()
		self.dates = {}
		self.t = t
		self.load()

	# @threaded
	def load(self):
		driver = get_driver(self.url)
		try:
			self.name = WebDriverWait(driver, self.t).until(
				EC.presence_of_element_located((By.CLASS_NAME, dest_title_class))
			)
			if not self.name:
				print("Could not load page - " + self.url)
				driver.quit()
				return
			else:
				self.name = self.name.text
			# self.name = self.driver.find_element_by_class_name(dest_title_class).text
			print(self.name)
			year_buttons = driver.find_elements_by_class_name(year_buttons_class)
			for b in year_buttons:
				year = b.text
				print(year)
				self.years.add(year)
				# b.click()
				# time.sleep(0.05)
				# ds = driver.find_elements_by_class_name(date_li_class)
				# for d in ds:
				# 	self.dates[year] = self.dates.get(year,[]) + [TripDate(d,year)]
		finally:
			driver.quit()
			# b.click()

def foo(t=10):
	start = time.time()
	ef_explore = "https://www.efultimatebreak.com/explore"
	driver = get_driver(ef_explore)
	dlinks = driver.find_elements_by_class_name(dests_class)
	dlinks = [d.get_attribute('href') for d in dlinks]
	driver.quit()
	dests = []
	futures = []
	for l in dlinks:
		# futures.append(Destination(l).load())
		d = Destination(l,t)
		if len(d.name) > 0:
			dests.append(d)
	# dests = [f.result() for f in futures]
	end = time.time()
	print(f'It took {end - start} seconds!')
	return dests

def save_dests(places, fname='p1.txt'):
	with open(fname,'a') as f:
		for p in places:
			f.write('#n-'+p.name+'\n')
			f.write('#u-'+p.url+'\n')
			for y in p.years:
				f.write('#y-'+y+'\n')
				for d in p.dates[y]:
					f.write('#s-'+d.start+'\n')
					f.write('#e-'+d.end+'\n')
					f.write('#a-'+d.avail+'\n')



























