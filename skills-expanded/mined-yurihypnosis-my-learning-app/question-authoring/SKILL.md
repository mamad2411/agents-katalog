---
name: question-authoring
description: この学習アプリの問題集に問題・解説を追加/修正するときの共通ルール（DBスキーマ、explanation_data の書き方、本番への適用手順、検証）。試験固有の情報は question-authoring-<試験> スキルにあるので、そちらを併せて読む。「問題を追加して」「解説を厚くして」「新しい問題集を作って」で使う。
---

# 問題・解説オーサリング（共通）

試験固有のカテゴリ名・source_ref 形式・解説の流儀は **試験別スキル**にある。必ず両方読むこと。

| 試験 | スキル |
|---|---|
| GCP ACE | `question-authoring-gcp-ace` |
| GCP PCA | `question-authoring-gcp-pca` |
| GCP PCDE (DevOps) | `question-authoring-gcp-pcde` |
| Terraform Associate | `question-authoring-terraform` |
| DCA (Docker) | `question-authoring-dca` |
| GH-200 (GitHub Actions) | `question-authoring-gh200` |
| CTAL-TA (ISTQB) | `question-authoring-ctal-ta` |
| G検定 (JDLA) | `question-authoring-g-kentei` |
| E資格 (JDLA) | `question-authoring-e-shikaku` |
| 英語・句動詞 (Speak-First) | `question-authoring-pv` |
| 統計学の基礎（図解ドリル） | `question-authoring-stats` |
| Linuxの教科書（図解ドリル） | `question-authoring-linux` |
| KCNA (Kubernetes and Cloud Native Associate) | `question-authoring-kcna` |

新しい試験を足すときは、既存の試験別スキルを雛形にして 1 枚追加する。

**50問を超える量産は、サブエージェント並列（作問と監査を別人に分ける）の型が確立済み。** `question-authoring-stats` の「大量生産の型と教訓」を読んでから発注書を書く（76問を21エージェント・24分で量産し、機械チェックで拾えない事実誤りを監査側が7セット全部で検出した実績）。

**解説を「わかりやすく」する作業は `explanation-clarity` スキルを読む。** たとえ(eg)・決め手(point)・前提ゼロ接地など、世界一わかりやすくするための方法論と、`opt` 整合・位置参照回避の実務がまとまっている。

## 大前提

- **本番 Supabase が唯一の DB。** ローカル DB もステージングも無い。書いた SQL はそのまま本番に当たる。
- **`supabase db push` は使わない。** `supabase/migrations/` には適用済みと未適用が混在しており、push は履歴を壊す。適用は必ず下記スクリプトで行う。
- anon key は読み取り専用。書き込みは Management API（keychain の CLI トークンを使用）。

```bash
.claude/skills/question-authoring/scripts/db.sh query "select ..."   # 確認用
.claude/skills/question-authoring/scripts/db.sh apply path/to.sql    # 適用
```

## 手順

### 1. 現状を DB で確認する（推測しない）

`docs/` や過去の SQL ファイルは古いことがある。カテゴリ名も問題数も、必ず DB に聞く。

```bash
db.sh query "select c.name, count(q.id) from public.categories c
  join public.subjects s on s.id = c.subject_id
  left join public.questions q on q.category_id = c.id
  where s.slug = '<slug>' group by 1 order by 1;"

db.sh query "select source_ref, left(question_text, 60) from public.questions q
  join public.subjects s on s.id = q.subject_id
  where s.slug = '<slug>' order by source_ref;"
```

### 2. 重複を避ける

既存の問題文・選択肢とほぼ同じものは足さない。同じテーマを別角度・別難易度で問うのは可。手順 1 の一覧に目を通してから書く。

### 3. SQL を書く

ファイル名は 2 パターン。新規の問題追加は前者。

- 問題の追加 : `supabase/migrations/000<N>_seed_<slug>.sql`（`<N>` は既存の最大 +1）
- 既存の更新 : `supabase/migrations/add_<内容>_<slug>_<YYYYMMDD>.sql`

