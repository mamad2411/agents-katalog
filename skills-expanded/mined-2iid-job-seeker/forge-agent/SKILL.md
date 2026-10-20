---
name: forge-agent
description: The agent BUILDER — mint one new senior specialist agent (and any skills it needs) on demand, to the house quality bar, when the roster lacks the expertise a project requires. Trigger words — forge agent, build an agent, create an agent, new agent, I need a <X> engineer, add a specialist, agent builder, make a skill.
---
# /forge-agent — mint a senior specialist on demand

**Use when:** the project needs expertise no current agent has (a framework, platform, or domain). Creates one
first-class agent — and, if needed, the stack-specific skills it should use. **Owner:** `agent-architect`.

## Procedure
1. **Name the gap** — the exact specialty (e.g. "Flutter/Dart mobile engineer", "Unity gameplay engineer",
   "Solidity smart-contract engineer", "data/ML engineer").
2. **Research if unfamiliar** — confirm current best practices, idioms, and the real risks of that stack
   (`WebSearch`/`WebFetch`) so the agent is genuinely expert, not generic.
3. **Write the agent** → `agents/<name>.md`, meeting the full quality bar:
   - frontmatter: `name`, a **trigger-rich `description`** (what + when + trigger words), `tools`, `model`;
   - a persona with **real years + judgment**, principles, what it owns, a "done when";
   - **wired to the skills** it should use (existing + any new ones below).
4. **Forge missing skills** — if the specialty needs a playbook the library lacks, write
   `skills/<skill>/SKILL.md` following the skill authoring convention (verification-first, guardrails,
   done-when).
5. **Register** — add the new agent to `docs/planning/team.md`.

## Guardrails
Never ship a thin agent — match the depth of the hand-written core. Ground stack-specifics in current reality
(research when unsure), not stale assumptions. One clear lane per agent; don't duplicate an existing role — extend
it instead. Secure-by-default carries into every stack.

## The frontmatter, exactly
`scripts/validate-agents.sh` enforces these, so writing them wrong costs a round trip:
- `name:` equals the filename. `description:` ends with the trigger words that decide when it fires.
- `tools:` is a **whitelist** — include `Skill`, or every playbook the persona names is inert. Include `Bash`
  for any persona naming `verify-change`, `write-tests`, `ci-pipeline` or `design-review`; those playbooks run
  things. Any persona with `Write` or `Edit` must name `verify-change`.
- `model:` — `opus` for a role that decides or blocks, `sonnet` for one that produces under a spec.

Never write a claim of seniority. "15 years of experience", "world-class", "battle-tested", "follows best
practices" are all rejected by name. Write the **judgement calls a generalist would get wrong** instead —
that is what the reader needs and what the validator measures, via the distinct domain tokens (identifiers,
file names, commands, measured quantities) a real specialist cannot avoid using.

## Ship it (the step that was missing)
A forged persona that is never validated, never mirrored and never listed is a liability, not a specialist.
1. Start from `docs/_templates/agent.template.md`. The `## Judgement you are expected to have` section is the
   one that matters — four to six calls this role makes *differently from a generalist*, each with its
   reasoning. If you cannot write six, you do not know the domain well enough to forge for it yet: say so.
2. `bash scripts/validate-agents.sh` must exit 0. It refuses a body under 25 lines, a persona with no
   `## Definition of Done`, and seniority-by-assertion ("years of experience", "world-class", "follows best
   practices") — assert nothing, show the judgement instead.
3. **List it in `agents/README.md`** — `/assemble-team` reads that roster to know what it may select, so a
   persona that exists but is not listed is shipped and unselectable. `debugger` was exactly that for two
   versions. `scripts/validate-agents.sh` now fails on it, and put it in the model-tier line too.
4. `./scripts/sync-adapters.sh` so the role reaches `.claude/agents/`.
5. `bash scripts/test/test-forge-quality.sh` — it proves the floor still holds.

## Done when
`agents/<name>.md` (and any new skills) exist, are as strong as the core, and are on the team roster.
