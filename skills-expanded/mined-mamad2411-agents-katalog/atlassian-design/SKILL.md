---
name: atlassian-design
description: >
  Design no padrão Atlassian Design System (ADS): tokens de cor/espaçamento/elevação, tipografia
  do sistema, azul de marca, densidade produtiva para ferramentas de trabalho (Jira, Confluence,
  Trello). Use quando o usuário mencionar: "Atlassian", "estilo Jira", "Confluence UI", "Trello",
  "design de ferramenta de time", "ADS", "design Atlassian". Consulta ../_shared/design-resources.md.
---

# Atlassian Design System (ADS)

Você atua como designer que domina o ADS — a linguagem por trás de Jira, Confluence, Bitbucket e Trello. É **produtivo, claro e consistente**: ferramentas onde times passam o dia, então o design reduz fricção e ruído.

## Princípios

1. **Token-first** — o ADS é 100% baseado em design tokens (cor, espaço, tipografia, elevação, sombra). Nunca valor cru.
2. **Clareza sobre decoração** — hierarquia forte, densidade confortável, nada que atrapalhe a tarefa.
3. **Acessível por padrão** — contraste, foco, teclado embutidos nos componentes.
4. **Consistência entre produtos** — mesmo botão, mesmo modal em todo o portfólio.

## Design tokens (ADS)

```css
:root {                              /* Light */
  --ds-background-neutral: #091e420f;
  --ds-surface: #ffffff;
  --ds-surface-sunken: #f7f8f9;
  --ds-surface-raised: #ffffff;
  --ds-text: #172b4d;                /* Neutral 1000 */
  --ds-text-subtle: #44546f;
  --ds-border: #091e4224;
  --ds-background-brand-bold: #0c66e4;      /* Atlassian Blue */
  --ds-background-brand-bold-hovered: #0055cc;
  --ds-background-danger-bold: #c9372c;
  --ds-background-success-bold: #22a06b;
  --ds-focus: #388bff;
}
:root[data-theme="dark"] {
  --ds-surface: #1d2125;
  --ds-surface-sunken: #161a1d;
  --ds-text: #c7d1db;
  --ds-background-brand-bold: #579dff;
  --ds-border: #a1bdd914;
}
```

## Tipografia (system font stack)

```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
/* code: 'SFMono-Regular', 'Roboto Mono', monospace */
--ds-font-heading-lg: 600 24px/28px;
--ds-font-heading-md: 600 20px/24px;
--ds-font-body: 400 14px/20px;       /* padrão */
--ds-font-body-sm: 400 12px/16px;
```

## Componentes-chave

```css
.ads-btn-primary {
  background: var(--ds-background-brand-bold); color: #fff; border: none;
  border-radius: 3px;                /* ADS usa radius pequeno (3px) */
  padding: 0 12px; height: 32px; font: 500 14px/1 inherit;
  transition: background .1s;
}
.ads-btn-primary:hover { background: var(--ds-background-brand-bold-hovered); }
.ads-btn-primary:focus-visible { outline: 2px solid var(--ds-focus); outline-offset: 2px; }

.ads-btn-subtle { background: transparent; color: var(--ds-text-subtle); border-radius: 3px; height: 32px; padding: 0 8px; }
.ads-btn-subtle:hover { background: var(--ds-background-neutral); }

.ads-card {
  background: var(--ds-surface-raised); border: 1px solid var(--ds-border);
  border-radius: 3px; box-shadow: 0 1px 1px #091e4240, 0 0 1px #091e424f;
}
.ads-lozenge { /* badge de status típico do Jira */
  display: inline-block; padding: 2px 6px; border-radius: 3px;
  font: 700 11px/1 inherit; text-transform: uppercase; letter-spacing: .5px;
  background: #dcfff1; color: #216e4e;   /* success */
}
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [atlassian.design](https://atlassian.design/) | Especificação completa: tokens, componentes, foundations, content. |
| [ADS tokens](https://atlassian.design/components/tokens/all-tokens) | Lista oficial de todos os design tokens (cor/espaço/tipografia). |
| [Atlaskit (GitHub)](https://bitbucket.org/atlassian/atlassian-frontend-mirror) | Componentes React oficiais. |
| [Atlassian Icons](https://atlassian.design/components/icon/icon-explorer) | Biblioteca oficial de ícones. |
| ../_shared/design-resources.md | Acessibilidade, densidade, dataviz. |

## Do / Don't

| Do | Don't |
|---|---|
| Tokens `--ds-*` | Hex/px solto |
| Radius 3px | Cantos muito arredondados |
| Lozenges para status | Texto colorido solto como status |
| Densidade confortável | Espaçamento gigante (é ferramenta de trabalho) |

## Checklist

- [ ] Tudo via tokens ADS
- [ ] Radius 3px em botões/cards
- [ ] Azul de marca `#0C66E4` em ações primárias
- [ ] Status via lozenge
- [ ] Foco 2px `focus-visible`
- [ ] Dark mode com tokens
