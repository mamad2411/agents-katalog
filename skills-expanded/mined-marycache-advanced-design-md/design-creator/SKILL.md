---
name: design-creator
description: |
  ヒアリング駆動でデザイン仕様書（DESIGN.md）を作るスキル。
  「コーポレートサイト作りたい」「LP のデザイン考えて」「ポートフォリオの世界観決めたい」
  「ファンタジーゲームみたいな公式サイト作りたい」など、用途・雰囲気・世界観の相談時に使用。
  静的 HTML クイズで意図を抽出し、Intent / Colors / Typography / Animations を含む DESIGN.md を生成。
  既存 DESIGN.md からの HTML モック生成や、URL からの抽出には使用しない（後者は design-extractor の役割）。
---

# design-creator

ユーザーの曖昧な「こういうサイトが作りたい」を、機械可読な DESIGN.md に翻訳するスキル。
**過去のデザイン抽出データに依存せず**、設問プールと辞書（lexicon）だけで動作する。

---

## コア原則

1. **Intent-first** — Use / Mood / 第一印象軸 / Target / 差別化軸を先に確定します。色やフォントはその後で決定します
2. **lexicon 厳守 + 全文保存** — 色・フォント・アニメは `references/lexicon/` から選定します。lexicon 外は `[要確認]` で残します。クイズの全設問・全選択肢・回答は完全保存して AI に渡します（「選ばれなかった選択肢」も判断材料です）。**例外**: Step 9 で design-extractor を呼んで戻った場合のみ、抽出済み INTERPRETED.md の値も lexicon と同格に扱えます（source コメント必須）
3. **配布性の死守** — 私的データ・外部 CDN・画像 URL に依存しません。`references/` 内だけで完結させます

---

## 初回チェック: 推奨権限

セッション内で本スキルを **初めて呼ぶ時のみ** 実施します（2 回目以降はスキップ）。

```bash
grep -q "python3 -m http.server" ~/.claude/settings.json 2>/dev/null && echo INSTALLED || echo MISSING
```

`INSTALLED` ならスキップして Step 1 へ進みます。

`MISSING` の場合、ユーザーに **1 度だけ** 以下を提案します（`lang=en` 指定時は英語で提示）:

```
本スキル群は mkdir / cp / python3 -m http.server / (Step 9 で) npm install / npx playwright install
などを自動で実行します。そのままだと毎回 "Do you want to proceed?" 確認が表示されます。

リポジトリ同梱の settings.recommended.json を ~/.claude/settings.json の permissions.allow に
マージすると、これらの安全なコマンドのみ確認なしで通るようになります。

マージしますか？ (yes / no / 後で)
- yes: 自動でマージして以降のプロンプトを抑制します
- no:  以降このセッションでは再提案しません
- 後で: 今回はスキップし、次回セッションで再度確認します
```

`yes` の場合、後述の **設定ファイルの解決手順** に従ってリポジトリの `settings.recommended.json` を読み込み、`~/.claude/settings.json` の `permissions.allow` 配列に **未登録の項目だけ** 追記します（重複させない）。`~/.claude/settings.json` が存在しない・JSON として不正な場合は手動マージを案内し、スキルは停止しません。

`no` / `後で`: 即座に Step 1 へ進みます。settings 操作はしません。

### 設定ファイルの解決手順

`settings.recommended.json` の場所はインストール形態（symlink / 直接配置 / 移設後）で変わるため、以下を上から順に試して **最初に見つかったもの** を採用します。

```
1. 環境変数 $ADVANCED_DESIGN_MD_DIR が設定されていれば $ADVANCED_DESIGN_MD_DIR/settings.recommended.json
2. このスキル本体の実体パス（symlink ならその参照先）から `../../settings.recommended.json`
   - 解決例: `readlink -f ~/.claude/skills/design-creator` → `/home/user/advanced-design-md/skills/design-creator`
   - その親の親 = `/home/user/advanced-design-md/`
3. ホーム直下の慣例パス: `~/advanced-design-md/settings.recommended.json`
4. カレントディレクトリ: `./settings.recommended.json` および `./advanced-design-md/settings.recommended.json`
```

いずれにも見つからない場合は手動マージを案内します。

