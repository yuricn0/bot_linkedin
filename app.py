from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as condicao_esperada
from selenium.webdriver.common.keys import Keys
from time import sleep 
import os
from random import randint

def iniciar_driver():
    chrome_options = Options()

    arguments = ['--lang=pt-BR', '--window-maximized', '--incognito']

    for argument in arguments:
        chrome_options.add_argument(argument)

    chrome_options.add_experimental_option('prefs', {
        'download.prompt_for_download': False,
        'profile.default_content_setting_values.notifications': 2,
        'profile.default_content_setting_values.automatic_downloads': 1,
})

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(
        driver,
        10,
        poll_frequency=1,
        ignored_exceptions=[
            NoSuchElementException,
            ElementNotVisibleException,
            ElementNotSelectableException,
        ]
    )
    return driver, wait

def automatizar_convites_linkedin(cargo, mensagem):
    try:
        driver, wait = iniciar_driver()
        # Abrir o site do linkedin

        driver.get('https://www.linkedin.com/login/pt?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
        print('Faça o login, a automação iniciará em instantes.')
        sleep(50)

        # Encontrar e clicar campo de pesquisa
        campo_pesquisar = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH,"//input[@placeholder='Pesquisar']")))
        campo_pesquisar.click()
        sleep((randint(1,4)))

        # Input pro usuário colocar qual profissão e digitar enter
        campo_pesquisar.send_keys(cargo)
        sleep((randint(1,3)))
        campo_pesquisar.send_keys(Keys.ENTER)
        sleep((randint(10,15)))

        # Marcar no campo 'Pessoas'
        campo_pessoas = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH,'//nav//div//ul//li[3]//button')))
        campo_pessoas.click()
        sleep((randint(4,8)))
    except:
        print('Não foi possivel fazer a automação, reinicie o sistema.')
    while True:   
        qtd_convites = 0
        # Descer e subir a página
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollTop);")
        sleep(2)
        if qtd_convites < 15:
        # Verificar se tem botões 'Conectar'?
            botões_conectar = wait.until(condicao_esperada.visibility_of_all_elements_located((By.XPATH,"//button//span[text()='Conectar']")))
            for botao in botões_conectar:
                if qtd_convites < 15:
                    # Clicar no 1° campo 'Conectar'
                    botao.click()
                    sleep(randint(5,10))

                    # Extrair o nome
                    nome_contato = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH,'//p//span//strong'))).text
                    primeiro_nome = nome_contato.split()[0]
                    sleep((randint(1,3)))

                    # Encontrar e clicar no campo adicionar nota
                    botao_adicionar_nota = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH,"//button[@aria-label='Adicionar nota']")))
                    botao_adicionar_nota.click()
                    sleep((randint(1,3)))

                    # Encontrar e digitar a mensagem personalizada com o nome extraido
                    mensagem_personalizada = f'Oii, {primeiro_nome}!{os.linesep}{mensagem}'

                    campo_mensagem = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH,"//textarea[@name='message']")))
                    campo_mensagem.click()
                    campo_mensagem.send_keys(mensagem_personalizada)
                    sleep((randint(1,5)))

                    # Encontrar botão 'Enviar' e clicar
                    botao_enviar_convite = wait.until(condicao_esperada.visibility_of_element_located((By.XPATH,'//button[@aria-label="Enviar convite"]')))
                    botao_enviar_convite.click()
                    sleep((randint(2,7)))
                    qtd_convites += 1 
                else:
                    print('Limite de convites atingidos.')       
        # Verificar se o botão avançar está ativo
            if qtd_convites < 15:
                try:
                    botao_avancar = wait.until(condicao_esperada.element_to_be_clickable((By.XPATH,'//button[@aria-label="Avançar"]')))
                    botao_avancar.click()
                    sleep((randint(1,5)))

                except Exception as error:
                    print(f'Acabou as pesquisas para {cargo}.')
                    driver.close()
                    break
        driver.close()
        break

                