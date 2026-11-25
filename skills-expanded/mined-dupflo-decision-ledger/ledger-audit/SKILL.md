---
name: ledger-audit
description: "Retrospective pass over a project built before the ledger existed: reconstruct the structural decisions already made and the conventions applied without a reason. (decision-ledger)"
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - AskUserQuestion
---

# ledger-audit

A retrospective pass over a project that already exists, which is every project, the first time this is installed. Without it the ledger only ever knows about work done after installation, and starts from an empty file on a codebase with two years of decisions in it.

**An audit is the one moment interrogation is welcome.** The user sat down for it. That makes a batch of questions acceptable here and nowhere else, and it is the only place in this family where that is true. Everything in `/ledger` exists to keep questions rare; that budget does not apply once someone has explicitly asked to be audited.

```bash
for p in ~/.claude/skills/decision-ledger/bin/ledger \
         ~/.claude/skills/ledger-audit/bin/ledger \
         .claude/skills/ledger-audit/bin/ledger \
         .agents/skills/ledger-audit/bin/ledger; do
  [ -x "$p" ] && LEDGER="$p" && break
done

$LEDGER audit --depth 5
```

The list covers both ways this can be installed: `install.sh`, which lays down the whole repo, and a skills registry, which copies this directory alone.

The command prepares the material: inherited conventions first, then previously undefended decisions. **It writes nothing.** Reading the codebase, asking the questions and recording the answers is your job.

## Rules

**Ground every question in this codebase.** This is what separates an audit from the quiz this whole project exists to avoid.

> Your `users` table has a soft-delete column. Why not a real delete?

is unanswerable from memory. It requires having thought about *this* schema.

> How should auth work?

is a quiz question, answerable by anyone who has read a blog post, and proves nothing. If a question could be asked of a stranger's project, it is the wrong question.

Read before asking: existing decision records (below), schema and migrations, module and package boundaries, the dependency list, state management, `CLAUDE.md` and `AGENTS.md`.

### Start with the decision records, if there are any

Look for `docs/decisions/`, `docs/adr/`, `doc/architecture/decisions/`. This is the ADR convention, roughly a decade old and vendor-neutral, and increasingly written for you by agentic pipelines rather than by hand. Each file already names one structural decision, the options considered, and why the others were rejected.

Where they exist, that is the best audit material a project can offer, and far better than scraping `CLAUDE.md`: the decisions are already isolated, scoped and dated. Where they don't, skip straight to the code. Most projects have none, and the audit works fine without them.

It is also the sharpest question available, because an ADR written by an agent proves nothing about the person:

> `docs/decisions/004-drizzle-over-prisma.md` says you rejected Prisma over bundle size. What did picking Drizzle cost you that Prisma would have given you for free?

An ADR records what the **project** decided. This ledger records whether **you** can defend it. Where both exist they answer different questions, and the ADR is the input. Never treat a decision as covered just because a file documents it. That confusion is the whole reason this tool exists.

Prefer ADRs whose author is the agent, or whose rationale reads as generated. Skip ones the user visibly wrote and argued themselves; those are already defended.

**Bounded and interruptible.** Five questions by default, `--depth` for more. Stop the moment the user wants to stop. A partial audit is still useful, and an audit that runs forty minutes only ever happens once, which means never again.

**Prioritise.** Largest areas, most recently changed, or with no ledger entry at all. Never an exhaustive sweep.

**Record each answer as you go**, exactly as during normal work, so an interrupted audit keeps everything it earned:

```bash
$LEDGER record --area data-model --concept soft-delete --signal partial --source audit \
  --note "knew the audit-trail argument; hadn't considered the unique-constraint cost"
```

**Always pass `--source audit`.** An audit hunts for what nobody arbitrated, so a map built from it is biased downward by construction, and a first report reading "0 of 5 defended" lands as a verdict on the person, which is the one thing this must never be. The flag makes `report` say so out loud.

**One question at a time.** A batch is acceptable here; a wall of five questions at once is not, because the user answers the first properly and skims the rest.

## Inherited conventions

A project's rules often live in `CLAUDE.md` or `AGENTS.md`, and they are frequently copied from another project or a template. That is comprehension debt too, and worse than generated code: a convention propagates across the whole codebase without ever meeting a moment of decision.

```bash
$LEDGER conventions
```

Three states for any project constraint:

| State | Behaviour |
|---|---|
| Documented **with** a reason, or already defended | Never ask. The decision is settled at project level. |
| Documented **without** a reason | `inherited`: applied but undefended. Fair game *here*, and only here. |
| Open decision | Belongs to `/ledger`, at the moment it comes up. |

The script's detection is a keyword heuristic on two axes: it keeps only lines that read as normative, and among those flags the ones that state no rationale. It deliberately under-reports, and command reference, pipeline diagrams and file imports are skipped wholesale, because counting them once produced dozens of phantom conventions on a real project.

So read the file yourself as well. A rule the scanner missed is still a rule, and a rule that explains itself is defended even if it uses none of the marker words.

Record a convention the user could not defend:

```bash
$LEDGER record --area forms --concept zod-validation --signal inherited \
  --note "CLAUDE.md:3, stated without a reason"
```

`inherited` entries carry a base confidence of `0.0` and never touch the personal file: nobody was ever asked, so there is nothing to say about a person. They convert to `justified` the normal way, through `record`, when the user defends them.

**Never create them outside an audit.** Discovering a config file during ordinary work must not fire ten questions in a row; that is the single fastest way to get the whole family uninstalled.

Tone matters here: inherited is not a reproach. Adopting a good convention is often the right call. What is being noted is only that nobody could currently defend it in review. Say so, out loud, the first time the word appears.

## Afterwards

Close with `/ledger-report`, not with a summary of your own. The map is the point; a paragraph of encouragement is not.
