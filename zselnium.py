import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
import requests
from bs4 import BeautifulSoup
import csv

def get_name(body):
    return body.find('span', {'class': 'jcn'}).a.string

def get_phone_number(body):
    try:
        phone = decode_phonenumber(body.find('p', {'class': 'contact-info'}).span.a.b)
        return phone
    except AttributeError:
        return ''

def decode_phonenumber(phone):
    try:
        main_phone = ""
        for span_tag in phone:
            main_class = span_tag.attrs['class']
            if 'icon-dc' in main_class:
                main_phone += "+"
            if 'icon-fe' in main_class:
                main_phone += "("
            if 'icon-hg' in main_class:
                main_phone += ")"
            if 'icon-yz' in main_class:
                main_phone += "1"
            if 'icon-wx' in main_class:
                main_phone += "2"
            if 'icon-vu' in main_class:
                main_phone += "3"
            if 'icon-ts' in main_class:
                main_phone += "4"
            if 'icon-rq' in main_class:
                main_phone += "5"
            if 'icon-po' in main_class:
                main_phone += "6"
            if 'icon-nm' in main_class:
                main_phone += "7"
            if 'icon-lk' in main_class:
                main_phone += "8"
            if 'icon-ji' in main_class:
                main_phone += "9"
            if 'icon-acb' in main_class:
                main_phone += "0"
        return main_phone
    except:
        return ''

def get_address(body):
    return body.find('span', {'class': 'mrehover'}).text.strip()

page_number = 1
service_count = 1

fields = ['Name', 'Phone', 'Address']
out_file = open('data.csv', 'w')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)

while True:

	if page_number > 50:
		break URL = "https://www.justdial.com/Kolkata/Home-Tutors/nct-10575643/page-%s" % (page_number)
	agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
	r = requests.get(URL, headers=agent)
	soup = BeautifulSoup(r.content, "html.parser")
	items = soup.find_all('li', {'class': 'cntanr'})

	for item in items:
		dict_service = {}
		name = get_name(item)
		phone = get_phone_number(item)
		address = get_address(item)
		if name != None:
			dict_service['Name'] = name
		if phone != None:
			
			dict_service['Phone'] = phone
		if address != None:
			dict_service['Address'] = address

		csvwriter.writerow(dict_service)

		print("#" + str(service_count) + " ", dict_service)
		service_count += 1

	page_number += 1

out_file.close()

	

