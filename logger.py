import logging
import colorlog

# Настройка цветовой схемы
log_colors = {
    'DEBUG': 'cyan',
    'INFO': 'green',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# Конфигурация формата и цветов
formatter = colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    log_colors=log_colors,
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Создание обработчика (вывод в консоль)
handler = logging.StreamHandler()
handler.setFormatter(formatter)

# Настройка логгера
logger = colorlog.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# Пример использования
logger.debug("Это DEBUG (голубой)")
logger.info("Это INFO (зелёный)")
logger.warning("Это WARNING (жёлтый)")
logger.error("Это ERROR (красный)")
logger.critical("Это CRITICAL (жирный красный)")
