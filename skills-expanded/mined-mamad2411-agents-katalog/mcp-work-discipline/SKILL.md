---
name: mcp-work-discipline
description: |
  MANDATORY discipline + self-audit for behavior-preserving refactors and MCP
  work on idu-pi (cli.ts / mcp-server.ts breakups, tool-handler extraction,
  pure moves, renames, file splits). Written for MiniMax/Qwen/KM5 workers that
  use tools less reliably than GPT-class models. Triggers: "mover", "extraer",
  "split", "desmembrar", "pure move", "behavior-preserving", "refactor",
  "cluster", "wrapper", "delegation", "case extraction", "byte-identity",
  "mcp-server", "tool handler", "tool-list", "envelope", or ANY change that
  claims "no behavior change" / "cero cambio de lógica". Use it BEFORE writing
  the change AND BEFORE reporting it. Pairs with idu-pi-parent-protocol
  (.pi/skills/idu-pi-parent-protocol) for the idu-pi MCP tool surface and, if
  installed, mcp-builder (.agents/skills/mcp-builder) for MCP server DESIGN
  quality — this skill does NOT replace either; it is the discipline layer.
category: development
risk: safe
source: project
date_added: "2026-06-20"
---

# MCP Work — Refactor Discipline & Self-Audit

> **Audience**: the implementer model (MiniMax, Qwen, KM5, Claude) doing a
> behavior-preserving refactor or MCP-surface change on idu-pi.
> **Why this exists**: across the cli.ts breakup the auditor caught **7 real
> drifts** that green-looking reports would have shipped (PR 7f shipped dead
> wrappers without rewiring the switch; PR 7j/7k hid line-collapse drifts behind
> a weakened gate). Every one was a **discipline / honesty / fail-open-gate gap,
> not a knowledge gap**. This skill encodes what stops them.

---

## 0. The ONE check that would have prevented PR 7f

Before you report ANY refactor, run:

```bash
git diff --stat <base-sha> HEAD
```

**Every file you claim to have changed MUST appear in that output.** If you say
"I moved bodies out of `cli.ts` / `mcp-server.ts`" but that file is not in the
diff stat, you did **NOT** do the refactor — you only added dead code
elsewhere. **STOP and finish the wiring before saying one more word.**

> The cheapest lie to catch is a diff stat. Read it. Believe it over your memory.

---

## 1. The pure-move contract

A behavior-preserving move changes **location, nothing else**. The ONLY deltas
allowed in moved code are:

- the `export` keyword (a private symbol becomes exported), and
- type annotations that strict mode (`noImplicitAny`) requires after the scope
  change, and
- the `activeRuntime` → `runtime` parameter rename for handler wrappers, and
- a documented **import alias** when the wrapper name collides with an imported
  helper (`import { handleX as runX }`).

**Anything else is NOT a pure move.** Not a typo fix. Not reformatting. Not a
string change. Not collapsing a multi-line statement to one line. Not "while I
was there." If you spot a real bug or typo, write it DOWN and do it in a
**separate, labelled PR**.

**Never duplicate a shared helper.** If a case/tool body calls a helper that is
private to the source file (e.g. `recordCliUsage`, `envelope`, `pisoBannerLine`),
do NOT copy it into your handler file. **Extract it once to a shared module and
import it from both places.** Duplicating in a de-duplication refactor is
self-defeating (PR 7b and 7k both made this mistake).

---

## 2. Case/tool extraction = TWO edits, both mandatory

When you extract `case` bodies into wrapper functions, it is two edits:

1. **Create** the wrapper in the cluster's `handlers.ts` with the verbatim body.
2. **Rewire** the dispatch: replace the inline body with
   `return handleX(activeRuntime, rest);` **and delete the inline body.**

Doing only (1) leaves dead code; the switch still runs the old body. Prove it:

```bash
git diff --stat <base> HEAD -- src/<file>            # file MUST appear and shrink
git show HEAD:src/<file> | grep -E "return (await )?handleX\("   # 1+ per group
git show HEAD:src/<file> | grep -E "<inlineMethod>\("            # MUST be 0
```

---

## 3. The four gate lessons (do NOT regress these)

The verify gate exists because green tsc/test are necessary, not sufficient
(PR 7f passed all of them while being a no-op). Hard-won rules:

