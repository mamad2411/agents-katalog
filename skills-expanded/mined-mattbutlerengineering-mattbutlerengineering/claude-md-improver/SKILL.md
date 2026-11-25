---
name: claude-md-improver
description: "Audits CLAUDE.md, AGENTS.md and .claude/rules/* for dangling paths, table drift, unresolvable mandates and undocumented surfaces; proposes, never writes silently. Use when instructions feel stale, after a big refactor or extraction, or from the monthly mbe-monthly-meta-audit routine."
user-invocable: true
allowed-tools: Read, Edit, Write, Glob, Grep, Bash, AskUserQuestion, TodoWrite
---

# CLAUDE.md Improver

Instruction files rot in a way code does not: nothing compiles them, no test imports them, and every reference inside them is a plain string. A path can move, a skill can be extracted to a plugin, an agent can be added — and `CLAUDE.md` keeps confidently pointing at the old world. The cost lands on exactly the sessions least able to notice: fresh cloud checkouts, worktree agents, scheduled routines.

This skill mechanically checks the claims instruction files make against what is actually on disk.

**Output is a proposal, never a silent write.** Show findings, get a decision, then edit.

## Arguments

- (none) — audit `CLAUDE.md`, `docs/claude-reference.md` (the skill/subagent/CLI tables moved out of CLAUDE.md), `AGENTS.md`, `docs/agents-reference.md` (the package inventory and tool lists moved out of AGENTS.md), and `.claude/rules/*.md`.
- `--file <path>` — audit one file only.
- `--apply` — after review, apply the accepted fixes.
- `--dry-run` — report only; make no edits even if accepted.

## Scope note

This is about **instruction quality**, not prose style. Do not rewrite wording that is merely verbose. Every finding must be a checkable claim that is false, or a documented surface that is missing. If you cannot state the finding as "X says Y, but Y is not true", it does not belong in the report.

## Process

### Step 0: Track the run

Use TodoWrite: inventory → dangling paths → table drift → unresolvable mandates → undocumented surfaces → rank → propose → apply.

### Step 1: Dangling path references

Every repo-relative path mentioned in an instruction file should exist. Extract and test them:

```bash
# path-like tokens from markdown links and backticked spans
grep -ohE '\]\(\./[^)]+\)|`[a-zA-Z0-9_./-]+\.(md|js|mjs|ts|tsx|json|sh|yml|yaml)`' CLAUDE.md docs/claude-reference.md AGENTS.md docs/agents-reference.md \
  | tr -d '`()[]' | sed 's|^\./||;s|#.*$||' | sort -u \
  | while read -r p; do [ -e "$p" ] || echo "MISSING: $p"; done
```

Also test paths that appear inside command examples (`node scripts/foo.js`, `bash .claude/hooks/bar.sh`) — those are the ones a session will actually try to run:

```bash
grep -ohE '(node|bash|sh) [a-zA-Z0-9_./-]+\.(js|mjs|sh)' CLAUDE.md docs/claude-reference.md AGENTS.md docs/agents-reference.md \
  | awk '{print $2}' | sort -u \
  | while read -r p; do [ -e "$p" ] || echo "MISSING (in command): $p"; done
