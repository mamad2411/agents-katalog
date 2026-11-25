---
name: webstone
description: Help an agent select Webstone tracks and benchmarks, prepare or resume evaluations, score saved evidence, build and share reports, submit leaderboard result PRs, or propose dataset updates. Use for the Webstone evaluation lifecycle; distinguish supported commands from stages requiring a source checkout or external services.
---

# Webstone workflow

Webstone is agent-oriented evaluation software. This skill plans the work; CLI commands execute existing deterministic owners. Do not invent a universal pipeline, infer scores from screenshots or substitute missing timing/cost with zero.

## Start and select

1. Inspect the user's goal and available evidence. Start at scoring or reporting if they already have compatible saved attempts. Determine the Track, benchmark, exact dataset commit, provider/model configurations, run or resume, requested scope and deliverables. `webstone tracks` and `webstone datasets list` print JSON from the installed lock without downloads or calls. The website's result edition, dataset revision and software version are distinct identities.
2. Check `webstone tracks`. If the CLI is missing or the installed release lacks this command, follow the [installation guide](https://github.com/lexmount/webstone/blob/main/docs/agent-workflows.md#install-software-and-skill) and use the source checkout if needed. Then open the selected track guide from the command output. For a checkout, read its AGENTS.md and the maintained benchmark-report skill before evaluation/report work. For a packaged installation, use a source checkout at the package's corresponding release tag when advanced code, profiles or reference assets are required; do not assume online main documentation matches an older installed version. Install only required optional extras and external browsers/sites. `--help` discovers the selected owner's actual flags; never guess a generic `--benchmark` or `--track` flag on a command that does not support it.
3. Freeze dataset/scorer IDs, task population, scopes, concurrency, retry policy, call budget, timers and billing units before expensive collection. Honor existing authorization; ask only for genuinely missing choices or permissions. Preflight a bounded sample, then run the existing owner. Save evidence outside Git under WEBSTONE_DATA_HOME or ~/.webstone, and preserve resumed cohorts.

## Prepare and run by Track

| Track | Recommended workflow |
| --- | --- |
| Web Fetch | Choose live URLs, frozen pages or the offline fixture. Follow the [Fetch guide](https://github.com/lexmount/webstone/blob/main/src/harness/web_fetch/README.md) for tools, credentials and scope. For a new live run, ask for full or main content if the user hasn't chosen (full for unattended runs). Validate a sample, fetch with each configured method, then score the saved responses against the selected references. |
| Web Search | Pin the retrieval dataset and output layer, then configure the selected providers and credentials as in the [Search guide](https://github.com/lexmount/webstone/blob/main/src/harness/web_search/README.md). Preflight the selected profile, issue the same queries for each provider and score each selected output layer separately from saved responses. |
| Web Extract | Pin the inputs and field schema. For frozen pages used by remote methods, verify a matching public snapshot host, such as Cloudflare Pages or an existing HTTPS host, from the provider's network. Use original URLs for live-page suites. Follow the [Extract guide](https://github.com/lexmount/webstone/blob/main/examples/web_extract/README.md) to prepare inputs, plan and preflight, collect tool outputs, then score the extracted fields. |
| Browser Trajectory Replay | Select the recorded suite and browser versions. For WebArena-Verified, prepare reachable sites and test accounts, reset writable sites and check baseline readiness before replay. Use the guide for [WebArena](https://github.com/lexmount/webstone/blob/main/docs/webarena-fixed-trajectory-reproduction.md), [curated replay](https://github.com/lexmount/webstone/blob/main/examples/trajectory_replay/README.md), or [Headless Browser](https://huggingface.co/datasets/Lexmount/LexBench-Headless-Browser#execute-with-the-original-runner). Replay the same actions in each browser and score the recorded outcome with the suite's evaluator. |
| Browser Use (experimental) | Select the task suite, agent, model and browser. Prepare isolated target sites with the accounts and evaluator in the [Browser Use guide](https://github.com/lexmount/webstone/blob/main/examples/browser_use/README.md). Preflight logins and evaluation, reset task state, let each agent choose its actions, then score its outcome. |

Use the [CLI entry points](https://github.com/lexmount/webstone/blob/main/docs/agent-workflows.md#supported-entry-points) and each command’s `--help` for flags and extras.

A changed scorer or reference reuses saved calls where possible. Never select retries for higher scores, overwrite historical verdicts or merge incomplete populations into a certified result. Retain denominator and source hashes. Keep all-call latency separate from success-only latency; retain actual charges, quoted intervals and missing cost separately.

## Report and share

Build only when requested, through the selected track's existing report/check/package stages. Web Fetch `webstone report RUN` rebuilds saved fixture/generic evidence; specialized profiles use the guide's current owner. Inspect HTML, evidence links, language, units, cost and latency; do not claim unavailable measurements. Report sharing requires an authorized host bound in that report's profile. Use its existing publish/verify command; never borrow another report's destination. A build is not a deployment. Return the inspected report path or verified live link and exact source identity.

## Submit leaderboard results

When the user asks to submit leaderboard scores, reuse the installed `submit-webstone-result` skill or install it from [webstone-site](https://github.com/lexmount/webstone-site/blob/main/.agents/skills/submit-webstone-result/SKILL.md) using the agent's skill installer. If there is no installer, copy that complete `SKILL.md` into `submit-webstone-result/` under the agent's skills directory. Open and follow it for this submission.

Hand off the measured scores, exact benchmark and participant versions, methods, and public evidence. The submission skill owns the result format, versioning and PR. It works with GitHub and Node.js. Submit only when asked, and leave merging to the maintainer.

## Update datasets

`webstone datasets fetch --help` restores pinned inputs. `webstone datasets propose --help` delegates to the shared definition publisher with explicit checkout, revision, output and optional HF --create-pr. This builds a proposal, never merges it or tags dataset main. `webstone datasets pin --help` changes a Webstone checkout's selection only after the dataset input commit has been reviewed and merged; inspect the diff and propose a code PR. Explicitly select the target checkout with --root. Preserve immutable tags and frozen source/hash bindings. See [dataset revision rules](https://github.com/lexmount/webstone/blob/main/docs/benchmarks.md#historical-bindings-and-new-revisions). No automatic adoption of latest tags.

## Finish

Return selected inputs, run/scoring/report status, actual tests, PR/share URLs, review coverage and limitations. Distinguish planned, executed, reviewed, merged and deployed. Never create software tags or PyPI uploads from a dataset/result update; software release needs its separate maintainer-approved PR, tag and protected publishing workflow.
