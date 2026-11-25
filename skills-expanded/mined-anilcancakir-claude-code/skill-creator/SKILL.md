---
name: skill-creator
description: "Create or audit a Claude Code skill or slash workflow."
when_to_use: "Use when writing, editing or debugging a skill or a /command, or turning a procedure you keep retyping into one."
disable-model-invocation: false
---

# Skill Creator

You are about to write or edit a skill another Claude will load. A skill is a directory with a `SKILL.md`: the frontmatter decides whether and how it loads, the body is a prompt that enters the conversation when it fires and stays for the rest of the session. User-typed slash workflows (`/deploy`, `/commit`) are skills too; custom commands were merged into skills, so this skill covers both.

The body of every skill you produce is a prompt: route that work through `ac:prompt-writer` instead of restating prompt principles here. This file owns the shape: scope, frontmatter, invocation, layout, bundling.

## Rules that hold for every skill

1. **Concise is the contract.** The body shares the context window with everything else. Add only what Claude would not know without you; each paragraph must justify its tokens.
2. **The listing decides.** The model picks a skill from `description` plus `when_to_use` alone. Imperative verb and object, one "Use when" sentence, about 200 characters combined, no mechanics.
3. **Minimal frontmatter.** `description` and `when_to_use` cover most skills. Add another field only when you can name the condition that needs it.
4. **Rules first, depth in references.** After compaction only the first 5,000 tokens of an invoked skill are kept, so standing rules go at the top and detail moves to one-level-deep `references/` files, each anchored with "read this when X".
5. **Standing instructions.** The body is read once and stays: write rules that hold for the session, not "for this turn".
6. **Scope in both directions.** Say where a rule spans and what the skill does not touch; current models widen scope on their own.
7. **Plain wording.** No "CRITICAL" or "you MUST"; state the rule once with its reason.
8. **Portable paths.** Reference bundled files through the skill-directory token, never a repo-relative path.

## Decision flow

```
Is a skill the right tool?
├── A fact that never changes → CLAUDE.md or a rule, via `ac:claude-md-rules-creator`.
├── A why-and-scope or architecture document → `ac:project-md-writer` or `ac:architecture-md-writer`.
├── Must happen deterministically → a hook, via `update-config`.
├── Needs its own context, tools or model → a subagent, via `ac:agent-creator`.
├── A one-off task → just do it.
└── A recurring procedure, playbook or body of knowledge → a skill. Continue.

Does the user type it as `/name [args]`, does it take arguments, gather live state, or have side effects?
├── YES → this file for shape, plus `${CLAUDE_SKILL_DIR}/references/user-typed-skills.md`
│         (arguments, shell injection, phases, approval gates, commands as the older format).
└── NO  → this file alone.

Auditing or fixing an existing skill?
├── YES → `${CLAUDE_SKILL_DIR}/references/anti-patterns.md`, then `claude-code-mechanics.md` if behaviour is unclear.
└── NO  → walk the Workflow below.
```

## Where skills live

- Managed: the enterprise managed directory; the whole org, highest precedence.
- User: `~/.claude/skills/<name>/SKILL.md`; every project on this machine.
- Project: `.claude/skills/<name>/SKILL.md` (walks up from cwd); this repo, commit to share.
- Plugin: `<plugin>/skills/<name>/SKILL.md`; wherever the plugin is installed, as `<plugin>:<name>`.

Precedence is managed > user > project; plugin skills sit in their own namespace. A legacy `.claude/commands/<name>.md` still creates `/name`, but a same-named skill wins; prefer a skill for new work.

## Frontmatter

> **Escape convention.** This SKILL.md is preprocessed on every invocation, so a token written with a plain dollar sign would be substituted and corrupt the docs. Tokens that are named rather than used appear with `&#36;` for the dollar sign (`&#36;ARGUMENTS`); in your own skill, write a plain `$`. Shell-injection examples appear as `\!`; write a plain `!` when you mean to run it.

Every field is optional; unknown fields are ignored. Frontmatter is read only when `---` is line 1.

| Field | Semantics, and when to set it |
|-------|-------------------------------|
| `name` | Display and slash name; lowercase, digits, hyphens, at most 64 characters. Optional when it equals the directory name |
| `description` | What it does; the trigger surface. Always set |
| `when_to_use` | One "Use when" sentence, appended to `description` in the listing |
| `argument-hint` | Autocomplete text after `/name`; never reaches the model |
| `arguments` | Named positionals for `&#36;name` substitution |
| `disable-model-invocation` | `true`: only the user can run it, its description leaves the model's listing, and it cannot be preloaded into a subagent. For irreversible side effects (deploy, commit, send). Default `false` |
| `user-invocable` | `false`: hidden from the `/` menu, the model can still load it. For background knowledge nobody would type. Default `true` |
| `allowed-tools` | Pre-approves matching tool calls for the invoking turn only; never restricts |
| `disallowed-tools` | Removes tools while the skill is active; cleared on the next message |
| `context` | `fork` runs the body as a task in a subagent without the conversation history. Default inline |
| `agent` | Subagent type for `context: fork`; default and fallback `general-purpose` |
| `background` | Fork only: whether the forked run goes to the background. Default `true` |
| `paths` | Globs (gitignore syntax); the skill is listed only once a matching file is touched |
| `model` | Model for the invoking turn; `inherit` allowed. Default the session model |
| `effort` | `low`, `medium`, `high`, `xhigh`, `max`; holds for the rest of the turn. Default the session effort |
| `hooks` | Registered when the skill is invoked and kept for the rest of the session |
| `shell` | `bash` (default) or `powershell`, for shell-injection blocks |
| `metadata`, `license`, `compatibility` | Agent Skills spec fields; accepted, not acted on |

