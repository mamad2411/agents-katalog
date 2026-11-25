---
name: council
description: Convene a panel of independent fresh-context reviewers (subagents with distinct personas) on a research proposal, our own manuscript, or a plan for a simulation campaign, then a separate fresh synthesizer. Use when asked for a council, panel review, mock evaluation panel, or "Referee 2" pass on a proposal, grant, aims page, or paper draft, or to stress-test whether planned calculations can answer a scientific question within time and compute limits. Also develops alternative aims/framings at the ideas stage.
argument-hint: "[proposal|manuscript|ideas|plan] [file:path] [call:path] [panel:a,b,c] [focus:...] [lit] [skills] [help]"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Agent
---

# /council — Independent Panel Review for Proposals, Manuscripts and Plans

Adapted from the `council` / `adversarial-review` skills in Chris
Blattman's [claudeblattman](https://github.com/chrisblattman/claudeblattman)
(MIT), simplified for local Claude subagents only.

**Core idea:** whoever helped write a draft rationalises its gaps. Each
panel member is a *fresh* subagent that sees only a neutral brief, the
document and its own persona — never this conversation. A further fresh
subagent synthesises their reports without voting. The host (you) only
prepares the brief, dispatches, and presents results.

## Scope

- Our **own** proposals, manuscripts and plans only. Do not run a council on a
  manuscript or proposal we have been sent to **referee**: journal and
  funder confidentiality rules generally forbid uploading it to AI tools.
  If the document looks like someone else's confidential submission, stop
  and ask.
- The council reviews and advises. It never edits the document. Revisions
  happen only afterwards, and only when the user authorises them.

## Step 0: Parse arguments

**If `$ARGUMENTS` is `help`, print this table and stop.**

| Flag | Syntax | Default | Purpose |
|------|--------|---------|---------|
| Mode | `proposal` / `manuscript` / `ideas` / `plan` | auto-detect | Which panel and output format |
| File | `file:path` | ask | Document to review (.tex, .md, .pdf, .docx, or a folder) |
| Call | `call:path` | ask (proposal) | Call text / evaluation criteria / templates |
| Panel | `panel:a,b,c` | mode default | Exact personas, any from `personas/` |
| Focus | `focus:"..."` | none | Extra question every member must address |
| Literature | `lit` | off | Members may check novelty/citations via PubMed/OpenAlex/bioRxiv skills |
| House skills | `skills` | off (`plan`: on) | Members may read our protocol skills and machine notes as reference |
| Dry run | `dryrun` | off | Write the brief and show the panel; do not dispatch |

**Default panels** (persona files in `personas/`):

| Mode | Members |
|------|---------|
| `proposal` | `panel-generalist`, `domain-skeptic`, `pre-mortem`, `call-compliance` |
| `manuscript` | `referee-methods`, `experimentalist`, `editor`, `reproducibility` |
| `ideas` | `panel-generalist`, `domain-skeptic`, `pre-mortem` (development instructions) |
| `plan` | `question-fit`, `sampling-methods`, `compute-budget`, `pre-mortem` |

Add `experimentalist` to a `plan` panel when the campaign is meant to be
compared with experimental data.

Auto-detect mode from the document (aims, work packages, budget, call →
`proposal`; abstract/results/figures → `manuscript`; systems, runs,
machines and a question to answer, but no call or results → `plan`). If
unclear, ask.
Announce the resolved mode and panel before dispatch.

## Step 1: Gather inputs

1. Locate the document. For a LaTeX project (e.g. an Overleaf git clone),
   identify the main `.tex` and the `\input` files and figures. For `.docx`
   or `.pdf`, convert to text in the archive (`pandoc`, `pdftotext`) and
   keep the original path as evidence too, since figures matter.
2. **Proposal mode:** the call text and evaluation criteria are required.
   If `call:` is missing, ask for the call document or URL, or for the
   criteria and page limits in the user's own words. Do not reconstruct a
   funder's criteria from memory.
3. **Plan mode:** the plan can be a markdown file, a section of
   `TODO.md`/`CHECKPOINT.md`, or a plan-mode file in `~/.claude/plans/`.
   If it exists only in this conversation, write it verbatim to
   `<archive>/PLAN.md` once the archive exists (Step 2) and review that
   file. The scientific question,
   the machines available and the deadline are required. If they are
   not in the plan, ask for them. Never fill them in yourself.
4. Ask only about facts that materially change the review, and only if they
   cannot be read from the documents: target funder/journal, stage
   (first draft vs. near-final), page/word limits, known constraints that
   reviewers should not relitigate (e.g. "the budget ceiling is fixed").

## Step 2: Write the brief

Choose an archive next to the document's project:
`<project>/council/YYYY-MM-DD_<topic>/`. If the document lives under
`~/Research/Projects/<Cat>/<Project>/`, use that project root. Otherwise
use the document's directory. Tell the user the path.

Fill `references/brief-template.md` and save it as `BRIEF.md`. The brief
must be **neutral**:

