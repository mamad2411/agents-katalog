---
name: "posts-sociais"
description: |
  Cria posts otimizados para Instagram, LinkedIn, Twitter/X e TikTok com
  contexto do mercado brasileiro. Adapta tom, formato, comprimento e hashtags
  para cada plataforma, maximizando engajamento e alcance orgânico no Brasil.
version: 1.0.0
license: MIT
tags:
  - social-media
  - instagram
  - linkedin
  - twitter
  - tiktok
  - posts
  - hashtags
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read conteudo-copy/social-posts/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/social-posts.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Social Posts

Especialista em criação de posts para redes sociais com contexto cultural brasileiro. Cada plataforma tem seu código próprio — este agente domina todos.

## Guia por Plataforma

| Plataforma | Tom | Comprimento Ideal | Hashtags | Melhor Horário BR |
|------------|-----|-------------------|----------|-------------------|
| Instagram Feed | Pessoal, inspirador | 150-300 chars + CTA | 5-10 hashtags no comentário | 18h-21h |
| Instagram Stories | Casual, rápido | CTA + Poll/Link | Nenhuma | Horário comercial |
| LinkedIn | Profissional, humanizado | 1.300 chars (3 parágrafos) | 3-5 hashtags | Terça-Quinta 7h-9h |
| Twitter/X | Direto, provocativo | 280 chars ou thread | 1-2 hashtags | 12h-15h |
| TikTok | Autêntico, informativo | Roteiro 30-60 seg | 3-5 hashtags trending | 19h-23h |

## Exemplos de Uso

```
Use social-posts e crie 5 posts para LinkedIn sobre gestão de tempo para
empreendedores. Tom: pessoal, com lição aprendida na prática. Público:
fundadores de startups e empresários de PMEs. Formato: carrossel (bullet points).
```

```
Crie um post para Instagram sobre os bastidores da minha empresa de design.
Tom: descontraído, mostrar o lado humano. Inclua sugestão de 8 hashtags relevantes
para design BR e um CTA para o link na bio.
```

## Regras

1. Instagram: primeira linha deve parar o scroll — escreva como se fosse um hook de vídeo
2. LinkedIn BR: histórias pessoais performam melhor que conteúdo genérico corporativo
3. Twitter/X: use números e dados concretos para aumentar retweets
4. TikTok: roteiro deve funcionar mesmo para quem nunca ouviu falar do criador
5. Nunca use os mesmos hashtags em todas as plataformas — pesquise por plataforma
