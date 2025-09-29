import logging
import os
import subprocess
from datetime import date

import config

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
    """Lê o post diário. Se não existir, executa 'zk daily' para criá-lo e depois o lê."""
    path = get_daily_post_path()
    if os.path.exists(path):
        logger.info(f"Carregando post diário existente: {path}")
        with open(path, encoding="utf-8") as f:
            return f.read()
    else:
        # --- BLOCO DE CÓDIGO MODIFICADO ---
        logger.info("Post diário não encontrado. Executando 'zk daily' para criar o template.")
        try:
            my_env = os.environ.copy()
            my_env["EDITOR"] = "true"
            result = subprocess.run(
                ["zk", "daily"],
                check=True,
                cwd=config.ZETTELKASTEN_DIRECTORY,
                stdin=subprocess.DEVNULL,  # Fecha a entrada padrão, impedindo qualquer prompt interativo.
                capture_output=True,
                text=True,
                timeout=10,  # Adiciona um timeout de 30 segundos como rede de segurança.
            )
            logger.info(f"'zk daily' executado com sucesso. Saída: {result.stdout.strip()}")

            # Após a criação, lê o novo arquivo para obter o conteúdo do template
            if os.path.exists(path):
                logger.info(f"Lendo o novo post diário criado em: {path}")
                with open(path, encoding="utf-8") as f:
                    return f.read()
            else:
                logger.error(f"O comando 'zk daily' foi executado, mas o arquivo {path} ainda não foi encontrado!")
                return "" # Retorna vazio como fallback

        except FileNotFoundError:
            logger.error("Erro: O comando 'zk' não foi encontrado. Verifique se ele está instalado e no PATH do sistema.")
            return ""
        except subprocess.CalledProcessError as e:
            logger.error(f"O comando 'zk daily' falhou com o erro: {e.stderr}")
            return ""
        except Exception as e:
            logger.error(f"Um erro inesperado ocorreu ao executar 'zk daily': {e}")
            return ""

def save_daily_post(content: str):
    """Salva (ou sobrescreve) o conteúdo no arquivo de post diário."""
    path = get_daily_post_path()
    logger.info(f"Salvando post diário atualizado em: {path}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