```
settings.recommended.json の場所を自動検出できませんでした。
リポジトリの settings.recommended.json を手動で開き、permissions.allow を
~/.claude/settings.json にマージしてください。

または、$ADVANCED_DESIGN_MD_DIR にリポジトリのパスを設定すると次回から自動検出されます:
export ADVANCED_DESIGN_MD_DIR="$HOME/advanced-design-md"
```

---

## フロー全体図

```
1.  インテイク — 用途宣言を受け取る
2.  プリサポート（任意）— 「◯◯みたいなサイト」と言われたら記入例を提示
3.  ボリューム選択 — Quick (5問) / Standard (10問) / Deep (20問) をユーザーに聞く
4.  クイズ起動 — assets/quiz.html を outbox にコピーしてユーザーに開いてもらう
5.  回答受領 — 完了プロンプト or 個別相談プロンプトを受け取る
6.  パース — 自然文プロンプトから Use / Mood / 各層回答を抽出
7.  lexicon 照合 — 回答シグナルを colors / typography / animations / parts に紐付け
8.  patterns 参照 — references/patterns/ で「mood × use の頻出組み合わせ」を確認
9.  補助抽出オファー（条件付き）— lexicon + patterns でも意図を満たせない場合、
    design-extractor へ引き渡し。OK なら抽出 → 復帰して Step 7 を再実行
10. DESIGN.md 生成 — references/templates/DESIGN-template.md に値を埋めて出力
11. 確認ループ — ユーザーに DESIGN.md を見せて修正点を聞く
```

---

## Step 1: インテイク

呼び出し時のユーザー発話から用途を抽出します。例:

| ユーザー発話 | 推定 |
|---|---|
| 「化粧品ブランドのコーポレート作りたい」 | use=corporate / 業種=cosmetics |
| 「ファンタジーゲームの LP みたいなの」 | use=lp / mood=fantasy |
| 「ポートフォリオサイトの世界観決めたい」 | use=portfolio |

**ここでは推定値を内部メモにとどめます**。クイズには反映しますが、ユーザーへの「こうですよね？」という確認は行いません（クイズで尋ねるため）。

---

## Step 2: プリサポート（参考サイト型インテイク）

ユーザーが「**◯◯みたいなサイト作りたい**」と既存サイトを引用した場合、クイズに進む前に **記入例** を提示します。

### 形式

```
「{参考サイト名}みたいなサイト」というご要望、以下のように受け取って問題ないでしょうか？
- 用途: {推定 use}
- 雰囲気: {推定 mood 群}
- 第一印象軸: {推定軸}
- 似せたい要素: {例: 配色 / タイポ / アニメ / レイアウト}
- 似せたくない要素: {例: 重さ / コーポレート臭 / トレンド感}

これを叩き台にしてクイズに進めます。
違う箇所があれば、クイズの「その他」で書き換えていただけます。
```

### 用途

- ユーザーが言語化に詰まる前に「このような枠組みで答えればよい」を提示する
- クイズ回答中の判断軸を共有する（後に「AI に相談」ボタンが押された際の対話がスムーズになる）
- **強制ではありません**。ユーザーが独力で全項目回答できる場合はスキップ可能です

参考サイトの実物 URL が示された場合も fetch は行いません（fetch は design-extractor の役割です）。あくまで会話文脈からの記入例提示にとどめます。

---

## Step 3: ボリューム選択

ユーザーに以下の選択肢を提示します。`[要確認]` 残しの目安も併記し、後で「思ったより空欄が多い」と感じる事故を防ぎます。

```
クイズの設問数を選択してください。

- Quick (5問) — Use / 第一印象軸 / Mood 主軸 / 配色傾向 / レイアウト型 のみ。即決向きです
  → 情報量が少ないため DESIGN.md に [要確認] が半数程度残ります
- Standard (10問) — Quick + Target / 差別化軸 / アクセント / フォント傾向 / モーション傾向 / 必須パーツ
  → [要確認] は 30% 以下が目安です
- Deep (20問) — 全 7 層・全 20 問。世界観をしっかり詰めたい場合向けです
  → [要確認] は 20% 以下を狙えます
```

選択された volume は `references/question-bank.md` の各設問の `volume.{quick|standard|deep}` フラグでフィルタします。

---

## Step 4: クイズ起動

### 出力先（OUTBOX）の解決

以下の順で `OUTBOX` を決定します:

