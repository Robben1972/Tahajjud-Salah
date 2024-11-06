from bs4 import BeautifulSoup
import requests

response = requests.get('https://namozvaqti.uz/shahar/toshkent')

soup = BeautifulSoup(response.content, 'html.parser')

link = str(soup.find_all('script')[-1])

print(link[link.find('const times')+25 : link.find('const times')+30])