```sql
BEGIN;

INSERT INTO public.questions
  (subject_id, category_id, source_ref, question_text, code, options,
   correct_index, correct_indices, question_type, explanation, explanation_data, initial_wrong_weight)
SELECT s.id, c.id, v.source_ref, v.question_text, v.code, v.options::jsonb,
       v.correct_index, v.correct_indices::jsonb, v.question_type, '', v.explanation_data::jsonb, 1
FROM public.subjects s
JOIN public.categories c ON c.subject_id = s.id
JOIN (VALUES

  ('<source_ref>', '<カテゴリ名>',
   '問題文',
   NULL::text,        -- code: 問題文に見せるコードがあれば文字列、無ければ NULL
   '["選択肢A","選択肢B","選択肢C","選択肢D"]',
   0,                 -- correct_index（0 始まり。multi では正解の先頭を入れる）
   '[0]',             -- correct_indices（multi なら '[0,2]'）
   'single',          -- 'single' | 'multi'
   '{"asked":"...","think":"...","vs":"...","opt":["...","...","...","..."]}'),

) AS v(source_ref, category_name, question_text, code, options,
       correct_index, correct_indices, question_type, explanation_data)
  ON c.name = v.category_name AND s.slug = '<slug>'
ON CONFLICT (subject_id, source_ref) DO NOTHING;

COMMIT;
```

既存問題への項目の後付けは、既存キーを消さないよう `||` でマージする。

```sql
UPDATE public.questions q
SET explanation_data = q.explanation_data || jsonb_build_object('snippet', v.value)
FROM jsonb_each_text('{"<source_ref>": "<値>"}'::jsonb) AS v(key, value)
WHERE q.source_ref = v.key
  AND q.subject_id = (SELECT id FROM public.subjects WHERE slug = '<slug>')
  AND q.explanation_data IS NOT NULL;
```

### 4. 適用して検証する

```bash
db.sh apply supabase/migrations/000NN_seed_<slug>.sql

# 入った件数とキーの充足を必ず確認する
db.sh query "select count(*) total,
  count(*) filter (where explanation_data ? 'opt') with_opt
  from public.questions q join public.subjects s on s.id=q.subject_id
  where s.slug='<slug>';"
```

UI での見え方まで変えた場合（新しい explanation_data のキーを足したときなど）は、`npm run dev` で実際に 1 問解いて解説の描画を確認する。**キーを足しただけでは画面には出ない** — `RichExplanation`（`src/app/(main)/learning-app.tsx`）に描画コードが要る。

## 選択肢の作り方（既存データが盛大に外している所）

**問題文を読まずに正解が当てられる問題を作らない。** 既存 1297 問のうち **981 問（76%）は「一番長い選択肢」を選ぶだけで正解できる**（偶然なら 25%）。新しく足す問題でこれを増やさない。

書いたら必ず自問する: **知識ゼロの人がこの4択を見て、正解を絞り込めてしまわないか。**

### やってはいけない

- **正解だけ長い・詳しい。** 正解に根拠や条件を盛り、誤答を短く済ませる。最大の癖。誤答も同じ密度・同じ長さで書く
- **誤答が自分の誤りを自白する。** 「〜を深く考えずに単純に2倍しただけの数である」「〜を混同してしまっている」。なぜ誤りかは `opt`（解説）に書く。**選択肢には書かない**
- **正解にだけ括弧の補足を付ける。** 「約83%（(30+15+5)÷60）」→ 計算式は `opt` へ。選択肢は「約83%」だけにする
- **投げやりな誤答。** 「目視で確認」「何もしない」「追加調査は行わない」「暗号化すれば検出不要」。誰も選ばない選択肢は 4 択を実質 2 択に縮める

### そうではなく

誤答は**現場で実際に選ばれる、もっともらしい間違い**にする。理想は「その分野を半分わかっている人が引っかかる」もの。

