---
name: workflow-graph
description: 作業を 3 つの強連結成分（① design / ② build / ③ review）のグラフとして回す。調査・設計が要るタスクを始めるとき、決定を実装に移すとき、PR を人間のレビューに回すとき、「グラフで進めて」「/design」「/build」「/review」「台帳」に言及したときに使う。保存ワークフロー 3 本の呼び方（args の組み立て）、台帳 decisions / verify / review .json の書式、人間ノード（decide / human-op / human-review）での手順、SCC を抜ける・離脱する判定を定める。短い Q&A や自明な変更には使わない。
compatibility: Designed for Claude Code (saved workflows and hooks)
---

メインセッションは**オーケストレータ**であり、この規約に従って 3 つの SCC を渡り歩く。
SCC の内側（機械ノードの周回）は保存ワークフローが回し、**人間ノードと SCC 間の遷移だけ**が
メインセッションの仕事である。グラフの形は `docs/adr/0018`、制御の分担は `docs/adr/0020`、
機構の詳細は `docs/design/workflow-graph.md`（dotagents リポジトリ）。

## 用語

- **SCC**（強連結成分）: 互いに行き来できるノードの集合。① design（research / propose / critique / decide）、
  ② build（implement / verify-local / human-op）、③ review（verify-CI / 差分の提示 / human-review / fix）。
- **台帳**: SCC ごとに 1 枚の JSON。`decisions.json` / `verify.json` / `review.json`。抜ける条件はこれで判定する。
- **離脱**: SCC から ① へ戻ること。回数ではなく「同じものの再発」で判定する。

## 0. 入るかどうか（intake）

| 状況 | 行き先 |
|---|---|
| 事実や設計の選択肢が足りず、人間が決める必要がある | ① `/design` |
| 決定は済んでいて、実装と検証だけが残っている | ② `/build` |
| 他人の MR / PR のレビューを頼まれた | ③ `/review`（merge へは行かない） |
| 短い Q&A、1 ファイルの自明な修正 | グラフに入らない |

入ると決めたら台帳ディレクトリを作る: `<作業ツリー>/.claude/workflow-graph/<task>/`
（`<task>` は kebab-case。`.claude/` はこのリポジトリでは gitignore 済み）。
ワークフローの `args.ledgerDir` には**絶対パス**を渡す。報告ファイル（`research-N.md` / `propose-vN.md` /
`critique-vN.md` / `implement-rN.md` / `verify-rN.md` / `review-v1.md`）もここに溜まる。

保存ワークフローは**ユーザーが `/design` `/build` `/review` と指示したときに**呼ぶ
（委譲は手動指示のみ、の規則と同じ）。呼ぶときは `Workflow` ツールに `name` と下記の `args` を渡す。

### 起動前にモデルを聞く

ワークフローは**実行中にユーザー入力を受けられない**ので、モデルを選べるのは起動前だけ。
`/design` `/build` `/review` `/web-research` を呼ぶ**直前に、毎回** `AskUserQuestion` でそのワークフローの
ノードごとのモデルを確認し、答えを `args.models` に入れる。1 回の質問にノードを 1 つずつ並べ、各ノードの
選択肢は「既定（<既定値>）」を先頭に、`opus` / `sonnet` / `haiku` / 継承 を続ける。既定を選んだノードは
`args.models` に書かない（スクリプト側の既定に任せる）。

聞く対象と既定:

| ワークフロー | ノード（既定） |
|---|---|
| `/design` | research（opus ※）/ propose（継承）/ critique（継承）/ integrate（haiku）/ webResearch（全段階 opus。`kind: "web"` の小問があるときだけ） |
| `/build` | implement（sonnet）/ verify（sonnet ※） |
| `/review` | review（継承）/ refute（sonnet） |

※ 役割で動くノードの既定は `user/agents/<役割>.md` の `model:` が決める（researcher = opus、verifier = sonnet、
他は未指定 = 継承）。`args.models` で渡した値は呼び出しごとの指定として frontmatter に勝つ。
| `/web-research` 単独 | scope / search / fetch / verify / synthesize（すべて opus） |

`/web-research` は 1 回で 100 体前後・1,000 万トークン級になるので、モデルと一緒に**回してよいか**も
同じ質問で確認する。`maxDeepResearch` を 1 以上にするのはその答えがあったときだけ。

ユーザーが「既定でいい」「聞かなくていい」と言ったら、その指示があったセッション中は聞かずに既定で回す。

