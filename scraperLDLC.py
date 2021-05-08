from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fuzzywuzzy import fuzz
import time
from csv import DictReader
from csv import DictWriter
import pandas as pd
import csv

def get_GPU_price(GPUmodel, **data):
	marketName=data['name']
	marketURL=data['url']
	marketSearch=data['barsearch_css_selector']
	marketResults=data['results_css_selector']
	marketElement=data['element_css_selector']
	imageTagName=data['image_tag_name']
	urlAttr=data['image_attr']
	titleAttr=data['title']
	priceSelector=data['price_css_selector']
	print("on cherche la carte graphique '"+ GPUmodel + "' à "+ marketName)
	prices=[]
	PATH="/Users/Shared/Files From d.localized/matchers/pappers&pj/chromedriver"
	#/*** CODE FOR HEADLESS CHROME ---------------------------------------- */
	# user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
	# options = webdriver.ChromeOptions()
	# options.headless = True
	# options.add_argument(f'user-agent={user_agent}')
	# options.add_argument("--window-size=1920,1080")
	# options.add_argument('--ignore-certificate-errors')
	# options.add_argument('--allow-running-insecure-content')
	# options.add_argument("--disable-extensions")
	# options.add_argument("--proxy-server='direct://'")
	# options.add_argument("--proxy-bypass-list=*")
	# options.add_argument("--start-maximized")
	# options.add_argument('--disable-gpu')
	# options.add_argument('--disable-dev-shm-usage')
	# options.add_argument('--no-sandbox')
	# driver = webdriver.Chrome(executable_path=PATH, options=options)
	#/** ------------------------------------------------------------ */
	driver=webdriver.Chrome(PATH)
	driver.get(marketURL)
	#driver.find_element_by_id("checkbox").click()
	#print(driver.title)
	#quoi=driver.find_element_by_name("search[search_text]")
	quoi=driver.find_element_by_css_selector(marketSearch)
	#driver.find_element_by_xpath('//*[@id="didomi-notice-agree-button"]').click()
	quoi.send_keys(GPUmodel)
	quoi.send_keys(Keys.RETURN)
	try:
		results=WebDriverWait(driver, 50).until(
			EC.presence_of_element_located((By.CSS_SELECTOR, marketResults))
			)
		print("/** i found results */")
		elements=results.find_elements_by_css_selector(marketElement)
		print(type(elements))
		print(len(elements))

		for element in elements:

			print("-----parsing element------")
			image_url=element.find_element_by_tag_name(imageTagName).get_attribute(urlAttr)
			print("image_url: "+image_url)
			title=element.find_element_by_tag_name(imageTagName).get_attribute(titleAttr)
			print("title: "+title)
			ratio=fuzz.token_set_ratio(title,GPUmodel)
			if(ratio>=80):
				print("l'élément de résultat matche le modèle de la carte graphic :) (score="+str(ratio)+")")
				price=element.find_element_by_css_selector(priceSelector).text
				print(type(price))
				price=price.replace("€", ".")
				print(price)
				prices.append(float(price))
				print("-----end element------")
			else:
				print("l'élément de résultat ne matche pas le modèle de la carte graphic :( (score="+str(ratio)+")")
				print("-----end element------")
				break;


		
	finally:
		#print("/** im in finally */")
		#time.sleep(10)
		driver.quit()
		#print(prices)
		return min(prices, default=40000.00)

def get_lowest_price(GPUmodel):

	markets=[
				{
					"name":"ldlc",
					"url":"https://www.ldlc.com/",
					"barsearch_css_selector":"input[name='search[search_text]']",
					"results_css_selector":"div[class='listing-product']",
					"element_css_selector":"li[class='pdt-item']",
					"image_tag_name":"img",
					"image_attr":"src",
					"title":"alt",
					"price_css_selector":"div[class='price']"
				},
				{
					"name":"cdiscount",
					"url":"https://www.cdiscount.com/",
					"barsearch_css_selector":"input[type='search']",
					"results_css_selector":"ul[id='lpBloc']",
					"element_css_selector":"li[data-sku]",
					"image_tag_name":"img",
					"image_attr":"src",
					"title":"alt",
					"price_css_selector":"div[class='prdtBILPrice']"


				}
	]
	return min(filter(None,[get_GPU_price(GPUmodel, **markets[0]),get_GPU_price(GPUmodel, **markets[1])]))



print(get_lowest_price("rtx 3060"))
