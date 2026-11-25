---
name: family-workflow
description: "Choose and explain a whole-effort development workflow, FAMILY — Frame, Architect, Make, Inspect, Launch, Yield — and pick which of four profiles fits: solo, developer, QA or team. Each stage has a gate, an artifact and a handoff. Use this skill when someone wants an end-to-end process and has not chosen how to run it. Triggers include choosing a development workflow, planning a feature from problem to release, asking what the stages are, or building software with no process — or phrasings like \"how should we structure this project\" or \"which workflow fits us\". Once the profile is known, hand off: one person to solo-development, a developer's loop to developer-workflow, QA's part to qa-workflow, a team's owners, handoffs and cadence to team-workflow. Not for reviewing a change (code-review), an API (api-design), a test strategy (test-design), or leading people (growth-review)."
allowed-tools: Read, Write, Edit, Grep, Glob, Bash(git:*)
---

# The FAMILY workflow

**Frame · Architect · Make · Inspect · Launch · Yield** — six stages that take an idea to a measured outcome, each with one gate, one artifact and one handoff, run at the depth the person or team actually needs.

A development effort is finished when each stage's gate was passed or, for Architect and Launch only, waived in writing, the artifact it produced exists, and the handoff to the next stage names who owns it. The point of naming the stages is that every failed project fails at one of them, and the failure is usually a skipped handoff rather than bad work: the build starts before the problem is framed, the release ships before the change is inspected, the retro never happens so the same defect returns. FAMILY makes the six decisions explicit and lets you choose how heavy each one is. A solo developer runs all six in an afternoon; a team of ten gives each a different owner.

## The six stages

| Stage | The decision it owns | Artifact | Agent |
| --- | --- | --- | --- |
| **Frame** | What problem, for whom, what "done" means, and the smallest valuable slice | A one-page frame: problem, users, success criteria, slice, out of scope | `framer` |
| **Architect** | The approach, the boundaries, the interfaces, and the recorded decision | A short design note and the ADR | `architect` |
| **Make** | The order the slice is built in, and the proof each step carries | An ordered, file-level change plan | `maker` |
| **Inspect** | Whether the change meets its frame, and is safe and accessible; the Inspect owner also owns the go/no-go that closes it | Criterion-by-criterion evidence from `inspector`; severity-ranked findings from `code-review` | `inspector`, and `code-review` for the diff |
| **Launch** | Whether the change is ready to reach users, and how it comes back | A launch plan: migration, monitoring, rollback | `launcher` |
| **Yield** | What the outcome teaches the next slice | A short retro feeding Frame | `yielder` |

Read `references/stages.md` for each stage's gate, the questions it must answer, the skills it routes to, and the failure it prevents.

## Choosing the profile and the depth

The stages do not change. A profile is the role running them; the depth is light or full, chosen per slice and written in the frame. Read `references/profiles.md` to choose, then read the profile's own skill for how to run it.

- **Solo** — one person, all six stages, usually light. The agents act as independent checkers so a single head does not review its own work. Read `solo-development`.
- **Developer** — Frame, Architect, Make and Yield owned; Inspect and Launch handed to a reviewer and a release owner. Read `developer-workflow`.
- **QA** — Inspect owned, with acceptance criteria and testability pushed back into Frame and Architect. Read `qa-workflow`.
- **Team** — all six with named owners, a handoff contract between each, and a cadence that runs Yield on a schedule rather than when someone remembers. Read `team-workflow`.

## Workflow

### 1. Pick the profile, then the slice

Name the profile, the depth (light or full) and the one slice of work this run covers, and write the depth in the frame. FAMILY is for a slice, not a roadmap: one user-visible change, end to end. A run that tries to cover a quarter is really several runs.

### 2. Run the stages in order, and do not skip a gate silently

Each stage's gate is a question with a yes or no answer, in `references/stages.md`. Passing it moves on; failing it returns to the stage before. Only Architect and Launch may be waived, and only in writing with the reason and the risk; the `Waivable` line of each stage in the reference says when. The failure FAMILY exists to stop is the gate skipped without anyone noticing.

### 3. Hand off explicitly

Every stage ends with a handoff: the artifact, who owns the next stage, and the next stage's `First question` from the reference. The Inspect to Launch handoff opens with the go/no-go, which the Inspect owner answers once. A handoff that is a document with no owner is where work stalls.

### 4. Delegate the reading to the stage's agent

Where a stage needs reading the main conversation does not want back — a frame from a long thread, an architecture from a codebase, a plan from a design, findings from a diff, a launch check from config, a retro from outcomes — delegate to that stage's subagent and keep the conclusion, not the material. The agents have no editing tools by design: they decide and report, and the main agent writes. `inspector` can also run commands, so it runs checks only on a change the owner wrote.

### 5. Close the loop

Yield is not optional. Every run ends by feeding its outcome back into Frame: what the success criteria measured, what to keep, and the next slice. A run with no Yield repeats its mistakes with more confidence.

## Anti-patterns

**Skipping Frame.** Starting to build before the problem, the user and the definition of done are written down. The most expensive stage to skip, because every later stage builds on it.

**Architecture as ceremony.** A design note nobody reads, written after the decision was already made. Record the decision and the alternative that lost, in a page, not a deck.

**Make without a plan.** Coding before the slice is broken into steps with a proof each. The change becomes one large commit that cannot be reviewed or rolled back.

**Inspect by the author alone.** Self-review finds what you already believe. The inspector is independent and has no editing tools, so it reports rather than fixes.

**Launch as "git push".** No migration, no monitoring, no rollback. A release with no way back is a bet, not a launch.

**The missing Yield.** Shipping and moving on, so the team learns nothing and the same defect returns in the next slice.

**One depth for everyone.** Running a solo developer through a ten-person team's ceremony, or a team through a solo developer's shortcuts. The stages are fixed; the depth is chosen per slice.

## References

- `references/stages.md`: read at step 2 for each stage's gate, first question, waiver rule, the questions it answers, the artifact, the agent, and the skills it hands detail to.
- `references/profiles.md`: read at step 1 to choose among the four profiles — solo, developer, QA and team — and between light and full depth, and the skill each one routes to.
- `references/slice-folder.md`: read at step 3 for the `docs/slices/<name>/` folder, one file per stage artifact, each opening with its stage's first question; the `/family` command creates it.
- `references/pull-request-template.md`: read at step 3 when a repository adopts FAMILY, for a pull request template that carries the six artifacts and the stage labels.
- `solo-development`, `developer-workflow`, `qa-workflow`, `team-workflow`: read the one the profile names for its full procedure, gates and handoffs.
