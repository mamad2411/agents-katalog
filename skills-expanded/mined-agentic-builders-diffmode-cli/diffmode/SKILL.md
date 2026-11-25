---
name: diffmode
description: Use this skill whenever the user asks to generate, run, retrieve, or apply a growth plan, marketing strategy, persona research, or focus group simulation with the Diffmode CLI. Triggers on phrases like "growth plan", "diffmode run", "personas", "focus group", "growth strategy", and any instruction to operate the `diffmode` CLI. The skill orchestrates the `diffmode` CLI end-to-end against the hosted growth-pipeline API — authenticate, pre-flight credits, submit a run, watch the job, retrieve manifest-shaped results, and apply tactics. Use this any time the user mentions Diffmode or asks for a bootstrapped-SaaS growth plan, even if they don't explicitly name the CLI.
---

# Diffmode

You are operating the `diffmode` CLI on behalf of the user. It is a thin HTTP
client to a hosted growth-strategy API. A full plan run can take 10 minutes to
several hours and produces dozens of markdown files. **Never dump full outputs
into your context** — always work through the manifest emitted by
`diffmode results`.

## When to use this skill

- User says "use diffmode", "generate a growth plan", "run diffmode for
  <product>", "show the personas", or asks to apply a plan produced by
  Diffmode.
- User has installed the CLI (verify with `diffmode --version`) and
  authenticated (verify with `diffmode whoami --json`).

## When NOT to use this skill

- For generic marketing advice not tied to a Diffmode product.
- If the user wants to top up credits — Diffmode billing is **browser-only**.
  On exit 8, use the `billing_url` from the error payload (e.g.
  `https://diffmode.app/app/billing?channel=cli` — the CLI credit-packs view).
  There is no `diffmode billing topup` command.
- If `diffmode` is not installed — instruct the user to run
  `npx diffmode@latest login` once, then resume.

## Operating contract

- The CLI is **non-interactive** when stdout is not a TTY. Always pass
  `--json` and parse the schema-versioned envelope.
- **Stdout is data; stderr is progress/errors.** Both carry valid JSON when
  `--json` is set.
- **Exit codes** are part of the public contract:
  - `0` ok · `1` generic · `2` usage · `3` network · `4` auth ·
    `5` conflict (409) · `6` not-found · `7` rate-limited ·
    `8` insufficient-credits (402) · `9` server ·
    `10` interrupted-resumable · `130` SIGINT
  - Full recovery guidance: `references/error-codes.md`.
- **Idempotency is the agent's responsibility.** The CLI does NOT
  auto-generate an `Idempotency-Key` header. Generate a UUIDv4 yourself and
  pass `--idempotency-key <uuid>` on every submit (`run`, `unlock`,
  `workflow`, `idea-eval`, `smoke-test`). Same key + same user → same
  `job_id` (no double-charge). Matches `gh`/`stripe` UX.
- **Founder input is required** for `run`, `workflow`, and `smoke-test`. Use
  `--input founder.json` (canonical) or `--from-url <url>` (CLI calls
  `/public/v1/analyze-website` to pre-fill). Schema:
  `references/founder-input-schema.md`. `unlock` reuses the prior
  free-tier's stored input — do not re-supply.
- **Idea-eval** takes a structured JSON array, not strings — see
  `references/idea-input-schema.md`.

## Default workflow

1. **Authenticate (one-time per machine).**
   `diffmode whoami --json` → on exit 4, stop and tell the user
   `npx diffmode@latest login` (or `diffmode login --token dm_pat_…`) in
   their terminal, then resume.
2. **Pre-flight credits.**
   `diffmode limits --json` → read `credit_costs` for the exact per-action
   cost (CLI channel: `run`=0, `smoke-test`=1, `idea-eval`=1, `unlock`=2,
   `workflow`=2). If `credits_available` is below the cost of your intended
   action, echo the `billing_url` and stop. Don't hardcode costs — read them
   from the server `credit_costs` matrix. The CLI's submit also does this
   pre-flight by default; `--no-preflight` skips it.
3. **Submit a run (default = free-tier, 1 credit).**
   Generate a UUIDv4 and run
   `diffmode run <product> --input founder.json --idempotency-key <uuid> --json`.
   On exit 5 (CONFLICT), parse `error.job_id` from stderr and resume at
   step 4 with that id.
4. **Watch.**
   `diffmode jobs watch <job_id> --json --wait 4h`. This blocks; the CLI
   handles `next_poll_ms` backoff and prints progress to stderr.
   - exit 10 (RESUMABLE) → run `diffmode jobs resume <job_id>` once, then
     re-watch.
   - exit 7 (rate-limited) → respect `error.retry_after`; sleep then retry.
   - exit 9 twice in a row → stop, surface to the user.
   - Ctrl-C never cancels the server job — print "resume with
     `diffmode jobs watch <job_id>`" and exit 130.
5. **Retrieve results (manifest-first; never read the full bundle).**
   `diffmode results <product> --json` → read the manifest only. Then read
   `report.json` keyFinding sections via
   `diffmode results <product> --summary --json` (~3 k tokens).
6. **Drill down deliberately.**
   - Buyer personas (free-tier report sections are: `landscape`,
     `advantages`, `buyers`, `blockers`, `growthPlan`):
     `diffmode results <product> --stage buyers --summary --json`, then
     `--pull` once and `--show <relative-path>.md` for any persona file
     listed in the manifest.
   - A tactic: `diffmode results <product> --tactic <id-or-name>` (look up
     valid tactic ids/names via `--stage growthPlan --summary --json`).
   - Always page large files with `--max-tokens 4000` unless the user asks
     for the full file.
7. **Optional unlock (2 credits via CLI).**
   `diffmode unlock <product> --idempotency-key <uuid> --json`. Requires a
   completed `diffmode run` for the same product first — on 422, prompt the
   user to run free-tier first.
8. **Apply the plan.** Present the executive summary and proposed actions.
   **Stop and confirm** before making any code/copy/config changes. Treat
   each tactic as its own edit-review-commit loop.

## Human-checkpoint policy

- Submit a run only after confirming product name AND that the user
  understands it costs credits.
- Apply changes to files only after presenting a diff and getting explicit
  user approval.
- Never re-run the pipeline against the same product within 30 minutes
  without asking.

## Failure recovery (cheat sheet)

| Exit | Meaning | Action |
| --- | --- | --- |
| 4 | Auth | Ask the user to `diffmode login`. |
| 5 | Conflict (in-flight job) | Parse `error.job_id`; jump to step 4 (watch). |
| 7 | Rate limited | Sleep `error.retry_after` (or surface if > 5 min). |
| 8 | Insufficient credits | Print `billing_url` from the error payload (e.g. `https://diffmode.app/app/billing?channel=cli`); stop. There is no `diffmode billing topup` command. |
| 10 | Interrupted (resumable) | `diffmode jobs resume <id>` once, re-watch. |
| 130 | SIGINT | Confirm whether to re-watch — do NOT auto-cancel. |

See `references/error-codes.md` for every code + per-command coverage.

## See also

- `references/commands.md` — full command catalog with endpoints, credit
  costs, flags, and example invocations.
- `references/error-codes.md` — exit codes + per-code recovery script.
- `references/founder-input-schema.md` — `FounderDiagnostics` shape for
  `--input`.
- `references/idea-input-schema.md` — `IdeaInput` array shape for
  `--ideas-file`.
- `https://github.com/agentic-builders/diffmode-cli` — repo + issue tracker.
- `https://diffmode.app` — top-up + dashboard (browser-only billing; CLI credit-packs view at `https://diffmode.app/app/billing?channel=cli`).
