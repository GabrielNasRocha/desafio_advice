from .logger_config import setup_logger
from .anticaptcha import solve_anticaptcha
from .json_manager import ler_json, escrever_json

logger = setup_logger(__name__)
logger.info("Utils Carregado")