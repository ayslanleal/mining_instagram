from bs4 import BeautifulSoup as bs
from selenium import webdriver
from time import sleep
import re
import json

def get_tag(tag_name):        
        driver = openFirefox()
        search(driver, 'explore/tags/'+tag_name)
        lista_pubs = []
        header_info = get_header_info(driver)
        click = click_navigation(driver)
        time=1 
        qtdPosts = re.sub('[,posts]','',header_info['Posts'])
        if int(qtdPosts)>=400000:
                time=1.5
        sleep(2)
        for i in range(0,20):
                try:
                        lista_pubs.append(get_post_info(driver))
                except:
                        pass
                click.click()
                sleep(time)

        lista_salvar = [header_info]
        dict_salvar = {'Tag Informations':lista_salvar, 'Posts':lista_pubs}
        dict_salvar = json.dumps(dict_salvar, indent=4, sort_keys=False, ensure_ascii=False)
        file = open("%s.json"%(tag_name), 'w')
        file.write(dict_salvar)
        file.close()
        driver.close()

def get_header_info(driver):
        header_info = {"Tag":"","Posts":"","TagImg":""}
        bs_obj = bs(driver.page_source, 'html.parser')
        header_info['Tag'] = bs_obj.find('div',{'class':'WSpok'}).find('h1',{'class':'_7UhW9 fKFbl yUEEX KV-D4 uL8Hv '}).text
        header_info['Posts'] = bs_obj.find('div',{'class':'WSpok'}).find('span',{'class':'-nal3 '}).text
        header_info['TagImg'] = bs_obj.find('div',{'class':'fZC9e'}).find('img').get('src')
        return header_info

def get_post_info(driver):
        bs_obj = bs(driver.page_source, 'html.parser')
        try:
                info_pubs_photo={'UserName':'','UserUrl':'','Likes':'','Content':'','ImgUrl':'','Caption':''}
                info_pubs_photo['Likes'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'Nm9Fw'}).find('span').text
                info_pubs_photo['Caption'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'P9YgZ'}).find('span').text
                info_pubs_photo['UserName'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'P9YgZ'}).find('h2', {'class':'_6lAjh'}).find('a').get('title')
                info_pubs_photo['UserUrl'] = 'https://www.instagram.com/'+info_pubs_photo['UserName']
                info_pubs_photo['Content'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'KL4Bh'}).find('img', {'class':'FFVAD'}).get('alt')
                info_pubs_photo['ImgUrl'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'KL4Bh'}).find('img').get('src')
                return info_pubs_photo
        except:
                info_pubs_video={'UserName':'','UserUrl':'','Views':'','VideoUrl':'','Caption':''}
                info_pubs_video['Views'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'HbPOm _9Ytll'}).find('span').text
                info_pubs_video['Caption'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'P9YgZ'}).find('span').text
                info_pubs_video['UserName'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'P9YgZ'}).find('h2', {'class':'_6lAjh'}).find('a').get('title')
                info_pubs_video['UserUrl'] = 'https://www.instagram.com/'+info_pubs_video['UserName']
                info_pubs_video['VideoUrl'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'_5wCQW'}).find('video').get('src')
                return info_pubs_video

def search(driver, string):
        driver.get("https://www.instagram.com/"+string)

def openFirefox():
        driver = webdriver.Firefox()
        return driver

def click_navigation(driver):
        driver.find_element_by_class_name('_9AhH0').click()
        return driver.find_element_by_class_name('D1AKJ').find_element_by_tag_name('a')
        
