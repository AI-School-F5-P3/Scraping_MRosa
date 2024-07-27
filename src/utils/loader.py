import threading
import time
from src.utils.constants import LIGHT_CYAN, RESET

class Loader:
    """
    Clase para manejar un loader animado en la consola.
    """

    def __init__(self):
        """
        Inicializa la instancia del Loader.
        """
        self.loading = False  # Controla si el loader está activo
        self.loader_thread = None  # Almacena el hilo del loader

    def start(self):
        """
        Inicia el loader en un hilo separado.
        """
        self.loading = True
        self.loader_thread = threading.Thread(target=self._animate)
        self.loader_thread.start()

    def stop(self):
        """
        Detiene el loader y limpia la línea de la consola.
        """
        self.loading = False
        if self.loader_thread:
            self.loader_thread.join()  # Espera a que el hilo del loader termine
        print(f"\r{RESET}", end="", flush=True)  # Limpia la línea del loader

    def _animate(self):
        """
        Método privado que anima el loader en la consola.
        """
        chars = "🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛"  # Caracteres para la animación
        while self.loading:
            for char in chars:
                print(f"\r{LIGHT_CYAN}Scrapeando... {char}  {RESET}", end="", flush=True)
                time.sleep(0.1)  # Pausa breve entre cada frame de la animación