```
1. output= パラメータが指定されていれば、その値
2. 環境変数 $DESIGN_OUTBOX_DIR
3. ~/.claude/outbox/  （Claude Code 標準）
4. ./outbox/           （cwd フォールバック）
```

ディレクトリが存在しない場合は `mkdir -p {OUTBOX}` で作成します。

### コピー手順

`assets/quiz.html` を `{OUTBOX}/quiz-{name}.html` にコピーします（`{name}` は use= から kebab-case で生成）。

### HTTP 配信（必須）

ブラウザに渡す URL は **必ず `http://localhost:{PORT}/...` 形式** にします。`file://` 直リンクは WSL / Linux コンテナ / Codespaces 等で開けないケースがあるため使用しません。

```bash
cd {OUTBOX} && python3 -m http.server 8765
```

- バックグラウンドで起動します（Bash の `run_in_background=true`）。Step 11（確認ループ）完了時または session 終了時に kill します
- ポート 8765 が使用中の場合は 8766 → 8767 と +1 ずつ試します
- `python3` が無い環境では `npx --yes http-server -p 8765 .` で代替します
- 起動直後に `curl -sI http://localhost:{PORT}/quiz-{name}.html | head -1` で `200 OK` を確認してからユーザーに案内します

URL のクエリパラメータは `#` 以下に埋め込みます:

```
http://localhost:{PORT}/quiz-{name}.html#volume=quick&lang=ja
```

- `volume` — quick / standard / deep（必須）
- `lang` — ja / en（任意・既定は ja）

> **注**: Step 1 で推定した `use` / `mood-hint` は URL に含めず、Claude 側の内部メモとして保持します。Step 6 のパース後、signal の重み付けに反映してください（quiz.html は `volume` / `lang` のみを処理します）。

ユーザーには以下を伝えます:

```
クイズを準備しました。以下の URL をブラウザで開いてください。
http://localhost:{PORT}/quiz-{name}.html#volume={volume}&lang={lang}

回答が完了しましたら、ページ下部の「完了」ボタンを押し、
生成された自然文プロンプトをここに貼り付けてください。
途中で判断に迷った場合は、各設問の「AI に相談」ボタンで設問単位の壁打ちも可能です。
```

> **注**: ハッシュパラメータは `volume` と `lang` の 2 つを使用します（quiz.html が処理する範囲）。Step 1 で推定した `use` / `mood-hint` はクイズ起動 URL ではなく、Claude 側の内部メモとして保持し、Step 6 のパース後に signal の重み付けへ反映してください。

---

## Step 5: 回答受領

ユーザーから 2 種類の入力が届きます。**プロンプトの先頭 1 行で判別します**。フォーマット詳細は `references/prompt-format.md` を参照してください。

| 先頭 | 種別 | 挙動 |
|---|---|---|
| `【相談】` (ja) / `[Consult]` (en) | A. 個別設問の相談 | 選択肢 a〜d の推奨 1 つ + 理由 1 行で簡潔に返答します。末尾に「クイズに戻り、この回答を入力したうえで進めてください」と添えます |
| `# Design Brief — {timestamp}` | B. 完了プロンプト | Step 6 へ進みます（`## 設定` / `## Settings` の Language 値で ja/en を判定し、見出し対応はパース仕様参照） |

A はクイズ途中で届く可能性があります（ユーザーがクイズ画面の「AI に相談」を押した場合）。B は完走後に貼り付けられます。

---

## Step 6: パース

完了プロンプトを `references/prompt-format.md` のパース仕様に従って抽出します。

各選択を `references/question-bank.md` の `signal.{field, value}` でルックアップし、
DESIGN.md の各フィールドに **生の値** として一旦集約します（intent / mood / visual / typography / motion / component / technical の 7 層キー）。

自由入力（その他選択時・末尾追記）は **原文転記** で保持してください。勝手な類推変換は行いません。

---

## Step 7: lexicon 照合

集約した生の値を `references/lexicon/` で具体名に解決します。各 lexicon ファイルに照合表と reason 雛形が含まれているため、それをそのまま参照してください。

| 解決対象 | 参照ファイル | 抽出するもの |
|---|---|---|
| Colors | `references/lexicon/colors.md` | パレット slug + bg/primary/accent/sub-accent の hex |
| Typography | `references/lexicon/typography.md` | role 別フォント + source + weight |
| Animations | `references/lexicon/animations.md` | scope 別の keyframe / transition 名 + spec |
| Parts | `references/lexicon/parts.md` | ja 名 + 初期 reason + 推奨アニメ scope |

