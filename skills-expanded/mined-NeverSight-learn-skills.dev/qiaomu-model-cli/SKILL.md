---
name: qiaomu-model-cli
description: |
  Call local Grok CLI, Kimi Code CLI, and Claude Code CLI with the strongest
  current default models and native tools. Use this qiaomu skill workflow when
  the user wants to run Grok
  4.5 for X/web search, image/video generation, research, or multi-tool agent
  work; run Kimi K3 (1M) for frontend UI/CSS/React/Vue work; run Claude Fable 5,
  Opus 4.8, or Sonnet 5 for coding/review/refactors; run independent multi-model
  comparisons concurrently with native stream progress, artifact verification,
  private logs, cancellation, and failed-job retry; choose between the three
  CLIs; or wrap non-interactive CLI invocations. Trigger on phrases
  like "用 grok cli", "用 kimi cli", "grok 搜 X", "kimi 写前端",
  "qiaomu-model-cli", "调用 grok4.5", "调用 k3 1m", "用 claude code",
  "用 fable 5", "opus 4.8 改代码", "分别调用三个模型", "多模型横评".
  Not for generic cloud API
  registry management (use qiaomu-llm) or OpenCLI site adapters.
metadata:
  author: 向阳乔木
  copyright: Copyright (c) 向阳乔木
  x: https://x.com/vista8
  github: https://github.com/joeseesun/
  maturity_tier: production
---

# Qiaomu Model CLI

用本机 **Grok CLI**、**Kimi Code CLI** 和 **Claude Code CLI** 做可验证的强模型调用。

Copyright (c) 向阳乔木

- X: https://x.com/vista8
- GitHub: https://github.com/joeseesun/

## Defaults

| Provider | CLI binary | Default model | Best for |
|---|---|---|---|
| xAI Grok | `grok` | `grok-4.5` | X/web 搜索、研究、生图、生视频、通用 agent |
| Moonshot Kimi | `kimi` | `kimi-code/k3` (1M context) | 前端 UI/CSS/组件、长上下文改码 |
| Anthropic Claude | `claude` | `fable` -> Fable 5 | 最复杂编码、长任务、深度推理；可切 `opus` / `sonnet` |

Always prefer these defaults unless the user names another model.

## Router Rules

1. User says **Grok / X 搜索 / 生图 / 生视频 / 实时信息 / 多工具 agent** → use Grok CLI with `grok-4.5`.
2. User says **Kimi / 写前端 / UI / CSS / React / Vue / 页面审美 / 长上下文改前端** → use Kimi CLI with `kimi-code/k3`.
3. User asks multiple models to **independently produce/compare/benchmark the same task** → use `batch`; start all independent jobs concurrently in isolated working directories.
4. User asks **one model to research and another to implement from that result** → use dependent `dual`; this is intentionally sequential.
5. User says **Claude Code / Fable / Opus / Sonnet / 复杂编码 / 多文件重构 / 严格 code review** → use Claude Code. Default `fable`; explicit alias wins.
6. Do **not** use OpenCLI for X if Grok native search/tools can do the job and the user wants Grok.
7. Prefer moving aliases (`fable`, `opus`, `sonnet`) over brittle dated Claude model IDs. If a default fails, run doctor and report the live CLI error.
8. Never print API keys, OAuth tokens, cookies, gateway URLs, or full auth/settings files.

## Modes

- `Doctor`: check binaries, login, default models.
- `Grok Chat/Agent`: non-interactive Grok task with tool permissions.
- `Grok X/Web`: force native search/fetch tools for live info.
- `Grok Image`: image generation/edit via Grok native image tools / `/imagine`.
- `Grok Video`: video generation via `/imagine-video` or native video tools.
- `Kimi Frontend`: K3 1M for UI implementation with concrete files and verification notes.
- `Claude Coding`: Fable 5 by default for complex coding; Opus 4.8 or Sonnet 5 by explicit selection.
- `Claude Review`: read-only review prompt with findings first.
- `Batch`: independent Grok/Kimi/Claude jobs run concurrently with native stream events, bounded capture, private logs, and artifact Done Gates.
- `Retry`: rerun only failed jobs from a prior `summary.json` in a fresh run directory.
- `Dual`: dependent pipeline; Grok gathers facts/assets, then Kimi receives that result and implements.

