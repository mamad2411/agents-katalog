---
name: orchestrate-review
description: Orchestrate a multi-perspective post-implementation review loop using a raw reviewer running the project /review skill and a CodeRabbit MCP reviewer in parallel. Implementer synthesizes findings into per-iteration commits. Use after /orchestrate-implement-plan finishes and before opening a PR. Use when the user says "orchestrate review", "agent review loop", or wants worker-assisted multi-perspective review.
---

# Orchestrate Review

Coordinate a thorough quality gate over recent local commits using two
complementary reviewers running in parallel as fresh worker runs:

- A **raw reviewer** that runs the project's `/review` (or `/review-pr`)
  skill against the diff, using the validated `code-review` profile.
- A **CodeRabbit reviewer** that invokes the `coderabbit` MCP server's
  `execute` tool with the `review ...` command, using the validated
  `coderabbit-reviewer` profile.

Each reviewer reports independently. The supervisor does NOT pre-merge
findings — the implementer is responsible for synthesizing the two reports
into one coherent fix that satisfies both perspectives. Each fix iteration
produces a new local commit. Nothing is pushed and no GitHub interaction
happens in this skill — that is the user's call after the review loop ends.

Read your repository's agent-orchestrator setup docs (MCP server config,
profiles manifest, package diagnostics) before starting. Read
`.coderabbit.yaml` (when present) for the project's CodeRabbit
configuration and `.mcp.json` for the canonical CodeRabbit MCP wiring.

## Profile Selection

- **Raw reviewer**: validated `code-review` profile.
- **CodeRabbit reviewer**: validated `coderabbit-reviewer` profile.
- **Implementer**: validated `implementation` profile.
- Provider/model/effort/service-tier settings are owned by the user via
  the profiles manifest, not hard-coded here.
- If any required profile is missing or invalid, stop and ask the user to
  configure it. For repairs use `list_worker_profiles` and
  `upsert_worker_profile` rather than dispatching a worker to edit config.

## Scope Detection

Identify the review target before launching:

- **Default**: the unpushed local commits (`origin/<branch>..HEAD`).
- **Broader scope** (specify when context calls for it): a single named
  commit, an explicit commit range, the full branch (`main..HEAD`), or
  uncommitted working tree.
- Confirm scope with the user out loud when ambiguous.

The chosen scope determines:

- Which `/review*` skill the raw reviewer runs:
  - `/review` for narrow scope (one commit, working tree).
  - `/review-pr` for branch-wide scope.
- Which CodeRabbit invocation matches the scope:
  - Unpushed-only: `--type committed --base <upstream-ref>` (compute via
    `git rev-parse --abbrev-ref --symbolic-full-name @{upstream}`).
    Avoid `--unpushed` — it's only supported by the local CLI wrapper,
    not the raw CodeRabbit CLI used by the MCP launcher.
  - Full branch vs base: `--type committed --base <merge-target>`
    (e.g., `origin/main`).
  - Working tree only: `--type uncommitted`.

## Reviewer Prompt Anti-Patterns

Reviewer workers are capable agents with access to the repository's review
skills and rules. The supervisor's reviewer prompt should be a slim handoff:
scope, diff command, upstream worker output when useful, and the relevant
repository workflow or external tool to use.

Avoid these reviewer-prompt failure modes:

- **Plan-compliance-only framing:** do not ask only whether the latest commit
  satisfies the implementer's report. Ask for an independent review with prior
  findings as context.
- **Dimension lists:** do not recreate the review rubric in the prompt. Point to
  `/review`, `/review-pr`, CodeRabbit, or the relevant repository skill instead.
- **Hint laundering:** do not summarize implementer claims as facts. Pass the
  implementer output verbatim when it matters.
- **Positive framing:** do not state intended fixes as something to confirm. Let
  reviewers derive remaining issues from the diff, prior findings, and
  repository rules.

If the supervisor notices a genuinely task-specific concern that is not already
in the diff, prior findings, upstream worker output, or repository rules, surface
it to the human as an **Open Human Decision**. Do not smuggle it into the
reviewer prompt as a checklist item.