### 共通ルール

- 候補が複数出た場合は **第一候補 1 つに決め打ち** します。第二候補は `[alternative: {slug}]` でコメントに残します
- 各値に `reason` を必ず添えます（Intent のどこに紐づくかを 1 行で記述）
- lexicon にない値（自由入力で来た色名・フォント名）は `[要確認]` で残します

---

## Step 8: patterns 参照

`references/patterns/` の経験則ファイルで、lexicon 単独では決め切れない **組み合わせ判断** を補強します。

| 参照ファイル | 使う場面 |
|---|---|
| `patterns/color-combos.md` | mood × use で複数パレット候補が出た / accent と sub-accent の選び方が曖昧 |
| `patterns/animation-recipes.md` | scope 横断のアニメ組み合わせ（mystic stack / minimal stack 等）を引きたい |
| `patterns/component-defaults.md` | クイズで required-parts が空 or 不足 / use × mood に応じた標準構成を引く |

### 適用ルール

- patterns は **経験則** です。lexicon の hex / slug / アニメ名は変更せずそのまま流用してください
- patterns と lexicon が衝突した場合は **lexicon 優先** とします
- patterns に該当組み合わせがない場合は、何も上書きせず Step 9 へ進んでください（patterns を捏造で埋めない）
- 適用した場合は DESIGN.md の `reason` に「patterns: {ファイル名} の {セクション} に該当」を 1 行追記します

---

## 色判断軸（standard 連携）

色を決める／差し色を補うときの判断軸。**角度表・OKLCH 値・WCAG 閾値・ランプは持たず** [color-judgment-standard](/home/cache08/.claude/docs/reference/color-judgment-standard.md) を引く（数値はあちらが単一真実源）。ここは決定フローだけ。

### 配色型を当てる
- `mood → 配色型` は standard の「配色型早見」を参照（補色／類似／三色／分裂補色／四色／単色）。
- 早見に無い mood は**決め切らず、lexicon パレットの色相関係から逆算する**（パレット側を真とする）。

### primary の色相
- `mood → primary 色相 h` は standard の「8色 OKLCH 心理マップ」を参照。

### 決定手順
1. lexicon（Step 7）から mood × use で候補を出す。
2. 候補が割れたら〔配色型に適合するか〕と〔**#fff/#000 本文 × 不透明面**（body bg・主要セクション bg）が **AA 4.5:1**〕で決め切る（着色文字・半透明面は強制しない＝努力目標。判定範囲は standard §0）。
3. lexicon に必要な role が無いときだけ、救済生成（下記）。

### 救済生成（user 確認ゲート）
- **配色型が確定している経路でのみ**発火する。配色型を決め切れなかったフォールバック経路では救済せず、`[要確認]` のまま人間へ返す。
- primary の色相から、確定済み配色型の角度（standard 角度表＝補色 h+180／類似 h+30 か h−30／三色 h+120／分裂補色 h+150 か h+210／単色 同一 h で L・C 違い）で1色を OKLCH 生成する。
- **±2候補の符号は「既存 accent/sub-accent との色相距離が最大になる側」で固定**（決定論を守る。standard 末尾の注記と同じ規約）。
- 生成色は `[要確認: generated 候補]` として残し、**人間の採択を待つ**（自分で確定しない）。採択されたら `source: generated` を添える。
- **救済トリガ**: lexicon の sub-accent 等が `—`（差し色なし）は「差し色不要の設計意図」＝既定では救済しない。use/mood が明確に差し色を要求するときだけ候補を提示する。

> この救済生成は creator 内部の補完で、Step 9 の extractor handoff（lexicon が意図に届かないときの外部抽出）とは別物。どちらも **user 確認を挟む**点は共通（コア原則 #2 の閉世界を勝手に破らない）。

---

## Step 9: 補助抽出オファー（条件付きで発動）

lexicon がユーザーの意図に届かないと判断した場合のみ発動します。詳細手順・オファー文・URL 選定ルール・暴走防止は `references/extractor-handoff.md` を参照してください。

### 発動条件（いずれか 1 つ以上）

