---
name: agent-identity-setup
description: "Use when setting up or resetting agent SOUL, memory, skills."
version: 1.1.0
author: coordinator role of hermes-fleet-apps
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [identity, soul, memory, skills, onboarding, profile, steering, personalization]
    related_skills: [hermes-agent]
---

# Agent Identity & Steering Setup

Configuring what an agent IS (voice, standing behaviour) and how it gets steered
(facts, procedures, per-repo rules), so future sessions start already aligned
instead of relearning the user each time.

Covers: bootstrapping a fresh profile, retuning an existing SOUL, onboarding a
user's preferences, and the recurring question of where a given durable lesson
belongs. For general Hermes configuration, paths, and CLI surface, use the
bundled `hermes-agent` skill — this skill is the identity workflow only.

Depth: `references/steering-layers.md` — exact paths, file formats, budgets,
precedence, and what is tool-managed vs hand-editable.
A domain agent gets only the skills of its domain.

## Always-on rules

**Never invent a user's preferences.** An empty identity file is recoverable; a
fabricated one silently steers every future session and reads as established
fact to the agent that inherits it. If preferences cannot be elicited, write the
verifiable structure and leave the personal content out, then say so.

**Verify the layout on disk before advising on it.** Users describe the identity
files from memory or from other agent frameworks, and the recalled names,
casing, and directories are routinely wrong. Read the profile directory, then
correct the premise explicitly — an answer built on the user's wrong filenames
teaches them the wrong model and the files land in places nothing loads.

**Route every durable thing to exactly one layer.** The same rule written into
two layers drifts and then contradicts itself. Pick by lifetime and load cost:

| Layer | Holds | Loaded |
|---|---|---|
| SOUL.md | Voice, autonomy level, candour, standing behaviour | Every turn, whole |
| memory `user` | Who the user is — role, stack, preferences | Every turn, char-capped |
| memory `memory` | Environment facts, conventions, tool quirks | Every turn, char-capped |
| skills | How to do a class of task — procedure + pitfalls | On demand, when triggered |
| AGENTS.md | Rules scoped to one repository | In that repo |

Because memory is injected every turn under a hard cap, it takes only facts true
in **every** session regardless of task. Anything that begins "when doing X…" is
a skill, not a memory entry — memory has no trigger, so a task-specific rule
parked there fires during unrelated work.

**Every layer above is per-agent, and each agent reads only its own.** A rule
written into one profile's skills steers that profile and nothing else. When the
user's real requirement is "this must hold no matter who is working" — them, a
sibling profile, a different CLI agent, a script — see the enforcement rule
below: no documentation layer can deliver that.

**Propagate a convention to a sibling profile as skill + memory pointer.**
Writing only into their memory burns the char budget on detail; writing only a
skill risks it never being triggered. Put the full rules in a skill under their
profile and add one memory line that names it. The skill file needs YAML
frontmatter with `name` and `description` or the loader ignores it entirely and
the propagation silently does nothing — verify against a skill already in that
profile, since layouts differ between installs. Touch only what concerns the
convention; another profile's other skills and memories are not yours.

**Enforce mechanically what must hold for every actor, not just for agents that
read docs.** Skills, memory, SOUL and `AGENTS.md`/`CLAUDE.md` are instructions —
they work only for an actor that loads them, and a CLI agent, a cron job or the
user at a shell loads none of them. Where a violation is expensive or
irreversible, add a gate the tool itself runs: a `pre-commit` hook installed
globally via `git config --global core.hooksPath <dir>` covers every repo,
including ones created later, for every actor on that machine. Keep the docs as
the explanation and the gate as the guarantee; the gate's failure message should
state the fix, so an actor that never read the docs can still recover.

Install the gate once per OS the user works in — a WSL install and a Windows
install are separate git configurations — and prove it with two tests: one
commit that should pass and one that should be refused. An untested hook that
silently allows everything looks identical to a working one.

**Back up any identity file before rewriting it.** Copy to `backups/` first.
These files are prose with no version control and no undo; a rewrite that loses
the user's own wording cannot be reconstructed from the diff.

**Do not hand-edit tool-managed stores.** Memory entries are written through the
memory tool, which enforces the character budget and the record separator. Hand
edits bypass both and eventually corrupt the parse. Same principle for
`config.yaml` — use `hermes config set KEY VALUE`.

