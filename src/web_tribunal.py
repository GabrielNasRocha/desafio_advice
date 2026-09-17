from utils import setup_logger, solve_anticaptcha
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
from dotenv import load_dotenv

logger = setup_logger(__name__)

class WebTribunal:
    def __init__(self):
        load_dotenv()
        self.url = 'https://eproc-consulta-publica-1g.tjmg.jus.br/eproc/externo_controlador.php?acao=processo_consulta_publica'
        self.limiteConsulta = int(os.getenv("limiteConsulta", 5))
        logger.info("Iniciando web tribunal")

    def openBrowser(self):
        logger.info("Iniciando openBrowser e abrindo o navegador")
        driver = webdriver.Chrome()
        driver.get(self.url)
        driver.find_element(By.ID, 'txtStrParte').send_keys('ADILSON DA SILVA')
        captcha = driver.find_element(By.ID, "lblInfraCaptcha").find_element(By.TAG_NAME, "img").get_attribute("src")
        imagemBase64 = captcha.split(",", 1)[1]
        solvedAnticaptcha = solve_anticaptcha(imagemBase64=imagemBase64)
        driver.find_element(By.ID, 'txtInfraCaptcha').send_keys(solvedAnticaptcha)
        driver.find_element(By.ID, 'sbmNovo').click()
        aba_principal = driver.current_window_handle
        tabela = driver.find_elements(By.TAG_NAME, 'tr')
        for index, item in enumerate(tabela):
            col = item.find_elements(By.TAG_NAME, 'td')
            if len(col) > 0:
                logger.info(col[0].text)
                link = col[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
                driver.execute_script("window.open(arguments[0], '_blank');", link)
                driver.switch_to.window(driver.window_handles[-1])
                link = driver.find_elements(By.TAG_NAME, 'td')[0].find_element(By.TAG_NAME, 'a').get_attribute('href')
                driver.get(link)
                nProcesso = driver.find_element(By.ID, 'txtNumProcesso').text
                dataAtuacao = driver.find_element(By.ID, 'txtAutuacao').text
                situacao = driver.find_element(By.ID, 'txtSituacao').text
                orgaoJulgador = driver.find_element(By.ID, 'txtOrgaoJulgador').text
                juiz = driver.find_element(By.ID, 'txtMagistrado').text
                classeAcao = driver.find_element(By.ID, 'txtClasse').text
                codigoDescricao = driver.find_element(By.XPATH, '//*[@id="fldAssuntos"]/table/tbody/tr[2]/td[1]').text
                assuntoDescricao = driver.find_element(By.XPATH, '//*[@id="fldAssuntos"]/table/tbody/tr[2]/td[2]').text
                logger.info(f'''Processo: {nProcesso},
                             Data Atuação: {dataAtuacao},
                             Situação: {situacao},
                             Orgão Julgador: {orgaoJulgador},
                             Juiz: {juiz},
                             Classe da Ação: {classeAcao},
                             Codigo: {codigoDescricao}
                             Descrição: {assuntoDescricao}''')
                driver.close()
                driver.switch_to.window(aba_principal)
                if index >= self.limiteConsulta:
                    logger.info(f'Limite de consultas batido: {self.limiteConsulta}')
                    break
        driver.close()
        logger.info('Processo finalizado')


WebTribunal().openBrowser()