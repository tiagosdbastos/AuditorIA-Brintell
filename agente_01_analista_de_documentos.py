import os

import fitz as preader
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
        doc = preader.open(caminho_do_arquivo)
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
    marcador_final = "1. DO OBJETO"
    posicao_final = texto_completo.find(marcador_final)
    bloco_resumo = ""
    if posicao_final != -1:
        bloco_resumo = texto_completo[:posicao_final]
        print("AGENTE 1: Bloco de resumo extraído com sucesso.")
    else:
        print(
            "AVISO (Agente 1): Marcador '1. DO OBJETO' não encontrado. Usando texto completo."
        )
        bloco_resumo = texto_completo

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

    print("\n--- AGENTE 1: INICIANDO BUSCA PROFUNDA POR SEÇÕES ---")

    # Lista de "pistas" (títulos de seções) que vamos procurar no texto completo.
    pistas = [
        "DO VALOR ESTIMADO",
        "DOS PRAZOS",
        "DAS OBRIGAÇÕES DA CONTRATADA",
        "DAS SANÇÕES ADMINISTRATIVAS",
    ]

    # Loop que passa por cada 'pista' da nossa lista.
    for pista in pistas:
        # Usamos o .find() para procurar a pista no texto completo.
        posicao = texto_completo.find(pista)

        # Verificamos se a pista foi encontrada (posição diferente de -1).
        if posicao != -1:
            print(f"  - Pista encontrada: '{pista}' na posição {posicao}")
        else:
            print(f"  - Pista NÃO encontrada: '{pista}'")

    print("--- AGENTE 1: BUSCA PROFUNDA FINALIZADA ---")

    return resposta_resumo_ia  # type: ignore
