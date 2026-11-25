---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill.
---

# Writing Skills

A skill exists to make a stochastic agent **predictable**: the same *process* every run, not the same output. Every lever below serves that.

## Process

1. **Gather requirements** - ask the user:
   - What task/domain does the skill cover?
   - What use cases (branches) should it handle?
   - Does it need executable scripts, or just instructions?
   - Any reference material to bundle?
2. **Decide invocation** (section 1) before drafting.
3. **Draft** - SKILL.md plus any bundled reference files or scripts.
4. **Review with user** - present the draft and ask: Does this cover your use cases? Anything missing or unclear? Should any section be more/less detailed?

## 0. Where it goes on disk

**`.agents/skills/` is the source of truth. Never write a skill into `.claude/skills/` directly.** Three agents read these roots and only one reads `.claude`: Claude Code reads `~/.claude/skills`, while Codex, the ChatGPT app, and **Zed read only `~/.agents/skills`** (Zed's scan is flat, one level, and never looks at `.claude`). A skill authored into `.claude` alone is invisible to two of the three.

| Kind | Create at | Then |
|---|---|---|
| Global, throwaway or machine-local | `~/.agents/skills/<name>/SKILL.md` | `ln -s ../../.agents/skills/<name> ~/.claude/skills/<name>` |
| Global, kept in git (the usual case) | `~/dotfiles/.claude/skills/<name>/SKILL.md` | `bash ~/dotfiles/scripts/skills/link-dotfiles-skills.sh` (links into `~/.agents`, then mirrors to `~/.claude`) |
| Project-local | `<project>/.agents/skills/<name>/SKILL.md` | `ln -s ../../.agents/skills/<name> <project>/.claude/skills/<name>` |

The dotfiles repo keeps authored skills under its own `.claude/skills/` because that is the stow-managed authoring home; the link script is what makes `~/.agents` canonical at runtime. Never hand-create an entry in `~/.claude/skills/`: `check-skill-integrity.sh` fails on any entry there that is not a symlink to `../../.agents/skills/<name>`.

**Do not vendor a skill that `skill-lock.json` already installs.** The installed copy wins in every agent and the committed one becomes dead code. The pre-commit hook rejects this.

Constraints worth honoring so the skill loads everywhere, not just in Claude Code (Zed enforces these strictly and drops the skill outright on a violation):

- `name`: `[a-z0-9-]` only, 1-64 chars, no leading or trailing hyphen, and matching the directory name.
- `description`: non-empty, and keep it under 1024 bytes. Every skill's `name + description` shares a fixed 50KB catalog budget; past it, skills are dropped by path order, not by size.
- Only `name`, `description`, and `disable-model-invocation` are portable. `allowed-tools`, `user-invocable`, and `argument-hint` are silently ignored outside Claude Code, so never rely on them for correctness.

## 1. Trigger: who invokes it

Any skill can be invoked by name. The real choice is whether the *agent* can also fire it on its own.

- **Model-invoked** (the default): keep the `description`; it sits in the agent's context every turn, so the agent can trigger it autonomously and other skills can reach it. Cost: **context load** (tokens and attention on every request) plus unpredictability (the agent may simply not call it).
- **User-invoked**: set `disable-model-invocation: true`; the description becomes human-facing and the agent cannot see or fire it. Zero context load, but it spends **cognitive load**: you become the index that has to remember it exists.

Rule: pick model-invocation only when the agent must reach the skill itself (or another skill must). If it only ever fires by hand, make it user-invoked and pay no context load. When user-invoked skills pile up past what you can remember, add a **router skill** that names the rest and when to reach for each.

## 2. Structure: steps and reference

Two content units, mixed freely (a skill can be all steps, all reference, or both):

- **Steps**: the ordered procedure the agent walks.
- **Reference**: facts, rules, templates, examples it consults on demand.

Keep `SKILL.md` as small as possible: easier to maintain and audit, and every word shaved is a token shaved on every call.

**Branches drive disclosure.** A branch is a distinct way the skill gets used; different runs take different paths. Inline what *every* branch needs; push branch-specific reference behind a **context pointer** (a link the agent follows only when needed) into a separate file in the skill folder. Example: a one-branch skill that always writes a PRD keeps its template inline; a skill that *sometimes* writes an ADR points to the ADR template externally so the unused branch costs nothing.

A pointer's *wording*, not its target, decides whether the agent follows it. A must-have file behind a weak pointer is a variance bug: sharpen the wording first, inline only if that fails.

## 3. Steering: leading words and legwork

**Leading words** are the main lever. A leading word is a compact phrase already loaded with meaning in the model's pretraining ("vertical slice", "tracer bullet", "fog of war"). Drop it in the skill text and the agent echoes it in its reasoning and output, which steers behavior in the fewest tokens. Prefer pretrained words over coined ones (a made-up word recruits no priors, so you pay in definition tokens). Repeat the *word*, never the explanation.

**Legwork** is how much digging the agent does inside a step (reading code, exploring, asking). Agents skimp on it when they can see the end goal and rush ahead. Two fixes:

- Tighten the **completion criterion** so done/not-done is checkable and, where it matters, exhaustive ("every modified model accounted for", not "list some changes").
- **Split steps** into separate skills or phases so the agent sees one step at a time and cannot rush toward later ones (for example, split a "grill the user" phase from the "write the doc" phase).

## 4. Pruning: cut to the bone

Once the skill works, shrink it. Watch for these failure modes:

- **Duplication**: the same meaning in two places. Enforce a **single source of truth** so changing the behavior is a one-place edit.
- **Sediment**: stale layers that pile up because adding feels safe and deleting feels risky. Cut them.
- **Sprawl**: simply too long, even when every line is live and unique. Cure with the structure levers (disclose reference, split by branch).
- **No-op**: a line the model already obeys by default, so you pay tokens to say nothing. Apply the **deletion test** per sentence: if removing it changes nothing, delete the whole sentence. A weak leading word ("be thorough" when the agent already is) is a no-op; the fix is a stronger word ("relentless"), not more words.

## Skill Structure

```
skill-name/
├── SKILL.md           # Main instructions (required)
├── REFERENCE.md       # Branch-specific reference behind a context pointer (if needed)
├── EXAMPLES.md        # Usage examples (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## SKILL.md Template

```md
---
name: skill-name
description: Brief description of capability. Use when [specific triggers].
# disable-model-invocation: true   # add this for a user-invoked skill
---

# Skill Name

[Steps and/or reference. Inline what every branch needs;
 point to separate files for what only some branches reach.]
```

## Writing the description

The description is **the only thing your agent sees** when deciding which skill to load. It is surfaced in the system prompt alongside every other installed skill, and the agent picks based on it.

**Goal**: give the agent just enough to know (1) what capability this provides and (2) when/why to trigger it (specific keywords, contexts, file types).

**Format**:

- Max 1024 chars
- Write in third person
- First sentence: what it does
- Second sentence: "Use when [specific triggers]"
- Front-load the **leading word** you actually use when you want this skill; the description is where it does its invocation work
- One trigger per branch (synonyms that rename one branch are duplication; collapse them)

**Good example**:

```
Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.
```

**Bad example**:

```
Helps with documents.
```

The bad example gives your agent no way to distinguish this from other document skills.

## When to Add Scripts

Add utility scripts when:

- The operation is deterministic (validation, formatting)
- The same code would be generated repeatedly
- Errors need explicit handling

Scripts save tokens and improve reliability versus generated code.

## Review Checklist

After drafting, verify:

- [ ] Invocation chosen on purpose (model- vs user-invoked), not by default
- [ ] Description includes triggers ("Use when...") and front-loads the leading word
- [ ] SKILL.md inlines only what every branch needs; branch-specific reference is disclosed
- [ ] Steering present where it matters: leading words, checkable completion criteria
- [ ] No duplication (single source of truth), no sediment, no no-ops (deletion test passes)
- [ ] No time-sensitive info; consistent terminology; concrete examples; references one level deep

---

*Framework adapted from Matt Pocock's `writing-great-skills` (mattpocock/skills): predictability, invocation loads, branch-based disclosure, leading words, legwork, and named failure modes.*
