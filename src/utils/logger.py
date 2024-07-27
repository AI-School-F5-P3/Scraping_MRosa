import logging
import os
from logging.handlers import RotatingFileHandler
from src.utils.constants import RED_CIRCLE, WHITE, RED, GREEN, YELLOW, PASTEL_YELLOW, RESET

# Ruta de la carpeta de logs
src_dir = os.path.dirname(os.path.dirname(__file__))
log_dir = os.path.join(src_dir, 'src', 'logs')

# Crea la carpeta si no existe
if not os.path.exists(log_dir):
    try:
        os.makedirs(log_dir)
    except OSError as e:
        raise OSError(f"{RED_CIRCLE} {RED}Error al crear la carpeta de logs: {YELLOW}{e}{RESET}")

log_file = os.path.join(log_dir, 'logs.log')

class ColoredFormatter(logging.Formatter):
    """
    Formatter personalizado para añadir colores a los mensajes de logging.
    """
    def format(self, record):
        log_message = super().format(record)
        if record.levelno == logging.ERROR:
            return f"\n{RED_CIRCLE} {RED}{log_message}{RESET}\n"
        elif record.levelno == logging.WARNING:
            return f"{YELLOW}{log_message}{RESET}"
        elif record.levelno == logging.INFO:
            return f"{GREEN}{log_message}{RESET}"
        else:
            return f"{WHITE}{log_message}{RESET}"

def setup_logging():
    """
    Configura el sistema de logging con color y rotación de archivos.
    """
    try:
        # Configuración del archivo de logs con rotación
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10 MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] [%(name)s] [%(filename)s:%(lineno)d] - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)

        # Configurar el root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        root_logger.addHandler(file_handler)
        
        # Crear el handler de consola
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)

        # Configurar el formatter con colores para la consola
        console_formatter = ColoredFormatter(f'[%(levelname)s] {PASTEL_YELLOW}[%(filename)s:%(lineno)d] - %(message)s')
        console_handler.setFormatter(console_formatter)

        # Añadir el handler de consola al logger root
        root_logger.addHandler(console_handler)
        
    except Exception as e:
        raise RuntimeError(f"{RED}{RED_CIRCLE} - Error al configurar el logging: {e}{RESET}")

def get_logger(name):
    """
    Obtiene un logger configurado.

    Args:
        name (str): Nombre del logger.

    Returns:
        logging.Logger: Logger configurado.
    """
    return logging.getLogger(name)

# Configura el logging
setup_logging()

# Obtén el logger
logger = get_logger(__name__)