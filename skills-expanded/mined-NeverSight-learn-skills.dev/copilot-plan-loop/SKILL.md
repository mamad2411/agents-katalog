---
name: copilot-plan-loop
description: |
  設計プランをCopilot CLIレビューで反復改善するループ。プラン作成→Copilotレビュー→FB反映→再レビューを収束まで繰り返す。
  --model でレビューモデル、--effort で推論レベルを指定可能。
  Use for: "copilot-plan-loop", "Copilotとプラン練る", "設計レビューループ(Copilot)", "プラン精度上げて(Copilot)"
user-invocable: true
---

# Plan Review Loop (Copilot)

設計プランをCopilot agentにレビュー依頼し、フィードバックを反映して再レビューする反復ループ。

## When NOT to use

- 単発レビューで十分なとき → `/copilot-review` (loop なし)
- 実装コードのレビュー対象 → `/copilot-review-loop`
- Codex CLI を使いたい → `/plan-loop`
- プランがまだ存在しない (作成は通常会話で進める)
- モデル比較が不要なら → `/plan-loop` (Codex 固定の方が軽い)

## Pitfalls (read first)

| Symptom | Cause | Fix |
|---|---|---|
| `--model` を変えても結果が同じ | argparse で model が agent に伝わっていない | Step 2 のテンプレで `{model}` を埋めているか確認 |
| `--effort high` で response が異常に遅い | high は推論コストが大きい。レート制限に達することも | medium にフォールバック、または target を絞り込む |
| 同じ指摘が毎ラウンド出る | history が次ラウンド prompt に渡っていない | `{previous_feedback_and_responses}` を必ず埋める |
| MUST が永遠にゼロにならない | reviewer が plan の最新版を読めていない | `plan_path` を絶対パスで渡す。`--model` を強モデルに変えて再試行 |
| Copilot の出力が日本語にならない | model によっては日本語指示が弱い | テンプレ末尾「日本語で回答してください」を維持。それでも英語なら model 変更 |

## Usage

```
/copilot-plan-loop                           # 会話中のプランを対象にループ開始
/copilot-plan-loop path/to/plan.md           # 指定ファイルを対象
/copilot-plan-loop --model gpt-5 plan.md     # GPT-5でレビュー
/copilot-plan-loop --model claude-opus-4.6   # Claude Opusでレビュー
/copilot-plan-loop --effort high plan.md     # 高推論レベルでレビュー
```

## Workflow

```python
plan = resolve_plan(args or conversation_context)
files = extract_related_files(plan)
model = parse_model_arg(args)    # None if not specified
effort = parse_effort_arg(args)  # None if not specified
round = 0
history = []

while True:
    round += 1
    review = copilot_review(plan, files, history, model, effort)
    must, should, nice = classify(review)
    report_to_user(round, must, should, nice)

    if not must and not should:
        break
    if user_wants_to_stop():
        break

    approved = ask_user_which_to_address(must + should)
    apply_feedback(plan, approved)
    history.append((review, approved))

print_summary(history)
```

## Step 1: プラン準備

プランファイルを特定する。引数があればそのパスを使用。なければ会話コンテキストから直近のプランファイルパスを探す。

プランが存在しない場合はユーザーに確認してから作成を支援する。

## Step 2: Copilot レビュー依頼

Task tool で copilot agent を起動。プロンプトに含める内容:

1. プランファイルのパス（Copilotに読ませる）
2. レビュー対象の関連ソースファイル一覧
3. レビュー観点の指定
4. 前回のレビュー結果と対応内容（2回目以降）
5. `--model` が指定されていればモデル指定
6. `--effort` が指定されていれば推論レベル指定

レビュープロンプトのテンプレート:

### 初回

```
以下の設計プランをレビューしてください。

## プランファイル
{plan_path} を読んでください。

## 関連ソースファイル
{file_list}

## レビュー観点
1. 設計: アーキテクチャの適切さ、責務分離
2. パフォーマンス: ホットパス、メモリ、計算量
3. スレッド安全性 / 並行性
4. 後方互換性: 既存の動作を壊さないか
5. テスト戦略: カバレッジの十分さ
6. エッジケース: 見落としている境界条件

## 出力形式
指摘を重大度で分類:
- [MUST] 対応しないとバグ・障害に直結
- [SHOULD] 対応すると品質が上がる
- [NICE] あると良いが必須ではない

日本語で回答してください。
```

### 2回目以降

```
前回の指摘への対応を反映したプランを再レビューしてください。

## プランファイル
{plan_path} を読んでください。

## 前回の指摘と対応状況
{previous_feedback_and_responses}

## レビュー依頼
1. 前回の指摘が適切に解消されているか確認
2. 対応により新たに生じた問題がないか確認
3. 残存する懸念点があれば指摘

同じ出力形式 ([MUST] / [SHOULD] / [NICE]) で回答してください。
日本語で回答してください。
```

## Step 3: FB 分類

Copilot の回答から指摘を抽出し、重大度別に整理:

```
Round N レビュー結果:
  MUST:   X件 — {一覧}
  SHOULD: X件 — {一覧}
  NICE:   X件 — {一覧}
```

ユーザーに結果を報告し、対応方針を確認する。

## Step 4: プランに反映

ユーザーの承認を得た MUST + SHOULD 項目をプランに反映する。
各指摘に対して、プランのどの箇所をどう変更したかを追跡する。

## Step 5: 収束判定

以下のいずれかで終了:
- MUST と SHOULD が両方 0 件
- ユーザーが終了を指示

終了時、全ラウンドのレビュー結果サマリーを報告:

```
## Plan Review Summary (Copilot: <model>)

| Round | MUST | SHOULD | NICE |
|-------|------|--------|------|
| 1     | 3    | 5      | 2    |
| 2     | 2    | 3      | 1    |
| 3     | 0    | 1      | 0    |
| 4     | 0    | 0      | 0    |

対応済み: X件 / 未対応 (NICE): X件
```

## Anti-patterns

| 合理化 | 実像 |
|---|---|
| 「`--model gpt-5` の方が常に良い」 | モデル特性で得意領域が違う。観点ごとに使い分ける |
| 「`--effort high` を毎回つける」 | コストとレイテンシが跳ねる。MUST 出尽くした後の確認用に温存 |
| 「ユーザー承認をスキップして自動反映」 | プランが意図せず歪む。承認は省略しない |
| 「2 ラウンドで MUST が出なかったから収束」 | 評価軸が偏っている可能性。観点 6 つすべてカバーされたか確認 |
| 「Copilot に任せれば中立な評価が出る」 | Copilot も prompt 設計の影響を受ける。テンプレを変えたら評価軸が揺れる |

## Related skills

- `/plan-loop` — 同じワークフローを Codex CLI で実施
- `/copilot-review-loop` — 実装コードを Copilot でループ (plan ではなく code)
- `/refactor-loop` — メトリクス駆動の構造改善ループ (CodeHealth 系、別系統)
- `/copilot-review` — このスキルの単発レビュー版 (loop なし)
- `/dual-review` — Claude + Copilot の単発統合レビュー
- `empirical-prompt-tuning` (mizchi) — このスキル自体の品質を bias-free に評価

## Notes

- Copilot agent は `subagent_type: copilot` で起動する
- `--model` が指定されていれば、copilot agent への指示に含める
- `--effort` が指定されていれば、copilot agent への指示に含める
- 各ラウンドの Copilot レビュー結果は次ラウンドのプロンプトに含め、同じ指摘の繰り返しを防ぐ
- NICE 項目は対応を強制しない。ユーザー判断に委ねる
