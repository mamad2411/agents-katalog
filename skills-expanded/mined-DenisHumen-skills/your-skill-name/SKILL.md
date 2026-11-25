---
name: your-skill-name
description: >-
  What this skill does AND when Claude should use it, in one or two sentences.
  Name the concrete triggers a user would actually type, for example
  "color grade this", "make a LUT", "write a shot list", "review this contract".
  Max 1024 characters. Third person, no marketing words.
# ---------------------------------------------------------------------------
# Optional fields from the Agent Skills spec (work everywhere):
# license: MIT
# compatibility: Requires Python 3.10+ (and e.g. ffmpeg 6+) on PATH
# metadata:
#   plugin: cinema
#   group: color-grading
#   version: "0.1.0"
#   author: your-github-handle
#
# Optional fields that only Claude Code understands. Remove them before
# uploading the skill to claude.ai or the Skills API (they reject unknown keys):
# argument-hint: "[file-or-folder]"
# allowed-tools: Bash(python:*) Read Write
# disable-model-invocation: false
# ---------------------------------------------------------------------------
---

# Skill title

<!--
How to use this template
1. Copy the whole `skill-template/` folder into a plugin:
     plugins/<plugin>/skills/<your-skill-name>/            (flat plugin)
     plugins/<plugin>/skills/<group>/<your-skill-name>/    (grouped plugin)
2. The folder name and the `name:` field MUST be identical: lowercase letters,
   digits and single hyphens, max 64 chars, unique across the whole repository,
   and starting with the group prefix if the plugin defines one in
   `plugins/<plugin>/skill-prefixes.json` (e.g. `grade-look-builder`).
3. Keep this file under ~500 lines. Move long material to `references/`,
   reusable code to `scripts/`.
4. Write everything in your own words. No quotes or excerpts from books,
   manuals, articles or other people's skills — summarise the principle instead
   and credit the source by title and author in "Sources".
5. Follow the plugin's own conventions (its README lists shared documents,
   IDs and the workflow the skill plugs into).
6. Delete these HTML comments and every section that does not apply.
-->

One short paragraph: the job this skill does, the result it produces, and where
it sits in its plugin's workflow (which skill usually runs before it and which
one after).

## When to use

- The user asks for … (list real phrasings and situations)
- A previous step produced … and the next step is …

## When not to use

- … → use `other-skill-name` instead
- … is out of scope (say why)

## Inputs

| Input | Required | Format | Usually comes from |
|---|---|---|---|
| Main input | yes | file / folder / pasted text | the user, or `previous-skill-name` |
| Project context | no | e.g. a brief or a spec document | the plugin's templates |

If a required input is missing, ask for it (or offer to create it with the
skill that owns it) instead of guessing.

## Steps

1. **Read the context.** Load the inputs and any shared project documents.
   Restate the goal in one line.
2. **Plan.** List what you will produce and how you will check it. For anything
   that costs money or overwrites files (paid APIs, long jobs, deletions), show
   the plan and wait for the user's OK.
3. **Do the work.** Concrete, numbered actions. Put exact commands in fenced
   code blocks. Long recipes go in `references/`, reusable code in `scripts/`.
4. **Check.** Run the quality checklist below; fix and re-check before reporting.
5. **Hand off.** Save outputs with the naming convention below and name the next
   skill, if there is one.

## Outputs

| File | Format | Notes |
|---|---|---|
| `…/result.ext` | … | naming convention, where it is saved |

## Quality checklist

- [ ] The result answers the request that triggered the skill
- [ ] Follows the plugin's conventions (shared documents, IDs, style rules)
- [ ] Technical details are correct and were checked, not assumed
- [ ] Files are named and placed as described in Outputs
- [ ] Nothing copied verbatim from copyrighted sources

## Supporting files

Load these only when needed:

- [references/overview.md](references/overview.md) — deeper explanation, tables, recipes
- `scripts/example.py` — run it, do not paste it into the conversation

## Sources

Principles in this skill are summarised in our own words from:

- *Book or article title* — Author (year)
