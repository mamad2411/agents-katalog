---
name: uber-base-design
description: >
  Design no padrão Uber Base (Base Web design system): preto-e-branco de alto contraste, tipografia
  Uber Move, grid rígido, tokens e componentes funcionais para mobilidade/marketplace em escala
  global. Use quando o usuário mencionar: "Uber", "Base Web", "estilo Uber", "app de mobilidade",
  "app de corrida", "marketplace de serviço", "design Uber". Consulta ../_shared/design-resources.md.
---

# Uber Base (Base Web)

Você atua como designer que domina o Base — o design system do Uber. É **preto-e-branco, funcional e global**: alto contraste para legibilidade em qualquer luz (motorista dirigindo, rua ensolarada), estrutura rígida e zero ornamento supérfluo.

## Princípios

1. **Alto contraste primeiro** — preto sobre branco; a UI precisa ser lida em movimento, no sol, com pressa. Cor é acento raro.
2. **Funcional e direto** — cada tela tem uma ação clara (confirmar corrida, pagar). Sem distração.
3. **Grid e tokens rígidos** — espaçamento em escala de 8px; componentes do Base Web tokenizados e temáveis.
4. **Global e acessível** — funciona em dezenas de idiomas/mercados; contraste e tamanho de toque generosos.

## Design tokens

```css
:root {                              /* Base light */
  --base-black: #000000;             /* primária (ações, texto) */
  --base-white: #ffffff;
  --base-mono-100: #f6f6f6;          /* fundos sutis */
  --base-mono-300: #e2e2e2;          /* bordas */
  --base-mono-600: #757575;          /* texto secundário */
  --base-accent: #276ef1;            /* Uber blue (acento/links) */
  --base-positive: #05944f;
  --base-negative: #e11900;
  --base-warning: #ffc043;
  --base-radius: 8px;
}
:root[data-theme="dark"] {
  --base-black: #ffffff; --base-white: #141414;
  --base-mono-100: #1f1f1f; --base-mono-300: #333333; --base-mono-600: #b0b0b0;
  --base-accent: #5b91f5;
}
```

## Tipografia (Uber Move / fallback)

```css
/* Uber Move é proprietária. Fallback próximo: */
font-family: 'Uber Move', 'UberMoveText', system-ui, -apple-system, 'Helvetica Neue', sans-serif;
--base-display: 700 36px/1.15;       /* preço, valor grande */
--base-heading: 500 20px/1.25;
--base-body: 400 16px/1.5;
--base-label: 500 14px/1.4;
```

## Componentes-chave

```css
.base-btn {                          /* botão preto full-width (padrão Uber) */
  background: var(--base-black); color: var(--base-white); border: none;
  border-radius: var(--base-radius); height: 48px; width: 100%;
  font: 500 16px/1 'Uber Move'; transition: opacity .15s;
}
.base-btn:hover { opacity: .85; }
.base-btn-secondary { background: var(--base-mono-100); color: var(--base-black);
  border: none; border-radius: var(--base-radius); height: 48px; width: 100%; font-weight: 500; }

.base-input {
  background: var(--base-mono-100); border: 2px solid transparent; border-radius: var(--base-radius);
  height: 48px; padding: 0 16px; font-size: 16px; color: var(--base-black);
}
.base-input:focus { border-color: var(--base-black); outline: none; background: var(--base-white); }

.base-card { background: var(--base-white); border: 1px solid var(--base-mono-300);
  border-radius: 12px; padding: 16px; }
.base-list-item {                    /* ex: opção de veículo */
  display: flex; align-items: center; gap: 16px; padding: 16px; border-radius: var(--base-radius);
}
.base-list-item--selected { border: 2px solid var(--base-black); }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [base.uber.com](https://base.uber.com/) | Design system Base: foundations, componentes, tokens. |
| [Base Web (baseweb.design)](https://baseweb.design/) | Biblioteca React open-source do Uber + tokens reais. |
| [Base Web (GitHub)](https://github.com/uber/baseweb) | Código dos componentes. |
| [Uber Brand](https://www.uber.com/us/en/about/) | Uso de preto/branco, Uber Move, fotografia. |
| ../_shared/design-resources.md | Contraste, tamanho de toque, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| Preto/branco de alto contraste | Paleta colorida chamativa |
| Botão preto full-width | Botão pequeno/colorido |
| Uma ação clara por tela | Múltiplos CTAs competindo |
| Grid 8px + tokens Base | Espaçamento ad-hoc |

## Checklist

- [ ] Alto contraste (preto sobre branco)
- [ ] Botão primário preto, full-width, 48px
- [ ] Azul `#276EF1` só como acento/link
- [ ] Uma ação primária clara por tela
- [ ] Espaçamento em escala de 8px
- [ ] Tamanhos de toque generosos + dark mode
