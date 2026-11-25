---
name: caic-pr-review
description: 'PR review conventions for carbon-design-system/carbon-ai-chat. Covers: severity by cost (Blocker, Important, Nit mapped to the output contract), Carbon flavor by path (Web Components vs React), no hardcoded cds-- in SCSS/TS, BEM + logical CSS, logic in plain modules not Lit elements, new UI in components/ not components-legacy/, no hand-edit of generated files, test-proof integrity, PR size, checklists by file type, large-diff triage, what is not a finding, and finding-wording rules. Use on every caic diff alongside the main review prompt.'
version: '1.1.0'
author: Carbon Monitor
---

<!-- upstream commit pinned: 75dada3856a718fe8022ef36bd195f17212e563a -->
<!-- rules-ledger: src/profiles/caic/RULES-LEDGER.md -->

# caic-pr-review

This skill is for **PR review only**. It uses only the diff, PR description,
and changed-files list. It does not write code, call external tools, or check
anything that is not visible in the diff.

It does **not** include output-format rules — those come from the main prompt.

---

## What is NOT a finding (X rules)

Before writing any finding, check this list. Nobody pays for these, so they
stay unsaid however small the edit:

- **X1** `telemetry.yml` changed _and_ a source file in the same PR regenerates
  it → not a finding. Example: a commit modifies `Foo.ts` and also updates
  `telemetry.yml`; only flag `telemetry.yml` when no source change regenerates it.
- **X2** The PR description explains an unusual change as intentional → that is
  valid context; do not flag it as "author says intentional".
- **X3** A linked issue has unmet "Done when" items → completeness is out of
  scope; do not flag it.
- **X4** A different-but-valid approach → do not flag it as wrong, including a
  route other than the one the linked issue suggests. Example: a PR uses
  `ResizeObserver` where `getBoundingClientRect()` would also work. A route that
  is defective is still a finding, on its own merits.
- **X5** The category follows what the claim depends on, not how it is worded.
  If being right depends on how a `cds-*` element or a `@carbon/*` API behaves
  (an attribute or property, what a slot renders as, a default, a variant, an
  event, a style hook, its accessibility behaviour), the claim is Cat 1: verify
  it through `carbon-builder` or Carbon MCP and quote the evidence, or it is
  not a finding. Never file it from model knowledge, never relabel it Cat 2 to
  get past the evidence rule, and never file it one level down (that step is
  for Cat 2 reasoning you did not finish). When MCP answers but has nothing for
  the element (0 variants, no docs), discard it as not indexed in MCP. If the
  uncertainty matters to the author, name it in `Not verified` (W9). Example: a
  guess that `cds-copy-button` shows its default slot as visible text, when the
  component forwards that slot to its tooltip.
- **X6** A tool already decided it: formatting, quote style, import order, line
  length. The commit hooks run prettier, eslint, stylelint and commitlint.
- **X7** A naming swap with no clarity gain (`data` → `payload`), or an
  equivalent style alternative (`for` versus `.map`, ternary versus `if`).
- **X8** "Add a comment here." The repo default is no comments. Ask for one only
  when the diff encodes a _why_ the code cannot show (a workaround for a named
  bug, an outside constraint, an ordering that looks arbitrary and is not), and
  say what the line has to record.
- **X9** Speculative extraction: "you might want to pull this out in case…".
- **X10** Code the diff did not touch. A pre-existing problem is not this PR's
  job. A regression is: a change that breaks a caller, consumer or snippet you
  can see elsewhere in the diff (a signature changed in one hunk, the old call
  still in another) is a Blocker. A caller outside the diff is one you cannot
  see: name it in `Not verified` (W9), do not guess.
- **X11** A defect you cannot trigger is a guess. Drop it, or file it one level
  down and say what you did not read (W5).
- **X12** A review that surfaces nothing is finished, not failed. Report no
  findings. Never manufacture one to look thorough.

---

## Section F — Carbon flavor by path (Cat 1)

Findings in this section require a Carbon MCP call with the correct
`filters.component_type` before reporting.

| Path pattern                                                           | Carbon package at runtime                            | MCP component_type |
| ---------------------------------------------------------------------- | ---------------------------------------------------- | ------------------ |
| `packages/ai-chat/src/**`                                              | `@carbon/web-components` (via `@lit/react` wrappers) | `"Web Components"` |
| `packages/ai-chat-components/src/**` (Lit elements)                    | `@carbon/web-components`                             | `"Web Components"` |
| `packages/ai-chat-components/**/__stories__/*-react.{stories.jsx,mdx}` | `@carbon/react`                                      | `"React"`          |

**F4 (Blocker):** A `+` line adding a `@carbon/react` import into
`packages/ai-chat/src/` or into a Lit element under
`packages/ai-chat-components/src/` is a Blocker. Verify via MCP first.

**F5:** The `carbon-builder` skill defaults to React. A React snippet from that
skill is a translation _hint_ for the primary Web Components paths — not a
copy-paste answer.

