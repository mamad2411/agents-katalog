---
name: mente-designer
description: DNA de design de 20 sites premium (engenharia reversa via DevTools) — a fórmula Webflow/HTML + Lenis + GSAP/ScrollTrigger destilada em leis, calibres medidos e 22 efeitos nomeados com código. Use ao criar landing pages animadas, sites com scrollytelling, heroes tipográficos, vídeo-fundo, marquees, pin/scrub ou qualquer página que precise de "feel" de agência de elite.
---

# mente-designer — como usar esta skill

Esta skill é o **calibre de gosto** de um designer de elite, medido em 20 sites reais. Ela não gera páginas sozinha — ela diz **o quê** usar e **em que dose** para o resultado parecer premium.

## Fluxo (5 passos)

1. Leia `dna.md` — as 10 leis + a fórmula-mestre. É a base de toda decisão.
2. Escolha o esqueleto por setor em `fichas-por-site.md` (tech/IA, luxo/wellness, food, indústria, portfólio, experiência).
3. Decida os 4 eixos antes de codar: tipo de hero (frase editorial 4-6vw OU wordmark monumental 8-21vw), base de cor (quase-preta OU clara terrosa) + 1 cor de assinatura racionada, as 2 fontes, e a mídia-rainha (vídeo-loop mudo OU frame-scrub).
4. Construa com `receitas-codigo.md` (padrões com calibres exatos) e peça efeitos pelo nome usando `catalogo-efeitos.md` (22 efeitos: stacking, wipe, pin+scrub, velocity skew, ken burns…).
5. Feche no checklist do `dna.md`: zero firula de entrada, no máximo 1 pin por página, ~14 telas, peso sob controle.

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `dna.md` | As 10 leis + a fórmula-mestre |
| `fichas-por-site.md` | Tabela dos 20 sites medidos + leituras transversais |
| `receitas-codigo.md` | Padrões em código com calibres medidos (boot da pilha, vídeo-fundo, wordmark, marquee, sticky, cursor…) |
| `catalogo-efeitos.md` | Glossário nomeado dos 22 efeitos, cada um com snippet |
| `data/fingerprints.json` | Dados brutos das 20 medições |
| `demos/stacking-e-wipe.html` | Demo ao vivo (rode `node server.mjs` → http://localhost:8091/demos/stacking-e-wipe.html) |

## Regras de ouro (resumo)

- Pilha única: HTML/Webflow + **Lenis** (sempre) + GSAP/ScrollTrigger (+ SplitType).
- 2 fontes no máximo; base neutra + 1 cor viva racionada (1-3 seções).
- Vídeo-loop mudo é a mídia rainha; frame-scrub é raro e cirúrgico.
- `position: sticky` em tudo, **1 único pin** por página.
- Zero preloader/cursor custom/carrossel/popup por padrão — a sofisticação está no scroll.
