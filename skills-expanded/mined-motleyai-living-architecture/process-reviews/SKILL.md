---
name: process-reviews
description: Use when the user asks to process / triage / address / handle PR reviews from CodeRabbit, SonarQube, Codex, and CI all together (CodeRabbit and Sonar only when they ran on the PR). Watches the PR every minute (30 min cap) and triages each new failed CI check, CodeRabbit comment and finished Sonar analysis as it appears, while a Codex review runs concurrently against the local diff. Once everything is terminal, fetches unresolved threads from all three code-review sources plus failed CI checks, validates each against the actual code / log, handles invalid ones in place (reply on thread / NOSONAR comment), and presents a unified plan for fixing the valid ones (split into logical groups if more than 3). Invoked from la:pr-review, it returns the triaged list instead.
---

**Preflight:** run `la-doctor --plugin <this skill's base directory>` once per session before using any `la-*` or `dr-*` command; if it fails, stop and show the user its output.

# Process unresolved review feedback (CodeRabbit + SonarQube + Codex + failed CI)

Combine CodeRabbit, SonarQube, Codex, and failed CI feedback into a single triage workflow: one sweep over every source. Run standalone, it stops at a written plan and does not start fixing. Invoked from `la:pr-review`, it returns the triaged list and `la:pr-review` fixes it.

**Sources on this PR.** Run `la-pr-reviewers <PR>` first. It prints `{"coderabbit": <bool>, "sonar": {"present": <bool>, "project_key": <key|null>}}`, detected from the PR itself, never from the repo config. Sonar counts as present once HEAD has a Sonar check suite, before its check run exists. Skip every step for a bot that is not on the PR (its fetches, validation, invalid-handling, and plan header count — show it as `off`). Re-run it at each sweep: CodeRabbit can first appear after a push.

**Codex follows `reviewers.codex`.** If `la-config get reviewers.codex` prints `false`, skip every Codex step and show Codex as `off`. Otherwise, if the Codex MCP server (`mcp__codex__codex`) is not available, STOP and tell me: this repo requires Codex reviews, so never skip one silently.

## Inputs

- PR number. If the user didn't say, infer from the cwd: `gh pr view --json number -q .number`. If that fails, ask the user.
- Repository (auto-detected from cwd via `gh repo view`, or pass explicitly).
- SonarQube project key (Sonar on the PR): `sonar.project_key` from `la-pr-reviewers`. When it is `null`, find the project with `mcp__sonarqube__search_my_sonarqube_projects`, or ask the user.

**Sonar fetching is MCP-only.** Use the `mcp__sonarqube__*` tools (`search_my_sonarqube_projects`, `search_sonar_issues_in_projects`, `get_project_quality_gate_status`, `search_security_hotspots`, `show_rule`). Do NOT shell out to the `sonar` CLI binary, do NOT invoke the `sonarqube:sonar-list-issues` skill (it wraps the CLI), and do NOT reach for raw `gh api` against the Sonar GitHub-App comments. If the `mcp__sonarqube__*` tools are not registered in this session, stop and ask the user to load the MCP — do not fall back to the CLI or `gh api`.

## Steps

### 0. Watch the PR (and kick off Codex in parallel)

Triage each source as soon as it reports, never a source that is still running: mid-flight CodeRabbit, Sonar or CI output is incomplete.

**Run Codex in parallel with the gate-wait.** Codex doesn't depend on GitHub — it analyses the local working-tree diff against the PR's base branch. Kick it off in the SAME assistant turn that arms the watch Monitor, so the two run concurrently. By the time the watch exits (often 5–15 minutes), Codex has already returned and you save that whole window.

