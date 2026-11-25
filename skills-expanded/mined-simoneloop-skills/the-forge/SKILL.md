---
name: the-forge
description: >-
  Scaffold a new Claude Code skill in this repository following its conventions.
  Use when the user wants to create or add a new skill, start a SKILL.md, bootstrap
  a skill folder, or contribute a skill to this marketplace. Generates the skill
  directory and a SKILL.md from the template, helps write a trigger-optimized
  description, adds the catalog row in README, and validates the result.
---

# Skill Creator

Bootstraps a new skill inside this repo so it matches the project's conventions
and passes validation on the first try.

## When to use
The user says something like "add a skill that…", "create a new skill",
"scaffold a SKILL.md", or "I want to contribute a skill here".

## Steps

1. **Clarify the skill.** Ask for (or infer), in this order:
   - The **purpose**: what it does and — crucially — **when it should trigger**
     (the concrete situations/phrases). This drives the `description`. Nail this
     FIRST — the name is derived from it.
   - The **name**. From the purpose/goal, **invent 3-5 evocative names** in the
     spirit of superpowers or special-move names (e.g. `shadow-clone`, `kamehameha`,
     `falcon-punch`, `mind-meld`) and propose them for the user to pick from. Lean
     on the skill's domain for the metaphor (cleanup → `spring-clean`/`purge`;
     search → `all-seeing-eye`; scaffolding → `genesis`). Each candidate MUST still
     be valid kebab-case (`[a-z0-9-]+`), since it becomes the folder name, the `name`
     frontmatter, AND the invoke command `/loop-skills:<name>`. Always also offer a
     plain functional fallback (gerund form, e.g. `reviewing-prs`) for when the user
     prefers a literal name, and let them request a fresh batch. Because discovery is
     driven by the `description` (not the name), a fanciful name does NOT hurt
     auto-triggering — but keep the catalog row's one-line description crystal-clear
     so the skill stays findable.
   - Whether it needs `references/` (long docs) and/or `scripts/` (helper code).
   - **Prerequisites & secrets** — which CLIs/tools the skill calls (e.g. `gh`,
     `jq`, `trufflehog`) and which credentials / env-var keys it needs (e.g.
     `GITHUB_TOKEN`). These drive the skill's own **Setup** section, so it can
     self-guide its setup on first run. Detect these from the skill's purpose;
     don't make the user configure things a *different* skill needs.

2. **Research prior art on the web (required).** Before writing anything, search
   the web for existing skills/tools/approaches that solve the same problem —
   Anthropic's official skills (`anthropics/skills`), community plugin
   marketplaces, `awesome-claude-*` lists, and comparable non-Claude tools. Use
   `WebSearch`/`WebFetch`. Then report to the user a short synthesis covering:
   - **Gaps** — capabilities the existing solutions miss that this skill should cover.
   - **Better approach** — proven patterns worth adopting instead of reinventing.
   - **Novelty / quality / rarity** — how common or valuable this idea is, and an
     honest recommendation: build it, build a differentiated version, or just point
     the user at an existing solution (and skip creating a near-duplicate).
   Let the user steer based on this before scaffolding. Capture the prior-art
   summary so it can go into the PR description (see [SCOPE.md](../../../../SCOPE.md)).

3. **Create the folder** under the plugin:
   `plugins/loop-skills/skills/<name>/`

4. **Generate `SKILL.md`** from the template at
   `${CLAUDE_SKILL_DIR}/assets/SKILL.template.md`. Replace the placeholders:
   - `{{SKILL_NAME}}` → the kebab-case name
   - `{{DESCRIPTION}}` → a description that states **what it does AND when to use
     it**, leading with the key use case and naming trigger phrases (this is the
     ONLY discovery signal — be specific, even "pushy").
   - `{{BODY}}` → the standing instructions (keep the whole file < 500 lines).
   - The **`## Setup (run first)`** section — fill `{{REQUIRED_TOOLS}}`,
     `{{REQUIRED_KEYS}}`, and `{{ENV_KEY}}` from the prerequisites identified in
     step 1, so the skill checks its tools/tokens and guides the user (secrets →
     `.claude/settings.local.json`) **as its first action** on every run. If the
     skill needs no tools or keys, delete the Setup section.
   Add `references/` and `scripts/` subfolders only if needed; reference bundled
   files with markdown links and `${CLAUDE_SKILL_DIR}/...`.

5. **Update the marketplace listing (always do this at the end).** A new skill must
   be discoverable:
   - Add a row to the **Skill catalog** table in `README.md` (name, one-line
     description, invoke command `/loop-skills:<name>`).
   - Refresh the plugin's `keywords`/`description` in
     `plugins/loop-skills/.claude-plugin/plugin.json` **and** the plugin entry in
     `.claude-plugin/marketplace.json` if the new skill adds a notable capability,
     so search/discovery reflect it.
   - Note: in this repo all skills live in the single `loop-skills` plugin, so
     `marketplace.json` lists **plugins, not skills** — it does NOT get a new entry
     per skill. Updating the catalog + keywords IS the marketplace update. (Only if
     you ever split a skill into its own separate plugin would you add a new
     `plugins[]` entry here.)

6. **Validate** before finishing:
   ```bash
   bash scripts/validate-skills.sh     # structure + manifests (no auth)
   claude plugin validate .            # official validator (if CLI available)
   ```
   Fix any error the linter reports (missing `name`/`description`, non-kebab-case
   folder, invalid manifest). Warnings (e.g. missing `version`) are acceptable.

7. **Tell the user how to load it**: from a local install, `/reload-plugins`
   picks up the new skill; from a GitHub install, push then
   `/plugin marketplace update`.

## Conventions to enforce
- kebab-case names (fanciful superpower / special-move names encouraged, still
  `[a-z0-9-]+`); one folder per skill; folder name == `name`.
- Lean `SKILL.md`; detail in `references/`, code in `scripts/`.
- No `version` in manifests (ship by commit SHA).
- See [CONTRIBUTING.md](../../../../CONTRIBUTING.md) for the full contributor flow.
