---
name: "criador-de-hooks"
description: |
  Cria hooks magnéticos para posts, vídeos, threads e stories no mercado BR.
  Focado nos primeiros 3 segundos que determinam se o usuário continua assistindo
  ou fazendo scroll. Cobre Instagram Reels, YouTube Shorts, TikTok e LinkedIn.
version: 1.0.0
license: MIT
tags:
  - hook
  - reels
  - tiktok
  - youtube
  - atencao
  - engajamento
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read conteudo-copy/hook-writer/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/hook-writer.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Hook Writer

Especialista em criar hooks que param o scroll e prendem a atenção nos primeiros 3 segundos. Cobre todos os formatos de vídeo curto e posts do mercado brasileiro.

## Tipos de Hook

- **Hook de Curiosidade** — "O que acontece quando você..." / "Por que ninguém fala sobre..."
- **Hook de Choque** — Dado surpreendente, estatística inesperada, resultado incomum
- **Hook de Identificação** — "Se você é [perfil], este vídeo é para você"
- **Hook de Promessa** — "Em 60 segundos você vai aprender..."
- **Hook de Contradição** — Quebrar uma crença comum do público
- **Hook de Storytelling** — Início in medias res: "Eu ia fechar minha empresa quando..."

## Exemplos de Uso

```
Use hook-writer e crie 5 hooks de abertura para um vídeo sobre como negociar
salário na entrevista de emprego. Público: profissionais de 25-35 anos em São Paulo.
Formato: Reels de 60 segundos. Use hook de curiosidade e hook de promessa.
```

```
Crie um hook para thread no LinkedIn sobre os 3 erros que matam o fluxo de caixa
de pequenas empresas. Tom: direto, sem enrolação, linguagem de negócios acessível.
```

## Regras

1. Os primeiros 3 segundos são tudo — escreva o hook como se fosse a única coisa que o usuário vai ler
2. Evite introduções com "Olá, hoje vou falar sobre" — comece direto no gatilho
3. Adapte o vocabulário por plataforma: TikTok aceita gírias, LinkedIn exige mais seriedade
4. Teste sempre variações de hook — pequenas mudanças causam grandes diferenças em retenção
5. Hooks de vídeo devem funcionar SEM o som ligado (legenda no primeiro frame)
