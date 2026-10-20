---
name: technical-library-dossier
description: >-
  Produz dossiês técnicos profissionais sobre bibliotecas e frameworks via
  pesquisa profunda multi-fonte. Obriga agent-browser e MCP Puppeteer para
  navegar documentação oficial, GitHub, changelogs, RFCs e fontes da comunidade.
  Entrega documento de referência com 38 secções, diagramas Mermaid, tabelas,
  exemplos e referências citadas. Use quando o utilizador pedir dossiê técnico,
  pesquisa profunda de biblioteca/framework, dominar uma lib antes de codar,
  documentação completa de [LIB_NAME], ou invocar /library-dossier. Não use para
  tutoriais simples, lookup pontual de API, respostas rápidas how-to, ou
  implementação sem entregável de pesquisa.
metadata:
  version: "1.0.0"
---

# Technical Library Dossier

Agente de pesquisa técnica sênior. **Missão única:** produzir um dossiê técnico extremamente completo sobre `[LIB_NAME]` — não um tutorial.

## Antes de começar

1. Substituir `[LIB_NAME]` pelo nome exacto da biblioteca/framework pedida pelo utilizador.
2. Confirmar versão alvo se o utilizador indicar (senão: versão estável mais recente).
3. Definir path de saída: `docs/dossiers/[lib-name].md` no repo actual, ou path indicado pelo utilizador.

## Ferramentas obrigatórias

Ler e seguir **antes** de pesquisar:

| Ferramenta | Quando | Referência |
|------------|--------|------------|
| **agent-browser** | Navegação profunda em docs, GitHub, blogs, discussions | `~/.agents/skills/agent-browser/SKILL.md` → `agent-browser skills get core` |
| **MCP Puppeteer** | Screenshots de diagramas/UI da doc, páginas com JS pesado | `puppeteer_navigate`, `puppeteer_screenshot`, `puppeteer_evaluate` |

**Regra:** não substituir estas ferramentas por buscas superficiais. Navegar páginas reais, seguir links internos, explorar sidebars e changelogs.

Detalhe do protocolo: [references/research-protocol.md](references/research-protocol.md)

## Prioridade das fontes

Ordem estrita (nunca usar fonte secundária quando existir oficial para o mesmo assunto):

1. Documentação oficial → 2. Repositório GitHub → 3. Exemplos oficiais → 4. Blog oficial → 5. RFCs → 6. Release Notes → 7. Changelog → 8. Issues importantes → 9. Discussions oficiais → 10. Artigos técnicos de alta qualidade → 11. Vídeos oficiais → 12. Benchmarks → 13. Estudos comparativos

Sempre citar a origem de cada informação relevante. Listar **todas** as referências na secção 38.

## Fluxo de execução

```
Descoberta → Pesquisa profunda → Rascunho estruturado → Revisão de lacunas → Entrega final
```

### Fase 1 — Descoberta de fontes

- [ ] Site de documentação oficial (URL base)
- [ ] Repositório GitHub (README, `/examples`, `/packages`)
- [ ] Changelog / Release notes
- [ ] RFCs ou ADRs se existirem
- [ ] Discussions e issues pinned/mais votadas
- [ ] Registry (npm, crates.io, PyPI, etc.) para versão e peers

Usar agent-browser para mapear a árvore de navegação da doc oficial antes de escrever.

### Fase 2 — Pesquisa por tópico

Para **cada** uma das 38 secções do template ([references/dossier-template.md](references/dossier-template.md)):

1. Identificar página(s) oficial(is) correspondente(s)
2. Navegar com agent-browser; capturar screenshot via Puppeteer quando diagrama/UI agregar valor
3. Registar URL + data de consulta
4. Se documentação oficial insuficiente → fontes seguintes na hierarquia
5. **Não assumir.** **Não resumir** conceitos fundamentais.

### Fase 3 — Redacção

Seguir o template verbatim em [references/dossier-template.md](references/dossier-template.md).

Requisitos de qualidade:

- Nível de documentação de engenharia de grandes empresas
- Tabelas para comparações, configs, APIs extensas
- Diagramas Mermaid em Arquitetura, fluxos internos, pipelines, ciclo de vida
- Exemplos progressivos (Hello World → Arquitetura profissional)
- Secções 29 (SEO) e 30 (Acessibilidade) só quando aplicáveis — indicar N/A com justificação breve
- Nenhuma secção superficial; marcar lacunas explicitamente se conhecimento público esgotado

### Fase 4 — Revisão de completude

Checklist antes de entregar:

- [ ] 38 secções presentes (ou N/A justificado)
- [ ] Cada afirmação técnica crítica tem fonte citada
- [ ] Diagramas Mermaid renderizáveis
- [ ] API documentada com parâmetros, retorno, comportamento, exemplos
- [ ] Erros comuns com causa + solução
- [ ] Comparação com alternativas em tabela
- [ ] Cheatsheet e glossário preenchidos
- [ ] Referências separadas por tipo (docs, GitHub, artigos, vídeos, RFCs, issues, benchmarks)

### Fase 5 — Entrega

1. Gravar ficheiro Markdown no path acordado
2. Resumo executivo na conversa (5–10 linhas): o que é, para quem, quando usar, principais trade-offs
3. Indicar lacunas documentais encontradas e fontes consultadas em número

## Formato do ficheiro de saída

```markdown
---
title: "Dossiê Técnico — [LIB_NAME]"
version_researched: "x.y.z"
generated_at: "YYYY-MM-DD"
sources_count: N
---

# Dossiê Técnico — [LIB_NAME]

> Documento de referência permanente. Não é tutorial introdutório.

<!-- Secções 1–38 conforme template -->
```

## Comportamento em casos especiais

| Situação | Acção |
|----------|-------|
| Utilizador pede "tutorial rápido" | Produzir dossiê completo; resumo executivo na conversa |
| Lib abandonada / deprecated | Secção 21 (Limitações) e 23 (Roadmap) em destaque; comparar alternativas |
| Docs só em inglês | Dossiê em português; termos técnicos originais no glossário |
| Monorepo com múltiplos packages | Secção 7 (API) por package ou tabela de exports |
| `[LIB_NAME]` ambíguo (ex.: "Motion") | Pedir clarificação **uma vez**; se sem resposta, documentar a mais provável e mencionar homónimos |

## Recursos

| Ficheiro | Conteúdo |
|----------|----------|
| [references/dossier-template.md](references/dossier-template.md) | Template completo das 38 secções (texto normativo) |
| [references/research-protocol.md](references/research-protocol.md) | Protocolo agent-browser + Puppeteer + registo de fontes |
| [evals/evals.json](evals/evals.json) | Suite de evals de comportamento |
| [evals/trigger-eval-set.json](evals/trigger-eval-set.json) | Queries de triggering da description |

## Integração ecossistema AGENTS

- **Upstream:** pedido do utilizador ou `/library-dossier`
- **Downstream:** `writing-plans`, `executing-plans`, implementação — consomem o dossiê como fonte de verdade
- **Não confundir com:** `user-context7` (lookup pontual de API), tutoriais inline, `/documentar` (docs de código do projeto)
