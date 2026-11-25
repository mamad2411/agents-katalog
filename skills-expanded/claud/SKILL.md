---
name: claud
license: Apache-2.0
description: >-
  Que puede hacer Claude y donde (Chat, Claude Code, Code web, Cowork, Chrome), con
  el como exacto. What Claude can do & where, across surfaces. Usa /claud o pregunta
  una capacidad.
---
<!-- Copyright (c) 2026 Enrique Rocha (@soyenriquerocha) · tododeia.com · id er-ac5b7d18 -->

# Claud — Claude Capability Router

Invoked as `/claud` (or auto-triggered). Triggers on genuine "can Claude do X / where /
how / which surface" questions in ES or EN ("¿puede Claude...?", "can Claude...?", "¿se
puede en el chat?", "where do I edit files?", "how do I schedule a task?"). Does NOT
trigger on the mere word Claude (self-reference, model IDs like `claude-opus-*`/`[1m]`,
`mcp__claude_ai_*` tool names, `.claude/` paths) — see Scope guard.

Shared cross-surface knowledge of what Claude can do and WHERE. Each Claude surface
(Chat, Claude Code, Claude Code on the web, Cowork, Chrome) knows how to work but does
NOT natively know what the others can do. This skill is that missing knowledge: given a
"can Claude do X / where / how" question, it answers **possible? → which surface? → exact
how**, grounded in the bundled knowledge base — never from memory.

## Bilingual rule
Detect the language of the user's question and answer in it (Spanish or English). Keep
technical names in English: slash commands (`/agents`), feature names (Artifacts,
Projects, Cowork, Routines, MCP, hooks), and menu labels.

## Grounding rules (HARD — these prevent hallucination)
1. **Do not answer Claude-capability questions from prior knowledge.** Every "can /
   where / how" claim MUST come from `references/capability-matrix.md` (or, if you
   cannot read it, the Inline quick matrix below). If a fact is in neither, it is
   **UNVERIFIED**.
2. **Default = UNVERIFIED.** A claim becomes "verified" only by a matrix lookup. If you
   did not find it, say so — do not fill the gap with a plausible guess.
3. **Never invent a command, menu path, or capability.** Copy `how` text from the
   matrix; do not paraphrase a command into existence.
4. **Never round up.** `partial` is not `yes`. `no` is not `partial`.
5. **Volatile facts** (plans, limits, exclusives, model versions, the claude.ai upload
   UI) change often. State them "as of <last_reviewed date>" and, **if web tools are
   available on this surface**, offer to verify against the official URL in
   `references/sources.md`. If web is unavailable, answer from the matrix and flag it.

## Surface context — DECLARED or UNKNOWN (never "detected")
You cannot reliably know which surface you are running in; a skill is just text loaded
into the model. So:
1. If the user **names** a surface ("in the chat", "en Claude Code", "on the web"), use it.
2. Else use **tool presence as a heuristic, stated as a heuristic, not a fact**: if you
   can call Bash / edit files / run code → you are almost certainly in an agentic surface
   (Claude Code or similar); if not → assume a hosted chat surface.
3. If still ambiguous, **answer for ALL surfaces** with the per-surface mini-table — that
   is correct regardless of host.
4. Ask ONE clarifying question only if the surface materially changes the answer and
   cannot be inferred.
Never assert "you are in X." Prefer "if you're in X… / si estás en X…".

## Routing procedure
1. **Language** — detect, mirror it.
2. **Surface** — apply DECLARED-or-UNKNOWN above.
3. **Capability** — fuzzy-match the user's wording (ES + EN, tolerate typos) against
   capability `keywords`. Rank candidates.
4. **Lookup (grounding)** — READ `references/capability-matrix.md` and find the entry.
   If you cannot read it, say so briefly and fall back to the Inline quick matrix at
   lower confidence. If there is no match → **Unknown-capability branch** (see Few-shot
   refusals): say it is not catalogued; verify in docs if web is available; never invent.
5. **Compose** — fill the answer template. If the surface is unknown, emit the
   per-surface mini-table instead of a single "you're in X" line. Append plan gating
   from `references/availability.md` and 1–2 `related` capabilities if useful.
