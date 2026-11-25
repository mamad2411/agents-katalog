---
name: evals-e2e-run
description: Evaluate a just-implemented feature end-to-end across its whole chain — storm, design, plan, implementation — scoring artefact quality (storm_quality, design_quality, plan_quality) and stage-to-stage consistency (design_consistency, plan_consistency, code_storm_consistency, code_design_consistency, code_plan_consistency), appending one JSON entry per eval to ~/.claude/evals/design.json. Use when the user wants to evaluate a finished feature, "run e2e evals", score the feature pipeline, or measure how well the storm/design/plan/implementation artefacts line up — typically right after /feature-implement has landed its stage commits and before they are pushed; the expected initiator is /feature-implement itself at the end of a run. Every score is 0–100 (higher is better); scores below 80 carry a ≤100-word recommendation for improving the responsible feature-* skill. Read-only with respect to the repo — never modifies project files, never commits, never pushes; its only write is the eval log. Step 0 confirms with the user via AskUserQuestion before doing any work when invoked proactively; the confirmation is skipped when the user explicitly typed /evals-e2e-run.
user-invocable: true
disable-model-invocation: false
argument-hint: <optional base ref to diff against when the branch has no upstream, or omit to use @{u}>
allowed-tools: Read, Grep, Glob, Write, AskUserQuestion, Agent, Bash(git *), Bash(ls *), Bash(find *), Bash(date *), Bash(pwd), Bash(test *), Bash(mkdir *), Bash(basename *), Bash(mv *), Bash(cat *), Bash(wc *), Bash(jq *), Bash(python3 *)
---

# evals-e2e-run — Score a feature's end-to-end chain

You are running the `evals-e2e-run` skill. The user may have arrived here by typing `/evals-e2e-run` (with an optional base ref in `$ARGUMENTS`) or because the model proactively invoked the skill. Your job is to evaluate a feature that was just implemented through the feature-* chain — its storm, design, and plan artefacts plus the implementation commits — score every applicable quality and consistency dimension 0–100, and append one JSON entry per eval to `~/.claude/evals/design.json`.

The expected flow is that this skill runs at the **end of a feature implementation** — normally initiated by `/feature-implement`'s closing eval offer (its Step 11), or typed directly. It therefore does not gate on proving that the unpushed work "is" a feature; being invoked implies it. It resolves the most recently implemented feature and evaluates whatever parts of its chain exist.

The scores build a longitudinal record of how well the `feature-storm → feature-design → feature-plan → feature-implement` chain performs, artefact by artefact and hand-off by hand-off, so honest, evidence-based scoring matters more than flattering numbers. **Higher is better** here (100 = flawless) — the opposite polarity to `evals-code-run`'s defect scores; the two logs are separate files partly for that reason.

This skill is **read-only with respect to the repo**: it never modifies project files, never stages, commits, checks out, or pushes anything. Its only write is the eval log under `~/.claude/evals/` (plus a sibling backup if that log turns out to be corrupt).

This skill has six steps (Steps 0–5). Execute them in order.

## Step 0 — Proactive-invocation confirmation

Check the current conversation turn for the literal tag `<command-name>/evals-e2e-run</command-name>` (or the plugin-qualified form). If present, the user explicitly invoked the skill — skip to Step 1.

Otherwise you are being invoked proactively. Ask once via `AskUserQuestion`:

- Question: "Run end-to-end feature evals for the just-implemented feature (artefact quality + stage-to-stage consistency), appending scores to ~/.claude/evals/design.json?"
- Options: **"Yes, run the evals"** (Recommended — read-only analysis, one log append) / **"No, skip"**.

If the user declines, stop. If you are running in a context with no user channel (e.g. inside a subagent), proceed only when the calling agent's brief explicitly told you to execute this skill; otherwise stop.

## Step 1 — Resolve the feature, its artefacts, and the evals to run

