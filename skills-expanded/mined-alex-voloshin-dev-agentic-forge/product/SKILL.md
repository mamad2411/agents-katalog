---
name: product
description: Product requirements — turn an existing research brief INTO a PRD (goals, non-goals, success metrics, acceptance criteria) with user stories, and assess the current product. Use to write a PRD, define requirements, goals or acceptance criteria, specify what to build, or write user stories. Producing the brief itself is research; not the technical design (architecture), task planning (plan), or market and pricing work (marketing).
allowed-tools: Read, Grep, Glob, Bash, Task, Write
---

# Product (phase workflow)

The product phase of the SDLC spine: decide *what to build and why*, turning a research brief
into a PRD the `architecture` phase consumes. This is the conversational phase — elicit what's
missing from the user rather than inventing it, *when there is a user*: a headless run has none,
so there the gaps become stated assumptions in the PRD, flagged in the summary.

**Scope: it creates new PRDs in its own format and amends existing ones in theirs.** A new PRD is
`prd.md` with the YAML header below, validated by `handoff-load`. An existing PRD is changed in
place, in whatever format the repository wrote it (a metadata table, its own headings and ids),
never converted, and never duplicated by a second PRD beside it.

## When to use

After research, when the question is *what & why*: goals, non-goals, success metrics,
acceptance criteria, user stories — or when a live PRD's requirements change (amend mode). Not for *what exists* (`research`), *how to build it*
(`architecture`), task breakdown (`plan`), or code (`develop`).

## Process

> **Recall first** — pull the project's relevant prior decisions with its own search, else the
> knowledge vault (see [knowledge-recall](../../patterns/knowledge-recall.md)); factor them in, pass
> the top hits (path + one line why) in every `Task` prompt you send, and skip if nothing is found.

> **Deliver in isolation** — when a `<feature-slug>` is in play, write into the feature's
> shared documentation worktree rather than the checkout, and deliver the result as a pull
> request (see [doc-delivery](../../patterns/doc-delivery.md)). One worktree and one PR per
> **feature**, shared by every document phase — that is what lets the next phase read what
> this one wrote. Skip it for a one-off document outside a feature flow. A repo with no remote (or
> no `gh`) still commits — on `docs/<slug>`, reported as not pushed / no PR — never a failed phase.

