import logging
import time

from watchdog.observers import Observer

from . import config
from .file_handler import MarkdownChangeHandler
from .logger_setup import setup_logging


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Iniciando o serviço de agregação de notas Zettelkasten...")
    logger.info(f"Monitorando o diretório de notas: {config.NOTES_DIRECTORY}")
    logger.info(f"Repositório Zettelkasten: {config.ZETTELKASTEN_DIRECTORY}")

    event_handler = MarkdownChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, config.NOTES_DIRECTORY, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Sinal de interrupção recebido. Encerrando o serviço...")
        observer.stop()
    observer.join()
    logger.info("Serviço encerrado.")

if __name__ == "__main__":
    main()
