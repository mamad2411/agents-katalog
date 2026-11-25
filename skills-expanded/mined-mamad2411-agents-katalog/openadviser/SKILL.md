---
name: openadviser
description: Consult ChatGPT Web, Grok, or another OpenAdviser-supported web AI provider as an external adviser using a manually prepared compact-style decision brief. Use when an AI agent is stuck, faces an engineering/product/design decision, needs a second opinion, needs current web-facing research, needs deep web research, needs online best-practice discovery, should gather web information to solve a problem, should validate an approach before continuing, or needs to search posts on X/Twitter. Use ChatGPT for deep web research and best-practice research; use Grok for X post search and include "search posts on X" in the prompt. The caller must write the context brief explicitly instead of reading hidden session files.
---

# OpenAdviser

Use this skill to ask an external web AI adviser through the `openadviser` CLI and Chrome extension.

Default provider is `chatgpt`. Pass `--provider grok` to use Grok after that Chrome profile is logged in. The skill is agent-agnostic: Codex, Claude Code, OpenCode, Cursor, and other local agents can use the same context contract.

Do not read rollout JSONL, `state_5.sqlite`, session metadata, encrypted reasoning, or other agent-internal hidden state. This skill intentionally avoids automatic context reconstruction. The calling model must decide what context matters and provide it explicitly.

## Prerequisites

The human user must have:

1. Installed the CLI: `npm install -g openadviser`
2. Started the bridge: `openadviser server`
3. Loaded the Chrome extension from `openadviser extension-path`
4. Logged in to the selected provider in Chrome
5. Kept Chrome and network healthy; `read`/`wait` will re-activate the OpenAdviser worker window before extraction

If the bridge is not already running, `scripts/openadviser.js` tries to start it automatically.

## Required Workflow

1. Use the `compact` skill's section structure as the source inventory.
2. Rewrite that inventory into a decision brief for an external expert. The brief must describe the user's real situation, not the act of calling OpenAdviser.
3. Put the real user goal and the exact adviser judgment in `Goal`. Never write `Primary task: ask adviser...`, `test adviser...`, or `success criteria: adviser returns an answer` unless the user's actual task is to debug this skill.
4. Separate verified facts, primary evidence, caller assessment, assumptions/hypotheses, decisions, risks, and unknowns.
5. Include enough information for the adviser to disagree intelligently: constraints, failed attempts, test results, exact errors, relevant files, source links, dates, version numbers, screenshots, observed page/DOM facts, and unresolved tradeoffs.
6. When local code affects the answer, include the directly relevant code evidence, not just paths. Web providers cannot read the caller's filesystem.
7. Add anti-bias context when useful: the best argument against the caller's preferred approach, what is not verified, and what would change the decision.
8. Exclude skill catalogs, encrypted reasoning, hidden system text, raw transcript dumps, low-signal tool chatter, secrets, generated/vendor files, and unrelated code.
9. Ask one focused adviser question with a decision frame.
10. Send the context brief plus question with `scripts/openadviser.js send`, capture `result.runId`, then run `scripts/openadviser.js wait --run-id <runId>` in a background terminal/session while continuing non-dependent work. Use `read` only when a single manual snapshot is needed.
11. Treat the answer as advice, not authority; reconcile it against primary evidence and continue locally.

Before first use, or whenever context quality is uncertain, read `references/context-brief-method.md`. For the design rationale and local limitations, read `references/adviser-strategy.md`.

## Context Brief Contract

Use the compact sections below, but write them as a decision brief. The section content matters more than the labels: `Goal` must be the real user goal, `Current State` must contain verified state, and `Critical Technical Context` must separate facts from interpretations.

```markdown
## Goal
- Primary task: [user's actual desired outcome]
- Secondary task(s):
- Success criteria:
- Adviser decision needed: [the exact judgment you want]

## Constraints & Preferences
- Verified constraints:
- User preferences:
- Exclusions / must not do:

## Current State
### Done
- [x] Fact: [completed work / confirmed finding / evidence]

### In Progress
- [ ] [Work currently underway]

### Blocked
- Fact:
- Assumption/Hypothesis:
- If none, write `(none)`

## Key Decisions
- **Decided**: [decision] - [reason/evidence]
- **Proposed**: [candidate decision] - [why under consideration]
- **Rejected / avoided**: [approach] - [why rejected]

## Important Files & Code Locations
- `path/to/file`: [Why it matters]
- Relevant code evidence:
  - `path/to/file` lines X-Y: [symbol / behavior / why this exact excerpt matters]
  - Include an excerpt only when the web adviser must reason about local implementation details.
  - If no local code is needed, write `(none; external research or strategy only)`.

## Critical Technical Context
- Verified facts:
  - [fact + evidence]
- Caller assessment / hypotheses:
  - [interpretation that may be wrong]
- Key functions / classes / modules:
  - `[symbol]`: [role]
- Important commands:
  - `[command]`: [purpose / result]
- Important errors:
  - `[exact error message]`
- Important config / API / environment details:
  - [detail]
- Important data / examples / references needed later:
  - [detail]
- If none, write "(none)"

## Validation Status
- Verified:
  - [What was tested / confirmed]
- Not yet verified:
  - [What still needs testing]
- Test / validation gaps:
  - [Any risky unverified areas]

## Risks & Open Questions
- [Known risks]
- [Unknowns that may affect next steps]
- [Potential places easy to make mistakes]

## Next Steps
1. [Most logical next action]
2. [Next action after that]
3. [Next action after that]

## Handoff Instructions for the Next Model
- Read first:
- Do not repeat:
- Check / verify first:
- Then continue with:
```

