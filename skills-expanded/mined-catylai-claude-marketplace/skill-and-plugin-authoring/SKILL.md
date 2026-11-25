---
name: skill-and-plugin-authoring
description: "Authors Claude Code skills and plugins that trigger reliably and stay cheap to load. Use when writing, packaging, or debugging a skill or plugin, or when one never fires or fires on everything. Covers descriptions with named anti-triggers, frontmatter semantics, progressive disclosure, plugin packaging, and measuring trigger rate with claude plugin eval. Not for auditing an existing skill tree (use review-skills); not for MCP wiring (use mcp-integration); not for subagent design (use agent-orchestration)."
when_to_use: "write a skill, SKILL.md frontmatter, skill never triggers, skill triggers too often, package a plugin, plugin.json, marketplace.json, skill description"
license: MIT
---

# Skill and plugin authoring

Claude decides whether to load a skill almost entirely from its `description`, read against a
listing that may hold a hundred or more skills. Write for that decision first and the body
second. Measure before you write at length: build a few should-trigger and should-not-trigger
prompts before the body grows, so you can tell whether each addition helped.

## 1. Write the description as a router entry

- **Third person, what plus when.** "Extracts tables from PDFs. Use when…", not "I can help…".
  The description is injected into the system prompt, so a shifting point of view hurts discovery.
- **Put the trigger early.** Each entry's `description` plus `when_to_use` is capped at 1,536
  characters. The whole listing also has a budget (by default a small share of the context window,
  adjustable with `skillListingBudgetFraction`). When the listing overflows, the least-invoked
  skills lose their descriptions first. A description that only works in full stops working under
  budget pressure.
- **Name the anti-triggers and their owners.** "Not for X (use sibling-skill)." That way the
  listing routes a request to one skill instead of several skills competing for it.
  Over-triggering does as much damage as under-triggering, because it spends the body's tokens on
  turns that did not need them.
- **Put user phrasings in `when_to_use`.** It is appended to the description in the listing. It is
  wasted on a skill with `disable-model-invocation: true`, because that skill's description is not
  in context at all.
- **Name the skill after its job.** Gerund (`processing-pdfs`) or noun phrase, used consistently
  across the collection. Avoid `helper`, `utils`, `data` and `files`. The name cannot contain
  "claude" or "anthropic".

<example>
```yaml
name: reconciling-bank-statements
description: >
  Reconciles a bank statement against general-ledger entries and produces a signed-off
  workpaper. Use when the user mentions bank rec, statement reconciliation, unreconciled items,
  or clearing a suspense account. Not for GL-to-subledger reconciliation (use
  reconciling-subledgers) or journal entries (use preparing-journal-entries).
```
</example>

<example>
A description that fails:

```yaml
description: Utilities for documents and data.
```

It matches nearly every request, names no word a user would type, and names no neighbour, so the
skill either never fires or fires constantly.
</example>

## 2. Know what each frontmatter field does

Claude Code accepts a superset of the portable Agent Skills fields. The fields that change
behaviour most, and are most often misread:

- **`allowed-tools` pre-approves; it does not restrict.** The tools listed run without a
  permission prompt during the turn that invokes the skill. To take tools away, use
  `disallowed-tools`.
- **`disable-model-invocation: true`** means only `/name` loads the skill.
- **`user-invocable: false`** means only Claude can load it.
- **`paths`** limits auto-activation to matching files.
- **`context: fork`** runs the body as an isolated subagent task. It suits a self-contained job
  that returns a result, not reference guidance.

The full field table, the substitution variables (`$ARGUMENTS`, `${CLAUDE_SKILL_DIR}` and others)
and the name-resolution rules are in
[references/frontmatter.md](references/frontmatter.md).

Two things to watch outside Claude Code:

- **Portability.** Skills uploaded to claude.ai or through the API are documented as requiring only
  `name` and `description`, within the same limits. Upload surfaces may reject keys that only
  Claude Code understands, so test an upload before shipping a Claude Code-only key.
- **Where skills load.** Cowork and cloud sessions do not read `~/.claude/skills/`. Skills synced
  from claude.ai do not expand `${CLAUDE_*}` and do not run `!` shell injection on the client. For
  a skill meant for the web, leave out `!` injection, and make any file-reading step also work from
  pasted content.

## 3. Keep the body short and the important rules first

| Level | Loaded | Content |
| --- | --- | --- |
| 1: Metadata | Always | Name and description (roughly 100 tokens) |
| 2: Instructions | When triggered | The SKILL.md body (aim for under 5k tokens) |
| 3: Resources | When read or run | Reference files and scripts |

- **Keep the body under 500 lines** and move detail into `references/`, linked **one level deep**
  from SKILL.md with a one-line note on what each file holds and when to read it. A file linked
  only from another reference file may be read partially, for example just its first 100 lines.
  Any reference over 100 lines opens with a table of contents.
