from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import math
import time
import json

driver = webdriver.Chrome()

with open('custInfo.json') as data_file:
	dataStream = json.load(data_file)

def assignCustInfo():
	custInfo = []

	custInfo.append(dataStream[0]['custInfo']['firstName']) #0
	custInfo.append(dataStream[0]['custInfo']['lastName']) #1
	custInfo.append(dataStream[0]['custInfo']['email']) #2
	custInfo.append(dataStream[0]['custInfo']['phone']) #3
	custInfo.append(dataStream[0]['custInfo']['address']['streetNo']) #4
	custInfo.append(dataStream[0]['custInfo']['address']['streetName']) #5
	custInfo.append(dataStream[0]['custInfo']['address']['addressNoTwo']) #6
	custInfo.append(dataStream[0]['custInfo']['address']['city']) #7
	custInfo.append(dataStream[0]['custInfo']['address']['zipCode']) #8

	#order =

	return custInfo

def assignCardInfo():
	cardInfo = []

	cardInfo.append(dataStream[0]['cardInfo']['cardType']) #0
	cardInfo.append(dataStream[0]['cardInfo']['cardNo']) #1
	cardInfo.append(dataStream[0]['cardInfo']['cardMonthExp']) #2
	cardInfo.append(dataStream[0]['cardInfo']['cardYearExp']) #3
	cardInfo.append(dataStream[0]['cardInfo']['cardSec']) #4
	cardInfo.append(dataStream[0]['cardInfo']['cardZip']) #5

	return cardInfo

def finalize():
	driver.find_element_by_id('order_is_confirmed').click()
	driver.find_element_by_id('place-order').click()

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

def checkout(custInfo, cardInfo):
	driver.find_element_by_id('btn-add').click()
	driver.get('https://eat.pizzahuthawaii.com/orders/996419/checkout/account')
	driver.find_element_by_id('order_guest_name').send_keys(custInfo[0] + " " + custInfo[1])
	driver.find_element_by_id('order_guest_email').send_keys(custInfo[2])
	driver.find_element_by_id('order_guest_email_confirm').send_keys(custInfo[2])
	driver.find_element_by_id('order_guest_phone_number').send_keys(custInfo[3])

	driver.find_element_by_class_name('gold-rounded-button').click()
	driver.find_element_by_id('pickup_now').click()
	driver.find_element_by_id('pickup_now').send_keys(Keys.ENTER)

	tip = calculateTip()
	
	driver.find_element_by_id('amount_on_tip').send_keys(Keys.CONTROL+'a')
	driver.find_element_by_id('amount_on_tip').send_keys(tip)
	selectCard = Select(driver.find_element_by_id('card_type'))
	selectCard.select_by_value(cardInfo[0])
	driver.find_element_by_id('_ticket_account').send_keys(cardInfo[1])
	driver.find_element_by_id('name_on_card').send_keys(custInfo[0] + " " + custInfo[1])
	selectExpMonth = Select(driver.find_element_by_id('expiration_month'))
	selectExpMonth.select_by_value(cardInfo[2])
	selectExpYear = Select(driver.find_element_by_id('expiration_year'))
	selectExpYear.select_by_value(cardInfo[3])
	driver.find_element_by_id('security_code').send_keys(cardInfo[4])
	driver.find_element_by_id('order_address_line1_1').send_keys(custInfo[4] + " " + custInfo[5])
	driver.find_element_by_id('order_address_line1_1').send_keys(custInfo[6])
	driver.find_element_by_id('order_address_city_1').send_keys(custInfo[7])
	driver.find_element_by_id('order_address_zip_1').send_keys(cardInfo[5])
	driver.find_element_by_id('order_address_zip_1').send_keys(Keys.ENTER)


def addToCart():
	body = driver.find_element_by_css_selector('body')
	body.click()
	driver.get('https://eat.pizzahuthawaii.com/orders/996318/items/choices?category_id=26&item_id=3457')
	selectMenu = Select(driver.find_element_by_id('item_721'))
	selectMenu.select_by_value('1')
	#selectMenu.select_by_visible_text('1')

def findStore(custInfo):
	driver.find_element_by_id('order_address_attributes_zip').send_keys(custInfo[8])
	driver.find_element_by_id('street_number').send_keys(custInfo[4])
	driver.find_element_by_id('street_name').send_keys(custInfo[5])
	time.sleep(1.5)
	driver.find_element_by_id('order_address_attributes_line2').send_keys(custInfo[6])
	driver.find_element_by_id('order_address_attributes_line2').send_keys(Keys.ENTER)

def main():
	driver.get('https://eat.pizzahuthawaii.com/orders/new');

	custInfo = assignCustInfo()
	cardInfo = assignCardInfo()

	correctedExpMonth = setCardMonthExp(cardInfo[2])
	correctedExpYear = setCardYearExp(cardInfo[3])

	cardInfo[2] = correctedExpMonth
	cardInfo[3] = correctedExpYear

	billingAddr = custInfo[4] + " " + custInfo[5]

	findStore(custInfo)
	addToCart()
	checkout(custInfo, cardInfo)
	finalize()
	driver.quit()

if __name__ == '__main__':
    main()
