from .logger_config import setup_logger
from .anticaptcha import solve_anticaptcha

logger = setup_logger(__name__)
logger.info("Utils Carregado")