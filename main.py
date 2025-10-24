from agente_01_analista_de_documentos import analisar_documento
from agente_02_pesquisador_de_legislacao import pesquisar_legislacao

# A configuração do nome do arquivo
NOME_ARQUIVO_PDF = "edital_teste.pdf"

if __name__ == "__main__":
    print("--- ORQUESTRADOR: INICIANDO FLUXO DE ANÁLISE ---")

    # --- Etapa 1: Chamar Agente 1 ---
    print("\n--- ORQUESTRADOR: Acionando Agente 1 (Análise do Documento)... ---")
    resultado_agente_1 = analisar_documento(NOME_ARQUIVO_PDF)

    if resultado_agente_1:
        print("\n--- ORQUESTRADOR: Resultado da Análise do Agente 1 ---")
        print(resultado_agente_1)
        print("-----------------------------------------------------")
        print("\n--- ORQUESTRADOR: Acionando Agente 2 (Pesquisa de Legislação)... ---")
        # --- Etapa 2: Chamar Agente 2 ---
        resultado_agente_2 = pesquisar_legislacao(resultado_agente_1)
        if resultado_agente_2:
            print("\n--- ORQUESTRADOR: Resultado da Pesquisa de Legislação (Agente 2) ---")
            print(resultado_agente_2)
            print("-----------------------------------------------------------------")
        else:
            print("--- ORQUESTRADOR: Falha na pesquisa de legislação do Agente 2. ---")

    else:
        print("--- ORQUESTRADOR: Falha na análise inicial do Agente 1. Abortando fluxo. ---")

    print("\n--- ORQUESTRADOR: FLUXO DE ANÁLISE FINALIZADO ---")