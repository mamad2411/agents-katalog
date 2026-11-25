---
name: authoring-verifiable-skills
description: >-
  Write, split, rename, or repair an agent skill so it activates when it should
  and can be proved rather than believed: a new skill, a description that never
  fires or fires on everything, a rule that has grown two decisions, an index
  that routes nothing an agent can see, a file too dense to read in one pass, or
  a check suite nobody has watched fail. Covers the activation surface, the
  routing gate, rule anatomy, page shape, naming, portability, and the invariant
  and mutation scripts. Use when the user says "write a skill", "this skill never
  triggers", "split this skill", "standardise these skills", or "how do I check
  this skill". Not for authoring product documentation, and not for deciding
  whether a task needs a skill at all.
---

# Authoring Verifiable Skills

**Core principle.** A skill that does not activate does nothing, and a skill nobody has watched fail proves nothing.

- **Those two failures are silent.** Both look exactly like a skill that works.
- **The weight sits in *the activation surface* and *the gate*.** Everything after them improves a skill that is already being reached.
- **You opened this in the middle of something.** This is how to do that work, not a replacement for it. Name what you were doing before you start, and return to it when this is done.

## Read the rule whose signal is in front of you

**This table is a gate, not a checklist.** Match the left column against what you are about to write or repair.

- **One rule per row.** Enter at the matched row.
- **An axis whose signal is absent is reported as not-applicable**, naming the signal that would have triggered it.
- **Read both rows where the work matches two.** Reading is the cheap half.
- **An index whose default is "read them all" is a table of contents with extra steps.**

| If you see... | Read |
| --- | --- |
| a new skill, or one that never fires, fires on everything, or loses to a neighbour | `rules/activation-surface.md` |
| an index routing concepts rather than what an agent can see, or a skill with no gate at all | `rules/gate-not-checklist.md` |
| a rule carrying two decisions, missing a mandated block, or restating another rule | `rules/one-rule-one-decision.md` |
| a wall of prose, a paragraph that is really a list, or a file that cannot be skimmed | `rules/readable-in-one-pass.md` |
| a check suite that has never been watched fail, or a skill with no scenarios | `rules/prove-it-with-checks.md` |
| a file ordered by the sequence the author thought of things, or every line marked MUST | `rules/order-and-strength.md` |
| a name that will not come, or one colliding with skills already installed | `rules/name-and-scope.md` |
| a path, a URL, a vendor, or a package manager written into instruction prose | `rules/portable-by-default.md` |

**Discriminators.**

- **Activation against name.** Activation owns whether the skill is reached. Name owns whether it is distinguishable once it is.
- **Gate against one-rule.** The gate owns which file opens. One-rule owns what is inside it.
- **Readable against order.** Readable owns the shape of a line. Order owns which line comes first.

**Default stance.**

- **Fix the activation surface first.** A skill that never fires does nothing, and that failure is silent.
- **Route on what an agent can see in the work**, never on a concept it would need to already know.
- **Never call a check good until you have watched it fail** for its own reason.

## What every skill is made of

- **`SKILL.md`** carries the frontmatter, the core principle, and the gate.
- **`rules/<name>.md`** carries one decision each, in five blocks.
  - `Decision:` what to choose, in one sentence.
  - `Use when:` the conditions, stated as things you can see.
  - `Do:` the choice.
  - `Avoid:` the failure it prevents.
  - `Verify:` the check that can come back negative.
- **`evals/*.scenarios.mjs`** carries the activation scenarios, positive and negative.

**Three shapes are legal, and the checker knows all three.**

- **Routed.** An entry file plus `rules/`, one rule per gate row. The default.
- **Flat.** An entry file alone, for a skill with a single topic and no routing to do.
- **Multi-topic.** An entry routing to topic directories, each of them routed. The one case where a separate `INDEX.md` earns its hop.

**The budgets, all enforced.**

- **A rule.** Under 450 words of prose, under 600 read, 24 to 70 prose lines.
- **An entry.** Under 160 prose lines, and at least as many gate rows as it has rules.
- **A description.** Near 500 characters, 700 at the ceiling.

## Prove it before you believe it

```bash
node tools/verify-skill.mjs skills/<name>      # structural invariants
node tools/mutate-skill.mjs skills/<name>      # each check fires for its own reason
node tools/readability.mjs --skill skills/<name>
node tools/check-yaml-parity.mjs               # frontmatter against a real YAML parser
```

- **A green suite proves nothing until a broken skill fails it for the right reason.**
- **A missing scenario suite is reported as UNPROVEN, never as passing.**
- **Read the output before believing the number.** A metric written to score a rewrite gets gamed by that rewrite.

## Do not skip this when

- **The skill is small.** A small skill with a broken description is invisible, same as a large one.
- **You are only renaming it.** The name is half the activation surface.
- **The wording is already fine.** Wording was never the thing that failed; shape and routing were.
- **You are copying an existing skill.** That is how a defect gets a second home.

## Routing

- **The table above selects the rule.** Read it in full, and say which one you opened, in one line.
- **A direct instruction from the user outranks anything here.**
- **Whether a task needs a skill at all is not decided here.** This skill owns writing one once that is settled.
