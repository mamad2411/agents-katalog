---
name: knowledge
description: Indexa, busca e sugere docs .md espalhados por ~/Desktop/knowledge/, pelo repo do projeto atual, e pelo dir de memory do Claude. Use quando o usuario perguntar "o que eu tinha doc sobre X?", "tem alguma ideia stale?", ou quando voce (Claude) terminar uma sessao tecnica e quiser sugerir docs relacionados pra atualizar/conectar. Tambem usado pra criar novos docs com frontmatter padronizado nos lugares certos. Aceita subcomandos: stale, drafts, related, suggest, new, index.
---

# /knowledge — federa busca + lifecycle em docs `.md`

Voce eh um "bibliotecario" pros docs `.md` do usuario. Tres fontes:

1. **`~/Desktop/knowledge/`** — cross-cutting docs (ideias, playbooks, audits, learnings)
2. **Repo do projeto atual** — `find . -name "*.md" -not -path "*/node_modules/*"` (cwd atual)
3. **Memory do Claude** — `~/.claude/projects/<projeto>/memory/` se aplicavel

## Subcomandos

`$1` define o que fazer. Se vazio, default eh `index`.

### `/knowledge index` (default)

Imprime visao organizada de tudo. Format:

```
Knowledge base summary
======================

CENTRAL (~/Desktop/knowledge/)
- ideas/ (N docs, X stale)
- playbooks/ (N docs)
- audits/ (N docs, X stale)
- learnings/ (N docs)
- archive/ (N docs)

PROJECT (cwd)
- doc1.md (last_review: 2026-05-17, status: active)
- doc2.md (last_review: 2026-04-12, STALE)
...

MEMORY (~/.claude/projects/.../memory)
- memory1.md (type: feedback)
- memory2.md (type: project)

CONTENT DRAFTS
- 2026-05-17-claude-mcp-bigquery-ga4/ (4 platforms, status: drafted)
- ...
```

Format limpo, ordenado, status visiveis. Maximo ~50 linhas — se passar, agrupa por tag.

### `/knowledge stale [days]`

Lista docs onde `last_review` > N dias atras (default 60).

Para cada `.md` em todas as fontes:
1. Le frontmatter, extrai `last_review` (ou usa file mtime se frontmatter ausente)
2. Calcula dias desde ultima review
3. Se > threshold, inclui na lista
4. Ordena por staleness (mais velho primeiro)

Output:
```
Docs stale (last_review > 60 dias):

1. ~/Desktop/knowledge/audits/ga4-audit-2025-q4.md
   last_review: 2025-11-20 (178 dias atras)
   tags: [analytics, ga4]
   sugestao: re-validar com dado atual ou archive

2. /Users/.../mysite/PORTFOLIO_STRUCTURE_RESEARCH.md
   last_review: ausente, mtime: 2026-02-10 (96 dias atras)
   sugestao: adicionar frontmatter ou archive
```

### `/knowledge drafts`

Lista content drafts nao publicados.

Scaneia `<project>/content/drafts/` no repo atual. Pra cada subdir:
- Le os 4 .md (linkedin/twitter/instagram/article)
- Checa se tem checklist `[x]` indicando posted ou se ainda esta `[ ]`
- Lista grouped por status

Output:
```
Content drafts:

UNPOSTED (todas checkboxes pendentes)
- 2026-05-17-claude-mcp-bigquery-ga4/ (4 platforms)
- 2026-05-17-site-audit-bot-discovery/ (4 platforms)
- 2026-05-17-claude-content-machine/ (4 platforms)

PARTIALLY POSTED
(nenhum)

POSTED (>=1 checkbox checked)
(nenhum)
```

### `/knowledge related <topico>`

Faz grep semântico atraves de todas as fontes. Procura `<topico>` em:
- Frontmatter tags
- Titulos H1/H2
- Body content (ranqueado por densidade)

Retorna lista ordenada por relevancia (max 10).

Output:
```
Docs relacionados a "analytics":

[CENTRAL/audits] ga4-audit-2025-q4.md (5 hits)
[PROJECT] ENGAGEMENT_AUDIT.md (12 hits, recent)
[PROJECT] ANALYTICS_CLEANUP.md (8 hits, recent)
[PROJECT] ANALYTICS_DB_SETUP.md (6 hits, recent)
[PROJECT] MCP_ANALYTICS_SETUP.md (4 hits, recent)
[MEMORY] skill-content.md (1 hit)
```

Se 0 resultados, sugere criar novo: "Nenhum doc sobre 'X'. Quer criar um com `/knowledge new`?"

### `/knowledge suggest`

Modo proativo: analisa o que foi trabalhado na sessao atual (git diff recente, commits, arquivos modificados) e sugere docs existentes relacionados.

Logica:
1. Identifica topicos da sessao (commit messages, file paths, conversation context)
2. Roda `/knowledge related` internamente pra cada topico
3. Apresenta docs candidatos pra:
   - **Atualizar** (mesmo topico, recent)
   - **Conectar** (topico adjacente, vale linkar)
   - **Substituir** (doc obsoleto sobre mesmo topico)

