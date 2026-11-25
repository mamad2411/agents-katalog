# Shared Skills

Esta biblioteca cobre as skills compartilhadas do ecossistema.

## Ecosystem Centrality

Trate `ControleOnline/agents-mcp` como a fonte primaria para agents, runners, ownership, handoffs e regras estruturais do fluxo.

## Escopo operacional permitido

**Único escopo permitido para mutações:** org [`ControleOnline`](https://github.com/ControleOnline/). Proibido comentar, alterar, rotular ou solicitar fora de `ControleOnline/*`. Fora = `OUT_OF_SCOPE`.

## Task-First Policy

Toda solicitacao precisa estar vinculada a pelo menos uma task ou issue valida no GitHub. Use a skill de backlog do CTO quando faltar task.

## Skill Layering Policy

- comum → `agents/skills/controleonline/shared-*/SKILL.md`
- por agent → `agents/skills/controleonline/by-role-*/SKILL.md`
- runtime → `agents/skills/controleonline/runners-README/SKILL.md`
- `agents/roles/*/agent.md` enxuto; wrappers finos em `.github/agents/`

## Priority Projects Policy

Somente org `ControleOnline`:

- `ControleOnline/agents-mcp`
- `ControleOnline/app-community`
- `ControleOnline/api-community`
- `ControleOnline/ui-common`
- `ControleOnline/ui-tests`

## Agent Delegation Policy

Delegue quando a trilha for de `Developer`, `Security`, `QA`, `DevOps` ou `Sysadmin`. Intervenha no `agents-mcp` quando a falha for estrutural.


## Paperclip Direct Execution (obrigatoria)

Todo agent **deve estender** `operations/paperclip-direct-execution.md`.

- Paperclip Coding Agent, workers, runners e GitHub Actions sao superficies de cooperacao
- Wrappers `.github/agents/*.agent.md` usam `target: github-paperclip`
- Sync: `workers/scripts/sync-paperclip-agents.mjs`

## Shared Operational Skills (por categoria)

### github/
- `github/github-flow.md`
- `github/conflict-resolution.md`
- `github/github-issue-handling.md`
- `github/operational-github-workflow.md`
- `github/master-publication.md`

### documentation/
- `documentation/documentation-governance.md`

### security/
- `security/security-guardrails.md`
- `security/operational-security-guardrails.md`

### quality/
- `quality/code-quality.md`
- `quality/task-completion-criteria.md`

### operations/
- `operations/agent-execution-baseline.md`
- `operations/agent-wrapper-contract.md`
- `operations/agent-handoff-governance.md`
- `operations/autonomous-operations.md`
- `operations/operational-source-of-truth.md`
- `operations/log-investigation-evidence.md`
- `operations/email-reading-fallback.md`
- `operations/paperclip-direct-execution.md — cooperacao obrigatoria com Paperclip/workers/runners/Actions
- `operations/issue-queue-discovery.md`

## GitHub Flow (branches e entrega)

A skill `github-flow.md` e a fonte canonica de:

- branch `task-{id_issue}` derivada de `master`
- entrega do Developer em **`dev`** por **merge** (sem PR)
- proibicao de PR para `Developer`, `QA` e `Security` no fluxo normal
- `staging` = tasks individuais promovidas pelo `DevOps` (sem pacote agregado)
- apos `Deploy`: `DevOps` mescla somente a branch da task → `master`; com quarteto → `Done`, sem quarteto → `Working` para segunda validacao

Todo agent que toque em branch, integracao ou promocao deve seguir essa skill.

## Issue Flow Governance (resumo)

- `Developer` entrega em **`dev`**, sem PR
- `QA` / `Security` decidem por labels; evidencia = merge em **`dev`**
- recusa: Developer corrige e re-mergeia em **`dev`**
- `DevOps` promove cada task individual para **`staging`**, `In Review` → `Deploy` → `master`; com quarteto → `Done`, sem quarteto → `Working` para segunda validacao
- nenhum agent fecha task no lugar do rito humano/board quando aplicavel
