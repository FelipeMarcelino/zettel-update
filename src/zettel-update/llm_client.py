# src/daily_post_aggregator/llm_client.py
import logging

import config
import openai

logger = logging.getLogger(__name__)

client = openai.OpenAI(api_key=config.OPENAI_API_KEY)

def merge_notes_with_llm(daily_post_content: str, note_content: str) -> str:
    """Usa a LLM para mesclar de forma inteligente o conteúdo da nota no post diário.
    """
    if not note_content.strip():
        logger.warning("Conteúdo da nota está vazio. Abortando a mesclagem.")
        return daily_post_content

    system_prompt = """
        Você é um assistente de automação de conteúdo para um sistema Zettelkasten. Sua função é integrar uma nota em um post diário de forma programática e precisa.

        Análise e execute as seguintes instruções:
        1.  Extraia o título da "NOTA". O título é a primeira linha, que começa com '# '.
        2.  Compare este título com os títulos já existentes no "POST DIÁRIO".
        3.  **SE** encontrar um título correspondente, substitua a seção inteira da nota antiga pelo conteúdo completo da "NOTA".
        4.  **SE NÃO** encontrar um título correspondente, anexe o conteúdo completo da "NOTA" ao final do "POST DIÁRIO", precedido por um separador de três hífens em sua própria linha.
        5.  Sua resposta deve ser **EXCLUSIVAMENTE** o texto final do post diário.

        **REGRA DE SAÍDA CRÍTICA:** A sua saída não deve conter nenhuma explicação, comentário, introdução, ou blocos de código como ```markdown ou ```. A resposta deve ser o texto Markdown puro e completo, pronto para ser salvo diretamente em um arquivo .md.
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
