---
name: robinhood-design
description: >
  Design no padrão Robinhood: investimento simples e acessível, verde de marca #00C805, minimalismo,
  números/gráficos grandes, dark-first e microinterações. Use quando o usuário mencionar:
  "Robinhood", "estilo Robinhood", "app de investimento", "trading simples", "corretora", "ações e
  gráficos", "fintech de bolsa", "design Robinhood". Consulta ../_shared/design-resources.md.
---

# Robinhood

Você atua como designer que domina a linguagem do Robinhood. Missão de design: **democratizar investir** — tirar a complexidade e o jargão da bolsa e deixar acessível para qualquer um. Minimalismo, gráfico de linha grande, verde vibrante.

## Princípios

1. **Simplicidade radical** — uma tela de ativo mostra o essencial: nome, preço, gráfico, comprar/vender. Sem terminais complexos de trader.
2. **Verde de marca** — `#00C805` vibrante como identidade e para alta; a marca é o verde neon.
3. **O gráfico é o herói** — linha de preço grande, animada, interativa (scrub com o dedo). O dado conta a história.
4. **Dark-first + números grandes** — fundo escuro, tipografia grande para preço/variação; leitura instantânea.
5. **Microinterações** — animações de número, confete em marcos, feedback tátil tornam finança menos intimidadora.

## Design tokens

```css
:root {                              /* dark-first (padrão) */
  --rh-green: #00c805;               /* marca / alta */
  --rh-green-dark: #00a804;
  --rh-red: #ff5000;                /* baixa */
  --rh-bg: #0e0e0e;
  --rh-surface: #1c1c1c;
  --rh-text: #ffffff;
  --rh-text-muted: #a3a3a3;
  --rh-border: #2a2a2a;
  --rh-radius: 8px;
}
:root[data-theme="light"] {
  --rh-bg: #ffffff; --rh-surface: #f7f7f7; --rh-text: #0e0e0e;
  --rh-text-muted: #6b6b6b; --rh-border: #e5e5e5;
}
```

## Tipografia (Capsule Sans / fallback)

```css
/* Robinhood usa 'Capsule Sans'. Fallback próximo: */
font-family: 'Capsule Sans', 'Inter', -apple-system, system-ui, sans-serif;
--rh-display: 700 34px/1.1;          /* preço/valor grande */
--rh-title: 600 20px/1.25;
--rh-body: 400 16px/1.5;
--rh-value: 500 16px/1.4;            /* tabular p/ valores */
font-variant-numeric: tabular-nums;
```

## Componentes-chave

```css
/* Gráfico de linha herói (a cor segue alta/baixa do dia) */
.rh-chart { --line: var(--rh-green); }
.rh-chart--down { --line: var(--rh-red); }
.rh-chart path { stroke: var(--line); stroke-width: 2; fill: none; }
.rh-chart-glow { filter: drop-shadow(0 0 8px var(--line)); }

.rh-btn-primary {
  background: var(--rh-green); color: #000; border: none; border-radius: var(--rh-radius);
  height: 52px; width: 100%; font: 600 16px/1 'Capsule Sans'; transition: background .12s;
}
.rh-btn-primary:hover { background: var(--rh-green-dark); }
.rh-btn-sell { background: transparent; color: var(--rh-text);
  border: 1px solid var(--rh-border); border-radius: var(--rh-radius); height: 52px; width: 100%; }

.rh-asset-row { display: flex; align-items: center; justify-content: space-between;
  padding: 14px 0; border-bottom: 1px solid var(--rh-border); }
.rh-change--up { color: var(--rh-green); } .rh-change--down { color: var(--rh-red); }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [robinhood.com](https://robinhood.com/) | Referência viva: gráfico herói, verde, simplicidade, dark. |
| [Robinhood Design (blog)](https://newsroom.aboutrobinhood.com/) | Estudos de caso e princípios. |
| [Robinhood Brand](https://newsroom.aboutrobinhood.com/brand-assets/) | Uso do verde e logo. |
| [dataviz (skill)](../../../README.md) | Gráficos de preço acessíveis (cor não é a única pista). |
| ../_shared/design-resources.md | Cor semântica, tabular-nums, microinterações, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| Uma tela simples por ativo | Terminal de trader complexo |
| Gráfico grande e interativo | Gráfico minúsculo secundário |
| Verde `#00C805` marca/alta | Verde e vermelho sem consistência |
| Números grandes com tabular-nums | Preço pequeno/desalinhado |

## Checklist

- [ ] Simplicidade: essencial por tela (preço/gráfico/comprar-vender)
- [ ] Gráfico de linha herói (cor segue alta/baixa)
- [ ] Verde `#00C805` marca/alta, `#FF5000` baixa
- [ ] Dark-first, preço em display grande + tabular-nums
- [ ] Microinterações (número anima, marcos)
- [ ] Acessibilidade da cor (variação também em texto/seta) + light mode
