# src/daily_post_aggregator/config.py
import os

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# --- Configurações da API ---
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("A variável de ambiente OPENAI_API_KEY não foi encontrada.")

# --- Configurações de Diretórios ---

# Pasta onde suas notas do Google Drive são sincronizadas.
# É esta pasta que será monitorada em busca de arquivos .md.
NOTES_DIRECTORY = "/home/felipemarcelino/Google_Drive/onyx/TabUltraCPro/Notebooks"

# Pasta raiz do seu repositório Zettelkasten.
# É aqui que o commit e push serão executados.
ZETTELKASTEN_DIRECTORY = "/home/felipemarcelino/Zettelkasten/"

# Subdiretório dentro do Zettelkasten onde os posts diários ficam.
DAILY_POST_SUBDIR = "content/blog"
