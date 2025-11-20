# agente_05_sintetizador_de_relatorio.py

def sintetizar_relatorio(resumo_edital: str, legislacao: str, jurisprudencia: str, analise_riscos: str) -> str:
    print("AGENTE 5: Iniciando a síntese do Relatório de Análise Preliminar...")


    relatorio_markdown = f"""
## 1. Resumo do Edital

**Pontos-chave:**
{resumo_edital}
## 2. Legislação Aplicável

**Artigos/Seções relevantes da Lei nº 14.133/2021 sugeridos para verificação:**

{legislacao}

## 3. Jurisprudência Relevante

**Precedentes relacionados (ou status da busca):**

{jurisprudencia}

## 4. Análise Crítica Preliminar

**Pontos de Atenção, Riscos Potenciais e Possíveis Não Conformidades Identificadas:**

{analise_riscos}
---
*Este relatório foi gerado automaticamente pelo sistema Auditor-IA como um auxílio preliminar e não substitui a análise completa e criteriosa por um auditor humano.*
"""

    print("AGENTE 5: Relatório Markdown gerado com sucesso.")

    return relatorio_markdown
