from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from bs4 import BeautifulSoup as bs
import time 
import re
import json 

username = input("Informe o usuário: ")
binary = FirefoxBinary('C:\\Program Files\\Mozilla Firefox\\firefox.exe')
driver = webdriver.Firefox(firefox_binary=binary, executable_path = r'C:\\geckodriver.exe')
driver.get("https://www.instagram.com/"+username)

#Pagelength = driver.execute_script("window.scrollTo(document.body.scrollHeight/1.5, document.body.scrollHeight/25.0);")
Comp_pag = driver.execute_script("window.scrollTo(0, document.body.scrollHeight/1.5);")

links = []
Comp_pag = driver.execute_script("window.scrollTo(document.body.scrollHeight/1.5, document.body.scrollHeight/3);")
pesquisa = driver.page_source
data =bs(pesquisa, 'html.parser')
body = data.find('body')
script = body.find('span')
for link in script.findAll('a'):
        if re.match("/p", link.get('href')):
                links.append('https://www.instagram.com/'+link.get('href'))

time.sleep(5)
print(links)