Substitutions in the body: `&#36;ARGUMENTS`, `&#36;N`, `&#36;ARGUMENTS[N]`, `&#36;name`, `&#36;{CLAUDE_SKILL_DIR}`, `&#36;{CLAUDE_SESSION_ID}`, `&#36;{CLAUDE_EFFORT}`, and in fork skills `&#36;{CLAUDE_PROJECT_DIR}` and `&#36;{CLAUDE_PLUGIN_DATA}`; plugin skills also get `&#36;{CLAUDE_PLUGIN_ROOT}`. Per-field detail, limits, examples and pitfalls: `${CLAUDE_SKILL_DIR}/references/frontmatter.md`.

## Invocation and execution

By default both the user (`/name`) and the model load a skill. A `disable-model-invocation` skill is reachable only by a user typing it, so never write "run `/name`" for the model in a plan or another skill; write "ask the user to run it".

Inline fits most skills: the body sees the conversation and the user can steer. Set `context: fork` only when the body is a bounded, actionable task that needs no steering; reference content in a fork gives a subagent guidelines and no goal. A fork has no AskUserQuestion, so a skill with approval gates stays inline. Pick `agent:` for the fork (`ac:explore` for read-only investigation, or a custom agent); built-in `Explore` and `Plan` are disabled on an `/ac:install` setup.

`allowed-tools` is friction reduction, not a boundary: list exactly the calls the body makes (`Bash(gh pr view:*)`, `Read Grep`), never bare `Bash`.

Leave `paths:` off unless the skill matters for only some files of a polyglot repo.

## Listing and compaction

- Every skill name is always listed; descriptions share a budget of 1% of the context window, and on overflow the least-invoked lose theirs first.
- `description` plus `when_to_use` is capped at 1,536 characters per entry; aim for about 200.
- After compaction each invoked skill keeps its first 5,000 tokens, within a 25,000-token budget shared by all invoked skills.
- `/reload-skills` sends only the skills that changed; `/skill-doctor` audits the installed skills.

Load order, overrides, settings and budgets: `${CLAUDE_SKILL_DIR}/references/claude-code-mechanics.md`.

## Bundled files

Detail the body points to goes in `references/<topic>.md`, code the body runs in `scripts/<name>.<ext>`, templates and other output material in `assets/<name>`.

