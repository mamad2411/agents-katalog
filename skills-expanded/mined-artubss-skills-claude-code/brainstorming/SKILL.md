---
name: brainstorming
description: "Você DEVE usar isso antes de qualquer trabalho criativo - criando funcionalidades, construindo componentes, adicionando funcionalidade ou modificando comportamento. Explora intenção do usuário, requisitos e design antes da implementação."
---

# Transformando Ideias em Designs

## Visão Geral

Ajude a transformar ideias em designs e especificações totalmente formados através de diálogo colaborativo natural.

Comece entendendo o contexto do projeto atual, depois faça perguntas uma por uma para refinar a ideia. Quando você entender o que está construindo, apresente o design em pequenas seções (200-300 palavras), verificando após cada seção se está certo até o momento.

## O Processo

**Entendendo a ideia:**
- Verifique primeiro o estado atual do projeto (arquivos, documentação, commits recentes)
- Faça perguntas uma por uma para refinar a ideia
- Prefira perguntas de múltipla escolha quando possível, mas aberto também é aceitável
- Apenas uma pergunta por mensagem - se um tópico precisar de mais exploração, divida em várias perguntas
- Foque em entender: propósito, restrições, critérios de sucesso

**Explorando abordagens:**
- Proponha 2-3 abordagens diferentes com trade-offs
- Apresente opções conversacionalmente com sua recomendação e raciocínio
- Comece com sua opção recomendada e explique o porquê

**Apresentando o design:**
- Uma vez que você acredite entender o que está construindo, apresente o design
- Divida em seções de 200-300 palavras
- Pergunte após cada seção se está certo até o momento
- Cubra: arquitetura, componentes, fluxo de dados, tratamento de erros, testes
- Esteja pronto para voltar e esclarecer se algo não ficar claro

## Depois do Design

**Documentação:**
- Escreva o design validado em `docs/plans/YYYY-MM-DD-<tópico>-design.md`
- Use a habilidade elements-of-style:writing-clearly-and-concisely se disponível
- Faça commit do documento de design no git

**Implementação (se continuando):**
- Pergunte: "Pronto para se preparar para a implementação?"
- Use superpowers:using-git-worktrees para criar espaço de trabalho isolado
- Use superpowers:writing-plans para criar plano de implementação detalhado

## Princípios-Chave

- **Uma pergunta por vez** - Não sobrecarregue com múltiplas perguntas
- **Múltipla escolha preferida** - Mais fácil responder do que aberto quando possível
- **YAGNI impiedosamente** - Remova funcionalidades desnecessárias de todos os designs
- **Explore alternativas** - Sempre proponha 2-3 abordagens antes de decidir
- **Validação incremental** - Apresente design em seções, valide cada uma
- **Seja flexível** - Volte e esclareça quando algo não ficar claro