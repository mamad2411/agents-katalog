---
name: failure-codifier
description: "Extract recurring failure patterns from breezing orchestration logs and Judgment Ledger, emit failure-rule.v1 proposals with confidence scores. SSOT promotion to patterns.md or decisions.md is proposal-only — human-approval-required. Use when user mentions failure codifier, failure patterns, self-learning loop, codify failures, or failure-rule proposals. Do NOT load for: direct SSOT edits, auto-promotion, or implementation unrelated to failure analysis."
description-en: "Extract recurring failure patterns from breezing orchestration logs and Judgment Ledger, emit failure-rule.v1 proposals with confidence scores. SSOT promotion to patterns.md or decisions.md is proposal-only — human-approval-required. Use when user mentions failure codifier, failure patterns, self-learning loop, codify failures, or failure-rule proposals. Do NOT load for: direct SSOT edits, auto-promotion, or implementation unrelated to failure analysis."
description-ja: "breezing ログと Judgment Ledger から再現失敗パターンを抽出し、confidence 付き failure-rule.v1 候補を提案する。patterns.md / decisions.md への昇格は human-approval-required（自動昇格禁止）。Use when user mentions failure codifier, 失敗パターン, self-learning loop, codify failures. Do NOT load for: SSOT 直接編集, 自動昇格."
allowed-tools: ["Read", "Bash", "Grep"]
argument-hint: "[propose|explain]"
user-invocable: true
---

# Failure Codifier

breezing orchestration ledger + Judgment Ledger から再現失敗を **read-only** で抽出し、`failure-rule.v1` 候補を confidence score 付きで提案します。

## 核心契約

- **human-approval-required**: codifier は dry-run 提案のみ。`patterns.md` / `decisions.md` への自動昇格は構造的に禁止。
- Confidence 閾値: occurrence **count ≥ 3 → medium**、**count ≥ 5 → high**（`go/internal/failurecodifier/confidence.go`）。
- 昇格先 heuristic: `proposed_ssot_target` フィールドで `patterns.md` または `decisions.md` を**提案するのみ**。

## 使い方

### Dry-run 提案（推奨）

```bash
./scripts/failure-codifier-propose.sh --dry-run
```

stdout は JSON 配列（`failure-rule.v1` 候補）。SSOT ファイルには一切書き込みません。

### Go テスト

```bash
cd go && go test ./internal/failurecodifier/... -count=1
```

## 参照

- 昇格ワークフロー: [references/promotion-workflow.md](${CLAUDE_SKILL_DIR}/references/promotion-workflow.md)
- Schema: `templates/schemas/failure-rule.v1.json`
- Core: `go/internal/failurecodifier/`

## 禁止事項

- `patterns.md` / `decisions.md` への Write / Edit（human 承認後も codifier 経由では不可）
- `AutoPromote` / unattended SSOT 更新
- Plans.md の `cc:*` マーカー変更