> **Write where the repository keeps its features** — run
> `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" artifact-home --repo <worktree> --slug <feature-slug> --kind prd`.
> Its `feature_dir` is `<feature-dir>` below (`docs/sdlc/<feature-slug>` only when the repository
> keeps no feature folder for it), and `documents.<kind>` (`research`, `prd`, `design`, `plan`,
> `ux`) gives each document's `abs` path. **Never put a path on a command line yourself:** run
> the commands it prints (`documents.<kind>.commands.*.shell`) verbatim, and where a call below shows
> `<path>`, use that document's `arg` (absolute, already quoted). A document or ADR directory with
> `unsafe` set (a symlink, or something other than a regular file, at or on the way to its path) is
> never written: stop and report it. On `ambiguous`, ask when interactive; headless, take its pick
> and record it as an assumption naming the alternatives
> ([where a feature's documents go](../../patterns/handoff.md#where-a-features-documents-go)).

> **Create or amend.** When the user points at an existing PRD, or `documents.prd.exists` is true and
> the request changes requirements rather than starting a feature, this is **amend mode**: follow
> [references/amend.md](references/amend.md) instead of steps 1–6. In short: edit the PRD in place,
> in its own format; run the same bounded skeptic loop on the **diff** of its requirements; persist
> each round as `review-prd-<n>.md` in `<feature-dir>/`; and, for a PRD in a **foreign format**
> (`format` is `foreign`), skip the `handoff-load` read-back, which would refuse it, and
> gate on `git diff --check` instead. Steps 1–6 below create a new PRD.

1. **Digest the inputs.** Load `research-brief.md`
   (`python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type research-brief`; **refuse to build on it unless its `ready` is true — an escalated upstream run leaves a schema-valid but rejected artifact on disk**; never edit its `status` to make it so) and assess the current product
   (repo, existing docs). Pick the `<feature-slug>`. **If `research-brief.md` is absent** (check
   that the file exists first — `handoff-load` fails on a missing file): build the PRD from the
   request + the repo + its existing docs, record the assumptions and that no brief existed in the
   PRD's body, and proceed — the brief is an input when it exists, not a precondition.
2. **Frame the change.** From the brief's findings + recommendation, decide the **goals** and
   the explicit **non-goals** (what's out of scope), and the **success metrics**. When the ask
   involves ordering the work (what to build next, MVP scope, roadmap) or picking the metrics,
   load [references/prioritization.md](references/prioritization.md) — the framework-selection
   table (RICE / ICE / MoSCoW / JTBD / Kano), the metric frameworks, and the roadmap shape.
3. **User stories.** Write the change as user stories (from the user's perspective), each with
   acceptance criteria.
4. **Acceptance.** Turn the stories into concrete, testable **acceptance criteria** for the
   feature. Elicit anything ambiguous from the user when interactive — don't guess load-bearing
   decisions. Headless, there is no one to ask: take the most defensible assumption, mark it
   `assumption:` in the PRD, and flag it in the summary rather than stopping.
5. **Write the PRD.** Produce `prd.md` (frontmatter `type`, `feature`, `status`, `goals`, `non_goals`, `metrics`,
   `acceptance`, and `review_decision: revise` until the loop exits; body = context + user stories; **valid YAML — quote any value containing a colon**,
   e.g. an acceptance criterion naming `{"high": 0}`, or the whole artifact fails to parse for every
   downstream phase) at `documents.prd.abs`; validate it (the read-back below). Keep every requirement traceable to
   the brief.
   Then **read the file back** — `documents.prd.commands.handoff_load.shell`, the printed form of `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" handoff-load --path <path> --type prd` — and fix whatever it reports: this reads the file, so it sees the YAML you typed, and a single
   malformed value (a flow sequence with prose after it, an unquoted `:`) leaves an artifact the
   next phase cannot read (ADR 0096).
6. **Skeptic pass (bounded).** Before handing off, fork a fresh `reviewer` (via `Task`) to
   challenge the draft adversarially — every acceptance criterion **testable**, every success
   metric **measurable**, the **non-goals complete**, and each requirement **traceable to the
   brief** — then revise worst-first. **External reviewer lens (on by default, ADR 0057):** when
   `external_reviewer.enabled` (settings), also run the external reviewer over `prd.md` —
   `documents.prd.commands.external_review.shell`, the printed form of `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/external_review.py" --target <path> --repo <worktree> --kind product`; codex critiques the PRD as an
   independent-model lens (testable criteria, measurable metrics, complete non-goals, traceability)
   and its `findings` fold into the same worst-first revision. It **degrades gracefully** (absent/
   disabled codex is skipped, not a failure; **exit 3 is a failed lens**, not a skip — record it in the round and tell the user) and its findings are **advisory** (prompt-injectable) —
   verify before acting. **Persist each round** — one `review-<artifact>-<iteration>.md` per round in `<feature-dir>/` (`feature_abs`), aggregating **both** lenses; on `proceed` keep only the final round, on `escalate` keep them all (naming + lifecycle: [review-loop.md](../../patterns/review-loop.md)). **Exit criterion (the shared, tested rule):** each round, compute
   `python3 -E "${CLAUDE_PLUGIN_ROOT}/bin/af.py" review-decision --verdict <approve or changes> --iteration <n> --gate-green <yes if prd.md validates, else no>` (see
   [adversarial-review.md](../../patterns/adversarial-review.md), bounded by
   [review-loop.md](../../patterns/review-loop.md)) — `revise` (loop back and fix worst-first),
   `escalate` (still `changes` at N = 3 → **commit nothing; mark the feature PR a draft** (the merge gate already refuses a draft), set the artifact's `review_decision` to `escalate` (never touch its `status`, the repo's lifecycle field), surface the unresolved gaps and stop; that field is what makes "don't hand off" enforceable — the file is already on disk), or
   `proceed` (**commit this phase's artifact and push — opening or updating the feature PR per [doc-delivery](../../patterns/doc-delivery.md)**; `approve` **and** the PRD validates → the doc is done). Don't hand off a PRD with
   untestable acceptance criteria.

## Output

**A full product run produces the finished feature documentation: a complete, validated `prd.md`**
(see [patterns/handoff.md](../../patterns/handoff.md)) — goals, non-goals, metrics, testable
acceptance, and user stories — that survived the bounded skeptic loop to `proceed`, ready as the
input to `architecture`. A run whose loop `escalate`s (unresolved gaps at N = 3) surfaces them and
stops; it does **not** hand off an incomplete PRD. **An amend run** produces the amended PRD, in its
own format, and its final review round beside it.

## Definition of done

- The skeptic loop exited on `proceed` (`review-decision`): `approve` **and** `prd.md`
  validates — not `escalate`.
- `prd.md` validates against the prd handoff schema (goals + acceptance present).
- Non-goals and success metrics are stated; user stories cover the goals.
- Requirements trace to the research brief; ambiguities were elicited, not invented.
- A bounded skeptic pass checked acceptance-criteria testability and metric measurability.
- Only product requirements — no technical design or code.
- In amend mode: the PRD keeps its own format (no YAML added to a foreign one, no `status` or
  metadata rewritten unasked), the diff holds only the requested change and what it forces, and the
  loop reviewed that diff ([references/amend.md](references/amend.md)).
