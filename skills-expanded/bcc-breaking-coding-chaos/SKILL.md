---
name: bcc-breaking-coding-chaos
description: >
  BCC main skill: dual-loop coding workflow (throughline → plan-spar → clean-cut)
  or quick status+next. Slash: /bcc-breaking-coding-chaos · chat: bcc:breaking-coding-chaos ·
  "run BCC" · "BCC status" · "what next BCC". Needs a real idea (1:1 implement).
  Args: goal text, or status. May pass plan-spar review budget as rounds=N when chaining.
argument-hint: "slash: /bcc-breaking-coding-chaos · chat: bcc:breaking-coding-chaos · [goal|status] [rounds=N]"
metadata:
  short-description: "BCC main workflow"
---

# bcc-breaking-coding-chaos

**One main skill + three sub-skills.** This file is the only “big” entry; the three children own deep rules.

| Sub-skill | Role |
|-----------|------|
| [bcc-throughline](../bcc-throughline/SKILL.md) | Global map: `plans.md` / `progress.md` / `findings.md` only |
| [bcc-plan-spar](../bcc-plan-spar/SKILL.md) | After throughline: single `PLAN.md` align + review |
| [bcc-clean-cut](../bcc-clean-cut/SKILL.md) | After human APPROVE: minimal code + verify + writeback |

Internal notes (not separate slash skills): [references/SESSION.md](./references/SESSION.md), [references/WRITEBACK.md](./references/WRITEBACK.md).

**Prerequisite:** a **reasonably concrete idea**. BCC is **1:1 implement + control**, not ideation from zero.

---

## Shared voice (Mode A and Mode B)

Talk like a sharp collaborator on **their work** — not a workflow product or ceremony host.

| Do | Don't |
|----|--------|
| Lead with goal / map / next choice | “先对齐上下文 / BCC 双环说明 / 恢复账本” on cold start |
| Short human gates (confirm hardpoint, APPROVE implement) | Unprompted “还没写代码 / throughline 不写产品代码” lectures |
| Load each child skill and follow **its** voice rules | Dump file-role tables, 5-question grids, skill architecture |
| Keep process quiet; enforce order silently | Sell the next skill every turn |

Mode A only **chains** the same comfortable steps Mode B uses one-by-one — same tone, same gates, less user typing.

---

## Two modes (this skill)

### Mode A — full chain

When user says run BCC / full flow / implement this idea end-to-end:

```text
1. bcc-throughline   (create/update map — required first; cold start = start the map, not “resume”)
2. confirm next hardpoint with user (one short question + recommended default)
3. bcc-plan-spar     (grill until clear enough; review budget = rounds if user set it, else plan-spar default)
4. human APPROVE → write .bcc/session.json (see references/SESSION.md)
5. bcc-clean-cut     (code + verify + mandatory writeback)
6. if any hardpoint still open → brief status + next hardpoint or stop
   if ALL throughline hardpoints complete AND wrap-up not yet offered/closed
     → one-shot endeavor wrap-up per bcc-throughline (Gate A+B); else do not re-ask
```

**Thin orchestration only** — open each child’s SKILL.md and follow it (throughline user-voice, plan-spar clear-enough + `rounds`, clean-cut ladder). Do not re-copy grill/review/ladder text here.

**Args to forward:** if the user passed `rounds=N` / `review=…` on the main skill, pass them into **bcc-plan-spar** for that slice. Grill still has **no** default Q&A quota.

### Mode B — user drives

User calls sub-skills directly. This main skill is optional. Same voice rules as above.

### Quick status (built-in — not a separate skill)

When user only wants “where are we / what next” (or args `status`):

1. Read `plans.md`, `progress.md`, `findings.md`, `PLAN.md`, `.bcc/session.json` if present.  
2. Prefer a **short natural** answer (goal · now · next · one why). Optional machine block if useful:

```text
BCC status
  goal:     ...
  phase:    ...
  slice:    ...
  PLAN:     missing|draft|locked|complete
  session:  ...
  next:     /bcc-throughline | /bcc-plan-spar | /bcc-clean-cut | ask-user
  why:      <one sentence>
```

3. **Stop** — no grill, no code. If they say “do that next”, load that sub-skill.

| Condition | `next` |
|-----------|--------|
| No `plans.md` / empty goal | `/bcc-throughline` |
| Need align / lock PLAN | `/bcc-plan-spar` (only if throughline OK) |
| PLAN approved for code (session or chat) | `/bcc-clean-cut` |
| All hardpoints `complete` **and** no wrap-up offered/closed yet | one-shot wrap-up (`bcc-throughline` Gate A+B) |
| Wrap-up already offered/closed | do not re-offer (unless user explicitly asks) |
| Unclear | `ask-user` + recommended default |

---

## Hard workflow rules (remind only)

1. **throughline before plan-spar**  
2. **One `PLAN.md`**, updated in place by plan-spar; global progress only in the three throughline files  
3. **Human APPROVE** before clean-cut (session file optional help); **cut freezes PLAN design** (progress 约减 only)  
4. **Writeback** after clean-cut success is mandatory ([WRITEBACK.md](./references/WRITEBACK.md))  
5. Infer next step from docs + chat; **suggest** to user — no heavy formal state machine  
6. Plan-spar: grill until **clear enough** (no default Q&A rounds); **`rounds`** budgets auto-review only  
7. Wrap-up **only** when **all** throughline hardpoints are `complete`, and **once** per cycle (progress/session markers)

## What NOT to do

- Don't install or invent extra slash skills (`bcc-status`, bare `bcc`, etc.).  
- Don't implement product code in this skill except by loading **bcc-clean-cut**.  
- Don't plan-spar without throughline.  
- Don't run Mode A as a long ceremony monologue — same comfort bar as Mode B.  