## Core Workflow

1. Classify intent: search/research, media, frontend, complex coding/review, independent batch, or dependent dual.
2. Run environment check when first used in a session or when a call fails:

```bash
python3 scripts/check_env.py
```

3. Choose provider and model:
   - Grok default: `-m grok-4.5`
   - Kimi default: `-m kimi-code/k3`
   - Claude default: `--model fable` (currently Fable 5); alternatives `opus` (Opus 4.8), `sonnet` (Sonnet 5)
4. Build a task prompt that tells the CLI to use native tools when relevant.
5. Draw the dependency graph before launching multiple models:
   - no job consumes another job's output → one `batch` call with `max_workers >= job count`
   - a later job consumes earlier output → `dual` or an explicit staged pipeline
6. For concurrent writers, give every job its own `cwd`; do not let models edit the same directory.
7. Invoke through the wrapper (preferred) or raw CLI.
8. For file-producing work, declare `expects` and optional `verify_commands`; exit code zero alone is not completion.
9. Keep progress visible: native provider events are normalized and default heartbeat is every 15 seconds.
10. On interruption, let the wrapper cancel every active process group. Resume with `retry --summary`, not by rerunning successful jobs.

### Preferred wrapper

```bash
# Grok research / X search
python3 scripts/qiaomu_model_cli.py grok --task x-search --prompt "查 @vista8 最近3条帖子，给正文和链接"

# Grok image
python3 scripts/qiaomu_model_cli.py grok --task image --prompt "一张极简黑白海报，主题是 AI coding"

# Grok video
python3 scripts/qiaomu_model_cli.py grok --task video --prompt "一只猫在爵士酒吧弹钢琴"

# Kimi frontend
python3 scripts/qiaomu_model_cli.py kimi --task frontend --prompt "把这个 landing hero 改成更精致的杂志感布局" --cwd /path/to/project

# Claude complex coding (Fable 5 default)
python3 scripts/qiaomu_model_cli.py claude --task coding --prompt "完成这个多文件重构并跑测试" --cwd /path/to/project

# Claude with a lower-cost latest model
python3 scripts/qiaomu_model_cli.py claude --model sonnet --task coding --prompt "修复这个组件" --cwd /path/to/project

# Three independent implementations: concurrent fan-out
python3 scripts/qiaomu_model_cli.py batch \
  --config examples/batch-homepages.json \
  --max-workers 3 \
  --log-dir logs/model-run

# Retry only failed jobs from a prior run
python3 scripts/qiaomu_model_cli.py retry \
  --summary logs/model-run/summary.json \
  --log-dir logs/model-retry

# Dependent pipeline: Grok output feeds Kimi
python3 scripts/qiaomu_model_cli.py dual --prompt "研究 2026 AI coding CLI 趋势，并写一个单页展示站"
```

### Raw CLI baselines

Grok:

```bash
grok -p "<PROMPT>" -m grok-4.5 \
  --permission-mode bypassPermissions \
  --output-format plain \
  --max-turns 12
```

Kimi:

```bash
kimi -p "<PROMPT>" -m kimi-code/k3 --output-format text
```

Claude Code:

```bash
claude -p "<PROMPT>" --model fable --effort xhigh \
  --output-format text --permission-mode bypassPermissions \
  --no-session-persistence
```

Notes:
- Single calls and batch jobs emit redacted JSON progress events to `stderr` immediately (`started`, `heartbeat`, `activity`, `finished`).
- Batch jobs default to each CLI's native JSON stream. High-frequency deltas are coalesced; Grok thought text is never copied into normalized events.
- `batch` writes raw stdout/stderr, normalized response text, `events.jsonl`, resumable state, and `summary.json`; one failure does not cancel independent jobs.
- Run directories use mode `0700`; logs/config/state use `0600`. In-memory stdout/stderr capture is bounded while full output continues to disk.
- `batch` is for independent work. `dual` stays sequential because stage 2 consumes stage 1 output.
- Never launch independent model calls one-by-one from the orchestrator and call that a comparison; create the config first, then make one batch invocation.
- Kimi `--prompt` cannot combine with `--yolo` or `--auto` in current CLI.
- Grok headless often needs `--permission-mode bypassPermissions` for unattended tool use.
- Claude aliases track the latest family release: `fable`, `opus`, `sonnet`. Fable may fall back to Opus for safeguarded topics.
- `bypassPermissions` allows project edits and commands. Use only in a trusted workspace; choose a stricter mode when unattended writes are not intended.
- For Grok image/video, instruct the model to use native tools (`image_gen` / `image_edit` / `/imagine` / `/imagine-video`) rather than writing fake image URLs.

