---
name: using-gabrielmoreira-skills
description: >-
  Read at the start of every session, before any other skill, and again after
  any compaction, model change, resume, or handoff. Routes the work to the
  right skill in this collection and holds one person's decisions rather than
  a recommendation: where generated files go, which skill wins when two match,
  which borrowed collections are trusted, where the ceremony is not wanted, and
  what the portable skills deliberately leave open. Machine-specific on
  purpose. Not a summary of the other skills, and not a substitute for reading
  the one that matched.
---

# Using Gabriel Moreira's Skills

**Core principle.** The other skills say how to do the work. This one says how *I* want it done, and it is the only file here that is allowed to be opinionated.

- **Nothing here is a recommendation.** It is one person's configuration, named after him so nobody mistakes it for advice.
- **The skill that matched still owns its subject.** This resolves what that skill left open, and never overrides it.
- **You opened this in the middle of something.** This is how to do that work, not a replacement for it. Name what you were doing before you start, and return to it when this is done.

## Routing the work

**Match the work to a row and open that skill.** Then come back here only for what the matched skill left open.

| When the work is | Open |
| --- | --- |
| a change to judge before it lands: a branch, a pull request, a diff against a base point, or uncommitted work | `evidence-backed-review` |
| something failing, flaky, hanging, or newly slow, with the cause not yet established | `debugging-by-evidence` |
| a feature or bugfix about to be implemented, or a test written after the code | `test-first-by-evidence` |
| a tool, runtime, install, auth, or network failure that is not the change being made | `treat-blockers-as-incidents` |
| a git operation that refused, a state you cannot name, or work about to be deleted or cleaned up | `keep-git-work-recoverable` |
| written material to create, correct, place, or remove, including whether a decision is worth recording | `make-the-docs-trustworthy` |
| code that should stay simple and testable: boundaries, cohesion, layering, hidden effects, abstraction added too early | `maintainable-code` |
| TypeScript specifics: standards, boundaries, composition, config, async, errors, observability, security, testing | `typescript-skills` |
| an answer that is dense, buried, or hard to resume | `progressive-reading` |
| a skill to write, split, rename, or check, or one that never fires | `authoring-verifiable-skills` |

- **Boundaries, so they do not fight.** Review judges a change that already exists; debugging establishes a cause when there is no change yet; once a fix exists it becomes a change again. `maintainable-code` owns language-neutral structure and only material architecture work; `typescript-skills` owns the ecosystem and is the primary one when both apply. Docs inside a diff belong to review; docs on their own belong to `make-the-docs-trustworthy`.
- **Other skills may fire alongside these.** On a procedure conflict, follow the one more adequate to the situation and say which one lost.

## Where generated files go

| What | Where | Committed |
| --- | --- | --- |
| scratch, temps, generated plans, abandoned investigations | `.local/` at the repository root | never |
| a learning anyone cloning this repository would need | `docs/learnings/` | yes |
| a learning only this machine has | `~/.agents/learnings/` | never |
| anything a skill produces and does not place | ask, then record the answer here |

- **`.local/` is ignored, in `.gitignore` or in the exclude file.** Set that up before writing to it.
- **One question decides between the two learnings directories.** Would a colleague cloning this repository hit the same thing? Yes goes inside, no goes outside.
- **Report the path chosen and whether it is tracked**, every time.

## Which skill wins

**Only genuinely ambiguous pairs belong here.** Everything else is settled by the skills themselves.

| Situation | Open | Not |
| --- | --- | --- |
| a command failed for a reason that is not the change being made | `treat-blockers-as-incidents` | `debugging-by-evidence` |
| a test fails because the behaviour is missing | `test-first-by-evidence` | `treat-blockers-as-incidents` |
| a defect in the code being changed | `debugging-by-evidence` | `treat-blockers-as-incidents` |
| where a test goes for behaviour being added | `test-first-by-evidence` | `debugging-by-evidence` |
| where a test goes to pin a defect | `debugging-by-evidence` | `test-first-by-evidence` |
| judging work that already exists as commits | `evidence-backed-review` | `maintainable-code` |
| designing work that does not exist yet | `maintainable-code` | `evidence-backed-review` |

- **Two or more matching is normal.** Process comes before implementation, and the narrower one wins where they overlap.
- **Not finding a match is an answer.** Do not stretch one to fit.
- **My own skills come first**, ahead of any borrowed collection, because they are being validated against real work.

## Discussion is not authorization

- **Analysis, alternatives, proposals and plans do not authorize anything.** Change code, configuration, infrastructure or external state only after I say to implement, apply, change, or select.
- **After a compaction, a model change, a resume, or a handoff, every prior proposal is pending again** unless the authorization is still visible in the active context.
- **Where authorization is unclear, ask one specific question** before touching anything.

## What I do not want

- **No ceremony on a one-line change** whose failure mode is visible on reading it.
- **No workaround reported as a fix.** Say the tool is broken and let me decide.
- **No review that closes on local test and lint output.** Numbers are not a judgment.
- **No skill's procedure replacing the thing I asked for.** Answer what I asked, then say what else you found.
- **No em dash anywhere**, in any file, in any message.

## Defaults the portable skills leave open

- **The primary agent is omp.** Others are secondary, and a procedure that only works in one of them is not finished.
- **Skills are not proven until a run shows it.** A green structural suite says the files are well formed and nothing about behaviour.
- **A number without its interval invites reading noise as movement.** Report both.
- **Where a measurement and my opinion disagree, the measurement wins**, and the opinion gets rewritten here.

## Hooks, when they exist

- **Nothing here installs itself.** No configuration is written, and no session tool is registered without being asked.
- **Where the harness offers a way to re-read this between turns, propose it and let me decide.** An instruction that only lives in the system prompt is read once and forgotten by some models.
- **Until then, name the procedure you are following in your first line of work**, so a lapse is visible to me rather than silent.

## Routing

- **This file resolves; it does not instruct.** The matched skill owns its subject.
- **Where this file has no answer, say so** rather than inventing one, and the gap gets filled here.
- **A direct instruction from me outranks anything here.**
