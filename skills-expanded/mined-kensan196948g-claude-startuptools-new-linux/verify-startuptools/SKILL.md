---
name: verify-startuptools
description: StartUpTools リポジトリの検証ループ — bash 構文チェック・bats/node テスト・テンプレート整合性を実行し、失敗を修正して再実行する。lib/ libexec/ scripts/ Claude/templates/ の変更後、および commit・PR 作成前に使用する。
---

# 🔁 verify-startuptools — 本リポジトリの検証ループ

本リポジトリ（Claude-StartUpTools-New-Linux）への変更を「実装しただけ」で終わらせず、
全チェック PASS まで 検出 → 修正 → 再実行 を繰り返す検証ループです。

## ✅ チェック一覧（この順で実行）

### 1. bash 構文チェック

```bash
bash -n start.sh
for f in lib/*.sh libexec/*.sh; do bash -n "$f" || echo "SYNTAX FAIL: $f"; done
```

`shellcheck` が利用可能な場合は変更したファイルに対して併用する（warning は報告のみ、error は修正）。

### 2. ユニットテスト

```bash
npm run test:bats   # bats tests/bats/unit/
npm run test:node   # node --test scripts/**/*.test.js
```

- 変更に対応するテストが存在しない場合は、テスト追加を検討してから次へ進む。
- main 由来の既存失敗（自分の変更と無関係と確認できたもの）は BLOCKED として明記し、修正対象へ含めない。

### 3. テンプレート整合性

```bash
bats tests/bats/unit/goal-inject.bats   # v10: verify-goal-set.js は廃止 (native /goal)
```

- `Claude/templates/claude/START_PROMPT.md` の必須キーワード欠落警告を確認する。
- `Claude/templates/claude/CLAUDE.md` が 100 bytes 以上であること（template-sync のサイズガードと同一基準）。

### 4. 正本・テンプレートの二重管理同期

`.claude/claudeos/skills/` と `Claude/templates/claudeos/skills/` のように正本と配布テンプレートが
対で存在するファイルを変更した場合、両方が同期していることを diff で確認する。

```bash
diff -rq .claude/claudeos/skills/ Claude/templates/claudeos/skills/ | head -20
```

### 5. secret 露出確認

変更差分に secret・credential・token・connection string が含まれていないことを確認する。

## 🔁 ループ規則

1. 失敗したチェックは原因を特定し、修正して**該当チェックのみ**再実行する
2. 修正が他のチェック対象に影響した場合は、影響範囲のチェックも再実行する
3. 同一チェックが 3 回の修正で解消しない場合は BLOCKED とし、原因分析と選択肢を報告して停止する
4. 環境要因で実行できないチェックは成功扱いにせず NOT RUN として理由を記載する

## 📊 報告形式

```text
| チェック | 結果 | 備考 |
|---|---|---|
| bash -n 構文 | PASS | - |
| test:bats | PASS | 34 files |
| test:node | PASS | - |
| テンプレート整合性 | FAIL→PASS | キーワード欠落を修正 |
| 正本・テンプレ同期 | PASS | - |
| secret 露出 | PASS | - |
```

## 🔗 チェーン連携

- `/cto-session-start` の Build フェーズ末尾から呼ばれる（embedded）
- commit・Draft PR 作成の直前に standalone で実行する
- WebUI へ影響する変更時は続けて `/webui-health-check` を実行する（chained）
