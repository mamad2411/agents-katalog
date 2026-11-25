---
name: pdf
vitrine:
  grupo: 'Entrega'
  rotulo: 'mexer em PDF'
description: "Ler, juntar, separar, extrair páginas, girar e preencher formulário de um PDF que já existe."
version: 1.0.0
author: Sentury
license: MIT
tools_used: [executar_script, entregar_arquivo]
metadata:
  category: productivity
---

# Mexer em PDF

Para um PDF que já existe. Para criar um relatório novo em PDF, use a skill
`relatorio-pdf`.

## Como fazer

Rode o script desta skill com `executar_script`, sempre com caminhos completos
(o diretório atual do script não é a pasta de trabalho):

```
arquivo: <pasta desta skill>/scripts/mexer_no_pdf.py
argumentos: ["<ação>", ...]
```

| ação | argumentos | o que faz |
|---|---|---|
| `info` | `arquivo.pdf` | páginas, título, autor, se é protegido e quantos campos de formulário tem |
| `texto` | `arquivo.pdf [--paginas 1-3] [--saida texto.txt]` | texto de cada página, marcado por página |
| `juntar` | `saida.pdf a.pdf b.pdf ...` | um PDF com todos, na ordem dada |
| `separar` | `arquivo.pdf pasta [--a-cada 1]` | um arquivo a cada N páginas |
| `paginas` | `arquivo.pdf "1-3,5" saida.pdf` | só as páginas pedidas |
| `girar` | `arquivo.pdf 90 saida.pdf [--paginas 2]` | gira de 90 em 90 graus |
| `campos` | `formulario.pdf` | nomes e valores dos campos, em JSON |
| `preencher` | `formulario.pdf valores.json saida.pdf` | preenche os campos com um JSON `{"campo": "valor"}` |

Página conta a partir de 1, como a pessoa vê no leitor. Para preencher, rode
`campos` antes: o nome do campo no JSON precisa ser igual ao do formulário, e
nome que o formulário não tem é recusado.

Entregue o resultado com `entregar_arquivo`.

PDF escaneado não tem texto para extrair: `texto` volta vazio. Nesse caso, o
caminho é ler a imagem da página.
