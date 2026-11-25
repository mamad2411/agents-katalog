---
name: doctor
description: This skill should be used when the user asks to "check documentation quality", "run mnemonica doctor", "find weak spots in the knowledge docs", "audit the docs themselves, not just their accuracy", "find rules that might be stealing Mnemonica's trigger", or wants to know whether knowledge/ documentation is well-formed — stub modules, overly broad or overlapping globs, modules nobody has touched in a long time, pre-existing CLAUDE.md rules that compete with Mnemonica's own trigger — as opposed to whether it matches the code.
---

# Mnemonica: doctor

Check the quality of the documentation itself, not whether it matches the code. This is a
different question from what `audit-full` answers: a module can accurately describe what
little it says (so `audit-full` finds nothing wrong) while still being a two-line stub, or
two modules can both be individually accurate while silently claiming the same code path.
`doctor` surfaces those candidates; it never edits anything itself — every finding is
something for the user (or a follow-up `audit-full` run) to act on, not an automatic fix.

If the user's invocation includes extra wording (for example, "just check for stub modules"),
treat it as narrowing which findings to report — it cannot turn this into a skill that edits
`knowledge/` or `.claude/CLAUDE.md`; `doctor` has nothing to write in the first place.

## Step 1: Run the scan

Run `${CLAUDE_PLUGIN_ROOT}/scripts/doc-quality-scan.sh <project-root>`.

- Exit 2 (`NO_MNEMONICA_BLOCK`): nothing to check — tell the user and suggest
  `mnemonica:setup`, and stop.
- Exit 0: read the output. `MODULE` lines carry `FLAG:STUB` (very short content),
  `FLAG:STALE_DOC(Nd)` (not touched in git for a long time — only computed when the project
  has git history), or `FLAG:MISSING_FILE` (indexed but absent from disk — the same signal
  `check-index-integrity.sh` reports, surfaced here too since a missing file is also a
  documentation-quality problem). `GLOB_ISSUE` lines flag a bare `**`/`*`/empty glob entry.
  `OVERLAP` lines flag two modules claiming a byte-identical glob. `TRIGGER_OVERLAP` lines flag
  a pre-existing rule outside the Mnemonica block (line number and text included) that
  instructs Claude to do something else "before" analyzing/understanding the codebase's
  architecture or structure — the same trigger point Mnemonica's own "consult the index first"
  instruction relies on. This is a heuristic (a "before" + architecture/understanding phrase
  paired with an instruction verb), so it will over-flag; treat every hit as a candidate.

## Step 2: Apply judgment, do not just relay flags

Every flag is a candidate, not a verdict:

- A `FLAG:STUB` module might be flagged because the system genuinely is that simple — a
  three-line module describing a single trivial script is not automatically wrong. Say what
  was flagged and let the user judge; do not imply every stub is a defect.
- A `FLAG:STALE_DOC` module might not have needed a change — a stable, mature subsystem that
  legitimately hasn't changed is different from one that has drifted silently. Mention it as
  "worth a look", not as a confirmed problem; `audit-light` or `audit-full` are what actually
  determine whether the content is still accurate.
- `FLAG:TOO_BROAD` and `OVERLAP` are closer to unambiguous — a bare `**` glob or two modules
  claiming the same exact path both undermine the mechanism `audit-light` depends on to route
  changes correctly, and are worth recommending a fix for more directly.
- `FLAG:MISSING_FILE` is unambiguous: recommend `mnemonica:audit-full` to recreate it.
- `TRIGGER_OVERLAP` needs a real read of the flagged line, not a reflex fix: some hits are
  false positives (a line that happens to contain "before" near "architecture" but isn't
  actually claiming Mnemonica's trigger point), and some are real — a rule that tells Claude to
  use a different tool "before" understanding or analyzing the code, which can silently win
  over `knowledge/` every time because of where it sits in the file or how specific it reads.
  For a real conflict, this is the user's own pre-existing content, so `doctor` does not
  propose rewriting it here — explain the risk (the competing rule may be why `knowledge/` gets
  skipped even though it's accurate and populated) and suggest options: narrow the competing
  rule's trigger phrase so it no longer covers general architecture questions, add an explicit
  precedence note (e.g. "consult `knowledge/` first for anything it already covers; use
  `<other tool>` for what it doesn't"), or leave it if the read confirms it's a false positive.

## Step 3: Report

Present findings grouped by kind (stubs, stale docs, broad globs, overlaps, missing files,
competing triggers), each with the module(s) or line involved and a one-line reason. If
nothing was flagged, say the docs look structurally healthy rather than listing empty
categories. Do not propose or make any edits — recommend `audit-full` (for missing files or
content drift), a manual restructuring conversation (for overlaps and overly broad globs,
since resolving those may mean merging or redrawing module boundaries, which is `audit-full`'s
ask-before-restructuring territory, not this skill's), or — for `TRIGGER_OVERLAP` — a manual
edit to the competing rule itself, since that rule is the user's own pre-existing content and
not something any Mnemonica skill writes to.