| Lesson | Rule |
|---|---|
| **fail-CLOSED** | A gate that can't run (undefined fn, parse error, missing file) must **ERROR + exit≠0**, never report OK. No silent `try/catch` around a check. (PR 7g) |
| **blocking, not WARN** | byte-identity stays `exit 1` on a real diff. Never downgrade a gate to WARN to make a PR pass. (PR 7j) |
| **teach, don't blind** | For a legitimate delta (alias, rename), make the check NORMALIZE it (resolve `import {X as Y}`, map `activeRuntime→runtime`) so it still reports IDENTICAL and stays blocking. Never weaken the gate. (PR 7j) |
| **check private too** | The duplication guard must include EVERY handler file in its list and flag functions defined in both the source and a handler file — **including non-exported privates**. (PR 7k) |

If you "fix" a red gate by making it quieter, you reintroduced the exact bug.

---

## 4. Honest reporting — say only what the command output shows

- Report **numbers you computed**, from a command you ran this run. Never
  template-fill diff stats — paste the actual `git diff --stat`.
- "live verified" / "bodies removed" / "byte-identical" are claims about
  **command output**. If you didn't see the output, don't write the claim.
- If a gate is red, or you skipped a step, **say so plainly**. A truthful "I
  haven't wired the switch yet" beats a green-looking false report.
- The auditor re-checks everything against real code. A fabricated report gets
  the work rejected and re-done — it does not get a merge.

---

## 5. mcp-server.ts specifics (different from cli.ts)

mcp-server.ts is ALSO a `switch(name)` over `idu_*` tool labels, so §1–§4 apply.
But it has extra surfaces the breakup MUST account for:

1. **THREE dispatch surfaces, not one.** Map all three in step-0:
   - the main `switch(name)` tool dispatch (the primary target),
   - **if-based tool routing** (`if (result.tool === ...)`, `if (name === "..." || ...)`) — tools handled OUTSIDE the switch; a naïve switch-only extraction ignores them,
   - the outer `switch(request.method)` (MCP protocol: tools/list, tools/call) — **do NOT decompose**; it is the thin protocol shell.
2. **`envelope()` is the universal contract.** Every tool response is
   `envelope({..., blocking, ...})` — what every orchestrator consumes. It is a
   shared helper (like `recordCliUsage`): import it, **never duplicate it**, and
   keep its shape byte-identical. A drift here silently breaks every orchestrator.
3. **Freeze tools + SCHEMAS, not just names.** The catalog-freeze analog is the
   full set of registered tool names AND their input schemas. A schema drift
   breaks orchestrators silently. `test/mcp-tool-catalog.test.ts` must pin both.
4. **Runtime-sensitive.** mcp-server is the long-running server. After each merge
   the human must run `/reloader` for the live server to use the rebuilt code,
   before anyone claims it is live. (CLI runs fresh per invocation; the server
   does not.)

For MCP server **design quality** (schemas, descriptions, error handling,
protocol conformance) — a separate concern from this behavior-preserving
breakup — read `.agents/skills/mcp-builder/reference/` (if installed). For the
idu-pi tool surface and when to consult the supervisor, follow
`.pi/skills/idu-pi-parent-protocol`.

---

## Pre-flight checklist (run top to bottom before reporting)

- [ ] `git diff --stat <base> HEAD` — every file I claim I changed is listed and shrank.
- [ ] Each new wrapper is CALLED from the dispatch (`grep return handleX(`).
- [ ] The old inline bodies are GONE (`grep <inlineMethod>(` = 0).
- [ ] No helper duplicated — shared helpers (recordCliUsage, envelope, …) extracted + imported once.
- [ ] For mcp-server: all three dispatch surfaces handled; tool-list + schema freeze green; envelope() untouched.
- [ ] Gates run with REAL output pasted; byte-identity is BLOCKING (exit 1 on real diff); no WARN downgrade; no silent try/catch.
- [ ] Every claim in my report maps to command output I saw this run.
- [ ] Any non-move change (typo, format, fix) moved to a separate PR, not smuggled in.
- [ ] If runtime-sensitive (mcp-server / cron): noted that merge + `/reloader` is required before "live".

If any box is unchecked, the change is not done. Do not report it as done.
