import logging
import os
from datetime import date

from . import config

logger = logging.getLogger(__name__)

def get_daily_post_path() -> str:
    """Retorna o caminho completo para o post diário do dia atual."""
    today_str = date.today().strftime("%Y-%m-%d")
    filename = f"{today_str}.md"

    # Garante que o diretório de posts exista
    post_dir = os.path.join(config.ZETTELKASTEN_DIRECTORY, config.DAILY_POST_SUBDIR)
    os.makedirs(post_dir, exist_ok=True)

    return os.path.join(post_dir, filename)

def read_or_create_daily_post() -> str:
    """Lê o post diário. Se não existir, retorna uma string vazia."""
    path = get_daily_post_path()
    if os.path.exists(path):
        logger.info(f"Carregando post diário existente: {path}")
        with open(path, encoding="utf-8") as f:
            return f.read()
    else:
        logger.info(f"Post diário não encontrado. Será criado um novo em: {path}")
        return ""

def save_daily_post(content: str):
    """Salva (ou sobrescreve) o conteúdo no arquivo de post diário."""
    path = get_daily_post_path()
    logger.info(f"Salvando post diário atualizado em: {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
