# src/daily_post_aggregator/llm_client.py
import logging

import openai
import config


logger = logging.getLogger(__name__)

client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

def merge_notes_with_llm(daily_post_content: str, note_content: str) -> str:
    """Usa a LLM para mesclar de forma inteligente o conteúdo da nota no post diário.
    """
    if not note_content.strip():
        logger.warning("Conteúdo da nota está vazio. Abortando a mesclagem.")
        return daily_post_content

    system_prompt = """
    Você é um assistente inteligente para um sistema Zettelkasten. Sua tarefa é integrar uma nova nota (ou uma versão atualizada de uma nota) a um post diário de forma organizada.

    INSTRUÇÕES:
    1.  Identifique o título da "NOTA NOVA/ATUALIZADA". O título é a primeira linha, geralmente começando com '# '.
    2.  Verifique se uma nota com este mesmo título JÁ EXISTE no "POST DIÁRIO ATUAL".
    3.  Se a nota JÁ EXISTE, você deve substituir a seção antiga inteira no post diário pelo conteúdo completo da "NOTA NOVA/ATUALIZADA".
    4.  Se a nota NÃO EXISTE, adicione uma linha de separação (`\n\n---\n\n`) ao final do post diário e, em seguida, anexe o conteúdo completo da "NOTA NOVA/ATUALIZADA".
    5.  Retorne APENAS o conteúdo final e completo do post diário. Não inclua nenhuma explicação, introdução, comentário sua resposta. Apenas o texto junto com os markdown.
    """

    user_prompt = f"""
    POST DIÁRIO ATUAL:
    ---
    {daily_post_content}
    ---

    NOTA NOVA/ATUALIZADA:
    ---
    {note_content}
    ---
    """

    try:
        logger.info("Enviando requisição para a API da OpenAI para mesclar as notas...")
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
        )
        merged_content = response.choices[0].message.content
        logger.info("Conteúdo mesclado recebido da API com sucesso.")
        return merged_content
    except Exception as e:
        logger.error(f"Erro ao chamar a API da OpenAI: {e}", exc_info=True)
        # Em caso de erro, retorna o post original para não perder dados.
        return daily_post_content
