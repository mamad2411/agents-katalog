---
name: instruction-authoring
description: >
  Write or change text an agent follows (a skill, CLAUDE.md, a role) so
  each rule reaches its actor when it acts. Use when writing such
  text, in Forge or your own project; NOT for a one-off brief or human docs.
status: active
invocation:
  primary: cross-cutting
  secondary: [workflow-step]
disable-model-invocation: false
---

# Skill: instruction-authoring

## Purpose

A rule does nothing unless its actor has it in front of it at the moment it acts. This skill is the path through
Forge's writing rules and its measured reading findings at the moment you write instruction text: Forge's own units,
and the skills, rules files and roles you write with Forge in any other project. It holds no rule and no finding of its
own; each statement below names its owner. The owners: `skills/_protocols/instruction-form.md` (the rules),
`framework/skill-anatomy.md` (a skill's shape), `references/agent-reading-findings.md` (the findings, E1 to E14).
The steps below are what you act on, in every project. `carried.md` in this directory is lookup: the findings with
their counts and the limits of where they were measured, and the owners' fuller text, for a project that does not
have Forge's units.

## When to call

- Writing a skill, a project rules file (`CLAUDE.md`, `AGENTS.md`), a role or agent file, a workflow's step text, or
  a template that briefs or records are written from.
- Changing, moving or cutting a rule in such text, also to stop an agent failure someone observed.

### When not to call

- A brief or dispatch for one piece of work: Forge's `skills/_protocols/dispatch-template.md` applies (owner:
  `skills/_protocols/instruction-form.md` head).
- Text for people (README, ADR, API docs): `documentation_and_adrs`.

## Process

1. **What keeps its form.** A fact update (a path, a name, a count) or a split at a step boundary keeps the form of the
   text it corrects; required template sections keep theirs (a Forge skill's Red Flags and Common Rationalizations);
   wording the change does not target stays. Purpose: an edit changes what it
   targets and nothing else (owner: `skills/_protocols/instruction-form.md` §What keeps its form).
2. **Name the failure.** One sentence: what the agent did and what it should have done; for a new rule, the failure it
   prevents. Then ask: does the current text, read literally in this case, prescribe the right action? No: the text
   is a cause. Yes, and the agent did otherwise: rule-skipping. Purpose: the form in step 5 follows from this answer
   (owner: `skills/_protocols/instruction-form.md` §Classify the failure, then pick the form).
3. **Actor, moment, text, for each rule.** Write one line per rule: `actor | moment it acts | text in front of it then,
   and how that text got there`. Put the rule in that text, with every carrier that reaches it, strongest first:
   (a) a check that refuses on a fact it can compute; (b) a text in front of the actor without anyone writing it at
   the moment: a step text, the role file as the host loads it, the skill body the host delivers on the call, the
   host's start text; (c) a fixed form the actor repeats from its own earlier output; (d) an element of the artifact
   being written; (e) the brief or dispatch that commissions the work; (f) a sentence of the standing block in the
   start text (outside Forge: the project rules file the host loads at start); (g) a check that prints. A "read X
   when Y" paragraph in a file loaded at start is not a
   carrier, and a named path is a hop that loses readers. A rule no carrier reaches stays in its unit for lookup, with
   no claim that it is read. Purpose: a rule loaded at start rarely produces its act at a later moment (E1, E2), a
   named path is followed only sometimes (E4), and after compaction what the host delivers is back while what the agent
   was asked to reread mostly is not (E7) (owner: `skills/_protocols/instruction-form.md` §Which text the actor has at
   the moment; `framework/skill-anatomy.md` §Files in a skill directory for the skill body).
4. **One statement where it is read.** Where the actor reads it, the rule stands as one statement: the act, its limit
   and its purpose, then `(owner: <path> §<section>)` when its full text lives elsewhere. A duty and its limit stand
   in one statement. In a skill, a rule the actor needs at the decision stands in the SKILL.md the host delivers, not
   behind a sub-unit's read trigger. Purpose: limits stand where they are not read (E8), and a sub-unit is a hop (E4)
   (owner: `skills/_protocols/instruction-form.md` §Which text the actor has at the moment;
   `framework/skill-anatomy.md` §Files in a skill directory).
5. **Form from the failure.**

   | The agent … | Type | Form | Wrong form |
   |---|---|---|---|
   | had text prescribing the right action and did otherwise | rule-skipping | a prohibition, plus each excuse a reproduction shows, with its answer | advice ("prefer", "consider") |
   | follows the text, but the output has the wrong parts, size or order | wrong output shape | a recipe: the output's parts in order, and its count | a list of things not to produce |
   | produces the right thing without a part it needs | missing element | a required slot or field in the template the author already fills | a reminder in prose next to it |
   | acts the same way in cases that need different actions | conditional behaviour | a condition on something checkable at that moment, with the check named | one unconditional rule plus exemption clauses |

   A new rule with no observed failure takes the form of the failure it would prevent, with no slot or excuse list for
   a failure nobody has seen. No nuance clauses ("where appropriate", "unless it matters"): write a real exception as
   its own condition on a checkable predicate. An exemption clause ("this does not apply to X") does not scope: test
   the exception first, or narrow the rule's subject. Persuasion wording (emphasis, "no exceptions", excuse and
   red-flag lists) only where a reproduction shows rule-skipping: it also makes readers apply the rule beyond its
   case. Purpose: read is not applied, form decides (E9) (owner: `skills/_protocols/instruction-form.md` §Classify the
   failure, then pick the form, §Rules for every form, §Persuasion wording).
