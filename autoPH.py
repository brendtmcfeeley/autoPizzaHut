from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

'''
seperate all the pages into different functions at the end
add error checking later
implemen api
'''

driver = webdriver.Chrome()

def menuPage():
	body = driver.find_element_by_css_selector('body')
	body.click()
	driver.get('https://eat.pizzahuthawaii.com/orders/996318/items/choices?category_id=26&item_id=3457')

def findStore():
	driver.find_element_by_id('order_address_attributes_zip').send_keys('96822')
	driver.find_element_by_id('street_number').send_keys('2569')
	time.sleep(1)
	driver.find_element_by_id('street_name').send_keys('Dole St')
	time.sleep(1)
	driver.find_element_by_id('order_address_attributes_line2').send_keys('Frear Hall')
	driver.find_element_by_id('order_address_attributes_line2').send_keys(Keys.ENTER)

def main():
	driver.get('https://eat.pizzahuthawaii.com/orders/new');

	findStore()
	time.sleep(4)
	menuPage()

if __name__ == '__main__':
    main()


"""
textPad = driver.find_element_by_id('text')
textPad.send_keys(Keys.CONTROL+'a')
textPad.send_keys('kys')
textPad.send_keys(Keys.ENTER)
textPad.send_keys('hehe xd')
time.sleep(2)
driver.quit()
search_box.send_keys('ChromeDriver')
search_box.submit()
time.sleep(5) # Let the user actually see something!

driver.quit()
"""