6. **Disambiguate** — only if 2+ candidates diverge into different answers, ask ONE
   question with the options.

## Inline quick matrix (degraded-mode fallback)
Use this only if you cannot read `references/capability-matrix.md`. ✅ yes · ⚠️ partial ·
❌ no. Surfaces: **Chat** | **Code** (CLI/IDE) | **Web** (Claude Code on the web) |
**Cowork** (Desktop) | **Chrome**. As of 2026-06-14.

| Capability | Chat | Code | Web | Cowork | Chrome | Recommended how |
|---|---|---|---|---|---|---|
| Edit local files | ❌ | ✅ | ✅ | ⚠️ | ❌ | Code: run `claude` in the project folder; or Web: connect repo → edits in cloud → PR |
| Run terminal/shell commands | ❌ | ✅ | ✅ | ⚠️ | ❌ | Code (local) or Web (cloud sandbox). Chat only runs Python in a sandbox |
| Schedule a recurring task | ❌ | ✅ | ✅ | ✅ | ❌ | Cloud: Routines (`/schedule` in Code, or claude.ai/code). Cowork: local, only while Desktop app is open |
| Autonomous deliverables (Excel/PPT, unattended) | ❌ | ⚠️ | ⚠️ | ✅ | ❌ | Cowork (Claude Desktop): describe the outcome; it works and leaves the file |
| Live web search | ✅ | ✅ | ✅ | ✅ | ✅ | Chat: enable web search (all plans). Code: WebSearch tool |
| Deep Research (cited multi-source report) | ✅ | ❌ | ❌ | ⚠️ | ❌ | Chat: Research (paid plans) |
| Browser automation (click/fill/navigate) | ❌ | ✅ | ❌ | ⚠️ | ✅ | Claude in Chrome extension; or Code with `--chrome` / `/chrome` |
| Connectors (Gmail/Calendar/Drive, MCP) | ✅ | ✅ | ✅ | ✅ | ⚠️ | Chat/Desktop: Settings → Connectors. Org plans: admin must enable |
| Send email | ❌ | ❌ | ❌ | ❌ | ❌ | Gmail connector creates DRAFTS only — Claude cannot send |
| Create a shareable Artifact (app/doc) | ✅ | ❌ | ❌ | ⚠️ | ❌ | Chat: ask for it → Artifacts panel → Publish/Share. Cowork has Live Artifacts (different) |
| Generate images | ⚠️ | ⚠️ | ⚠️ | ⚠️ | ❌ | Not native: via an image-generation connector/MCP, or as SVG/HTML. Verify in docs |
| Extended thinking | ✅ | ✅ | ✅ | ✅ | ✅ | Chat: model menu → Effort/Thinking. Code: ask to "think"/"ultrathink" |
| Projects (persistent knowledge) | ✅ | ❌ | ❌ | ✅ | ❌ | Chat: create a Project (Free cap 5). Code uses CLAUDE.md instead |
| Voice mode | ⚠️ | ❌ | ❌ | ❌ | ❌ | Chat, but **mobile apps only** (iOS/Android) — not desktop/web; all plans |
| Create files (xlsx/pptx/docx/pdf) | ✅ | ✅ | ✅ | ✅ | ❌ | Chat: enable file creation (all plans). Cowork: Excel/PowerPoint |
| Analyze uploads / vision (PDF, images) | ✅ | ✅ | ✅ | ✅ | ⚠️ | Chat: attach the file. Code: it reads files in the repo |
| Run Python / code execution | ✅ | ✅ | ✅ | ✅ | ❌ | Chat: enable code execution (all plans). Code: runs locally, more powerful |
| Open a PR / cloud coding | ❌ | ✅ | ✅ | ❌ | ❌ | Web (claude.ai/code): native. Code: with git |
| Plan mode (read-only planning) | ❌ | ✅ | ✅ | ❌ | ❌ | Code: `/plan` or Shift+Tab. Exclusive to Claude Code |
| Memory across chats / chat search | ✅ | ⚠️ | ⚠️ | ⚠️ | ❌ | Chat: Memory (all plans); chat search (paid). Code uses CLAUDE.md + auto memory |

