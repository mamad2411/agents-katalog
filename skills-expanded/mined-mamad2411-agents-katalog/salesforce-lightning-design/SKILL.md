---
name: salesforce-lightning-design
description: >
  Design no padrão Salesforce Lightning Design System (SLDS): design tokens, tipografia Salesforce
  Sans, BEM com prefixo slds-, densidade para CRM/enterprise, cor com semântica e acessibilidade.
  Use quando o usuário mencionar: "Salesforce", "Lightning", "SLDS", "estilo Salesforce", "CRM UI",
  "design enterprise Salesforce", "app Lightning". Consulta ../_shared/design-resources.md.
---

# Salesforce Lightning Design System (SLDS)

Você atua como designer que domina o SLDS — a linguagem do Salesforce para apps de CRM e enterprise. É **denso, orientado a dados e altamente padronizado** (nomenclatura BEM `slds-`), com foco em produtividade de quem usa o dia inteiro.

## Princípios

1. **Design tokens SLDS** — cor, espaço, tipografia e sizing vêm de tokens (`--slds-g-color-*`, design tokens do SLDS 2). Nunca valor cru.
2. **Nomenclatura BEM `slds-`** — classes utilitárias/componentes seguem `slds-block__element--modifier`.
3. **Densidade produtiva** — muita informação por tela (record pages, list views), com ritmo de 4px/8px.
4. **Semântica de cor** — sucesso/erro/aviso/info consistentes; marca em ações-chave.

## Design tokens

```css
:root {
  --slds-brand: #0176d3;             /* Salesforce Blue (SLDS 2) */
  --slds-brand-dark: #014486;
  --slds-bg: #ffffff;
  --slds-bg-alt: #f3f3f3;            /* app background */
  --slds-text: #181818;
  --slds-text-weak: #444444;
  --slds-border: #c9c9c9;
  --slds-success: #2e844a;
  --slds-warning: #fe9339;
  --slds-error: #ea001e;
  --slds-radius: 0.25rem;            /* 4px */
  --slds-radius-pill: 15rem;
}
:root[data-theme="dark"] {
  --slds-bg: #1a1b1e;
  --slds-bg-alt: #131315;
  --slds-text: #e5e5e5;
  --slds-border: #444;
  --slds-brand: #57a3fd;
}
```

## Tipografia (Salesforce Sans / fallback)

```css
font-family: 'Salesforce Sans', Arial, sans-serif;
--slds-heading-large: 700 1.75rem/1.25 'Salesforce Sans';
--slds-heading-medium: 700 1.25rem/1.25;
--slds-text-regular: 400 0.8125rem/1.5;   /* 13px, padrão SLDS */
--slds-text-small: 400 0.75rem/1.4;
```

## Componentes-chave (BEM slds-)

```css
.slds-button_brand {
  background: var(--slds-brand); color: #fff; border: 1px solid var(--slds-brand);
  border-radius: var(--slds-radius); padding: 0 1rem; height: 2rem;
  font: 400 0.8125rem/1 'Salesforce Sans'; transition: background .1s;
}
.slds-button_brand:hover { background: var(--slds-brand-dark); }
.slds-button_brand:focus { outline: 2px solid var(--slds-brand); outline-offset: 2px; }

.slds-input {
  border: 1px solid var(--slds-border); border-radius: var(--slds-radius);
  height: 2rem; padding: 0 0.75rem; background: var(--slds-bg);
}
.slds-input:focus { border-color: var(--slds-brand); box-shadow: 0 0 3px var(--slds-brand); outline: none; }

.slds-badge { display: inline-block; padding: 0.125rem 0.5rem; border-radius: var(--slds-radius-pill);
  background: var(--slds-bg-alt); color: var(--slds-text-weak); font-size: 0.75rem; }

.slds-card { background: var(--slds-bg); border: 1px solid var(--slds-border);
  border-radius: var(--slds-radius); box-shadow: 0 2px 2px rgba(0,0,0,.05); }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [lightningdesignsystem.com](https://www.lightningdesignsystem.com/) | Especificação completa: tokens, componentes (blueprints), utilities, ícones. |
| [SLDS Design Tokens](https://www.lightningdesignsystem.com/design-tokens/) | Lista oficial de tokens (cor/espaço/tipografia/sizing). |
| [SLDS Icons](https://www.lightningdesignsystem.com/icons/) | Biblioteca oficial (utility, standard, action, doctype). |
| [SLDS (GitHub)](https://github.com/salesforce-ux/design-system) | CSS/tokens open-source. |
| ../_shared/design-resources.md | Acessibilidade, densidade, dataviz. |

## Do / Don't

| Do | Don't |
|---|---|
| Classes `slds-*` BEM | Nomes ad-hoc |
| Tokens SLDS | Hex/rem solto |
| Densidade de CRM (linha ~2rem) | Layout arejado de landing page |
| Ícones SLDS | Ícone de outro set |

## Checklist

- [ ] Nomenclatura BEM `slds-`
- [ ] Tokens `--slds-*`
- [ ] Radius 4px (0.25rem)
- [ ] Fonte base 13px (0.8125rem)
- [ ] Semântica de cor consistente (success/warning/error)
- [ ] Foco visível + dark mode