**The one exception: seeding a profile that is not the active one.** The memory
tool writes only to the running session's profile, so it cannot populate a
profile you just created. Hand-write `memories/USER.md` and `memories/MEMORY.md`
there instead, entries separated by a line containing only `§`. This is correct
only before that agent has ever run; once it is live, its own memory tool owns
the files.

**Build skills from real work, not from a questionnaire.** A skill written from
what a user *says* they want encodes aspiration; one written from a completed
task plus their corrections encodes what actually satisfies them. When asked to
pre-build a skill library during setup, write the identity layers, then say
plainly that the skill layer gets built from the first few real tasks.

The exception is a **method** skill: when the role itself is a procedure — a
planner, a builder, a reviewer — encode the procedure the agent must always
follow at creation time. That is behaviour, which the owner can specify up
front. Facts about tools, repos, and quirks still wait for real work.

**Give SOUL.md a named, ordered method when the role is a build or review
role.** A list of virtues ("thinks like a senior engineer", "plans well")
produces no repeatable behaviour, because there is no step to be on. A numbered
shape the agent announces before working — and names again at hand-over — is
what makes the next run a repeat instead of a reinvention.

**Name the role's core skills in SOUL.md, one line, mapped to the method step
where each applies.** A skill in the index is only a description the model may
or may not match; when the owner never talks to that agent and no brief tells
it what to load, a core skill silently goes unused. Write "Skills by step, load
each when you reach it, the owner never has to name them: Research `x`; Spec `y`"
under METHOD — names only, never the content, so the always-on cost stays one
line. Pick by walking the agent's `skills/` tree against its METHOD line: the
2–7 skills that ARE its job go in; niche, duplicate and sibling-owned skills
stay on demand. A rule that must hold on every turn regardless of recall (e.g.
a coding-discipline ladder) gets its essentials in SOUL and the full text in the
skill; the SOUL line then says when to load the skill. Propose the list to the
owner per agent before writing — they decide what is core.

**Write the owner's constraints into SOUL.md as behaviour, not as facts about
them.** "The owner is impatient" is a fact that ages into an excuse; "deliver a
running artefact early, keep planning to a handful of bullets" is the same
information as an instruction the agent can act on every turn.

## Verifying an identity actually took

Reading the files back proves they landed. It does not prove they work — the
agent has to be run.

Use **two** tests, and make the second one adversarial:

- **Capability** — a small real task from the role. Proves the tools and the
  method fire.
- **Character** — a request the SOUL should push back on, refuse, or hand off.
  Proves the expensive parts: tone, candour, limits, admitting its own edges.

A capability test alone always passes and tells you nothing about identity;
the behaviours that cost the most to get wrong never fire on a task the agent
is simply good at.

Delete the test sessions afterwards (`hermes -p <name> sessions list`, then
`sessions delete <id> --yes`). They are transcripts of throwaway work that the
agent can later resume and mistake for its own history. Tests also write to
the agent's workspace (trackers, caches): restore those files too, or the
agent starts with a fake item in its source of truth.

To overwrite a freshly cloned placeholder SOUL.md, `rm` it and write fresh:
`write_file` may refuse to replace a file it considers only partly read, and
an unmodified template needs no backup.

## Procedure

1. **Read the profile directory.** Resolve the active profile home — never
   hardcode the default — and list it. Confirm which identity files exist,
   their real names and casing, and whether the memory store is empty.

2. **State the corrected model before writing anything.** Name each layer, what
   it holds, and when it loads. The user needs this to make the choices in the
   next step; skipping it produces answers to questions they misunderstood.

3. **Elicit preferences in one structured pass.** Ask together, as selectable
   options: what classes of work the agent is for, default autonomy on
   non-trivial tasks, and how much pushback they want. These three determine
   most of SOUL.md. Put them before any free-text question — free-text prompts
   are the ones that go unanswered, and losing them still leaves the structured
   answers usable.

4. **Treat an unanswered question as unanswered.** If the response times out or
   comes back empty, write only what was actually answered and tell the user
   which part is still missing and what it would sharpen. Never backfill the gap
   with a plausible default.

5. **Back up, then write SOUL.md.** Prose, not bullets — it is read as identity,
   not as a checklist. Name the agent and the user. Give each standing
   behaviour its own short paragraph with the reason it exists, since a bare
   directive with no rationale gets overridden the first time a task pulls
   against it. Cover at minimum: voice and length, autonomy, candour, honesty
   about unverified results, and where corrections get stored.

