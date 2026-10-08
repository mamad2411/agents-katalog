---
description: Search skills for coverage, pick strongest per principle, write our own consolidated version, verify lossless + line-reduced.
---

$ARGUMENTS

---

# Search And Write Own Skill

Pipeline: (1) coverage audit of candidate skills → (2) per-row delegate verification (narrow aspect, parallel) → (3) pick strongest per row (coverage + wording) → (4) WRITE OUR OWN consolidated version → (5) verify LOSSLESS (no principle dropped) + LINE-REDUCED (our version ≤ strongest winner).

Builds on `audit-skill-coverage` (step 1-3). ADDS the synthesis (step 4) + lossless+compression verify (step 5).

## GOAL (DOD)

Given a principle set + candidate skills, deliver:
- A NEW skill/playbook FILE authored by us
- That COVERS every principle the union of winners covered (LOSSLESS)
- In FEWER lines than the strongest single winner (CONSOLIDATED)
- With STRONGER+MORE-CONCISE wording than any individual winner (BETTER)
- Verification report proving the 3 invariants

NOT a recommendation. AN ARTIFACT + proof.

---

## Steps (imperative)

### 1. Run `audit-skill-coverage` FIRST
- Produce the principle × skill coverage matrix.
- Identify ● cells.
- DO NOT skip. This pipeline's input = that audit's output.

### 2. Delegate PER ROW to verify (narrow aspect, parallel)
- ONE teammate per principle row. Each worker's scope = ONE principle across MULTIPLE skills (narrow aspect = deep, not wide).
- Task text MUST include:
  - The principle name + the ● skills list + their SKILL.md URLs (raw.githubusercontent, branch + path).
  - Fetch instructions (try main, then master).
  - Scoring rubric: **Coverage/Sophistication (weight 0.6)** 0-3, **Wording Strength+Conciseness (weight 0.4)** 0-3. Combined = c*0.6 + w*0.4.
  - Report format: per-skill scores table + WINNER (highest combined) + 2-line rationale + verbatim STRONGEST wording snippet (the exact sentences to lift).
- Spawn via `teams delegate`, `workspaceMode: shared`, `contextMode: fresh`. Name workers `row<N>-<principle>`.
- Leader: sleep 90-180s, poll `~/.pi/agent/teams/<UUID>/tasks/<UUID>/<N>.json` `status` + `metadata.result`. DO NOT use `session_status`/`session_progress` (they lie for team workers).
- **PIN team UUID explicitly.** `ls -dt ~/.pi/agent/teams/*/ | head -1` mtime ordering breaks when multiple teams exist → reads wrong team's tasks.

### 3. Pick strongest per row
- Per row: WINNER = highest combined score.
- Collect the verbatim STRONGEST wording snippet from each winner (worker reports it).
- Flag rows where sole winner scores < 2.0 → "shallow, market gap, hand-author".

### 4. WRITE OUR OWN VERSION (the synthesis)
Target file: per the playbook-save rules (global = `~/.pi/agent/prompts/` OR `~/.pi/agent/skills/<name>/SKILL.md`; local = `./.pi/prompts/` OR `./.agents/skills/<name>/SKILL.md`).

Author rules:
- **ONE section per principle.** Lift the strongest wording snippet from each row winner. REPHRASE for consistency (voice/tense/imperative mood), DO NOT copy-paste verbatim across sources (attribution drift).
- **Strip redundancy.** If 3 winners explain SRP the same way, keep the tightest phrasing ONCE.
- **Imperative mood.** "MUST / DO NOT / AVOID / NEVER". No hedging ("should consider", "might want to").
- **Detection smell per principle.** Every principle gets a "violation looks like → fix looks like" pair. This is the review-use-case enabler.
- **Cross-link, do not inline.** If a principle needs depth, put depth in `references/<topic>.md`, keep SKILL.md body terse.
- **Cap body at the line count of the strongest single winner.** If our draft exceeds it → trim. See step 5.

### 5. VERIFY — lossless + line-reduced (the gate)
This is the DOD gate. FAIL = rework.

#### 5a. Lossless check (every principle still covered)
```bash
for p in <original-principle-list>; do
  if ! grep -iq "<principle-pattern>" <our-file>; then
    echo "LOSSY: $p dropped"; exit 1
  fi
done
echo "LOSSLESS: all principles present"
```
- Use the SAME grep patterns from the audit (step 1). Word-boundary for acronyms.
- If ANY principle absent → LOSSY. Re-add before proceeding.

