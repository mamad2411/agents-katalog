---
name: rc-seo
description: "Guias de SEO para auditoria e otimização. Use ao fazer auditoria técnica (meta tags, sitemap, robots.txt, schema.org, Core Web Vitals, indexação), otimização on-page e de conteúdo (palavra-chave, intenção de busca, headings) ou SEO programático (páginas em escala, internal linking). Não use para mídia paga ou análise de backlinks."
user-invocable: true
model: sonnet
effort: medium
---

# SEO — guias por tarefa

Guias práticos de SEO. Leia o guia da tarefa em `references/` antes de agir — cada um traz
o checklist, os comandos de verificação e os critérios de aceite. Ao auditar um projeto real,
combine com Grep/Glob para inspecionar o HTML/templates gerados; não presuma o markup.

## Roteamento

| Tarefa | Guia |
| ------ | ---- |
| Auditoria técnica (crawl, index, tags, structured data, CWV) | `references/technical.md` |
| Otimização on-page e de conteúdo (keyword, intent, copy) | `references/on-page.md` |
| SEO programático / páginas em escala | `references/programmatic.md` |

## Princípios sempre válidos

- **Uma intenção por página.** Cada URL responde a uma intenção de busca clara. Duas intenções → duas páginas.
- **Índice antes de rank.** Uma página não ranqueia se não for rastreada e indexada. Resolva crawl/index primeiro.
- **Conteúdo > truque.** Nenhuma tag conserta conteúdo que não satisfaz a intenção. Otimização técnica é piso, não teto.
- **Meça, não adivinhe.** Verifique com comandos/ferramentas reais (curl, o HTML renderizado, Search Console) antes de afirmar um problema.

## Error Handling

- Sem acesso ao site em produção: audite os templates/HTML no repo e diga explicitamente que a verificação é estática (sem CWV de campo nem status de indexação real).
- Se o site depende de renderização client-side (SPA), sinalize que o crawler pode ver HTML vazio — verifique o HTML servido, não só o DOM.
