---
name: brainstorm
description: >
  Multi-persona divergent→convergent brainstorm (platform skill). Agent loads
  this skill and runs the co-located runner (diverge → challenge → converge);
  humans only state intent (头脑风暴 / 帮我发散一下 / brainstorm / 想点子).
  Sibling of adversarial-review; reuses its provider layer. Use when the user
  wants ideas / options / approaches for an open-ended problem — NOT for
  reviewing existing code (that is adversarial-review).
---

# Brainstorm (platform skill — single source)

**Who runs:** the coding agent, **not** the human.
**Never** tell the user to copy-paste `run.sh` as the primary path.
**Never** replace this with a solo idea dump and call it a brainstorm — the
point is *multiple independent personas + cross-model*, then a judge.

This directory is the **only** skill + runner unit. Other paths are symlinks
(installed by `scripts/dev/link-platform-skills.sh`). Do not maintain a second
SKILL.md body.

## Who runs what

| Actor | Duty |
| --- | --- |
| **Human** | Intent only:「头脑风暴」「帮我想想点子」「发散一下这个问题」 |
| **Any agent** | Load this skill → phrase the problem → run → relay result |
| **Host headless backends** | `claude` / `codex` / `grok` as personas / challenger / judge |

## When to load / run

- User wants ideas, options, approaches, or angles on an open-ended question
- User explicitly says 头脑风暴 / brainstorm / 发散 / 想点子

**Skip / redirect:**

- Concrete diff / existing **code** → **adversarial-review** (this skill is
  generative, not a defect finder)
- Someone's **design doc / RFC / ADR / 方案** when the intent is only to
  **evaluate that proposal** → default **设计评审** (main-agent structured
  challenge; host `validation.md` → Design proposal review). Do **not** default
  to a full diverge pass that ignores the proposal
- Same design doc when the user still wants **alternatives** → this skill is
  appropriate: phrase problem + extract hard constraints from the doc; prefer
  challenge-heavy use; full diverge only if the problem space is still open

## Three stages (divergent → convergent)

| Stage | Role | Stance |
| --- | --- | --- |
| 1 diverge | N persona lenses × cross-provider | expand — maximize novelty, no self-censoring |
| 2 challenge | devil's advocate | stress-test feasibility/risk, do not delete ideas |
| 3 converge | judge / facilitator | blind-rank + synthesize a recommendation |

Built-in personas (lenses): Moonshot Innovator · Pragmatic Builder ·
End-User Advocate · Contrarian/First-Principles. Configurable in
`lib/personas.conf` — add a lens = one line, no code edits.

**Reasoning effort per stage** (passed to the provider CLI): diverge=`low`
(favour breadth/speed over deep reasoning), challenge=`medium`, converge=`high`
(scoring + synthesis is where depth pays off).

## Why stateless (no session resume)

Each stage is a **fresh provider call**; the prior stage's JSON is passed as
INPUT, **not** via `claude --resume` / `codex exec resume`. Deliberate:

- **Diverge personas must not see each other** — independence is what defeats
  groupthink / anchoring; resume would share one context.
- **Resume binds a single provider**; brainstorm wants cross-model diversity
  (personas + challenger + judge on *different* backends when available).
- Stateless calls stay reproducible and each stage's JSON is schema-checked.

(Same rationale as adversarial-review — see memory `adversarial-review-no-resume`.)

## Agent procedure

1. **Phrase** the problem in one line; gather any hard constraints.
2. **Run** (defaults: 4 personas rotated over all available providers,
   challenger = 2nd available, judge = 3rd available):
   ```bash
   "$TOOL_HOME/run.sh" "<the problem>" --constraints "<optional>"
   ```
   Pin backends only if the user named them:
   ```bash
   "$TOOL_HOME/run.sh" "<problem>" \
     --diverge claude,codex --challenger codex --judge grok
   ```
   **长跑解耦(host 支持后台时)**：多角色 × 慢后端可能数分钟。若 host 支持后台执行
   （Claude Code 的 Bash `run_in_background`），后台跑 run.sh 且 `--json > <file>`，
   完成后读该文件再汇报，别同步阻塞会话；host 不支持（如 Codex-TUI）则同步跑并
   先给「耗时约 N 分钟」预告。
3. **Relay** the top ideas + synthesis + key tradeoffs, with the disclosure
   block below. Honest note if a stage was skipped (single-model / unavailable).

`$TOOL_HOME` = this directory (where `run.sh` lives); resolve via
`$ADV_REVIEW_HOME`-style discovery or `$HOME/github/wezterm-config/skills/brainstorm`.

## Options (see `run.sh --help`)

`--problem-file F` · `--constraints TEXT` / `--constraints-file F` ·
`--personas N` (1–4) · `--diverge CSV` · `--challenger P` · `--judge P` ·
`--top N` · `--json` · `--dry-run`

## Mandatory disclosure (paste into 结果)

```text
## 头脑风暴披露
- diverge personas: <N> over <providers>
- challenger: <provider>
- judge: <provider>
- consensus: 单盲评委推荐，非多模型共识（cross-model UNREVIEWED）
- notes / skipped: … | 无   (single-model? stage skipped?)
- top 想法(带 score/verdict) + synthesis + key tradeoffs
```

## Helper commands (agent-only)

```bash
"$TOOL_HOME/run.sh" selfcheck claude codex grok
"$TOOL_HOME/run.sh" "<problem>" --dry-run
"$TOOL_HOME/test.sh"           # offline smoke — PROVIDER_MOCK=1, no LLM calls
"$TOOL_HOME/test.sh" --live    # same checks, but against real providers
```

Install / refresh user-level discovery (idempotent):

```bash
./scripts/dev/link-platform-skills.sh
```

## Don't

- Don't ask the human to run `run.sh` as the main path
- Don't collapse to a solo idea list and call it a multi-persona brainstorm
- Don't use it to review existing code — that's adversarial-review
- Don't default to full multi-persona diverge just to critique one closed proposal
  (that is 设计评审, not brainstorm) unless the user wants alternatives
- Don't claim cross-model diversity when only one provider was available (the
  runner marks single-model in `notes`)

## Related

- Runner (this dir): `run.sh`, `lib/ideas-schema.json`, `prompts/`
- Sibling skill (provider layer source): `../adversarial-review/`
- Design-doc routing (no dedicated skill): host `validation.md` → Design proposal review
- Link installer: `scripts/dev/link-platform-skills.sh`
- Memory: `adversarial-review-no-resume` (why stateless, not resume)
