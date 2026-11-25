---
name: skillci-guardrails
description: Use this skill whenever you create, edit, or review a Claude Skill — any SKILL.md file, or the eval cases/config next to one. Most SKILL.md files today are written or edited by an agent, not typed by hand, so this closes the loop by having the agent that just wrote the skill also author it defensively and verify it, the same way a linter and test suite run after any other code change. Trigger phrases include "write a skill", "create a SKILL.md", "add a new skill", "edit this skill", "update the skill's frontmatter/description/triggers", or any diff that touches a SKILL.md path.
---

# skillci guardrails

A `SKILL.md` is code: its frontmatter is an API, its body is an
executable instruction set. It fails silently — a model just quietly
does the wrong thing — rather than loudly, which makes both authoring it
defensively and verifying it after the fact more important than for
ordinary code, not less.

## Step 1 — Author defensively, don't just lint afterward

These map directly to skillci's own static checks, so getting them right
up front means Step 2 finds nothing instead of catching it after the
fact:

- **`description`** is the single field that decides whether this skill
  gets discovered and triggered at all — state what it does *and* when to
  use it, in language close to how a user would actually phrase the
  request. Keep it under 1024 characters (skillci flags longer — it eats
  into every caller's trigger-matching budget).
- **Never instruct piping a downloaded script straight into a shell
  interpreter**, and never reference an unpinned `:latest`/`@latest`
  dependency — OWASP AST01/AST02, both real risk, not just lint noise.
- **Don't request network access to non-localhost hosts** unless the
  skill's purpose requires it (AST03).
- **Never fetch remote content and tell the model to treat it as
  authoritative instructions** (AST05) — use frontmatter's
  `pinned_sources` (a declared `sha256`, verifiable on request) instead.
- **Keep the body lean**: under ~8000 characters, no exact-duplicate
  lines, no more than ~10 referenced files or ~100KB combined. Every
  extra line loads on every invocation.

## Step 2 — Verify

Prefer calling skillci's own MCP tools directly if available in this
session (`check`, `eval`, ...) over shelling out. Fall back to the CLI
otherwise:

```bash
skillci check <path-to-skill-dir>
```

1. **Always run `check`** — local-only, free, no API calls. Fix every
   finding, including Minor ones. If the repo pilots skillci
   non-blocking, `--mode warn` (or `.skillci.yaml`'s `lint.mode`) reports
   without failing — still read and act on the output.
2. **If eval cases exist, run `eval`** — confirms a trigger/behavior
   change actually works, not just that it reads plausibly.
3. **If eval cases don't exist and the skill is non-trivial, write at
   least one first.** "Non-trivial" means: more than one trigger
   condition, any security-relevant behavior, or reuse beyond this
   session.
4. **If skillci isn't installed**: `go install
   github.com/kabirnarang39/skillci/cmd/skillci@latest` (or see
   https://github.com/kabirnarang39/skillci#install). Install it, don't
   skip verification.

## Step 3 — Pick the right assertion for a new eval case

Don't reach for the heaviest tool by default — match the assertion to
what actually needs checking:

| The skill... | Reach for |
|---|---|
| Should fire on certain phrasings | `triggered: true` |
| Must produce specific required text | `contains: [...]` |
| Must never produce certain text | `not_contains: [...]` |
| Needs subjective/quality judgment a substring match can't express | `judge:` (named rubric criteria, scored by a separate model) |
| Fetches/executes untrusted content, or is otherwise security-sensitive | `redteam:` (named attack plugins across the injection, jailbreak, pii, harmful, and agency categories — see the redteam plugin table in skillci's README for the current list) |
| Needs to hold up under realistic rewording, not just the exact prompt you tested | `fuzz: true` (add `fuzz_llm: true` for model-generated paraphrases, cached once) |
| Must not silently change behavior on a model update | `snapshot: true` |
| Has a real cost/latency/token budget to enforce | `max_cost_usd` / `max_latency_ms` / `max_tokens_loaded` |

A minimal but real example:

```yaml
name: "haiku-request-triggers"
prompt: "Can you write me a haiku about autumn leaves?"
skill_under_test: "haiku-writer"
assert:
  triggered: true
  contains: ["autumn"]
```

## Step 4 — Beyond check/eval: the rest of the toolkit

check and eval are the two you'll reach for almost every time, but know
the rest of the surface exists — call these as MCP tools where available,
or the equivalent CLI command otherwise:

- **`init <path>`** — scaffolds `.skillci.yaml` and an example eval case.
  Check it doesn't already exist first; run once, the first time a skill
  gets eval coverage.
- **`regress <path>`** — the full model-matrix run CI actually gates on,
  diffed against the last known-good run, failing only on a *new*
  regression. Normally CI's job, not something to trigger speculatively —
  but the command to add when wiring up CI for a skill the first time.
- **`fuzz <path>`** — just the fuzz-enabled cases in isolation, without a
  full eval pass.
- **`bisect <case-name> --path <path>`** — finds which commit broke a
  known-failing case, binary-searching real git history via a `git
  worktree`. Needs the skill inside a git repo with real commits.
- **`accept <case-name> --path <path>`** — promotes a `regress`-generated
  case (or, with `--model`, a pending snapshot change) into permanent
  coverage. Read what it asserts first — it's evidence a regression
  happened, not automatically correct behavior to lock in.
- **`diff <case-name> --path <path>`** — shows a pending snapshot change
  against its golden baseline without accepting it.
- **`badge <path>`** — regenerates the SVG status badge; `regress` already
  does this automatically, rarely needed standalone.
- **`report --compliance nist-ai-rmf|eu-ai-act <path>`** — a Markdown
  evidence report (not a certification) for a governance reviewer. Only
  when someone's actually asking for it.

## What to do with findings

Fix them, the same way you'd fix a failing test or a lint error before
telling the user a code change is complete — don't report the skill as
finished with known-but-unfixed findings unless the user explicitly says
to leave them.

## Don't

- Don't reach for `judge:` for something `contains:`/`not_contains:`
  could check for a fraction of the cost.
- Don't add `redteam:` to every skill by default — reserve it for skills
  that fetch external content, execute code, or touch anything
  credential-adjacent.
- Don't set a `*_strict` flag (`snapshot_strict`, `latency_strict`,
  `flake_strict`, `judge_strict`, `redteam_strict`) without understanding
  what it gates — each is a no-op without its paired base assertion also
  set, and it now hard-fails CI.
- Don't run `eval`/`regress` speculatively against unrelated skills
  "while you're at it" — scope this to the skill you actually touched.
- Don't add an elaborate eval suite to a trivial, static skill with no
  real trigger logic or security surface to test.
