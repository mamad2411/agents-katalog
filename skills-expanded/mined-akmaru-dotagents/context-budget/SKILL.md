---
name: context-budget
description: Claude Code のコンテキスト使用量を計測し、どこに何トークン使っているか・何を減らせるかを特定して対処する。「コンテキストを減らしたい」「トークンをどこに使っている」「MCP やスキルが重い」「コンテキストが足りない」などに言及したとき、または SessionStart hook が出す [context-budget] の指摘に対応するときに使う。計測は dotagents の claude-context.py（`claude -p /context` のスナップショットと transcript 解析）に依存する。
compatibility: Designed for Claude Code. Requires claude-context.py installed by akmaru/dotagents user/install.sh
---

コンテキストの使い道を**測ってから**減らす。推測で MCP を外したり CLAUDE.md を削ったりしない。
削減は設定やファイルの変更を伴うので、提案 → ユーザーの承認 → 適用 → 再計測、の順に進める。

## 用語

- **ベースライン**: セッション開始直後に既に埋まっている量。システムプロンプト・組み込みツール定義・
  MCP ツール定義・メモリファイル（CLAUDE.md / AGENTS.md / rules）・スキル一覧・カスタムエージェント一覧。
  毎セッション、毎リクエスト必ず載る固定費
- **増加分**: 会話中に積み上がる量。アシスタント出力・ツール結果・ユーザー入力・attachment
  （Claude Code が自動で差し込む system-reminder 類）

## 手順

### 1. 計測する

```bash
claude-context.py report --cwd "$PWD" --days 14   # このプロジェクト
claude-context.py report --days 14                # 全プロジェクト（ベースラインは出ない）
```

`command not found` なら dotagents の `user/install.sh` が未実行。`~/.local/bin` が PATH に無い場合は
`~/.local/bin/claude-context.py` を直接叩く。

レポートに「スナップショットなし」と出たら先に取る（API は呼ばれない。数秒で終わる）:

```bash
claude-context.py snapshot --cwd "$PWD"
```

### 2. 読む

レポートは 3 部構成。

1. **ベースライン**: 区分ごとのトークンと、MCP サーバーごとの「定義トークン × 期間中の呼び出し回数」
2. **セッション表**: 開始時・最大・ウィンドウ比・主な増加要因
3. **削減候補**: ルールベースの指摘（未使用 MCP、肥大したメモリファイル、支配的なツール、巨大な単発結果、
   ウィンドウの 60% 超え、前回スナップショットからの増加）

内訳は API が返した実測差分を推定比で按分した値。**合計は正確、個々は目安**として扱う。
「assistant output」には thinking も含まれるため、実際に残る量より大きめに出る。

### 3. 対処を提案する

指摘ごとに「毎セッション何トークン × 何セッション」で効果を見積もり、大きい順に並べる。
レバーは決まっている:

| 指摘 | レバー | 変更場所 |
|------|--------|----------|
| MCP サーバーが未使用・ほぼ未使用 | サーバーを外す / 無効化 | dotagents 管理機: `mcp/master-mcp.json` を編集して `mcp/sync-mcp.sh all`。それ以外: `claude mcp remove <name>` か settings の `disabledMcpServers` |
| `claude_ai_*` の MCP が未使用 | claude.ai のコネクタを外す | claude.ai 側の設定。CLI からは変えられないのでユーザーに案内する |
| Hindsight のツールが多すぎる | 使うツールだけに絞る | Hindsight の bank 設定 `mcp_enabled_tools`（`update_bank` で変更可） |
| メモリファイルが大きい | 場面が限られる節をスキル / rules へ移す | `user/AGENTS.md`、プロジェクト `CLAUDE.md`、`.claude/rules/` |
| スキル一覧が大きい | 使わないプラグイン・同期スキルを外す | `claude plugin` / claude.ai の同期設定 |
| Bash / Read の結果が支配的 | 出力を絞る癖をつける。上限を設ける | settings の `bashOutputMaxChars`。AGENTS.md に「head / grep で絞る」「長い調査はサブエージェント」の指示 |
| 巨大な単発結果 | その呼び出し方を見直す | 該当ツールの使い方（WebFetch の prompt を絞る、recall の `max_tokens` を下げる等） |
| セッションがウィンドウの 60% 超 | 話題の切れ目で `/clear`、長い調査は別セッション | 運用 |

### 4. 承認を得て適用する

設定ファイルの変更は差分を見せて承認を得てから行う。dotagents 配下の設定を変える場合は、そのリポジトリの
CLAUDE.md の手順（`sync-mcp.sh`、`install.sh`）に従う。

### 5. 再計測して効果を確認する

```bash
claude-context.py snapshot --cwd "$PWD"
claude-context.py report --cwd "$PWD" --days 14
```

ベースライン表の「前回」列で差分を示す。MCP の変更は新しい `claude` プロセスにしか効かないので、
スナップショットは `claude -p` で新規に起動して測る（このスクリプトがそうしている）。

### 6. 記録する

外した MCP や動かした指示は、なぜ外したか（未使用の根拠）を Hindsight に retain する。設計として残す価値が
あれば ADR を書く。

## やらないこと

- 計測せずに「重そうだから」で外す
- ユーザーの承認なしに MCP / メモリファイル / settings を変更する
- レポートの推定値を実測値として断言する
