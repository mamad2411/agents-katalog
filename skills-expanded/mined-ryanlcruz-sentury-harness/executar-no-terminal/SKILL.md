---
name: executar-no-terminal
description: "Analisar arquivo, banco de dados, planilha ou pasta do usuário rodando script no terminal, com autorização."
version: 1.0.0
author: Sentury
license: MIT
platforms: [linux, macos, windows]
tags: [terminal, shell, python, script, execucao, automacao,
       arquivo, arquivos, pasta, diretorio, banco, "banco de dados",
       sqlite, csv, planilha, xlsx, json, log, repositorio, meus,
       ler, leia, le, abrir, abre, extrair, processar, converter]
category: cognitive
---

# Executar no terminal

Quando o trabalho é sobre **os arquivos do usuário** — um banco numa pasta, uma
planilha, um repositório, uma automação — a rota é o terminal, não o sandbox.

O motivo é simples: no terminal o Python é o Python. Todas as bibliotecas
instaladas na máquina, o sistema de arquivos inteiro dentro do que foi liberado,
e a mesma permissão que vale para qualquer outro comando. O sandbox tem lista
branca de import, confinamento próprio e não enxerga pacote de terceiro — ele
existe para gerar artefato a partir de dado já em sessão, não para explorar o
material de alguém.

## A ordem que funciona

**1. Olhe antes de calcular.** Nunca adivinhe a estrutura.

```
ler_arquivo(caminho="C:/dados/vendas.csv", linhas=5)
```

Para um banco, liste as tabelas antes de consultar. Adivinhar o nome de uma
coluna, errar e devolver o erro ao usuário custa mais que uma chamada de leitura.

**2. Escreva o script.** Use `escrever_arquivo`. Um arquivo, com nome que diz o
que ele faz.

**3. Rode.**

```
executar_comando(comando="python analise_vendas.py", diretorio="C:/dados")
```

A saída volta em `saida`, com `codigo` de saída e `duracao_ms`. Se demorar, o
comando continua em segundo plano e você pega o resultado com `processos` (`acao: ver`)
usando o `id` devolvido.

**4. Leia a saída de verdade.** Erro de coluna, arquivo vazio, encoding errado —
tudo aparece ali. Corrija e rode de novo em vez de concluir por cima do erro.

## Autorização

Leitura roda direto. O que **altera** passa pelo registro de permissão: o harness
devolve a pergunta para a interface e o usuário escolhe — desta vez, nesta
sessão, sempre, ou não. Você não decide isso, e não tente contornar pedindo o
mesmo por outro caminho.

Se a pasta não estiver liberada, a resposta diz isso com o caminho. Peça acesso
em vez de tentar outro diretório.

## O que NÃO fazer

- Não use `python -c` com o código inteiro numa linha. Um script em arquivo é
  legível, corrigível e fica de rastro — a linha única vira uma parede.
- Não encadeie com `|`, `;` ou `&&`: aqui o comando roda sem shell interpretado,
  e o metacaractere é recusado. Rode um por vez.
- Não escreva fora da pasta de trabalho sem que ela tenha sido liberada.
- Não diga que gerou um arquivo antes de a saída confirmar que gerou.

## Quando o sandbox ainda é o certo

Gráfico, diagrama, slide, meme e PDF continuam pelo `executar_python`: ele
detecta o artefato gerado e **anexa sozinho** na conversa. Pelo terminal o
arquivo fica no disco e ninguém entrega — se precisar entregar um arquivo que o
script criou, use `entregar_arquivo` depois.
