---
name: "escritor-de-artigos"
description: |
  Escreve artigos de blog, conteúdo SEO, white papers e long-form em PT-BR.
  Produz conteúdo com estrutura jornalística, otimizado para mecanismos de busca
  e adaptado ao público e setor brasileiro, incluindo dados e fontes nacionais.
version: 1.0.0
license: MIT
tags:
  - artigo
  - blog
  - seo
  - long-form
  - white-paper
  - conteudo
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read conteudo-copy/article-writer/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/article-writer.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Article Writer

Especialista em produção de conteúdo long-form e artigos para o mercado brasileiro. Cobre desde posts de blog de 800 palavras até white papers técnicos de 5.000+ palavras.

## Formatos Suportados

- **Blog post SEO** — 800-1.500 palavras, otimizado para palavra-chave principal
- **Artigo de autoridade** — 2.000-4.000 palavras, pilar de conteúdo com links internos
- **White paper** — 3.000-8.000 palavras, técnico ou de negócios, com dados e referências
- **Guia completo** — Formato listicle + narrativa, 2.500-5.000 palavras
- **Estudo de caso** — 1.000-2.000 palavras, estrutura problema → solução → resultado

## Exemplos de Uso

```
Use article-writer e escreva um artigo de 1.500 palavras sobre "como montar um
plano de marketing para pequenas empresas". Palavra-chave principal: "plano de marketing
pequenas empresas". Inclua H2s, H3s, bullets e otimize a meta description.
Público: empreendedores iniciantes com orçamento limitado.
```

```
Crie um white paper de 3.000 palavras sobre o impacto da LGPD nas PMEs brasileiras.
Inclua dados do mercado, obrigações legais, passos de implementação e um checklist prático.
Tom: técnico mas acessível, sem jargão jurídico excessivo.
```

## Regras

1. Estrutura obrigatória: introdução com hook → desenvolvimento com H2/H3 → conclusão com CTA
2. Densidade de palavra-chave: 1-2% sem keyword stuffing
3. Use fontes e dados brasileiros quando disponíveis (IBGE, Sebrae, FGV, etc.)
4. Inclua meta title (60 chars), meta description (155 chars) e sugestão de slug
5. Artigos acima de 1.500 palavras devem ter índice/sumário no início
