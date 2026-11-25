---
name: uic-writing
description: Writes and edits this plugin's skills and documents to Anthropic's skill authoring practices, then finds and fixes the stale references and contradictions the edit left. Use when changing a skill, the session text, USING.md, README.md, .claude/CLAUDE.md, AGENTS.md, CONTRIBUTING.md, docs/ or .claude/rules/ in this repository.
paths:
  - skills/**
  - hooks/session-context.md
  - USING.md
  - README.md
  - .claude/CLAUDE.md
  - AGENTS.md
  - CONTRIBUTING.md
  - docs/**
  - .claude/rules/**
  - .claude/skills/**
---

# Writing the plugin

## Overview

The plugin is Markdown an agent acts on. Judge a change by one thing — whether the plugin gets more effective: fewer words for the agent to carry, clearer steps, better results on real projects.

## While writing

Anthropic's skill authoring guide (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices), applied here.

**What goes in**

- Only what the model does not already know: an instruction, a definition, a template or an example.
- Remove an instruction the current models follow without being told: one written for an earlier model is often too prescriptive for a newer one (the model pages of the prompting guide, https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).
- When a change adds a line to a skill, remove what that line makes unnecessary in the same skill.
- Keep the session text, `hooks/session-context.md`, as short as what it must say allows: every session pays for it before any work starts.
- No story of an earlier run, no history of the plugin, no argument for its design, no maxim.
- Keep a clause of why where it changes a judgment.
- Keep a concrete failure where it shows a rule nobody would guess.
- Earlier issues, commits and decisions are not arguments for or against a change; how the plugin behaves now is.

**How a line is written**

- One instruction to a line, in the imperative: what to do, not how it was arrived at.
- Say what to do, rather than only what not to do.
- Name the scope a rule covers — *every page*, *each line of the checklist* — where it holds beyond the item in front of it: the current models read an instruction literally and do not carry it to the next item.
- Write what holds through a task as a standing instruction — *re-read the checklist before every page*, not *re-read the checklist*: Claude Code does not load a skill again on later turns (https://code.claude.com/docs/en/skills, *Skill content lifecycle*).
- Write an exception as its own line, its condition first — *If …, …* — never as a clause inside the rule it limits.
- Fix a line that reads two ways by rewriting it, and two lines that disagree by rewriting the pair, rather than by adding a clause beside them.
- Ask for what was done and what settled it, never for the reasoning written out: the current models may decline a request to write out their reasoning (the Fable 5.1 and Opus 5 pages of the prompting guide).
- Have a check note every finding, the uncertain ones included, and filter in a step of its own: a check told to report only what matters finds less (the Sonnet 5 and Opus 4.8 pages).

**A `SKILL.md`**

- Frontmatter, title, `## Overview` in one or two sentences, then the steps in order.
- Under 500 lines, as the authoring guide asks.
- As short as what it asks allows, with no number of characters to meet: every word is paid for each time the skill loads, and after compaction Claude Code re-attaches only the beginning of each invoked skill, within a budget they share, past which the oldest is dropped whole (https://code.claude.com/docs/en/skills, *Skill content lifecycle*).
- Put the instructions that matter most near the top: the beginning is what compaction keeps.
- Keep in it what every run of the skill needs.
- Move what only one case of the work needs to a reference file, linked from that case's step: the file costs nothing until that step opens it.

**A reference file**

- Title, then one line `**Read when:** …`, then `## Contents` when it runs over 100 lines.
- One case to a file, named for it: a step opens only the case it meets (the authoring guide, *Domain-specific organization*).
- Keep the files flat in the skill's folder: `scripts/check-skills.sh` reads no subfolder.
- Link it with its title — `[*A position no member has*](position-no-member-has.md)` — so a case another skill names is found in the `SKILL.md`.
- Link it directly from the `SKILL.md` of its own skill that needs it, never only from another reference file. Another skill that needs it gives its path, below.

**A description**

- Say what the skill does, then *Use when …* with the words a request uses.
- Do not summarise the steps.
- Third person, at most 1,024 characters, no XML tags.
- A shipped skill's description says in its first words that the work is what an end user sees.

**Terms and rules**

- One term per meaning. In a shipped skill, use the plugin's own terms as `skills/finding-patterns/words.md` defines them; a word a model already knows is not defined there.
- Say a rule once inside a skill, where it is first needed, and link it everywhere else in that skill.
- Keep a rule repeated across skills: each skill can be loaded alone.
- Name another skill for the agent to invoke as `ui-consistency:<name>`, with the section. Reach `values`, `conventions` and `decisions` only that way, their own files included: an invoked skill is re-attached after compaction, a file read with a tool is not.
- Where a step reads a file of another skill rather than invoking the skill, write the file as its path from the skill's folder, `` `../<skill>/<file>.md` ``, never as a link: a catalog's linter fails a skill whose link leaves its folder.

## After writing

Before the change is done:

1. **Stale references.** Search for every file, section, skill, test and command the changed text names; each must still exist.
2. **Contradictions.** For every rule the change touched, search for its other copies — in other words as well as the same ones — in `skills/`, `USING.md`, `README.md`, `.claude/CLAUDE.md`, `AGENTS.md`, `CONTRIBUTING.md`, `docs/`, `.claude/rules/` and `.claude/skills/`.
   - Each copy now says the same thing, or the change is not done.
3. **Fix every stale reference and every contradiction in the same change**, and say in the pull request which copies were found.
4. **One fresh read, once — if a skill changed.** Hand a subagent with no other context the diff of the changed skill files, and those files in full as context only — with `skills/finding-patterns/words.md` if a shipped skill changed. Ask it about the **changed lines only**:
   - a changed line that can be read two ways;
   - a changed line that disagrees with any line of the full files;
   - a word a changed line uses in a sense different from its other uses in the full files — or, in a shipped skill, a term of the plugin's own that `words.md` does not define.

   Ask it to find every such line first, then to name at most five, ranked by how much each changes what an agent does. Then:

   - Fix every item that changes what an agent does. If a changed line disagrees with older wording, fix the pair, as step 2 asks.
   - Say in the pull request what was fixed and name any other item; "nothing" is a result.
   - Leave older wording that no changed line touches or contradicts: reviewing whole files is `uic-auditing`'s, which runs only when somebody asks for an audit.
   - Do the read once. Do not repeat it after the fixes, and never run the skill on a project for it.
   - If the harness has no subagents, skip it and say so.

How a wrong statement is corrected, and what may never be written publicly, is `.claude/rules/uic-docs.md`.