#### 5b. Line-reduction check (consolidation = compression)
```bash
OURS=$(wc -l < <our-file>)
WINNER=$(wc -l < <strongest-winner-file>)
if [ "$OURS" -gt "$WINNER" ]; then
  echo "BLOAT: ours=$OURS winner=$WINNER — trim"; exit 1
fi
echo "COMPRESSED: ours=$OURS ≤ winner=$WINNER (saved $((WINNER-OURS)) lines)"
```
- Our version MUST be ≤ the strongest single winner's line count.
- If ours > winner → we added bloat, not consolidation. Cut redundancy, push depth to `references/`.

#### 5c. Wording-strength spot check
- Re-read our file. Every rule MUST be imperative (no "should"). Every principle MUST have a detection smell.
- If a section reads descriptive → rewrite imperative.

### 6. Report
```
## Synthesized artifact
- Path: <our-file>
- Lines: <ours> (winner was <winner>, saved <delta>)
- Principles covered: <N> (lossless check: PASS)

## Per-row winner → our section
| Principle | Winner skill | Winner score | Our section |

## Verification
- Lossless: PASS (all <N> principles grepped present)
- Line-reduced: PASS (<ours> ≤ <winner>)
- Wording-strength: PASS (imperative + detection smell per principle)

## Callsouts
- Market gaps (rows flagged shallow): <list>
- Principles hand-authored (no winner qualified): <list>
```

---

## What WORKS (follow next time)

