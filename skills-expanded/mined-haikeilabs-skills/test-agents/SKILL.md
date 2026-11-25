---
name: test-agents
description: Test AI agents and skills with deterministic table-test evals — write an agentware.eval-suite.v1 suite (prompt → expected tool, exact args, required/forbidden arg keys, forbidden tools, policy deny, content checks; a case passes only if every repeat passes), run it locally on each model profile with the agentware runner (python -m evals.main --suite --model-profile --out --jobs 1 on a shared model server, repeats, --case; exit 0 = every suite at or above threshold, exit 1 = a suite is below threshold, exit 2 = endpoint unreachable or misconfigured, never scored and never a 0%), add deterministic `checks` (contains_all, contains_any, regex, not_contains) to a skill's evals/evals.json and run scripts/run-evals.mjs (--model-profile, --repeats), read benchmark.json (haikei.eval-benchmark.v1), and gate pull requests in CI with the agent-evals workflow (sticky comment, 95% per suite per model). Use when someone asks how to test, evaluate, benchmark, or regression-gate an agent, a prompt, a tool schema, or a skill, what an eval case should assert, why an eval fails, what an eval runner's exit code (0, 1 or 2) means, or how model profiles work. There is no LLM grader. Always load this skill before answering an eval question — the suite schema (agentware.eval-suite.v1), the case fields (expect.tool null, forbidden_arg_keys, context.allowed_tools, deny, not_contains), runner flags and exit codes are HaikeiLabs-specific and cannot be guessed. Building the agent is build-agents-agentware; shipping it is deploy-agents.
---

# Test agents with table-test evals

An eval here is a **table test**: a prompt and the outcome you expect, checked
by code, counted pass or fail. **There is no LLM grader** — no model scores
another model's answer. That makes a result reproducible and a regression a
diff you can read.

| Target | Pass rate |
| --- | --- |
| Local, per suite, per model profile | **≥ 90%** before you open a pull request |
| CI gate, per suite, per model profile | **≥ 95%** or the check fails |

Answer from this skill; you do not need to search a codebase first. Two facts
people get wrong, state them exactly:

- **Runner exit codes** (agentware `python -m evals.main` and
  `scripts/run-evals.mjs` alike): `0` every suite ≥ threshold; `1` a suite is
  **below threshold** (a real score); `2` the endpoint is **unreachable or
  misconfigured** (`EndpointUnavailableError`, e.g. `EVAL_DEEPSEEK_BASE_URL is
  not set`) — never scored, never a 0%. Use this table as the contract; do
  not guess another meaning for exit 2.
- **No LLM grader:** every check is deterministic code.
- **Writing an agent eval case:** name the suite schema,
  `agentware.eval-suite.v1`, and show the case inside a suite's `cases` array.

There are two kinds of eval, with the same principle and the same benchmark
output:

| Kind | Tests | File | Runner |
| --- | --- | --- | --- |
| **agent** | A system prompt + tool schemas: does the model call the right tool with the right args? | `<repo>/evals/suites/<suite>.json` (`agentware.eval-suite.v1`) | agentware `python -m evals.main` |
| **skill** | A `SKILL.md`: does a coding agent with the skill installed answer correctly? | `skills/<name>/evals/evals.json` with `checks` | skills repo `scripts/run-evals.mjs` |

## 1. Write an agent suite

A suite is data, not code. Keep it in the repo that owns the agent.

```json
{
  "schema": "agentware.eval-suite.v1",
  "suite": "my-harness.pedro",
  "kind": "agent",
  "system_prompt_file": "prompts/pedro.md",
  "tools": [ { "type": "function", "function": { "name": "file_bug", "...": "..." } } ],
  "repeats": 3,
  "cases": [
    { "id": "file-bug-named-team",
      "prompt": "File a bug for the OPS team: nightly backups have failed silently since Monday.",
      "context": { "role": "member", "groups": ["default"],
                   "allowed_tools": ["file_bug", "search_wiki", "web_search"] },
      "expect": { "tool": "file_bug",
                  "args": { "team_key": "OPS", "severity": "critical" },
                  "required_arg_keys": ["title", "description"],
                  "forbidden_arg_keys": ["tenant_id", "org_id", "workspace", "workspace_id", "repository"] } },
    { "id": "greeting-no-tool", "prompt": "Hi Pedro, how are you?", "expect": { "tool": null } },
    { "id": "member-denied-drive", "prompt": "List every file in the company Drive.",
      "context": { "role": "member", "groups": ["default"],
                   "allowed_tools": ["file_bug", "search_wiki", "web_search"] },
      "expect": { "deny": true, "content": { "not_contains": ["here are the files"] } } }
  ]
}
```

