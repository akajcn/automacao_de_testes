from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
import time
import pathlib

# Configuração para o navegador Chrome
# navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def executar_teste_de_pagina():
    # Abrindo a página HTML local para execução dos testes

    localizacao_pagina = pathlib.Path(__file__).parent.resolve()
    
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    navegador = webdriver.Chrome(options=options)
    
    navegador.get(f"file:////{localizacao_pagina}/sample-exercise.html")
    

    # Clicando no botão para gerar um código
    botao_gerar = navegador.find_element(By.NAME, "generate")
    botao_gerar.click()

    # Espera até que o código gerado esteja visível na tela
    elemento_codigo = WebDriverWait(navegador, 10).until(
        EC.visibility_of_element_located((By.ID, "my-value"))
    )
    codigo_recebido = elemento_codigo.text

    # Inserindo o código gerado no campo de entrada
    campo_codigo = navegador.find_element(By.ID, "input")
    # Limpa o campo antes de inserir o novo código
    campo_codigo.clear()  
    campo_codigo.send_keys(codigo_recebido)

    # Clicando no botão para testar o código inserido
    botao_testar = navegador.find_element(By.NAME, "button")
    botao_testar.click()

    # Aceitando o alerta "Done!" que aparece após a validação
    alerta_terminado = Alert(navegador)
    # Fecha o alerta
    alerta_terminado.accept()  

    # Obtendo o texto de resultado e comparando com o esperado
    texto_final = navegador.find_element(By.ID, "result").text
    mensagem_esperada = f"It workls! {codigo_recebido}!"

    # Validando se o resultado é o esperado
    print("Teste realizado com sucesso!" if texto_final == mensagem_esperada else "Teste falhou!")


# Realizando o teste de geração várias vezes com uma pausa entre eles
for _ in range(3):
    executar_teste_de_pagina()
    # Pausa para evitar a sobreposição dos testes
    time.sleep(3)  

# Fechando o navegador após a execução dos testes
navegador.quit()