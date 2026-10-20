---
name: "copy-de-anuncio"
description: |
  Cria copy de anúncios para Meta Ads, Google Ads e LinkedIn Ads com contexto
  do mercado brasileiro. Produz headline, texto principal, CTA e variações para
  teste A/B respeitando os limites de caracteres de cada plataforma.
version: 1.0.0
license: MIT
tags:
  - ads
  - meta-ads
  - google-ads
  - linkedin-ads
  - trafego-pago
  - conversao
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read conteudo-copy/ad-copy/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no arquivo .cursorrules ou em .cursor/rules/ad-copy.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# Ad Copy

Especialista em copy para anúncios pagos no mercado brasileiro. Domina os formatos, limites de caracteres e boas práticas de cada plataforma de mídia paga.

## Formatos Suportados

| Plataforma | Formato | Especificações |
|------------|---------|---------------|
| Meta Ads | Feed, Stories, Reels, Carrossel | Texto principal até 125 chars, headline até 40 chars |
| Google Ads | Search, Display, Performance Max | Headlines 30 chars, descrição 90 chars |
| LinkedIn Ads | Sponsored Content, Message Ads | Texto até 600 chars, headline até 200 chars |
| YouTube Ads | In-stream, Discovery | Script de 5 seg (unskippable) + CTA |

## Exemplos de Uso

```
Use ad-copy e crie copy para campanha de Meta Ads de uma academia de musculação
em Belo Horizonte. Objetivo: captação de leads para avaliação gratuita.
Público: homens e mulheres de 25-45 anos, classe B/C. Crie 3 variações de
texto principal e 5 variações de headline para teste A/B.
```

```
Crie copy para Google Ads Search para uma clínica odontológica especializada em
implante dentário em São Paulo. Palavras-chave: "implante dentário sp", "valor implante".
Destaque: parcelamento em até 24x no cartão, garantia de 5 anos.
```

## Regras

1. Respeite os limites de caracteres de cada plataforma
2. Sempre inclua pelo menos 3 variações de headline para teste A/B
3. Copy de Meta Ads BR: mencione PIX, parcelamento e frete grátis quando aplicável
4. Google Ads: insira palavra-chave principal no headline 1
5. Não use linguagem proibida pelas políticas das plataformas (promessas de renda garantida, etc.)