Call `mcp__codex__codex` directly (don't shell out to the `la:codex-review` skill, which is the single-call form). Use `sandbox: "read-only"`, `approval-policy: "never"`, and `cwd` set to the repo root. Prompt template:

```
Review the PR diff for this branch against `origin/<base>`. Steps you should take:

1. Run `git fetch origin <base>` then `git diff --stat origin/<base>...HEAD` to scope the review to this PR's changes only.
2. For each changed file, read the diff (`git diff origin/<base>...HEAD -- <file>`) and the surrounding code as needed.
3. Flag actionable findings only. Categories: correctness, regressions, security, test gaps, maintainability, cross-file consistency, missed edge cases.
4. For each finding return: file:line range, severity (critical|major|minor|info), one-sentence summary, and a one-paragraph rationale.
5. Skip stylistic nits unless they materially impact readability. Skip findings you have less than 70% confidence in.

Do NOT modify files. Do NOT run tests. Return only the findings list (or "No findings." if clean). Be terse — no preamble.
```

Substitute the actual base branch (`main`, `master`, or what `gh pr view --json baseRefName --jq .baseRefName` returns) and run `mcp__codex__codex` once. Stash the response — you'll merge it into the normalised list at Step 2.

Never fall back to a different review tool when Codex is on (see "Codex follows `reviewers.codex`" above).

#### 0a + 0b. Watch status checks + CodeRabbit

Arm `la-wait-for-reviews <PR>` with the Monitor tool (`timeout_ms` at its maximum). It polls the PR every minute and prints one stdout line per new item, never the same item twice, even across runs:

- `ci-failed <sha> <url> <check>`: a check on HEAD failed;
- `coderabbit-comment <url>` / `coderabbit-review <url>`: a new CodeRabbit thread, reply, or review body;
- `sonar-done <sha> <conclusion>`: HEAD's Sonar analysis finished;
- `coderabbit-settled <sha> <outcome>`: reviewed, carried-forward, rate-limited, paused, skipped, or cap;
- `head-moved <old> <new>`.

On each event, run Steps 1–4 for that item alone, at once: `la-fetch-failed-pr-checks <PR> --check <url>` for a failed check (`--check <check>` when `<url>` is `-`), `la-fetch-coderabbit-threads <PR>` for a CodeRabbit item (triage only the named comment or review), the Sonar calls of Step 1 for `sonar-done`. If the Monitor expires before the command exits, re-arm the same command; it prints only what is new.

It exits 0 when every check on HEAD is terminal and CodeRabbit has settled on HEAD (or is not on the PR, or the 10-minute settle cap after the checks finish ran out), 1 if the checks do not finish within 30 minutes, and 3 when CodeRabbit was rate limited, paused or skipped its review on HEAD, once the checks finish.

A check is **non-terminal** if it's:
- a `StatusContext` with `state` ∈ {`PENDING`, `EXPECTED`} — CodeRabbit reports this way, OR
- a `CheckRun` or `WorkflowRun` with `status` ∈ {`QUEUED`, `IN_PROGRESS`, `WAITING`, `REQUESTED`, `PENDING`} — Sonar and GitHub Actions jobs report this way, OR
- a Sonar check suite on HEAD that is not `completed` — SonarQube Cloud creates its check run only when the analysis finishes.

Anything else (`SUCCESS` / `FAILURE` / `ERROR` / `COMPLETED`) counts as terminal — even a failed check is "done". Checks that are *missing entirely* from the rollup (e.g. CodeRabbit not installed on the repo) do not block — only checks that exist AND are non-terminal do.

Why Stage 0b is keyed to HEAD's SHA: CodeRabbit refreshes its summary as a placeholder seconds after a push, and its status reaches the rollup only when it finishes, so neither the rollup nor a timestamp shows whether HEAD was reviewed. Stage 0b reads only evidence tied to HEAD's SHA. The summary is the comment carrying the `summarize by coderabbit.ai` marker; command replies never count.

- **Reviewed** (exit 0): a CodeRabbit status on HEAD described `Review completed`, the summary's `final_review_risk_coverage` marker naming HEAD as `coveredCommitId`, or a CodeRabbit review on HEAD with a body (empty-body reviews are thread replies). Reviewed wins over every other outcome.
- **Carried forward** (exit 0): HEAD's latest CodeRabbit status is `Prior review carried forward`; the existing threads stand for HEAD.
- **Rate limited, paused or skipped** (exit 3): HEAD's latest CodeRabbit status is `Review rate limited`, `Review paused`, or ends in `review skipped` (e.g. `Incremental review skipped`). The summary's rate-limit text is not used: it stays from an earlier HEAD until CodeRabbit reaches the new one.
- Anything else: keep polling until the cap.

Only Step 5, the fix plan, waits for the command to exit, so the plan covers every source. When it exits, run Step 1 for every source once more and triage whatever no event named: edited CodeRabbit comments, and older threads that need a reply.

**CodeRabbit did not review this HEAD (rate limited, paused or skipped, script exit 3, or
the 10-minute settle cap).** If CodeRabbit has already posted at least one real
review on this PR (on any earlier HEAD), this is NOT a blocker. Treat CodeRabbit
as done for this HEAD, fetch and triage its existing threads, and carry on
without re-triggering. Only when there has never been a real review on the PR
does it block, and then you report it.

### 1. Fetch all unresolved feedback (in parallel)

- **Codex** — already returned from Step 0's parallel call. Parse the response into findings: one entry per flagged file:line, with severity from the model's own classification. If the response was "No findings." treat the channel as empty.
- **CodeRabbit** (on the PR) — run `la-fetch-coderabbit-threads <PR>` (see the `la:fetch-coderabbit-threads` skill). Read the JSON file it writes (`JSON: <path>` last line of stdout) — that's the structured input for the rest of this skill. **Read the comment BODIES from the rendered Markdown the script prints to stdout** (capture full stdout, not `tail`), and use the JSON only for the structured fields you need to act (per-thread `path` / `line` / `id` / `isResolved`, and the per-comment `url` for replies). In the JSON, `threads[]` carries `{id, isResolved, isOutdated, path, line, originalLine, comments}` where **`comments` is a GraphQL connection OBJECT, not a flat list** — the bodies live at `threads[].comments.nodes[].body` (each node also has `author.login`, `url`, `createdAt`). Iterating `comments` directly walks the object's keys (`pageInfo`, `nodes`), not the comments — a common parsing mistake. The review-summary `nitpicks[]` and `outside_diff[]` arrays instead carry a pre-rendered `block` string.
- **SonarQube (on the PR) — check EVERY gate criterion AND the new-issues count, not just the gate verdict.** The Sonar quality gate can fail on issues, duplications, coverage, security hotspots, or other metrics independently. Crucially, **the gate's `conditions` list does NOT include a "new issues count" condition by default** — a gate can return `status: OK` while still introducing OPEN issues attributed to this PR. The Sonar GitHub bot comment shows the headline `N New issues` right under "Quality Gate passed/failed"; that count is the authoritative signal for PR-attributed issues, and it must reconcile with the issue search below. Fetch all of the following so the plan is not missing the actual cause of a red gate OR a silently-introduced new issue. **Mandatory calls** (all MCP, never the CLI / `sonarqube:sonar-*` skills / `gh api`):
  - `mcp__sonarqube__get_project_quality_gate_status(projectKey=..., pullRequest="<PR>")` — the headline pass/fail and the individual gate conditions (which metric tripped, threshold vs actual). Treat any non-OK condition as something to address even if no Sonar issue is filed against it. Remember: gate `OK` does NOT mean "no new issues" — verify against the issue search.
  - `mcp__sonarqube__search_sonar_issues_in_projects(projects=["<key>"], pullRequestId="<PR>", issueStatuses=["OPEN","CONFIRMED"])` — bugs, vulnerabilities, code smells. **The API can return CLOSED/FIXED issues alongside the requested statuses** (the `issueStatuses` filter is not strictly enforced when `pullRequestId` is set — Sonar returns the historical issue set for the PR including ones already closed by prior commits or by the retarget). After fetching, **filter client-side to `status in ("OPEN", "CONFIRMED")`** before triage. The remaining count MUST match the "N New issues" headline from the bot comment — if it doesn't, re-query or investigate before declaring done. **Never dismiss an OPEN issue under `pullRequestId=...` as "pre-existing" just because it appears alongside CLOSED entries from prior commits or parent branches** — under PR scope, OPEN means the issue is attributed to this PR's current HEAD.
  - `mcp__sonarqube__search_security_hotspots(projectKey=..., pullRequest="<PR>", status=["TO_REVIEW"])` — hotspots are NOT issues; they have a separate review workflow and are easy to miss.
  - For each duplication-related gate condition (`new_duplicated_lines_density` etc.) or whenever the quality gate cites duplication: `mcp__sonarqube__search_duplicated_files(projectKey=..., pullRequest="<PR>")` and then `mcp__sonarqube__get_duplications(componentKey=..., pullRequest="<PR>")` on the specific file(s). Duplications never surface as Sonar issues — they show up only via these tools and the gate.
  - For each coverage-related gate condition (`new_coverage`, `new_lines_to_cover` etc.): `mcp__sonarqube__search_files_by_coverage(projectKey=..., pullRequest="<PR>", ...)` to find under-covered files, then `mcp__sonarqube__get_file_coverage_details(componentKey=..., pullRequest="<PR>")` for the specific uncovered lines.
  - Optional but useful when the gate cites a metric you don't recognise: `mcp__sonarqube__get_component_measures(component=..., metricKeys=[...], pullRequest="<PR>")` and `mcp__sonarqube__search_metrics(...)` to look up what the metric means.

  If `mcp__sonarqube__*` tools are not registered in this session, stop and ask the user to load the MCP — do not fall back to the CLI or `gh api`.
- **Failed CI** — run `la-fetch-failed-pr-checks <PR>` (see the `la:fetch-failed-pr-checks` skill). Read its JSON for the failed checks plus their log excerpts (or why each has none).
- **Conventions gate (deterministic)** — run `la-check-conventions <PR>` from the repo root; see "Conventions gate" below.

Run the three GitHub-side fetches and the conventions gate in parallel — they're independent. Codex is already done (Step 0). Inside SonarQube, the gate-status call comes first so you know which secondary tools (duplications / coverage / hotspots) are actually load-bearing; everything else can run in parallel.

#### Conventions gate

`la-check-conventions <PR>` (or `--base <branch>` before a PR exists) checks the WHOLE of every `.py` and TS/JS file the change touches (committed ∪ working tree), on purpose, to force each touched file fully compliant. It enforces the rules listed in `conventions.rules` (default: all):

- `[import-not-top]`: no imports inside functions/classes, none after module-level code; type-only and optional-dependency import wrappers are fine (the language docs name them). Fix by hoisting the import. Only a genuine circular or optional import may instead get a reasoned waiver on the flagged line (`la-config get lang.<language>.waiver`, rule `import-not-top`), and CONFIRM WITH THE USER before landing one.
- `[text-ratio]`: comment/docstring-only lines at most `conventions.text_ratio_max` (default 15%) of the total, aggregated separately over test and source files. Fix by trimming comments/docstrings in the flagged group (follow the `la:concise-comments` skill); there is no per-line waiver. NEVER trim outward-facing docstrings (MCP tool servers, CLI `--help`, OpenAPI routes — list such files under `exempt`); trim the other touched files instead, unless the user names such a file.
- `[composite-assert]` and `[raises-single-throw]` (test files): split the assert; move all but the call under test out of the raises block. These are mechanical and assertion-preserving, so they need no separate OK.

Files matching `exempt` are skipped. Exit 0 = clear, 1 = RED (one `file:line: [rule] message` per finding; a `[text-ratio]` block per breached group, worst file first), 2 = usage, config or git error. It is a HARD GATE: the change is not done while it is RED. Fix every flagged line; never dodge it (moving code to another file, splitting tests out, …) and never offer a dodge as an option.

### 2. Merge into one normalised list

Build a single in-memory list. Each entry:

- `source`: `"coderabbit"` | `"sonar"` | `"codex"` | `"ci"` | `"conventions"`
- `sonar_kind` (when `source == "sonar"`): `"issue"` | `"hotspot"` | `"duplication"` | `"coverage"` | `"gate_condition"` — distinguishes the gate-criterion subtypes since each has its own invalid-handling channel (NOSONAR only applies to issues; hotspots have a review workflow; duplications/coverage/gate-conditions need code changes or `--force-clean`-style suppressions specific to the metric).
- `file`: path relative to repo root, or `null` for CI failures (the failure may not map to a single file) and for project-level gate conditions
- `line`: integer or `null` (or a `[start, end]` range for duplication blocks; codex findings should carry a line range when they cite one, single line otherwise)
- `severity`: `critical` | `major` | `minor` | `info` (best-effort mapping; CodeRabbit emoji → severity: 🔴/⚠️ Potential issue → major, 🟡/💡 → minor, 💤 → info; CI failures default to `major`; gate-condition entries inherit from the failing condition's severity field; hotspots default to `major`; codex findings use the severity the model assigned)
- `rule`: Sonar rule key (issues / hotspots), the metric key (`new_duplicated_lines_density`, `new_coverage`, ...) for gate / duplication / coverage entries, the CodeRabbit thread/comment ID, the CI workflow/job name, or `"codex"` + a short tag for codex findings (codex doesn't issue rule keys)
- `summary`: one-line description (for CI: `<workflow> / <job>` failed at conclusion `<X>`; for gate conditions: `<metric>: <actual> vs <threshold>`; for codex: the model's one-sentence summary line)
- `body`: full text (CodeRabbit comment body, Sonar issue/hotspot message + rule description, duplication block range + duplicate locations, coverage's uncovered-line list, the check's log excerpt, or codex's one-paragraph rationale)
- `ref`: thread URL (CodeRabbit), Sonar issue/hotspot key, run/job URL (CI), or `null` for codex (no remote thread to link)

Don't dedupe across sources blindly — if multiple sources flag the same area, keep them all. They need separate invalid-handling channels. **Don't drop a failing quality-gate condition just because no individual issue is filed** — duplication and coverage conditions routinely fail the gate without producing any `search_sonar_issues_in_projects` rows.

**Codex overlap with CodeRabbit / Sonar is expected and fine.** Codex and CodeRabbit both flag broad correctness/security/regression issues; sometimes they catch the same thing, sometimes one catches what the other misses. Treat overlapping findings as independent entries — the plan can collapse them into a single fix at Step 5 when the proposed change is identical, but keep both rows during triage so each source's invalid-handling channel stays intact.

### 3. Validate each issue

For each entry, classify as VALID or INVALID using a source-appropriate signal:

- **CodeRabbit / Sonar / Codex** — READ the cited file at the cited line(s). Apply the repo's and the user's standing rules (their CLAUDE.md files: e.g. trust internal code, validate only at boundaries; imports at the top). Lean toward VALID when uncertain — false positives are easier to defend later than missed bugs now. Over-verbose comments/docstrings in the diff (design essays, ticket-ID-on-every-line, code-restating comments, name-echo docstrings) are a valid maintainability finding per the `la:concise-comments` skill — flag them even if no bot did.
- **CI failure** — READ the log excerpt in the JSON. Classify as INVALID only when the failure is clearly unrelated to this PR's changes (network blip / runner died / well-known flaky test that the user has previously confirmed is flaky / out-of-date Action that times out before doing anything). Otherwise VALID. **A test failure that points at code this PR touched is always VALID** — don't argue your way out of it.
- **A finding that proposes an option the plan's decisions log rejected** (when the branch has a plan): VALID only if it raises something the logged reason does not answer, and then it is a plan edit to put to me under the `/la:pr` frozen-plan rule. Otherwise INVALID, and the rationale cites the decision. The rule covers that proposal only: any other claim in the same finding is its own entry, validated on its own.
- **Conventions** — always VALID (the check is deterministic; there is nothing to second-guess); fix per "Conventions gate" below. Severity `minor`, `rule` = the bracketed rule name, `ref` = `null`.

Codex-specific validation hazards (apply on top of the shared CodeRabbit/Sonar rules):

- Codex sometimes flags issues that are TRUE in isolation but resolved by other lines in the diff it didn't read. Always verify by reading a wider slice of the cited file, not just the cited line, before classifying.
- Codex doesn't see CI output, so it can re-raise the same concern as a CI failure. If both fire on the same area, mark them as overlapping in the plan rather than deduping — Step 5's group strategy collapses them.

For each entry, write a one-line classification rationale (`why-valid` or `why-invalid`) — used in steps 4 and 5.

### 4. Handle INVALID issues in place

#### CodeRabbit (every unresolved thread)

At every sweep, list ALL CodeRabbit threads on the PR, including outdated ones and ones from reviews several commits back. Any thread CodeRabbit has still not marked resolved once CI has completed on a commit pushed AFTER the thread was opened MUST get a reply in that sweep: which later commit(s) fixed it (SHA plus a one-line how and the test that pins it), or why no fix was or will be made. Start every such reply with `@coderabbitai` so CodeRabbit re-evaluates the thread. A thread you already replied to that CodeRabbit left unresolved after a later CI run needs a new reply that answers its latest comment. Never skip a thread because it is outdated, old, or was "already addressed" in a commit message; the reply on the thread is the only record that counts, and a fixed-but-unreplied thread reads as unaddressed. Review-summary nitpicks are exempt: never reply to them.

#### CodeRabbit (invalid)

**Never** call the resolve mutation. Post a reply on the thread tagging `@coderabbitai` with the rationale, using `la-reply-invalid-coderabbit`. It auto-prepends `@coderabbitai ` if the body doesn't already start with that mention, and delegates URL parsing + the gh call to `la-reply-to-pr-thread`:

```bash
la-reply-invalid-coderabbit <discussion-url-from-la-fetch-coderabbit-threads-output> <<'EOF'
<one or two sentences explaining why this is invalid / where it was already addressed>
EOF
```

Reference the relevant `CLAUDE.md` rule or commit hash when possible — gives the bot and the human reviewer something concrete to evaluate against. Do NOT call `gh api .../replies` directly; the command is the only allowed channel. (You may still call `la-reply-to-pr-thread` directly for non-CodeRabbit threads — e.g. replying to a human reviewer — where the `@coderabbitai` prefix would be wrong.)

#### SonarQube (invalid)

NOSONAR is a code change, and this skill stops at the plan — so do **not**
apply NOSONAR comments in step 4. Instead, list each invalid Sonar issue in
the plan (step 5) with the proposed NOSONAR line ready to apply. The user
picks a group; only then does the suppression actually land.

When the user does pick a group containing invalid Sonar issues, use the
following format. Bare `// NOSONAR` is forbidden — always include rule and
reason. The rule key inside `NOSONAR(...)` MUST be alphanumeric only (e.g.
`S125`, `S7632`); never include the language prefix like `python:` /
`javascript:` — Sonar's own `python:S7632` rule rejects `# NOSONAR(python:S125)`
as malformed, and a malformed suppression silently suppresses nothing.

| Language family | Syntax |
|---|---|
| Python, Shell, Ruby, YAML | `# NOSONAR(<rule>) — <reason>` |
| C, C++, Java, JS, TS, Go, Rust, Scala | `// NOSONAR(<rule>) — <reason>` |
| HTML, XML, Vue templates | `<!-- NOSONAR(<rule>) — <reason> -->` |
| SQL | `-- NOSONAR(<rule>) — <reason>` |

Examples:
- ✅ `# NOSONAR(S125) — arithmetic explanation, not commented-out code`
- ❌ `# NOSONAR(python:S125) — ...` (colon in rule key — silently fails to parse)
- ❌ `# NOSONAR` (bare — no rule key, no reason)

Place the comment at the end of the offending line. For multi-line issues (e.g. cognitive complexity on a function), put the suppression on the line Sonar cites.

(CodeRabbit invalid replies stay in step 4 — they're comments, not code changes.)

#### SonarQube security hotspots

Hotspots are **not** issues — `NOSONAR` does **not** clear them. The gate
condition `new_security_hotspots_reviewed` requires every new hotspot to be
**reviewed** (100%), so a red gate on this metric is only cleared two ways:

1. **Rewrite the flagged code so no hotspot is raised.** Verify the rewrite
   actually removes it on the next analysis — a plausible-looking change can
   still trip the rule. In particular, `python:S5852` (ReDoS) flags a regex with
   **two or more unbounded quantifiers** that can backtrack; switching `.*` to a
   bounded class like `[^"]*` does **NOT** help if two such segments remain
   (`[^"]*X[^"]*Y` is still flagged). Reduce to a **single** quantified segment
   (`PREFIX[^"]*X`) and assert any tail with a plain substring check.
2. **Mark it REVIEWED via `mcp__sonarqube__change_security_hotspot_status`**
   (`status=["REVIEWED"]`, `resolution=["SAFE"|"FIXED"|"ACKNOWLEDGED"]`, with a
   justification `comment`) when the hotspot is a genuine false positive (e.g. a
   test-only regex over deterministic, non-attacker-controlled input). This is a
   Sonar-state mutation — list it in the plan and get the user's go-ahead before
   applying. **Order matters:** PR re-analysis assigns *new* hotspot keys each
   run, so mark REVIEWED only **after** the final code push has been analysed,
   then re-query `get_project_quality_gate_status` to confirm the metric flipped
   to OK. (Marking on an earlier analysis's keys does not carry over.)

Prefer (1) — it leaves no Sonar-state debt and shows the resolution in the diff.

Since the skill stops at the plan, do not rewrite or mark-reviewed in step 4 —
list each hotspot in the plan (step 5) with the chosen resolution.

#### Codex (invalid)

Codex has no remote thread or status check to update — it's a local-only review. For invalid codex findings, list them in the plan at Step 5 under an `INVALID — codex` sub-section with the rationale. No reply, no suppression comment, no NOSONAR. The whole audit trail lives in the plan output you give the user, which they can refer back to.

#### CI failure (invalid — flake / infrastructure)

Do **not** silently dismiss. Surface in the plan as an "INVALID — flake/infra" note with the rationale and the run/job URL. Suggest a rerun in the plan but do **not** run `gh run rerun` automatically — that mutates shared state and needs the user's go-ahead. (If the user later says "rerun it", `gh run rerun <run-id> --repo <repo>` is fine.)

### 5. Plan for the VALID issues

**Invoked from `la:pr-review`:** skip the plan. Return the valid list (and what you did with the invalid ones) to `la:pr-review`, which fixes it autonomously in its loop.

**Run standalone:** after step 4, present a written plan to the user covering ONLY the valid issues. Include:

- A header line: `Triaged: <V> valid / <I> invalid (<C> CodeRabbit + <S> Sonar + <X> Codex + <CI> CI)` — show every source even when its count is 0, so the user can see which channels ran.
- One section per valid issue (or per group if >3 — see below): file:line, source, severity, summary, the proposed fix in 1–3 lines. When two or more sources flag the same fix (e.g. Codex + CodeRabbit both raise the same correctness concern), list each row but mark them as `[merged: <other-source>]` so the user sees the corroboration; the actual code change is one edit.

If there are **more than 3** valid issues, split them into 2–4 LOGICAL GROUPS. Group by what makes them coherent to fix together — usually one of:

- **Same root cause** (one bug surfaces in multiple places)
- **Same module / file**
- **Same category** (e.g. all formatting, all imports, all unused-var)
- **Same severity tier** (all majors first)

Within each group, list the individual issues. End each group with a 1–2 line "fix strategy" describing the unified approach.

End the plan with a one-line proposal:

> Want me to implement group 1 first? (or: pick a group, or say "all" to do them in order)

Do **not** start writing code until the user picks.

Any further decision the plan needs (a design fork, an approval of a spec or
test edit), including one that surfaces mid-fix, is a question: stop, ask every
one of them, ONE per message, back to back, and write code only after the last
answer.

## Constraints

- NEVER call any "resolve" mutation on CodeRabbit threads (no `resolveReviewThread`, no UI-equivalent). Only `/replies`.
- NOSONAR suppressions MUST include the rule key and a reason. Bare `// NOSONAR` is forbidden. The rule key inside the parentheses must be alphanumeric only — never include the `python:` / `javascript:` / etc. language prefix (it makes Sonar treat the suppression as malformed).
- Run standalone, this skill stops at the plan; code fixes happen only after the user picks a group. Invoked from `la:pr-review`, it returns the triaged list instead.
- When you later write fixes, keep any comments/docstrings concise per the `la:concise-comments` skill — don't add design essays or code-restating comments while resolving findings.
- If validation makes you LESS than 80% confident an issue is invalid, classify it as VALID and put it in the plan. Better to over-fix than to silently dismiss a real bug.

## When NOT to use this skill

- User asks for just CodeRabbit threads → use `la:fetch-coderabbit-threads` directly.
- User asks for just Sonar issues → use `sonarqube:sonar-list-issues` directly.
- User asks for just a Codex review of the local diff → use the `la:codex-review` skill directly.
- User says "fix the CodeRabbit comments" without mentioning Sonar / Codex → use `la:fetch-coderabbit-threads` and skip the merge step.
- User wants you to start coding immediately → this skill is triage + plan only.
