import fitz

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

    texto_completo += pagina.get_text()  # type: ignore #texto completo recebe o texto da pagina atual

print("\nExtração finalizada com sucesso!")

print("\n--- EXTRAINDO SEÇÃO DO resumo ---")

# EXTRAIR APENAS A SEÇÃO DO resumo

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
    print(texto_do_resumo)
else:
    print(
        "ERRO: Não foi possível delimitar a seção do resumo com os marcadores definidos."
    )

try:  # tente salvar o texto extraído em um arquivo
    with open(
        NOME_ARQUIVO_SAIDA, "w", encoding="utf-8"
    ) as f:  # o with open cria o arquivo
        f.write(texto_completo)  # escreve o texto extraído no arquivo
    print(f"O texto completo foi salvo no arquivo: '{NOME_ARQUIVO_SAIDA}'")
except Exception as e:  # erro se der erro, avise o usuário
    print(f"ERRO: Não foi possível salvar o arquivo de saída.")
    print(f"Detalhe do erro: {e}")

# --- MELHORIA 2: UM RESUMO NO FINAL ---
print("--- RESUMO DA EXTRAÇÃO ---")
print(f"Total de páginas lidas: {doc.page_count}")
print(f"Total de caracteres extraídos: {len(texto_completo)}")
print("--------------------------")