1. **固有名詞・ブランド言及** — 自由入力にブランド名・作品名・URL が含まれる（既存サービスや作品を直接参照しているケース）
2. **mood 衝突** — lexicon 第一候補がユーザーの別要件と矛盾する（例: brightness=中明度 だが mood=神秘 で第一候補が dark しかない）
3. **`[要確認]` 多発** — Step 7 までで volume 別目安を超過（quick: 50% / standard: 30% / deep: 20%、成功条件節の表を参照）
4. **lexicon カバー外シグナル** — 自由入力に lexicon にないスタイル名が含まれる（例: ニューモーフィズム / Y2K）

### 発動しない場合

- 上記がいずれも満たされない → そのまま Step 10 へ進みます
- Quick (5問) で自由入力が空 → 発動しません（情報不足で勝手に拡張しない）
- 当該セッションで既に 1 回オファー済み → 再オファーしません

### 発動した場合の流れ

1. ユーザーに「lexicon 不足の理由 + 候補 URL 2 件 + 進める」を提示します（オファー文は handoff.md を参照）
2. ユーザーが抽出 OK → design-extractor を呼び出し → 完了後に Step 7 へ復帰し、INTERPRETED.md を追加ソースとして再照合します
3. ユーザーが NO → そのまま Step 10 へ進み、不足は `[要確認]` で残します

### 復帰後（Step 7 への戻り）の挙動

extractor 完了後に Step 7 を再実行する際、以下のルールが **コア原則 #2 の例外** として適用されます:

- 抽出された INTERPRETED.md の色値・フォント名・アニメ名は **lexicon と同格に扱えます**
- ただし DESIGN.md 内で採用箇所には `<!-- source: extracted from {slug}/INTERPRETED.md -->` のコメントを必ず添えてください
- lexicon にも INTERPRETED.md にも該当値がない場合は通常通り `[要確認]` で残します

### 設計意図

- design-creator は本来 lexicon 内で完結するのが原則です
- ただし lexicon は有限であり、固有ブランド・新規スタイルへの救済路として例外的に extractor を呼びます
- AI が勝手にサイト選定すると user 意図とズレるため、必ず user 確認を挟みます

---

## Step 10: DESIGN.md 生成

テンプレートを読み込み、Step 6 の生値と Step 7〜9 の解決結果を埋めて出力します。
テンプレートは `lang` パラメータに応じて選択してください:

- `lang=ja`（既定）: `references/templates/DESIGN-template.md`
- `lang=en`: `references/templates/DESIGN-template.en.md`

### 出力先

```
{OUTBOX}/DESIGN-{name}.md
```

`{OUTBOX}` は Step 4 と同じ解決ルールに従います（output= → $DESIGN_OUTBOX_DIR → ~/.claude/outbox/ → ./outbox/）。
`{name}` の決定:
- ユーザーが `name=` を明示 → そのまま採用します
- それ以外 → use= ＋ Mood 主軸から kebab-case で生成します（例: `corporate-cosmetics-dark`）

### 必須ルール

- 各値に `reason` を必ず添えてください。未確定でも空欄にせず `[要確認: 理由]` で残します（`lang=en` の場合は `[pending review: reason]`）
- 自由入力は原文転記とします。勝手に lexicon 値に正規化しません
- 外部 lib は採用しません（Animations.Libraries は CSS + IO を標準とします）
- Step 9 で extractor 由来の値を採用した場合は `<!-- source: extracted from {slug}/INTERPRETED.md -->` コメントを残します
- 完成形のセクション順序・記法は `references/samples/` のサンプルを参照してください

---

## Step 11: 確認ループ

生成した DESIGN.md をユーザーに提示し、修正点を確認します。よくある修正点はパレット差し替え / パーツ追加・削除 / フォント再選定などです。

ユーザー修正が来た場合は、該当部分のみ修正し、**再生成ではなく既存ファイルを編集** してください（reason の整合性も合わせて更新します）。

---

## 呼び出し形式

```
/design-creator [パラメータ]
```

スキル名と同名のスラッシュコマンドです。会話文脈に「コーポレートサイト作りたい」等の用途宣言が含まれる場合は、明示コマンドなしでも発動します（description のトリガー参照）。