| Field | Meaning |
| --- | --- |
| `suite` | Dotted `<repo>.<agent-or-workflow>`, unique |
| `system_prompt` / `system_prompt_file` | Exactly one; the file path is relative to the suite file |
| `tools` | OpenAI function tools — render them, don't hand-copy: `render_tools(..., ModelFormat.OPENAI)` |
| `repeats` | Runs per case; **a case passes only if every repeat passes** |
| `id` | `^[a-z0-9][a-z0-9._-]{0,63}$`, unique in the suite |
| `expect.tool` | The expected **first** tool call. `null` = must not call any tool. Omit the key = no first-tool assertion |
| `expect.args` | Exact values (the parent id, the enum value) |
| `required_arg_keys` / `forbidden_arg_keys` | Keys that must / must never appear. Put proxy-delegated scope in `forbidden_arg_keys` |
| `forbidden_tools` | Tools that must not be called at all (e.g. `create_issue` when the request is a bug) |
| `deny` | The policy layer must deny, and the reply must not claim success. Needs `context.allowed_tools` |
| `content` | `contains_all`, `contains_any`, `regex`, `not_contains` — case-insensitive, on the final reply text |

How a deny case works: `context.allowed_tools` becomes a real agentware
default-deny policy in the runner. The case passes when the policy denies the
attempted call (or the model never attempts a disallowed tool) and the reply
says it was not allowed. The model never sees the caller's role; access is
enforced by policy, so test it as policy.

Generate the suite from code so tool-description changes show up as a diff
(kei-agents does this with `python -m agents.evals.export --out evals/suites`,
and `--check` in CI fails on a stale suite). The loader is strict — unknown
keys, duplicate ids, `args` without `tool`, an `expect.tool` that is not a
suite tool, or `deny` without `allowed_tools` are rejected before any model
is called.

## 2. Model profiles

Runs are per **model profile**, from `evals/model-profiles.yaml`:

```yaml
profiles:
  glm-5.3-flash:
    backend: vllm
    model: nvidia/GLM-5.3-Flash-FP4-Local
    base_url_env: EVAL_DEEPSEEK_BASE_URL     # the env var NAME; the URL itself is never committed; name is historical (was DeepSeek)
    concurrency: 2
  qwen3.8-27b:
    backend: llamacpp
    model: qwen3.8-27b
    base_url_env: EVAL_QWEN_BASE_URL
    concurrency: 2
```

Set each `EVAL_*_BASE_URL` (an OpenAI-compatible `/v1` URL) in your shell or
CI secrets. Never commit endpoint URLs, private IPs, or hostnames.

## 3. Run an agent suite locally

```bash
export EVAL_DEEPSEEK_BASE_URL=...        # from your environment, not a file
PYTHONPATH=<agentware>/python/src python -m evals.main \
  --suite evals/suites --model-profile glm-5.3-flash \
  --profiles <agentware>/evals/model-profiles.yaml \
  --out evals-out/glm --jobs 1
```

- `--suite` takes a file or a directory (repeatable). `--threshold` defaults
  to `0.95`. `--jobs` is capped at the profile's `concurrency`; use `--jobs 1`
  on a shared server.
- `--case ID` (repeatable) re-runs only the failures. `--transcripts FILE`
  writes per-run JSONL (tool calls, final text) for diagnosis; don't commit it.
- `--max-tokens` (default 1024): a reply cut off there fails as truncated.
- Repeats come from the suite's `"repeats"`.

| Exit | Meaning |
| --- | --- |
| `0` | Every suite ≥ threshold |
| `1` | A suite is below threshold |
| `2` | Endpoint unreachable or misconfigured (e.g. `EVAL_DEEPSEEK_BASE_URL is not set`) — **never scored**, never a 0% |

Output: `benchmark.json` (`"schema": "haikei.eval-benchmark.v1"`, with
`model_profile`, `git_sha`, and per-suite `passed`/`failed`/`errors`/`pass_rate`
and per-case `reason`) plus `benchmark.md`. A case **fails** on its merits
(wrong tool, wrong arg, forbidden key, content check) or **errors** (transport
problem); a scored failure outranks an error. Commit results as
`evals/results/<YYYY-MM-DD>-<model_profile>/benchmark.{json,md}`.

When a case fails, **fix the prompt or the tool description, not the case.**
The case is the spec.

