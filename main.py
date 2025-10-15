from agente_01_analista_de_documentos import analisar_documento

NOME_ARQUIVO_PDF = "edital_teste.pdf"

if __name__ == "__main__":
    print("--- ORQUESTRADOR: INICIANDO FLUXO DE ANÁLISE ---")

    resultadoAgente1 = analisar_documento(NOME_ARQUIVO_PDF)

    if resultadoAgente1:
        print("\n--- RESULTADO DA ANÁLISE DO AGENTE 1 ---")
        print(resultadoAgente1)
    else:
        print("ORQUESTRADOR: A análise do Agente 1 falhou.")
