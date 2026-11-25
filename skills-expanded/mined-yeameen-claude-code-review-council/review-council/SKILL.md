---
name: review-council
description: Multi-agent code review by delegating to (1) codex-cli with gpt-6-astra high, (2) gemini-cli with Gemini 3.8 Flash (High), and (3) five Claude specialist subagents (security, performance, logic, regression, robustness — the last one run blind, without the intent briefing) spawned via the Agent tool — then synthesizing all seven streams with your own diligence. Use this whenever the user asks for a deep review, second opinion, council review, multi-tool review, or wants the most thorough analysis of code changes / a PR / a commit / staged changes / a branch — even if they don't explicitly say "review-council". Stronger than any single-model review because different model families catch different classes of issues and the specialist subagents add focused depth on each axis; the synthesis step verifies findings against the actual code before applying fixes.
---

# review-council

Run seven flagship-effort reviewers on the same change in parallel — Codex CLI, Gemini CLI, and five Claude specialist subagents (security, performance, logic, regression, robustness — the last one run blind) — then synthesize all of their feedback into a unified, verified report. Apply fixes only after you've confirmed each finding against the real code.

## Why this skill exists

Different model families miss different things, and even within one family, a focused specialist prompt finds issues that a holistic prompt sails past. Codex (GPT lineage) and Gemini bring vendor independence; the five Claude specialists bring axis depth. Their union catches substantially more real issues than any one alone — but they also produce false positives that look authoritative. The value is in the **synthesis**: dedupe across all seven streams, verify each claim by reading the code, decide which fixes to apply, and use the resume / re-prompt mechanisms to push back on dubious findings rather than blindly applying them.

One reviewer (robustness) deliberately runs **blind** — diff only, no intent briefing. Field experience: a context.md note saying "unresolvable values are dropped by design" anchored six intent-briefed reviewers away from the drop path, and a human reviewer without that framing then found real hardening gaps there (case-sensitive marker matching, curly-apostrophe lookups). Intent briefing catches divergence-from-intent; blindness catches what the framing declared uninteresting. You want both.

Do not just paste the seven reports together and call it done. The user wants your judgment layered on top.

## When to use

Trigger on any of: "review this change/PR/commit", "second opinion", "council review", "multi-tool review", "review with codex and gemini", "what does codex/gemini think", "thorough review", "deep review". Also offer it proactively before risky merges (security-sensitive code, migrations, infra changes) if the user is pondering review depth.

## Workflow

### 1. Determine scope

Ask the user only if ambiguous. Otherwise infer from context:

