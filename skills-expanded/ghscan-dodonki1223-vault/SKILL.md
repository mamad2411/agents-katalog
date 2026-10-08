---
name: workflow-fetch-and-classify-materials
description: Slack、Linear、Notion、GitHub、Google Meet、Google Sheets、一般的な Web ページなどから必要な情報を集め、fetch 系 skill を組み合わせて取得結果を分類し、後続の更新や判断に渡しやすい形へ整理する workflow skill。Project 更新前の材料集め、単発調査、issue に限らない文脈収集を依頼されたときに使う。
---

# 情報取得と分類 workflow

## 目的

必要な情報源を見極め、fetch 系 skill を使って情報を取得し、`classify-fetched-materials` に渡して、後続の更新や判断で使える形に整理する。

この skill は進行役であり、各情報源の取得手順の細部や、最終的な更新判断は capability skill またはメイン agent に委譲する。

複数の情報源を使う場合は、fetch 系の取得を read-only サブエージェントとして並列実行してよい。統合判断と分類結果の最終確認はメイン agent が行う。

## 入力

- 調べたい対象。例: topic、Slack thread、Linear issue、Project、Notion page、Google Meet、Google Sheets。
- 調べたい理由。例: status 更新前の材料集め、単発調査、意思決定確認、依頼の棚卸し。
- 必要に応じて、対象期間、優先して見る情報源、観点、除外条件。
- 任意の短い文脈。例: Project path、note 名、関係者、関連 issue。

対象が広すぎる場合は、最初に狭く切るための短い質問を 1 つだけする。

## 使う skill

- `fetch-slack-materials`: Slack から指定対象の情報を取得する。
- `fetch-linear-materials`: Linear から指定対象の情報を取得する。
- `fetch-notion-materials`: Notion / Docs から指定対象の情報を取得する。
- `fetch-github-materials`: GitHub から指定対象の情報を取得する。
- `fetch-google-meet-materials`: Google Meet の MTG メモや関連 Docs / Drive 情報を取得する。
- `fetch-google-sheets-materials`: Google Sheets から指定対象の情報を取得する。
- `fetch-web-materials`: 特定サービスの connector に依存しない、一般的な Web ページ・ブログ・ニュース・公式ドキュメントから情報を取得する。GitHub / Notion / Linear など専用 skill がある対象には使わない。
- `classify-fetched-materials`: 取得済み情報を事実、決定事項、推測、重要リンク、未解決事項、次アクション、ユーザー対応待ちに分類する。

## 参照する reference

- `.agents/references/subagent-fetch-contract.md`: fetch 系サブエージェントの入力と出力の共通契約。
- `.agents/model-profiles/fetch-light.toml`: fetch 系の軽量取得で使う repository 推奨 profile。
- `.agents/model-profiles/fetch-standard.toml`: fetch 系の通常取得で使う repository 推奨 profile。
- `.agents/scripts/run-fetch-skill.mjs`: fetch 系 skill を profile 付きで実行する command wrapper。

## 手順

1. 依頼の単位を確認する。
   - 「何について」「何のために」情報を集めるのかを確認する。
   - issue は一例として扱い、依頼単位を issue に固定しない。
   - 更新先が未定でもよい。まずは取得と分類を進める。

2. 必要な情報源を決める。
   - ユーザーが明示した情報源を優先する。
   - 明示がない場合は、対象と理由から必要最小限の情報源を決める。
   - 例:
     - 会話経緯や依頼確認なら Slack
     - 状態や担当確認なら Linear
     - 仕様や決定事項なら Notion / Docs
     - 実装や CI なら GitHub
     - MTG 由来の決定確認なら Google Meet
     - 数表や設定値なら Google Sheets
     - 特定サービスに紐づかない一般的な Web ページ・ブログ・ニュース・公式ドキュメントなら Web

3. 情報源ごとの取得条件を揃える。
   - `.agents/references/subagent-fetch-contract.md` に従い、各 fetch 系 skill へ渡す入力をそろえる。
   - 少なくとも、対象、期間、観点、除外、呼び出し理由を明示する。
   - 情報源ごとに無理に同じ対象を探さず、その情報源で自然に取得できる単位へ落とす。
   - サブエージェントで実行する場合は、各情報源ごとに独立した入力として切り出す。