1. Confirm you are inside a git repository (`git rev-parse --show-toplevel`). If not, tell the user and stop.
2. Determine the **base** the implementation diffs against:
   - If `$ARGUMENTS` contains a ref, verify it resolves (`git rev-parse --verify <ref>`) and use it. If it doesn't resolve, tell the user and stop.
   - Otherwise use the branch upstream: `git rev-parse --abbrev-ref --symbolic-full-name @{u}`.
   - If there is no upstream but `origin/HEAD` resolves, use it and say so in the final summary.
   - If neither exists, there is no base — the three `code_*` evals will be skipped (noted in the summary); the artefact evals can still run.
3. Identify the **feature version `<N>`**:
   - Preferred: from `feature-implement`'s stage commits in the unpushed range — `git log <base>..HEAD --extended-regexp --grep='\(plan v[0-9]+\): Stage [0-9]+' --pretty=%s`. Take the **highest** `<N>` when several appear, and note the others in the final summary. This also yields the stage-commit SHAs for point 5.
   - Fallback (no base, or no stage-format commits): the highest-versioned `features/feature-v<N>-*/` folder — numeric compare on `<N>`, so `v10` > `v9`.
   - If `features/` contains no feature folders at all, there is nothing to evaluate — tell the user and stop **without writing anything** to the eval log.
4. Locate the feature folder: `ls -d features/feature-v<N>-*/` from the repo root. Expect exactly one; if several match, take the most recently modified and note it. Do **not** call `feature-resolve` — it creates folders and seeds trackers on first use, and an eval must never mutate `features/`. Read-only globbing is the deliberate exception here. Then check which artefacts exist inside the folder:
   - storm: `feature-storm-v<N>-<desc>.md`
   - design: `feature-design-v<N>-<desc>.md`
   - plan: `feature-plan-v<N>-<desc>.md`
5. Collect the **implementation change set**:
   - Preferred: the stage commits for this feature — `git log <base>..HEAD --extended-regexp --grep='\(plan v<N>\): Stage' --oneline` — plus their diffs (`git show <sha>` per commit), with the full `git diff <base>...HEAD` available as secondary context.
   - If there are no stage commits but there are unpushed commits, the whole unpushed diff (`git diff <base>...HEAD`) is the implementation change set.
   - If there is no base or no unpushed commits at all, there is **no implementation change set** — the three `code_*` evals are skipped and noted in the summary.
6. Select the evals from this table — an eval whose required inputs are missing is skipped and produces **no** log entry:

   | eval_type | Runs when | Judges | Recommendation targets |
   |---|---|---|---|
   | `storm_quality` | storm exists | storm vs product-design best practices | `feature-storm` |
   | `design_consistency` | storm + design exist | design vs storm | `feature-design` |
   | `design_quality` | design exists | design vs software-design & UX best practices | `feature-design` |
   | `plan_consistency` | design + plan exist | plan vs design | `feature-plan` |
   | `plan_quality` | plan exists | plan vs implementation-planning best practices | `feature-plan` |
   | `code_storm_consistency` | storm + change set exist | implementation vs storm | `feature-implement` |
   | `code_design_consistency` | design + change set exist | implementation vs design | `feature-implement` |
   | `code_plan_consistency` | plan + change set exist | implementation vs plan | `feature-implement` |

7. If none of the three artefact files exists, no eval can run (the `code_*` evals also need an artefact to compare against) — explain that and stop without writing.

A chain-produced feature always has a design and a plan, so the usual selection is five evals (no storm) or all eight.

## Step 2 — Run the evals (parallel subagents)

Launch **one subagent per selected eval** (general-purpose, read-only intent), all in a single message; each inherits the session model and effort. The evals are fully independent, so parallelism is free wall-clock time. If the Agent tool is unavailable in your context, run the same analyses yourself, sequentially, applying the briefs below verbatim.

Each subagent knows nothing about this conversation, so its brief must be self-contained. Include:

