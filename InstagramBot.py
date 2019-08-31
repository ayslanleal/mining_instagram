from bs4 import BeautifulSoup as bs #Módulo com funções para analisar e filtrar conteúdo do código fonte
from selenium import webdriver #Ferramenta utilizada para automatizar comandos no browser
from time import sleep #Função que faz o programa "parar" por um determinado tempo em segundos passado por parâmetro 
from re import sub #Função para trabalhar com strings
import os #Módulo que traz informações sobre o sistema operacional e permite manipular diretórios
import json #Módulo com funções para trabalhar com arquivos json

def get_tag(tag_name):        
        driver = openFirefox() 
        search(driver, 'explore/tags/'+tag_name) #passando 'explore/tags' pois a função get_tag() pesquisa apenas por tags, caso fosse usuário, passaríamos apenas o nome do mesmo. 
        header_info = get_header_info(driver)
        if header_info!=None:
                qtdPosts = sub('[,posts]','',header_info['Posts']) #Pega a quantidade de posts coletada e remove as vírgulas e a palavra 'posts' da string para que possa ser convertida em inteiro.
                time=1 #Intervalo entra uma publicação e outra.
                if int(qtdPosts)>=400000: #Caso o número de posts seja maior que 400.000, o intervalo aumenta, pois o tempo de carregamento da página é maior.
                        time=1.5
                lista_pubs = []
                sleep(3)
                click = click_navigation(driver)
                sleep(2)
                for i in range(0,20):
                        sleep(time)
                        lista_pubs.append(get_post_info(driver))
                        click.click()
                        
                lista_salvar = [header_info]
                dict_salvar = {'Tag Informations':lista_salvar, 'Posts':lista_pubs}
                save(dict_salvar, tag_name) #Salva resultados encontrados
                driver.close()
                print("%d Publicações coletadas."%(len(lista_pubs)))
                return True
        else:   
                print("Sem resultados para #"+tag_name)
                driver.close()
                return False

def get_header_info(driver): #Função que coleta as informações do cabeçalho da tag, que seria o número de publicações, o nome da tag e a imagem. 
        try:    
                header_info = {"Tag":"","Posts":"","TagImg":""} #Dicionário do python
                bs_obj = bs(driver.page_source, 'html.parser') #Invocando método do beautiful soup que analisa todo o código fonte da página e retorna um objeto do mesmo.
                header_info['Tag'] = bs_obj.find('div',{'class':'WSpok'}).find('h1',{'class':'_7UhW9 fKFbl yUEEX KV-D4 uL8Hv '}).text #Filtrando conteúdo até chegar no nome da tag
                header_info['Posts'] = bs_obj.find('div',{'class':'WSpok'}).find('span',{'class':'-nal3 '}).text #Filtrando conteúdo até chegar no número de publicações
                header_info['TagImg'] = bs_obj.find('div',{'class':'fZC9e'}).find('img').get('src') #Filtrando conteúdo até chegar na url da imagem da tag.
                return header_info #Retornando dicionário com os dados encontrados.
        except: 
                #Caso a busca acima falhe, significa que não houveram resultados para a tag pesquisada.
                return None

def get_post_info(driver):
        bs_obj = bs(driver.page_source, 'html.parser')
        try:
                #Publicações em foto
                info_pubs_photo={'UserName':'','UserUrl':'','Likes':'','Content':'','ImgUrl':'','Caption':''} #Dicionário que guarda informações de foto
                try:
                        #Verifica se há algum like, do contrário, ele não encontrará nada e retornará um erro.
                        info_pubs_photo['Likes'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'Nm9Fw'}).find('span').text
                except:
                        #Caso o try de cima falhe, significa que a publicação ainda não possui nenhum like, então, ela recebe 0.
                        info_pubs_photo['Likes']='0'
                        pass #Continua para as próximas buscas.
                info_pubs_photo['Caption'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'P9YgZ'}).find('span').text
                info_pubs_photo['UserName'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'P9YgZ'}).find('h2', {'class':'_6lAjh'}).find('a').get('title')
                info_pubs_photo['UserUrl'] = 'https://www.instagram.com/'+info_pubs_photo['UserName']
                info_pubs_photo['Content'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'KL4Bh'}).find('img', {'class':'FFVAD'}).get('alt')
                info_pubs_photo['ImgUrl'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'KL4Bh'}).find('img').get('src')
                return info_pubs_photo
        except: 
                #Publicações em vídeo
                #Caso a busca acima falhe, significa que o tipo de publicação que está sendo análisada é um vídeo, então o nome das classes e tags html será como a seguir:
                info_pubs_video={'UserName':'','UserUrl':'','Views':'','VideoUrl':'','Caption':''} #Dicionário que guarda informações de vídeo
                info_pubs_video['Views'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'HbPOm _9Ytll'}).find('span').text
                info_pubs_video['Caption'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'P9YgZ'}).find('span').text
                info_pubs_video['UserName'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div',{'class':'P9YgZ'}).find('h2', {'class':'_6lAjh'}).find('a').get('title')
                info_pubs_video['UserUrl'] = 'https://www.instagram.com/'+info_pubs_video['UserName']
                info_pubs_video['VideoUrl'] = bs_obj.find('div',{'class':'PdwC2 _6oveC Z_y-9'}).find('div', {'class':'_5wCQW'}).find('video').get('src')
                return info_pubs_video

def search(driver, string): 
        driver.get("https://www.instagram.com/"+string) #Método do objeto "driver" que executa pesquisa no browser da string passada como parâmetro

def openFirefox(): #Fução abre o navegador e retorna objeto "driver" para manipulação do browser
        driver = webdriver.Firefox()
        return driver

def click_navigation(driver): 
        driver.find_element_by_class_name('_9AhH0').click() #Método de "driver" que encontra elemento no código fonte da página pelo nome da classe '_9AhH0', que é a primeira publicação que será aberta na página, e depois chama o método ".click()" para abrir a publicação.
        return driver.find_element_by_class_name('D1AKJ').find_element_by_tag_name('a') #Neste método, ele encontra o botão que vai passando os posts pro lado retorna pra função principal o objeto encontrado. Ele fica dentro da classe "D1AKJ" dentro da tag "a".
        
def save(dictionary, fileName): #Função que rebe um dicionário e o nome que será salvo no arquivo
        dictionary = json.dumps(dictionary, indent=4, sort_keys=False, ensure_ascii=False) #Converte dicionário para arquivo json
        if not os.path.exists("Tags_Info"): #Cria um diretório com o nome Tags_Info, caso ainda não exista, para guardar os arquivos .json
                os.mkdir('./Tags_Info')
        file = open("./Tags_Info/%s.json"%(fileName), 'w') #Cria arquivo .json com o nome passado como parâmetro 
        file.write(dictionary) #Armazena as informações no arquivo que foi criado
        file.close() 
