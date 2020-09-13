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
	chromedriver = "/Users/dhawalmajithia/Desktop/works/test/ef_scrap/chromedriver"
	driver = webdriver.Chrome(chromedriver, options=options)
	driver.get(link)
	time.sleep(5)
	return driver

class Destination():
	def __init__(self,dlink):
		self.url = dlink
		self.name = ""
		self.years = set()
		self.dates = {}
		self.load()

	# @threaded
	def load(self):
		driver = get_driver(self.url)
		try:
			self.name = WebDriverWait(driver, 10).until(
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
				print(b.text)
				self.years.add(b.text)
		finally:
			driver.quit()
			# b.click()

def foo():
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
		d = Destination(l)
		if len(d.name) > 0:
			dests.append(d)
	# dests = [f.result() for f in futures]
	end = time.time()
	print(f'It took {end - start} seconds!')
	return dests


	# places = []
	# years = set()

	# for dest in destinations:
	# 	driver.get(dest)
	# 	time.sleep(2)
	# 	trip_name = driver.find_element_by_class_name(dest_title_class).text
	# 	print(trip_name)
	# 	valid = False
	# 	try:
	# 		# 'iYkdPv' is class name for all years labels
	# 		year_buttons = driver.find_elements_by_class_name(year_buttons_class)
	# 		print(','.join([b.text for b in year_buttons]))
	# 		year_buttons = [b for b in year_buttons if b.text=='2021']
	# 		if len(year_buttons) == 1:
	# 			year_buttons[0].click()
	# 			valid = True
	# 			places.append({"name":trip_name,"url":dest})
	# 	except:
	# 		print("HTML error!")
	# 	if not valid:
	# 		print('invalid')
	# return places
	# # print("\n\n # places = " + str(len(places.keys())))
	# # print("Printing trip names: ")
	# # for p in places:
	# # 	print(p["name"])


# year-selector__YearButton-sv0ryn-2
# year-selector-button-2021
# iYkdPv