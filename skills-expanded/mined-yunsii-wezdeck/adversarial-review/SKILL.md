---
name: adversarial-review
description: >
  Multi-role adversarial code review (platform skill). Agent loads this skill and
  runs the co-located runner (find → refute → sandbox repro); humans only state
  intent (审一下 / 对抗审查). Works for OpenClaw Main and host TUI agents via
  user-level skill links. Use when user asks for adversarial review, acceptance
  recommends review, or runtime code changed before merge.
---

# Adversarial review (platform skill — single source)

**Who runs:** the coding agent (OpenClaw Main / Claude-TUI / Codex-TUI), **not** the human.  
**Never** tell the user to copy-paste `run.sh` as the primary path.  
**Never** replace this with a solo monologue and call it 对抗审查 (that is 设计批判).

This directory is the **only** skill + runner unit. Other paths are **symlinks**
(user-level or in-repo discovery). Do not maintain a second SKILL.md body.

## Who runs what

| Actor | Duty |
| --- | --- |
| **Human** | Intent only:「对抗审查」「审一下这批改动」「按推荐审查」 |
| **Any agent** | **Load this skill → resolve TOOL + TARGET → run → disclose** |
| **Host headless backends** | `claude` / `codex` / `grok` as find/refute (not ACP by default) |

## When to load / run

- User asks for 对抗审查 / adversarial review / multi-role review
- Write-task checklist: acceptance suggests review
- Runtime code/scripts changed (any git TARGET the agent may review)
- After editing this toolkit itself → `dogfood`

**Skip / redirect:**

- Pure docs/tests-only (runner auto-skips); user explicitly skips with reason
- **Design docs / RFC / ADR / 方案提案** (no runtime diff): do **not** force this
  skill. Use **设计评审** (structured checklist in host
  `validation.md` → Design proposal review) or **brainstorm** only when the user
  still wants alternative approaches. Never label a doc critique 对抗审查.

## Multi-role minimum

| Role | Stance | Runner stage |
| --- | --- | --- |
| find / reviewer | guilty-until-proven | stage 1 |
| refute / refuter | kill weak findings | stage 2 |
| repro | empirical in sandbox | stage 3 |

- Prefer **different families** than the **writer** (strategy B via `--writer`).
- Same capability twice OK → label **SINGLE-MODEL** / degraded; **do not skip refute**.
- Solo essay without opposite roles → **设计批判**, not 对抗审查.

## Paths: TOOL vs TARGET (critical)

**Do not** assume `./skills/adversarial-review` exists in the repo under review.

| Name | Meaning |
| --- | --- |
| **TOOL_HOME** | This skill/runner directory (where `run.sh` lives) |
| **TARGET** | Git repo being reviewed (`--repo` or current git toplevel) |

### Resolve TOOL_HOME (first hit wins)

```text
1. $ADV_REVIEW_HOME                          # explicit override
2. directory of this SKILL.md if run.sh is co-located
3. $WEZDECK_ROOT/skills/adversarial-review
4. $HOME/github/wezterm-config/skills/adversarial-review
5. else: fail clearly — "adversarial-review tool not installed; run link-platform-skills.sh"
```

**Never** default to `$TARGET/skills/adversarial-review` unless that path
actually exists (compat only).

### Resolve TARGET

```text
--repo <path>  if given
else: git rev-parse --show-toplevel from cwd
```

## Context pack v1

Find and refute receive the **same** pack (not bare diff):

- META / INTENT / CHANGESET / DIFF / FILES / PROJECT_SLICE / NOTES
- PROJECT_SLICE = downstream refs to changed symbols (blast radius); grep floor,
  language-aware resolvers pluggable. `--no-impact` to skip.
- **Main-agent filter (optional):** coarse filter of grep `same-name` candidates
  before gates — not a fourth adversarial role. See procedure below.
- `--head WORKTREE` includes uncommitted TARGET changes
- `--intent` or `--intent-file` (else commit message or degraded none)
- Budget: `--max-files` (10) `--max-file-bytes` (40960) `--context-window` (200)
- Optional: `--keep-pack DIR` to retain pack.md + `impact_candidates.json`

```bash
# One-shot (no filter) — still valid default
"$TOOL_HOME/run.sh" HEAD --head WORKTREE --repo "$TARGET" \
  --writer main --intent "what this change is for" --mode strict
```

## Agent procedure

1. **Identify** TARGET cwd/repo, `BASE_REF`, **writer**  
   (`main` | `claude` | `codex` | `grok` | `human`)
2. **Resolve** TOOL_HOME (above). Confirm `"$TOOL_HOME/run.sh"` is executable.
3. **Optional dry probe**
   ```bash
   "$TOOL_HOME/lib/select-backends.sh" --writer <writer> --no-probe
   ```
