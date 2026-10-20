---
name: cost-route
description: Claude のコストを下げる作業ルーティング規程。タスクをモデル階層(Haiku/Sonnet/Opus)と実行経路(Claude Code内 / Kimi委譲 / Claude API直叩き)に振り分け、重いものだけ高い経路に流す。月次コストは cost-report.js で可視化。デフォルトが opus[1m]+xhigh の環境で「軽い作業に重いモデルを払い続ける」浪費を止めたいとき、セッション冒頭や重い作業の前に使う。
origin: user
---

# cost-route (コストを下げる作業ルーティング)

現環境のデフォルトは **`opus[1m]` + `effortLevel: xhigh`**(最重量・非変更方針)。この規程は「軽い作業まで最重量で払う」浪費を止める。方針=**既定は据え置き、タスクに応じて手動で軽い経路へ切り替える**。

## まず前提を確認(重要)

**節約の効き方はプラン依存**:
- **従量(API credits)**: トークン/モデルを下げれば**実請求が下がる**。直叩き経路が効く。
- **サブスク定額(Max等)**: 実額は固定。下げても請求は変わらないが、**利用上限への到達リスク**と**notionalコスト**が下がる。直叩き(従量)へ出すのは、定額の上限に当たっているときだけ得。

`node ~/.claude/scripts/cost-report.js` の値は **notional(素の API 従量換算)**。実請求ではない。まず自分のプランを踏まえて解釈する。

## 3 階層 × 3 経路で振り分ける

### モデル階層(何を使うか)
| 階層 | 使いどころ |
|---|---|
| **Haiku** | 決定的・低リスクの機械作業: フォーマット、定型変換、ログ要約、分類、doc 更新、コメント解析 |
| **Sonnet** | 実装・リファクタ・レビューの主戦力。多くの作業はここで足りる |
| **Opus** | アーキ判断、深い原因調査、多ファイル不変条件、曖昧要件の分解。**ここぞだけ** |

### 実行経路(どこで走らせるか)
| 経路 | 使いどころ | 切替 |
|---|---|---|
| **Claude Code 内** | 対話的な作業。文脈が要るもの | `/model haiku` `/model sonnet` `/model opus` で都度切替 |
| **Kimi 委譲** | 実装・リファクタの一括処理(トークン節約) | `~/.claude/bin/ask-kimi`(対象リポジトリ直下から) |
| **Claude API 直叩き** | 重い反復ジョブ。Claude Code の巨大 context overhead を捨て、prompt caching を効かせる(Batch API はラッパー未実装=現状は同期1発) | `~/.claude/bin/ask-claude`(要 `ANTHROPIC_API_KEY`) |

## 判断ヒューリスティック(セッション冒頭 or 重い作業前)

1. **軽い定型か?** → `/model haiku` に落とす。または ask-kimi へ委譲。
2. **実装・リファクタか?** → Sonnet で足りる。大きければ ask-kimi(委譲でメイン文脈を汚さない)。
3. **深い判断・原因調査・多ファイル不変条件か?** → Opus に上げる。ただしこの turn だけ。終わったら下げる。
4. **重い反復・バッチ(同型を大量)か?** → ask-claude で直叩き(`--system` を共有して caching)。Claude Code の overhead を払わない。※ Batch API による一括 50%off はラッパー未実装(将来 `/v1/messages/batches` 対応予定)。
5. 迷ったら [[fable]] Phase 0 の「完了条件」を書く。判断の重さ=モデルの重さ。

**原則: 上げるのは一時的、既定は軽い経路。** Opus に上げたまま軽作業を続けない。

## 可視化と閾値

```bash
node ~/.claude/scripts/cost-report.js                 # 全月サマリ(モデル別)
node ~/.claude/scripts/cost-report.js --month 2026-07 # 当月内訳
node ~/.claude/scripts/cost-report.js --threshold 40  # 当月が閾値超なら警告
```
`~/.claude/scripts/hooks/cost-tracker.js` は Stop フック配線で使用量を取得できず**空回り(全行ゼロ)**。信頼せず、上の cost-report を使う。

## 関連
- [[fable]] — 判断の重さを見積もる土台(Phase 0 の完了条件)。
- [[agentic-engineering]] / `/model-route` — モデル階層の一般則。
- ラッパー: `~/.claude/bin/ask-kimi`(実装委譲)/ `~/.claude/bin/ask-claude`(API直叩き)。
- subagent の階層: 軸ワーカー(doc-updater 等)は `model: haiku`、実装/レビューは sonnet、深い分析は opus。
