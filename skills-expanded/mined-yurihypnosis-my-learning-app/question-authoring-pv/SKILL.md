---
name: question-authoring-pv
description: 英語・句動詞（Speak-First 文産出ドリル、CAE C1 / IELTS 7.5 向け）の問題集に問題・解説を追加/修正するときの試験固有ルール（pv-* slug、意味クラスタのカテゴリ、日本語の場面＋レジスタータグの設問、直訳/粒子/レジスターの3種トラップ誤答）。「句動詞の問題を追加して」「PVセットを作って」「英語の問題集を作って」で使う。共通ルールは question-authoring スキルにある。
---

# 英語・句動詞（Speak-First 文産出ドリル）

**先に `question-authoring` スキル（共通ルール・適用手順）を読むこと。** ここは試験固有の情報だけ。
投入の順序・スケジュール・チャンク台帳の運用は `docs/pv-seed-strategy.md`（作戦側）を見る。

このファミリーだけの特殊事情: 資格の暗記ではなく**英文の産出**を鍛える。アプリの MCQ は再認エンジンなので、そのままでは「put off を見ればわかるが言えない」で止まる。対策は2つで、どちらも作問側の責任。

1. **Speak-First フロー（実装済み）**: `pv-` で始まる slug の科目は選択肢が強制非表示になり、3秒カウントの後「選択肢を表示」→ 解答後に「口では言えなかった」自己申告チップが出る（`isSpeakFirstSubject` / `src/lib/quiz/stats.ts`、フラグは `user_question_progress.last_spoken_ok`、false は苦手だけ演習に流入）。**選択肢を見る前に声に出して英作するのが学習行為で、MCQ は答え合わせ**。この前提を各 subject の description に必ず書く。
2. **誤答肢＝日本人がまさに作る失敗文**。ランダムな誤答は作らない（下記）。

## 科目（9セット・約200チャンク）

slug が `pv-` で始まることが Speak-First 発動条件。**`EXAM_ALIAS`（`src/lib/quiz/stats.ts`）に slug→`"pv"` のエントリが必要**（pv-t1-a〜pv-t3-d と pv-test は登録済み。セットを増やしたらコードにも足す）。

| slug | 名前 | 問題数 | 狙い |
|---|---|---|---|
| `pv-t1-a` `pv-t1-b` | 英語・句動詞（Set T1-A/B） | 各25 | 学術・フォーマル。IELTS Writing Task 2 / CAE essay |
| `pv-t2-a` `pv-t2-b` `pv-t2-c` | 英語・句動詞（Set T2-A/B/C） | 各20 | 議論動詞。Speaking Part 3 / CAE Speaking 3-4 |
| `pv-t3-a` 〜 `pv-t3-d` | 英語・句動詞（Set T3-A〜D） | 各22-23 | 日常・語り。Speaking 1-2 / Listening |

名前の「（Set T1-A）」表記は `examDisplayName` が剥がすので、メニューでは「英語・句動詞」1試験に束なる。25問≒ポモドーロ1本がセットの単位。

subject の description（テンプレ）:
「【Speak-First】日本語の場面を見たら、選択肢を見る前に3秒以内で英文を声に出す。言ってから表示。口で言えなかったら解答後にチップを押す。」

## source_ref

`pv-<tier><set>-q<NN>` ゼロ埋め2桁（例: `pv-t1a-q01` 〜 `pv-t1a-q25`）。

## カテゴリ＝意味クラスタ（粒子で分類しない）

**クラスタ内のメンバーは互いの誤答肢に使う** — 近縁語の弁別こそ C1 の技能。ティアごとに固定:

- **T1**: 原因・結果系（stem from, bring about, result in, account for）／実行・遂行系（carry out, set out, follow through）／除外・特定系（rule out, single out, point to）／依拠・構成系（draw on, build on, make up）／要約・帰着系（boil down to, come down to, add up to）
- **T2**: 主張・提起系（put forward, bring up, point out）／賛否・譲歩系（go along with, back up, hold out against）／検討・判断系（weigh up, think over, settle on）／継続・断念系（keep up, press on, back out）
- **T3**: 先送り・回避系（put off, get out of, back off）／開始・着手系（set off, take up, get down to）／関係・対立系（get along with, fall out, make up）／増減・変化系（go up, cut down on, turn into）／発覚・判明系（find out, turn out, come across）／感情・反応系（freak out, calm down, get over）— T3の元クラスタが5つで奇数のためセットに割り切れず、pv-t3-c で発覚・判明系の相方として追加した補助クラスタ

