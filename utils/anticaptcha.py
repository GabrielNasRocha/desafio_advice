from utils import setup_logger
from dotenv import load_dotenv
import os
import requests
import time

logger = setup_logger(__name__)
logger.info("Iniciando a função anticaptcha")
load_dotenv()
apiKey = os.getenv("anticaptchaApiKey")

def solve_anticaptcha(imagemBase64)->str:
    logger.info("Chamando a função anticaptcha")
    payload = {
        "clientKey": apiKey,
        "task": {
            "type": "ImageToTextTask",
            "body": imagemBase64
        }
    }
    response = requests.post(
        "https://api.anti-captcha.com/createTask",
        json=payload
    )
    resultado = response.json()
    if resultado["errorId"] != 0:
        raise Exception(
            f"Erro Anti-Captcha: "
            f"{resultado.get('errorCode')} - "
            f"{resultado.get('errorDescription')}"
        )
    task_id = resultado["taskId"]
    while True:
        response = requests.post(
            "https://api.anti-captcha.com/getTaskResult",
            json={
                "clientKey": apiKey,
                "taskId": task_id
            }
        )
        resultado = response.json()
        if resultado["status"] == "ready":
            captcha_texto = resultado["solution"]["text"]
            break
        time.sleep(2)
    logger.info("CAPTCHA:", captcha_texto)
    return captcha_texto