## Workflow

1. **Preflight.** Confirm cwd, current branch, that the chosen scope has
   commits to review (or working-tree changes if scope is uncommitted),
   and that all required profiles validate. Treat unrelated dirty files
   as user-owned. Stop and ask if anything looks risky.

2. **Round 1 — parallel reviewers.** Launch BOTH as fresh worker runs:

   - **Raw reviewer** (`code-review` profile): runs `/review` (narrow) or
     `/review-pr` (branch-wide) against the chosen diff. Asks for
     structured findings with severity classification.
     The raw reviewer MUST run in read-only mode for orchestrate-review:
     report findings via the worker's final output text only. Do NOT write a
     review artifact file to disk, even if the project's `/review` skill
     normally does so. Findings are aggregated by the supervisor and passed
     to the implementer in step 4 — the artifact would be redundant and
     risks polluting the diff.
   - **CodeRabbit reviewer** (`coderabbit-reviewer` profile): invokes the
     `coderabbit` MCP server's `execute` tool with the post-prefix
     `review ...` command. Do not include a leading `coderabbit`; the
     project's CLI-MCP wrapper prepends it.
     Use:
     - The right `--type` for scope:
       - `committed --base <upstream>` for unpushed-only — derive the upstream
         ref via `git rev-parse --abbrev-ref --symbolic-full-name @{upstream}`
         (e.g., `origin/<branch>`). Do NOT use `--unpushed`: that flag is only
         supported by some local wrapper scripts, not the raw CodeRabbit CLI
         exposed through the MCP launcher.
       - `committed --base <merge-target>` for full branch (e.g.,
         `--base origin/main`).
       - `uncommitted` for working-tree-only scope.
     - `--agent` for structured JSON output.
     - `--config AGENTS.md --config <project rule files> --config
       .coderabbit.yaml` — the project's standard config set per
       `.mcp.json`.
     - Generous idle timeout (≥ 2700 seconds; CodeRabbit reviews take
       7–30+ minutes upstream).
     The reviewer reports CodeRabbit's findings verbatim — no editing
     or pre-filtering.

3. **Both reports arrive.** Do NOT merge them. Pass both verbatim to the
   implementer in step 4.

4. **Implementer fix pass (fresh `implementation` run).** Hand the
   implementer:
   - Both review reports as separate inputs.
   - The current diff under review.
   - Repo instructions, ordering rules, and scope.
   - Authority to: fix findings, decline incorrect or out-of-scope
     findings with rationale, escalate genuine product/scope/contract
     questions as Open Human Decisions.

   The implementer:
   - Synthesizes the two reports (deduping overlap, identifying false
     positives, choosing behavior-preserving fixes).
   - Applies fixes.
   - Runs relevant verification.
   - **Commits the iteration as a new local commit** with a message
     describing the fixes and which review sources they address.
   - Reports: commit SHA, files changed, findings addressed/declined per
     reviewer, residual risks.

5. **Round N+1 — re-review.** For each new fix commit:
   - Send the implementer's report (per-finding fixed/declined + new
     commit SHA + new diff) verbatim to the existing raw reviewer session via
     `send_followup`. Ask for an independent re-review of the new commit with
     prior findings as context, not confirmation of the implementer's claims.
   - Re-invoke the CodeRabbit MCP on the new commit as a FRESH worker
     run — CodeRabbit doesn't carry session state; each invocation is
     independent.

6. **Continue until aligned.**
   - Both reviewers report no blocking findings on the latest commit.
   - Open Human Decisions = none (or all explicitly answered/deferred).

7. **Impasse handling.** If the same finding survives 2 fix attempts,
   escalate to the dissenting reviewer with a "make-a-final-call"
   prompt:
   - Summarize what was tried and why the reviewer was not satisfied.
   - Ask the reviewer to choose ONE of: (a) fix this exact way (provide
     specific code or pseudocode), (b) accept as decline with rationale,
     or (c) escalate to human.
   - The reviewer's answer is final for that finding. If they choose
     (c), bundle as Open Human Decision and surface to the user.
   - Hard ceiling: 5 rounds of fix-then-rereview per finding. After
     round 5, force the impasse-resolution prompt regardless.

