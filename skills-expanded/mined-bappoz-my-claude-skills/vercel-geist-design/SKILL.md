---
name: vercel-geist-design
description: >
  Design no padrão Vercel Geist: preto-e-branco de altíssimo contraste, tipografia Geist Sans/Mono,
  minimalismo absoluto, bordas finas, cantos moderados e foco em conteúdo/dev. Use quando o usuário
  mencionar: "Vercel", "Geist", "estilo Vercel", "preto e branco minimalista", "dev tool UI",
  "landing dev", "design Vercel". Consulta ../_shared/design-resources.md.
---

# Vercel (Geist)

Você atua como designer que domina o Geist — o design system da Vercel. É **preto-e-branco radical**: contraste máximo, tipografia como protagonista, quase nenhuma cor, e uma sensação de precisão técnica.

## Princípios

1. **Contraste é o design** — preto puro sobre branco puro (e vice-versa). Cinzas apenas para hierarquia secundária.
2. **Tipografia protagonista** — Geist Sans/Mono carregam a estética; pouco ornamento além do texto.
3. **Minimalismo funcional** — bordas de 1px, sombras quase inexistentes, muito espaço negativo.
4. **Cor com extrema parcimônia** — acentos semânticos (sucesso/erro/aviso) e nada mais.

## Design tokens (Geist)

```css
:root {                              /* Light */
  --geist-background: #ffffff;
  --geist-foreground: #000000;
  --geist-gray-100: #f2f2f2;
  --geist-gray-200: #ebebeb;
  --geist-gray-600: #666666;
  --geist-gray-900: #171717;
  --geist-border: #ebebeb;
  --geist-success: #0070f3;          /* Vercel blue (acento raro) */
  --geist-error: #e5484d;
  --geist-warning: #f5a623;
  --geist-radius: 6px;
}
:root[data-theme="dark"] {
  --geist-background: #000000;
  --geist-foreground: #ffffff;
  --geist-gray-100: #1a1a1a;
  --geist-gray-200: #2e2e2e;
  --geist-gray-600: #999999;
  --geist-border: #2e2e2e;
}
```

## Tipografia (Geist Sans / Geist Mono — open source)

```css
font-family: 'Geist', 'Geist Sans', -apple-system, system-ui, sans-serif;
/* code/números: 'Geist Mono' */
--geist-title: 600 40px/1.1 'Geist';   /* heros: grande e apertado */
--geist-heading: 600 24px/1.3;
--geist-body: 400 16px/1.5;
--geist-label: 500 14px/1.4;
--geist-mono: 400 13px/1.5 'Geist Mono';
letter-spacing: -0.02em;               /* headings apertados */
```

## Componentes-chave

```css
.geist-btn-primary {                 /* preto no light, branco no dark: inverte o fg */
  background: var(--geist-foreground); color: var(--geist-background);
  border: 1px solid var(--geist-foreground); border-radius: var(--geist-radius);
  height: 40px; padding: 0 16px; font: 500 14px/1 'Geist';
  transition: opacity .15s;
}
.geist-btn-primary:hover { opacity: .85; }

.geist-btn-secondary {
  background: var(--geist-background); color: var(--geist-foreground);
  border: 1px solid var(--geist-border); border-radius: var(--geist-radius); height: 40px; padding: 0 16px;
}
.geist-btn-secondary:hover { border-color: var(--geist-foreground); }

.geist-card {
  background: var(--geist-background); border: 1px solid var(--geist-border);
  border-radius: 12px; padding: 24px;
}
.geist-input {
  border: 1px solid var(--geist-border); border-radius: var(--geist-radius);
  height: 40px; padding: 0 12px; background: var(--geist-background); color: var(--geist-foreground);
}
.geist-input:focus { border-color: var(--geist-foreground); outline: none; }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [vercel.com/geist](https://vercel.com/geist/introduction) | Design system oficial: foundations, componentes, cor, tipografia. |
| [Geist fonts (GitHub)](https://github.com/vercel/geist-font) | Geist Sans/Mono open-source. |
| [Geist UI / Vercel design](https://vercel.com/design) | Guidelines de marca e uso. |
| [Vercel Icons / Geist Icons](https://vercel.com/geist/icons) | Biblioteca oficial de ícones. |
| ../_shared/design-resources.md | Tipografia, contraste, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| Preto/branco puro | Paleta colorida |
| Botão primário = fg invertido | Botão colorido chamativo |
| Bordas 1px, sem sombra | Sombras dramáticas |
| Geist Sans/Mono | Fonte decorativa |

## Checklist

- [ ] Preto/branco de contraste máximo
- [ ] Geist Sans + Geist Mono (números/código)
- [ ] Headings com `letter-spacing: -0.02em`
- [ ] Botão primário inverte foreground/background
- [ ] Bordas 1px, sombras mínimas
- [ ] Dark mode = preto puro
