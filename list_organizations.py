import sys
import asyncio
import requests
from bs4 import BeautifulSoup 
import aiohttp
from aiohttp import ClientSession

global c
c=1

url = 'https://summerofcode.withgoogle.com/archive/'+sys.argv[1]+'/organizations/'

async def fetch_soup(link: str, session): 
	org_page = await session.request(method="GET", url=link)
	html = await org_page.text()
	
	soup = BeautifulSoup(html, 'lxml')
	return soup


async def list_tech(link, session):
	soup = await fetch_soup(link, session)
	result = soup.find_all('li',class_='organization__tag organization__tag--technology')
	organization = soup.find('h3',class_='banner__title')

	global c
	print(c,end=") ")
	c=c+1
	print(organization.text.strip(),end=" - ")
	for i in result:
		print(i.text.strip(),end=", ")
	print()
	


async def main():
	page = requests.get(url)
	m_soup = BeautifulSoup(page.content , 'lxml')
	org_list = m_soup.find_all('li' , class_='organization-card__container')

	print(len(org_list))

	tasks = []
	async with aiohttp.ClientSession() as session:
		for org in org_list:
			linke = org.find('a')['href']
			link = 'https://summerofcode.withgoogle.com' + linke
			tasks.append(list_tech(link, session))
		await asyncio.gather(*tasks)


asyncio.run(main())

	