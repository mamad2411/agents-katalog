---
name: revolut-design
description: >
  Design no padrão Revolut: fintech premium dark-first, gradientes vibrantes, tipografia Aeonik,
  cartões metálicos, motion sofisticado e sensação de produto financeiro de ponta. Use quando o
  usuário mencionar: "Revolut", "estilo Revolut", "banco digital premium", "fintech dark", "cartão
  metálico", "super app financeiro", "neobank premium", "design Revolut". Consulta
  ../_shared/design-resources.md.
---

# Revolut

Você atua como designer que domina a linguagem do Revolut. É **premium, dark e sofisticado**: um super-app financeiro que parece caro e moderno. Fundos escuros, gradientes vibrantes, cartões que brilham e motion refinado.

## Princípios

1. **Dark-first premium** — fundos pretos/quase-pretos que fazem gradientes e cartões brilharem. Sensação de exclusividade.
2. **Gradientes como acento** — degradês vivos (roxo/azul/rosa) em cartões, gráficos e destaques. Energia contida, não poluição.
3. **Cartão é herói** — o cartão (metálico/gradiente) é o objeto central; renderizado com cuidado, quase 3D.
4. **Motion sofisticado** — transições suaves, números que animam, feedback tátil. O app parece "vivo" e caro.
5. **Denso mas elegante** — super-app com muitas funções, organizado com hierarquia clara e ícones consistentes.

## Design tokens

```css
:root {                              /* dark-first (padrão) */
  --rv-bg: #0a0a0a;
  --rv-surface: #171717;
  --rv-surface-2: #1f1f1f;
  --rv-text: #ffffff;
  --rv-text-muted: #8f8f8f;
  --rv-border: #2a2a2a;
  --rv-accent: #191c1f;
  --rv-blue: #0666eb;               /* ação */
  --rv-positive: #16b364;
  --rv-negative: #f04438;
  --rv-radius: 16px;
  /* Gradientes de marca */
  --rv-gradient-1: linear-gradient(135deg, #7b61ff 0%, #0666eb 100%);
  --rv-gradient-2: linear-gradient(135deg, #ff5e8a 0%, #7b61ff 60%, #0666eb 100%);
}
:root[data-theme="light"] {
  --rv-bg: #ffffff; --rv-surface: #f7f7f7; --rv-text: #0a0a0a;
  --rv-text-muted: #6b6b6b; --rv-border: #e5e5e5;
}
```

## Tipografia (Aeonik / fallback)

```css
/* Revolut usa 'Aeonik'. Fallback próximo: */
font-family: 'Aeonik', 'Inter', -apple-system, system-ui, sans-serif;
--rv-display: 700 clamp(32px,6vw,56px)/1.05;   /* saldo grande */
--rv-title: 600 22px/1.25;
--rv-body: 400 16px/1.5;
--rv-mono: 500 16px/1.4;             /* valores */
letter-spacing: -0.02em;             /* títulos apertados */
```

## Componentes-chave

```css
.rv-card-visual {                    /* o cartão herói, gradiente */
  aspect-ratio: 1.586;               /* proporção de cartão */
  background: var(--rv-gradient-2); border-radius: 20px;
  box-shadow: 0 20px 40px rgba(123,97,255,.25);
  padding: 20px; color: #fff; position: relative;
}
.rv-btn-primary {
  background: var(--rv-blue); color: #fff; border: none; border-radius: 100px;
  height: 52px; padding: 0 24px; width: 100%; font: 600 16px/1 'Aeonik'; transition: filter .12s;
}
.rv-btn-primary:hover { filter: brightness(1.1); }
.rv-btn-glass {                      /* botão em vidro sobre dark */
  background: rgba(255,255,255,.08); backdrop-filter: blur(20px); color: #fff;
  border: 1px solid rgba(255,255,255,.12); border-radius: 100px; height: 52px; padding: 0 24px;
}
.rv-list-item { display: flex; align-items: center; gap: 12px; padding: 14px 0;
  border-bottom: 1px solid var(--rv-border); }
.rv-amount--up { color: var(--rv-positive); font-variant-numeric: tabular-nums; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [revolut.com](https://www.revolut.com/) | Referência viva: dark premium, gradientes, cartões, motion. |
| [Revolut Design (Medium)](https://medium.com/revolut) | Estudos de caso de produto/design. |
| [Revolut Brand](https://www.revolut.com/news/) | Uso de gradiente, logo, tom premium. |
| [Codrops Hub](https://tympanus.net/codrops/hub/) | Gradientes animados e render 3D de cartão. |
| ../_shared/design-resources.md | Gradientes, glass/blur, dark mode, motion. |

## Do / Don't

| Do | Don't |
|---|---|
| Dark premium com gradiente de acento | Gradiente em cada pixel |
| Cartão renderizado com cuidado | Cartão genérico/flat |
| Motion suave e refinado | Animação exagerada/lenta |
| `tabular-nums` em valores | Números pulando de largura |

## Checklist

- [ ] Dark-first (bg `#0a0a0a`), gradientes como acento
- [ ] Cartão herói com gradiente + sombra colorida
- [ ] Azul `#0666EB` em ação; botões pill 52px
- [ ] Aeonik (ou fallback) com letter-spacing negativo
- [ ] Valores com `tabular-nums`, verde/vermelho semânticos
- [ ] Motion suave + light mode alternativo