- **Put rules that override the references first.** After auto-compaction, Claude Code re-attaches
  only the first 5,000 tokens of each invoked skill, within a shared budget, so the tail of a long
  body is what gets lost.
- **Say whether each script is run or read.** For example, "Run
  `python "${CLAUDE_SKILL_DIR}/scripts/parse.py" <file>`" versus "See `scripts/parse.py` for the
  algorithm". A script that is run costs only its output. Scripts should handle their own errors
  rather than leave Claude to guess.
- **Name MCP tools in full.** In Claude Code, refer to MCP tools by their full name,
  `mcp__<server>__<tool>`.

## 4. Choose skill, hook, or subagent deliberately

- **Hook**: it has to happen the same way every time, with no judgement involved.
- **Skill**: Claude should decide whether and how to apply it, or it is knowledge rather than an
  action.
- **Subagent**: it needs an isolated context window and returns a summary.

A skill that says "always do X before Y" for something with financial or security consequences is
a hook in disguise, and it will fail some fraction of the time. See deterministic-enforcement.

## 5. Package the plugin

Everything below except the first point is covered in detail, with examples, in
[references/plugin-packaging.md](references/plugin-packaging.md).

- `.claude-plugin/plugin.json` is the only file in `.claude-plugin/`. Components sit at the
  plugin root.
- A root `SKILL.md` is loaded only when the plugin has no `skills/` directory and no `skills`
  field. Otherwise it is ignored.
- `author` is an object and `keywords` is an array. A wrong type on a recognized field fails the
  load.
- **Versioning.** A plugin with a `version` set only updates for users when you bump it. Leave
  `version` out to have every new commit update users, which suits internal plugins.
- **Paths and secrets.** Reference bundled files through `${CLAUDE_PLUGIN_ROOT}`, and quote it in
  shell-form commands. Keep persistent state in `${CLAUDE_PLUGIN_DATA}`. Ask for secrets through
  `userConfig` with `sensitive: true`.
- **Naming.** Plugin skills are invoked as `/<plugin>:<skill>`, and plugin agents are referred to as
  `<plugin>:<agent>`.

## 6. Measure triggering and benefit

- **`claude plugin eval`** runs each case in isolated sessions with and without the plugin, several
  times per case. It reports the with-plugin and without-plugin scores and their difference, and
  can gate CI on a threshold. A `tool_used: Skill` grader measures whether the skill fired on
  natural phrasing. `claude plugin eval init` drafts the cases for you.
- **Anthropic's skill-creator plugin** iterates on a single skill: it generates should-trigger and
  should-not-trigger prompts, measures the hit rate, and proposes description edits.

Rules for trusting a number:

- Triggering is stochastic, so treat the result as a rate and never as a single pass or fail.
- Include negative cases. A suite with none cannot detect over-triggering.
- A high score with a zero difference means the plugin did not cause the pass.

## 7. Diagnose

- **The skill works when invoked by name but never triggers on its own.** The frontmatter probably
  failed to parse. The body then loads with empty metadata, so `/name` works but Claude never sees a
  description. Run with `--debug` to see the YAML error.
- `claude plugin validate --strict` catches manifest and frontmatter errors, and in strict mode
  unknown fields become errors.
- `/skill-doctor` shows each skill's context cost and how often it is used. `/doctor` and the Skills
  row in `/context` show the listing's total cost.
- For a fast local loop, run `claude --plugin-dir ./my-plugin`, and pick up edits with
  `/reload-plugins`.

For a full audit of an existing skill tree, use review-skills. The checks that catch the most:

- The opening `---` is the first line of the file.
- The description is third person, has "Use when" early, and names the owner of each anti-trigger.
- The body is under 500 lines, and every reference is linked directly from SKILL.md.
- Scripts are marked as run or read, and no skill is really a hook in disguise.
- `claude plugin validate --strict` passes.

Notes on applying this outside Claude Code are in
[references/porting.md](references/porting.md).

## Verify

After any change to a skill or plugin:

1. Run `claude plugin validate --strict <plugin-dir>` (or the repo's own validate script). It
   passes.
2. Run `claude plugin eval <plugin-dir>` with at least two should-trigger and two
   should-not-trigger cases per changed skill. Trigger rate is up, false triggers are flat or down,
   and the difference between with-plugin and without-plugin runs is positive.
3. Start a fresh session with `--plugin-dir` and confirm the skill appears in `/` and loads on a
   natural phrasing.

If `claude plugin eval` is unavailable in your build, run the prompts by hand in fresh sessions,
with the skill enabled and then disabled, and report the counts. Without a checkout: review the
SKILL.md or manifest the user pastes, and list the commands they still need to run.
