for i, secao_atual in enumerate(secoes_ordenadas):
    nome_secao = secao_atual[0]
    posicao_inicio = secao_atual[1]
    posicao_fim = None
    if i + 1 < len(secoes_ordenadas):
        posicao_fim = secoes_ordenadas[i + 1][1]

    trecho_da_secao = texto_completo[posicao_inicio:posicao_fim]

    # Criamos o promp para esta seção
    prompt_secao = f"""
    Analise o seguinte trecho da seção '{nome_secao}' de um edital e faça um resumo dos pontos mais importantes para um auditor.

    Trecho:
    ---
    {trecho_da_secao[:4000]} # Limitamos para garantir que não estoura a janela de contexto
    ---
    """

    # Bloco para análise profunda e por seção.
    try:
        print(f"AGENTE 1: Analisando seção '{nome_secao}' com a IA...")
        resposta_secao_ia = llm.invoke(prompt_secao)
        analises_profundas += f"\n\n--- Análise da Seção: {nome_secao} ---\n{resposta_secao_ia.content}\n"
    except Exception as e:
        print(f"ERRO ao analisar a seção '{nome_secao}'. Detalhe: {e}")

        analises_profundas += (
            f"\n\n--- Análise da Seção: {nome_secao} ---\nERRO NA ANÁLISE: {e}\n"
        )
resultado_final_combinado = resposta_resumo_ia + analises_profundas  # type: ignore
return resultado_final_combinado