- The repo root, the feature folder path, and the absolute paths of the artefact files its eval reads.
- For the three `code_*` evals: the stage-commit SHAs (or the base ref when the change set is the whole unpushed diff) and the commands to reproduce the change set (`git show <sha>`, `git diff <base>...HEAD`).
- Its eval definition — the relevant rubric or consistency method below, copied verbatim — and the shared scoring model.
- Its literal `eval_type` string from the Step 1 table, with an instruction to echo it character-for-character in the output block.
- The output contract (below), and an instruction that its final message must be exactly one output block and nothing else.
- A hard constraint: read-only — it must not modify, stage, commit, or push anything.

### Shared scoring model

- Enumerate the items the eval assesses (rubric criteria for quality evals; upstream commitments for consistency evals). Judge each item **met** (1), **partially met** (0.5), or **unmet** (0).
- **score** = `round(100 × items_met / items_assessed)`, clamped to 0–100. Higher is better.
- Every deduction must cite evidence: a quoted section of the artefact, or `file:line` in the implementation. A deduction you cannot point at is not a deduction.
- Stay language- and domain-agnostic: judge structure and substance, not stack choices or formatting taste. A score of 100 is the correct outcome for a genuinely clean artefact — never manufacture deductions to look rigorous.

### Quality rubrics

**storm_quality** — judge the storm document against this rubric, item by item:

1. **Problem & motivation (§1)** — the summary states what is being built and why now. Partial = the what without the why.
2. **Users (§1)** — target users/actors are named specifically (a role, persona, or system — not "users" generically).
3. **Goal testability (§2)** — each goal bullet is testable: a reasonable person could agree the outcome was or wasn't achieved. Met = all bullets pass; partial = a minority fail; unmet = a majority fail.
4. **Explicit non-goals (§3)** — out-of-scope names actual deferred things, not generic disclaimers.
5. **Product altitude (§4)** — technical direction is framed as constraints the design must respect, never solutions ("Must run offline on iOS 16+" yes; "use SwiftData with CloudKit sync" no). Partial = constraints overall with isolated solution-level detail.
6. **Alternatives recorded (§5)** — at least one alternative is recorded with the reason it lost, or a credible "Not applicable — <reason>". Unmet = section missing, empty, or boilerplate.
7. **Feature-specific risks (§6)** — each risk names something that could plausibly go wrong with this feature specifically, with impact; generic boilerplate ("timeline risk") is unmet. A credible "Not applicable — <reason>" is met.
8. **Concrete open questions (§7)** — each item is a specific decision `/feature-design` must close (not "figure out the architecture"), with captured user preferences annotated.
9. **Structural completeness** — all seven sections present, each with real content or an explicit "Not applicable — <reason>".
10. **Requirement unambiguity** — for each goal and in-scope bullet: would two competent designers infer the same intended behavior? Met = all pass; partial = a minority fail; unmet = a majority fail.
11. **Scope decisiveness (§3)** — the in/out boundary is decided, not hedged: no "maybe", "probably", "possibly", "TBD", "depending on", or "we may also" qualifiers on scope items, and no capability mentioned elsewhere in the document (a goal, a risk, an alternative, an open question) that is left unplaced on the boundary. Product-level scope only — a §7 open question about *how* something is built is design-level uncertainty and does not count against this item. Partial = one hedged or unplaced item; unmet = several.

Items 3, 4, 5, 8, and 11 quote `feature-storm`'s own section content rules so producer and judge share one standard; if those rules change, re-sync this rubric.

