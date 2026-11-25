---
name: planilha
vitrine:
  grupo: 'Entrega'
  rotulo: 'planilha xlsx'
description: "Planilha xlsx formatada a partir de CSV ou JSON, com cabeçalho, filtro e números que somam."
version: 1.0.0
author: Sentury
license: MIT
tools_used: [escrever_arquivo, executar_script]
metadata:
  category: productivity
---

# Planilha xlsx

Para entregar dados em Excel, grave a tabela e converta. O script resolve o
que costuma sair errado à mão: número gravado como texto (a planilha não soma),
coluna estreita, cabeçalho sem destaque, sem filtro.

## Como fazer

1. Grave os dados em CSV com cabeçalho, ou em JSON (`escrever_arquivo`):
   - uma lista de objetos vira uma aba;
   - um objeto `{"Setembro": [...], "Outubro": [...]}` vira uma aba por chave.
2. Rode o script desta skill com `executar_script`, com caminhos completos
   (o diretório atual do script não é a pasta de trabalho):

   ```
   arquivo: <pasta desta skill>/scripts/tabela_para_xlsx.py
   argumentos: ["<caminho completo>/vendas.csv", "<caminho completo>/vendas.xlsx",
                "--aba", "Setembro"]
   ```

3. Entregue o arquivo com `entregar_arquivo`.

A planilha sai com cabeçalho escuro, primeira linha congelada, filtro em todas
as colunas e largura ajustada ao conteúdo. Número em formato brasileiro
(`1.240`, `2.310,5`) vira número de verdade.

Fórmula, gráfico dentro da planilha e formatação condicional ficam de fora:
para isso, escreva o código com `openpyxl` em `executar_python`.