6. **Write memory through the memory tool,** batching all entries into one call.
   Phrase entries as declarative facts about the user or environment, not as
   instructions — imperative phrasing is re-read in later sessions as a live
   directive and can override the user's actual current request.

7. **Read the files back from disk and confirm byte counts and content.** The
   memory tool reports usage, not correctness of placement; reading back is what
   proves the entries landed in the intended profile and the intended store.

8. **Report the split and what is still empty.** Close by naming which layer is
   unpopulated (usually skills) and how it gets filled, so the user knows the
   setup is deliberately incomplete rather than finished.

## Retiring a project's knowledge (user restarts a project from scratch)

When the owner says "delete the skills and memories about project X, we restart from
what is on disk", the goal is that no old decision steers the new attempt.

1. **Inventory first, in one pass:** list what is left in the project folder
   (skip `.venv`/`__pycache__`), grep `memories/*.md` for the project name, and
   grep every `SKILL.md` and `references/*.md` for the project name, its
   codenames and its domain words. Hits fall in three groups: project-owned
   skills, generic skills carrying project lessons, and fleet docs (`FLEET.md`).
2. **Rescue tool knowledge before deleting a skill about a kept tool.** A skill
   like "how to run tool Y" holds pitfalls the tool's README lacks; copy the
   tool-only rules (limits, exit codes, path traps) into that README, without
   the project's business context, then delete the skill.
3. **Delete the project-owned skills** (`skill_manage delete`, one per call).
4. **Strip project lessons from generic skills too, by default.** Recipes,
   picks, rejected options and measured comparisons made for the old project
   are exactly the bias the owner wants gone; leaving them and asking costs a
   second round-trip. Keep only facts that hold
   for any project: hardware speed/VRAM numbers, run/stop procedures, API
   quirks, privacy and consent rules, paths to tools that still exist.
5. **Fix every dead pointer** to deleted skills, files and folders (scripts
   included: a hardcoded path to a deleted file becomes an explicit
   placeholder). Re-grep until only tool paths and generic rules match.
6. **Remove the project's section from `FLEET.md`** (planned seats, specs that
   point at deleted files).
7. **Commit** the fleet repo if you keep one, and report: deleted, kept and why, verified
   by grep, and what was not exercised.

## Pitfalls

**Check the profile before every write when profiles are in use.** A named
profile and the default install have identical directory layouts, so a path
built from habit writes to the wrong agent and the change appears to do nothing.

**Keep SOUL.md about behaviour, not knowledge.** Facts placed there cannot be
updated by the memory tool and go stale with no mechanism to correct them.

**Never write an absolute the agent can disprove.** "Only a human can do this,
there is no way for you" becomes a refusal the moment the task is actually
within reach — the agent cites its SOUL against the user and stops trying.
State the real constraint (what needs a human's browser, what needs a paste)
and give the agent the steps around it; dramatic phrasing buys nothing and
costs a working feature.

**Give the agent an explicit missing-tool rule.** Without one, a confined
agent asked for a capability it lacks will silently try to bootstrap it —
downloading packages into /tmp, building venvs — and leave scratch behind with
no report. Write: "If a task needs a tool you do not have, say so in one line
and stop. Never install, download, unpack or build anything to get it." Put it
next to the tool list, not in a separate section.

**Forbid unverified UI click-paths in agents that coach a user through a third-party app.** Models confidently invent menu names ("Settings > Payments") they have never seen, and the user burns a round-trip tapping a menu that does not exist. Write the rule into the agent's skill: state a click-path only when the user's screenshot or an official help page shows it; otherwise name the feature and ask for a screenshot. The adversarial character test is where this surfaces — check for it.

**A SOUL edit does not reach a live gateway session.** The system prompt is
frozen per chat session, so a service restart alone leaves the old text in
play. Restart the service, then send `/new` in the chat, then run the
character test.

**Never write an intention into memory without where it lives.** "A rework is
planned", "we will migrate this later" — with no pointer to the plan, a future
session reads it as established shared context and either invents the missing
detail or asks the user to re-explain from scratch. Either record the intention
with the path or session link that holds the detail, or leave it out; the
intention alone is worse than nothing.

**Reconstruct before claiming recall.** When memory asserts something about past
work, check session history and the artifacts on disk before answering as if you
remember it. Memory is a compressed claim written at one moment; the files are
the current truth, and the gap between them is exactly where a fabricated answer
forms.

**When the user asks for a preference to be remembered, put it in the layer that
governs the task, not only in memory.** Memory states that they prefer it;
the skill is what makes the next session actually do it.