## 設問の形式

`question_text` ＝ **日本語の場面 ＋ レジスタータグ**。直訳文を設問にしない（直訳を見た瞬間、産出でなく翻訳になる）。

```
〔口語〕締め切りが近いのに、いちばん大変な作業を後回しにし続けている。どれが自然？
〔フォーマル・受動〕追加調査が終わるまで、その決定は先送りされたと報告書に書く。どれが自然？
```

- レジスタータグは 〔口語〕〔中立〕〔フォーマル〕〔フォーマル・受動〕 の4種
- 前の発話が要る場面は `code` 列に対話を置く（A: ... / B: ___）
- `question_type` は基本 `single`。「自然なものを**2つ**」のレジスター問題のみ `multi`

## 選択肢＝フル英文4つ（作る順番が命）

**誤答肢3つを先に書き、正解文を最後に書く。** 逆順だと長さ・構造が漏れる（正解だけ長い問題は共通スキルの長さリーク自己チェックで検出。**validate_seed.py という道具は存在しない** — 検証は共通スキルの SQL スニペット）。

誤答肢は毎問この3種（クラスタ内の近縁句動詞を最低1つ含める）:

1. **直訳トラップ** — 文法は正しいが和文英訳調で不自然（"I continue to postpone the most difficult task."）
2. **粒子ニアミス** — 動詞は正しいが粒子が違い、意味がずれる（put off → put away / put out）
3. **レジスターミス** — 実在する英語だが場面の格に合わない（フォーマル指定に "I keep putting off the hardest bit, mate."）

長さは正解±20%に揃える。誤答が自分の誤りを自白する文（"This is unnatural because..."）は書かない。

## explanation_data の流儀（このファミリーの再割当）

キーは `src/lib/quiz/types.ts` の `ExplanationData` のまま。意味だけ言語学習用に読み替える:

| キー | このファミリーでの中身 |
|---|---|
| `asked` | どの意味クラスタ・機能を試したか（「先送りを口語で自然に言えるか」） |
| `point` | 決め手1文。粒子のコアイメージかレジスター則（「off＝切り離して遠ざける→時間軸なら先送り」） |
| `kid` | チャンク＋最速の訳（「put off＝後回しにする。keep -ing と組んで『ずっと後回し』」） |
| `eg` | 追加の実例文1〜2本（正解文とは別の場面で） |
| `terms` | 分離可否・コロケーション（`[["put off the meeting / put the meeting off","分離可"], ["put it off","代名詞は必ず間に"]]`） |
| `think` | 想起手順: 場面→レジスター→動詞→粒子の順で選ぶ鎖 |
| `vs` | **トラップ解剖（最重要・必須級）**: 直訳がなぜ不自然か、粒子違いの意味、レジスターのずれ。位置(A/B/C/D)でなく**内容で**指す（共通スキルの位置参照禁止） |
| `why_asked` | CAE Use of English Part 1 / IELTS Lexical Resource でどう問われるか |
| `usecase` | Speaking / Writing での実戦投入場面 |
| `opt` | 選択肢別注。選択肢と同数・同順。正解は「正解。」で始める |

`snippet` は原則使わない（コードではないので）。対話の前提は `code` 列。

## セット間再登場ルール（再認つぶし）

同じチャンクは**場面・レジスター・トラップを全部変えたときだけ**別セットに再登場できる。例: put off は T3-a では口語の先延ばし、T1-b では "the decision was put off pending further review"（フォーマル受動）。同一表面文の複製は禁止。セットAの暗記でセットBが解けたら作問の負け。

## 適用と検証

共通スキルどおり `db.sh apply` → 件数と `opt` 充足の確認 → **長さリーク SQL** → 位置参照が無いことを確認。加えてこのファミリー固有:

```bash
# クラスタ内近縁語が誤答に入っているかは目視レビュー（自動化なし）
# multi 問題の correct_indices 充足
db.sh query "select source_ref from public.questions q join public.subjects s on s.id=q.subject_id
  where s.slug like 'pv-%' and q.question_type='multi' and q.correct_indices is null;"
```

## 内容の注意

- 素材はハーベスト済みの実文（GCP docs・podcast 由来）を優先。裸の動詞から作文しない
- 「done」の基準は本人の口頭3秒×2日×2場面。クイズ正答率は指標にしない — 作問側は場面の多様性でこれを支える
- 1セット25問以内を厳守（1ポモドーロ＝1セットの単位を崩さない）