4. **Optional · main-agent PROJECT_SLICE filter** (recommended when impact noise is high
   or you already know the module map; skip when candidates are few / empty):

   You (the orchestrating main agent) have project context. You may **coarse-filter**
   grep floor hits before find/refute. This is **material budget**, not review:

   | Do | Don't |
   | --- | --- |
   | Drop obvious decoy same-name (wrong language tree, generated, lock, unrelated package) | Drop because “probably unused” without a reason |
   | Keep anything that might be a real consumer | Write findings / severities here |
   | When unsure → **KEEP** | Shrink the slice to make the change look safer |
   | Record short notes on what you dropped | Replace refute or claim you “pre-reviewed” |

   ```bash
   PACK_DIR="$(mktemp -d "${TMPDIR:-/tmp}/adv-pack.XXXXXX")"
   "$TOOL_HOME/run.sh" <BASE_REF> --repo "$TARGET" --writer <writer> \
     --head WORKTREE --pack-only --keep-pack "$PACK_DIR" --json \
     > "$PACK_DIR/pack-only.json"
   # Read $PACK_DIR/impact_candidates.json (or .impact_candidates in pack-only.json).
   # Write keep list (array of hits, or object form):
   #   { "keep": [ ... ], "dropped": [ ... ], "filter": "main-agent",
   #     "notes": "dropped foo.go: decoy same-name in vendor" }
   # Template: $PACK_DIR/project_slice.keep.example.json
   ```

   If `impact_candidates_n == 0` or you choose not to filter, skip to step 5 without
   `--project-slice-file`.

5. **Run gates**
   ```bash
   "$TOOL_HOME/run.sh" <BASE_REF> --repo "$TARGET" --writer <writer> --mode strict \
     --project-slice-file "$PACK_DIR/project_slice.keep.json"   # if filtered
   ```
   Or one-shot without filter:
   ```bash
   "$TOOL_HOME/run.sh" <BASE_REF> --repo "$TARGET" --writer <writer> --mode strict
   ```
   Explicit backends only if user named them:
   ```bash
   "$TOOL_HOME/run.sh" <BASE_REF> --repo "$TARGET" \
     --reviewer claude --refuter codex --mode strict
   ```
   **长跑解耦(host 支持后台时)**：三门全量 + 慢后端（codex）可能数分钟。若 host
   支持后台执行（Claude Code 的 Bash `run_in_background`），后台跑 run.sh 且
   `--json > <file>`，完成后读该文件再汇报，别同步阻塞会话；host 不支持后台
   （如 Codex-TUI）则同步跑，先给用户一句「耗时约 N 分钟」预告。
6. **Report** with mandatory disclosure (below). Include `impact_filter` when set.
   Honest fail if tool/backends fail.
7. **Do not** claim cross-agent if form is single-model; do not invent green gates.

### Writer → expected pair (strategy B)

| writer | Typical pair when available |
| --- | --- |
| `claude` / Claude-ACP/TUI | `codex` × `grok` |
| `codex` / Codex-* | `claude` × `codex` (else × `grok`) |
| `main` / Main-Grok | `claude` × `codex` |
| `human` | same as global best |

## Mandatory disclosure (paste into 结果)

```text
## 对抗审查披露
- writer: Main-Grok | Claude-ACP | Codex-ACP | human | …
- 形态/form: cross-family | partial-avoidance | single-model-multi-role | …
- form/degraded/reason: (from select-backends / run log)
- reviewer 全名 / 立场: …
- refuter 全名 / 立场: …
- impact_filter: none | main-agent (kept K / candidates C; dropped D) + notes if any
- repro: 已跑 | 跳过（理由）
- 命令或范围: run.sh <BASE> --repo <TARGET> --writer … [--project-slice-file …]
- skipped_gates: … | 无
- 关键结论（每条标 [阻塞] / [非阻塞·backlog]）: …（绑 find/refute/repro）
```

## Helper commands (agent-only)

```bash
"$TOOL_HOME/run.sh" selfcheck claude codex grok
"$TOOL_HOME/run.sh" dogfood --mode strict --fail-on-finding
"$TOOL_HOME/run.sh" <BASE> --repo "$TARGET" --writer main --dry-run --no-probe
"$TOOL_HOME/run.sh" <BASE> --repo "$TARGET" --pack-only --keep-pack /tmp/p --json
"$TOOL_HOME/run.sh" <BASE> --repo "$TARGET" --project-slice-file /tmp/p/project_slice.keep.json
PROVIDER_MOCK=1 "$TOOL_HOME/run.sh" <BASE> --repo "$TARGET"   # offline, no LLM
# reasoning effort per stage: find/refute=high, repro=low (passed to provider CLI)
```

Install / refresh user-level discovery (idempotent):

```bash
# from wezdeck primary
./scripts/dev/link-platform-skills.sh
```

## Don't

- Don't ask the human to run `run.sh` as the main path
- Don't use ACP CODEX_HOME for review (`env -u CODEX_HOME` is inside provider)
- Don't skip refute when claiming 对抗审查
- Don't call solo Main analysis 对抗审查
- Don't run this skill on pure design-doc review and claim 对抗审查
- Don't treat main-agent PROJECT_SLICE filter as a review gate or drop hits to hide risk
- Don't assume the skill lives only under the TARGET repo
- Don't force-push; wezdeck personal mainline may push master after green (L0-13/19)

## Related

- Runner (this dir): `run.sh`, `lib/`, `prompts/`
- Docs: `docs/adversarial-review.md` (wezdeck)
- Host doctrine: `agent-profiles/v1/en/validation.md`
- Link installer: `scripts/dev/link-platform-skills.sh`
- OpenClaw L0-21: short always-on rule in `workspace/AGENTS.md`; **disclosure template SoT = this file**
