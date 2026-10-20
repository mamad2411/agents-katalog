---
name: airtable-design
description: >
  Design no padrão Airtable: híbrido planilha-banco de dados, colorido e amigável, azul #2d7ff9,
  campos coloridos por tipo, cantos arredondados e produtividade lúdica. Use quando o usuário
  mencionar: "Airtable", "estilo Airtable", "planilha-banco", "no-code database", "grid de dados
  colorido", "app de tabelas", "base de dados visual", "design Airtable". Consulta
  ../_shared/design-resources.md.
---

# Airtable

Você atua como designer que domina a linguagem do Airtable. É **produtivo e colorido**: a potência de um banco de dados com a cara amigável de uma planilha. Cor organiza a informação e torna dado estruturado agradável.

## Princípios

1. **Cor como estrutura** — tipos de campo, tags e registros usam cor para dar sentido rápido a uma grade densa de dados. Cor é funcional, não decorativa.
2. **Planilha-banco amigável** — grade familiar (planilha) com poder de banco (relações, views, tipos de campo). A UI reduz o medo de "banco de dados".
3. **Views flexíveis** — mesma base em grid, kanban, calendar, gallery. UI consistente entre views.
4. **Amigável e arredondado** — cantos suaves, cores pastéis, microinterações; produtivo sem ser intimidador.

## Design tokens

```css
:root {
  --at-blue: #2d7ff9;                /* primária/ação */
  --at-blue-dark: #2568d8;
  --at-bg: #ffffff;
  --at-bg-alt: #f7f7f8;             /* app chrome */
  --at-text: #1d1f25;
  --at-text-muted: #616670;
  --at-border: #e5e5e5;
  /* Paleta de campos/tags (pastéis funcionais) */
  --at-red: #f82b60; --at-orange: #ff6f2c; --at-yellow: #fcb400;
  --at-green: #20c933; --at-teal: #20d9d2; --at-purple: #8b46ff; --at-pink: #ff08c2;
  --at-radius: 6px;
}
:root[data-theme="dark"] {
  --at-bg: #1d1f25; --at-bg-alt: #16171b; --at-text: #e5e5e5;
  --at-text-muted: #9ba1ac; --at-border: #3a3d45;
}
```

## Tipografia (system / Inter)

```css
font-family: 'Inter', -apple-system, 'Helvetica Neue', system-ui, sans-serif;
--at-title: 600 20px/1.3;
--at-body: 400 13px/1.4;             /* célula: densa */
--at-field-label: 500 11px/1.3;      /* nome de campo, uppercase-ish */
```

## Componentes-chave

```css
.at-btn-primary {
  background: var(--at-blue); color: #fff; border: none; border-radius: var(--at-radius);
  padding: 0 14px; height: 32px; font: 500 13px/1 'Inter'; box-shadow: 0 0 0 1px rgba(0,0,0,.08);
  transition: background .1s;
}
.at-btn-primary:hover { background: var(--at-blue-dark); }

.at-cell {                           /* célula de grid */
  border: 1px solid var(--at-border); padding: 6px 8px; font-size: 13px; min-height: 32px;
  background: var(--at-bg);
}
.at-cell:focus-within { box-shadow: inset 0 0 0 2px var(--at-blue); }

.at-tag {                            /* opção de single/multi-select colorida */
  display: inline-block; padding: 2px 10px; border-radius: 12px;
  font-size: 12px; font-weight: 500; color: #1d1f25;
  background: #ffeab6;               /* ex: yellow-light */
}
.at-record-card {                    /* card na view kanban/gallery */
  background: var(--at-bg); border: 1px solid var(--at-border); border-radius: var(--at-radius);
  padding: 12px; box-shadow: 0 1px 3px rgba(0,0,0,.08);
}
```

## Recursos externos

| Recurso | O que pegar |
|---|---|
| [airtable.com](https://www.airtable.com/) | Referência viva: grid colorido, views, tags, campos. |
| [Airtable — Design/Brand](https://www.airtable.com/newsroom) | Uso de cor, logo, tom amigável. |
| [Airtable Blocks/Extensions SDK](https://airtable.com/developers/apps) | Componentes de UI (cores, elementos). |
| ../_shared/design-resources.md | Paletas pastéis, densidade, dark mode. |

## Do / Don't

| Do | Don't |
|---|---|
| Cor funcional em tipos/tags | Cor aleatória decorativa |
| Grid familiar + poder de banco | UI de banco intimidadora |
| Views consistentes (grid/kanban/etc.) | Cada view com padrão diferente |
| Tags pastel com texto escuro | Tag saturada sem contraste |

## Checklist

- [ ] Cor usada para estruturar (tipos de campo, tags, registros)
- [ ] Azul `#2D7FF9` em ação primária
- [ ] Grid denso (célula ~13px) com foco azul
- [ ] Tags/selects coloridos em pill (texto legível)
- [ ] Cantos arredondados + tom amigável
- [ ] Views consistentes + dark mode
