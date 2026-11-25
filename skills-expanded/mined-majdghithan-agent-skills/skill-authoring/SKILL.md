---
name: skill-authoring
description: Author, structure, verify, and publish a high-quality agent skill (SKILL.md). Use whenever the user wants to "write a skill", "create a skill for X", turn expertise or a workflow into a reusable skill, improve an existing SKILL.md, or publish a skill to their repo. Covers the SKILL.md format, writing a strong description, progressive disclosure with reference files, the detect-context-first pattern, fact-verification discipline, testing, and the publish workflow.
---

# Skill authoring - write a great, publishable skill

A skill is a `SKILL.md` file (YAML frontmatter + markdown instructions) that an agent loads when its work matches. Optionally it bundles supporting files (`references/*.md`, `scripts/`) loaded on demand. Good skills are **specific, accurate, and lean**. This skill is how to write one.

## 1. Decide it should exist

Write a skill when there's real, reusable know-how an agent would otherwise get wrong or generic: a framework's version-specific rules, a migration's gotchas, a self-hosting workflow, a house style. **Don't** write one for a one-off task, or for something the model already does well. Check the ecosystem first (`npx skills find <topic>`) - if a great one exists, install it instead; if only generic ones exist, that's your gap.

## 2. Frontmatter - name + description (the description is critical)

```yaml
---
name: kebab-case-name          # matches the folder name
description: <what it does> + <when to use it> + <trigger phrases> + <when NOT to use>
---
```
The **description is how the agent decides to activate the skill** - spend real effort on it. Pack it with concrete trigger phrases the user might say, the situations it covers, and an explicit "use when… / do not use for…" boundary. A vague description means the skill never fires (or fires wrongly).

## 3. Structure - lean SKILL.md, detail in references (progressive disclosure)

- **Keep SKILL.md short and scannable.** It's loaded every time the skill activates - don't bloat the context. Put the always-true guidance here; push deep or bulky detail into `references/<topic>.md` that the agent reads only when needed.
- **When the topic has variants (versions, dialects, platforms), lead with a "detect first" step**, then route to the matching reference. Example: a framework skill opens by reading `composer.json`/`package.json` to find the installed major version, then loads `references/<name>-vN.md`. This is what keeps a skill correct as the tool evolves.
- **Separate the stable layer from the volatile layer.** Version-independent principles live in SKILL.md; exact namespaces/signatures live in per-version references (and say "verify against the official docs for this version" rather than freezing volatile API).
- Layout for a multi-file skill:
  ```
  skills/<name>/
    SKILL.md                 # detect + route + stable principles
    references/<topic>.md     # loaded on demand
    references/upgrades/*.md   # e.g. migration/upgrade paths
  ```

## 4. Write for the agent, not a human reader

- Imperative and concise. Every line should change what the agent does. If an explanation is longer than the thing it explains, cut it.
- **Concrete, labeled code examples** beat prose. Label each example with the version/context it applies to.
- Give a short "Output expectations" section (what the agent should produce/state).
- No marketing, no filler, no restating the obvious.

## 5. Verify every fact before you write it (non-negotiable)

Skills are trusted and reused, so a wrong claim scales. **Web-verify against primary/official sources** (docs, changelogs, the framework's repo) before writing - do not rely on training memory for version numbers, API names, signatures, or dates. For a multi-part topic (e.g. 5 versions), **run parallel research agents**, one per part, each returning sourced findings, then synthesize. Cite source URLs in the reference files. Flag anything you couldn't confirm as uncertain rather than stating it confidently.

## 6. Test it

Install it and try it on a real task: `npx skills add <owner/repo> --skill <name>` (or point the agent at the local file). Confirm the description makes it activate at the right moment, the routing loads the right reference, and the guidance produces correct output. Iterate on the description first if it doesn't fire.

## 7. Publish (Majd's workflow)

Skills live in the monorepo **`majdghithan/agent-skills`** (local: `/Users/user/Desktop/Code/agent-skills`).
1. Create `skills/<name>/SKILL.md` (+ `references/` if multi-file).
2. Add a row to the repo `README.md` skills table.
3. Commit as **`Majd Ghithan <majd.ghithan20@gmail.com>`** (never the session email; no AI co-author trailer), then push:
   ```bash
   git add -A && git commit -m "Add <name> skill" && git push
   ```
4. Installable immediately: `npx skills add majdghithan/agent-skills --skill <name>`. skills.sh and claudemarketplaces.com auto-index the public repo (no submit form). To use it everywhere, install globally: add `-g`.

## Checklist
- [ ] Gap confirmed (`npx skills find` - not already well-covered)
- [ ] `name` kebab-case = folder; `description` loaded with triggers + when-to-use + when-not
- [ ] SKILL.md lean; detail in `references/`; detect-first routing if there are variants
- [ ] Stable principles separated from volatile per-version syntax
- [ ] Every factual claim web-verified against official sources; sources cited; uncertainties flagged
- [ ] Concrete, version-labeled examples
- [ ] Tested by installing and running on a real task
- [ ] Published to `majdghithan/agent-skills` (README row, correct commit identity, pushed)

## Sources
[Anthropic - Agent Skills](https://docs.anthropic.com/en/docs/agents-and-tools/agent-skills) · [skills.sh CLI](https://skills.sh)
