---
name: grafico
vitrine:
  grupo: 'Visuais'
  rotulo: 'gráfico em PNG'
description: "Gráfico em PNG a partir de CSV ou JSON, com o visual do Sentury e desenhado na própria máquina."
version: 1.0.0
author: Sentury
license: MIT
tools_used: [escrever_arquivo, executar_script]
metadata:
  category: creative
---

# Gráfico em PNG

Para gráfico estático (anexar, mandar no Telegram, pôr num relatório), grave
os dados num arquivo e rode o script. Ele desenha local: os dados não saem da
máquina.

## Como fazer

1. Grave a tabela em CSV com cabeçalho, ou em JSON como lista de objetos
   (`escrever_arquivo`). Os números vêm de resultado que já está na conversa.
2. Rode o script desta skill com `executar_script`, com caminhos completos
   (o diretório atual do script não é a pasta de trabalho):

   ```
   arquivo: <pasta desta skill>/scripts/dados_para_grafico.py
   argumentos: ["<caminho completo>/vendas.csv", "<caminho completo>/vendas.png",
                "--x", "regiao", "--y", "total", "--titulo", "Vendas por região"]
   ```

   - `--y` repetido desenha várias séries lado a lado ou em linhas.
   - `--tipo`: `barra` (padrão), `barra-horizontal`, `linha`, `rosca`, `dispersao`.
3. Entregue o PNG com `entregar_arquivo`, e diga em uma frase o que ele mostra.

## Qual tipo

- Comparar categorias: `barra`; com rótulos longos ou muitas categorias,
  `barra-horizontal`.
- Evolução no tempo: `linha`.
- Partes de um todo, com até seis fatias: `rosca`.
- Relação entre duas medidas: `dispersao`, com `--y` duas vezes (x e y).

Número em formato brasileiro (`1.240`, `2.310,5`) é lido certo.
