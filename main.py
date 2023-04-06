import requests
import bs4
import pprint
from fake_headers import Headers

parsed_data = {}
HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
headers = Headers(browser='firefox', os='win').generate()
html = requests.get(HOST, headers=headers).text
soup = bs4.BeautifulSoup(html, features='lxml')
vacancies = soup.find_all("a", class_='serp-item__title')
for vacancy in vacancies:
    link_vacancy = vacancy.attrs['href']
    html = requests.get(link_vacancy, headers=headers).text
    soup = bs4.BeautifulSoup(html, features='lxml')
    vacancy_description = soup.find('div', class_="vacancy-description").text
    if 'Django' in vacancy_description and 'Flask' in vacancy_description:
        title = soup.find('h1', class_="bloko-header-section-1").text
        vacancy_salary = soup.find('span', class_="bloko-header-section-2 bloko-header-section-2_lite").text
        vacancy_company = soup.find("span", {"data-qa": "bloko-header-2"}).text 
        vacancy_city = soup.find("p", {"data-qa": "vacancy-view-location"})
        if vacancy_city == None:
            vacancy_city = soup.find("span", {"data-qa": "vacancy-view-raw-address"})
        parsed_data[vacancy_company] = []
        parsed_data[vacancy_company].append({'link': vacancy.attrs['href'], 'salary': vacancy_salary, 'company': vacancy_company, 'city': vacancy_city.text})
pprint.pprint(parsed_data)