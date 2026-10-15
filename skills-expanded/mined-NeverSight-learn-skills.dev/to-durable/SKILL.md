---
name: to-durable
description: Harvest the durable value out of a feature's ephemeral findings log, spec, and tickets, before the PR — decisions into ADRs, defects into a known-issues file, vocabulary into the glossary, operating hazards into the agent doc.
argument-hint: "[feature-slug]"
---

# To Durable

A spec and its tickets exist to carry thinking between context windows. Once the feature merges,
nobody asks "what are we building" or "what do I build next" again — so those files stop being
documentation and start being a stale copy of decisions that live elsewhere.

This skill moves what must survive into the repo's durable docs, **before the PR**, so the rationale
lands in the same diff as the code it explains and a reviewer sees both together.

**It does not delete anything.** Deletion happens after the merge, and belongs to the repo's own
documented procedure — see *Handoff* below.

## Where this fits

After `/implement` has finished a feature's tickets, before you open the PR. Run it once per
feature, on the feature branch.

## Process

### 1. Resolve the feature

Derive the slug from the current branch name with any `<type>/` prefix stripped —
`fix/duplicate-payments` → `duplicate-payments` — and check it against `.scratch/`.

If the argument was given, use that instead. If neither resolves to a real directory, **list what is
actually there and ask** — do not guess. A branch can predate the naming convention, or cover two
features.

`.scratch/<feature-slug>/` exists on every repo whatever the tracker is: it holds the findings log and
the test report. Whether the spec and tickets are in there too, or are issues on GitHub or Jira, is
the tracker's business — read `docs/agents/issue-tracker.md` for that.

### 2. Report readiness, then confirm

Read the tickets and report anything that looks unfinished: unchecked acceptance criteria, a status
that is not the tracker's done state.

**Warn; never refuse.** Checkbox state is not a reliable done-signal — tickets routinely ship with
criteria unchecked, and some freeze their checklists deliberately as a record of what was verified at
the time. Show the user what you found and let them decide.

### 3. Survey

**Read `.scratch/<feature-slug>/findings.md` first** — the findings log. It is the primary input,
because it is the only file written *at the moment* something surprised someone. Everything else here
is reconstruction: the spec describes what was intended, the tickets what was planned, and both were
written before the surprises happened.

Then read the spec and **every** ticket, in full. Tickets accumulate implementation notes the spec
never absorbed — a measurement, a reverted approach, a defect found in passing. Those notes are
frequently the most valuable thing in the directory, and the first thing lost.

A findings log with entries already marked `→ <destination>` has been curated before. Those are
done; work the unmarked ones.

### 4. Propose, then stop

Four categories. Propose concrete entries for each, then **stop and wait for approval** — deletion
downstream is irreversible, so a bad extraction cannot be corrected later.

**Decisions → an ADR.** Write to **anti-inference**: an ADR earns its length only by carrying what a
reader cannot infer from the code in front of them.

> Would a competent reader, working from the code alone, independently arrive at the opposite?

If no, cut it. The full keep/cut lists and the two corollaries live in `/domain-modeling`'s
`ADR-FORMAT.md`, which governs every ADR this project writes — follow it rather than a second copy
of the rule here.

**Defects → a known-issues file.** Defects and accepted coverage gaps discovered while building and
deliberately not fixed. Not design rationale, and not a backlog. These are silently lost otherwise,
because nothing else records them: a bug in a neighbouring module, a check that could not be
verified, a test the team decided not to write and the consequence they accepted.

**Vocabulary → the glossary.** Terms the feature introduced or sharpened, in whatever format the
glossary already uses. Terms the spec used consistently but the glossary never defined are the ones
to look for. General programming concepts do not belong there however heavily the project uses them
— the glossary is domain language only.

**Operating hazards → the repo's agent doc.** A fact about the tooling or environment that will
mislead the next agent, as opposed to a fact about our design or our defects. Its tell is that the
fix is a warning rather than a ticket: nobody is going to "fix" the ORM that drops an `undefined`
filter key instead of matching nothing.

This bucket is **residual** — check `docs/agents/` first and route to whichever file already owns the
subject. Test constraints belong in `testing.md`, VCS conventions in `vcs.md`. Only what no existing
doc owns lands in `CLAUDE.md` / `AGENTS.md`, and then **co-located with the section it concerns**
rather than in a gotchas pile, because a hazard collected into a list is one nobody reads at the
moment it would have helped.

