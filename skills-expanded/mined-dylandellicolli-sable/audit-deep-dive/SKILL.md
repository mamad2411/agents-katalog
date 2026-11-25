---
name: audit-deep-dive
description: |
  Convert an `AUDIT: ...` bead into an epic + child bead graph through
  direct code exploration, prioritized findings, user approval, and
  structured bead creation. Use when:
    - User says "audit X", "let's do an audit", "tackle the next audit
      bead", "do an audit deep-dive on Y", or "/audit-deep-dive"
    - A bead in `bd ready` has the title prefix `AUDIT:`
    - The deliverable is "produce a bead graph" rather than code
  Validated four times across security, observability, frontend, and
  testing audits — produced 54 bead-graph items the user described as
  "extraordinarily valuable."
allowed-tools:
  - Read
  - Glob
  - Grep
  - LS
  - Bash
  - AskUserQuestion
---

# /audit-deep-dive

Workflow for turning an `AUDIT:` bead into an epic with prioritized child
beads. The deliverable is the bead graph, not code changes.

## When to use

- The user wants to work an `AUDIT: ...` bead from `bd ready`
- The user says "let's do an audit" or names a specific audit
- They want to plan a focused area before any implementation work begins

If the user wants you to FIX something (not plan), this is the wrong skill —
use the relevant feature-dev or debugging workflow instead.

## Inputs

- The audit bead (must exist in `bd`; if not, ask the user to create one
  first — captures scope and acceptance in a durable place)
- The audit bead's `description` — defines scope as a numbered list of
  areas to investigate
- Coordination beads referenced in the description ("coordinate with X",
  "bundled into Y", "depends on Z")
- The actual codebase
- Recent closed audit beads of the same kind for format precedent

## The pause-before-create rule

The single highest-leverage step in this workflow is **presenting the
findings list for approval BEFORE creating any beads**. Skipping it forces
the user to review N beads one-by-one after the fact instead of approving
the structure once. Treat it as non-negotiable.

## Steps

### 1. Locate the audit bead

If the user named one (e.g., "let's do twine-XXXX"), use that. Otherwise:

```bash
bd list --status=open -n 100 | grep -i AUDIT
```

Show the open audit beads with brief descriptions. Recommend one based on
priority and scope size, but let the user pick.

### 2. Claim and load coordination context

```bash
bd update <audit-id> --claim
bd show <audit-id>
```

In the description, scan for references like "coordinate with twine-XXXX"
or "bundled into twine-YYYY" or "depends on twine-ZZZZ". `bd show` each so
you can avoid duplicating their scope.

Also pull format precedent from any closed audit beads:

```bash
bd list --status=closed -n 200 | grep -i audit
bd show <closed-audit-id>
```

