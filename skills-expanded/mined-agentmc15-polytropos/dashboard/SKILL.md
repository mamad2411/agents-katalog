---
name: dashboard
description: Build the local observability dashboard — one offline HTML page over the attempt ledger and history, the routing scorecard across every checkout, the telemetry snapshots and journal digests, and the evaluation, policy and training status — then report where it landed. Use when the user asks for the dashboard, an overview of what the ledger, scorecard or telemetry show, or to refresh the observability page. Not for analysis or routing changes; it renders what the owning engines report.
allowed-tools: Bash
---

# Dashboard

Resolve the plugin root before shelling out: use `${CLAUDE_PLUGIN_ROOT}` if Claude Code has set
it; otherwise resolve `../../bin/dashboard.py` relative to this SKILL.md to an ABSOLUTE path
(bash cwd is not the skill dir). Confirm you are inside a checkout before building — an empty
`--checkout` value makes the engine refuse outright (exit 2), and outside a git repository this
itself fails:

```bash
git rev-parse --show-toplevel
```

If that fails, build nothing: tell the user this only works from inside a checkout, and that
they can pass `--checkout <path>` themselves instead. Otherwise, build, passing the session's
own repo as a `--checkout`. The engine already takes the working directory's git toplevel as its
primary checkout; the flag names that repo explicitly, so it stays mapped even if the engine's
own git lookup fails:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/bin/dashboard.py" build --checkout "$(git rev-parse --show-toplevel)"
```

## Context hygiene — binding, not a suggestion

Run the plain `build` shown above only. Relay two things from its output: the page path it
prints, and the one-screen summary beside it (namespace counts, one line per panel, which caps
were hit, and a bare count of notes — every one of these is a count, never note text). Never
`cat`, `Read`, `grep`, `head` or otherwise load `index.html` or `build.json` into this session —
the page is for a browser, the summary is for you to relay. Never paste, quote, publish, attach
or upload the page or the receipt anywhere, in this session or any other. Never run `open`,
`xdg-open`, or any browser to view it — opening the file is the user's own action, never this
skill's.

**Never run `build --json` in this session, under any circumstance.** It prints the WHOLE
receipt — the `notes` array included — straight into this session as tool output, before any
rule about which fields to relay could apply. A note can interpolate a kit name, a namespace
label or a ledger detail read out of a cloned checkout, which is untrusted text this session has
no business seeing, let alone repeating. If the user wants the receipt itself, give them the
receipt path the plain build already printed and let them open it themselves — `--json` exists
for a script running outside a session, never for this skill to invoke.

## What the page holds

One panel per source; each names its engine, the date it was observed, and its own notes —
never a figure this skill or the engine invented itself:

- **Namespaces** — every data-home namespace, classed mapped / unmapped / residue (residue only:
  a heuristic — counted and named, never opened past one shallow listing, excluded from every
  other total).
  The plugin install's namespace counts as mapped — the plugin's own `telemetry_snapshot`,
  `journal_collect` and `workflow_eval` write there — and is never treated as a checkout.
- **Attempts** — the ledger and its history projection: records by source, by harness and tier,
  cost and duration one row per basis (never summed across bases), and coverage.
- **Routing scorecard** — one history card over every kits directory found together (tiers,
  kits, dollars, role quality), then role value per kits directory, in the scorecard's own
  words, its "insufficient sample" wording included where that applies.
- **Kits in flight** — task status counts and dependency-graph state for every kit under
  `.claude/kits/` and `tasks/kits/` in each checkout found.
- **Telemetry snapshots** — per source: count, first, last, latest status and labels of its
  captured envelopes, plus the fixed, per-source set of headline fields the engine registers.
  The plugin's own captures are read from the plugin install store, labelled "plugin install".
- **Journal digests** — per day: the priced totals and session counts the journal itself
  reports, by source — no free text (no inbox lines, no narrative prose) is ever rendered. The
  plugin's own digests are read from the plugin install store, labelled "plugin install".
- **Evaluation runs, policy, approvals and activation** — one card per vetted run directory,
  never a declared run id; while any run in a store cannot be vetted, the runs-summary table is
  left out (listing would touch the bad run) and every other run's card still renders. Policy,
  approvals and activation come from the owner's own preferences read set, never a wider scan.
  The plugin install's runs and policy are read too, labelled "plugin install".
- **Training data readiness** — the training pipeline's own switches, store path and notes.
- **RSI status** — per checkout, whether the recursive-improvement engine
  (`bin/recursive_improvement.py`) is present and, when it is, its contract versions, arms and
  any record store or reader it defines — read from the file as text, never run, never typed in
  here; then the `tasks/kits/recursive-improvement` kit's task statuses and `outcome:` lines,
  with its `actual-use:` and `routing:` lines counted, not parsed. The panel reads no RSI
  records itself, and says plainly what the file does and does not define rather than
  guessing.

Honesty rules hold across every panel above: an owner's `labels` and `notes` render verbatim
and in full, never shortened or dropped to make a table fit; a value the owner did not report
is the word `unknown`, never `0` or a blank cell; an absent store uses the owner's own absence
wording; in the telemetry, journal and evaluation stores, a link is noted and its content is
never rendered; no cell ever sums two cost bases, two harnesses or two owners together; and
every cap the build hit is named in the page's own bounds section, never hidden by quietly
showing less.

## Refreshing

The page is a file, not a live view — rebuilding is the only way to refresh it. If the
telemetry panel looks stale, capture a new snapshot first, then rebuild the same way (checking
for a checkout first, as above). The snapshot lands in the plugin install store, which the page
reads and labels "plugin install":

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/bin/telemetry_snapshot.py"
python3 "${CLAUDE_PLUGIN_ROOT}/bin/dashboard.py" build --checkout "$(git rev-parse --show-toplevel)"
```

## Flags

- `--checkout PATH` (repeatable) — map another checkout's namespaces too, beside the one this
  skill always passes.
- `--no-transcripts` — price no transcripts: the scorecard panel reads an empty directory
  instead of the real one.
- `--no-git` — run neither git verb; the primary checkout becomes the working directory itself.
- `--out-dir DIR` — write the page and receipt somewhere other than the default dashboard
  store.
- `where` — print where the page would land, and why, without building anything.
- `demo` — build once from synthetic data in a temporary directory that is removed on exit;
  reads and writes nothing real, and spawns nothing.

## What this cannot do

It never analyzes, ranks, prices or classifies anything the owning engines have not already
said themselves — a figure the page wants that no owner reports is stated as not reported,
never computed here. It never changes routing, a policy, or any stored preference. It never
reaches the network: the page's own Content-Security-Policy forbids every load, and nothing on
it references a URL. It has no share, publish, or "open in browser" path of its own.

## Privacy

The page holds personal data — dollar figures, task and kit titles, checkout paths, namespace
digests. Every absolute path under the user's home renders on the page as `~`. It never
contains transcript or prompt text (no engine it calls returns any), nor report, tail or inbox
text, which the ledger and the journal digests carry and the page leaves out by selection. It
stays on this machine: nothing in this skill or the engine it runs uploads, emails, or posts
the page or its receipt anywhere.