- 数値問題 : ありがちな誤計算の結果を置く（母数の取り違え、2倍、2乗、足し算と掛け算の混同）。値だけを並べ、根拠は書かない
- 概念問題 : 「技術的には動くが要件のどれかを壊す案」「一世代前の正解」「隣接サービスの機能」
- 長さは揃える。正解が 60 字なら誤答も 50〜70 字に収める

### 解説で選択肢を位置（A/B/C/D）で呼ばない

**アプリは出題時に選択肢をシャッフルする**（`shuffleOptions` / `src/lib/quiz/selection.ts`）。`correct_index` と `opt` は追従して付け替わるが、`asked` / `think` / `vs` / `explanation` の自由文に「選択肢Bは過剰装備」と書くと表示と食い違う。

コードはこれを検知して**その問題だけシャッフルを止める**。つまり位置参照を書くと、**その問題は DB の並び順のまま出続け、正解位置が固定される**（既存データはほぼ全問 `correct_index=0` なので、事実上「答えは常にA」になる）。安全側に倒す実装だが、書く側が気をつければ起きない。

- ✗ 「選択肢Aは過剰装備」「正解はC」
- ○ 「Cloud Interconnect との組み合わせは過剰装備」（**内容で指す**）

括弧内の1文字も誤検知される。`(C)(R)(U)(D)` のような略号は `(Create)(Read)…` と綴る。

なお `correct_index` が 0 に偏ること自体はシャッフルが吸収するので、無理に散らさなくてよい。**位置参照を書かないことのほうが重要。**

### 自己チェック

適用後に必ず走らせる。正解が単独最長になっていたら書き直す。

```bash
db.sh query "
with x as (
  select q.source_ref, length(q.options->>q.correct_index) as clen,
    (select max(length(value)) from jsonb_array_elements_text(q.options)
      with ordinality o(value,i) where o.i-1 <> q.correct_index) as dmax
  from public.questions q join public.subjects s on s.id=q.subject_id
  where s.slug='<slug>' and q.question_type='single')
select source_ref, clen, dmax from x where clen > dmax order by clen-dmax desc;"
```

## explanation_data のスキーマ

`src/lib/quiz/types.ts` の `ExplanationData` と一致させること。片方だけ足しても表示されない。

| キー | 必須 | 内容 |
|---|---|---|
| `asked` | ○ | 何を問うているか。1 文 |
| `why_asked` | | なぜ試験に出るか。作問者の意図・受験者が落ちる思考の癖 |
| `kid` | | ざっくり言うと。噛み砕いた 1〜2 文 |
| `terms` | | キーワード。`[["用語","説明"], ...]` を 2〜4 個 |
| `think` | ○ | 考え方。解法の流れ |
| `calc` | | 手で計算してみる。小さい数字で全ステップを1行1手で（等幅・縦積み描画）。書き方は question-authoring-stats の「計算系解説の3段ロケット」 |
| `snippet` | | 正しい書き方。コード/コマンドの模範解答。`<pre>` で等幅描画される |
| `eg` | | たとえると。身近な比喩 |
| `vs` | | 混同ポイント。紛らわしい選択肢との違い |
| `opt` | | 選択肢の解説。**選択肢と同数**。正解は「正解。」で始める |

`code`（questions の列）と `snippet`（explanation_data 内）は別物。

- `code` … 問題文と一緒に出る。これを読んで解く題材
- `snippet` … 解答後の解説に出る。模範解答

## つまずきどころ

- `ON CONFLICT (subject_id, source_ref)` は複合ユニーク制約。`(source_ref)` 単体は不可
- カテゴリ名は完全一致で `JOIN`。1 文字でも違うと**その行が黙って落ちる**（エラーにならない）。適用後に件数を数えて確かめる
- SQL 文字列内のシングルクォートは `''` にエスケープ
- `terms` は配列の配列。オブジェクトではない
- `question_type='multi'` では `correct_indices` を必ず入れる
- 全キーを全問に付けなくてよい。`snippet` はコードで示す価値のある問題にだけ付ける（概念問題に無理に付けない）