The structure of past closed reasons ("Produced epic X with N children
across M phases ...") tells you what shape to aim for.

### 3. Map the code surface DIRECTLY

**Critical — do NOT dispatch a subagent for this.** Audit scope is
well-defined enough that direct Read/Grep/Glob keeps findings grounded in
real `file:line` references rather than agent-summarized prose.

For each numbered scope item in the audit description:
- Use `Glob` / `LS` to find relevant files
- Read each file (full file for small ones; relevant ranges for large ones)
- Note findings inline as you read — file path + line number + observation
- Run targeted `Grep` for cross-cutting concerns (e.g., "every place that
  references env var X")

If an item turns out to be larger than expected and you're getting
overwhelmed, switching to a subagent is acceptable — but only for that
one chunk, with a tight scope description.

### 4. Verify critical findings

Before claiming any P0:
- For "missing auth check" → grep the migration / function for explicit
  GRANT/REVOKE; check default Postgres permissions
- For "endpoint never works" → trace caller → callee paths to confirm the
  shape mismatch
- For "config missing" → check for the file in all expected locations
  (root, frontend/, package.json scripts)
- For "credential leaked to client" → check the import graph; verify the
  file actually reaches a client component

Hallucinated beads waste a full agent cycle when someone tries to fix
them. Spend 30 seconds verifying.

### 5. Catalog findings as a prioritized list

Severity tiers:

| Tier | Definition |
|------|------------|
| **P0** | Data loss, security hole exploitable today, silent total feature breakage (e.g. cron not running) |
| **P1** | Silent partial breakage, easy attack vector, missing validation that ships in next release |
| **P2** | Code smell with shipped impact, observability gap, dev-experience drag |
| **P3** | Cleanup, low-priority hardening, dead-code removal |

Every finding gets:
- Title (short, action-oriented, opens with `[Phase] ` prefix)
- File path(s) + line number(s) — concrete refs
- One-sentence "what's wrong"
- One-sentence "why it matters"
- Suggested approach (1-2 sentences, name the pattern to copy if one exists)
- Test spec (file path + assertion shape, even if the test doesn't exist yet)

ADRs (architectural decision records) are their own line items, prioritized
by what they unblock.

Group findings into 3-5 phases (e.g., A1 Critical security, A2 Tokens,
A3 Identity flow, A4 Public surface, A5 Cleanup). Phases become the
epic's organizing principle and show up in every child title.

### 6. Present BEFORE creating

Present the full findings list to the user with this shape:

```markdown
## Critical (P0)
1. **<short title>** (`path:line`). One sentence what + why.
2. ...

## High (P1)
3. **<short title>** (`path:line`). ...

## Medium (P2)
...

## Low (P3)
...

## Plus an ADR (if any)
...

Sound right? Any to drop, merge, or re-prioritize before I create the epic?
```

If the audit description includes open questions you couldn't answer from
the code alone (e.g. "is X actually configured in production?"), ASK THEM
HERE. Answers can swing P2 to P0. Two examples from the observability audit:
"Are crons actually running?" and "Do preview deploys hit prod Supabase?"
Both answers turned P1s into P0s.

WAIT for explicit user approval before creating beads. "Looks good, create
them" is enough; silence is not.

### 7. Create epic + children

Naming conventions (matching twine pattern):
- Epic title: `[epic] <area> hardening (audit <audit-id>)`
- Epic priority: P0 if ANY child is P0, else match highest child priority
- Child title: `[<phase>] <action-oriented summary>` — e.g.
  `[A1 Security] merge_ghost_profiles SECDEF missing auth.uid check (P0)`

`bd` constraints (from CLAUDE.md global rules):
- ONE `bd` command per Bash call (no `&&` chains, no `;` separators)
- Inline `--description "..."` (no heredoc — opens `$EDITOR`)
- No newline-prefixed `#` in description text (triggers ambiguous-syntax
  check even inside quotes)
- Use the right field for the right concern:
  - `--description` — the WHAT and WHY (a fresh agent can act on this alone)
  - `--design` — the HOW (approach, code pattern to copy, alternatives)
  - `--acceptance` — verification criteria
  - `--notes` — coordination context, dependencies, reminders

Create the epic FIRST (sequential — you need its ID for parenting), then
batch children in parallel — 4-5 `bd create` Bash calls per message.

### 8. Parent and dep links

Parent every child under the epic:

```bash
bd update <child-id> --parent <epic-id>
```

For inter-bead dependencies (e.g. "bead A needs bead B before it can
land"): use **`bd dep relate`** (bidirectional `relates_to`), NOT
`bd dep add`. The latter currently fails with `table not found:
wisp_dependencies` on twine's `.beads` schema. Logged via `sable-note`.

```bash
bd dep relate <bead-A> <bead-B>
```

If the dep is a hard blocker rather than just "related", note it in the
description's `--notes` field as well so future agents see it.

Batch the parent updates and relate calls in parallel — they're independent.

### 9. Close the audit bead

The TDD gate hook blocks `bd close` without test evidence. Audit beads
have no code changes, so add `[no-test]` to notes first:

```bash
bd update <audit-id> --notes "[no-test] Audit task — deliverable is the bead graph, no code changes."
```

Then close with a structured reason:

```bash
bd close <audit-id> --reason="Audit complete. Produced epic <epic-id> '<epic-title>' with N child beads across M phases (<phase-list>). P0s: <list>. <One-line coordination notes pointing at related beads outside this epic>. <Notes on superseded/closed predecessor beads if any>. [no-test] audit task."
```

The reason field becomes searchable history — make it informative.

### 10. Push to Dolt

```bash
sable-dolt-push  # blessed wrapper, never bare `bd dolt push`; chuck-only in a swarm
```

Beads live in `.beads/` via Dolt. Auto-commit is local; `dolt push` makes
them visible across sessions and machines. Skip this and the next agent
session won't see your work.

### 11. Final summary to user

End with a markdown table of children:

```markdown
| Phase | Bead | Pri | Title |
|---|---|---|---|
| A1 | twine-xxxx | P0 | ... |
| ... |
```

Plus a one-line note on what's been pushed and what's next-actionable.

## Anti-patterns

| Don't | Do |
|---|---|
| Create beads then ask user "approve?" | Present findings list FIRST, create after approval |
| Dispatch a subagent for the exploration | Direct Read/Grep/Glob — grounds findings in file/line refs |
| Use `bd dep add` for the inter-bead link | Use `bd dep relate` (workaround for known schema bug) |
| Skip verifying P0 findings before filing | Grep/Read to confirm — hallucinated beads waste cycles later |
| Forget `[no-test]` before `bd close` | TDD gate hook blocks; add note first |
| Use heredoc or chained bash for `bd` commands | One `bd` per Bash call, inline strings |
| Cram all findings into one mega-description | One bead per finding (or tight cluster) — beads are the unit of work |
| Re-discover what an existing bead already tracks | Check `bd search` before filing — supersede or update the existing one |

## Output shape

After running this skill end-to-end, the user has:

- One closed audit bead with a structured close-reason pointing at the epic
- One new epic bead at the appropriate priority
- N child beads (typically 4-14, depending on audit scope) — each with
  fresh-agent-quality descriptions, file paths, suggested approaches, and
  test specs
- Parent links from every child to the epic (visible via `bd children <epic-id>`)
- Optional inter-bead `relate` links for cross-bead coordination
- Stale or obsolete predecessor beads either updated (with supersession
  note) or closed
- All pushed to Dolt

The user's `bd ready` queue now reflects actionable, prioritized work that
a future fresh agent can pick up without re-exploring source files.

## Variant: ad-hoc audit (no pre-existing AUDIT bead)

If the user wants to audit an area but no bead exists yet, suggest
creating one first:

```bash
bd create --type=task --priority=0 --title="AUDIT: <area> deep-dive" --description="<scope as numbered list>"
```

Then proceed from Step 2. The bead captures the scope and acceptance in a
durable place — without it, the audit's existence depends on conversation
context, which is amnesiac across sessions.
