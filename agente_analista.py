import os
import fitz
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")


# --- INÍCIO DA CONFIGURAÇÃO ---
NOME_ARQUIVO_PDF = "edital_teste.pdf"
NOME_ARQUIVO_SAIDA = "edital_completo.txt"
# --- FIM DA CONFIGURAÇÃO ---

try:  # tente abrir o arquivo PDF
    doc = fitz.open(NOME_ARQUIVO_PDF)  # biblioteca de leitura de pdf abrir o pdf
except Exception as e:  # se der erro, avise o usuário
    print(f"ERRO: Não foi possível abrir o arquivo '{NOME_ARQUIVO_PDF}'.")
    print(f"Detalhe do erro: {e}")
    # Encerra o script se não conseguir abrir o PDF
    exit()

print(
    f"PDF '{NOME_ARQUIVO_PDF}' aberto com sucesso! O documento tem {doc.page_count} páginas."  # f string  que mostra o nome do arquivoe suas paginas
)
print("Iniciando a extração de texto...")

texto_completo = ""  # slva o texto nessa variavel

for pagina in doc:  # para cada pagina no documento
    texto_completo += pagina.get_text()  # type: ignore # texto completo recebe o texto da pagina atual

print("\nExtração finalizada com sucesso!")

print("\n--- EXTRAINDO SEÇÃO DO RESUMO ---")

# EXTRAIR APENAS A SEÇÃO DO RESUMO
inicio_resumo = texto_completo.find(
    "PROCESSO ELETRÔNICO"
)  # encontra o inicio do resumo na variavel texto completo
fim_resumo = texto_completo.find(
    "1. DO OBJETO"
)  # procura o fim do resumo na variavel texto completo

if inicio_resumo != -1 and fim_resumo != -1:  # se encontrar o inicio e o fim do resumo
    texto_do_resumo = texto_completo[
        inicio_resumo:fim_resumo
    ]  # extrai o texto que ensta entre o inicio e o fim do resumo
    print("Seção do resumo extraída com sucesso:")
    # print(texto_do_resumo) # Vamos desativar este print para não poluir a tela
else:
    print(
        "ERRO: Não foi possível delimitar a seção do resumo com os marcadores definidos."
    )
    texto_do_resumo = ""  # Garante que a variável existe mesmo se não encontrar

# --- NOVO BLOCO: INTERAÇÃO COM A IA USANDO LANGCHAIN ---

if texto_do_resumo:  # Apenas executa a IA se tivermos um resumo para analisar
    print("\n--- INICIANDO CONEXÃO COM A IA---")

    # 1. Pega a chave de API do ambiente que o load_dotenv() carregou

    # 2. Verifica se a chave foi encontrada antes de continuar
    if not google_api_key:
        print("ERRO: Chave GOOGLE_API_KEY não encontrada no arquivo .env")
    else:
        # 3. Cria a instância do modelo de IA, passando a chave
        llm = ChatGoogleGenerativeAI(
            google_api_key=google_api_key,
            model="gemini-2.5-flash",  # Usando o modelo principal do Gemini
            temperature=0.1,
        )

        # 4. Cria a pergunta (prompt) para a IA, usando o texto que você extraiu
        prompt = f"""
        Você é um assistente especialista em análise de editais de licitação.
        Com base no texto de resumo do edital fornecido abaixo, extraia as seguintes informações:
        - Objeto da Licitação
        - Modalidade da Licitação
        - Data e Horário da Realização

        Texto do Resumo:
        ---
        {texto_do_resumo}
        ---

        Responda de forma clara e organizada.
        """

        print("Enviando pergunta para a IA... Aguarde.")

        # 5. Tenta enviar o prompt para a IA e receber a resposta
        try:
            resposta_ia = llm.invoke(prompt)

            # 6. Imprime o conteúdo da resposta da IA
            print("\n--- RESPOSTA DA INTELIGÊNCIA ARTIFICIAL ---")
            print(resposta_ia.content)
            print("-----------------------------------------")

        except Exception as e:
            print(f"\nERRO: Ocorreu um problema ao se comunicar com a API do Maritaca.")
            print(f"Detalhe do erro: {e}")

# ----------------------------------------------------------------

# O código abaixo continua o mesmo, salvando o arquivo completo
try:  # tente salvar o texto extraído em um arquivo
    with open(
        NOME_ARQUIVO_SAIDA, "w", encoding="utf-8"
    ) as f:  # o with open cria o arquivo
        f.write(texto_completo)  # escreve o texto extraído no arquivo
    print(f"\nO texto completo foi salvo no arquivo: '{NOME_ARQUIVO_SAIDA}'")
except Exception as e:  # erro se der erro, avise o usuário
    print(f"\nERRO: Não foi possível salvar o arquivo de saída.")
    print(f"Detalhe do erro: {e}")

# --- RESUMO FINAL DA EXTRAÇÃO ---
print("\n--- RESUMO DA EXTRAÇÃO ---")
print(f"Total de páginas lidas: {doc.page_count}")
print(f"Total de caracteres extraídos: {len(texto_completo)}")
print("--------------------------")
