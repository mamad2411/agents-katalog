---
name: architecture-decision-records
license: MIT
description: >-
  Records, supersedes and retrieves architecture decision records (ADRs) in
  MADR 4.0.0 format. Use when a session settles a significant, hard-to-reverse
  choice between alternatives; when the user says "record this decision",
  "write an ADR" or "supersede ADR-0003"; when asked "why did we choose X?";
  before changing code that an accepted ADR governs; or when archiving a merged
  spec as an ADR. Offers first and never writes files without explicit consent.
compatibility: >-
  MADR 4.0.0 (adr/madr, released 2024-09-17). scripts/adr-scan.sh needs Bash
  3.2+, POSIX find/sed/awk, and git for history-aware numbering.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
---

# Architecture Decision Records

Capture why a significant decision was made, in MADR 4.0.0, at the moment it is
made. Answer later "why did we choose X?" questions from the records instead of
from memory. Records are durable project memory for people and agents. A wrong
or invented rationale is worse than no record, so evidence rules come first.

When the MADR format itself matters (field names, status values), verify against
the canonical [MADR site](https://adr.github.io/madr/) and the
[4.0.0 template](https://github.com/adr/madr/blob/4.0.0/template/adr-template.md).
Being wrong would mislead every later reader.

## Consent gate

Applies to every write below: new records, the index, status edits and
directory setup.

1. **Offer, don't write.** At a decision moment, say in one or two sentences what
   you would record and ask. Example: "That settles queue vs. cron polling.
   Record it as ADR-0007?" Offer once per decision. If the user declines or
   ignores it, drop it and write nothing.
2. **Show before writing.** Present the full draft, the target path, the index
   row, and any edit to an older record. Write only after an explicit yes. A yes
   to "record it" covers that draft. It does not cover unrelated edits, a commit,
   or a push.
3. **Retrieval is read-only.** Answering questions never needs consent and never
   writes.

## Decision moments

Offer a record when the session:

- chooses between two or more viable options for structure, a dependency,
  framework or service, a data model, an interface or protocol, a deployment
  topology, or a security or compliance posture;
- accepts a quality trade-off (latency vs. cost, consistency vs. availability);
- makes a choice that is costly to reverse or that other teams will build on;
- rejects a tempting option for a reason that someone will otherwise rediscover
  ("we tried X, it fails because …"). Rejections are worth recording too;
- reverses or contradicts an existing accepted ADR (offer a superseding record).

Do not offer for routine, local or easily reversed choices: naming, formatting,
a library's internal API, a bug fix, or anything the code already states
plainly. One decision per record. Split multi-part decisions.

## Locate the records

Run the scanner from the repository root before numbering, drafting or
answering:

```bash
bash <skill-dir>/scripts/adr-scan.sh next    # dir, exists, index, style, highest, next, others
bash <skill-dir>/scripts/adr-scan.sh list    # number, status, date, title, path (TSV)
bash <skill-dir>/scripts/adr-scan.sh check   # duplicate numbers, unindexed records
```

`<skill-dir>` is this skill's installed directory. The scanner honours an
adr-tools `.adr-dir` file. It then checks, in order: `docs/adr`,
`docs/decisions`, `doc/adr`, `docs/architecture/decisions`,
`docs/architecture-decisions`, `adr`, `decisions`. With no records anywhere, the
default is `docs/adr/`. If `others=` is non-empty, the repository has several
ADR directories. Ask which one is authoritative and don't merge them.

If the scanner cannot run, compute the same result by hand. Do not skip the
history check.

### Numbering and file names

- **Use `next=`.** It is one above the highest number in the files, the index
  links, `ADR-NNNN` mentions in the index, and ADR files anywhere in git history
  on every local and fetched ref. Numbers are never reused. A deleted record or
  an unmerged branch's record keeps its number. Gaps are fine.
- **Branch collisions.** Two branches can still claim the same number. Run
  `git fetch` first when the user agrees. If `check` reports a duplicate after a
  merge, renumber the record that has not merged yet. Never renumber a merged
  one.
- **Name style.** New directories use `NNNN-title-with-dashes.md`, which is
  MADR's convention: four digits, lowercase, imperative or noun phrase.
  Existing directories keep their style. `style=adr-NNNN-` means the
  repository uses the legacy `adr-NNNN-slug.md` names, so match them. Never
  rename existing files.

### Existing formats

Follow an established house format if the directory already has one: Nygard
(`## Status` / `## Context` / `## Decision` / `## Consequences`), the coded
`POS-001` / `NEG-001` style, or another. Consistency inside one log beats
conversion. Never rewrite old records into MADR. Use MADR for new logs, or when
the user asks for it.

## Record a decision

1. **Gather evidence.** Use only the session, the user, and repository
   artefacts (issues, PRs, specs, benchmarks, code). For each MADR field, note
   where its content came from.
2. **Ask before guessing.** If drivers, options or the reason for the choice are
   missing, ask one compact round of targeted questions. Anything still unknown
   is written as `Not recorded — <the open question>`. It is never filled in
   with plausible text.
3. **Draft from [assets/madr-4.0.0-template.md](assets/madr-4.0.0-template.md).**
   Delete unused optional sections and the template comment. House rules on top
   of MADR:
   - `status: "proposed"` unless the user confirms the decision is made, in
     which case use `"accepted"`. `date` is today, in ISO format.
     `decision-makers` lists only people the user names. Don't infer them from
     git authors.
   - **Drivers first.** The outcome sentence repeats the chosen option's title
     verbatim from Considered Options. Its `because` clause names at least one
     driver.
   - **Real alternatives only.** Each option was seriously considered and
     appears in the evidence. Never add a straw-man option. Doing nothing is a
     real option only if someone proposed it.
   - **Honest consequences.** List at least one `Bad, because` for the chosen
     option, or state plainly that none was identified. Each rejected option
     gets the reason it lost.
   - **Confirmation** names a real check (a test, a lint rule, a review gate).
     Otherwise delete the section.
   - **Retrospective records** use today as `date`. State the original decision
     date and source in More Information.
   - Keep it short: about a page. Link detailed design. Don't paste it in.
4. **Self-review before showing.** Use the quality check below. Fix what fails,
   or flag it to the user.
5. **Show and confirm** under the consent gate, then write. If a user-confirmed
   new directory has no index, create
   [assets/index-template.md](assets/index-template.md) as `README.md` there.
6. **Update the index.** Add one row: `| [NNNN](<file>) | Title | status |
   YYYY-MM-DD |`. `<file>` is the exact basename just written, so it includes
   the `adr-` prefix when `style=adr-NNNN-`. `check` matches index links to
   file names exactly. If the repository has an `index.md` (adr-log, log4brains),
   or a generated log marked `<!-- adrlog -->`, follow that convention or its
   generator instead.
7. **Verify.** Run `adr-scan.sh check`. Confirm every relative link in the new
   record resolves. Report the path and number. Don't commit unless asked.

## Supersede, deprecate or reject

Accepted and rejected records are immutable. A change of mind is a new record.

- **Supersede.** Write the new record under the consent gate. Its More
  Information says `Supersedes [ADR-NNNN](<old-file>)` with the reason, where
  `<old-file>` is the old record's actual basename from `list`. In the
  old record, change only two front-matter fields: `status: "superseded by
  ADR-MMMM"` (MADR expresses supersession only through status) and `date`.
  Nygard-style records get the same status line under `## Status`, followed by
  a link to the new record. Update both index rows. Show the old record's diff
  before applying it.
- **Deprecate.** Set the status to `deprecated` and update `date`. Add one
  sentence in More Information saying why, and what replaces the decision, if
  anything.
- **Reject.** A proposal turned down is kept with `status: "rejected"` and its
  reason. It prevents the same debate from starting again.
- **Corrections.** Typo or broken-link fixes to an accepted record are fine
  with consent. Any change to meaning needs a new record.

## Answer "why did we choose X?"

1. Read the index (or the `list` output). Grep titles, then bodies, for X and
   its synonyms. Read only the matching records.
2. Answer with the record ID, status and date. Give the chosen option and the
   drivers or `because` clause that justified it, and the main rejected
   alternatives with their reasons. Link the file.
3. **Follow supersession chains** to the current record. Say so when the
   answer comes from a superseded, deprecated or proposed record.
4. **Check staleness.** A record is a dated snapshot. If the code now
   contradicts it, say so and offer a superseding record. Don't silently trust
   either side.
5. **Not recorded means not recorded.** If no record covers X, say so. You may
   point to evidence (a commit message, PR or issue) and label it as such. Never
   reconstruct a rationale and present it as the recorded one. Offer to capture
   the decision if the user can supply it.

## Before changing governed code

When a planned change would contradict an accepted record (replacing the chosen
library, or breaking a stated constraint), stop and name the record. Ask whether
to proceed, adjust the plan, or supersede the record. Never contradict an
accepted ADR silently.

## Archive a merged spec

When a feature spec (for example a speckit `specs/NNN-slug/` directory) has
merged and its decisions would otherwise be lost, offer to archive it as one or
more ADRs. If the project provides a dedicated archival command (such as a
speckit extension that finalizes specs into ADRs), offer that first. Otherwise
follow [references/spec-archival.rst](references/spec-archival.rst). It covers
the field mapping, which decisions qualify, and permalinks that survive the spec
directory's removal. The consent gate still applies.

## Quality check

Before showing a draft, confirm that:

- the problem is worth recording, and the record covers one decision;
- the drivers are explicit and drawn from evidence, not reverse-engineered from
  the winner;
- every option is real, and each rejected option has a stated reason;
- the outcome names a driver, and consequences include a downside or say none
  was identified;
- nothing reads like a sales pitch, and no unknown was filled with plausible
  text;
- links resolve, and the number came from `next=`.

These follow Olaf Zimmermann's ADR
[review checklist](https://ozimmer.ch/practices/2023/04/05/ADRReview.html) and
[common mistakes](https://ozimmer.ch/practices/2026/09/12/ADRMistakes.html),
including "unvetted AI output". The user reviews the draft. You don't approve
your own record.

## Agent context pointer

After setting up a new log, offer (under the consent gate) to add a two-line
pointer to the project's `AGENTS.md` or `CLAUDE.md`. For example: "Architecture
decisions are in `docs/adr/` (index: `docs/adr/README.md`). Check them before
changing architecture." Never copy record contents into those files. Copies
drift from the source.

## Optional delegation

[references/subagent.rst](references/subagent.rst) contains the subagent outline,
handoff inputs, execution boundaries, and expected result. Read it when
delegating would help, for example when backfilling records from many merged
specs, or when the user asks to "create a subagent to execute this." Otherwise,
work directly from this skill; the reference does not need to be loaded.
