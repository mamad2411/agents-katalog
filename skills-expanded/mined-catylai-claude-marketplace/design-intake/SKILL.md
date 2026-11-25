---
name: design-intake
description: "Classifies a build request as a spike, a bounded change or an architectural change, runs the matching depth of design, and stops for explicit approval before implementation; the architectural path writes a spec to docs/specs/ and hands off to writing-plans. Use when starting a new project, subsystem or service, redesigning how components fit together, or when asked to design or spec something before coding. Not for routine edits to an existing flow; not for bugs (use root-cause); not for a time-boxed POC (use project-scaffold:poc-start) or recording a past decision (use project-scaffold:adr-init)."
when_to_use: "new service, new subsystem, new project, redesign this, how should we structure this, design it before we code, turn this idea into a spec, write a spec for, architect this"
argument-hint: "[what you want to build]"
allowed-tools: Read, Grep, Glob, Bash(git log *), Bash(git status *), Bash(date *), Edit(docs/specs/**), Edit(docs/adr/**), AskUserQuestion
license: MIT
---

# Design intake

Turn a request into a design, and a design into an approved intent, before anything is built.

The request: $ARGUMENTS

This skill decides how much design the request needs, does that much, and waits for a human yes
before implementation starts. It applies to the request it was invoked for; routine edits to an
existing flow do not need it.

## The gate

Once this skill is running, state what you intend to build and wait for explicit approval before
writing code, scaffolding, a file layout, or adding a dependency. The artifact scales with the
task — two sentences in chat for a small change, a written spec for a new subsystem — but the
approval step does not. Presenting a design and starting in the same message skips it.

Approval is to a stated intent. If you cannot quote what the human approved, ask again.

## Classify first, and say it out loud

Before the first clarifying question, pick a path and announce it with the reason in one
sentence, so the human can override it:

> "This looks bounded — the retry logic already lives in `client/fetch.ts`, so I'll present a
> short design here rather than write a spec."

**Spike** — a feasibility question whose output is an answer, not kept code ("can we…", "would
this library work"). Present the question and the probe in two or three sentences, get a nod,
find out as cheaply as correctness allows, and report a recommendation. Anything built stays
labelled throwaway; keeping it is a new request. A request that also asks for a time box, a
falsifiable success signal and kill criteria is a proof of concept — hand it to
`project-scaffold:poc-start`.

**Bounded** — a well-scoped change to a flow that already exists in this repository: a new flag,
one more endpoint on an existing router, a field on an existing schema. Bounded measures the
repository, not your familiarity with the problem: with no existing flow to open and change, the
task is not bounded, and a new project never is. Procedure: the clarifying questions that matter →
a short design in chat (approach, files touched, how it will be tested) → wait for yes →
implement normally. No spec file.

**Architectural** — new projects, new subsystems, changes that restructure how components fit
together, or changes to an interface something else depends on. Run the full path below.

When unsure between two paths, take the heavier one. Hidden complexity found mid-task upgrades the
path: stop, say what you found, re-classify and re-present. Each task gets its own classification
and approval — approving a spike does not approve building what it proved possible.

## The architectural path

Create a todo per step and work them in order.

1. **Explore the project context.** Run `git log --oneline -10` and `git status -sb`; use Glob for
   the top-level layout, `README*` and `CLAUDE.md` within two levels, `docs/adr/*` and
   `docs/specs/*`. Read the conventions files and any ADRs touching the area. Design from what you
   read, because a confident design for an unread codebase is internally consistent and wrong.
   **Without a checkout (Cowork/web):** ask the user to paste the layout, README and relevant ADRs,
   and wait for them.
2. **Decompose scope first.** If the request describes several independent subsystems, name them,
   say how they relate, propose a build order, and take only the first through this path. Each
   sub-project gets its own spec, plan and implementation cycle.
3. **Ask clarifying questions one at a time**, multiple choice where the answer space allows,
   aimed at purpose, constraints and what counts as success.
4. **Propose two or three approaches** with trade-offs, leading with your recommendation and why.
   Strip speculative features from each before presenting.
5. **Present the design in sections** — architecture, components, data flow, error handling,
   testing — a few sentences each, up to two or three hundred words where genuinely nuanced. Ask
   after each section whether it looks right. Design for isolation: each unit has one purpose, a
   statable interface and known dependencies. In an existing codebase follow its patterns, and
   include only the refactoring the change actually needs.
6. **Write the spec** to `docs/specs/<YYYY-MM-DD>-<topic>.md`, with the date from `date +%F`. An
   existing repository convention (for example `docs/design/`) wins; say so if you use it.
7. **Self-review the spec inline**, once, fixing as you go:

   | Pass | Look for | Fix |
   | --- | --- | --- |
   | Placeholders | "TBD", "TODO", empty sections, intentions phrased as requirements | Write the content |
   | Consistency | Sections that contradict each other | Reconcile, and say which was wrong |
   | Scope | Too broad for one plan | Return to step 2 |
   | Ambiguity | A requirement readable two ways | Pick one reading and state it |

8. **Human review.** "Spec written to `docs/specs/<name>.md`. Please read it and tell me what to
   change before I write the implementation plan." Wait; apply changes and re-run step 7.
9. **Hand off to `writing-plans`** once the spec is approved. That is the only next step on this
   path, so the design phase does not leak straight into code.

## Specs and ADRs

A spec describes one piece of work. An ADR records one decision that had real alternatives.
`project-scaffold:adr-init` owns the ADR convention: `docs/adr/NNN-kebab-title.md`, three-digit
sequential numbers, an index at `docs/adr/README.md`, and Context / Decision / Consequences
sections with a Status line.

- If an ADR already settles a question the design is re-opening, say so and get that
  acknowledged before continuing.
- A design that reverses a recorded decision amends or supersedes that ADR in the same change.
- A design that makes a new lasting decision gets its own ADR (`Status: Proposed` until it lands),
  numbered after the last existing file and added to the index; the spec links to it rather than
  restating the rationale.
- If the repository has no `docs/adr/`, keep the rationale in the spec and mention
  `project-scaffold:adr-init` as an option; adopting ADRs is its own decision.

Test for which record: would the choice outlive this feature, and would a future engineer ask "why
is it like this"? Then it is an ADR.

## Terminal states

| Path | Ends with | Next |
| --- | --- | --- |
| Spike | A recommendation, anything built labelled throwaway | Nothing; keeping code is a new request |
| Bounded | An approved short design | Normal implementation |
| Architectural | A spec the human has read and approved | `writing-plans` |

## Verify

Before handing off, confirm: the classification was announced; you can quote the approval; on the
architectural path the spec file exists, has no placeholders, and links any ADR it relies on.

## Examples

<example>
Request: "Add a `--dry-run` flag to the sync command."
Announce bounded — `cli/sync.ts` exists and is the flow being changed. Ask the one question that
matters (print the plan, or exit non-zero on drift?). Present four sentences: the flag, the file,
the branch it short-circuits, the test. Wait for yes.
</example>

<example>
Request: "Build us an internal billing platform."
Announce architectural, then decompose before detailed questions — metering, rating, invoicing,
payment capture and reporting are five sub-projects with five specs. Propose an order and take the
first through the path.
</example>

<example>
Request: "Can we use SQLite for the local cache instead of the JSON file?"
Announce spike: "The question is whether SQLite's write concurrency holds under the CLI's parallel
workers. I'll write a throwaway harness running eight writers against both and report the failure
rate. Sound right?" If they then want it built, re-classify — probably bounded.
</example>

<example>
Halfway through a bounded change, "one more endpoint" turns out to need a new auth scope in the
token issuer that three other services read.
Stop: "This has crossed into architectural — it changes an interface other services depend on.
I'm re-classifying and going back to the design step."
</example>