Output (compacto):
```
Trabalho da sessao toca em: [analytics, ga4, mcp]

Docs candidatos:
- ENGAGEMENT_AUDIT.md → atualizar com numbers novos
- MCP_ANALYTICS_SETUP.md → linkar do novo doc se criar
- ~/Desktop/knowledge/playbooks/ga4-audit.md → criar este (ainda nao existe, mas devia)

Quer que eu abra algum ou crie o novo playbook?
```

Esse modo eh particularmente util ao final de uma sessao tecnica — dispara junto com a sugestao de `/content` (skill content) se aplicavel.

### `/knowledge new <type> <title>`

Cria novo doc com frontmatter padronizado, no lugar certo.

Args:
- `$1` (subcommand): `new`
- `$2` (type): `idea | playbook | audit | learning | doc`
- `$3+` (title): titulo livre, sera kebab-case'd pro filename

Logica:
1. Determine target dir baseado no type:
   - `idea` → `~/Desktop/knowledge/ideas/`
   - `playbook` → `~/Desktop/knowledge/playbooks/`
   - `audit` → `~/Desktop/knowledge/audits/`
   - `learning` → `~/Desktop/knowledge/learnings/`
   - `doc` → repo atual (root) — pra docs project-specific
2. Kebab-case do title + date prefix pra audits: `YYYY-MM-DD-<title>.md`
3. Cria com frontmatter pre-preenchido:

```markdown
---
type: <type>
status: active
tags: []
created: 2026-05-17
last_review: 2026-05-17
priority: medium
related: []
---

# <Title>

[content goes here]
```

4. Abre no editor padrão (`code` ou `nvim` baseado em `$EDITOR`) ou apenas reporta o path criado

5. **Auto-commit (so quando criar em `~/Desktop/knowledge/`)**:

```bash
cd ~/Desktop/knowledge
git add <novo-arquivo>
git commit -m "Add <type>/<title>: created via /knowledge new"
git push
```

Falhas devem ser reportadas mas nao bloquear (ex: sem network, conflito merge). Se ocorrer, mostra:

```
WARN: auto-commit falhou ([erro]). Arquivo criado em <path>, mas nao versionado ainda.
Pra resolver manualmente: cd ~/Desktop/knowledge && git status
```

6. **Mensagem final pro usuario** (sempre, mesmo se commit deu certo):

```
Doc criado: <path>
Commitado e pushado pra origin/main (commit <sha>).

LEMBRE-SE: revisar e ajustar o conteudo. Frontmatter foi pre-preenchido com defaults — voce
provavelmente quer ajustar:
- tags: agora vazia, adiciona 2-3 tags
- related: vincular a outros docs se aplicavel
- priority: default eh medium

Depois de editar: cd ~/Desktop/knowledge && git add -A && git commit -m "..." && git push
```

**NAO auto-commitar** quando `type=doc` cria em repo do projeto atual (nao central) — esse fica na responsabilidade do usuario porque o repo do projeto tem seu proprio fluxo (ex: PRs, branches).

### `/knowledge migrate`

Helper raro: percorre `.md` files existentes (em `~/Desktop/knowledge/` ou repo), detecta ausencia de frontmatter, e oferece pra adicionar boilerplate.

NAO modifica arquivos sem confirmacao. Apresenta lista, espera "yes" pra cada um.

## Regras criticas

- **NAO modifica arquivos sem confirmacao explicita** — exceto quando o usuario invoca `/knowledge new`
- **NAO publica nada** — eh so descoberta, organizacao, sugestao
- **Respeita git** — se um doc esta versionado num repo, considera last commit como `last_review` se frontmatter ausente
- **Project-aware** — sempre detecta cwd e scaneia o projeto atual, nao so o central
- **Performance** — pra repos grandes (>200 .md), considera limit ou paginacao
- **Output compacto** — preferir tabelas/listas curtas a textao corrido

## Convencao de frontmatter (obrigatoria pra docs novos)

```yaml
---
type: idea | playbook | audit | learning | doc | draft
status: active | stale | archived
tags: []  # lower-case, kebab-case, max 5
created: YYYY-MM-DD
last_review: YYYY-MM-DD
priority: high | medium | low
related: []  # paths absolutos ou relativos pra outros .md
---
```

Quando o usuario criar doc via `/knowledge new`, frontmatter eh pre-preenchido. Quando ele criar manualmente (Write tool, $EDITOR), eu (Claude) devo sugerir adicionar frontmatter se faltar.

## Quando NAO usar essa skill

- Pra ler/editar UM doc especifico que ja foi mencionado → use Read/Edit direto
- Pra criar doc novo num lugar especifico fora da convencao → use Write
- Pra git/version control de docs → use `git` direto
- Pra busca lexical simples ("achar string X") → use `grep` direto

A skill eh pra organizar, descobrir, e dar lifecycle a uma colecao de docs — nao pra micro-edicoes.

## Integracao com `/content`

Se a skill `content` ja existe (ver `~/.claude/skills/content/SKILL.md`), `/knowledge suggest` deve considerar:
- Drafts em `content/drafts/` como output da skill `content`
- Sugerir "rodar /content" se trabalho recente bate como content-worthy AND nao tem rascunho ainda