| User intent | Scope |
|-------------|-------|
| "review my changes" with dirty tree | uncommitted (staged + unstaged + untracked) |
| "review this branch" / "review the PR" | diff vs main (or whatever the PR's base is) |
| "review commit abc123" | that specific commit |
| GitHub PR number given | fetch with `gh pr diff <num>` |

Capture the scope as a short label (e.g. `uncommitted`, `branch:feature/x vs main`, `commit:abc123`) — you'll feed this to both tools and use it in the final report.

### 2. Build a workspace

Create a workspace directory to hold both reports and any follow-up exchanges. This keeps everything inspectable and lets you reference the raw outputs later.

```bash
WS="/tmp/review-council-$(date +%s)"
mkdir -p "$WS"
```

Save the diff once so both tools see exactly the same input:

```bash
# Pick the right one for your scope
git diff HEAD > "$WS/changes.diff"                    # uncommitted (tracked)
git diff main...HEAD > "$WS/changes.diff"              # branch vs main
git show <sha> > "$WS/changes.diff"                    # specific commit
gh pr diff <num> > "$WS/changes.diff"                  # GitHub PR
```

Also write a short `context.md` with: scope label, repo path, key files touched, and any project conventions worth flagging (CLAUDE.md highlights, e.g. "this repo uses dynaconf settings — no hardcoded thresholds"). Both reviewers will benefit from this framing.

### 3. Run all seven reviewers in parallel

This step is one **single message** with multiple tool calls so everything runs concurrently:

- **One Bash call** that backgrounds codex + gemini with `&` and captures their PIDs (don't `wait` yet — let the Agent calls run in parallel with them).
- **Five Agent tool calls** (one per specialist) in the same message.

Codex/gemini take 3–8 minutes at flagship effort; the Claude specialists usually finish faster. Tell the user up front: "Kicking off seven reviewers — codex, gemini, and five Claude specialists (security, performance, logic, regression, robustness). Expect 3–8 min wall time." Don't go silent.

#### Codex (gpt-6-astra, high effort)

Codex's `review` subcommand writes a structured report with severity tags. **Always use it in prompt-mode** so Codex sees the same intent (PR description, project conventions, out-of-scope items) that Gemini and the intent-briefed Claude specialists get from `context.md` (the blind robustness agent is the deliberate exception). Without intent, Codex misses entire classes of "implementation diverges from stated rule" findings — verified empirically: in an A/B test on the same diff, prompt-mode caught 3 P1s (including a stated-rule violation) that no-prompt mode could not surface.

**Important CLI constraint**: `--base/--commit/--uncommitted` are **mutually exclusive** with `[PROMPT]`. The CLI rejects the combo with `error: the argument '--base <BRANCH>' cannot be used with '[PROMPT]'`. So when you want intent, inline the diff into the prompt yourself and drop the scope flag:

```bash
codex review \
  --title "<commit subject or scope label>" \
  -c model="gpt-6-astra" \
  -c model_reasoning_effort="high" \
  - <<EOF > "$WS/codex.out" 2> "$WS/codex.err" &
$(cat "$WS/context.md")

When reviewing, focus on whether the diff actually accomplishes its stated intent above. Severity-tag (P0–P3) as usual. Call out where the implementation diverges from what the description claims, AND respect any out-of-scope items the description says are deliberately deferred (don't re-flag those).

Diff:
$(cat "$WS/changes.diff")
EOF
CODEX_PID=$!
```

The structured P0/P1/P2/P3 output behavior is preserved when you use `[PROMPT]` — you don't lose the review template, you augment it.

**When prompt-mode is impractical**: if the diff is so large that inlining it would blow Codex's context window (rare — a few thousand lines fits), fall back to flag-only mode (`codex review --base main ...`) and accept that Codex will be intent-blind. Flag that limitation in the synthesis so the user knows the council was uneven.

**Do not use `codex exec`** for code review — `codex review` with a prompt gives you the same custom-prompt flexibility AND the structured severity-tagged output. `codex exec` is a generic agent runner and produces unstructured prose.

#### Gemini via Antigravity CLI (`agy`)

The standalone `gemini` CLI is dead (`IneligibleTierError` — individual tier deprecated 2026). Use the Antigravity CLI `agy` instead (verified v1.1.0): non-interactive mode is `--print`, model names come from `agy models` (use "Gemini 3.8 Flash (High)"), and `--dangerously-skip-permissions` is the yolo-equivalent so it doesn't stall on tool confirmations. Set `--print-timeout 9m` (default 5m is tight for flagship reviews). `--add-dir` grants repo access:

```bash
agy --print "$(cat <<EOF
You are a senior code reviewer. Review the diff below against the repo
at $(pwd). Focus on correctness, security, performance, SOLID violations,
race conditions, and project-convention drift. Cite file:line for each
finding. Categorize as P0 (block merge) / P1 (fix before merge) / P2
(follow-up) / P3 (nit). Be specific — vague findings like "consider
adding tests" are not useful.

Scope: <scope label>

Diff:
$(cat "$WS/changes.diff")
EOF
)" --model "Gemini 3.8 Flash (High)" --dangerously-skip-permissions \
  --add-dir "$(pwd)" --print-timeout 9m \
  > "$WS/gemini.out" 2> "$WS/gemini.err" &
GEMINI_PID=$!
```

#### Claude specialist subagents (Agent tool, five parallel calls)

In the **same message** that launches the bash backgrounded codex/gemini, also issue five `Agent` tool calls. Use `subagent_type: "general-purpose"` (no specialist subagent type exists for these axes; the focus comes from the prompt, not the type). Each gets the diff path and the context file. Pass `run_in_background: false` so the results return inline once they finish — but because they're issued in the same message as the others, they all start in parallel.

**Fallback when the Agent tool is unavailable** — if you're running this skill from inside a subagent, the Agent tool may not be in your toolset (nested-subagent restriction). In that case do not skip the specialist pass — instead run the five reviews in-context yourself. Read the diff and PR body once, then produce five sequential focused analyses keyed to security/performance/logic/regression/robustness with the same axis discipline described below (for the robustness pass, deliberately re-read the raw diff ignoring the intent notes), and save each to `<workspace>/claude-<role>.md` as if a real subagent had written it. The output quality is comparable; you just lose parallelism within this turn. Note the fallback in the final report so the user knows specialists ran serially.

For each subagent, the prompt should:
- Brief the agent like a smart colleague who just walked in: state what change is being reviewed, the scope label, the diff path (`<workspace>/changes.diff`), and the repo path.
- Define their **single axis** of focus and tell them explicitly to ignore findings outside that axis (the other specialists and the holistic reviewers cover those).
- Require file:line citations and P0–P3 severity.
- Cap the response length so the synthesis isn't drowning in prose: "Report under 500 words. Be specific — vague concerns like 'consider adding tests' are not useful."
- **EXCEPTION — the robustness agent runs blind**: give it the diff path and repo path only. Do NOT give it `context.md`, the PR description, or any "by design / out of scope" notes. Those notes anchor reviewers away from the very paths the author declared intentional, which is exactly where this agent must look.

The five roles:

1. **Security** — vulnerabilities, data safety, authn/z, injection, secrets, PII handling, unsafe deserialization, SSRF, crypto misuse, dependency CVEs implied by the diff.
2. **Performance** — latency, memory pressure, disk usage, N+1 queries, unnecessary shuffles/repartitions in PySpark, hot-path allocations, missed caching opportunities, big-O regressions. Tell it whether the repo is PySpark-heavy (check `pyproject.toml` / requirements) and to weight Spark-specific concerns accordingly.
3. **Logic** — correctness against the change's stated intent. If a PR description / commit message exists, paste it into the prompt and tell the agent its job is to verify the diff actually does what the description claims (and to flag where it doesn't). Off-by-one, null handling, error swallowing, race conditions, incorrect aggregation boundaries.
4. **Regression** — breaking changes to existing functionality, output schemas, public APIs, downstream contracts. Have it grep for callers of changed functions / consumers of changed tables / external schema files and call out anything the diff would silently break. This is the axis the holistic reviewers most often miss.
5. **Robustness (BLIND — diff + repo only, no intent briefing)** — input-domain drift and hardening over time. Its checklist: (a) anywhere the code exact-matches or dict-looks-up externally-controlled strings — case, whitespace, punctuation (curly vs straight apostrophes), and Unicode variants WILL drift across providers and over time; (b) silent-drop/filter paths — what happens to rejects, and would anyone notice systematic over-dropping?; (c) type and shape assumptions on provider data; (d) size assumptions — what breaks or degrades if the collection is 100× typical?; (e) invariants the change relies on that nothing enforces (duplicate keys, subset relations, ordering) — name the missing test. Cheap speculative hardening is allowed on this axis; have it tag such findings "hardening" so synthesis weighs them as robustness improvements rather than bug claims.

Ask each to write its report to `<workspace>/claude-<role>.md` so all seven streams land in the same place for synthesis.

#### Wait for codex/gemini, gather subagent results

After the message that kicks everything off, you'll have:
- A bash background job running codex + gemini (PIDs in shell vars).
- Four Agent results coming back as tool results.

The Agent results return when each subagent finishes. Once you have all four, run a `wait` for the bash PIDs to drain codex/gemini:

```bash
wait $CODEX_PID $GEMINI_PID
```

If the Claude specialists finish well before codex/gemini, you can start verifying their findings against the code (Step 4 work) while waiting — useful work in dead time.

### 4. Synthesize — this is where you earn your keep

Read all seven outputs (`codex.out`, `gemini.out`, `claude-security.md`, `claude-performance.md`, `claude-logic.md`, `claude-regression.md`, `claude-robustness.md`). Build a single deduplicated finding list. For each finding, do **all** of the following:

1. **Verify against the code.** Open the cited file:line. Does the issue actually exist as described? Reviewers hallucinate — especially about call sites they didn't read. If the citation is wrong, demote or drop the finding.
2. **Tag sources.** Use a compact bracket like `[CODEX|GEMINI|sec|reg]` listing every reviewer that flagged it (codex, gemini, and which Claude specialists by short name: `sec`, `perf`, `logic`, `reg`, `rob`). The more reviewers that independently flagged something, the higher confidence — but verify even the unanimous ones, because shared blindspots happen too.
3. **Re-rate severity.** The reviewers' P0/P1/P2/P3 tags are starting points, not gospel. A "P0" that's actually a style nit gets downgraded; a "P3" that's a real race condition gets upgraded. Use your own judgment after reading the code.
4. **Note disagreements.** If codex says "this is fine" about something gemini flags (or one specialist contradicts another's framing), surface it — the user should see where the council split.
5. **Watch for axis bleed.** A specialist sometimes wanders outside its lane (security agent flagging a perf issue, etc.). That's fine to keep — but note it, because findings outside an agent's stated focus are weaker signal than findings inside it.
6. **Measure before dismissing.** Any dismissal (yours or a reviewer's) that rests on an assumed data shape or size — "n is single digits", "that input never occurs", "this field is always uppercase" — gets the real number first: query the warehouse/DB if the project has one, or grep fixtures and real samples. Field experience: a perf finding was dismissed with "n is single digits" when the real production max was 221 — the human reviewer was right and the council was wrong. An unmeasured empirical claim is not a verification.
7. **Convert manual verifications into tests.** If verifying (or dismissing) a finding required hand-checking an invariant — "no duplicate keys", "strict subset", "never null here" — that invariant is load-bearing and unguarded. Add a unit test asserting it to the proposed fixes, even when the finding itself is dismissed. The act of needing to check it by hand is the proof the test is missing.
8. **Audit the drop path on data transforms.** Replay-style verification (run real inputs through the new logic, compare to stored outputs) proves *consistency*, not *completeness* — an input that the logic silently drops produces a perfect match while still being a bug. When the diff adds filtering/matching/lookup logic, also sample the **rejected** items from real data and eyeball them for systematic patterns (case variants, punctuation, double spaces) that should have matched.

### 5. Push back when needed

If a finding is suspicious — citation looks wrong, severity feels inflated, fix suggestion would break something — don't just dismiss it silently. Ask the original reviewer to defend itself. This is faster and more accurate than litigating from scratch.

**Codex** — verified syntax is `codex exec resume --last "<prompt>"`. `--last` resumes the most recently recorded session without a session ID. Confirmed against `codex exec resume --help`.

```bash
codex exec resume --last \
  "You flagged a P0 in pipeline/foo.py:42 about X. I read the code and
   the function actually does Y, which handles that case. Am I missing
   something, or should this be downgraded?" \
  > "$WS/codex.followup1.out" 2>&1
```

**Gemini (agy)** — `--continue`/`-c` resumes the most recent conversation (or `--conversation <id>` by ID):

```bash
agy --print "You flagged X. On re-reading, the code does Y. Defend or retract." \
  -c --model "Gemini 3.8 Flash (High)" --dangerously-skip-permissions \
  > "$WS/gemini.followup1.out" 2>&1
```

**Claude specialists** — Agent tool calls don't have a built-in resume. Either re-spawn a fresh `Agent` of the same role with the disputed finding + your counter-evidence in the prompt, or (if the original agent is still running in the background, which they aren't by default in this skill) use `SendMessage` to its name. For most cases, a fresh re-spawn is simplest and cheap:

```
Agent(subagent_type: "general-purpose",
      description: "Re-examine flagged finding",
      prompt: "Earlier review flagged <finding> in <file:line>. On re-reading
              the code, <counter-evidence>. Defend or retract this finding
              with specific code references. Under 200 words.")
```

Save each round to the workspace (`*.followupN.out` or `claude-<role>.followupN.md`) so the audit trail is intact.

### 6. Present the unified report

Before applying any fixes, show the user a synthesized report. Structure:

```
# Review Council Report — <scope label>

## Summary
- 7 reviewers ran: codex (gpt-6-astra high), gemini (3.8 Flash High), claude-{security,performance,logic,regression,robustness(blind)}
- N findings total (X verified, Y dismissed as false-positive after re-reading)
- M items flagged by 3+ reviewers independently (high-confidence)
- K items where reviewers disagreed (called out below)

## P0 — Block merge
- [CODEX|GEMINI|sec] file.py:42 — <one-line issue>. <why it matters>. Fix: <concrete>.
- [reg] file.py:108 — schema-breaking change to `gold_posts.author_id` type;
  consumed by narrative_aggregations.py:55. (Holistic reviewers missed this;
  the regression specialist caught it via grep for callers.) Fix: <concrete>.

## P1 — Fix before merge
- [GEMINI|perf|logic] file.py:230 — N+1 query inside `for user in users:` loop;
  perf agent flagged the latency, logic agent flagged that `user.posts` is also
  loaded eagerly. Codex thought this was fine — its reasoning relied on a cache
  that doesn't actually exist on this code path. Fix: <concrete>.

## P2 — Follow-up
...

## P3 — Nits
...

## Dismissed (false positives)
- [GEMINI] file.py:200 — claimed missing null check, but `foo` is non-null per
  the type signature in bar.py:14. Skipped after asking gemini to defend (see
  gemini.followup1.out — it retracted).
- [sec] file.py:300 — flagged SQL injection, but the value is a hardcoded enum
  validated at the boundary in validators.py:22. Skipped.

## Proposed actions
1. Apply fix for P0 #1
2. Apply fix for P0 #2
3. Open follow-up issue for P2 #1
4. Skip the rest

Want me to apply these fixes?
```

Then **stop and wait for the user**. Do not apply fixes without confirmation — the user may have context that changes what should land.

### 7. Apply fixes

Once approved, edit the files. After the edits:
- Run the project's tests / linters / type checks if they're cheap (`pytest <touched paths>`, `mypy`, etc.). Don't run a 20-minute full suite unless the user asked.
- For each applied fix, leave a one-line note in the final summary: what changed, what verified it.
- If a fix needs a judgment call you didn't already raise (e.g. an API rename ripples wider than expected), pause and ask rather than guessing.

## Cost / time guidance

Seven flagship-effort reviewers cost real money and 3–8 minutes of wall time. Don't run review-council for trivial changes (typo fixes, doc tweaks, single-file refactors with tests). Reach for it when the change is non-trivial: new business logic, security-sensitive code, infra/migrations, schema changes, or anything the user signals as high-stakes.

If the user invokes the skill on a trivial change, say so and offer the lighter `/pr-review` skill instead.

## Pitfalls to avoid

- **Don't paste raw outputs as the report.** The user can read all seven files themselves; your value is the synthesis.
- **Don't apply fixes before showing the report.** This is a review-first workflow — the user gates the edits.
- **Don't trust citations blindly.** All seven reviewers occasionally cite the wrong line or claim a function exists that doesn't. Always open the file.
- **Don't let one reviewer's silence imply agreement.** If only one source flagged something, the others may have just missed it, or may have actively considered it fine. Use re-prompts to find out which.
- **Don't run them serially.** Launch the bash backgrounded codex+gemini *and* the four Agent calls in the SAME message so everything starts in parallel. Issuing the Agent calls after `wait`-ing on bash wastes wall-time.
- **Don't skip `--dangerously-skip-permissions` on agy** in non-interactive mode — without it the process can hang on tool-confirmation that will never come.
- **Don't let the specialists drift wide.** If the security agent comes back with 80% style nits, its prompt was too soft — re-spawn with a tighter scope rather than synthesizing through the noise.
- **Watch for shared blindspots.** All seven reviewers can miss the same class of issue (e.g. a project-specific convention that isn't in the diff). Bring your own knowledge of the codebase as an eighth check, especially for regression and convention-drift findings.
- **Don't let context.md become a gag order.** "By design / out of scope" notes are for genuinely user-decided deferrals — they stop reviewers re-flagging known items, but they equally suppress scrutiny of those paths (verified in the field: an intent-briefed council missed hardening gaps in a "dropped by design" filter that a fresh human reviewer caught). Never mark something "by design" that you decided yourself rather than the user, and rely on the blind robustness reviewer to cover the declared-uninteresting paths.
- **Expect codex and gemini to fail sometimes — synthesize without them.** In practice the holistic CLI reviewers fail more often than you'd expect: codex sometimes returns empty stdout or a one-sentence non-answer despite exiting cleanly, and gemini has a small daily quota that browns out after a few runs (`TerminalQuotaError 429`, ~24h reset). Time-box each at a few minutes; if one returns empty/errored, surface it clearly in the report's "Reviewer execution status" section and synthesize from whatever streams *did* produce output. The five Claude specialists are reliable enough to carry a review on their own when the holistic reviewers are degraded — do not block the user waiting for retries that won't change anything.

## Quick reference — verified commands

```bash
# Codex review — prompt-mode (preferred: passes intent)
# Note: --base/--commit/--uncommitted are mutually exclusive with [PROMPT].
# Inline the diff in the prompt and drop the scope flag.
codex review \
  --title "<commit subject>" \
  -c model="gpt-6-astra" -c model_reasoning_effort="high" \
  - <<<"$CONTEXT_AND_DIFF"

# Codex review — flag-only mode (fallback for huge diffs; loses intent)
codex review --base main -c model="gpt-6-astra" -c model_reasoning_effort="high"
codex review --uncommitted -c model="gpt-6-astra" -c model_reasoning_effort="high"
codex review --commit <sha> -c model="gpt-6-astra" -c model_reasoning_effort="high"

# Codex follow-up (verified syntax)
codex exec resume --last "<prompt>"

# Gemini via Antigravity CLI (non-interactive; gemini CLI is dead — IneligibleTierError)
agy --print "<prompt>" --model "Gemini 3.8 Flash (High)" --dangerously-skip-permissions --print-timeout 9m

# Gemini follow-up (resume most recent conversation)
agy --print "<prompt>" -c --model "Gemini 3.8 Flash (High)" --dangerously-skip-permissions
```
