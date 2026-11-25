---
name: apresentacao
vitrine:
  grupo: 'Entrega'
  rotulo: 'apresentação pptx'
description: "Apresentação .pptx em 16:9 a partir de um roteiro: capa, tópicos, imagem, tabela, duas colunas e notas."
version: 1.0.0
author: Sentury
license: MIT
tools_used: [escrever_arquivo, executar_script]
metadata:
  category: productivity
---

# Apresentação pptx

Para entregar slides, escreva o roteiro e converta. O script cuida do que
costuma sair errado à mão: texto que encolhe até ninguém ler, imagem
distorcida, tabela sem cabeçalho.

## Como fazer

1. Grave o roteiro em JSON (`escrever_arquivo`):

   ```json
   {
     "titulo": "Resultados de setembro",
     "subtitulo": "Equipe comercial",
     "slides": [
       {"secao": "Visão geral"},
       {"titulo": "O que mudou", "topicos": ["Vendas subiram 12%", "Churn caiu"],
        "notas": "Começar pelo número de vendas."},
       {"titulo": "Evolução", "imagem": "grafico.png", "legenda": "Vendas por semana"},
       {"titulo": "Por região", "tabela": [["Região", "Vendas"], ["Sul", "1.240"]]},
       {"titulo": "Antes e depois", "colunas": [["Antes", "manual"], ["Depois", "automático"]]}
     ]
   }
   ```

   Caminho de imagem relativo é relativo ao arquivo do roteiro. Para gráfico,
   gere a imagem antes (skill `grafico`).

2. Rode o script desta skill com `executar_script`, com caminhos completos:

   ```
   arquivo: <pasta desta skill>/scripts/roteiro_para_pptx.py
   argumentos: ["<caminho completo>/roteiro.json", "<caminho completo>/apresentacao.pptx"]
   ```

3. Entregue o arquivo com `entregar_arquivo`.

Um slide com mais de 7 tópicos vira dois, com "(continuação)" no título.
Tema, cores da marca e animação ficam de fora: para isso, escreva o código com
`python-pptx` em `executar_python`.
