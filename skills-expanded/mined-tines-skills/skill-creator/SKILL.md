---
name: skill-creator
description: Write and improve 3B skills. Use when creating a new skill from scratch or refining an existing one — covers writing a description that triggers reliably, structuring clear instructions, and testing on realistic prompts.
license: Apache-2.0
compatibility: Tines 3B
---

# Writing a good skill

A 3B skill is an Agent Skills bundle the AI loads on demand. Each skill is a directory with a required `SKILL.md` and optional supporting files:

```text
my-skill/
├── SKILL.md
├── references/
│   └── api.md
├── assets/
│   └── report-template.md
└── scripts/
    └── collect.ts
```

`SKILL.md` starts with YAML frontmatter. `name` and `description` are required. The name uses lowercase letters, numbers, and single hyphens, and it matches the parent directory. `license`, `compatibility`, string-valued `metadata`, and the experimental `allowed-tools` field are optional. `allowed-tools` is guidance, not a grant of 3B permissions. The body contains the instructions the AI reads once the skill is in play.

## The description is the trigger

The AI decides whether to consult a skill from its name and description alone, so this is the highest-leverage text you’ll write. Put _all_ the “when to use this” information here, not in the body. State both **what the skill does** and **the specific situations that should pull it in**.

AIs tend to under-trigger skills — to not reach for one when it would help. Counter that by being a little pushy and concrete. Instead of “Guidance for building dashboards,” write “Guidance for building dashboards. Use this whenever the request involves dashboards, data visualization, internal metrics, or displaying any kind of company data — even if the word ‘dashboard’ is never used.”

Note that simple, one-step requests may not trigger any skill, because the AI can just handle them directly. Skills earn their keep on complex, multi-step, or specialized tasks — write the description for those.

## Writing the instructions

- **Keep it focused.** Include what the AI can’t reliably infer on its own; cut throat-clearing. A tight, well-organized skill beats an exhaustive one.
- **Use the imperative.** “Read the API docs first,” not “The model should read the API docs.”
- **Define the output format** when it matters — give the exact template or structure you expect.
- **Show an example or two.** A concrete input → output pair teaches faster than a paragraph of rules.
- **Explain the why.** Today’s models have good judgment; tell them _why_ something matters and they generalize. Reserve hard “ALWAYS/NEVER” rules for genuine footguns — if you’re reaching for all-caps MUSTs, that’s usually a sign to reframe and explain the reasoning instead.

Keep `SKILL.md` focused on the workflow and decision points. Move detailed material or deterministic work into supporting files, and link to each supporting file from `SKILL.md` with clear guidance about when to use it.

## References, assets, and scripts

- **`references/`** contains documentation the AI should read only when it needs that detail: API notes, schemas, domain rules, or longer examples. Link directly from `SKILL.md`, and avoid chains where one reference points to another reference.
- **`assets/`** contains files used to produce the final output, such as templates, fixtures, images, or starter projects. Assets are available to copy or transform; they do not need to be loaded into context unless the task requires reading them.
- **`scripts/`** contains deterministic helpers for work that should not be regenerated on every use. Tell the AI what each script does, when to run it, what arguments or stdin it expects, and what it writes to stdout or files.

Use paths relative to the skill directory. Include static dependencies in the bundle, and state any runtime or package requirements in `SKILL.md` and `compatibility`.

3B runs shell (`.sh`), Python (`.py`), JavaScript (`.js`), and TypeScript (`.ts`) skill scripts through sandboxed execution. The skill bundle is copied into an ephemeral sandbox, the script runs from that skill root with explicit arguments and stdin, and changes do not persist back to the skill. A script can use only connectors already authorized for the current chat through the existing inline execution path; the skill never grants connector access. Make required inputs explicit rather than embedding secrets or assuming ambient access.

## Test and iterate

Write 2–3 realistic prompts — the kind of thing someone would actually type — and run the AI with the skill enabled. Watch where it goes wrong, then tighten the skill: generalize from the failure rather than patching the one example, remove instructions that send it down unproductive paths, and re-run. Exercise references and scripts directly, including their failure cases. Repeat until it behaves the way you want across all your test prompts, not just one.

## Saving the skill

When you’ve drafted a skill in chat and the `proposeSkill` tool is available, call it with the name, description, and `SKILL.md` body instead of pasting the skill into your reply for the user to copy into 3B. The chat shows the user the full `SKILL.md` from that call. The user confirms, then reviews the new skill and saves it. Supporting files can be added from the skill’s Files tab afterward.

---

_Adapted by 3B from Anthropic’s “skill-creator” skill (github.com/anthropics/skills), © Anthropic PBC, licensed under Apache-2.0. Modified for 3B’s Agent Skills bundles and sandboxed script execution._