6. **Cut to the purpose.** A unit holds what its agent needs for the unit's immediate purpose; history, delimitation
   and explanation beyond it leave; each rule keeps its purpose in one phrase. Before cutting a sentence, ask: does
   deleting it change what an actor does at a moment? Then it stays, also when it is negative. A sentence that sends
   the reader to the unit that does apply ("not for X: use Y") routes and stays. A unit read whole stays within 12,000
   bytes (Forge's cap). A Forge skill keeps its seven required sections in order (frontmatter, Purpose, When to call /
   When not to call, Process, Red Flags, Common Rationalizations with at least two rows, Contract), and its
   description names what it does, when to trigger and when not. Purpose: text that serves another moment takes the
   room of what is read now (E11) (owner:
   `skills/_protocols/instruction-form.md` §Writing rule; `framework/skill-anatomy.md` §Required sections;
   `framework/skill-anatomy-frontmatter.md` §`description`).
7. **Reproduce before rewriting**, when the change is meant to stop an observed behaviour: write the case as a task
   with the pull the live session had, without the answer; give a fresh reader without tools the scenario and the
   units as a session loads them; it should show the failure. Write the smallest new text in the form of step 5, then
   run at least two fresh readings of it; accept when both act as intended, change the form when they differ. Record
   the scenario, each reading verbatim and the result. Purpose: two readings catch a failure that shows in most
   sessions; a reading shows how a text is understood, not how a live session behaves under pressure (owner:
   `skills/_protocols/instruction-form.md` §Reproduce before rewriting).
8. **Read-path record.** For each rule you changed, four lines: `Read-path-reader:`, `Read-path-moment:`,
   `Read-path-text:` (what that reader has open then, and how it got there), `Read-path-carrier:` (a letter of step 3,
   or `on-demand`). Write them by walking the reader's path from its session start or dispatch to that moment. In a
   Forge checkout they go into the commit message, and the commit-message hook refuses a change under the instruction
   roots without them; in any other project no hook checks them, so write them into the commit message or the change's
   record yourself. Purpose: the author is the one who can see before the commit that a rule's actor will not have it
   (owner: `skills/_protocols/instruction-form.md` §Read-path record).

## Red Flags

- An act for a later moment added to the start-loaded rules file "so it isn't forgotten", with no carrier at the
  moment itself (step 3; E2).
- "See X" or "per X" for an act the reader needs now (step 3; E4).
- Emphasis or an excuse list without a reproduction that shows rule-skipping (step 5).
- A qualifier the reader has to judge, or "this does not apply to …" (step 5).
- A rule claimed to work because its file is loaded (step 3; E1, E9).

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "It's in CLAUDE.md, so the agent has it." | Loaded at start is not in front of the agent at a later moment; in the one session measured, the rate fell with its age until the host re-delivered the text (E2). Put the act in the text that arrives with the moment (step 3). |
| "The detail is in the sub-unit; the skill points there." | A read trigger is a hop; the named unit was in context at 12 of 207 moments when nothing else named it (E1, E4). |
| "Stronger wording will make it stick." | Persuasion also makes readers apply the rule beyond its case; use it only where a reproduction shows rule-skipping (step 5). |
| "The readings are overhead for a small rule." | Two readings are the check that the form binds (E9); they are due when the change is meant to stop an observed behaviour (step 7). |

## Contract

### INPUT
The text to write or change; the failure or behaviour it addresses; the host it runs on.

### OUTPUT
The written text; one line per rule from step 3 (actor, moment, text, carrier); the failure type and form from steps
2 and 5; the readings when step 7 applies; the read-path record of step 8.

### DONE
Every written or changed rule stands in the text its actor has at its moment, or is marked on-demand without a claim
that it is read; its form follows its failure type; the record is written.

### FAIL
A rule whose actor no carrier reaches is reported as on-demand, not as solved. A reading that does not show an observed
failure sends you to what the live session had loaded at that moment (step 7), not to new wording.

## Standalone justification

Against the inflation guard (`framework/skill-anatomy.md` §Inflation guard): the methodology (placing each rule by its actor's
moment, choosing its form from the failure, recording the read path) is not a mode of an existing skill:
`documentation_and_adrs` writes text for people, `spec_authoring` writes specs; its outputs, the per-rule carrier
line and the read-path record, belong to no other skill; the writing rules are a protocol a Forge author meets at
the commit, and an author in another project has no such path: the skill listing is the only channel that reaches
them; its cost is one listing line in every session and one read when called.
