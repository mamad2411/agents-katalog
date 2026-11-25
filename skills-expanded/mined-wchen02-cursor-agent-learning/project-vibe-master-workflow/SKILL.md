---
name: project-vibe-master-workflow
description: End-to-end project-level vibe workflow with split on-disk state under .cursor/project-vibe-master/ for resume; state template and optional generated data live in this skill (initial-state/, data/). Combines rules, shell/scripts, MCP, hooks, subagents, HITL, and review/deploy skills.
---

# Project vibe master workflow (full stack)

**Orchestration skill.** This workflow **does not replace** the focused skills (`/agile-project-lifecycle-mcp`, `/release-with-approval`, etc.); it **chains** them conceptually so one session can exercise **rules + scripts + MCP + hooks + subagents + HITL + review/deploy skills**.

Apply **`@general-conventions`**, **`@mcp-patterns`** (when using MCP), and **`@human-in-the-loop`** at gates. For file-type rules, add **`@typescript-patterns`** / **`@api-conventions`** as the stack requires.

## On-disk state (split files + resume) — do this first, every run

1. **Default directory:** `.cursor/project-vibe-master/` (folder under project root, next to other `.cursor/` config). If the user names another directory, use it consistently.
2. **Start of session** — If the folder **does not exist**, create it by copying the template tree [initial-state/](initial-state/) (bundled next to this skill) to `.cursor/project-vibe-master/` (entire directory). Set **meta.md** (project one-liner, last updated) and initial checkboxes in **progress.md**.
3. **Read order** — `project-vibe-master/README.md` (layout), then **meta.md**, **progress.md**, **gates.md**, **slices/README.md**, **only the active slice file(s)** listed there, **backlog.md**, top of **sessions.md**.
4. **Resume logic** — From **progress.md** (snapshot + phase checklist), then **gates.md** (do not re-ask a gate already approved unless the user asks to revisit), then **slices/** (first slice with an unchecked critical step = current work; **current slice file** is named in **slices/README.md** and **progress.md**).
5. **After any meaningful step** — Update the **smallest file that fits** (see README “Write rules” in that folder): e.g. slice work → only that `slices/NN-slug.md`; gate reply → **gates.md** + **progress.md**; session wrap → prepend **sessions.md**; always bump **Last updated** in **meta.md** when you change state.
6. **At each HITL stop** — Set **Blocked on** in **progress.md** before stopping.
7. **User visibility** — When resuming, summarize *Completed / In progress / Next up* from **progress.md** + active slice file so the user can correct you.
8. **Generated artifacts** — Put exports, scratch captures, or MCP dumps from practicing this workflow in [data/](data/) (see [data/README.md](data/README.md)); keep [initial-state/](initial-state/) unchanged as the clean template.

**Legacy:** If you find an old single file `.cursor/project-vibe-master-state.md`, migrate its sections into the split layout (or ask the user); prefer the **directory** layout for new work.

## When to use

- Greenfield or large change where you want **requirements → iterative build → tests → human feedback → security/review → deploy checklist → release gate** in one narrative.
- Learning: run through every technique this repo demonstrates **in order** without editing the underlying skills.
- **Stop/start:** New chat — rerun the skill; it picks up from `.cursor/project-vibe-master/`.

## Phase 0 — Pre-flight (orientation, no code yet)

1. **Rules** — Load conventions above; mention where MCP/hooks apply.
2. **Shell (safe demos)** — From repo root, optionally run `./examples/scripts/demo-info.sh` and `./examples/scripts/count-docs-md.sh` (read-only; see [tool-script-calling](../tool-script-calling/SKILL.md)).
3. **MCP (optional)** — If servers are configured: check tool schema first; e.g. **project-docs** `list_example_scripts` to list script docs without executing on the server. For heavy doc fetch, optionally delegate **mcp-docs-helper** subagent.
4. **Hooks (awareness)** — If the user enabled them: **beforeShellExecution** / **afterShellExecution** (audit/block shell) and **beforeMCPExecution** / **afterMCPExecution** (audit MCP); see `.cursor/hooks/README.md` — do not modify hook files in this skill.
5. **State** — Mark Phase 0 in **progress.md**; update **progress.md** snapshot; **meta.md** timestamp.

## Phase 1 — Discovery, requirements, Gate 1 (HITL)

1. **Research** — **explore** subagent (or main agent): map codebase and patterns.
2. **External truth** — **MCP** for live docs/APIs where relevant; follow `@mcp-patterns`.
3. **Requirements** — User outcomes, acceptance criteria, out of scope, constraints.
4. **Optional security baseline** — **`/security-audit`** (quick pass) or **security-auditor** subagent on sensitive areas (readonly).
5. **Gate 1 — Requirements** — Explicit handoff: *Approve requirements / Refine / Abort.* **Stop** until the human replies.
6. **State** — Optional requirements pointer in **sessions.md** or slice notes; before stop, **Blocked on** in **progress.md**; after human replies, **gates.md** + **progress.md** checkboxes.

## Phase 2 — Plan slices

- Invoke **planner** subagent with approved requirements. Optionally use MCP to refine API/library scope. Present slices and the **current slice**.
- **State** — Add one `slices/NN-slug.md` per slice (copy from `slices/01-placeholder.md` pattern); update **slices/README.md** (table + **Current slice file**); set **Current slice file** in **progress.md**; check Phase 2 boxes in **progress.md**.

## Phase 3 — Development cycle per slice (loop)

For each slice until the human says **Complete** or final approval:

1. **Develop** — Implement; use MCP for up-to-date APIs/libs when needed.
2. **Tests** — Unit → integration → e2e (or manual checklist) per [agile-project-lifecycle/reference.md](../agile-project-lifecycle/reference.md).
3. **If red** — **debugger** subagent → fix → re-run; treat as a mini **`/bugfix-and-verify`** loop.
4. **Verify** — **verifier** subagent (can optionally cross-check with MCP against docs).
5. **Gate 2 — Iteration** — Summary + *Approve / Next slice / Feedback: … / Complete / Abort.* **Stop** until the human replies.
6. **State** — Update **only the active slice file** for develop/test/verify checkboxes; **progress.md** snapshot; before Gate 2 stop, **Blocked on**; after reply, **gates.md** + **progress.md**.

## Phase 4 — Quality and ship prep

1. **`/code-review`** skill on the changed surface.
2. If auth/payments/PII touched: **security-auditor** subagent (readonly).
3. **`/deploy-checklist`** skill before any deploy suggestion.
4. **State** — **progress.md** Phase 4 boxes; prepend **sessions.md** with outcomes.

## Phase 5 — Final release handoff (HITL)

- Run the **same human gate pattern** as **`/release-with-approval`**: review package, breaking changes, risks; *Approved / Request changes / Abort*; **no tag/deploy** unless the user explicitly asks after approval.
- **State** — **gates.md** Gate 3 row; **progress.md** current phase `done`; **Remaining** empty or handoff-only; **meta.md** timestamp.

## Reference

- Full narrative + diagram: [examples/agent-frameworks/project-vibe-master-workflow.md](../../../examples/agent-frameworks/project-vibe-master-workflow.md)
- State template (copy to `.cursor/project-vibe-master/`): [initial-state/](initial-state/)
- Generated outputs (optional): [data/](data/)
- Pointer doc (old links): [examples/agent-frameworks/project-vibe-master-state.template.md](../../../examples/agent-frameworks/project-vibe-master-state.template.md)
- Technique map: [reference.md](reference.md)