Bad context: `Primary task: Ask adviser to research X`. This describes the tool call.

Good context: `Primary task: Decide how to redesign X under constraints Y; Adviser decision needed: whether approach A or B is safer`. This describes the situation.

For broad research requests such as `调研 skills`, do not brief the adviser as if the answer itself is the goal. Brief the real local decision: why the research matters, what artifact or implementation it should inform, what is already known, what constraints apply, and what recommendation is needed.

## Code Evidence Rules

When the adviser needs to reason about local code, provide the smallest sufficient code packet:

- Include only files, functions, call sites, config blocks, tests, errors, or DOM snippets directly connected to the question.
- For each excerpt, include path, line range, relevant symbols, and why it matters.
- Prefer narrow excerpts around the bug/decision path. Include an entire file only if it is small and most of it is relevant.
- Include related tests or fixtures when the question depends on behavior, not just implementation.
- Do not include unrelated code, generated output, dependencies, lockfiles, secrets, credentials, or large raw logs.
- If code is intentionally omitted, say why the adviser can answer without it.

Use wrapper-managed inclusion when possible:

```bash
node path/to/skills/openadviser/scripts/openadviser.js send "your focused question" \
  --context-file ./adviser-context.md \
  --include-file src/provider.ts#L40-L120 \
  --include-file tests/provider.test.ts#L1-L90
```

`--include-file` is explicit and repeatable. It does not discover files automatically; the calling agent must decide which code is relevant. Use `--code-file` as an alias. If a file is large, provide a `#Lstart-Lend` range.

## Background Terminal Use

OpenAdviser answers can take a long time because they depend on a live browser, network health, provider page load, web search, and model response time. Do not run `send` in the background just to wait for the answer: `send` returns quickly after submitting the prompt. Run `wait` in a background terminal/session whenever the answer is not an immediate blocker.

Recommended agent flow:

1. Run `send` in the foreground and capture the returned `result.runId`.
2. Start `wait --run-id <runId> --json` in a background terminal/session, redirecting output to a file if useful.
3. Continue local work that does not depend on the adviser answer.
4. Later inspect the `wait` output, or call `read --run-id <runId> --json` for a manual snapshot.
5. Integrate the adviser result only after checking it against the local evidence and constraints.

## Commands

Send a manually prepared context file:

```bash
node path/to/skills/openadviser/scripts/openadviser.js send "your focused question" --context-file ./adviser-context.md
```

Send with caller-selected code evidence:

```bash
node path/to/skills/openadviser/scripts/openadviser.js send "your focused question" \
  --context-file ./adviser-context.md \
  --include-file src/background.js#L204-L260
```

Pipe context through stdin:

```bash
cat ./adviser-context.md | node path/to/skills/openadviser/scripts/openadviser.js send "your focused question"
```

Use Grok instead of the default ChatGPT provider:

```bash
cat ./adviser-context.md | node path/to/skills/openadviser/scripts/openadviser.js send "your focused question" --provider grok
```

The `send` command starts the local bridge if needed, submits the prompt to the selected web AI provider, and prints a bridge task JSON containing `result.runId`. It does not wait for the answer.

`send` opens a new provider tab in the OpenAdviser worker window. This is intentional: ChatGPT and Grok can stall or render partial answers when their tab is hidden, even when Chrome Memory Saver is disabled. The worker tab must remain active and visible in its own window. If a run stays `waiting` or `streaming` for about 3 minutes with no progress, check whether the worker window is minimized, fully covered, offline, logged out, or blocked by provider verification.

The worker window is positioned automatically: a small popup at the bottom-right of the primary screen's available work area, leaving a margin above the Windows taskbar or equivalent system shelf. Do not pass manual window geometry; the tool owns this placement.

`read` always re-activates the run's worker window before extracting text. `wait` does this on every polling cycle because it repeatedly calls `read`. Treat this as the default pin substitute: while a long answer is generating, keep `wait` running so the small worker window periodically returns to the foreground and gives ChatGPT/Grok an active visible tab to continue rendering in.

