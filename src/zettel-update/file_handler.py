import logging
import time

import daily_post_manager
import git_manager
import llm_client
from watchdog.events import FileSystemEventHandler

l
ogger = logging.getLogger(__name__)

class MarkdownChangeHandler(FileSystemEventHandler):
    """Manipulador que reage a criação/modificação de arquivos Markdown."""

    def __init__(self):
        super().__init__()
        self._last_processed_time = 0

    def _process_file(self, file_path: str):
        # Debounce: Evita processamento duplo rápido
        if time.time() - self._last_processed_time < 5:
            return

        # Evita loops infinitos: não processa o próprio arquivo de post diário
        daily_post_path = daily_post_manager.get_daily_post_path()
        if file_path == daily_post_path:
            return

        if not file_path.lower().endswith(".md"):
            return

        logger.info(f"Evento detectado para o arquivo de nota: {file_path}")
        self._last_processed_time = time.time()

        try:
            # 1. Lê a nota modificada
            with open(file_path, encoding="utf-8") as f:
                note_content = f.read()

            # 2. Lê o post diário atual (ou cria um novo)
            daily_post_content = daily_post_manager.read_or_create_daily_post()

            # 3. Usa a LLM para mesclar os conteúdos
            merged_content = llm_client.merge_notes_with_llm(daily_post_content, note_content)

            # 4. Salva o post diário atualizado
            daily_post_manager.save_daily_post(merged_content)

            # 5. Commita e envia as alterações
            git_manager.commit_and_push_changes(daily_post_path)

        except Exception as e:
            logger.error(f"Falha no fluxo de processamento para '{file_path}': {e}", exc_info=True)

    def on_modified(self, event):
        if not event.is_directory:
            self._process_file(event.src_path)

    def on_created(self, event):
        if not event.is_directory:
            self._process_file(event.src_path)
