---
name: cloudscape-design
description: >
  Design no padrão Amazon Cloudscape (design system do console AWS): denso e orientado a dados,
  tokens, tipografia Amazon Ember, tabelas/formulários complexos, padrões de console em nuvem e
  acessibilidade. Use quando o usuário mencionar: "Cloudscape", "AWS console", "estilo AWS", "painel
  de nuvem", "console de administração", "dashboard técnico denso", "design Amazon". Consulta
  ../_shared/design-resources.md.
---

# Amazon Cloudscape

Você atua como designer que domina o Cloudscape — o design system open-source por trás do console da AWS. É **funcional, denso e consistente**: feito para telas complexas de administração de nuvem, onde clareza e produtividade dominam qualquer estética.

## Princípios

1. **Orientado a dados** — tabelas, filtros, paginação, propriedades: a informação é o produto. UI serve à leitura e ação em massa.
2. **Densidade com respiro** — espaçamento em escala (compact/comfortable), sem desperdício mas sem sufocar.
3. **Tokens e padrões prontos** — cor, espaço, tipografia via tokens; layouts de app padronizados (AppLayout, navegação lateral).
4. **Acessível por padrão** — contraste, teclado e leitor de tela embutidos.

## Design tokens

```css
:root {                              /* Light */
  --cs-bg: #ffffff;
  --cs-bg-secondary: #f2f3f3;        /* app background */
  --cs-text: #0f141a;
  --cs-text-secondary: #656871;
  --cs-border: #c6c6cd;
  --cs-primary: #006ce0;             /* Cloudscape blue */
  --cs-primary-hover: #002b66;
  --cs-success: #00802f;
  --cs-error: #db0000;
  --cs-warning: #8d6605;
  --cs-radius: 8px;
}
:root[data-theme="dark"] {
  --cs-bg: #161d26;
  --cs-bg-secondary: #0f141a;
  --cs-text: #d1d5db;
  --cs-border: #424650;
  --cs-primary: #42b4ff;
}
```

## Tipografia (Amazon Ember / fallback)

```css
font-family: 'Amazon Ember', 'Helvetica Neue', Roboto, Arial, sans-serif;
--cs-heading-xl: 400 42px/1.15 'Amazon Ember';
--cs-heading-m: 700 20px/1.25;
--cs-body: 400 14px/1.4;             /* padrão denso */
--cs-body-s: 400 12px/1.35;
```

## Componentes-chave

```css
.cs-btn-primary {
  background: var(--cs-primary); color: #fff; border: none; border-radius: 20px; /* Cloudscape usa botões pill */
  padding: 4px 20px; height: 32px; font: 700 14px/1 'Amazon Ember'; transition: background .1s;
}
.cs-btn-primary:hover { background: var(--cs-primary-hover); }
.cs-btn-normal {
  background: var(--cs-bg); color: var(--cs-primary);
  border: 2px solid var(--cs-primary); border-radius: 20px; padding: 4px 20px; height: 32px; font-weight: 700;
}

.cs-table th { background: var(--cs-bg-secondary); text-align: left; font-weight: 700;
  padding: 8px 20px; border-bottom: 1px solid var(--cs-border); }
.cs-table td { padding: 12px 20px; border-bottom: 1px solid var(--cs-border); }

.cs-container {                      /* card/section padrão */
  background: var(--cs-bg); border: 1px solid var(--cs-border);
  border-radius: var(--cs-radius); box-shadow: 0 1px 4px rgba(0,7,22,.1);
}
.cs-status--success { color: var(--cs-success); }   /* status inline com ícone */
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [cloudscape.design](https://cloudscape.design/) | Especificação completa: foundations, componentes, patterns de console. |
| [Cloudscape (GitHub)](https://github.com/cloudscape-design/components) | Componentes React open-source + tokens reais. |
| [Cloudscape — Design tokens](https://cloudscape.design/foundation/visual-foundation/design-tokens/) | Lista oficial de tokens. |
| [Cloudscape patterns](https://cloudscape.design/patterns/) | Padrões de tabela, formulário, criação de recurso. |
| ../_shared/design-resources.md | Acessibilidade, dataviz, densidade. |

## Do / Don't

| Do | Don't |
|---|---|
| Padrões de tabela/filtro prontos | Reinventar data table |
| Botões pill (radius 20px) | Cantos retos |
| Tokens `--cs-*` | Hex solto |
| AppLayout com nav lateral | Layout ad-hoc |

## Checklist

- [ ] Tokens Cloudscape (cor/espaço/tipografia)
- [ ] Botões pill, radius 20px
- [ ] Tabelas densas com header destacado
- [ ] Status inline com ícone + cor semântica
- [ ] Amazon Ember (ou fallback)
- [ ] Acessibilidade (teclado, contraste) + dark mode