**design_quality** — judge the design document against this rubric, item by item. The rubric is self-referential: it judges the design against its own sections and the code it cites — coverage of the storm's commitments is `design_consistency`'s job. Where an item allows "Not applicable", it is met only by an explicit, credible "Not applicable — <reason>" line (or the section's explicit none-wording), never by silence:

1. **Framing (§1, §2)** — the summary states what the feature is, who it is for, and what problem it solves; goals are concrete outcomes; non-goals name actual exclusions with a brief why, not generic disclaimers.
2. **Requirement testability (§3)** — each numbered requirement is testable. Met = all pass; partial = a minority fail; unmet = a majority fail.
3. **Requirements coverage (§3→§5)** — every numbered requirement in §3 maps to concrete design content in §5. Met = all mapped; partial = a minority unmapped; unmet = a majority unmapped.
4. **Grounded background (§4)** — the design cites real, specific code (`path:line`) and existing structures; with repo access, spot-check that a sample of citations resolves. Absent, generic, or (when checkable) invented references are unmet.
5. **Component decomposition (§5)** — each component has a single responsibility, a public interface, and named dependencies; a one-unit implementation carries an explicit rationale why splitting would be artificial.
6. **Implementable contracts (§5)** — data model, interfaces, and control flow are specified so a competent engineer can implement without re-deriving decisions. Partial = isolated re-derivation needed; unmet = wholesale.
7. **Failure and edge cases (§5)** — concrete behavior for each failure and edge case, not hand-waves.
8. **Security at trust boundaries (§5)** — authn/authz, input validation, and secret handling addressed where the feature has trust boundaries; a credible "Not applicable — <reason>" is met.
9. **User-facing flows and states (§5)** — user-facing surfaces specify flows and states (empty/loading/error/success); for a feature with no user-facing surface, a credible "Not applicable" is met. When the feature folder contains a `mockups/` directory, §5 must also cite the accepted mockup by relative path (with a `#<option>` fragment when the accepted option shares its page with others) and describe the surface as that mockup shows it — an uncited or contradicted mockup is unmet. When there is no `mockups/` directory but the feature has a user-visible surface, §5 must record which named skip condition applied (and, for an already-settled appearance, cite the user's own artefact); silence about a missing mockup is unmet.
10. **Per-component test plan (§5)** — each component named in *Architecture / components* has a unit-test plan that does not require the rest of the feature to be running.
11. **Trade-offs and simplicity (§6)** — actively-evaluated alternatives are recorded with why each was rejected (or an explicit "None — <reason>"); the chosen design shows no speculative generality.
12. **Mitigated risks (§7)** — each risk is specific to this feature with likelihood/impact and a mitigation; generic boilerplate ("timeline risk") is unmet; a credible "Not applicable — <reason>" is met.
13. **Decision closure (§8 + whole document)** — §8 is empty or exactly "None — all decisions closed.", and no TBD/TODO/FIXME/hand-wave language appears anywhere in the document.
14. **Rollout readiness (§9)** — phasing and rollback are addressed (flags/dark launch where relevant); a credible "Not applicable — <reason>" is met.
15. **Cross-section consistency (§5–§9)** — any scenario described in more than one section agrees on the same outcome everywhere it appears.
16. **Cross-project briefs (§5, §9)** — when the feature folder contains a `briefs/` directory, each brief is implementable by a reader with no access to this repo (no citations into it, no "see the design", no unstated contract field), states the same contract as §5's *Cross-project contract* field for field, and — where the two sides are built with cross dependencies — carries the same joint-plan statement as §9. When there is no `briefs/` directory, the item is met unless the design assigns work to another project without writing one.
17. **Design language (§5)** — when the feature has a user-visible surface, §5's *Design language* sub-section cites `DESIGN.md` and the specimen, lists the feature's language deltas with their `pending v<N>` status (or states there are none), and names any drift touching the surface; with repo access, spot-check that colours, type styles and components §5 names appear in `DESIGN.md` or in the delta list. A credible "Not applicable — no user-visible surface" is met.

Items 2, 5, 6, 9, 10, 13, 16, and 17 quote `feature-design`'s own template and self-review rules so producer and judge share one standard; if those rules change, re-sync this rubric. Item 9's mockup clause mirrors `feature-design` Step 5 and its *Mockup fidelity* self-review lens; item 16 mirrors its Step 6b and the *Cross-project brief completeness* lens; item 17 mirrors its §5 *Design language* sub-section and the *Design-language conformance* lens.

**plan_quality** — judge the plan document against this rubric, item by item. The rubric is self-referential: it judges the plan against its own sections and the code it cites — whether the plan honors the actual design is `plan_consistency`'s job. The plan template's sections are named, not numbered; items anchor to those names. Per-stage items are graded majority-rule across stages (met = all stages pass; partial = a minority fail; unmet = a majority fail); "Not applicable"/"None" is met only when explicit and credible, never by silence:

1. **Overview & structural completeness (*Overview* + all sections)** — the overview states what is built, how it is staged, and how it maps to the design; all ten template sections are present with real content or their explicit none-wording.
2. **Coverage map integrity (*Requirements coverage map*)** — every requirement row maps to at least one stage, every stage cited in the map exists under *Stages*, and no row is empty.
3. **Stage completeness (*Stages*)** — every stage carries its Goal (one sentence), *Design references*, *Touches* (concrete paths), Steps, *Definition of done* (checkable bullets), and stage risks ("None" allowed).
4. **TDD discipline (*Steps (TDD)*, per *Development strategy — Test-Driven Development*)** — every behavior-changing, host-testable stage has the four TDD steps in order with a concrete expected initial failure (not "it will fail"); every other stage carries one of the five sanctioned category labels declared in the strategy section, with a one-line justification — an unlabeled or ad-hoc category is unmet.
5. **Committable increments** — each stage ends with a working, tested, mergeable increment; no stage leaves the system broken between merges.
6. **Dependency-respecting order** — no stage relies on something a later stage introduces; a stage replacing an existing implementation states coexistence or an atomic swap.
7. **Right-sized, single-concern stages** — each stage is reviewable in one sitting, no trivial fragment stages, no stage mixes unrelated concerns; a deliberately-atomic large stage carries its recorded rationale.
8. **Grounded citations** — files, functions, and harnesses the plan cites as already existing resolve in the repo (spot-check with repo access); to-create paths are consistent across stages and follow a named sibling convention or the plan's own greenfield-convention stage. Absent, generic, or invented references are unmet.
9. **Cross-cutting concerns tracked (*Cross-cutting concerns*)** — security, performance, observability, and compatibility/migration are each tracked across stages or credibly noted as not applicable for this feature.
10. **Secure staging order** — no ordering window leaves the system insecure between merges (e.g. an endpoint live before its authz is wired); protections land with or before the code they protect; a credible no-security-surface note is met.
11. **End-to-end verification (*Verification*)** — states how the user confirms the feature against the design's acceptance criteria once all stages are complete, beyond per-stage unit tests where the work warrants it.
12. **Mitigated implementation risks (*Risks and open issues*)** — each risk is implementation-specific with a mitigation; generic boilerplate ("timeline risk") is unmet; a credible "None" is met.
13. **Decision-log purity (*Planning decisions taken*)** — exactly the none-line, or a numbered list where every entry is genuinely planning-level (stage order, flags, harness, file paths) with a one-line rationale; any design-level entry (scope, requirements, approach, interfaces) is unmet.
14. **Deviations discipline (*Deviations from the design*)** — exactly the none-line, or a numbered list with rationale; whether listed deviations are truthful against the design is `plan_consistency`'s job — judge form and explicitness here.
15. **Closure** — no TBD/TODO/FIXME/hand-wave language ("we'll just…", "should be straightforward") anywhere; open items live in *Risks and open issues* with mitigations.
16. **Execution schedule soundness (*Execution schedule*)** — every stage appears in exactly one batch, batches are numbered in execution order, and every pair of stages in a parallel batch clears all seven independence tests the plan skill applies — *Disjoint files*, *No symbol or string-keyed dependency*, *No shared registration point*, *Same base state*, *Category exclusions*, *Security ordering*, *No shared test resource* — with the *Why this mode* cell naming the evidence; a parallel batch violating item 6's ordering or item 10's security window is unmet, as is any stage split, merged or invented to create parallelism; the *Critical path* line is present and consistent with the table. A plan with no parallel batch is met when its all-serial table is present. A plan without the section is judged as item 16 unmet and item 1 partial — never silently as all-serial.

Items 3, 4, 7, 13, 14, and 16 quote `feature-plan`'s own template and review rules so producer and judge share one standard; if those rules change, re-sync this rubric.

### Consistency method

For every `*_consistency` eval: enumerate the **upstream** artefact's discrete commitments — requirements, decisions, constraints, and (for the plan) stages — then classify how the **downstream** artefact (or the implementation change set) treats each one:

- **Honored** (1): implemented/carried through as stated, or explicitly deferred/descoped downstream with acknowledgment — deliberate narrowing is the chain working as intended.
- **Partially honored** (0.5): present but diverges in a way the downstream artefact does not acknowledge.
- **Silently dropped or contradicted** (0): missing without a word, or the downstream does the opposite.

`code_plan_consistency` additionally checks the reverse direction: every plan stage has a matching stage commit, and no significant unplanned scope crept into the implementation. Stage commits may be interleaved with `docs:` and `fix:` reconciliation commits, and a stage's batch membership is never judged from commit order — `feature-implement` lands parallel batches in stage order regardless of which subagent finished first.

### Recommendation rules

The recommendation is **not** a project-specific fix — it is process feedback for the responsible skill (`skills/<slug>/SKILL.md`, per the Step 1 table). Phrase it as a generic, language-agnostic improvement to how that skill works (e.g. a sharper prompt in its clarification round, an extra self-review lens, a coverage check before writing), such that the gaps found this run would have been caught or prevented.

- Maximum 100 words. One recommendation per eval per run.
- If the score is **80 or above**, the recommendation is the empty string `""` — do not manufacture advice for a healthy artefact.

### Subagent output contract

The subagent's final message must be exactly this block:

```
EVAL_RESULT
eval_type: <storm_quality|design_consistency|design_quality|plan_consistency|plan_quality|code_storm_consistency|code_design_consistency|code_plan_consistency>
items_assessed: <N>
items_met: <N, halves allowed>
score: <0-100 integer>
findings:
- <artefact section or file:line — one-line description of the deduction>
recommendation: <one paragraph, ≤100 words, or empty>
END_EVAL_RESULT
```

(`findings:` may be followed by `- none` when the score is 100.)

## Step 3 — Validate the results

For each returned result block:

- Verify `eval_type` is exactly one of the eight literal names above (underscored, lowercase). If a subagent returned a variant spelling, correct it to the literal name of the eval it was briefed for — never let a variant reach the log.
- Recompute `round(100 × items_met / items_assessed)` and use that as the score if the subagent's arithmetic disagrees; clamp to 0–100.
- Verify score and findings are consistent: a score below 100 with no cited findings, findings with no deductions, or a sub-80 score with an empty recommendation means the block is unreliable — re-run that one eval (once) with the same brief before accepting it.
- Trim any recommendation over 100 words down to its core; force the recommendation to `""` whenever the score is ≥80.

If a subagent failed or returned garbage twice, run that eval's analysis yourself using the same brief rather than shipping a hole in the record.

## Step 4 — Append to ~/.claude/evals/design.json

The log is a **single JSON array**; this run appends one entry object per eval actually run (typically five or eight) with **exactly these five fields** — no extras, no omissions:

```json
{
  "repo_name": "<repo name>",
  "timestamp": "<UTC ISO-8601, e.g. 2026-07-04T10:12:00Z>",
  "eval-type": "storm_quality",
  "score": 86,
  "recommendation": "…or the empty string"
}
```

- `repo_name`: basename of `git remote get-url origin` with any `.git` suffix stripped; if there is no `origin`, the basename of `git rev-parse --show-toplevel`.
- `timestamp`: one `date -u +%Y-%m-%dT%H:%M:%SZ` value shared by all entries of the run, so a run is identifiable in the log.
- `eval-type`: exactly one of the literal strings `storm_quality`, `design_consistency`, `design_quality`, `plan_consistency`, `plan_quality`, `code_storm_consistency`, `code_design_consistency`, `code_plan_consistency` — copy them character-for-character (underscored, lowercase); never abbreviate, rephrase, or re-case them, since log consumers match on these exact values. The field name itself is hyphenated to match `~/.claude/evals/code.json`'s schema. All selected evals are written, including score-100 ones — a clean run is signal too. Skipped evals (missing inputs) write nothing, so entry count varies per run; consumers must key on `eval-type`, never on position.

Append with a read-modify-write that cannot half-destroy the log. Preferred: a `python3` heredoc that loads the file (missing or empty file → `[]`), extends the array, and writes atomically via a temp file + `os.replace` in the same directory:

```bash
mkdir -p ~/.claude/evals
python3 - <<'EOF'
import json, os, tempfile
path = os.path.expanduser('~/.claude/evals/design.json')
new_entries = [
    # the entry objects, filled in literally for this run
]
data = []
if os.path.exists(path) and os.path.getsize(path) > 0:
    with open(path) as f:
        data = json.load(f)
data.extend(new_entries)
fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), suffix='.tmp')
with os.fdopen(fd, 'w') as f:
    json.dump(data, f, indent=2)
    f.write('\n')
os.replace(tmp, path)
print(f'{len(new_entries)} entries appended; log now has {len(data)}.')
EOF
```

If `python3` is unavailable, do the same with the Read and Write tools and then verify the result parses (`jq . ~/.claude/evals/design.json`).

If the existing file **fails to parse**: do not silently discard it. Move it aside to `~/.claude/evals/design.json.corrupt-<UTC timestamp>`, start a fresh array containing this run's entries, and tell the user about the backup in the final summary.

## Step 5 — Present the summary

Report in chat, in this order:

1. What was evaluated: the feature version and folder (and whether it was resolved from stage commits or by the latest-folder fallback), the base ref, the stage-commit count, which artefacts were found and therefore which evals ran or were skipped — including the `code_*` evals when there was no implementation change set; a note if other feature versions or unrelated commits sat in the unpushed range.
2. A compact score table:

   | Eval | Score | Items met / assessed |
   |---|---|---|
   | storm_quality | 86% | 6.5 / 8 |

3. For each eval scoring below 80: the top findings (with their evidence) and the recommendation.
4. Confirmation of the log write: "N entries appended to `~/.claude/evals/design.json` (log now has M entries)." — plus the corrupt-backup note if Step 4 needed one.

This skill does **not** call `lessons-capture` — like `evals-code-run`, it is a recording skill, and its recommendations already have a home (the JSON log).

## Constraints (non-negotiable)

- **Read-only with respect to the repo.** Never modify, create, stage, commit, checkout, or push anything in the project. Subagent briefs must carry the same constraint.
- **The only write is `~/.claude/evals/design.json`** (and its `.corrupt-<ts>` backup when needed). Never write under the project's `features/`, `bugs/`, or `docs/`.
- **Never call `feature-resolve`.** It creates folders and seeds trackers on first use; this skill locates artefacts by read-only globbing instead.
- **Nothing to evaluate → nothing written.** No feature folder, or a folder with no artefact files, means stop without touching the log.
- **Exactly five fields per entry, one shared timestamp per run, entries only for evals that ran.** Consumers of the log depend on the shape staying stable.
- **Higher is better.** 100 = flawless, and sub-80 is the recommendation threshold — do not import `evals-code-run`'s defect polarity.
- **Evidence or it didn't happen.** Every deduction traces to a cited finding; every score ≥80 carries an empty recommendation. Do not pad.
- **Committed-but-unpushed only.** Uncommitted working-tree changes are out of scope by design; mention them, don't evaluate them.
- **No symlinks**, per plugin-wide convention.
