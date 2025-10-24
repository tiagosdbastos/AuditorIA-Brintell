from agente_01_analista_de_documentos import analisar_documento
from agente_02_pesquisador_de_legislacao import pesquisar_legislacao
from agente_03_pesquisador_de_jurisprudencia import pesquisar_jurisprudencia
import json

# A configuração do nome do arquivo
NOME_ARQUIVO_PDF = "edital_teste.pdf"

if __name__ == "__main__":
    print("--- ORQUESTRADOR: INICIANDO FLUXO DE ANÁLISE ---")

    # --- Etapa 1: Chamar Agente 1 ---
    print("\n--- ORQUESTRADOR: Acionando Agente 1 (Análise do Documento)... ---")
    resultado_agente_1 = analisar_documento(NOME_ARQUIVO_PDF)

    if resultado_agente_1:
        print("\n--- ORQUESTRADOR: Resultado da Análise do Agente 1 ---")
        print(json.dumps(resultado_agente_1, indent=2, ensure_ascii=False))
        print("-----------------------------------------------------")

        # --- Etapa 2: Chamar Agente 2 ---
        contexto_para_agentes = resultado_agente_1["resumo_cabecalho"]

        print("\n--- ORQUESTRADOR: Acionando Agente 2 (Pesquisa de Legislação)... ---")
        resultado_agente_2 = pesquisar_legislacao(contexto_para_agentes)

        if resultado_agente_2:
            print("\n--- ORQUESTRADOR: Resultado da Pesquisa de Legislação (Agente 2) ---")
            print(resultado_agente_2)
            print("-----------------------------------------------------------------")
            # --- Etapa 3: Chamar Agente 3 ---
            print("\n--- ORQUESTRADOR: Acionando Agente 3 (Pesquisa de Jurisprudência)... ---")
            resultado_agente_3 = pesquisar_jurisprudencia(contexto_para_agentes)

            if resultado_agente_3:

                print("\n--- ORQUESTRADOR: Resultado da Pesquisa de Jurisprudência (Agente 3) ---")
                print(...)
                print("----------------------------------------------------------------------")
            else:
                print("--- ORQUESTRADOR: Falha na pesquisa de jurisprudência do Agente 3. ---")

        else:
            print("--- ORQUESTRADOR: Falha na pesquisa de legislação do Agente 2. ---")

    else:
        print("--- ORQUESTRADOR: Falha na análise inicial do Agente 1. Abortando fluxo. ---")

    print("\n--- ORQUESTRADOR: FLUXO DE ANÁLISE FINALIZADO ---")