import fitz as preader
import os
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
        model="gemini-2.5-pro",
        temperature=0.1,
        convert_system_message_to_human=True,
    )

    prompt = f"""
    Você é um assistente especialista em análise de editais de licitação.
    Com base no texto de resumo do edital fornecido abaixo, extraia as seguintes informações:
    - Objeto da Licitação
    - Modalidade da Licitação
    - Data e Horário da Realização

    Texto do Resumo:
    ---
    {bloco_resumo}
    ---

    Responda de forma clara e organizada.
    """

    try:
        resposta_ia = llm.invoke(prompt)
        print("AGENTE 1: Análise da IA recebida com sucesso.")
        # Em vez de imprimir, agora vamos RETORNAR o resultado
        return resposta_ia.content  # type: ignore
    except Exception as e:
        print(
            f"ERRO (Agente 1): Problema ao se comunicar com a API do Google. Detalhe: {e}"
        )
        return None
