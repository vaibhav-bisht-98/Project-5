from selenium import webdriver
import pandas as pd 
import numpy as np 
from bs4 import BeautifulSoup
import requests
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver = 'C:\webdrivers\chromedriver'
driver = webdriver.Chrome(chromedriver)

'''Creating a function to extratc the odi record for the a player.The function takes name of the batsman and url to the stats webpage'''
def calc_rec(name,url):
	final_url = url.replace('PlayerOverview','PlayerYears')
	parser = BeautifulSoup(requests.get(final_url).content,'html.parser')

	table = parser.select('table')

	real_table = table[7]
	rows = real_table.select('tr')

	runs_by_year={}

	for i in range(1,len(rows)-1):
		year = rows[i].select('td')[0].text.strip()
		runs = rows[i].select('td')[8].text.strip()
		runs_by_year[year] = runs

	return runs_by_year

'''Creating a pandas DataFrame to store the information of a player'''
records = pd.DataFrame(columns = ['birth_date','country','1971','1972','1973','1974','1975','1976','1977','1978','1979',
									 '1980','1981','1982','1983','1984','1985','1986','1987','1988','1989',
									 '1990','1991','1992','1993','1994','1995','1996','1997','1998','1999',
									 '2000','2001','2002','2003','2004','2005','2006','2007','2008','2009',
									 '2010','2011','2012','2013','2014','2015','2016','2017','2018','2019',
									 ])
'''Iterating over the various letter searches for a player'''
for i in range(ord('A'),ord('Z')+1):
	char = chr(i)
	driver.get(f'http://howstat.com/cricket/Statistics/Players/PlayerList.asp?Country=ALL&Group={char}')
	table = driver.find_elements_by_css_selector('table')
	print(len(driver.find_elements_by_css_selector('table')))

	for row in table[6].find_elements_by_css_selector('tr')[2:-1]:
		print(row.find_elements_by_css_selector('td')[4].text)
		if row.find_elements_by_css_selector('td')[4].text != ' ' :
			name = row.find_elements_by_css_selector('td')[0].text
			records.loc[name,'birth_date'] = row.find_elements_by_css_selector('td')[1].text
			records.loc[name,'country'] = row.find_elements_by_css_selector('td')[2].text
			runs_by_year = calc_rec(name,row.find_elements_by_css_selector('td')[4].find_element_by_css_selector('a').get_attribute('href'))


			for year in runs_by_year.keys():
				records.loc[name,year] = runs_by_year[year] 
		
records.fillna('0',inplace=True)

'''cummulifying the data'''
records_final = records.copy()
for batsman in records.index:
    for year in records.columns[2:52]:
    	records.loc[batsman,year] = records_final.loc[batsman,'1979':year].astype(int).sum()

print(records.tail())
records.to_csv('records_final.csv')


driver.close()