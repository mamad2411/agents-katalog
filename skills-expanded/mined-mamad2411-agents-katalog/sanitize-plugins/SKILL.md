---
name: sanitize-plugins
argument-hint: '[plugin-name(s) | all] — omit when calling this interactively to be asked; a caller invoking this from another script must always pass an explicit scope, never call it bare'
description: >
  Pre-publish privacy/IP/secrets gate for this repo (ember-claude-toolkit).
  Runs a team of scanner subagents over a plugin's content before it is
  published, to catch secrets, personal data, other-project/IP leakage,
  non-portable hardcoded paths, and non-generic wording. Read-only — reports
  findings, never edits. Trigger on "/sanitize-plugins", "sanitize the
  plugins", "scan for leaks", "is this safe to publish", or automatically as
  the mandatory first step of refresh-plugins before any plugin is
  tagged/pushed.
---

# sanitize-plugins

A small **virtual security-review team** that checks plugin content for
anything that shouldn't go into a public, shared repo before `refresh-plugins`
ever commits/tags/pushes it. This exists because a plugin here started life as
a personal, loose skill in `~/.claude/skills/` — those accumulate real paths,
real config, real project references, and personalized wording that must be
stripped or genericized before the same content is safe to publish.

This skill is an **orchestration**: you (the main agent) run the phases and
delegate to subagents. Like the librarian, you own a **human approval gate** —
nothing gets silently auto-fixed. This skill only finds and reports; fixing is
a separate, explicit step afterward.

## The team (first-class agents in `.claude/agents/` at this repo's root)
| Agent | Lens | Writes? |
|-------|------|---------|
| `sanitize-secrets-scanner` | API keys, tokens, passwords, private keys, connection strings | No (proposes findings file) |
| `sanitize-personal-data-scanner` | Absolute home paths, personal emails/phone numbers, personal financial figures | No |
| `sanitize-ip-scanner` | References to *other* projects/clients/codebases on this machine | No |
| `sanitize-portability-scanner` | Hardcoded paths/assumptions that break (not necessarily leak) for another installer | No |
| `sanitize-genericity-reviewer` | Personalized phrasing that should read as generic, shareable guidance | No |
| `sanitize-verifier` | Adversarial second pass — tries to refute each finding before it reaches the human | No |

> Launch each with `subagent_type: "<name>"`. All five finders can run in
> parallel — send them in a single message with multiple Agent tool calls.

## Step 1 — Scope

**If an argument was given** (one plugin name, several, or the literal `all`):
scope to exactly that — no prompt, no auto-detection, no second-guessing the
caller. This is the path any other script/skill (e.g. `refresh-plugins`) MUST
use: a caller invoking this skill from within its own flow always passes its
own already-determined scope explicitly. Never invoke this skill bare from
inside another script — an unattended prompt would stall that flow.

**If no argument was given** (a direct, interactive `/sanitize-plugins`
invocation with nothing after it): this is the only case where you ask.
Determine the candidate list — every plugin under `plugins/` that has
uncommitted changes OR no commits since its last `<name>--v*` git tag counts
as "changed" (reuse `refresh-plugins`' `scripts/check.sh` change-detection
rather than re-deriving it); every other plugin under `plugins/` is a
candidate too, just not pre-selected. Then use `AskUserQuestion` to ask which
to sanitize, offering: each changed plugin individually, an "all changed
plugins" option, and an "all plugins regardless of change state" option. Scope
to whatever was picked.

If the resolved scope (from either path) is empty, report that and stop —
there's nothing to sanitize.

## Step 2 — Sweep (parallel finders)
For each plugin in scope, run all five finder agents in parallel, each given:
the plugin's directory path, and a scratchpad output path for its findings
file (use the session scratchpad directory, never a path inside this repo —
findings files must never be committed).

Each finder returns a findings path and a one-line headline count. Read each
findings file.

## Step 3 — Adversarial verify
For every **high-confidence** finding (and any low-confidence one that looks
material on inspection), spawn a `sanitize-verifier` with that specific
finding plus the plugin path. Collect verdicts. A finding marked **REFUTED**
is downgraded to "dismissed — see reasoning" but still shown at the gate, not
silently dropped. A finding marked **NOT REFUTED** is "confirmed."

## Step 4 — Human gate
🟧🟧🟧 HUMAN GATE REQUIRED 🟧🟧🟧
Present all confirmed findings first, grouped by scanner/category, each with:
file:line, what was found, why it matters, and the verifier's take if one ran.
Then list dismissed findings briefly, so nothing was silently thrown away. For
each confirmed finding, ask how to proceed: fix it now, accept as-is with a
stated reason, or hold off publishing this plugin entirely. Do not proceed
past this gate without an explicit answer per confirmed finding.

## Step 5 — Verdict
- **PASS**: zero confirmed findings remain unresolved (all fixed or
  explicitly accepted). Report PASS and the plugin(s) it covers.
- **FAIL**: any confirmed finding is still open. Report FAIL, list what's
  still open, and state plainly that `refresh-plugins` must not tag or push
  this plugin until it passes.

## Integration with refresh-plugins
`refresh-plugins`' publish cycle calls this skill as its mandatory first step
for any plugin with changes in scope, and refuses to version-bump, tag, or
push on anything short of PASS. This skill can also be run standalone at any
point during drafting, before you're ready to publish, to check
work-in-progress early.

## Rules
- **Read-only.** This skill and every agent in its team only reads and
  reports. Fixing findings is a separate, explicit step by the main agent or
  Sara, never automatic.
- **No findings content in the repo.** Scanner output goes to the scratchpad,
  never to a tracked file. A findings file that named a real secret or a real
  other-project name must never itself become something `git add -A` would
  pick up.
- **Nothing silently dismissed.** Every finding — confirmed or refuted — is
  shown at the human gate. Refutation is visible reasoning, not deletion.
- **Re-run after fixing.** A "fix it now" resolution isn't done until this
  skill is re-run on the affected plugin and comes back PASS.
