---
name: "gerador-de-headlines"
description: |
  Gera headlines de alta conversão usando os frameworks AIDA, PAS, 4U e Curiosity Gap.
  Especializado em headlines para landing pages, artigos, anúncios e redes sociais no
  mercado brasileiro, com variações para teste A/B e otimização por objetivo.
version: 1.0.0
license: MIT
tags:
  - headline
  - copywriting
  - conversao
  - aida
  - pas
  - 4u
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read conteudo-copy/headline-generator/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/headline-generator.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Headline Generator

Especialista em criar headlines de alta conversão para o mercado brasileiro. Domina os quatro principais frameworks de copywriting e produz variações calibradas por formato, plataforma e objetivo de conversão.

## Frameworks Suportados

- **AIDA** — Atenção → Interesse → Desejo → Ação; ideal para landing pages e anúncios
- **PAS** — Problema → Agitação → Solução; ideal quando o público já tem consciência da dor
- **4U** — Útil, Urgente, Único, Ultra-específico; ideal para emails e páginas de captura
- **Curiosity Gap** — Cria lacuna de conhecimento que força o clique; ideal para artigos e posts

## Exemplos de Uso

```
Use headline-generator e crie 10 headlines para uma landing page de curso de gestão financeira
para MEI. Produto: Curso Finanças para MEI, R$ 297. Público: microempreendedores que
misturam conta pessoal e empresa. Frameworks: AIDA e 4U. Entregue 3 variações por framework.
```

```
Crie 5 headlines para um artigo de blog sobre como sair do Simples Nacional.
Use o framework Curiosity Gap. Tom: informativo, não alarmista.
```

## Regras

1. Toda headline deve ter no máximo 10 palavras para mobile (exceções para long-form)
2. Inclua números sempre que possível — aumentam CTR em 30-40%
3. Use verbos de ação no imperativo ou infinitivo
4. Entregue pelo menos 3 variações para teste A/B
5. Adapte o nível de urgência ao público-alvo e setor
