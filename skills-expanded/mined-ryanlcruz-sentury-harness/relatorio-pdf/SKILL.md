---
name: relatorio-pdf
vitrine:
  grupo: 'Entrega'
  rotulo: 'relatório em PDF'
description: "Relatório em PDF a partir de markdown, com o visual do Sentury e sem escrever código de PDF."
version: 1.0.0
author: Sentury
license: MIT
tools_used: [escrever_arquivo, executar_script]
metadata:
  category: productivity
---

# Relatório em PDF

O conteúdo é seu; o desenho do PDF é do script. Escreva o relatório em
markdown e converta. Montar o PDF à mão com reportlab ou fpdf custa várias
voltas e costuma sair desalinhado; o script já resolve capa, cabeçalho,
rodapé com paginação, tabelas e acentos.

## Como fazer

1. Escreva o relatório em markdown num arquivo da pasta de trabalho
   (`escrever_arquivo`), por exemplo `relatorio.md`. Cada número vem de algo
   que já está na conversa: resultado de ferramenta, arquivo lido, dado que a
   pessoa passou.
2. Rode o script desta skill com `executar_script`, com caminhos completos
   (o diretório atual do script não é a pasta de trabalho):

   ```
   arquivo: <pasta desta skill>/scripts/markdown_para_pdf.py
   argumentos: ["<caminho completo>/relatorio.md", "<caminho completo>/relatorio.pdf",
                "--titulo", "Vendas de setembro"]
   ```

   Sem `--titulo`, a capa usa o primeiro `#` do texto.
3. Entregue o PDF com `entregar_arquivo`.

## O que o script entende

- `#` e `##` viram título de seção; `###` vira subtítulo.
- Lista com `-` ou `*`.
- Tabela markdown, com número e porcentagem alinhados à direita.
- Negrito, itálico e código inline saem como texto simples.

Emoji some: as fontes do PDF não têm esses caracteres. Imagem e gráfico não
entram por markdown; para gráfico, gere o PNG com a skill `grafico` e conte no
texto o que ele mostra.