4. 必要な情報を取得する。
   - 情報源ごとに対応する fetch 系 skill を使う。
   - 実行時は、個別に prompt を組み立てるより、原則として `.agents/scripts/run-fetch-skill.mjs` または `pnpm fetch:materials` / `pnpm codex:fetch:materials` / `pnpm claude:fetch:materials` の command 層を使う。
   - 複数情報源が必要な場合は、read-only の取得をサブエージェントで並列実行してよい。
   - サブエージェントに渡す役割は「取得だけ」に限定する。分類、更新、優先度判断、通知判断は渡さない。
   - 各サブエージェントには、対応する fetch 系 skill、profile 名、`.agents/references/subagent-fetch-contract.md` の契約を前提として渡す。
   - 取得対象が 1 情報源だけ、またはサブエージェント化のオーバーヘッドが大きい場合は、メイン agent がそのまま取得してよい。
   - fetch 系 skill の返答は、そのまま更新先へ貼らず、取得結果として保持する。
   - 認証不足、権限不足、対象不明の場合は、その情報源だけ失敗理由を保持し、他の取得を継続できるなら継続する。

5. 取得結果をそろえる。
   - fetch 系 skill の返答が `.agents/references/subagent-fetch-contract.md` の骨格に沿っているか確認する。
   - 取得範囲、取得結果、取得できなかった理由、不足している可能性を情報源ごとに整理する。
   - 契約に沿っていない返答でも、内容を壊さない範囲で最小限に整形してから後続へ渡す。

6. 分類する。
   - `classify-fetched-materials` を使う。
   - 取得済み情報、取得元、取得理由、必要な短い文脈を渡す。
   - classify には追加取得、優先度判断、更新先への反映をさせない。

7. 結果を統合する。
   - 情報源ごとの取得結果と分類結果を、後続で使いやすい形にまとめる。
   - 矛盾がある場合は workflow 内で解消せず、分類結果の `未解決事項` または `分類できなかったもの` として残す。
   - 「何が取れたか」と「何がまだ不足しているか」を分けて返す。

8. 結果を返す。
   - 使った情報源。
   - 取得できた対象と取得できなかった対象。
   - 分類結果。
   - 不足している情報。
   - 必要なら、次にどの更新 skill や review skill に渡すべきか。

返答には次の形を含める。

```markdown
## 情報取得結果

- 使った情報源:
- 取得できた対象:
- 取得できなかった対象:

## 分類結果

### 事実

- 

### 決定事項

- 

### 推測

- 

### 重要リンク

- 

### 未解決事項

- 

### 次アクション

- 

### ユーザー対応待ち

- 

### 分類できなかったもの

- 

## 不足している情報

- 

## 次に渡す候補

- 
```

## 境界

- この skill は取得と分類までを担当し、Project、note、Linear、Slack などの更新は行わない。
- fetch 系 skill の代わりに独自の取得手順を書き始めない。
- write 系 skill を勝手に呼ばない。
- 取得結果をそのまま正本扱いせず、必要なら後続の review や更新 skill に渡す。
- model の選択や固定は、shared skill の長い文章ではなく、repository 管理の model profile と実行 wrapper で扱う。
- サブエージェントを使う場合でも、書き込み可能な操作や file 編集を委譲しない。取得系は read-only に限定する。

## サブエージェント実行の指針

- 並列実行する「サブエージェント」は、Claude Code の `Agent` tool ではなく、`### command 入口` の command 経由で呼び出す（並列に Bash で複数起動してよい）。理由:
  - `Agent` tool は Claude family（`sonnet` / `opus` / `haiku` / `fable`）以外の model を指定できない。GPT 系 model（`gpt-5.6-terra` など）は command 経由でしか使えない。
  - `Agent` tool を使う場合、`.agents/model-profiles/*.toml` は自動適用されない。model を反映させるには `model` パラメータを明示指定する必要があり、profile との対応がずれやすい。
  - command 経由なら `.agents/model-profiles/fetch-light.toml` / `fetch-standard.toml` の `model` がそのまま使われるため、profile と実行結果が一致する。
- 並列化してよいもの:
  - Slack、Linear、Notion、GitHub、Google Meet、Google Sheets、Web など、情報源ごとの取得
- 並列化しないもの:
  - 情報源横断の統合判断
  - 分類結果の最終確認
  - 更新先への反映判断
- サブエージェントへの依頼文には、少なくとも次を含める:
  - 使う fetch 系 skill 名
  - 使う profile 名。例: `fetch-light` / `fetch-standard`
  - 対象
  - 期間
  - 観点
  - 除外条件
  - 呼び出し理由
  - `.agents/references/subagent-fetch-contract.md` に従って返すこと
- 返ってきた結果は、そのまま正として採用せず、メイン agent が重複、矛盾、取りこぼしを確認する。

### command 入口

- Codex:
  - `pnpm codex:fetch:materials -- --skill <fetch-skill> --profile <fetch-light|fetch-standard> "依頼内容"`
- Claude Code:
  - `pnpm claude:fetch:materials -- --skill <fetch-skill> --profile <fetch-light|fetch-standard> "依頼内容"`
- 共通:
  - `pnpm fetch:materials -- --agent <codex|claude> --skill <fetch-skill> --profile <fetch-light|fetch-standard> "依頼内容"`
