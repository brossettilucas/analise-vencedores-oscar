import time
import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Configuração e inicialização do navegador
options = Options()
options = webdriver.FirefoxOptions()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)

# Recebe os slugs dos filmes a serem coletados
import os
filename = 'films2.txt'
file = open(filename, 'r')
oscar_films = file.readlines()
for i in range(len(oscar_films) - 1):
    oscar_films[i] = oscar_films[i][:-1]
#print(oscar_films)

# Variável para monitorar o tempo gasto na coleta de cada filme
start = time.time()

# Configuração e inicialização do Data Frame
filmes = oscar_films
data = []
df = pd.DataFrame({"Filme":[], "Usuario": [],"Nota_Comentario":[],"Comentario":[], "Likes_Comentario":[]})

# Repete as ações para cada filme na lista
for filme in filmes:

    # Acessar página de reviews
    driver.get("https://letterboxd.com/film/"+ filme +"/reviews/by/activity/")
    page = 1
    stop = False
    i = 0
 
    while stop == False:
        time.sleep(2)

        # Captura cada reviews e coleta o conteúdo, o autor, a nota para o filme dada pelo autor e o número de likes da review
        secoes = driver.find_elements(By.CLASS_NAME,"film-detail")
        
        for secao in secoes:
            i = i + 1
            if i >= 1000 :
                stop = True
            try: 
                nota = secao.find_element(By.CSS_SELECTOR,"span.rating")
                nota = nota.text
            except NoSuchElementException: 
                nota = "-"
            try: 
                usuario = secao.find_element(By.CLASS_NAME,"avatar")
                usuario = usuario.get_attribute('href')
            except NoSuchElementException: 
                usuario = "-"
            try: 
                comentario = secao.find_element(By.CLASS_NAME,"-prose")
                comentario = comentario.text
                if comentario == "This review may contain spoilers. I can handle the truth.":
                    element = secao.find_element(By.CSS_SELECTOR,"a.reveal")
                    driver.execute_script("arguments[0].scrollIntoView();", element)
                    driver.execute_script("arguments[0].click();", element)
                    time.sleep(1)
                    comentario = secao.find_element(By.CLASS_NAME,"-prose")
                    comentario = comentario.text
            except NoSuchElementException: 
                comentario = "-"
            try: 
                like = secao.find_element(By.CLASS_NAME,"-like")
                like = like.text
            except NoSuchElementException: 
                like = "-"

            # Adiciona as informações no Data Frame
            row = {"Filme": filme, "Usuario": usuario, "Nota_Comentario": nota, "Comentario": comentario, "Likes_Comentario": like}
            df = pd.concat([df,pd.DataFrame([row])], ignore_index = True)

        print(i)
        
        # Acessa a próxima página de reviews
        page = page + 1
        driver.get("https://letterboxd.com/film/"+ filme +"/reviews/by/activity/page/"+ str(page) +"/")

    end = time.time()
    print(end - start)
    start = time.time()

    # Gera um csv com os dados
    df.to_csv('ComentarioFilmes21.csv')
    print(df)
    
# Finalização
print(df)
input("Press ENTER to exit\n")
driver.quit()