- State the user's objective and constraints in their own words.
- Give absolute paths to the document, call text and any other evidence.
  Do not paste a summary in place of the source.
- Include **no host opinion** about the draft's strengths or weaknesses.
- Keep user decisions as fixed constraints, separate from open questions.

Show the brief and panel to the user. On `dryrun`, stop here.

## Step 3: Dispatch the panel (in parallel)

Launch one `Agent` call per member **in a single message** so they run
concurrently. Use `subagent_type: "general-purpose"`, **never `fork`**: a
fork inherits this conversation and defeats the purpose.

Prompt for each member (fill in the placeholders, change nothing else):

```
You are an independent member of a review panel. Other members are working
in parallel; you will not see their reports and they will not see yours.

1. Read your persona: <skill_dir>/personas/<persona>.md
2. Read the brief: <archive>/BRIEF.md
3. Read the full document and any evidence listed in the brief.
4. <MODE INSTRUCTION>
5. Write your report to <archive>/reports/<persona>.md using
   <skill_dir>/personas/_report-format.md and any additions in your
   persona file. Then reply with only the report path and a 3-line
   summary.

Rules: Do not edit the document or any file except your report. Cite
locations (section, page, line, figure, equation) for every finding. Keep
demonstrated defects separate from concerns and from taste. If you find
nothing material in an area, say so. Do not pad the report.
<LIT RULE>
```

- **MODE INSTRUCTION, review modes:** "Review the document through your
  persona's lens."
- **MODE INSTRUCTION, `ideas`:** "Do not critique line by line. Through
  your persona's lens, propose 2–3 meaningfully different directions
  (aims, framing, scope, methods). For each one, give its rationale, the
  main risk, and what it would take. Say which you would choose and why."
- **LIT RULE with `lit`:** "You may use the pubmed-database,
  literature-search-openalex or literature-search-biorxiv skills to check
  novelty claims, competing work and key citations. Report what you
  searched for. Search queries leave this machine, so use only general
  scientific terms and never paste text from the document."
  **Without `lit`:** "Do not search the web or literature databases;
  flag claims that need checking instead."
- **SKILLS RULE with `skills`** (append to the LIT RULE): "You may read
  the reference files listed in the brief: our house protocols and
  machine notes. Treat them as the group's current practice, not as
  ground truth. Say where the plan departs from them, and also where
  they may be inadequate for this question."
  List in the brief only the files relevant to the plan, chosen from
  `~/.claude/skills/<skill>/SKILL.md` for `gmx-prep`, `plumed-us`,
  `plumed-metad`, `plumed-remd` and `amber-parameterize` (and the
  templates they point to), plus the "Compute Infrastructure" section of `~/.claude/CLAUDE.md`. Copy that
  section to `<archive>/machines.md` so members read only the machine
  notes, not the rest of the file.

Wait for all members. Check that every report file exists and is
substantive. If a member failed, re-dispatch it **once** with the same
prompt. If it fails again, record it as missing. Never write a missing
report yourself.

## Step 4: Fresh synthesis

Launch one more `general-purpose` Agent (not one of the members):

```
You are the synthesizer for a review panel. Read
<skill_dir>/references/synthesis.md and follow it exactly.
Brief: <archive>/BRIEF.md. Reports: <archive>/reports/*.md.
The original document is at <path>; check decisive claims against it.
Missing members: <none | list>. Mode: <mode>.
Write <archive>/SYNTHESIS.md and reply with only its path.
```

The host never writes the synthesis inline. If synthesis fails twice,
present the raw reports and label them "unsynthesised".

## Step 5: Present results

Read `SYNTHESIS.md` and report to the user concisely:

1. Verdict line (see the mode-specific ending in `synthesis.md`).
2. The top 3–5 required changes, each with its location and its
   supporting members.
3. Material disagreements between members, which the user decides.
4. Any missing members or limitations.
5. Links to `SYNTHESIS.md` and `reports/`.

Then ask which findings to act on. When the user authorises revisions:
apply only the selected ones, preserve the author's voice, check that
the edits introduce no new unsupported claims, and append a short
`DISPOSITION.md` to the archive (accepted / rejected / deferred, one line
each). Do not edit `SYNTHESIS.md` or the reports.

A re-review of a revised draft is a **new** council with a new archive
and fresh members, and only when the user asks for one.

## Examples

```
/council proposal file:~/Grants/ERC-CoG-2027/main.tex call:~/Grants/ERC-CoG-2027/call.pdf
/council manuscript file:paper/main.tex focus:"Is the MSM convergence argument convincing?"
/council ideas file:aims_v1.md call:aei_2027_criteria.md lit
/council proposal panel:panel-generalist,experimentalist,pre-mortem file:draft.pdf
/council plan file:PLAN_rest2_as4.md focus:"Is 1 µs per replica enough?"
/council plan panel:question-fit,sampling-methods,compute-budget,pre-mortem,experimentalist
```
