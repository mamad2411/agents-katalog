---
name: dm-skill-creator
description: Create new team-wide skills inside the darkmatter/skills repo following its conventions (skills/<name>/SKILL.md, no external deps, self-contained, validated by scripts/validate-skill.sh, registered in docs/catalog.md, distributed via the flake's home-manager module). Triggers when the user asks to "add a skill", "create a skill", "promote this into a skill", "make a darkmatter skill", or wants to generalize a workflow used across multiple darkmatter projects into the shared catalog. Also triggers when editing or refactoring an existing skill in this repo. Do NOT trigger for personal/project-local skills (those live elsewhere) or for skills outside the darkmatter/skills catalog.
---

# Darkmatter skill creator

Create skills that ship in `darkmatter/skills/skills/` and are auto-installed via the repo's Nix Home Manager module. This skill encodes the conventions specific to _this_ repo — directory layout, frontmatter, validator, catalog row, and how to test the change end-to-end through `~/darwin`.

If the user is creating a skill that isn't intended to be shared across multiple darkmatter projects, redirect them: project-local skills go in `<project>/.agent/skills/`, personal skills go in their gitignored `personal/skills/`. This skill is only for the team-wide catalog.

## When to use

- "Add a skill that does X" / "create a darkmatter skill for X"
- "Promote this into a shared skill" — usually after a workflow has been useful in two or more projects
- "Refactor / update / improve the X skill" inside this repo
- "Bundle this script as a skill so the team can use it"
- The user describes a recurring workflow they keep doing manually and asks for it to be reusable

## When NOT to use

- The user wants a skill scoped to a single project — point them at `<project>/.agent/skills/` instead
- The user wants a personal-only skill — point them at `personal/skills/` (gitignored, separate repo)
- The user is asking about discovering/installing skills from elsewhere — that's `find-skills`
- The user wants to create a skill in some other repo's conventions (Anthropic upstream, vercel-labs, etc.) — use the upstream `skill-creator` instead

## Repo conventions (the load-bearing parts)

These come from `skills/README.md` and `scripts/validate-skill.sh`. Following them is what makes the skill ship correctly through the flake.

1. **Layout.** Each skill is a directory at `skills/<name>/` containing a `SKILL.md` at its root. Optional `scripts/` (runnable code) and `reference/` (extra docs loaded on demand). Use `reference/` singular — that's the documented form.

2. **Frontmatter.** `SKILL.md` must start with a YAML block declaring `name` and `description`. The validator only checks these two fields, but a good description carries its weight: it's the only thing an agent sees when deciding whether to load the skill, so include both _what the skill does_ and _concrete trigger phrases / contexts for when to use it_. The first ~200 characters matter most.

3. **Naming.** Lowercase, hyphenated. Directory name must equal the `name:` field. Don't prefix with the domain (`funding-screener`, not `hl-funding-screener`) unless the venue is genuinely load-bearing — `hl-funding-analysis` and `kickoff-dm-design` qualify because they only make sense in those contexts.

   The name's grammar also signals how the skill expects to be triggered (see ADR-0001):
   - **Auto-triggered skills** are noun phrases describing a domain or capability — `<domain>-<aspect>` or compound nouns. The skill reads as a thing the agent consults. Examples: `hl-funding-analysis`, `codebase-cleanup`, `end-of-turn-review`.
   - **Manual-invocation skills** start with an imperative verb prefix from a fixed set: `run-`, `kickoff-`, `setup-`, `init-`, or `do-` as a generic fallback. The verb makes the name read as a command, only sensible at invocation time. Examples: `kickoff-dm-design`, `run-funding-screen`, `setup-vault`.

   A skill is manual when its action is expensive, irreversible, has side effects on shared resources (Linear tickets, Slack posts, vault mutations), or drives a multi-step user-facing workflow with check-ins. Otherwise default to auto.

4. **No external deps.** A user must be able to consume this skill solely by adding `darkmatter/skills` as a flake input. That means: don't require `pip install` of anything outside the standard library, don't require a particular CLI tool that isn't already on a teammate's machine, don't reach for secrets that aren't reachable through `.sops.yaml`. If a script needs Python, only use the stdlib. If it needs a CLI tool, document it conspicuously and prefer something already common (jq, curl, git).

5. **Secrets.** Assume the consumer is a recipient in `.sops.yaml`. Fetch via the project's existing sops setup; don't bake credentials into the skill or expect env vars without documenting how they're populated.

6. **Self-containment.** Everything the skill needs lives inside `skills/<name>/`. Don't reference paths outside that directory. The home-manager module exposes only the skills directory; anything outside won't be installed on consumer machines.

## Workflow

### 1. Capture intent

Before writing anything, get clear on:

- What the skill does in one sentence
- The trigger phrases the user expects to invoke it
- Which projects need it (it should be at least two — otherwise it's project-local)
- What scripts/reference files it needs
- Any external commands or env vars it depends on (and whether those are universally available or need documenting)

If the user came in with a workflow they've been doing manually, extract the steps from the conversation history first; ask only for the gaps.

### 2. Scaffold the directory

Use the scaffold helper to create the standard layout:

```bash
scripts/scaffold-skill.sh <skill-name> "One-sentence description"
```

This creates `skills/<name>/SKILL.md` with the frontmatter pre-filled and `scripts/` + `reference/` subdirectories ready to use. See `scripts/scaffold-skill.sh` in this skill for the exact source.

### 3. Write SKILL.md

Fill in these sections. Use the imperative form. Explain the _why_ behind instructions rather than piling on `MUST`s — modern models reason better when they understand what's load-bearing and what's a guideline.

- **Frontmatter `description`** — for an auto-triggered skill, combine "what it does" with "when it triggers". A pushy description (`Triggers when the user asks…`, `Also triggers for…`) helps because the default failure mode for auto skills is _under_-triggering, not over-triggering. Include explicit _do not trigger_ clauses for adjacent things that aren't a fit. For a **manual-invocation skill** (verb-prefixed name), open the description with this exact line so the agent knows not to auto-fire:

  > `Manual-invocation skill — run only when the user explicitly asks for "<name>" or invokes it as a slash command. Do not auto-trigger on adjacent topics.`

  Then describe what the skill does. The verb-prefix in the name plus this opening line together make under-triggering the safe default for these. See ADR-0001 in `docs/adr/` for the full rationale.

- **When to use** — concrete trigger phrases and situations.
- **When NOT to use** — adjacent-but-different cases that would naively look like fits.
- **Tools** — for each script the skill ships, document its purpose, usage, key flags, and any env vars or external deps.
- **Reference** — point to anything in `reference/` and explain when to load it.

Keep `SKILL.md` under ~500 lines. If you're trending past that, push detail into `reference/<topic>.md` files and reference them from the body. Big reference files benefit from a table of contents.

### 4. Add scripts and reference files

Put runnable code in `scripts/`. Stick to languages already on a darkmatter machine (bash, Python 3 stdlib, node if absolutely necessary). Make scripts directly executable (`chmod +x`) and start with a sensible shebang.

Reference markdown goes in `reference/`. Each file should be loadable on its own — don't write `reference/api.md` that depends on having read `reference/setup.md` first without saying so.

### 5. Validate

```bash
scripts/validate-skill.sh skills/<name>
```

Validator checks: `SKILL.md` exists, frontmatter has `name` and `description`, directory name matches the `name:` field. Fix anything it flags.

### 6. Add a catalog row

Open `docs/catalog.md` and add a row to the table:

```
| `<name>` | One-line human-skim description (overlaps with frontmatter description but reads cleaner). | Trigger phrases, comma-separated. | Notes — runtime deps, env vars, anything operationally interesting. |
```

The catalog is what teammates skim when looking for what already exists. Make it useful — if the skill needs Python 3 or a specific env var, say so in Notes.

### 7. Test end-to-end via `~/darwin` rebuild

The skill only matters if it actually flows through the flake to consumer machines. Rebuild the user's home-manager config from `~/darwin`, overriding the agents input to point at the local checkout so we don't need a push first:

```bash
cd ~/darwin
darwin-rebuild switch \
  --flake .#$(hostname -s) \
  --override-input darkmatter/darkmatter-skills path:~/git/darkmatter/skills
```

Why the slash-syntax: `darkmatter-skills` is a _nested_ input — it's an input of the `darkmatter` flake, not a top-level input of `~/darwin`. The slash form (`darkmatter/darkmatter-skills`) addresses the nested input. Without the override, Nix would try to fetch the pinned GitHub revision and would not see the local change.

If the rebuild succeeds, the new skill is live for the user in every CLI surface the home-manager module wires up (Claude, Codex, agents).

If the rebuild fails, the most common causes are:

- Validator-level errors that slipped through (bad frontmatter, name mismatch) — re-run `scripts/validate-skill.sh`.
- A reference to a path outside `skills/<name>/` — fix and retry.
- The skills flake's own `flake.nix` doesn't compile — `cd ~/git/darkmatter/skills && nix flake check` to localize.

### 8. Commit and push

Once the rebuild is clean, commit the skill so the next teammate's `darwin-rebuild` (without the override) picks it up. Use the user's preferred SSH key explicitly — it lives in `~/.ssh/`, and committing through the default ssh-agent triggers a 1Password prompt that the user wants to avoid:

```bash
GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes' \
  git -C ~/git/darkmatter/skills commit -am "Add <name> skill"

GIT_SSH_COMMAND='ssh -i ~/.ssh/id_ed25519 -o IdentitiesOnly=yes' \
  git -C ~/git/darkmatter/skills push
```

Substitute `id_ed25519` for whichever key is actually present in `~/.ssh/`. Don't commit on the user's behalf without confirmation — that's their call.

## Writing style

- Imperative form for instructions ("Run the validator before opening a PR"), not "you should run the validator".
- Explain _why_ rather than barking `ALWAYS` and `NEVER` in caps. The model reads tone — if the prompt sounds anxious, it gets anxious. Reserve emphatic forms for things that genuinely break if violated (validator-level checks, security boundaries).
- Show, don't restate. If a script's `--help` output is informative, lean on that and link to it; don't recapitulate every flag in `SKILL.md`.
- Concrete examples beat abstract rules. A worked example of "what triggers this skill" reads cleaner than three paragraphs of policy.

## Reference

- `reference/checklist.md` — copy/paste end-to-end checklist to walk through with the user
- `scripts/scaffold-skill.sh` — creates the skill directory with frontmatter pre-filled. Pass `--manual` to scaffold a manual-invocation skill (verb-prefixed name + manual-invocation opening line in the description).
- `../../docs/adr/0001-skill-naming-convention.md` — manual-vs-auto naming convention
