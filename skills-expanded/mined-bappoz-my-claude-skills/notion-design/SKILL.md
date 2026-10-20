---
name: notion-design
description: >
  Design no padrão Notion: minimalismo monocromático, muito espaço em branco, conteúdo em blocos,
  tipografia limpa, cor pontual e sensação de documento vivo/editável. Use quando o usuário
  mencionar: "Notion", "estilo Notion", "editor de blocos", "wiki", "workspace de notas", "docs
  colaborativo", "app de produtividade minimalista", "design Notion". Consulta
  ../_shared/design-resources.md.
---

# Notion

Você atua como designer que domina a linguagem do Notion. É **calmo, monocromático e centrado no conteúdo**: quase preto-e-branco, espaço em branco generoso, e tudo é um bloco editável. A UI desaparece para o texto do usuário aparecer.

## Princípios

1. **Conteúdo é a interface** — o documento é o produto. Cromo mínimo, sem cores fortes competindo com o texto.
2. **Tudo é bloco** — parágrafo, título, imagem, tabela, toggle: unidades editáveis que se arrastam e transformam. Handles aparecem no hover.
3. **Monocromático + acento pontual** — base cinza/branco; cor só em callouts, tags e destaques raros.
4. **Espaço em branco como estrutura** — hierarquia por espaçamento e peso, não por linhas/caixas.
5. **Progressive disclosure** — controles surgem no hover; a tela em repouso é limpíssima.

## Design tokens

```css
:root {                              /* Light */
  --ntn-bg: #ffffff;
  --ntn-text: #37352f;               /* preto-quente característico */
  --ntn-text-secondary: #787774;
  --ntn-border: #e9e9e7;
  --ntn-hover: #f1f1ef;
  --ntn-accent: #2383e2;             /* azul de link/ação, discreto */
  /* Cores de tag/callout (fundos suaves) */
  --ntn-tag-gray: #f1f1ef; --ntn-tag-blue: #e7f3f8; --ntn-tag-red: #fbe4e4;
  --ntn-tag-yellow: #fbf3db; --ntn-tag-green: #edf3ec;
  --ntn-radius: 4px;
}
:root[data-theme="dark"] {
  --ntn-bg: #191919;
  --ntn-text: #d4d4d4;
  --ntn-text-secondary: #9b9b9b;
  --ntn-border: #2f2f2f;
  --ntn-hover: #2c2c2c;
  --ntn-accent: #529cca;
}
```

## Tipografia (system / limpa)

```css
font-family: ui-sans-serif, -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif;
/* opções do usuário: 'Serif' (Lyon) e 'Mono' */
--ntn-title: 700 40px/1.2;           /* título de página, grande */
--ntn-h1: 600 30px/1.3;
--ntn-h2: 600 24px/1.3;
--ntn-body: 400 16px/1.5;
letter-spacing: -0.01em;
```

## Componentes-chave

```css
.ntn-block {                         /* bloco: handle surge no hover */
  position: relative; padding: 3px 2px; border-radius: var(--ntn-radius);
}
.ntn-block:hover { background: var(--ntn-hover); }
.ntn-block__handle { opacity: 0; position: absolute; left: -24px; cursor: grab; }
.ntn-block:hover .ntn-block__handle { opacity: 1; }

.ntn-callout {                       /* bloco de destaque com emoji */
  display: flex; gap: 8px; padding: 16px; border-radius: var(--ntn-radius);
  background: var(--ntn-tag-blue); color: var(--ntn-text);
}
.ntn-tag { display: inline-block; padding: 2px 8px; border-radius: 3px;
  background: var(--ntn-tag-gray); font-size: 14px; color: var(--ntn-text-secondary); }

.ntn-btn { background: var(--ntn-accent); color: #fff; border: none;
  border-radius: var(--ntn-radius); padding: 6px 12px; font-size: 14px; font-weight: 500; }
.ntn-btn-ghost { background: transparent; color: var(--ntn-text-secondary); border-radius: var(--ntn-radius); padding: 6px 8px; }
.ntn-btn-ghost:hover { background: var(--ntn-hover); }
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [notion.so](https://www.notion.so/) | Referência viva: blocos, hover handles, espaço em branco, callouts. |
| [Notion — Brand](https://www.notion.so/brand) | Uso de logo, ilustração line-art, tom. |
| [Notion Design (blog)](https://www.notion.so/blog) | Filosofia de produto/craft. |
| [Fontshare](https://www.fontshare.com/) | Fallbacks limpos (sans/serif/mono) no espírito Notion. |
| ../_shared/design-resources.md | Tipografia, espaço em branco, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| Preto-quente `#37352f` sobre branco | Preto puro corporativo |
| Cor só em callout/tag | UI colorida |
| Controles no hover (progressive disclosure) | Tela cheia de botões |
| Hierarquia por espaço/peso | Caixas e bordas por toda parte |

## Checklist

- [ ] Monocromático, texto `#37352f` (light) / calmo
- [ ] Conteúdo em blocos com handle no hover
- [ ] Cor apenas em callouts/tags/links
- [ ] Espaço em branco generoso como estrutura
- [ ] Título de página grande (~40px)
- [ ] Dark mode + progressive disclosure
