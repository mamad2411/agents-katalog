---
name: organizador-de-links
description: Use quando o usuário mandar vários links soltos e pedir para organizar, catalogar ou transformar em lista. Gatilhos: organiza esses links, junta esses links, monta uma lista com isso, catálogo de links. Não usar para salvar uma nota ou link único.
---

# Organizador de links

## O que ela faz

Recebe uma pilha de links soltos, descobre do que cada um trata, agrupa por
tema e devolve uma lista organizada em Markdown, pronta para colar em qualquer
lugar.

## Quando usar

- Você acumulou links nos salvos, no bloco de notas ou no WhatsApp.
- Você quer virar isso uma lista publicável, não um monte de URL.

## Como funciona

1. Separa todos os links do texto que o usuário mandou.
2. Abre cada um e identifica: título real, do que se trata e para que serve.
3. Agrupa por tema, criando os grupos a partir do que apareceu, sem forçar
   categorias que não existem no material.
4. Escreve uma linha de descrição própria para cada link, em português, dizendo
   o que a pessoa ganha ao clicar. Nunca copia a meta description do site.
5. Devolve em tabela Markdown, agrupada por tema.
6. Avisa separadamente sobre links quebrados, repetidos ou que exigem login.

## Regras

- Nunca inventa a descrição de um link que não conseguiu abrir. Marca como
  "não foi possível verificar" e segue.
- Nunca reordena os grupos por preferência própria. Ordena pelo número de
  links em cada um, do maior para o menor.
- Não adiciona links que o usuário não mandou, a menos que ele peça
  sugestões.

## Saída esperada

Uma tabela por tema, com as colunas Link, O que é e Para quem serve, mais uma
seção final com os links problemáticos.
