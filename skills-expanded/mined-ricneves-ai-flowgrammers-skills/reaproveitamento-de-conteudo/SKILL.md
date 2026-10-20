---
name: "reaproveitamento-de-conteudo"
description: |
  Reaproveita conteúdo entre formatos com máxima eficiência: vídeo → artigo → posts →
  thread → email → stories. Preserva a essência da mensagem original e adapta o tom
  e estrutura para cada plataforma do ecossistema digital brasileiro.
version: 1.0.0
license: MIT
tags:
  - reaproveitamento
  - repurposing
  - conteudo
  - multicanal
  - distribuicao
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read conteudo-copy/content-repurposing/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/content-repurposing.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Content Repurposing

Especialista em extrair o máximo valor de cada conteúdo produzido, transformando uma fonte em múltiplos formatos para todos os canais da sua estratégia.

## Mapa de Transformação

```
FONTE PRINCIPAL
├── Vídeo/Podcast/Webinar
│   ├── Transcrição + edição → Artigo de blog
│   ├── Destaques → 5-10 posts para LinkedIn
│   ├── Citações → Thread Twitter/X
│   ├── Resumo → 3 emails para a lista
│   ├── Tópicos → 10 stories do Instagram
│   └── Clipes de 60s → Reels/TikTok
└── Artigo de blog
    ├── Resumo → Post LinkedIn longo
    ├── Subtópicos → Carrossel Instagram
    ├── Pontos principais → Thread Twitter/X
    └── CTA → Email para a lista
```

## Exemplos de Uso

```
Use content-repurposing. Tenho a transcrição de uma aula de 45 minutos sobre
estratégias de precificação para freelancers. Transforme em:
1. Artigo de blog de 1.200 palavras com SEO
2. 3 posts para LinkedIn (formato storytelling)
3. 1 thread Twitter/X com 8 tweets
4. Email de valor para a lista de leads
5. Roteiro para Reels de 60 segundos (top 3 insights)
```

## Regras

1. Nunca copie e cole o mesmo texto em plataformas diferentes — adapte o formato
2. O gancho de cada formato deve ser único, mesmo que o conteúdo seja o mesmo
3. Preserve a voz original do criador na adaptação
4. Identifique os 3-5 insights mais valiosos e priorize-os em todos os formatos
5. Cada formato deve ter um CTA específico para a plataforma de destino