Two further rules for this bucket:

- **A hazard whose violation causes damage is one entry in two halves.** A guardrail line goes in the
  always-loaded agent doc — worded so the wording itself does the triggering — and the detail goes in
  the `docs/agents/` file that owns the subject. Not duplication: the guardrail carries the trigger,
  the body carries the detail. An agent can run the destructive command at any moment, including one
  where it never opened the detail file.
- **Length gates the destination.** Short and firing unpredictably → always-loaded. Long, or scoped
  to one activity you can name → behind a pointer in `docs/agents/`.

### 5. Write

Write only what was approved. Create the known-issues file lazily if the repo has none. Stage the
result so it rides in the PR rather than trailing it.

If a decision belongs in an ADR that already exists, extend that ADR rather than adding a second one
on the same subject.

**Mark each extracted finding in place**, appending its destination to the line rather than deleting
it:

```
- Prisma drops an `undefined` filter key … [implement] → CLAUDE.md
```

Two reasons. A second run is then idempotent — it can tell settled from unhandled without re-reading
every destination file. And the log stays a complete record of what was found, which is what makes
an *unmarked* line at merge time meaningful: it was judged not worth keeping, deliberately, by
someone who looked at it.

A finding that is no longer true — fixed in this branch, or wrong when written — is marked `→
dropped` with the reason, never silently removed.

### 6. Commit what you wrote

Commit the durable files with `/commit`, on the feature branch, before `/pr` runs.

`/pr` computes its scope from **committed** work, and skipping this errors nowhere: the files are on
disk, the PR opens, and only the rationale is missing.

`/pr`'s staleness check also excludes `docs/` on the assumption that a docs-only commit sits
immediately before every PR. This step is what puts it there.

### 7. Report

Name the durable files written, and stop. There is no manifest to append anywhere.

Deletion happens after the merge and needs no list from you: the durable files this feature produced
are derivable from the merged range, so writing them down would be a cache of a one-command lookup.

```bash
git diff --name-only <merge-base> <merge-commit> -- docs/ CLAUDE.md AGENTS.md CONTEXT.md
```

`/workflow`'s *After the merge* section owns that procedure.

## Repo conventions win

Read the repo's own agent documentation first if it has any — an issue-tracker doc for where specs
and tickets live, a domain doc for ADR location and numbering. Where the repo states a convention,
follow it. This skill supplies the method; the repo supplies the file layout.

Where the repo says nothing: ADRs in `docs/adr/` numbered sequentially, known issues in
`docs/known-issues.md`, glossary in `CONTEXT.md`, hazards in `CLAUDE.md` or `AGENTS.md`. The findings
log is always `.scratch/<feature-slug>/findings.md` — that one is not a repo convention.

ADR *length* is not a repo convention — anti-inference governs it everywhere, from
`/domain-modeling`'s `ADR-FORMAT.md`.

## Anti-goals

- **Do not summarise the spec.** A summary is a third copy that drifts. Extract only what prevents a
  future mistake; let the rest die with the file.
- **Do not delete, move, or archive the spec or tickets.** Not even after a successful extraction.
- **Do not restate an ADR's argument at the call site.** Point at it in one line. Two copies drift,
  and the code copy is the one nobody updates.
- **Do not pad to look thorough.** A feature with one real decision gets one short ADR, no
  known-issues entries, and no new vocabulary. That is a successful run.
- **Do not write a finding to two destinations.** Each line gets exactly one home. A defect that is
  also a hazard is a defect; a hazard that is also a test constraint belongs to `testing.md`. Pick
  the one an affected reader would look in, and only then consider whether a guardrail line is owed.
- **Do not carry an ephemeral reference into a durable file.** This is the step most likely to do it:
  every finding you are extracting arrived with a ticket, a spec and a slug attached, and the phrasing
  comes along for free. A committed file may not name a ticket, a spec, a feature slug or a
  `.scratch/` path — not in an ADR, not in known-issues, not in the glossary, not in a code comment.
  State the fact, not where it was decided; see `ADR-FORMAT.md`'s *Reference nothing ephemeral*.