```

> Real finding (2026-08): `CLAUDE.md` told sessions to re-run `node scripts/acmm/audit.js` as a source-of-truth check. That directory no longer exists — the script moved to `plugins/acmm/scripts/audit.js` when the plugin was extracted in #818. The same file _also_ documented the extraction elsewhere, so it contradicted itself.

A path inside a fenced block is still a real reference. Do not skip fenced blocks.

### Step 2: Table drift (documented vs. on disk)

Instruction files carry hand-maintained tables of skills, labels, and commands. Diff each against reality — in **both** directions.

```bash
# skills: documented in docs/claude-reference.md vs. directories on disk
grep -oE '^\| `/[a-z0-9-]+`' docs/claude-reference.md | tr -d '|` /' | sort -u > /tmp/doc-skills
ls .claude/skills/ | sort -u > /tmp/disk-skills
echo "--- documented but absent from .claude/skills/:"; comm -23 /tmp/doc-skills /tmp/disk-skills
echo "--- on disk but undocumented:"; comm -13 /tmp/doc-skills /tmp/disk-skills
```

A documented-but-absent entry is not automatically a bug — it may have moved to a plugin or to user level. Resolve each before reporting:

```bash
ls plugins/*/skills/ 2>/dev/null   # extracted to a plugin?
ls ~/.claude/skills/ 2>/dev/null   # user-level install?
```

If it moved, the table entry needs to say so. If it is simply gone, the row should go.

Apply the same both-directions diff to the GitHub label table (`gh label list`) and the `mbe` CLI command list (against `tools/cli/src/index.ts`).

### Step 3: Mandates that cannot be followed

The highest-severity class. An instruction file says _do X_, and X does not resolve in the environment reading it. Collect every imperative reference to a skill or command and check it:

```bash
grep -nE '(Use|Run|Always use|Invoke) .*`/[a-z0-9-]+`' CLAUDE.md docs/claude-reference.md AGENTS.md docs/agents-reference.md
```

For each, check all three resolution sites — `.claude/skills/<name>/`, `plugins/*/skills/<name>/`, and `~/.claude/skills/<name>/`.

Weigh this by **who reads the file**. `CLAUDE.md` is checked in, so it is read by cloud sessions, worktree agents, and scheduled routines that have none of a developer's local installs. A mandate resolvable only at user level is effectively broken for every automated session — which are the ones relying on written instructions most.

> Real finding (2026-08): the "Feature Implementation" section mandated _"Always use TDD… Use `/tdd` skill for the workflow"_, while another section of the same file recorded that `/tdd` had been retired to user-level installs by #3323. No `tdd` directory existed in the repo, and none in `~/.claude/skills/` in a cloud checkout.

Flag the same way any tool documented as ready-to-use that actually needs an install step first.

### Step 4: Undocumented surfaces

The inverse of steps 1–3: things that exist and matter, that no instruction file mentions. A capability nobody documents is a capability nobody uses.

```bash
for d in .claude/agents .claude/hooks .claude/rules plugins; do
  [ -d "$d" ] || continue
  if grep -qF "$d" CLAUDE.md docs/claude-reference.md AGENTS.md docs/agents-reference.md 2>/dev/null; then echo "documented: $d"; else echo "UNDOCUMENTED: $d"; fi
done
```

For any undocumented directory, count what is in it — a single stray file is noise, a populated directory of specialist tooling is a real gap.

> Real finding (2026-08): `.claude/agents/` held 8 specialist reviewer subagents, several encoding specific past failures (an E2E selector-drift arc, a merge-train Integrity wedge, a component prop-drift breakage). `grep -niE "\.claude/agents|subagent" CLAUDE.md AGENTS.md` returned zero matches — nothing told a session they existed.

### Step 5: Rank and propose

Order findings by blast radius, not by how easy they are to fix:

1. **Unfollowable mandate** — instructs an action that cannot be performed.
2. **Dangling path in a command** — a session will run it and fail.
3. **Table drift** — sends a session to the wrong place.
4. **Undocumented surface** — capability sits unused.
5. **Dangling path in prose** — a broken link.

Present as a table (finding, evidence command + its output, severity, proposed fix). Include the _evidence_, not just the claim — a reviewer must be able to re-run one command and see it.

Then apply the repo's standard contract:

- Fix the single best finding directly → **one reviewable PR**.
- File the rest as `ready` + `meta-improvement` issues with self-contained acceptance criteria.
- Never merge; every change lands as a reviewable PR.

## Anti-patterns

- **Don't** rewrite prose for tone, length, or style. Out of scope.
- **Don't** report a documented-but-absent skill without first checking plugins and user-level installs — extraction is the common case and the fix is different.
- **Don't** treat a `~/.claude/`-only resolution as passing when the file is checked in. State which environments it breaks for.
- **Don't** bundle unrelated fixes into the one PR. Strict scope; the rest become issues.
- **Don't** propose a hand-maintained table where a generated one is cheap. Hand-written tables are the thing that drifts — if a generator plus a drift check is a few lines, propose that instead.
