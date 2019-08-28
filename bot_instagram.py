from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import requests

def remove_repetidos(lista):
    l = []
    for i in lista:
        if i not in l:
            l.append(i)
    return l

tag = 'nome da tag'
ff = webdriver.Firefox()
ff.get('https://www.instagram.com/explore/tags/'+tag)
sleep(3)

motion_len=250
current_scroll_position, new_height = 0, 100
aux,cont=0,0

bs_obj, content, img_urls = None, None, None
img_content = []

while current_scroll_position <= new_height:
    if cont%5==0:
        bs_obj = bs(ff.page_source, 'html.parser')
        content = bs_obj.findAll('div', {'class':'KL4Bh'})
        img_urls = [cont.find('img').get('src') for cont in content]
        img_content.extend(img_urls)
    current_scroll_position += motion_len 
    for i in range(0,5):
        ff.execute_script("window.scrollTo(0, %d);"%(current_scroll_position))
    sleep(0.5)
    new_height = ff.execute_script("return document.body.scrollHeight")
    if current_scroll_position>=new_height and aux!=4:
        current_scroll_position-=250
        sleep(8)
        aux+=1
    cont+=1

img_links = remove_repetidos(img_content)

contador = 1
for img in img_links: 
    imag_bc = requests.get(img)
    save = open('./Imagens/%s%d.jpg'%(tag,contador), 'wb')
    save.write(imag_bc.content)
    contador+=1
