---
name: autotdd
description: Fully-automatic mode — runs tdd2 then acpd for each issue, one issue completely finished (implement+verify+merge+push+deploy) before the next starts, never batching, never prompting mid-run. With no issue numbers, lists everything left in issues/ and asks once whether to run through all of it. Use when the user says "/autotdd", "autotdd #", or gives a list/range of issue numbers to fully implement and ship unattended.
---

# autotdd — tdd2, then acpd, per issue, fully automatic

The name is literal: **tdd** (via `tdd2`) **+ auto**mating everything
after it (`acpd`: archive, commit, push, deploy). Pure orchestration:
no script of its own. It composes `tdd2` (implementation, stops at
`git add`) and `acpd` (archive+commit+push+deploy), run back-to-back
for each issue number.

**= implement (+verify+git add) + merge (archive+commit+push) + deploy to dev**

## How this package relates to plain `/tdd`

Once Matt Pocock's `tdd` skill and this package are both installed,
`tdd2` is what `/tdd` *means* in a repo that tracks work as local
`issues/issue-#.md` files — it's the same red→green→refactor
discipline, just pointed at that local-file SDLC instead of a bare
prompt. `/tdd # + /acpd #` and `/tdd2 # + /acpd #` do the same thing;
saying `tdd2` is just unambiguous about which flavor you mean. All
three of `/tdd`, `/tdd2`, and `/acpd` can stop and ask the user
something. `/autotdd` is the odd one out: it chains `tdd2` and `acpd`
per issue and is built to run **unattended** — see "The one rule that
matters" below for exactly what that rules out.

## Dependency check — run this first, every invocation

`tdd2` depends on Matt Pocock's `tdd` skill for the actual
red→green→refactor discipline (`tdd2` just wraps it with the
local-file issue SDLC). Before doing anything else — before listing
issues, before the "run through all N?" prompt, before touching any
issue — confirm `tdd` is actually available:

```bash
[ -f ~/.claude/skills/tdd/SKILL.md ] || [ -f "$(git rev-parse --show-toplevel 2>/dev/null)/.claude/skills/tdd/SKILL.md" ]
```

(Or check it against the Available Skills listing already in context —
either way of confirming is fine.)

- **Found** → proceed normally.
- **Not found** → stop immediately and tell the user:

  > Matt Pocock's `tdd` skill isn't installed (checked
  > `~/.claude/skills/tdd/` and `.claude/skills/tdd/` in this repo —
  > neither exists), and `tdd2` depends on it. This package doesn't
  > know where you originally got it from, so it can't hand you an
  > install command — but you already have several of its sibling
  > skills installed (`ask-matt`, `grill-me`, `to-issues`, `to-prd`,
  > `code-review`, `implement`, etc., all under `~/.claude/skills/`):
  > install `tdd` from wherever those came from, the same way, so it
  > ends up at `~/.claude/skills/tdd/SKILL.md` (or
  > `.claude/skills/tdd/SKILL.md` if you're installing it per-project
  > instead of globally). Re-run `autotdd` once it's there.

  Do **not** guess a GitHub URL or invent an install command — if none
  of `tdd`'s sibling skills are present either to point at, just report
  that `tdd` is missing and required, and stop.

## Two ways to invoke it

### `/autotdd <numbers>` — scope given, runs immediately

No confirmation — the numbers are the scope. Go straight to the loop
below.

### `/autotdd` — no numbers, scope is implicit

1. List every issue still in `issues/` (not yet archived) — everything,
   regardless of state: not started, in-progress, or already
   pending-deploy.

   ```bash
   ls issues/issue-*.md 2>/dev/null
   ```

2. Show the list, ask **once**: "run through all N of these in order?"
3. Yes → build the ordered issue-number list from that listing and
   enter the fully-automatic loop below. No further questions from
   this point on.
4. No → stop; don't guess a partial scope.

This is the *only* prompt `autotdd` ever shows (aside from the
dependency check above, which isn't really a prompt — it's a hard stop
if `tdd` is missing, not a question). Once the run starts (whichever
way it started), it does not ask anything else — see "The one rule
that matters" below for what that means concretely.

## Parsing an explicit issue list

| Input | Meaning |
|---|---|
| `autotdd 100` | issue 100 |
| `autotdd 100 101 102` | issues 100, 101, 102 |
| `autotdd 100, 101, 102` | issues 100, 101, 102 |
| `autotdd 100 to 110` | issues 100–110 inclusive |
| `autotdd 100 ~ 110` | issues 100–110 inclusive |

Rule: extract all numbers from the input. If there are exactly two and
they're joined by `to` or `~`, expand to the inclusive range. Otherwise
treat every extracted number as a listed issue, in the order given.

## The one rule that matters

> ⚠️ Never run all the `tdd2`s first and all the `acpd`s after. Each
> issue must be **fully finished** — `tdd2 #` immediately followed by
> `acpd #` — before touching the next issue number. And within a run,
> **never prompt** — not per-issue, not for UI verification (see the
> exception noted in `tdd2`'s step 10), not for anything. The single
> upfront "run through all N?" question (no-number case only) and the
> dependency check above are the entire interactive/blocking surface of
> this skill.

`autotdd 1 2 3` is:

```
tdd2 1 → acpd 1 → tdd2 2 → acpd 2 → tdd2 3 → acpd 3
```

**not**

```
tdd2 1 → tdd2 2 → tdd2 3 → acpd 1 → acpd 2 → acpd 3
```

Why: once an issue is pushed and deployed to dev, it's a clean
checkpoint — a mid-batch failure has an unambiguous boundary between
what's live and what's untouched. Stacking implementations first
destroys that boundary.

## Per-issue loop

For each issue `#` in the target list, **check its state first** —
don't redo finished work:

```bash
grep -q '\*\*구현 완료 일시\*\*: *(미정)' "issues/issue-${n}.md"
```

- Placeholder still `(미정)` (not implemented, or in-progress) →
  `tdd2 #` (implements + verifies + `git add`, stops there), then
  `acpd #`.
- Already filled in (implemented earlier, never merged — e.g. a prior
  `tdd2` run that stopped short of `acpd`) → skip straight to `acpd #`.

```
for # in <target list>:
    if issues/issue-#.md does not exist:
        warn and skip #, continue to next
    if 구현 결과 already filled in:
        acpd #
    else:
        tdd2 #      ← implement + verify + git add (stops there)
        acpd #      ← archive + commit + push + deploy --env dev
    # is done only once the applicable step(s) above have completed
```

- **Any failure stops the whole run immediately** — a non-zero verify,
  a failed commit/push/deploy, a UI-verification step that needed a
  human and `agent-browser` wasn't available, anything. Report which
  issue failed and at which step; do not proceed to the remaining
  issues.
- On success, report the full list of completed issue numbers.
