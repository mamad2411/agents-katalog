---
name: skill-authoring
description: |
  Write, review, or improve a SKILL.md for a Skill Tree library: a description that triggers, a lean body, hub frontmatter, done criteria. Use on "create a skill", "improve this skill", "skill review".
---

# Skill authoring

A skill is an instruction package a coding agent loads on demand. Two budgets
decide whether it works. The `description` sits in every session's context and
carries the whole triggering decision. The body loads only after a trigger, so
it has to earn its tokens with facts the agent would otherwise get wrong.

Read the gotchas first. Then follow the workflow in order; each step ends with
something you can check.

## Gotchas (facts that defy reasonable assumptions)

- The frontmatter `name` must equal the directory name and the registry key.
  Slug only: lowercase letters, digits, hyphens. pi tolerates a mismatch;
  spec-strict clients and the hub do not.
- Three description ceilings apply at once: 200 characters (the hub's rule
  and claude.ai's upload limit), 250 (Claude Code truncates there when it
  decides whether to trigger), 1024 (the Agent Skills spec; Codex refuses a
  longer one). Stay at or under 200 and put the trigger words early.
- "When to use" belongs in the description, not the body. The body is not
  loaded until the skill has already triggered.
- Codex and opencode ignore Claude-only frontmatter (`disable-model-invocation`,
  `user-invocable`, `allowed-tools`). They read `name`, `description`,
  `license`, `compatibility`, `metadata`. Anything else must not be
  load-bearing for those harnesses.
- The hub counts a mention of another skill as a reference only as a backtick
  span (`` `deliver-it` ``) or a slash token (`/deliver-it`). A bare slug in
  prose is not a reference and will not surface a `missing_refs` finding when
  the project lacks that skill.
- Keep bundled files one level deep (`references/x.md`, `scripts/x.sh`) and
  link them with relative paths. The hub's content walkers do not follow
  symlinks out of the skill directory, and nested reference chains get read
  partially.
- Never write a machine path: no home-directory prefix, no drive letter, no
  backslashes. Use forward slashes and paths relative to the skill or the
  project.
- A rarely needed workflow should be `user-only` invocation: it then costs no
  context until someone types `/name`.
- Claude Code keeps a triggered body in context across turns. Write standing
  instructions, not a one-shot script.

## Workflow

### 1. Confirm it should be a skill

| The instruction is... | Make it a |
|---|---|
| a multi-step workflow the agent should follow on demand | skill |
| one or two rules that apply on every turn in a project | agent-doc rule or a hub snippet |
| a tool the agent should call with structured input | MCP server |
| a role with its own model and tool set | sub-agent (a skill may ship one via `ships_with`) |
| knowledge the model already has | nothing; delete it |

If the workflow is one step the agent can already do, stop: one-step utility
skills undertrigger no matter how they are described.

### 2. Capture intent

Answer four questions before writing, from the conversation if it already
holds the workflow, otherwise by asking:

1. What should the agent be able to do after loading this?
2. What will a user actually type when they need it? Collect the literal
   phrases.
3. What does the output look like? Name the artifact and its shape.
4. Is the result objectively checkable? If yes, plan two or three test
   prompts now.

### 3. Write the description first

Formula: what it does, then when to use it, then the literal trigger phrases,
then a boundary if a neighbouring skill could fire instead.

```yaml
description: |
  <verb phrase: what it produces or changes> for <context>. Use when <situation>
  or on "<phrase>", "<phrase>". Not for <adjacent case>; use `<other-skill>`.
```

Check it against six prompts in your head: three that must trigger, three
near-misses that must not. Fix a near-miss by adding the boundary, not by
deleting keywords. Count the characters; the hub's editor shows the meter.

### 4. Draft the body

Use this order and nothing the model already knows:

```markdown
# <Title>

<Two or three sentences: what this skill changes about how the agent works.>

## Gotchas
- <environment fact that defies a reasonable assumption>

## Workflow
1. <step with a checkable end state>
2. ...

## Done when
- <machine-checkable criterion>
- <what the agent must show, not claim>

## References
- `references/<file>.md` — read when <condition>.
```

Rules for the body:

- Put the non-negotiable constraints at the top or the bottom. Nothing
  critical in the middle of a long block.
- Prefer a numbered workflow with checkable ends over prose advice. Prefer
  one worked example over a rule about style.
- Give one default and a named escape hatch, never a menu of equal options.
- Match prescriptiveness to fragility: exact commands for destructive or
  order-dependent steps, heuristics everywhere else.
- Name the step the agent will talk itself out of and pre-empt the excuse.
- Explain why once; do not stack MUST and NEVER.
- Stay under 500 lines. Above about 150 lines, move material into
  `references/` and say exactly when to read each file.
- Bundle a script for anything the agent would reinvent each run, and handle
  its errors inside the script.

### 5. Choose the Skill Tree frontmatter

Decide scope, invocation, harness affinity, and companions. The table and the
field shapes are in `references/skill-tree-frontmatter.md`; read it when you
set anything beyond `name` and `description`.

### 6. Register and equip

- New skill in the library: `hub new skill <name>`, or the `skill_create`
  tool of the `skill-tree` MCP server. Then edit the files it scaffolded.
- A skill you wrote inside a project's `.claude/skills/`:
  `hub project import-skill <name> --project <p>`.
- Equip it where it is needed: `hub enable <name> --project <p>`. A
  `scope: global` skill is on everywhere without an equip.
- `hub sync` runs after every registry write, so the symlinks are in place
  when the command returns.

### 7. Review before you call it done

Run `references/review-checklist.md` against the file. Every red item is a
fix, not a note. Two items are non-negotiable: the description fits the
ceiling, and the body has a done-criteria section.

### 8. Prove it

Run the two or three test prompts from step 2 in fresh sessions, once with the
skill equipped and once without. Read the traces, not only the outputs: an
over-long skill shows up as the agent following instructions that do not
apply. Keep the skill only when the with-skill run is better in a way you can
name. For a full eval loop with graded assertions and trigger-rate tuning,
hand the skill to `skill-creator` (Anthropic's), which this skill does not
duplicate.

## Done when

- `name` equals the directory name and passes the slug rule.
- The description is at or under 200 characters, states what and when, and
  carries the literal trigger phrases.
- The body has a gotchas section, a numbered workflow, and a done-criteria
  section, and is under 500 lines.
- No machine path and no backslash path appear anywhere in the skill.
- Every file the body links exists, one level deep.
- The skill is registered, equipped where intended, and `hub sync` reports no
  warning for it.
- The with-skill run beat the no-skill run on the test prompts, and you can
  say how.

## References

- `references/skill-tree-frontmatter.md` — the fields the hub reads
  (`scope`, invocation flags, `harnesses`, `ships_with`), their exact shapes,
  and the registration commands. Read at step 5 and step 6.
- `references/review-checklist.md` — the checklist for step 7, with the fix
  for each red item. Also the tool for "review my skill" requests.
