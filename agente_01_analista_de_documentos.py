import os
import fitz
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# A lógica está dentro de uma função para ser utilizada por outros módulos
def analisar_documento(
    caminho_do_arquivo: str,
) -> (
    str | None
):  # parametro caminho do arquivo do tipo string, com retorno string ou None
    # Carrega as variáveis de ambiente do arquivo .env
    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        print("ERRO (Agente 1): Chave GOOGLE_API_KEY não encontrada.")
        return None

    # --- Extração de Texto do PDF ---
    try:
        doc = fitz.open(caminho_do_arquivo)
    except Exception as e:
        print(
            f"ERRO (Agente 1): Não foi possível abrir o arquivo '{caminho_do_arquivo}'. Detalhe: {e}"
        )
        return None

    texto_completo = ""
    for pagina in doc:
        texto_completo += pagina.get_text()  # type: ignore
    print("AGENTE 1: Texto completo extraído com sucesso.")

    # --- Extração do Bloco de Resumo ---
    primeira_pagina_texto = doc[0].get_text()
    bloco_resumo = primeira_pagina_texto
    print("AGENTE 1: Bloco de resumo (primeira página) extraído com sucesso.")
    # --- Interação com a IA ---
    print("AGENTE 1: Conectando com a IA para análise do resumo...")
    llm = ChatGoogleGenerativeAI(
        google_api_key=google_api_key,
        model="gemini-2.5-flash",
        temperature=0.1,
        convert_system_message_to_human=True,
    )

    prompt = f"""
    Você é um assistente especialista em análise de editais de licitação.
Sua tarefa é **exclusivamente** analisar resumos de editais de licitação.

Regras:
- Se o texto fornecido for realmente um resumo de edital de licitação, extraia e apresente **somente** as seguintes informações:
  - Objeto da Licitação
  - Valor Total da Contratação
  - Modalidade da Licitação
  - Data e Horário da Realização

- Responda sempre no formato:

Objeto da Licitação: [texto ou "não informado"]
Modalidade da Licitação: [texto ou "não informado"]
Data e Horário da Realização: [texto ou "não informado"]

- Se o texto fornecido **não for um edital de licitação válido**, responda apenas com:
  Erro: não é um edital de licitação válido.

- Não inclua introduções, comentários adicionais, justificativas ou explicações.
- Não invente informações que não estejam no resumo.


    Texto do Resumo:
    ---
    {bloco_resumo}
    ---

    Responda de forma clara e organizada.
    """

    try:
        resposta_resumo_ia = llm.invoke(prompt).content
        print("AGENTE 1: Análise do resumo pela IA recebida com sucesso.")
    except Exception as e:
        print(
            f"ERRO (Agente 1): Problema ao se comunicar com a API do Google. Detalhe: {e}"
        )
        # Em caso de erro, definimos a resposta como vazia para não quebrar o resto do script
        resposta_resumo_ia = "Não foi possível analisar o resumo."

        # --- Busca por seções ---
    # Lista de "pistas" (títulos de seções) que vamos procurar no texto completo.
    pistas = [
        "DO OBJETO",
        "DA PARTICIPAÇÃO NA LICITAÇÃO",
        "DA APRESENTAÇÃO DA PROPOSTA",
        "DO TERMO DE CONTRATO",
    ]
    posicoes_encontradas = {}
    for pista in pistas:  # para cada pista na lista de pistas
        posicao = texto_completo.find(
            pista
        )  # encontrar a posição da pista no texto completo
        if (
            posicao != -1
        ):  # se a posição for diferente de -1, ou seja, se a pista foi encontrada
            print(f"  - Seção encontrada: '{pista}'")
            posicoes_encontradas[pista] = (
                posicao  # posicao encontrada  recebe a posicao da pista
            )
        else:
            print(f"  - Seção NÃO encontrada: '{pista}'")
    # --- busca específica por seção---
    secoes_ordenadas = sorted(
        posicoes_encontradas.items(), key=lambda item: item[1]
    )  # secoes ordenadas recebe a lista de posicoes.items que sao os itens com a chave e o valor, ordenados pela posicao (item[1])
    for i, secao_atual in enumerate(
        secoes_ordenadas
    ):  # para cada secao atual na lista de secoes ordenadas, com o indice i
        nome_secao = secao_atual[
            0
        ]  # nome da secao atual recebe o primeiro item da secao atual (o nome da secao)
        posicao_inicio = secao_atual[
            1
        ]  # posicao inicio recebe o segundo item da secao atual (a posicao da secao)
        posicao_fim = None
        if i + 1 < len(secoes_ordenadas):
            posicao_fim = secoes_ordenadas[i + 1][1]
        trecho_da_secao = texto_completo[posicao_inicio:posicao_fim]
        print(f"\n--- CONTEÚDO DA SEÇÃO: {nome_secao} ---")
        print(trecho_da_secao)
        print("----------------------------------------")

    return resposta_resumo_ia  # type: ignore
