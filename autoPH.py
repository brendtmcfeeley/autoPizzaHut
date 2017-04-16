from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import math
import time
import json

driver = webdriver.Chrome()


def finalize():
	#driver.find_element_by_id('order_is_confirmed').click()
	#driver.find_element_by_id('place-order').click()


def setCardYearExp(yearExp):
	return '20' + yearExp


def setCardMonthExp(monthExp):
	if monthExp[0] == '0':
		return monthExp[1]
	else:
		return monthExp

def calculateTip():
	totalField = driver.find_element_by_id('amount_on_cc').get_attribute('value')
	tax = (int(float(totalField)) * 0.045)
	subTotal = (int(float(totalField)) - tax)
	calculatedTip = math.ceil(subTotal * 0.15) #15% tip
	return calculatedTip

def checkout(firstName, lastName, emailAddr, billingAddr, secondAddress, phoneNo, cardType, cardNo, cardMonthExp, cardYearExp, cardSec, city, cardZip):
	driver.find_element_by_id('btn-add').click()
	driver.get('https://eat.pizzahuthawaii.com/orders/996419/checkout/account')
	driver.find_element_by_id('order_guest_name').send_keys('Brendt McFeeley')
	driver.find_element_by_id('order_guest_email').send_keys(emailAddr)
	driver.find_element_by_id('order_guest_email_confirm').send_keys(emailAddr)
	driver.find_element_by_id('order_guest_phone_number').send_keys(phoneNo)
	driver.find_element_by_class_name('gold-rounded-button').click()
	driver.find_element_by_id('pickup_now').click()
	driver.find_element_by_id('pickup_now').send_keys(Keys.ENTER)

	tip = calculateTip()
	
	driver.find_element_by_id('amount_on_tip').send_keys(Keys.CONTROL+'a')
	driver.find_element_by_id('amount_on_tip').send_keys(tip)
	selectCard = Select(driver.find_element_by_id('card_type'))
	selectCard.select_by_value('Visa')
	driver.find_element_by_id('_ticket_account').send_keys(cardNo)
	driver.find_element_by_id('name_on_card').send_keys('Brendt McFeeley')
	selectExpMonth = Select(driver.find_element_by_id('expiration_month'))
	selectExpMonth.select_by_value(cardMonthExp)
	selectExpYear = Select(driver.find_element_by_id('expiration_year'))
	selectExpYear.select_by_value(cardYearExp)
	driver.find_element_by_id('security_code').send_keys(cardSec)
	driver.find_element_by_id('order_address_line1_1').send_keys(billingAddr)
	driver.find_element_by_id('order_address_line1_1').send_keys(secondAddress)
	driver.find_element_by_id('order_address_city_1').send_keys(city)
	driver.find_element_by_id('order_address_zip_1').send_keys(cardZip)
	driver.find_element_by_id('order_address_zip_1').send_keys(Keys.ENTER)

def addToCart():
	body = driver.find_element_by_css_selector('body')
	body.click()
	driver.get('https://eat.pizzahuthawaii.com/orders/996318/items/choices?category_id=26&item_id=3457')
	selectMenu = Select(driver.find_element_by_id('item_721'))
	selectMenu.select_by_value('1')
	#selectMenu.select_by_visible_text('1')

def findStore(zipCode, streetNo, streetName, secondAddress):
	driver.find_element_by_id('order_address_attributes_zip').send_keys(zipCode)
	driver.find_element_by_id('street_number').send_keys(streetNo)
	driver.find_element_by_id('street_name').send_keys(streetName)
	time.sleep(1.5)
	driver.find_element_by_id('order_address_attributes_line2').send_keys(secondAddress)
	driver.find_element_by_id('order_address_attributes_line2').send_keys(Keys.ENTER)

def main():
	driver.get('https://eat.pizzahuthawaii.com/orders/new');

	with open('custInfo.json') as data_file:
		dataStream = json.load(data_file)

	firstName = dataStream[0]['custInfo']['firstName']
	lastName = dataStream[0]['custInfo']['lastName']
	emalAddr = dataStream[0]['custInfo']['email']
	phoneNo = dataStream[0]['custInfo']['phone']
	streetNo = dataStream[0]['custInfo']['address']['streetNo']
	streetName = dataStream[0]['custInfo']['address']['streetName']
	secondAddress = dataStream[0]['custInfo']['address']['addressNoTwo']
	city = dataStream[0]['custInfo']['address']['city']
	zipCode = dataStream[0]['custInfo']['address']['zipCode']
	cardType = dataStream[0]['cardInfo']['cardType']
	cardNo = dataStream[0]['cardInfo']['cardNo']
	cardMonthExp = dataStream[0]['cardInfo']['cardMonthExp']
	cardYearExp = dataStream[0]['cardInfo']['cardYearExp']
	cardSec = dataStream[0]['cardInfo']['cardSec']
	cardZip = dataStream[0]['cardInfo']['cardZip']

	dashMAC = 0
	order = 0
	
	correctedExpMonth = setCardMonthExp(cardMonthExp)
	correctedExpYear = setCardYearExp(cardYearExp)

	billingAddr = streetNo + " " + streetName

	findStore(zipCode, streetNo, streetName, secondAddress)
	addToCart()
	checkout(firstName, lastName, emalAddr, billingAddr, secondAddress, phoneNo, cardType, cardNo, correctedExpMonth, correctedExpYear, cardSec, city, cardZip)
	finalize()
	#driver.quit()

if __name__ == '__main__':
    main()
