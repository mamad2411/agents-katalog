---
name: harness-orchestration
description: "Backend orchestration scorecard (Claude/Codex/Cursor) — HTML + terminal summary. Triggers: scorecard, backend usage, 自慢. Skip for: implementation, review, planning, release."
description-en: "Backend orchestration scorecard (Claude/Codex/Cursor) — HTML + terminal summary. Triggers: scorecard, backend usage, 自慢. Skip for: implementation, review, planning, release."
description-ja: "このセッション/プロジェクトでどれだけマルチバックエンド (Claude / Codex / Cursor) を活用したかを見せる。ledger と累計から HTML スコアカード + ターミナルサマリを on-demand で生成する。「オーケストレーション活用」「scorecard」「どのバックエンド使った」「Codex/Cursor どれだけ使った」「累計」「自慢」で発動。実装・レビュー・計画・リリースでは読み込まない。"
allowed-tools: ["Read", "Bash"]
disallowed-tools: ["Write", "Edit", "MultiEdit"]
argument-hint: "[--out <path>|--no-open|--terminal]"
---

# Harness Orchestration Scorecard

このセッション/プロジェクトの backend 活用度（Claude=ホスト / Codex / Cursor への委譲）を可視化する read-only スキル。
記録の正本は `.claude/state/orchestration-ledger.jsonl`（companion が委譲ごとに追記、Phase 90.1.1）と
`.claude/state/orchestration-totals.json`（セッション終了/完了時に冪等 roll up、Phase 90.1.2）。

> 表示は on-demand のみ。作業中は出さず、見たい時にこのスキルで出す。
> 全タスク完了時の 1 回だけは task-completed が自動でターミナルサマリを出す（このスキルとは別経路）。

## Quick Reference

- 「**オーケストレーション活用度見せて**」→ HTML スコアカードを生成して開く
- 「**どのバックエンド使った**」「**Codex/Cursor どれだけ**」→ ターミナルサマリ
- 「**累計見せて**」「**自慢できるやつ**」→ HTML スコアカード（lifetime totals が主役）

## Deliverables

| 出力 | 生成物 |
|------|--------|
| HTML スコアカード | `scripts/orchestration-scorecard.sh --format html-data` → `scripts/render-html.sh --template orchestration` で単一 HTML |
| ターミナルサマリ | `scripts/orchestration-scorecard.sh --format terminal`（3-5 行） |

tri-state: `used`（count>0）/ `available`（設定済み未使用）/ `not-configured`（binary 不在＝中立、壊れではない）。
委譲ゼロなら "no delegations observed" に degrade。

## Execution

helper script は plugin bundle root から呼ぶ:

```bash
HARNESS_PLUGIN_ROOT="${HARNESS_PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}"
```

### ターミナルサマリ（`--terminal`）

```bash
bash "${HARNESS_PLUGIN_ROOT}/scripts/orchestration-scorecard.sh" --format terminal
```

3-5 行を要約してそのまま提示する。

### HTML スコアカード（既定 / `--out` / `--no-open`）

```bash
OUT="${1:-.claude/state/orchestration-scorecard.html}"   # --out <path> で上書き
bash "${HARNESS_PLUGIN_ROOT}/scripts/orchestration-scorecard.sh" --format html-data \
  | bash "${HARNESS_PLUGIN_ROOT}/scripts/render-html.sh" --template orchestration --data - --out "$OUT"
```

- `--no-open` 指定がなければ生成後にパスを提示し、ブラウザで開くよう案内する（自動 open は環境依存なのでパス提示を基本とする）
- redaction は使わない: scorecard データは構造的に非機密（カウント + backend 名 + repo basename + 時刻のみ）。no-secret 保証は上流の ledger 契約が担保する

## Related Skills

- `harness-progress` — 進捗ダッシュボード（タスク進捗。本スキルは backend 活用度に特化）
- `harness-work` / `breezing` — 実装（backend を実際に使う側）