- **Delegate per ROW, not per skill.** One worker = one principle across N skills = narrow aspect = deep score. Per-skill workers repeat fetches and miss cross-skill comparison.
- **Demand verbatim strongest snippet in the worker report.** Lets you synthesize without re-fetching. Worker already read the file.
- **Weighted scoring (coverage 0.6 + wording 0.4).** Favors substance over style. Reverse weights only if use case is "quick reference card".
- **Pin team UUID explicitly.** `ls -dt | head -1` lies when multiple teams coexist. Hardcode the UUID from the `delegate` return.
- **One section per principle in our version.** Mirrors the audit matrix 1:1. Makes the lossless grep trivial.
- **Imperative mood + detection smell per principle.** Turns the file from "advice" into "enforceable review checklist". This is what makes it usable for review/scaffold.
- **references/ subdirs for depth.** Keep SKILL.md body ≤ winner. Push Liskov&Wing citations, worked examples, smell catalogs into `references/<topic>.md`.
- **Lossless grep uses the SAME patterns as the audit.** Consistency. If audit found SRP via `\bSRP\b`, verify uses `\bSRP\b`.
- **Line-reduction gate vs the strongest SINGLE winner (not the sum).** Sum is unfair (we're consolidating). Single winner is the right bar — we must beat the best one, not replicate all of them.

## What does NOT work (AVOID)

- **Copy-paste verbatim across winner sources.** Attribution drift + license risk + voice inconsistency. ALWAYS rephrase.
- **Per-skill delegation (one worker per skill).** Re-fetches the same file N times, no cross-skill ranking, shallow scores. Delegate per PRINCIPLE.
- **Trusting `ls -dt ~/.pi/agent/teams/*/ | head -1` for team UUID.** Mtime ordering breaks with concurrent teams. Read contamination = wrong results. PIN UUID.
- **Using `session_status`/`session_progress` for team state.** They report interactive sessions, not team workers. Read task JSON from disk.
- **Skipping the lossless check.** "I wrote all principles" belief = false. Synthesis drops principles silently. GREP PROVES it.
- **Comparing our line count to the SUM of winners.** Sum is unfair. Compare to the strongest SINGLE winner.
- **Inlining depth into SKILL.md body.** Bloats line count, fails the reduction gate. Push to `references/`.
- **Descriptive mood ("should consider").** Unenforceable. Reviewer cannot act on it. ALWAYS imperative.
- **Hand-authoring a principle without flagging it.** If no winner scored ≥ 2.0, that's a market gap — callsout it. DO NOT silently synthesize from thin air.
- **Averaging teammate disagreement on row winners.** Surface it. Disagreement catches single-leader blind spots.

## Tips / tricks

- **Worker report MUST include the strongest wording snippet verbatim.** Add this to the task text explicitly: "Quote the 2-3 strongest sentences for the winning skill verbatim." Saves re-fetching during synthesis.
- **Pre-fetch all candidate SKILL.md to `/tmp/<repo>.md` before spawning team.** Workers can `cat /tmp/...` instead of curl. Faster + avoids rate limits. Share the cache path in task text.
- **Use `references/` aggressively.** Anything beyond a 3-line rule → `references/<principle>.md`. SKILL.md body stays terse, passes line gate.
- **Detection smell = the review enabler.** Without it, the file is a textbook, not a reviewer. Format: "VIOLATION: <pattern> → FIX: <pattern>".
- **Score threshold for hand-author flag = 2.0.** Below = market gap. Hand-author + callsout.
- **Line-count the strongest winner BEFORE writing ours.** Sets the budget. Write to budget, not past it.
- **Grep patterns audit→verify MUST match.** Save them as a list during audit. Re-use verbatim in verify.
- **Name workers `row<N>-<principle>`.** Readable dashboard, no spawn collisions, easy result aggregation.
- **If a row has only 1 ● skill**, winner = that skill IF combined ≥ 2.0, else FLAG. Do not rubber-stamp a monopoly.

## Useful references (REMOTE only — global)

- Skillsmp marketplace: https://skillsmp.com
- Skillsmp search script: bundled in `skillsmp` skill (`scripts/skillsmp_search.py`)
- GitHub raw content: https://raw.githubusercontent.com/<owner>/<repo>/<branch>/<path>
- GitHub trees API (locate SKILL.md + count code files): https://docs.github.com/en/rest/git/trees
- Canonical software-design principles: https://github.com/webpro/programming-principles
- SOLID (Wikipedia): https://en.wikipedia.org/wiki/SOLID
- Liskov & Wing 1994 (LSP primary source): https://en.wikipedia.org/wiki/Liskov_substitution_principle
- Martin 1996 DIP paper: https://web.archive.org/web/20150906155826/http://www.objectmentor.com/resources/articles/dip.pdf
- Teams workflow skill (for per-row parallel verification): see `teams-workflow` + `teams-first` skills locally
- Predecessor cmd `audit-skill-coverage`: produces the coverage matrix input for this pipeline

## Mistakes / lessons learned

- **L1**: Used `ls -dt ~/.pi/agent/teams/*/ | head -1` to find my team → got an OLDER team's tasks (CI/Docker content, unrelated). LESSON: pin team UUID from the `teams delegate` return value. Mtime lies.
- **L2**: Delegated per-skill first → workers re-fetched the same files, no cross-skill ranking. LESSON: delegate per PRINCIPLE (row), each worker compares N skills.
- **L3**: Synthesized without demanding verbatim strongest snippet → had to re-fetch every winner to quote it. LESSON: worker report MUST quote the 2-3 strongest sentences verbatim.
- **L4**: Compared our line count to the SUM of winners → always failed (unfair bar). LESSON: compare to the strongest SINGLE winner.
- **L5**: Inlined Liskov&Wing worked example into SKILL.md body → bloated past winner line count. LESSON: push depth to `references/`, body stays terse.
- **L6**: Wrote a principle section in descriptive mood ("interfaces should be small") → unenforceable in review. LESSON: imperative + detection smell ("VIOLATION: 10-method Service interface → FIX: segregate per client").
- **L7**: Skipped lossless grep, trusted memory → dropped ISP in synthesis. LESSON: grep PROVES coverage. Memory lies.
- **L8**: Polymorphism row had no winner ≥ 2.0 → silently hand-authored. LESSON: flag as market gap, callsout in report.
- **L9**: `session_status` showed workers `[idle] 0 tokens` mid-task → false stuck read. LESSON: read task JSON `status` from disk, never `session_*` for teams.

## Other

- **Relationship to `audit-skill-coverage`**: that = benchmark (matrix + winners, no artifact). This = benchmark + AUTHOR our version + verify. Run that first, this consumes its output.
- **Relationship to `find-cli-agent-skills`**: that = discover ONE skill for ONE capability (adopt/skip). Different DOD. Do not confuse.
- **Global vs local output**: global cmd writes to `~/.pi/agent/` (remote-only refs in the cmd body). Local variant may reference project paths in the synthesized artifact.
- **Use-case fit**: output artifact serves scaffold / revise / review. Detection smell per principle = the review enabler. Without it, file = textbook, not reviewer.
- **Re-verify on edit**: any future edit to our synthesized file MUST re-run step 5 (lossless + line-reduced). Drift accumulates silently.
- **If a principle is genuinely uncovered by all candidates**: callsout as market gap. Hand-author from canonical remote source (Wikipedia, primary paper). DO NOT synthesize from nothing.
- **License/attribution**: rephrase, do not copy-paste. If quoting > 3 sentences verbatim from one source, cite it inline.
