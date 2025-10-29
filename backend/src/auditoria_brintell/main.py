from .agents.agente_01_analista import analisar_documento
from .agents.agente_02_legislacao import pesquisar_legislacao
from .agents.agente_03_jurisprudencia import pesquisar_jurisprudencia
from .agents.agente_04_conformidade import verificar_conformidade
from .agents.agente_05_sintetizador import sintetizar_relatorio
import json
import os

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)


# NOME_ARQUIVO_PDF foi movido para o bloco __main__

def executar_fluxo_auditoria(caminho_do_pdf: str) -> str:
    print("--- ORQUESTRADOR: INICIANDO FLUXO DE ANÁLISE ---")

    # --- Etapa 1: Chamar Agente 1 ---
    print("\n--- ORQUESTRADOR: Acionando Agente 1 (Análise do Documento)... ---")
    resultado_agente_1 = analisar_documento(caminho_do_pdf)

    if resultado_agente_1:
        print("\n--- ORQUESTRADOR: Resultado da Análise do Agente 1 ---")
        # Imprime apenas o resumo e as chaves das seções para concisão
        print("Resumo Cabeçalho:", resultado_agente_1.get("resumo_cabecalho", "N/A"))
        print(
            "Seções Extraídas:",
            list(resultado_agente_1.get("secoes_extraidas", {}).keys()),
        )
        print("-----------------------------------------------------")

        # Guarda as informações importantes do Agente 1 para os próximos agentes
        resumo_cabecalho = resultado_agente_1.get("resumo_cabecalho", "")
        secoes_para_agente_4 = resultado_agente_1.get(
            "secoes_extraidas", {}
        )  # Dicionário com textos das seções

        # --- Etapa 2: Chamar Agente 2 ---
        print("\n--- ORQUESTRADOR: Acionando Agente 2 (Pesquisa de Legislação)... ---")
        resultado_agente_2 = pesquisar_legislacao(resumo_cabecalho)  # Passa só o resumo

        if not resultado_agente_2:
            print(
                "--- ORQUESTRADOR: Falha na pesquisa de legislação do Agente 2. ---"
            )
            resultado_agente_2 = "Falha ao buscar legislação."  # Define um valor padrão
        else:
            print(
                "\n--- ORQUESTRADOR: Resultado da Pesquisa de Legislação (Agente 2) ---"
            )
            print(resultado_agente_2)
            print("-----------------------------------------------------------------")

        # --- Etapa 3: Chamar Agente 3 ---
        print(
            "\n--- ORQUESTRADOR: Acionando Agente 3 (Pesquisa de Jurisprudência)... ---"
        )
        resultado_agente_3 = pesquisar_jurisprudencia(
            resumo_cabecalho
        )  # Passa só o resumo

        # Garante que resultado_agente_3 seja uma string, mesmo que retorne None ou falhe
        if not resultado_agente_3:
            resultado_agente_3 = (
                "Falha ao buscar jurisprudência."  # Define um valor padrão
            )

        print(
            "\n--- ORQUESTRADOR: Resultado da Pesquisa de Jurisprudência (Agente 3) ---"
        )
        print(resultado_agente_3)
        print(
            "----------------------------------------------------------------------"
        )

        # --- Etapa 4: Chamar Agente 4 ---
        print(
            "\n--- ORQUESTRADOR: Acionando Agente 4 (Verificação de Conformidade)... ---"
        )

        # Chama o Agente 4 passando as seções, legislação e jurisprudência
        resultado_agente_4 = verificar_conformidade(
            secoes_extraidas=secoes_para_agente_4,
            legislacao_aplicavel=resultado_agente_2,
            jurisprudencia_relevante=resultado_agente_3,
        )

        # Verifica e imprime o resultado do Agente 4
        if not resultado_agente_4:
            print(
                "--- ORQUESTRADOR: Falha na verificação de conformidade do Agente 4. ---"
            )
            resultado_agente_4 = "Falha na verificação de conformidade."  # Define um valor padrão
        else:
            print(
                "\n--- ORQUESTRADOR: Resultado da Verificação de Conformidade (Agente 4) ---"
            )
            print(resultado_agente_4)  # Imprime a análise de riscos
            print(
                "-------------------------------------------------------------------------"
            )

        # --- Etapa 5: Chamar Agente 5 ---
        print(
            "\n--- ORQUESTRADOR: Acionando Agente 5 (Sintetizador de Relatório)... ---"
        )

        # Chama o Agente 5 passando todos os resultados anteriores
        relatorio_final = sintetizar_relatorio(
            resumo_edital=resumo_cabecalho,  # Do Agente 1
            legislacao=resultado_agente_2,  # Do Agente 2
            jurisprudencia=resultado_agente_3,  # Do Agente 3
            analise_riscos=resultado_agente_4,  # Do Agente 4
        )

        # Verifica e imprime o Relatório Final
        if relatorio_final:
            print("\n--- ORQUESTRADOR: Relatório Final Gerado (Agente 5) ---")
            print(relatorio_final)  # Imprime o relatório em Markdown
            print("-------------------------------------------------------")
        else:
            # Isso não deve acontecer se a função retornar uma string, mas é uma segurança
            print(
                "--- ORQUESTRADOR: Falha na geração do relatório final pelo Agente 5. ---"
            )
            print("\n--- ORQUESTRADOR: FLUXO DE ANÁLISE FINALIZADO ---")
            return "Erro: Falha na geração do relatório final."

        print("\n--- ORQUESTRADOR: FLUXO DE ANÁLISE FINALIZADO ---")
        return relatorio_final

    # Se o Agente 1 falhar, o fluxo para aqui
    else:
        print(
            "--- ORQUESTRADOR: Falha na análise inicial do Agente 1. Abortando fluxo. ---"
        )
        print("\n--- ORQUESTRADOR: FLUXO DE ANÁLISE FINALIZADO ---")
        return "Erro: Falha na análise inicial do Agente 1."


if __name__ == "__main__":
    # Este bloco agora serve apenas para TESTAR sua função
    NOME_ARQUIVO_PDF = os.path.join(BASE_DIR, "data", "edital_teste.pdf")

    print("--- INICIANDO TESTE LOCAL DA FUNÇÃO 'executar_fluxo_auditoria' ---")
    relatorio_teste = executar_fluxo_auditoria(NOME_ARQUIVO_PDF)

    print("\n--- TESTE CONCLUÍDO ---")
    # print(relatorio_teste) # Opcional: imprimir o resultado do teste