## Task Prompt Contracts

### Grok X / live search

Require:
- use native web/X search tools
- no fabrication of posts, metrics, or dates
- return time, full/summary text, media flag, engagement if available, and links

### Grok image

Require:
- use native image tools
- return local/remote asset paths actually produced
- if blocked by safety, stop and report

### Grok video

Require:
- use native video generation path
- report shot plan + final asset path/URL if produced
- if unavailable, say unavailable with the CLI error

### Kimi frontend

Require:
- read existing project style first
- implement real files, not only advice
- preserve design system tokens when present
- list changed files and a short visual QA checklist
- prefer production-quality UI polish over demo scaffolding

### Claude coding/review

Require:
- read project rules and existing code before edits
- use Fable for maximum capability; use Opus/Sonnet when the user chooses speed/cost balance
- preserve existing changes and verify with project-provided checks
- for review, report findings first and do not edit

## Output Contract

For every invocation, report:

1. provider + model actually used
2. command shape (no secrets)
3. result summary / artifact paths
4. tool usage evidence when relevant (searched, generated image/video, edited files)
5. failures and next fix (`login`, binary missing, permission, rate limit)
6. for batch: `summary.json`, each job's status, elapsed time, stdout/stderr/response paths, Done Gate checks, and any timeout/cancellation

## Boundaries

- Do not store or echo credentials or private provider settings from Grok, Kimi, or Claude config files.
- Do not claim X search/image/video succeeded without CLI evidence.
- Do not push to `main` or publish accounts from this skill.
- Do not replace project-specific coding agents when the user only wants local file edits already in context; use this skill when an external strong model CLI is the point.
- Do not place concurrent writing jobs in the same `cwd`; isolate outputs and combine them only after every job has finished.
- Do not treat a heartbeat as model success. Success still requires the CLI exit code and expected artifacts.
- Do not parse thought/reasoning text into public progress. Keep raw streams private and emit only safe counters.
- Do not blindly rerun a whole successful batch. Use `retry --summary` so only failed jobs execute in a fresh directory.
- Public docs must not hardcode private absolute machine paths as required usage.

## Required Reading

1. [references/routing.md](references/routing.md)
2. [references/grok-cli.md](references/grok-cli.md)
3. [references/kimi-cli.md](references/kimi-cli.md)
4. [references/claude-cli.md](references/claude-cli.md)
5. [references/frontend-playbook.md](references/frontend-playbook.md)
6. [references/batch-and-progress.md](references/batch-and-progress.md)
7. [references/provider-adapters.md](references/provider-adapters.md)

## Useful Commands

```bash
python3 scripts/check_env.py
python3 scripts/qiaomu_model_cli.py doctor
python3 scripts/qiaomu_model_cli.py grok --task chat --prompt "..."
python3 scripts/qiaomu_model_cli.py kimi --task frontend --prompt "..." --cwd .
python3 scripts/qiaomu_model_cli.py claude --task coding --prompt "..." --cwd .
python3 scripts/qiaomu_model_cli.py batch --config examples/batch-homepages.json --max-workers 3
python3 scripts/qiaomu_model_cli.py retry --summary logs/model-run/summary.json
python3 -m unittest discover -s tests -v
python3 scripts/validate_skill.py .
```

## Metadata

- Skill: `qiaomu-model-cli`
- Version: `1.3.0`
- Owner: 向阳乔木
- Defaults verified against local CLI metadata: Grok `grok-4.5`, Kimi `kimi-code/k3` (1M), Claude aliases `fable` / `opus` / `sonnet`
