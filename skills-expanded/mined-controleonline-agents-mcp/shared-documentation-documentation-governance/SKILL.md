# Documentation Governance

## Overview

Governanca da documentacao tecnica e de tutorial no ecossistema ControleOnline.

## Trilhas

- `agent:tutorial-assistant` — ajuda pratica para cliente final (MediaWiki / Central de Ajuda)
- `agent:technical-documenter` — wiki tecnica/negocio por projeto (GitHub Wiki + `docs/technical/`)

## Fila compartilhada (sem ProjectV2)

Ambas as trilhas usam `agents/skills/controleonline/shared-operations-issue-queue-discovery/SKILL.md`:

- sem ProjectV2;
- uma issue por execucao;
- org inteira se o prompt nao restringir;
- labels `agent:<papel>` (qualquer status) e `agent:<papel>:done`.

## Technical Documenter

O `technical-documenter` **cria e atualiza** a wiki tecnica dos repositorios afetados pela tarefa.

- **Nao aprova** e **nao recusa** tarefas.
- Labels: `agent:technical-documenter` / `agent:technical-documenter:done`.
- Issues `closed` sem `:done` tambem sao elegiveis.
- Multi-repo: documentar todos os afetados; links cruzados preferiveis.
- Navegacao humana: Home da wiki por categoria + `AGENTS.md` como ponte.

## Tutorial Assistant

O `tutorial-assistant` **cria e atualiza** documentacao **publica** para cliente final.

- **Nao aprova** e **nao recusa** tarefas.
- Labels: `agent:tutorial-assistant` / `agent:tutorial-assistant:done`.
- Destino: MediaWiki `https://ajuda.controleonline.com/` via **API** (`api.php`).
- Credenciais de runtime: referencia no Google Drive (`wiki.json` com `host`, `user`, `password`) — nunca versionar no Git.
- Nao versionar paginas `.wiki` nem imagens publicas no Git.
- E-mail `todos@controleonline.com` so apos publicacao validada, com links publicos.

As labels `tutorial-assistant:accepted` / `tutorial-assistant:rejected` **nao** fazem parte deste fluxo.

## Seguranca

Toda publicacao documental deve obedecer `agents/skills/controleonline/shared-security-security-guardrails/SKILL.md`.

## Fonte completa

Detalhes operacionais por papel ficam em `agents/skills/controleonline/by-role-<role>-README/SKILL.md` e nos `agents/roles/*/agent.md` correspondentes.

## Handoff apos dual-gate / publish (anti-furo)

Para **nao furar** a documentacao no caminho ate `Done`/`master`:

1. **DevOps** (publish `staging`→`master`): ao mover filhas de produto para `Done`, se ainda nao houver `:done` documental, **aplica** `agent:technical-documenter` e/ou `agent:tutorial-assistant` (solicitacao). Nunca inventa `:done`. Ver `master-publication.md`.
2. **Manager** (P6 higiene): `Done`/`closed` sem quarteto → aplica labels de solicitacao documental ausentes (ou reabre se faltar dual-gate). So fecha com quarteto completo + evidencia. Ver `agents/roles/manager/agent.md` e checklist do README do Manager.
3. Documentadores processam a fila por `agent:<papel>` (ou `closed` sem `:done`) conforme `issue-queue-discovery.md`.