---

## Section N — Naming and prefix discipline (Cat 2, Blocker)

**N1:** A `+` line in SCSS containing the literal string `cds--` is a Blocker.
The build re-prefixes tokens at build time; a hardcoded `cds--` breaks the
`es-custom` output. Use `#{$prefix}--` instead.

**N2:** A `+` line in TS/TSX containing a literal `cds--` class string is a
Blocker. Use the shared prefix helpers.

**N3:** In Lit, tag strings must come from the shared prefix constant, not
inline literals.

---

## Section S — SCSS authoring (Cat 2, Important)

**S1:** SCSS uses BEM with `#{$prefix}--` prefix.

**S2 (Important):** A `+` line adding a descendant selector (`.a .b {}`) is
Important. `&:hover`, `&--modifier`, and `@media` queries are fine.

**S3 (Important):** A `+` line adding a physical directional CSS property
(`padding-left`, `right`, `padding-top` where `padding-block-start` is
correct, etc.) is Important. Use CSS logical properties
(`padding-block-start`, `inset-inline-end`, …) for RTL support.

---

## Section L — Framework-agnostic logic and placement (Cat 2, Important)

**L1 (Important):** A `+` line adding parsing, formatting, validation, state
transitions, or geometry math _directly inside_ a component method where a
plain module would do is Important. Logic belongs in modules without
React/Lit imports. Flag logic you could only test by rendering.

**L2 (Important):** A `+` line adding a new component file under
`packages/ai-chat/src/chat/components-legacy/` is Important: nothing ships
broken, but the component has to move later. New UI goes in `components/`.

---

## Section C — Comments (Cat 2, Nit)

**C1 (Nit):** A `+` line adding a comment that restates the code, or that
references the current PR/task/issue number, is a Nit.

---

## Section G — Generated output (Cat 2, Blocker)

**G1 (Blocker):** A `+` line directly editing `dist/`, `es/`, `es-custom/`,
`storybook-static/`, `storybook-react-static/`, `node_modules/`,
`custom-elements.json`, `telemetry.yml` (without an accompanying source
change), or the release-owned API docs `packages/ai-chat/docs/api/markdown/` and
`packages/ai-chat/docs/api/symbol-index.json` is a Blocker. The hand-written
`packages/ai-chat/docs/api/README.md` is docs, not generated.

**G2:** `telemetry.yml` accompanied by a source change that regenerates it is
fine — see X1.

---

## Section T — Test integrity (Cat 2, Blocker or Important)

A weakened proof turns the run green while the requirement still reads as
written. It is a **Blocker** when the weakened proof covers behavior this diff
changes, and **Important** (`major`) otherwise.

**T1:** A `+` line replacing a specific assertion with a weaker one
(e.g. `.toBeDefined()` replacing `.toBe(5)`).

**T2:** `test.skip`, `xit`, `xdescribe`, `.skip` with no replacement test.

**T3:** A regenerated snapshot that masks a behavior change (updated to match
current broken output, not a real improvement). Regenerating is allowed and
sometimes correct; ask for the reason, not for the absence of the command.

---

## Section P — New dependencies (Cat 2, Important)

**P1 (Important):** A `+` line adding a new dependency in `package.json` with no
explanation in the PR description or in a comment is Important. Flag the
dependency name and the lack of rationale. If the PR description explains why the
new package is needed, discard. A package that duplicates one already listed
needs the reason too.

---

## Section Z — PR size (Cat 2, Important)

Count additions plus deletions, and only in non-generated, non-test,
non-snapshot, non-fixture, non-doc files. Exclude: lockfiles, `dist/`, `es/`,
`es-custom/`, `custom-elements.json`, `telemetry.yml`, `versions.js`,
`packages/ai-chat/docs/api/markdown/`, `packages/ai-chat/docs/api/symbol-index.json`,
`.claude/skills/`, `.agents/skills/`, `.bob/skills/carbon-builder/`, `*.snap`,
`*.test.*`, `*_spec.*`, `*.spec.*`, fixtures, everything under `examples/` and
`demo/`, `.md`/`.mdx` docs. Shared test setup (jest or playwright config, test
helpers) counts.

| Counted lines | Severity                                                                               |
| ------------- | -------------------------------------------------------------------------------------- |
| ≤ 200         | No finding                                                                             |
| 201–400       | Important — suggest a useful split                                                     |
| > 400         | Important — split by default, unless the PR description explains why it stays together |

**Size is a finding.** When the change should have been several PRs, say so as
`major`, at any size, including a PR that bundles unrelated work. Name the
seams: which files would have made the second PR. Mechanical bulk is not size:
a rename sweep across sixty files is one job. Do not ask for arbitrary chunks,
incomplete work, or tests deferred to lower the count.

---

## Section R — Large diffs

