import pathlib
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions

def executar_teste_de_pagina():
    localizacao_pagina = pathlib.Path(__file__).parent.resolve()
    options = ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    navegador = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    navegador.get(f"file:///{localizacao_pagina}/sample-exercise.html")

    try:
        botao_gerar = navegador.find_element(By.NAME, "generate")
        botao_gerar.click()
        elemento_codigo = WebDriverWait(navegador, 10).until(
            EC.visibility_of_element_located((By.ID, "my-value"))
        )
        codigo_recebido = elemento_codigo.text
        campo_codigo = navegador.find_element(By.ID, "input")
        campo_codigo.clear()
        campo_codigo.send_keys(codigo_recebido)
        botao_testar = navegador.find_element(By.NAME, "button")
        botao_testar.click()
        Alert(navegador).accept()
        texto_final = navegador.find_element(By.ID, "result").text
        mensagem_esperada = f"It works! {codigo_recebido}!"
        assert texto_final == mensagem_esperada, f"Esperado '{mensagem_esperada}', mas obteve '{texto_final}'"
        print("Teste realizado com sucesso!")
    finally:
        navegador.quit()

# Chamando o teste
if __name__ == "__main__":
    for _ in range(3):
        executar_teste_de_pagina()
        time.sleep(3)
