---
name: descomponer-multirepo
description: Analiza un requerimiento sobre un ecosistema multirepo (carpeta padre con varios repos hijos documentados) y lo descompone en specs acotados por repo más los contratos de comunicación entre ellos. Use when the user describes a feature or requirement that spans a multirepo ecosystem and needs to know which repos are affected and what to build in each.
type: skill
tags: [multirepo, arquitectura, sdd]
---

# Multirepo Requirement Decomposer

## Goal

Take a natural-language requirement against a multirepo ecosystem (a parent folder with several
sibling repos, each documented with its own CLAUDE.md, plus a parent CLAUDE.md describing the
overall architecture) and decompose it into: which repos it touches and why, an explicit
cross-repo contract for any shared interaction, and a scoped spec per affected repo.

This skill does not run SDD itself and does not write code — it produces the map that each repo's
own SDD cycle (`sdd-new`/`sdd-propose`) will consume separately, one repo at a time.

## Required Input

- The parent CLAUDE.md — required. Without it there's no map of what each repo owns.
- Each affected child repo's CLAUDE.md — required for that repo. If a repo has no CLAUDE.md, fall
  back to its README.md.
- A requirement in natural language from the user — required. If it's vague about scope (which
  repo(s), what changes), ask once before proceeding — do not guess silently.

## Workflow

1. Read the parent CLAUDE.md fully — the architecture, the repo table, and any contract
   conventions already established (e.g., where contracts/specs are expected to live if the
   ecosystem already has one).
2. Read every child repo's CLAUDE.md (or README.md fallback) to build a map of what each repo
   owns and exposes.
3. Given the requirement, decide which repos it touches and explain the reasoning to the user —
   never assume in silence. If scope is ambiguous, ask before writing anything.
4. For every cross-repo interaction implied by the requirement (a new/changed endpoint, an event,
   a shared data shape), write a contract file at `<parent>/contracts/<requirement-slug>.md` using
   the Contract Format below. Skip this step if the requirement is fully contained in one repo — a
   single-repo requirement gets no contract file, only its spec.
5. For each touched repo, write a spec file scoped ONLY to that repo's part at
   `<parent>/specs/<requirement-slug>/<repo-name>.md`, using the Spec Format below.
6. If one repo's work depends on another's (e.g., the API must define the contract before the
   frontend can consume it), state that order explicitly in the summary — never imply parallel
   work when there's a real dependency.
7. Present the summary (Output Format below) to the user. Do not run `sdd-new` or any SDD phase —
   that happens separately, per repo, afterward.

## Contract Format (`contracts/<requirement-slug>.md`)

```markdown
# Contrato: {Nombre del requerimiento}

## Repos involucrados
- {repo-a} — {qué expone/provee}
- {repo-b} — {qué consume}

## Interacción
{Descripción del endpoint/evento/dato compartido: forma, dirección, quién es dueño}

## Notas
{Cualquier detalle que ambos lados necesiten conocer y que no vive en ningún repo individual}
```

## Spec Format (`specs/<requirement-slug>/<repo-name>.md`)

```markdown
# Spec: {Nombre del requerimiento} — {repo-name}

## Qué hay que construir en este repo
{Descripción acotada SOLO a la parte de este repo}

## Contrato relacionado
{Link a contracts/<requirement-slug>.md si existe, o "N/A" si el requerimiento no cruza repos}

## Listo para
`sdd-new` / `sdd-propose` en este repo, usando esta spec como input.
```

## Output Format (resumen final)

```markdown
# Requerimiento: {Nombre}

| Repo | Toca | Depende de | Spec |
|---|---|---|---|
| {repo-a} | Sí — {por qué} | — | specs/{slug}/{repo-a}.md |
| {repo-b} | Sí — {por qué} | {repo-a} | specs/{slug}/{repo-b}.md |

Contrato: contracts/{slug}.md (o "N/A" si no cruza repos)

## Orden sugerido
1. {repo-a} — define el contrato primero
2. {repo-b} — consume el contrato ya definido
```

## Quality Gate

Before returning, silently check:

- Every touched repo is traceable to something explicit in the requirement or in a repo's
  CLAUDE.md — nothing invented.
- A repo is never marked "touched" without a stated reason.
- If two or more repos share an interaction, a contract file exists — no repo spec silently
  assumes a shared contract that isn't written down anywhere.
- Dependency order is explicit whenever one repo's spec references something another repo must
  define first.
