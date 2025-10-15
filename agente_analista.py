import fitz

# --- INÍCIO DA CONFIGURAÇÃO ---
NOME_ARQUIVO_PDF = "edital_teste.pdf"
NOME_ARQUIVO_SAIDA = "edital_completo.txt"
# --- FIM DA CONFIGURAÇÃO ---

try:  # tente abrir o arquivo PDF
    doc = fitz.open(NOME_ARQUIVO_PDF)
except Exception as e:  # se der erro, avise o usuário
    print(f"ERRO: Não foi possível abrir o arquivo '{NOME_ARQUIVO_PDF}'.")
    print(f"Detalhe do erro: {e}")
    # Encerra o script se não conseguir abrir o PDF
    exit()

print(
    f"PDF '{NOME_ARQUIVO_PDF}' aberto com sucesso! O documento tem {doc.page_count} páginas."
)
print("Iniciando a extração de texto...")

texto_completo = ""


for pagina in doc:

    texto_completo += pagina.get_text()  # type: ignore

print("\nExtração finalizada com sucesso!")

print("\n--- EXTRAINDO SEÇÃO DO OBJETO ---")

inicio_objeto = texto_completo.find("1. DO OBJETO")
fim_objeto = texto_completo.find(
    "2. DA IMPUGNAÇÃO AO EDITAL E DO PEDIDO DE ESCLARECIMENTO"
)

if inicio_objeto != -1 and fim_objeto != -1:
    texto_do_objeto = texto_completo[inicio_objeto:fim_objeto]
    print("Seção do objeto extraída com sucesso:")
    print(texto_do_objeto)
else:
    print(
        "ERRO: Não foi possível delimitar a seção do objeto com os marcadores definidos."
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
