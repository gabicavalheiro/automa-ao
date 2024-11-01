from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from dotenv import load_dotenv
import time
import logging
import pywhatkit as kit
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import unidecode

# Carregar variáveis do arquivo .env
load_dotenv()

# Configuração do logging
logging.basicConfig(
    filename='versiculo_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'  # Certifica-se de que o log esteja em UTF-8
)

def obter_versiculo():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--lang=pt-BR")
    options.add_argument("charset=UTF-8")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://www.bibliaon.com/versiculo_do_dia/")
    time.sleep(3)

    try:
        # Utilizar textContent para capturar o texto com acentuação correta
        versiculo_elemento = driver.find_element(By.CSS_SELECTOR, "p.destaque#versiculo_hoje")
        versiculo = versiculo_elemento.get_attribute("textContent").strip()

        capitulo_versiculo = versiculo_elemento.find_element(By.TAG_NAME, "a").get_attribute("textContent").strip()
        capitulo, numero_versiculo = capitulo_versiculo.split(":")
        capitulo = capitulo.split(" ")[1]

        logging.info("Versículo extraído com sucesso: %s", versiculo)
    except Exception as e:
        logging.error("Erro ao extrair o versículo: %s", str(e))
        versiculo = None
        capitulo = None
        numero_versiculo = None
    finally:
        driver.quit()
    
    return numero_versiculo, capitulo, versiculo

def obter_leitura_liturgica():
    options = Options()
    options.add_argument("--incognito")
    options.add_argument("--lang=pt-BR")
    options.add_argument("charset=UTF-8")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://liturgia.cancaonova.com/pb/")
    time.sleep(3)

    try:
        leitura_elemento = driver.find_element(By.ID, "liturgia-1")
        leitura = leitura_elemento.get_attribute("textContent").strip()  # Usando textContent para captura

        logging.info("Leitura da liturgia extraída com sucesso.")
    except Exception as e:
        logging.error("Erro ao extrair a leitura da liturgia: %s", str(e))
        leitura = None
    finally:
        driver.quit()

    return leitura

def remover_acentos(texto):
    return unidecode.unidecode(texto)

def enviar_whatsapp(mensagem):
    try:
        # Remove acentos da mensagem antes de enviar
        mensagem_sem_acentos = remover_acentos(mensagem)
        kit.sendwhatmsg_to_group_instantly("JVmMTOXnD6r7JtG48QhGz9", mensagem_sem_acentos)
        logging.info("Mensagem enviada com sucesso!")
        time.sleep(5)  # Aguarda um pouco após o envio
    except Exception as e:
        logging.error("Erro ao enviar mensagem: %s", str(e))

def tarefa_diaria():
    numero_versiculo, capitulo, versiculo = obter_versiculo()
    leitura = obter_leitura_liturgica()

    if versiculo and leitura:
        mensagem = f"Versículo do dia:\n\n{versiculo}\n\nLeitura da Liturgia:\n\n{leitura}"
        enviar_whatsapp(mensagem)
    else:
        logging.warning("Nenhum versículo ou leitura disponível para enviar.")

# Executa a tarefa imediatamente
tarefa_diaria()