この skill をユーザーが先に叩く必要はない。プロンプトに `/design` `/build` `/review` `/web-research` が
含まれたターンに、`UserPromptSubmit` hook（`workflow-graph-state.sh`）がこの本文をそのまま注入する
（セッションにつき 1 回）。同じ指示は各ワークフローの `meta.whenToUse` にもある。そして
`PreToolUse` hook（`workflow-graph-guard.sh`）が、`args.models` の無い起動を拒否する。
既定のまま回すときも `"models": {}` を渡す（聞いた証拠）。

## 1. ① design

**`/design` の args**

```json
{
  "task": "<task>",
  "goal": "何を決めたいか（1〜3 文）",
  "constraints": ["制約"],
  "confirmed": [{"axis": "判断軸", "choice": "確定した選択", "reason": "根拠"}],
  "open": [],
  "reports": ["先行する報告・ADR・関連ファイルの絶対パス"],
  "researchQuestions": [
    "このリポジトリの事実を確かめる小問（文字列 = codebase）",
    {"question": "外部ツール・技術の仕様や比較を確かめる小問", "kind": "web"}
  ],
  "optionResearch": true,
  "maxDeepResearch": 0,
  "ledgerDir": "<絶対パス>",
  "maxRounds": 2,
  "models": {}
}
```

**モデルはノードごとに決まる**。役割で動くノードは役割ファイルの `model:` が既定（ADR 0021 で可能になった）、
役割ファイルの無いノード（implement / integrate / refute / web-research の各段階）はスクリプトが既定を持つ。既定は
「起動前にモデルを聞く」の表のとおり。`args.models` には起動前の質問で既定から変えたノードだけを
`{"research": "sonnet", "webResearch": {"verify": "sonnet"}}` のように部分的に渡す。

`confirmed` に入れた軸は再オープンされない。2 周目以降は前回の `decisions.json` の `confirmed` と
`open` をそのまま渡す。

**調査の振り分け**: 小問は並列に調べる。`kind: "codebase"`（既定）は `researcher`、`kind: "web"` は
`/web-research`（同梱 `/deep-research` の写しで、段階ごとにモデルを固定したもの。Web 検索を角度ごとに
並列 → 出典を照合 → 主張ごとに 3 票の反証投票）を `/design` の中から呼び、結果を researcher と同じ
報告形式に整形する。**1 回で 100 体前後のエージェントを回し、実測で 1,000〜1,400 万トークン・数時間
かかった**（2026-09-23 の追試、同梱版）。既定の `maxDeepResearch` は 0 で、**人間が明示的に数を渡した
ときだけ**回る。超過分は researcher（WebSearch 可）で代替される。回すときは PC をスリープさせない
（合成段階が「computer went to sleep」で失敗し、`resumeFromRunId` でもキャッシュが当たらず全再実行になった）。
単独で使うなら `/web-research` に質問を渡す（`args` は文字列か `{question, models}`）。同梱の
`/deep-research` はモデルを固定できないので使わない。

**案ごとの調査**: designer は 1 周目に「案を比べるのに足りない事実」を `researchNeeded`（案 / 小問 / 種別）
として返す。`optionResearch` が真なら同じ周で並列に調べ、designer が改訂してから critic に渡る。
人間の decide に届く `open` を減らすための、`decide → research` の戻りを先回りする仕組み。

**戻り値を台帳にする**: 戻り値の `confirmed` / `open` / `recommendation` / `options` / `fatalRemaining` /
`reports` / `stoppedBecause` を `decisions.json` に書く（`rounds` は累積で数える）。

**decide（人間ノード）**: `open` の各行を `AskUserQuestion` で 1 問ずつ聞く。`question` と `options` を
そのまま使う。答えが出た行は `open` から `confirmed` へ移す（`reason` に人間の言葉を残す）。
人間が「もう少し調べて」と言えば、その問いを `researchQuestions` にして `/design` を再実行する。
人間が新しい軸を出せば `open` に追加して再実行する。

**抜ける条件**: `open` が 0 件 → **record**（`madr-writer` で ADR を書く。`confirmed` がそのまま
Decision Outcome、`options` が Considered Options になる）→ ②へ。

**空転の判定**: 1 周（`/design` 実行 + decide）で `confirmed` が増えず、`open` にも新しい軸が
増えなかったら 1 回。**2 回続いたら**「打ち切るか、軸を分割するか」を人間に聞く。
`stoppedBecause` が `no-progress`（同じ致命的指摘が丸ごと残った）のときも同じ扱い。

## 2. ② build

**`/build` の args**

