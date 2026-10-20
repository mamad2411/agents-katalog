---
name: meta-design
description: >
  Design no padrão Meta (Facebook/Instagram): feed denso baseado em cards, azul de marca #0866FF,
  tipografia system/Optimistic, cantos suaves, alta densidade social e foco em conteúdo do usuário.
  Use quando o usuário mencionar: "Facebook", "Meta", "Instagram", "estilo Facebook", "feed social",
  "rede social", "timeline", "app social", "design Meta". Consulta ../_shared/design-resources.md.
---

# Meta (Facebook / Instagram)

Você atua como designer que domina a linguagem de produto da Meta. É **social, denso e limpo**: o conteúdo das pessoas é o protagonista; a UI é neutra, azul discreto, feita para escala de bilhões.

## Princípios

1. **Conteúdo do usuário primeiro** — a UI é cinza/branca e neutra para que fotos, textos e vídeos das pessoas ganhem foco.
2. **Card-based feed** — tudo é um card empilhado verticalmente; ação (curtir/comentar/compartilhar) padronizada no rodapé.
3. **Azul de sistema** — `#0866FF` (refresh 2023) para links, botões e marca; usado com moderação.
4. **Densidade confortável** — muita informação por tela, mas com respiro; hierarquia por peso e divisores sutis.
5. **Instagram = visual-first** — quando o contexto é IG: fundo branco/preto puro, grid de imagens, gradiente de marca só no branding.

## Design tokens

```css
:root {                              /* Facebook light */
  --meta-blue: #0866ff;              /* primary (2023) */
  --meta-blue-hover: #0a5dd8;
  --meta-bg: #f0f2f5;                /* fundo do feed */
  --meta-surface: #ffffff;          /* cards */
  --meta-text: #050505;
  --meta-text-secondary: #65676b;
  --meta-divider: #ced0d4;
  --meta-hover: #f2f2f2;
  --meta-radius: 8px;
  --meta-radius-card: 8px;
  /* Instagram brand gradient (só p/ branding) */
  --ig-gradient: linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);
}
:root[data-theme="dark"] {
  --meta-bg: #18191a;
  --meta-surface: #242526;
  --meta-text: #e4e6eb;
  --meta-text-secondary: #b0b3b8;
  --meta-divider: #3e4042;
  --meta-hover: #3a3b3c;
}
```

## Tipografia (system / Optimistic)

```css
/* Meta usa 'Optimistic' (proprietária) + system fallback */
font-family: 'Optimistic Display', -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
--meta-title: 700 24px/1.25;
--meta-post-name: 600 15px/1.3;      /* nome de quem postou */
--meta-body: 400 15px/1.4;
--meta-meta: 400 13px/1.35;          /* timestamp, secondary */
```

## Componentes-chave

```css
.meta-card {
  background: var(--meta-surface); border-radius: var(--meta-radius-card);
  box-shadow: 0 1px 2px rgba(0,0,0,.1); margin-bottom: 16px;
}
.meta-btn-primary {
  background: var(--meta-blue); color: #fff; border: none; border-radius: 6px;
  padding: 8px 12px; font: 600 15px/1 inherit; transition: background .1s;
}
.meta-btn-primary:hover { background: var(--meta-blue-hover); }
.meta-btn-secondary { background: #e4e6eb; color: var(--meta-text); border-radius: 6px; padding: 8px 12px; font-weight: 600; }
.meta-btn-secondary:hover { background: #d8dadf; }

/* Barra de ação do post */
.meta-actions { display: flex; border-top: 1px solid var(--meta-divider); }
.meta-action { flex: 1; padding: 8px; text-align: center; color: var(--meta-text-secondary);
  font-weight: 600; border-radius: 6px; }
.meta-action:hover { background: var(--meta-hover); }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [design.facebook.com](https://design.facebook.com/) | Filosofia de design da Meta, estudos de caso. |
| [Meta Brand](https://about.meta.com/brand/resources/) | Uso de logo, azul, tipografia. |
| [Instagram Brand](https://about.instagram.com/brand) | Gradiente e uso de marca do IG. |
| [Meta Design (Medium)](https://medium.com/meta-design) | Padrões de produto e acessibilidade em escala. |
| ../_shared/design-resources.md | Fotos, ícones, dark mode, densidade. |

## Do / Don't

| Do | Don't |
|---|---|
| UI neutra, conteúdo em foco | UI colorida competindo com o post |
| Azul `#0866FF` moderado | Azul por toda parte |
| Gradiente IG só no branding | Gradiente no feed inteiro |
| Cards com ação padronizada | Layout de post inconsistente |

## Checklist

- [ ] Feed em cards, fundo `#f0f2f5` (FB) neutro
- [ ] Azul `#0866FF` só em ação/link/marca
- [ ] Barra de ações (curtir/comentar/compartilhar) padronizada
- [ ] Instagram: visual-first, gradiente só no branding
- [ ] Dark mode
- [ ] Densidade confortável com divisores sutis