Use this when reading every file at one depth would mean reading all of it
shallowly: the file list is long, or you catch yourself skimming. No line count
triggers it. A 600-line lockfile bump is not a large diff; four files rewriting
the store is. Rank the files by risk per line before cataloguing, and spend
attention in that order. Every file still gets its catalogue line.

- **Glance:** pure renames and moves (nothing to read but the new path);
  `package-lock.json` (review the `package.json` change that caused it);
  generated output (an edit is a Blocker on sight under G1; `telemetry.yml` is
  the exception under G2).
- **Read every line:** `packages/ai-chat/src/types/**` (the public contract; a
  wrong line ships to consumers); `packages/ai-chat/src/chat/store/**` (reducers
  and state transitions); new files (there is no unchanged context to lean on).
- **Everything else:** the changed lines and the context around them.

---

## Section E — Checklists by file type

Step 1 walks the checklist that matches each file. Skip the rest.

**Code changes**

- Over-built code is `major` unless it hides a defect: single-caller
  abstractions, deep nesting, shared mutable state, dead code, unused
  flexibility, JS that re-creates what CSS, a native element or a browser API
  already does.
- Bugs and security: logic errors, injection, XSS, unsafe deserialization,
  secrets in code.
- Edge cases: empty or null input, error paths, concurrency, cancellation,
  large input.
- Accessibility on UI changes: keyboard navigation, focus, ARIA roles and
  labels, color contrast, RTL. A regression is a Blocker.
- Scope creep is `major`: drive-by refactors, handling for cases that cannot
  happen, shims for code with no outside consumer.
- Suggest another implementation only for a concrete defect, never for taste.

**Tests**

- Name each changed behavior that has no test. A missing test for changed
  behavior is `major`.
- Check whether any existing proof got weaker (T1-T3). A passing run will not
  tell you.
- UI change with no browser or interaction check in the diff: say so in the
  summary as `Not verified`.

**Docs and text**

- Spelling, grammar, punctuation; correct and standard technical terms.
- Clarity, concision, consistent headings, bullets and structure.
- The text gives the reader what they need to act. A misleading name or doc
  (a wrong unit, a unit the caller has to guess, a wrong default) is `major`;
  a style slip is a nit.
- Markdown that tells an agent what to do (`AGENTS.md`, `references/`, skills)
  is a specification: ask whether an agent following the changed text does the
  right thing.

---

## Section W — Finding wording

**W1** A `minor`-or-above finding body reads in this order, on one line:

1. **Orient:** what the code does and when it runs, opened by one bold label:
   `**What this block does:**` (a function or branch), `**Context:**` (a line
   whose neighbors matter), `**What this test is for:**` (a spec),
   `**Why this line matters:**` (a cost the line hides). Do not invent a fifth.
   Describe the code, not the review: never recap the diff or restate the
   severity.
2. **Diagnose:** what is wrong.
3. **Cost:** what it costs, naming the input or path that reaches it ("on every
   close", "when the list is empty"), not the category.
4. **Fix:** an imperative the author can act on. Never post the objection
   without the fix. When you cannot name one, end with the check that would
   settle it, as an imperative.

A nit's body is one line. Only its title and `file:line` are posted.

Rules:

- **W2** No hedging ("might", "could potentially", "I think"). State the finding
  directly. Say what you checked instead: "read the happy path only".
- **W3** Name the file path and the line from the diff.
- **W4** End with the imperative fix (step 4 above).
- **W5** Run a **refute step** before shipping a Blocker: read enough of the
  diff and PR description to be certain. A false Blocker costs the author as
  much as a missed one. If you read only the happy path, file it as Important
  (`major`) and say in the body what you did not read.
- **W6** No throat-clearing ("just", "simply", "one small thing", "it is
  important to note"). Delete the phrase.
- **W7** No praise inside a finding ("nice refactor, but…"). A finding is the
  defect and the fix.
- **W8** Cap the diagnosis and cost at three sentences.
- **W9** Say what you did not read. When you skipped or skimmed something you
  would have needed to be sure, say so in that finding's body (W5) and end the
  summary with one sentence `Not verified: <path or behavior>`. Omit it when
  you read everything you needed; never write "Not verified: nothing".

---

## Severity

Each caic label maps to one output contract value. A finding is rated by what
it costs if it merges as written.

- **Blocker** → `blocking`. Something ships broken or a commitment breaks: wrong behavior on a path you can name, a regression, a security hole, a broken build or tests, an accessibility requirement violated, or an edit to generated output.
- **Important** → `major`. Nothing ships broken, but someone pays later: a missing test for changed behavior, a defect you could not confirm past the happy path, needless work, a misleading name or doc, scope creep, or unrelated work bundled in.
- (no upstream label) → `minor`. A maintainability risk with evidence of functional impact.
- **Nit** → `nit`. Convention or hygiene with no functional consequence. Kept, collapsed in the summary, never posted inline.
- If nobody pays, it is not a finding at `minor` or above. A nit is reported because it costs nothing to read and the report collapses it.
- A convention break costs what its consequence costs. It is not a Blocker by default.