Read the current answer snapshot later:

```bash
node path/to/skills/openadviser/scripts/openadviser.js read --run-id <runId> --json
```

Wait until the answer is complete:

```bash
node path/to/skills/openadviser/scripts/openadviser.js wait --run-id <runId> --json
```

Run `wait` in a background terminal/session when the adviser answer is not the immediate blocker. It polls `read` until `result.status` is `complete` or the timeout is reached. `wait` uses full-read mode by default: it hydrates lazy-rendered answer content and, when available, uses the provider's own Copy response button inside the page to capture full text without requiring the agent or user to touch the system clipboard.

Use `read --full` for one manual full snapshot:

```bash
node path/to/skills/openadviser/scripts/openadviser.js read --run-id <runId> --full --json
```

Use plain `read` when a quick DOM snapshot is enough and the caller will decide whether to wait longer.

The built-in adviser prompt tells the web AI provider: "Before answering, first analyze your task, examine the problem structure from multiple angles, then search the web for relevant information to support your judgment."

## Deep Web Research Use Case

When the task needs deep network research, online best-practice discovery, or web information gathering to solve a concrete problem, use ChatGPT:

```bash
cat ./adviser-context.md | node path/to/skills/openadviser/scripts/openadviser.js send "请进行深度网络调研，查找相关最佳实践，并基于事实、推断和建议回答这个决策问题。" --provider chatgpt
```

Rules for this use case:

- Prefer `--provider chatgpt` unless the requested evidence is specifically X/Twitter posts.
- Brief the real problem, decision, constraints, and what the caller already knows. Do not send only `调研 X`.
- Ask ChatGPT to distinguish public facts, source-backed claims, inference, and recommendations.
- Use this path for current ecosystem research, implementation best practices, architecture comparisons, library/tooling choice, security guidance, operational practices, and market/product research that benefits from broad web sources.
- After receiving the answer, verify important claims against primary sources before acting.

## X Post Search Use Case

When the task needs current posts from X/Twitter, use Grok:

```bash
cat ./adviser-context.md | node path/to/skills/openadviser/scripts/openadviser.js send "search posts on X" --provider grok
```

Rules for this use case:

- Always pass `--provider grok`.
- The adviser question sent to Grok must include the exact phrase `search posts on X`; keep any topic, scope, and desired output structure in the context brief.
- Do not use ChatGPT for this use case unless Grok is unavailable and the user accepts the fallback.

## Useful Options

- `--context-file <path>`: Compact-style context file.
- `--context <text>`: Inline compact-style context.
- `--include-file <path[#Lx-Ly]>`: Caller-selected relevant code evidence. Repeatable. Use only for code directly related to the adviser question.
- `--code-file <path[#Lx-Ly]>`: Alias for `--include-file`.
- `--question-file <path>`: Adviser question file.
- `--provider <chatgpt|grok>`: Web AI provider. Default `chatgpt`.
- `--url <url>`: Override provider URL for the send action.
- `--strict-context`: Fail before sending if core compact/adviser signals are missing.
- `--json`: Print the full bridge task object.
- `--timeout <ms>`: Atomic bridge action wait timeout. Default `120000`.
  - For `wait`, total wait timeout. Default `600000`.
- `--interval <ms>`: Poll interval for `wait`. Default `5000`.
- `--page-load-timeout <ms>`: Soft provider page-load wait before continuing to inject/send. Default `15000`.
- `--input-timeout <ms>`: Provider composer wait timeout before send.
- `--run-id <id>`: Run id returned by `send`; required for `read`.
- `--full`: Hydrate rendered content and use provider Copy response before DOM fallback.
- `--read-timeout <ms>`: Page read timeout. Default `15000`.
- `--read-task-timeout <ms>`: Per-read bridge task timeout for `wait`. Default `120000`.
- `--copy-button`: On `read`, also try the provider's Copy response button. Default is DOM extraction only.
- `--no-full`: Disable `wait`'s default full-read mode.
- `--openadviser-bin <command>`: OpenAdviser executable. Default `openadviser`.

## Adviser Question Style

Ask focused questions:

- `基于这些约束，哪个实现路线风险最低？`
- `这个 bug 的下一步最有效验证是什么？`
- `请审查这个设计是否存在明显遗漏。`
- `请调研当前网络信息，并给出事实、推断和建议。`

Do not ask broad questions without a decision frame. If the user asks a broad research question, first brief the current situation and why the research matters.

Prefer question forms like:

- `基于这些事实和约束，这个 context contract 是否足够，哪里会误导外部顾问？`
- `请区分当前公开事实、你的推断和建议，评估方案 A/B 哪个更适合本项目。`
- `如果你是外部 reviewer，你会要求我先补哪些证据再做决定？`
