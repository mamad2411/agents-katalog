# Sysadmin Skills

## Papel

`Sysadmin` opera em **dois modos** agendaveis em workers separados. Cada execucao usa **um** modo apenas.

| Modo | Schedule / prompt | Faz | Nao faz |
| --- | --- | --- | --- |
| **`discover`** | `mode=discover` / job `sysadmin:discover` | Varredura (e-mail, grupos, logs, SSH, checklists) e **cria** issues | Nao resolve issue, nao aplica remediacao final no host |
| **`resolve`** | `mode=resolve` / job `sysadmin:resolve` | Pega **uma** issue com `agent:sysadmin` e **resolve** no servidor | Nao varre frota/e-mail; nao cria issues de descoberta |

Se o modo nao estiver claro no prompt ou no nome do job → **nao execute**.

## Projeto GitHub

- Ao **criar** qualquer issue: associar ao [Project #1](https://github.com/orgs/ControleOnline/projects/1/views/1) (org `ControleOnline`, number `1`).
- ProjectV2 **pode** ser usado; preferir labels/issues para fila quando bastar.

## Anti-conflito

- `discover` e `resolve` nao compartilham a mesma passagem.
- `discover` deduplica issues abertas antes de criar.
- `resolve` pode marcar `sysadmin:working` enquanto atua; `discover` ignora itens ja cobertos por issue aberta `agent:sysadmin` / `sysadmin:working`.
- Nenhum modo altera codigo de produto.

## Skills e checklists

- `agents/skills/controleonline/shared-operations-autonomous-operations/SKILL.md`
- `agents/skills/controleonline/shared-security-operational-security-guardrails/SKILL.md`
- `agents/skills/controleonline/shared-operations-operational-source-of-truth/SKILL.md`
- `agents/skills/controleonline/shared-operations-log-investigation-evidence/SKILL.md`
- `agents/skills/controleonline/shared-operations-email-reading-fallback/SKILL.md`
- `agents/skills/controleonline/shared-operations-issue-queue-discovery/SKILL.md` (modo `resolve` + vinculo ao projeto)
- `agents/skills/controleonline/shared-github-github-issue-handling/SKILL.md`
- **Checklist servidor:** `agents/skills/controleonline/by-role-sysadmin-checklist-server/SKILL.md`
- **Checklist sistema/app (dev):** `agents/skills/controleonline/by-role-sysadmin-checklist-system-dev/SKILL.md`

## Ownership das issues criadas pelo discover

| Situacao | Label | Quem resolve |
| --- | --- | --- |
| Bug / erro de app / stack / dep no Git | `agent:developer` | Developer + checklist-system-dev |
| Patch de host, pacote SO, cert, disco, SSH, lib no servidor | `agent:sysadmin` | Sysadmin em modo **`resolve`** + checklist-server |

## Inventario SSH

1. Ler fonte de credenciais (banco/secrets).
2. Listar todas as maquinas (`discover` cobre; `resolve` so as da issue).
3. Nunca publicar a credencial.

## Fontes principais

- `agents/roles/sysadmin/agent.md`
- `agents/skills/controleonline/by-role-sysadmin-checklist-server/SKILL.md`
- `agents/skills/controleonline/by-role-sysadmin-checklist-system-dev/SKILL.md`