```json
{
  "task": "<task>",
  "decision": "何をどう実装するか（decisions.json の confirmed を文章にしたもの）",
  "adrPath": "<ADR の絶対パス>",
  "checks": [{"name": "pytest", "kind": "test", "command": "uv run pytest -q", "target": null}],
  "ledgerDir": "<絶対パス>",
  "prevCause": null,
  "notes": "実装者への補足",
  "maxRounds": 6,
  "models": {}
}
```

`checks` の `kind` は `test` / `build` / `bench` / `startup`。ベンチは `target` に目標値を書く。
CI でしか走らない項目はここに入れず、③ の verify-CI に委ねる。

**戻り値を台帳にする**: 戻り値の `status` / `items` / `sameCauseCount` / `lastCause` / `needsHumanOp` /
`reports` を `verify.json` に書く。

**status ごとの手順**

| status | 次にすること |
|---|---|
| `pass` | commit → push → PR。`gh pr create` は hook が `verify.json` 全 pass を確認する |
| `needs_human_op` | **human-op**: `needsHumanOp.command` と理由を人間に示し、`! <command>` で実行してもらう。結果を確認したら `/build` を再実行（`resumeFromRunId` を渡すと完了済みエージェントは再利用される） |
| `escape_design` | ① へ戻る。`lastCause` を新しい軸として `decisions.json` の `open` に追加し、`/design` を再実行する。実装は捨てない（差分はそのまま） |
| `backstop` / `*-failed` | 人間に状況を報告し、続けるか ① に戻すかを聞く |

2 回目以降の `/build` では、前回の `verify.json` の `lastCause` を `prevCause` に渡す。

## 3. ③ review

**`/review` の args**

```json
{
  "task": "<task>",
  "range": "main...HEAD",
  "description": "PR の説明",
  "confirmed": [ "decisions.json の confirmed" ],
  "adrPath": "<ADR の絶対パス>",
  "ledgerDir": "<絶対パス>",
  "verifyFindings": true,
  "models": {}
}
```

**戻り値を台帳にする**: 戻り値の `items`（各行 `status: "open"`）/ `dropped` / `mergeOpinion` /
`consistency` / `testsAssessment` / `reportPath` を `review.json` に書く。

**human-review（人間ノード）**: `items` を重要度順に人間に見せる（`file:line` と `fix` 付き）。
人間の答えで各行の `status` を更新する。

| 人間の答え | status | 次にすること |
|---|---|---|
| 直す | `fixed` | 自分で直す（小さければ main が直接、大きければ `/build` を `checks` 付きで再実行）。直したら CI を待つ |
| 自分で直した | `fixed` | 差分を確認して CI を待つ |
| 棚上げ | `deferred` | `br create` で beads issue にする（グラフが自己増殖する唯一の場所） |
| 却下 | `rejected` | 理由を行に残す |

**抜ける条件**: `status == "open"` が 0 件 → merge。`gh pr merge` は hook が `review.json` を確認する。
指摘が実装でなく**設計に及ぶ**（決定そのものが誤りだった）なら ① へ戻り、`open` に軸を足す。

他人の MR / PR のレビューでは `items` を指摘として返して終わる。merge や `verify.json` は要らない。

## 4. hook が何をするか

- `UserPromptSubmit`: 台帳があるタスクでは毎ターン `[workflow-graph] task=… scc=… 未確定 n / 未pass n / 未対応 n` を注入する。
  **この行を見て今どの SCC にいるかを判断する**。記憶に頼らない。
- `UserPromptSubmit`: プロンプトにワークフローのコマンド名があるターンに、この skill の本文を注入する
  （セッションにつき 1 回）。skill を叩き忘れても規約が載る。
- `PreToolUse`（Workflow）: `/design` `/build` `/review` `/web-research` を `args.models` 無しで起動
  しようとしたら拒否する。同梱 `/deep-research` は `/web-research` に誘導して拒否する。
- `PreToolUse`（Bash）: `gh pr create` は `verify.json` 全 pass、`gh pr merge` は `review.json` 未対応 0 を要求し、
  満たさなければ理由付きで拒否する。拒否されたら台帳を直すのが先で、hook を外す判断は人間がする。
- 台帳ディレクトリが無い作業には Bash 側は一切干渉しない。グラフを使わない作業は普段どおりでよい。

## 5. やってはいけないこと

- ワークフローの戻り値を台帳に書かずに次へ進む（hook も人間も現在地を見失う）。
- `confirmed` の軸を再オープンする。人間が確定したことは前提として扱う。
- 回数で SCC を打ち切る。離脱は「同じものの再発」でだけ判定する。
- 人間ノードを飛ばす。`decide` / `human-op` / `human-review` は必ず人間に返す。