8. **No pushing, no PR opening, no GitHub interaction.** This skill stops
   at "stack of fix commits, both reviewers READY." Pushing belongs to
   the user (or `git push`); opening a PR belongs to `/create-pr`;
   resolving PR comments belongs to `/orchestrate-resolve-pr-comments`.

9. **Final handoff.** Tell the user:
   - Stack of commits produced (oldest fix → newest), with SHA list.
   - Findings summary per reviewer (concise table:
     addressed / declined / deferred).
   - Final verdicts (both READY).
   - Residual risks / non-blocking suggestions.
   - Working tree state.
   - Whether squash before push is recommended (default: not required).
   - **Declined non-blocking findings (carry-forward).** A separate
     subsection listing every reviewer suggestion the implementer declined
     with the rationale "would balloon scope" / "out of scope" rather than
     as a false positive. Each entry: source reviewer, severity, file
     reference, one-line description, and the implementer's recorded
     rationale. This list is the cue for downstream PR-comment workflows
     (or the human directly) to file a tech-debt tracking issue once the
     PR exists — `/orchestrate-review` itself does not create GitHub
     issues because it runs pre-PR. If there are no such declines, write
     "Declined non-blocking findings: none."

## Critical Rules

- Two reviewers run as fresh, independent runs. The supervisor does not
  pre-merge their findings. The implementer is the synthesizer.
- Each fix iteration is a separate local commit. No squashing during the
  loop. Squash optional at the end.
- No pushing, no PR opening, no GitHub thread interaction in this skill.
- CodeRabbit reviews are slow (7–30+ minutes upstream). Use long idle
  timeouts and do not cancel based on elapsed wall-clock time alone.
- The CodeRabbit MCP invocation must NOT use `--unpushed`. That flag is
  only supported by the local wrapper `scripts/coderabbit-cli.mjs`. The
  raw CodeRabbit CLI exposed via the MCP launcher errors with
  `unknown option '--unpushed'`. Use `--base <upstream-ref>` instead.
- Verify CodeRabbit auth at start: if there is any doubt, run
  `auth status --agent` through the MCP `execute` tool first and fail fast if not
  authenticated rather than silently dropping the review.
- A clean CodeRabbit run on a substantive diff is informational, not an
  automatic green light. The local MCP-driven setup may behave differently
  from PR-side CodeRabbit. If `0 findings` returns on a non-trivial commit,
  consider that a signal to spot-check local CodeRabbit health (run
  `auth status --agent` through the MCP `execute` tool and re-run on a
  known-buggy diff) rather
  than treating the result as definitive. The raw reviewer is the primary
  bug-finding signal until local CodeRabbit is confirmed equivalent to the
  PR-side experience.
- The implementer holds authority to synthesize findings, including
  declining incorrect or out-of-scope reviewer feedback with rationale
  recorded in the commit message. Out-of-scope declines must ALSO
  appear in the final handoff's "Declined non-blocking findings"
  subsection so a downstream workflow (or the human) can convert them
  to a tracked GitHub tech-debt issue once the PR exists. False-positive
  declines do not need to be carried forward.

## Human Escalation

Escalate to the user only for:

- Genuine product/scope/behavior changes a reviewer's finding would force.
- A reviewer-explicit-requested escalation in the impasse round.
- Material disagreement the implementer cannot resolve via a
  behavior-preserving fix or a principled decline.
- Verification failures the implementer cannot fix without authorized
  scope expansion.

Do NOT escalate routine reviewer findings, false positives the implementer
declines with rationale, or ordinary fix-versus-decline judgment calls.

## Follow-Up Prompts

See `references/follow-up-prompts.md` for the standard prompt templates
(round-1 raw reviewer, round-1 CodeRabbit, round-N implementer,
re-review raw reviewer, re-review CodeRabbit, impasse final-call).
