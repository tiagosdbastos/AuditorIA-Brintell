# Importa as funções de cada agente
from agente_01_analista_de_documentos import analisar_documento
from agente_02_pesquisador_de_legislacao import pesquisar_legislacao
from agente_03_pesquisador_de_jurisprudencia import pesquisar_jurisprudencia
from agente_04_verificador_de_conformidade import verificar_conformidade # <- Importação do Agente 4
import json

# Nome do arquivo PDF a ser analisado
NOME_ARQUIVO_PDF = "edital_teste.pdf"

if __name__ == "__main__":
    print("--- ORQUESTRADOR: INICIANDO FLUXO DE ANÁLISE ---")

    # --- Etapa 1: Chamar Agente 1 ---
    print("\n--- ORQUESTRADOR: Acionando Agente 1 (Análise do Documento)... ---")
    resultado_agente_1 = analisar_documento(NOME_ARQUIVO_PDF)

    if resultado_agente_1:
        print("\n--- ORQUESTRADOR: Resultado da Análise do Agente 1 ---")
        # Imprime apenas o resumo e as chaves das seções para concisão
        print("Resumo Cabeçalho:", resultado_agente_1.get("resumo_cabecalho", "N/A"))
        print("Seções Extraídas:", list(resultado_agente_1.get("secoes_extraidas", {}).keys()))
        print("-----------------------------------------------------")

        # Guarda as informações importantes do Agente 1 para os próximos agentes
        resumo_cabecalho = resultado_agente_1.get("resumo_cabecalho", "")
        secoes_para_agente_4 = resultado_agente_1.get("secoes_extraidas", {}) # Dicionário com textos das seções

        # --- Etapa 2: Chamar Agente 2 ---
        print("\n--- ORQUESTRADOR: Acionando Agente 2 (Pesquisa de Legislação)... ---")
        resultado_agente_2 = pesquisar_legislacao(resumo_cabecalho) # Passa só o resumo

        if resultado_agente_2:
            print("\n--- ORQUESTRADOR: Resultado da Pesquisa de Legislação (Agente 2) ---")
            print(resultado_agente_2)
            print("-----------------------------------------------------------------")

            # --- Etapa 3: Chamar Agente 3 ---
            print("\n--- ORQUESTRADOR: Acionando Agente 3 (Pesquisa de Jurisprudência)... ---")
            resultado_agente_3 = pesquisar_jurisprudencia(resumo_cabecalho) # Passa só o resumo

            # Garante que resultado_agente_3 seja uma string, mesmo que retorne None ou falhe
            if not resultado_agente_3:
                 resultado_agente_3 = "Falha ao buscar jurisprudência." # Define um valor padrão

            print("\n--- ORQUESTRADOR: Resultado da Pesquisa de Jurisprudência (Agente 3) ---")
            print(resultado_agente_3)
            print("----------------------------------------------------------------------")

            # --- Etapa 4: Chamar Agente 4 ---
            print("\n--- ORQUESTRADOR: Acionando Agente 4 (Verificação de Conformidade)... ---")

            # Chama o Agente 4 passando as seções, legislação e jurisprudência
            resultado_agente_4 = verificar_conformidade(
                secoes_extraidas=secoes_para_agente_4,
                legislacao_aplicavel=resultado_agente_2,
                jurisprudencia_relevante=resultado_agente_3
            )

            # Verifica e imprime o resultado do Agente 4
            if resultado_agente_4:
                print("\n--- ORQUESTRADOR: Resultado da Verificação de Conformidade (Agente 4) ---")
                print(resultado_agente_4) # Imprime a análise de riscos
                print("-------------------------------------------------------------------------")
            else:
                print("--- ORQUESTRADOR: Falha na verificação de conformidade do Agente 4. ---")

        # Se o Agente 2 falhar, o fluxo para aqui para os agentes dependentes
        else:
            print("--- ORQUESTRADOR: Falha na pesquisa de legislação do Agente 2. Abortando verificação de conformidade. ---")
    # Se o Agente 1 falhar, o fluxo para aqui
    else:
        print("--- ORQUESTRADOR: Falha na análise inicial do Agente 1. Abortando fluxo. ---")

    print("\n--- ORQUESTRADOR: FLUXO DE ANÁLISE FINALIZADO ---")