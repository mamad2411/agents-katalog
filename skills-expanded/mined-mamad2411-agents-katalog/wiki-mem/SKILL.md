---
name: wiki-mem
description: >
  Knowledge / librarian MegaBrain: memória episódica de sessões Cursor (.ai/sessions,
  LATEST.md) e promoção controlada (promote-queue → log.md ± wiki/). Use quando
  /mem, Knowledge Agent, librarian, continuidade entre chats, mem search, promote
  para canónico, ou estilo claude-mem. Não use para grounding/contratos canónicos
  (wiki Context Engineer + RAG), pesquisa web externa (/pesquisar),
  nem como substituto do HARD-GATE MegaBrain. Não duplica knowledge.search
  (DeterministicProvider).
metadata:
  version: 1.0.0
  status: experimental
  capability: knowledge-promote
  type: worker
  command: mem
  pda_roles: [librarian]
  specialization: Knowledge
disable-model-invocation: true
---

# Wiki Mem — Knowledge (episódico + promote)

**Specialization:** Knowledge (Lead matrix Wave C1).  
**Papel:** continuidade de sessão + promoção librarian para conhecimento canónico.  
**Não é** SSOT de domínio — canónico = vault `wiki/` + RAG via **wiki**.

**Template comportamental:** orchestration-support (librarian); não research externo.

**Decisão Wave C1:** `EXTEND_EXISTING_AGENT` — **não** criar package thin `knowledge`  
(grounding interno = wiki; search = `knowledge.*` deterministic; promote = este).

**Researcher ≠ Knowledge:** `/pesquisar` (`researcher`) = fontes externas; este package = store interno + promote.

---

## DO

- Recuperar continuidade: `mem.py search` + ler `LATEST.md`
- Gerir / refrescar consciência de `promote-queue.md` (hook enfileira; Agent promove)
- Como **librarian**: promover itens da fila → `{Projeto}/log.md` (± páginas `wiki/` se contratos)
- Recusar escrita em `raw/`
- Deixar claro quando o pedido exige **wiki** (contratos/arquitectura canónicos)
- Declarar se episódico está vazio / path em falta (sem inventar histórico)

## DO NOT

- Criar package novo `knowledge` com o mesmo DO
- Substituir HARD-GATE / Context Engineer (`wiki` / `/wiki`)
- Tratar `LATEST.md` como contrato de arquitectura
- Pesquisa web / papers / docs externas (`/pesquisar` — Researcher)
- Reimplementar `knowledge.search` / `knowledge.inspect` (já no orchestrator)
- Implementar features de produto
- Escrever `raw/` ou dump cego da wiki canónica
- Auto-conceder autoridade Policy Engine

---

## Fronteiras

| Skill / papel | Responsabilidade | Handoff |
|---------------|------------------|---------|
| **wiki-mem** (Knowledge) | Episódico + promote librarian | → canónico via log/wiki |
| **wiki** (Context Engineer) | Grounding / context pack RAG | HARD-GATE Fase 0 |
| Deterministic `knowledge.*` | Bridge BM25/hybrid | infra |
| Researcher (`/pesquisar`) | Externo | ≠ promote interno |

Ver também: [wiki/references/boundaries.md](../wiki/references/boundaries.md).

---

## Capability scope

| Classe | Capabilities |
|--------|----------------|
| **required** | `knowledge-promote` (esta skill) |
| **optional** | leitura fs de `.ai/sessions/` |
| **forbidden** | `context-grounding` como substituto; `knowledge.search` ownership; research web; coding produto |

---

## Paths

| Recurso | Path |
|---------|------|
| Vault (SSOT alinhado wiki) | `$WIKI_ROOT` (alias `$RAG_REPO_ROOT`) — required |
| Store | `$RAG_REPO_ROOT/.ai/sessions/` |
| Digest | `…/LATEST.md` |
| Fila promoção | `…/promote-queue.md` |
| CLI | `python3 ~/.cursor/hooks/wiki-mem/mem.py` |

Legado `Documentos/karpathyWiki` (sem `gitHub`): só se existir no host; preferir path SSOT acima.

## Comandos

```bash
python3 ~/.cursor/hooks/wiki-mem/mem.py search "filtro projeto BM25"
python3 ~/.cursor/hooks/wiki-mem/mem.py promote   # prepara/fila — não escreve wiki/ sozinho
python3 ~/.cursor/hooks/wiki-mem/mem.py digest
```

## Ritual

1. Pedido de continuidade → `search` + ler `LATEST.md`
2. Contratos/arquitectura → skill **wiki** / RAG (HARD-GATE MegaBrain)
3. Após trabalho estável → `promote` **ou** o hook de fecho já enfileirou → **librarian** (este papel) append em `{Projeto}/log.md` (± `wiki/` se contratos)
4. Output estruturado (abaixo)

## Output

```markdown
## Knowledge / Mem
- **modo:** search|digest|promote|clarificar
- **confiança:** … | n/a

### Episódico
- LATEST: sim/não (resumo 1–3 linhas)
- hits search: …

### Promote
- fila: itens … | vazia
- acção: enfileirado | promovido para `{Projeto}/log.md` | bloqueado
- raw/: nunca

### Handoff
- próximo: continuidade | /wiki grounding | librarian done | clarificar
```

## Failure / degradation

| Falha | Classe | Acção |
|-------|--------|-------|
| Sessions path em falta | `knowledge_failure` | declarar; não inventar histórico |
| Pedido = grounding canónico | `out_of_scope` | redireccionar `/wiki` |
| Pedido = research web | `out_of_scope` | recusar; `/pesquisar` (`researcher`) |
| Promote sem projecto | `context_failure` | clarificar projecto |
| Tentativa write `raw/` | `policy_denial` | recusar |

## Hooks (automáticos)

`sessionStart` · `afterFileEdit` · `stop` · `sessionEnd` em `~/.cursor/hooks.json`.

**Fecho (`stop` / `sessionEnd`):** se houver `promote_candidates` ou file_edits de código, **append/refresh** `promote-queue.md`. **Nunca** escreve `{Projeto}/wiki/` nem `raw/`. `followup_message` vazio (sem loops MegaBrain). Promoção canónica = librarian / Agent (este skill).

Se `sessionStart.additional_context` falhar (bug Cursor conhecido), o Agent **deve** ler `LATEST.md` quando precisar de continuidade.