| パラメータ | 説明 | 例 |
|---|---|---|
| `volume=` | quick / standard / deep | `volume=standard` |
| `name=` | 出力ファイル名 | `name=cancan` |
| `lang=` | クイズと Claude 応答の言語。`en` の場合、クイズ HTML だけでなく Claude 自身の返答テキスト（Step 2 のプリサポート例文・Step 5 の相談返答・Step 11 の確認ループ等）もすべて英語で書く | `lang=ja` (default) / `lang=en` |
| `use=` | 用途を即指定（プリサポートをスキップ） | `use=corporate` |
| `output=` | 出力ディレクトリを直指定 | `output=~/my-briefs/` |

すべて省略可能です。省略時は会話文脈から推定し、不足分はステップ進行中に確認します。

---

## 成功条件

| 種別 | 条件 |
|---|---|
| 定量 | DESIGN.md の Intent / Colors / Typography / Spacing / Components / Animations / Constraints の 7 セクションが全て存在 |
| 定量 | Colors / Typography / Components の各値に reason が埋まっている（`[要確認]` 含む） |
| 定量 | クイズで提示した全設問のログが完了プロンプトに含まれていた |
| 定性 | lexicon に存在しない色値・フォント・アニメ名を新規創作していない |
| 定性 | 自由入力（その他）の値はそのまま転記し、勝手に類推変換していない |
| 定性 | `[要確認]` 比率が volume 別目安以内（下表参照） |

### `[要確認]` の許容比率（volume 別）

情報量と埋まる率は比例関係にあるため、volume ごとに目安を分けます。

| volume | 設問数 | `[要確認]` 比率の目安 | 解釈 |
|---|---|---|---|
| quick | 5 | 50% 以下 | 自由入力が空でも Use / Mood / 第一印象軸が確定していれば許容 |
| standard | 10 | 30% 以下 | Target / 差別化軸 / アクセントが埋まる前提 |
| deep | 20 | 20% 以下 | 全層回答ありなので Typography / Motion / Component まで確定すべき |

これを超える場合は情報不足のシグナルです。Step 9（補助抽出オファー）の発動条件「`[要確認]` 多発」は **volume 別目安の超過** を指します。

---

## Reference Files

- `references/question-bank.md` — 全 20 問の設問プール（YAML 構造仕様つき）
- `references/prompt-format.md` — クイズ完了プロンプト・個別相談プロンプトの仕様（Step 5/6 で使用）
- `references/extractor-handoff.md` — 補助抽出オファーの詳細（Step 9 で使用）
- `references/lexicon/colors.md` — 配色パレット辞書（mood × 用途で引ける）
- `references/lexicon/typography.md` — フォント組み合わせ辞書
- `references/lexicon/animations.md` — アニメーション scope 別辞書
- `references/lexicon/parts.md` — パーツ辞書（ja 名・推奨アニメーション・初期 reason）
- `references/patterns/color-combos.md` — mood × use で頻出するパレット組み合わせの経験則（Step 8 で使用）
- `references/patterns/animation-recipes.md` — mood 別のアニメ組み合わせレシピ（Step 8 で使用）
- `references/patterns/component-defaults.md` — use × mood 別の必須パーツ構成テンプレ（Step 8 で使用）
- `references/templates/DESIGN-template.md` — DESIGN.md の空テンプレート（日本語版・lang=ja で使用）
- `references/templates/DESIGN-template.en.md` — DESIGN.md の空テンプレート（英語版・lang=en で使用）
- `references/samples/` — 用途別の捏造サンプル（corporate / lp / portfolio）
- `assets/quiz.html` — 静的 HTML クイズ本体

---

## アンチパターン

コア原則からは直接読み取れない、具体的に踏みやすい失敗例です。

- ❌ 対話形式で長々とヒアリングする — クイズの完全保存性が壊れます（コア原則 #2 違反）。必ず `assets/quiz.html` を起動してください
- ❌ 自由入力を勝手に正規化する（"明朝系" → "Noto Serif JP" 等） — ユーザー意図を歪めます。原文転記が原則です
- ❌ AI 記憶ベースで参照サイト URL を捏造して design-extractor を発動する — 必ず候補提示 → user 確認を経てください（Step 9 / handoff.md 参照）
- ❌ 外部 CDN・画像 URL を DESIGN.md に書く — Constraints 節の「外部 CDN・外部画像 URL の使用禁止」原則違反です
