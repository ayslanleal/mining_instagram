from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import json

def get_tag(tag_name, numero):        
        driver = openFirefox()
        search(driver, 'explore/tags/'+tag_name)
        lista_pubs = []
        info_tag = get_tag_info(driver)
        click = click_navigation(driver)
        sleep(3)
        while numero>1:
                try:
                        #Publicações em foto.
                        lista_pubs.append(get_post_info(driver))
                except:
                        #Publicações em vídeo... Falta Completar.
                        pass
                sleep(1)
                click.click()
                sleep(1)
                numero-=1
                
        lista_salvar = [info_tag]
        dict_salvar = {'Tag Informations':lista_salvar, 'Posts':lista_pubs}
        dict_salvar = json.dumps(dict_salvar, indent=4, sort_keys=False, ensure_ascii=False)
        
        file = open("%s.json"%(tag_name), 'w')
        file.write(dict_salvar)
        file.close()

def get_tag_info(driver):
        info_tag = {"Tag":"","Posts":"","TagImg":""}
        bs_obj = bs(driver.page_source, 'html.parser')
        info_tag['Tag'] = bs_obj.find('div',{'class':'WSpok'}).find('h1',{'class':'_7UhW9 fKFbl yUEEX KV-D4 uL8Hv '}).text
        info_tag['Posts'] = bs_obj.find('div',{'class':'WSpok'}).find('span',{'class':'-nal3 '}).text
        info_tag['TagImg'] = bs_obj.find('div',{'class':'fZC9e'}).find('img').get('src')
        return info_tag

def get_post_info(driver):
        info_pubs={'UserName':'','UserUrl':'','Likes':'','Content':'','ImgUrl':'','Caption':''}
        bs_obj = bs(driver.page_source, 'html.parser')
        info_pubs['Likes'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'Nm9Fw'}).find('span').text
        info_pubs['Caption'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'P9YgZ'}).find('span').text
        info_pubs['UserName'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'P9YgZ'}).find('h2', {'class':'_6lAjh'}).find('a').get('title')
        info_pubs['UserUrl'] = 'https://www.instagram.com/'+info_pubs['UserName']
        info_pubs['Content'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'KL4Bh'}).find('img', {'class':'FFVAD'}).get('alt')
        info_pubs['ImgUrl'] = bs_obj.find('div', {'class':'KL4Bh'}).find('img').get('src')
        return info_pubs

def search(driver, string):
        driver.get("https://www.instagram.com/"+string)

def openFirefox():
        driver = webdriver.Firefox()
        return driver

def click_navigation(driver):
        driver.find_element_by_class_name('_9AhH0').click()
        return driver.find_element_by_class_name('D1AKJ').find_element_by_tag_name('a')