Reference each from the body with the condition that loads it: "Read `&#36;{CLAUDE_SKILL_DIR}/references/api-schema.md` when the request touches the API." Relative paths break when the cwd differs; for plugin skills the token (the skill's own directory, not the plugin root) is the only form that survives install. Reference files are read raw, so live syntax in them is safe; a reference over 100 lines opens with a `## Contents` list.

## Workflow

### 1. Capture intent

Extract from the conversation when it shows the procedure (corrections, tool sequence, format edits); otherwise ask in short AskUserQuestion rounds: what it does, what situation loads it, the scope. Ask about forking, user-only invocation, arguments or pre-approved tools only when an answer implies the field.

**Success criterion**: you can state the skill in one sentence and name each optional field it needs, with the reason.

### 2. Sketch the directory

Plan `references/`, `scripts/` and `assets/` before writing. A step that would add 200 lines of detail becomes a reference with an anchored pointer; a script the model would rewrite every run becomes a file in `scripts/`.

### 3. Write the frontmatter

`description`: imperative verb + object, one sentence, 60 to 120 characters ("Create a git commit."). `when_to_use`: one "Use when..." sentence naming the situation, not a list of phrasings, under 150 characters. Add only the fields step 1 justified.

- At most one boundary clause, with a redirect.
- No stages, file paths or agent names. Name a flag only when the model must pass it, because `argument-hint` never reaches the model.
- A skill that does not fire gets a more exact situation, not more synonyms or caps; a trigger that must never be lost goes in CLAUDE.md.

Prefer gerund or noun-phrase names (`processing-pdfs`); avoid vague ones (`helper`, `utils`).

### 4. Write the body

Invoke `ac:prompt-writer` for the prompt itself. Skill-specific conventions: a one-paragraph overview first; a Goal with Steps and a success criterion each for workflows, a Scope and rules for reference content; under 500 lines, with detail moved out to references rather than compressed into longer lines (the compaction window is measured in tokens). User-typed workflows add argument design, shell-injected context, phases and approval gates: `${CLAUDE_SKILL_DIR}/references/user-typed-skills.md`.

The shell-injection preprocessor scans raw bytes and ignores markdown fences: a documentation example written as `` \!`gh pr view` `` with a plain bang runs on every invocation. Escape the bang when documenting; use a plain `!` only when you mean it.

### 5. Verify

1. Frontmatter parses: `---` on line 1, quoted strings where they contain colons, no invented fields.
2. Every `&#36;{CLAUDE_SKILL_DIR}/...` path in the body exists.
3. The trigger surface would load on a relevant request and stay out of a neighbouring one.
4. The body holds up for a reader who has never seen the conversation.
5. A fresh-session invocation behaves as intended; for a typed workflow, run `/name` with typical arguments.

Examples: `${CLAUDE_SKILL_DIR}/references/examples.md`.

### 6. Iterate

When the skill does not trigger, triggers on unrelated work, loads but changes nothing, stops influencing mid-session, repeats setup every run, or renders a literal `&#36;ARGUMENTS` or an unexpected command, read the symptom-to-fix table and the failure catalogue in `${CLAUDE_SKILL_DIR}/references/anti-patterns.md`.

## Model notes

A skill body runs on the session model, usually Opus 5.5 or Sonnet 5.5. Both land on Claude Code's lean prompt, which lacks the classic code-style rules, so a skill that needs one states it. Set `effort:` only when the work needs a different level from the session's; Haiku 4.5 takes none. Per-model tuning lives in `ac:prompt-writer`.

## Sibling skills

Invoke the sibling for its shape and keep this skill loaded for what is still skill-shaped.

- The prompt body inside any skill: `ac:prompt-writer`; this skill keeps the structure around it.
- A subagent definition: `ac:agent-creator`; this skill decides whether a skill or a `context: fork` skill fits instead.
- CLAUDE.md or `.claude/rules/<topic>.md`: `ac:claude-md-rules-creator`; this skill decides procedure (skill) versus standing fact.
- PROJECT.md, ARCHITECTURE.md or DESIGN.md: `ac:project-md-writer`, `ac:architecture-md-writer`, `ac:design-md-writer`; this skill decides procedure (skill) versus fact (design document).
- Hook configuration: `update-config`; this skill decides determinism (hook) versus judgment (skill).

## Pre-flight checklist

- [ ] Right scope; directory name is the slug.
- [ ] `description` opens with a verb, `when_to_use` is one "Use when" sentence, about 200 characters combined, no mechanics.
- [ ] Every optional field has a named reason; none copied from a template.
- [ ] (`disable-model-invocation: true`) the skill has side effects, and nothing tells the model to run it.
- [ ] (`context: fork`) the body is a bounded actionable task with no approval gates.
- [ ] (`allowed-tools`) narrow patterns matching the calls the body makes.
- [ ] (`paths`) the skill is genuinely path-conditional.
- [ ] (Typed workflow) the `user-typed-skills.md` pre-flight additions pass.
- [ ] Body under 500 lines, standing rules in the first 5,000 tokens, bundled files via the skill-directory token.
- [ ] Body passes the `ac:prompt-writer` audit.
- [ ] A fresh-session invocation passes.

## References

| File | Load when... |
|---|---|
| `${CLAUDE_SKILL_DIR}/references/frontmatter.md` | Designing or auditing frontmatter: every field, values, examples, parsing pitfalls. |
| `${CLAUDE_SKILL_DIR}/references/user-typed-skills.md` | A `/name [args]` workflow: arguments, shell-injected context, phases, approval gates, commands as the older format. |
| `${CLAUDE_SKILL_DIR}/references/patterns.md` | Reference vs task content, inline vs fork, scripts, progressive disclosure, conditional activation, hooks. |
| `${CLAUDE_SKILL_DIR}/references/claude-code-mechanics.md` | Runtime lifecycle: discovery, listing budget, compaction, substitutions, permissions, precedence. |
| `${CLAUDE_SKILL_DIR}/references/examples.md` | Copying from a worked example: reference, manual-action, forked, scripted, path-conditional, plugin-distributed. |
| `${CLAUDE_SKILL_DIR}/references/anti-patterns.md` | Diagnosing a misbehaving skill or auditing one before shipping. |
| `${CLAUDE_SKILL_DIR}/references/opus-5-tuning.md` | Effort, verbosity and model overrides for a skill, per model. |
| `${CLAUDE_SKILL_DIR}/assets/SKILL.template.md` | Starting from a blank annotated template. |

Sibling skills are reached by invocation (`/ac:prompt-writer`), not by path, because the install layout is unknown at author time.

Canonical documentation (raw markdown): `https://code.claude.com/docs/en/{skills,sub-agents,hooks,plugins-reference}.md`; Agent Skills standard `https://agentskills.io/specification`. If docs and the live binary disagree, trust the binary.
