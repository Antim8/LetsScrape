from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time




def get_number(String: str) -> float:
	"""This function returns the numbers of type float which appear in the given String. Lieferando.de uses the german format to represent point numbers, therefore "," will be transformed to ".".
	 Only works for the german format."""
    #TODO Error potential if more than one , 
	result = ''.join(x for x in String if x.isdigit() or x == ',')
	if result == "":
		return -1.0
	result = float(result.replace(',','.'))
	return result

# TODO time.sleep ersetzen
def restaurants(adress: str) -> list:
	"""This funtion will return a list of tuples.
	Each tuple represents one restaurant which can be found at the input variable (adress) on Lieferando.de.
	One tuple has the form: (restaurant_name: str, [type_kitchen1: str, type_kitchen2: str, ...]: list,
							time_of_delivery: int, delivery_costs: float, min_order_value: float,
							rating: float, number_of_ratings: int): tuple.
	"""

	# Copy the path of the chromedriver in here
	PATH = "chromedriver_91.exe"  
	driver = webdriver.Chrome(executable_path=PATH) 
	# Enter adress on Lieferando and search for it
	driver.get("https://www.lieferando.de")
	search = driver.find_element_by_id("imysearchstring")
	search.click()
	search.send_keys(adress)
	time.sleep(2)
	search.send_keys(Keys.ENTER)

    #TODO Check if there is a nicer way to wait, might also fail if the brower/internet is slow
	#time.sleep(2) # seconds

	#driver.find_element_by_id("submit_deliveryarea").click()

	time.sleep(2) # seconds

	restaurants = []

	# create entrys for every restaurant found
	for restaurant in driver.find_elements_by_class_name("restaurant.js-restaurant"):

		try:
			restaurant_name = restaurant.find_element_by_class_name("restaurantname").text
		except NoSuchElementException:
			restaurant_name = None

		try:

			kitchen =  restaurant.find_element_by_class_name("kitchens").text
			kitchen = kitchen.split(", ")

		except NoSuchElementException:
			kitchen = None

		try: 

			delivery_time = restaurant.find_element_by_class_name("avgdeliverytime.avgdeliverytimefull.open").text
			
			if delivery_time.startswith("Ab") or delivery_time.startswith("From"):
				delivery_time = -1
			else:
				delivery_time = int(get_number(delivery_time))

		except NoSuchElementException:
			delivery_time = -1

		try: 
			delivery_cost = get_number(restaurant.find_element_by_class_name("delivery-cost.js-delivery-cost.notranslate").text)
		except NoSuchElementException:
			delivery_cost = -1

		try: 
			min_order = get_number(restaurant.find_element_by_class_name("min-order.notranslate").text)
		except NoSuchElementException:
			min_order = -1

		try:
			rating = get_number(restaurant.find_element_by_class_name("review-stars-range").get_attribute("style")) / 20
		except NoSuchElementException:
			rating = -1

		try:
			num_of_rating = int(get_number(restaurant.find_element_by_class_name("rating-total").text))
		except NoSuchElementException:
			num_of_rating = -1

		restaurant_tuple = (restaurant_name, kitchen, delivery_time, delivery_cost, min_order, rating, num_of_rating)
		restaurants.append(restaurant_tuple)

	driver.quit()
	restaurants = restaurants[:-1]

	return restaurants


	


if __name__ == '__main__':
	print(restaurants("Osnabrück"))
	