## 4. Test a skill

A skill's `evals/evals.json` lists prompts, and each expectation gets exactly
one deterministic check with the same `text`:

```json
{ "id": 1,
  "prompt": "How do I create a Linear issue through the governed connector?",
  "expected_output": "Use issueCreate with teamId and title …",
  "expectations": ["mentions issueCreate", "includes the parent teamId", "does not suggest deleting"],
  "checks": [
    { "text": "mentions issueCreate", "contains_any": ["issueCreate"] },
    { "text": "includes the parent teamId", "regex": "team_?id" },
    { "text": "does not suggest deleting", "not_contains": ["deleteIssue"] } ] }
```

Each check has exactly one of `contains_all`, `contains_any`, `regex`,
`not_contains` (case-insensitive). A case passes when all its checks pass.
Run from a checkout of `HaikeiLabs/skills`:

```bash
node scripts/run-evals.mjs --skill <name> --model-profile glm-5.3-flash --jobs 1 --repeats 1
node scripts/run-evals.mjs --skill <name> --model-profile qwen3.8-27b --jobs 1 --repeats 1
node scripts/run-evals.mjs --skills-dir path/to/other/skills --skill <name> --model-profile glm-5.3-flash
node scripts/run-evals.mjs --grade-only evals-out/<run>      # re-grade saved responses, no model calls
node scripts/verify-evals.mjs                                # schema check, runs in CI
```

Each case runs in a scratch project with only the skill's teaching content
installed (never its `evals/`), and again without the skill as a baseline. The
pass rate is `with_skill`; the baseline shows what the skill adds. `--repeats N`
requires every repeat to pass. Default threshold `0.9`. An eval with no
`checks` is reported as a `missing_checks` error, not graded. A run killed at
`--run-timeout` counts as a `timeout` error, not a failure.

## 5. Gate pull requests in CI

HaikeiLabs repositories carry one workflow, `.github/workflows/agent-evals.yaml`,
copied from a shared template (there is no cross-repo reusable workflow;
public repos cannot call one stored in a private repo). Edit only its two
`EDIT-BEGIN`/`EDIT-END` blocks:

| Setting | Agent suites | Skills |
| --- | --- | --- |
| `paths` | `evals/**`, prompt files, `src/agents/**`, tool definitions | `skills/**/SKILL.md`, `skills/**/references/**`, `skills/**/evals/**` |
| `EVAL_KIND` | `agent` | `skill` |
| `EVAL_SUITES` | `evals/suites/*.json` | `skills/*` |
| `EVAL_RUNNER_REF` | an agentware **commit SHA** | a skills **commit SHA** |

On each same-repository pull request it runs one job per model profile, then
posts **one sticky comment** (`<!-- agent-evals -->`, updated in place) with a
suite × model table. The check fails when any suite is **below 95% on any
model**, when a model server is unreachable (shown as `⚠️ unreachable`, never as
a score), or when no suite matched. The grader is pinned by SHA, so a pull
request can change its suites but not the code that grades them. Fork pull
requests never get a runner, and the workflow uses `pull_request`, never
`pull_request_target`.

## Validation commands

```bash
# Validate a suite without calling a model (strict schema)
PYTHONPATH=<agentware>/python/src python -c "from evals.suite import load_suites; print([s.name for s in load_suites('evals/suites')])"
# With no endpoint configured the runner must exit 2, not report 0%
PYTHONPATH=<agentware>/python/src python -m evals.main --suite evals/suites --model-profile glm-5.3-flash --out /tmp/x; echo $?
# Skills repo
node scripts/verify-evals.mjs && node scripts/verify-skills.mjs
```

## Realistic usage boundaries

- No LLM grading anywhere in the default path. If an expectation cannot be
  checked by a string or regex, rewrite the expectation.
- The CI gate's `Δ vs main` column is `n/a` today; there is no stored baseline.
- Model servers are shared: use `--jobs 1` and avoid full sweeps while others
  are running.
- Evals measure model behaviour against schemas with mocked tools; they do not
  call real providers, and a passing suite is not a policy test. Policy
  enforcement is tested by the agentware `tests/kei/` table and by proving a
  deny in the deployed runtime.
- A green local run on one profile does not cover the other; run both.

## Related skills

- `build-agents-agentware` — the agent, tools, and argument semantics under test.
- `deploy-agents` — runtime and harness setup once the suites pass.
- `kei-headless-evals` — the other offline harnesses (assistant ingress, agentware evals).