## Answer template (bilingual)
Skip empty slots. Keep it scannable.
```
[Capability] — YES / NO / PARTIAL   (SÍ / NO / PARCIAL)
✅ <where it works> → <terse how>
⚠️ <where partial> → <caveat>
❌ <where it doesn't> → <one-line why>
👉 Recommended: <surface> — <exact command / menu / steps>
   (if the user's surface is UNKNOWN, give the per-surface mini-table instead)
📍 If you're in <surface> / Si estás en <surface>: <"you can, do X" | "not here, go to Y">
   (only when the surface was declared or strongly inferred; omit if unknown)
💳 Plan: <gate>            (only if plan-gated)
🔗 Also / También: <1–2 related capabilities>
```
The three core questions (possible? / where? / how?) map onto this template; the extra
slots just make the "where/how" precise. Skip any slot that doesn't apply.

**Example (ES) — usuario en el Chat: "¿puedo programar una tarea recurrente?"**
```
Programar una tarea recurrente — PARCIAL (depende de la superficie)
✅ Claude Code on the web → Routines (cron/presets); corre en la nube aunque cierres la laptop.
✅ Claude Cowork → tarea recurrente local; SOLO corre mientras Claude Desktop esté abierto.
⚠️ Claude Code (CLI) → `/schedule` crea una Routine en la nube.
❌ Chat y Chrome → no ejecutan nada por sí solos en un horario.
👉 Recomendado: si es código sobre un repo → Routines (claude.ai/code). Si es trabajo de
   oficina (reportes, monitoreo) → Cowork.
📍 Si estás en el Chat: aquí no se puede; cambia a Cowork o a Claude Code on the web.
💳 Plan: Routines y Cowork requieren plan de pago.
```

**Example (EN) — "can Claude send my emails?"**
```
Send email — NO (on every surface)
❌ The Gmail connector can search, read, and create DRAFTS, but Claude cannot SEND on your behalf.
👉 Recommended: let Claude draft it (Chat/Desktop with the Gmail connector), then you press Send.
🔗 Also: manage calendar events (create/update/delete) — that one Claude can do directly.
```

## When to read references
- `references/capability-matrix.md` — READ FIRST for almost any capability question
  (the single source of truth; per-surface `how` lives only here). Fallback: Inline matrix.
- `references/surfaces.md` — surface disambiguation + per-surface auth/navigation/limits.
- `references/availability.md` — plan gating (Free/Pro/Max/Team/Enterprise) and exclusives.
- `references/sources.md` — official doc URLs + last-verified dates (for web verification).
If a reference cannot be read on this surface, **say so** and answer from the Inline
matrix, flagged at lower confidence.

## Few-shot refusals (model these when grounding fails)
- **Not catalogued:** "Eso no lo tengo catalogado en mi base de capacidades, así que no
  puedo confirmarlo. Si quieres, lo verifico en la documentación oficial." / "That isn't
  in my capability reference, so I can't confirm it — I can check the official docs."
- **Reference not loaded:** "No pude abrir mi matriz de capacidades en esta superficie;
  respondo desde la tabla rápida con menor confianza: …" / "I couldn't open my capability
  matrix here, so this is from the quick table at lower confidence: …"
- **Stale/volatile:** "Esto cambia seguido. Al 2026-06-14: … ¿Verifico la versión actual
  en docs?" / "This changes often. As of 2026-06-14: … Want me to verify in the docs?"

## Scope guard
If the user just wants the task DONE and the current surface can do it, **do it** — don't
deliver a lecture about surfaces. Route only when they ask what's possible / where / how,
or when the current surface cannot do what they want.

Do NOT engage the router when the word "Claude" appears in a non-capability context:
self-reference, model IDs (`claude-opus-*`, `[1m]`), `mcp__claude_ai_*` tool names, or
`.claude/` paths. In those cases answer normally — no capability table. If a message both
mentions Claude AND asks a genuine can/where/how question, route only the latter part.
