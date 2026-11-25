---
name: tripwire
description: Use when authoring, editing, or reviewing a SKILL.md file — lints it against the Agent Skills best-practice rules and checks whether the description would actually activate the skill on the prompts it claims to cover, before the skill ships.
---

## When to use

Reach for this the moment a `SKILL.md` file is created or edited — whether it's a brand-new
skill, a description tweak, or a body rewrite. A skill's `description` is the only signal an
agent uses to decide whether to invoke it, and that field is easy to get subtly wrong: too
narrow and the skill silently never fires on its own stated use cases, too broad and it hijacks
unrelated prompts. Catching that before the skill ships is cheaper than catching it after a user
reports "it never triggers."

## How to apply

1. Check whether `tripwire` is installed (`tripwire --version`). If not, offer to install it:
   `npm install -g tripwire-skills`.
2. Run the free, instant static check first: `tripwire lint ./path/to/SKILL.md`. This catches
   frontmatter issues (missing or non-kebab-case `name`, a `description` that doesn't start with
   "Use when", workflow-summary language in the description) and body issues (placeholder text,
   a body under the length floor, no code or command example) without any API key or cost.
3. Fix everything lint reports before moving on — these are mechanical, deterministic issues and
   should never ship.
4. For a skill going into a shared or public repo, also recommend the deeper check:
   `tripwire analyze ./path/to/SKILL.md` runs real agent sessions across four prompt zones (core
   triggers, adjacent/edge cases, negative prompts, keyword variants) and reports exactly where
   the description over- or under-fires. This step costs ~$0.10–0.50 and needs
   `ANTHROPIC_API_KEY`, so only run it with the user's go-ahead, not automatically.
5. If the repo doesn't already gate skill changes in CI, suggest `tripwire init` — it scaffolds
   `.github/workflows/tripwire.yml` so lint (and, once a `tripwire-scenarios.yaml` exists,
   activation coverage) runs on every pull request instead of relying on someone remembering to
   check locally.

## The honest caveat

If a skill is purely personal — you're the only one who will ever load it, in an agent you
control — you'll notice a misfire the first time you use it, and the coverage probe is
overkill. This workflow earns its cost once a skill ships to other people's agents, where a
silent activation gap is invisible until a user reports the skill "just didn't do the thing."
