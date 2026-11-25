---
name: repo-walkthrough
description: "Gives a read-only guided tour of an unfamiliar repository that leaves the reader able to contribute safely: a hypothesis from the manifests, a structure map, the patterns in use contrasted with the naive alternative, one flow traced end to end, and the traps a newcomer is likely to hit. Use when joining a project, orienting before a first change, or asked how a codebase works. Not for reviewing a specific diff (use code-review-core:review-scan); not for auditing Claude Code configuration (use agent-craft:config-audit)."
when_to_use: "walk me through this repo, explain this codebase, I am new to this project, how does this system work, where do I start, orient me in this repository"
argument-hint: "[repository path; defaults to the current directory]"
allowed-tools: Read, Glob, Grep
disallowed-tools: Write, Edit, NotebookEdit
license: MIT
---

# Repository walkthrough

Tour the repository at: $ARGUMENTS (if empty, the current directory; if the path does not exist,
say so in one line and stop).

The reader should finish knowing what the system does, why it is built the way it is, and what
not to get wrong in a first change. This is a read-only task: work through the steps, then give
the complete report in the template at the end, written to stand alone.

**Without a checkout (Cowork/web):** if there is no repository to read, ask the user to paste the
root file listing, the README, the package manifest, and the main entry file, and wait for them.
When the arguments or the conversation already carry that content, tour it instead, and cite
the pasted file names where the template asks for `path:line`.

Apply the teaching method at the end of this file throughout; it is the point of the skill.

## Step 1 — Orient before reading source

Read the root listing, the README and the manifests (package descriptors, build files, CI
configuration, container definitions) before any source, so that reading source confirms or
corrects a hypothesis instead of piling up unattached detail. Establish: what the system does in
one sentence; language, runtime and framework; the entry point; external dependencies; and its
shape — library, service, CLI or monorepo.

State the hypothesis ("from the manifests this looks like a *type* that *does X*"), and later say
where it turned out wrong. That correction teaches more than getting it right first time.

## Step 2 — Map the structure

Walk the tree without reading contents. Find where the business logic, entry points, data models
and tests live, and any directory that breaks the stack's conventional layout — that is where the
project's real decisions usually hide. Produce an annotated tree, one line per top-level entry.

## Step 3 — Name the patterns

Read the significant source files and identify each architectural or design pattern actually in
use. For each:

- **Name it precisely** — "a repository pattern", "a circuit breaker", not "some abstraction".
- **Give a structural analogy** that maps parts to parts, and say where it breaks down.
- **Say what it is for** here, and what would be worse without it.
- **Show the contrast** — the naive approach a competent newcomer would reach for, and the
  concrete way it fails in this codebase.

Places worth checking (report what is present, not this list): dependency injection, data access,
middleware and decorators, events versus request-response, configuration and secrets, error
strategy, retry and idempotency, where auth is enforced, test strategy, build and deploy shape.

## Step 4 — Trace one flow end to end

Pick the most important operation (a request, a consumed message, a command run) and trace it as
a numbered list: entry, validation, transformation, side effects in order, exit. Annotate each
non-obvious step with its file:line and what happens on the failure path.

## Step 5 — What a newcomer is likely to break

Name three to five: invariants nothing enforces, code that looks wrong but is correct, the obvious
refactor that breaks something subtle, external contracts with consumers outside the repo, and
tests that look complete but miss important paths. For each: the mistake, what breaks, what to do
instead.

## Report template

Return exactly this structure. Cite `path:line` for every claim about the code, so the reader can
check it.

```markdown
# <repo name> — walkthrough

## Hypothesis
<one sentence from the manifests> — **Correction:** <where it was wrong, or "held">

## Structure map
<annotated tree, one line per top-level entry>

## Patterns
### <Pattern name> — `path:line`
- Analogy: <parts-to-parts mapping; where it breaks>
- Why here: <problem it solves>
- Naive alternative: <what a newcomer writes> → <concrete failure>

## Flow: <operation>
1. <step> — `path:line` — on failure: <what happens>

## Traps for a first change
| Mistake | What breaks | Do instead |
| --- | --- | --- |

## Mental model (two-minute read)
<what it does, the three or four patterns that matter, the first files to read>
```

## Verify

Before answering, confirm every `path:line` in the report came from a file you read in this run,
and that the Hypothesis section has its correction filled in.

---

## Teaching method

Lead with the mental model: give the reader a frame they already hold, name the pattern, then show
this code as an instance of it.

- Explain why code was written that way and what breaks without it, not only what it does.
- Use real names and numbers from the codebase in analogies; generic analogies are forgotten.
- Flag what is genuinely surprising: "this is counterintuitive — here is why it is correct."
- Call out technical debt and aged decisions directly, with reasoning.
- Spend depth where the reader is most likely to hold a wrong model, and skip what they know.

<example>
Weak analogy: "the auth middleware is like a box that holds things."
Strong analogy: "it is like a bouncer at a door — it checks the list, not what you want inside;
the policy (`policies.yaml`) is separate from the enforcement (`auth.ts:40`), so the guest list
changes without retraining the bouncer. It breaks for background jobs, which never pass the door —
those check scopes in `jobs/runner.ts:112` instead."
</example>

<example>
Weak contrast: "doing it directly could cause issues."
Strong contrast: "a newcomer would call `db.save()` inside the handler. Two retries of the same
webhook then insert two rows, because the idempotency key is only checked in
`outbox.ts:57` — the invariant is 'every write goes through the outbox'."
</example>
