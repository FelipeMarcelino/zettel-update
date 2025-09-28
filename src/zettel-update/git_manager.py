import logging
from datetime import datetime

import config
import git  # GitPython

logger = logging.getLogger(__name__)

def commit_and_push_changes(file_path_to_commit: str):
    """Executa git add, commit e push para o repositório Zettelkasten.
    """
    try:
        repo = git.Repo(config.ZETTELKASTEN_DIRECTORY)

        # Garante que estamos no branch principal
        repo.git.checkout(repo.active_branch.name)

        # Verifica se há alterações
        if not repo.is_dirty(untracked_files=True) and file_path_to_commit not in repo.untracked_files:
             # Se o arquivo específico não está sujo, verificamos se ele já foi commitado mas não está no index
            if file_path_to_commit in [item.a_path for item in repo.index.diff(None)]:
                 pass # Arquivo modificado, continuar
            else:
                logger.info("Nenhuma alteração detectada no repositório para o arquivo de post diário. Pulando commit.")
                return

        logger.info(f"Adicionando arquivo ao stage: {file_path_to_commit}")
        repo.index.add([file_path_to_commit])

        commit_message = f"Autocommit: Atualiza post diário com notas - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        logger.info(f"Realizando commit com a mensagem: '{commit_message}'")
        repo.index.commit(commit_message)

        logger.info("Executando push para o repositório remoto 'origin'...")
        origin = repo.remote(name="origin")
        origin.push()

        logger.info("Commit e push realizados com sucesso!")

    except git.exc.GitCommandError as e:
        logger.error(f"Erro de comando Git: {e}", exc_info=True)
    except Exception as e:
        logger.error(f"Erro inesperado no gerenciamento do Git: {e}", exc_info=True)
