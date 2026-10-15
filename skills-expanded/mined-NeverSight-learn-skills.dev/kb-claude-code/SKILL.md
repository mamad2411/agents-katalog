---
name: kb-claude-code
description: Claude Code/AIツールのナレッジ。Claude Code設定、MCP、プロンプト設計、スキル作成等
user-invocable: true
---

# Claude Code/AIツールナレッジ

Claude CodeおよびAIツール全般に関する学びを記録する。

## Claude Code設定

### Hooks の stdin フォーマット

hooks はイベント発火時に stdin で JSON を受け取る。共通フィールドと各イベント固有のフィールドがある。

共通フィールド: `session_id`, `transcript_path`, `cwd`, `permission_mode`, `hook_event_name`

Stop 固有:
- `stop_hook_active` (bool): 前回の stop hook で継続中かどうか。無限ループ防止に使う

Notification 固有:
- `message`: 通知テキスト
- `title`: 通知タイトル
- `notification_type`: `permission_prompt` / `idle_prompt` / `auth_success` / `elicitation_dialog`

`transcript_path` の JSONL を逆順に走査すれば、最後のアシスタント応答を取得できる。

### -p モードでのシステムプロンプト上書き

| フラグ | 効果 | 対応モード |
|--------|------|-----------|
| `--system-prompt` | デフォルト全体を置換 | Interactive + Print |
| `--system-prompt-file` | ファイルで全体置換 | Print only |
| `--append-system-prompt` | デフォルトに追記 | Interactive + Print |
| `--append-system-prompt-file` | ファイルをデフォルトに追記 | Print only |

`--system-prompt` でデフォルトを置換しても、Haiku は指示に従わず応答的な文（「理解しました」等）を返したり、文字数制限を守らないことがある。短文抽出・要約のような単純タスクでは LLM を介さずヒューリスティック処理の方が確実。

### CLAUDECODE 環境変数とネスト実行

Claude Code セッション内から `claude` コマンドを実行すると、`CLAUDECODE` 環境変数によりネスト検知でブロックされる。

hooks の command から `claude -p` を呼ぶ場合も同様に失敗する。対策は subprocess 呼び出し時に `CLAUDECODE` を除外した env を渡すこと:

```python
env = {k: v for k, v in os.environ.items() if k != "CLAUDECODE"}
subprocess.run(["claude", "-p", ...], env=env)
```

---

## スキル作成

<!-- SKILL.md構造、frontmatter、references等 -->

### Agent ファイル (.claude/agents/*.md) の制約

- `.claude/agents/` 以下の `.md` ファイルはサブディレクトリ含めすべてagentとしてパースされる
- リファレンスファイルや補足資料を `agents/` 内に置くとパースエラーになる
- 対策: 補足資料はagent本体の `.md` に統合するか、`agents/` 外に配置する

### Agent Frontmatter の description 記法

`description` フィールドでYAMLパースが壊れるパターン:

- `\n` リテラル文字列（改行のつもりで書いたもの）
- コロン+スペース（`: `）を含むexample形式（`user: 'text'`）
- シングルクォート内にアポストロフィ（`'I've written...'`）

これらが組み合わさるとfrontmatter全体のパースが失敗し、エラーメッセージは "Missing required 'name' field in frontmatter" と表示される（`name` は存在するのにパーサーがfrontmatter自体を読めていない）。

対策:
- `description` は簡潔な1-2文に留める（特殊文字を避ける）
- 詳細なexampleはfrontmatter外の本文に記述する
- 複数行が必要な場合はYAMLのブロックスカラー（`|`）を使用する

---

## MCP (Model Context Protocol)

<!-- MCPサーバー、ツール連携等 -->

---

## 並列エージェント開発パターン

anthropics/claudes-c-compiler の分析から得た、複数Claude Codeインスタンスの協調パターン。

### タスクロック方式 (`current_tasks/`)

ファイルベースの排他制御。エージェントが `current_tasks/` にテキストファイルを作成してタスクを宣言し、完了後に削除する。

```
current_tasks/
  implement_feature_x.txt    # Agent 1が作業中
  fix_bug_y.txt              # Agent 2が作業中
```

ファイル内容にはタスク説明、対象ファイルパス、技術的コンテキストを記載。gitの同期機構と組み合わせることで、2つのエージェントが同じタスクを取ると後続がブロックされる。

コミットサイクル:
```
Lock: implement feature X       # タスク取得宣言
Implement feature X              # 実装
Unlock: feature X (completed)    # 完了報告
```

人間の開発でも有効。worktree並列作業時のタスク衝突防止に使える。

### アイデア蓄積方式 (`ideas/`)

作業中に発見した改善案や課題をファイルとして記録。Issueを起票するほどではないが忘れたくないもの。

```
ideas/
  high_codegen_runtime_perf.txt   # 優先度付きで改善案を記述
  new_projects.txt                # 対応状況ダッシュボード
```

命名規則でトリアージ: `high_`, `low_` プレフィックスで優先度を示す。

### セッションリスタート設計

エージェントは定期的にリスタートされる。復帰時の状態把握を高速化するための設計:

1. `Starting new run; clearing task locks` で全ロックをクリア
2. `current_tasks/` と `ideas/` を読んで状況把握
3. 次のタスクを自律選択

CLAUDE.md だけでなく、機械可読な状態ファイル（`current_tasks/`, `ideas/`）を用意するとセッション復帰が速い。

### 長時間実行ハーネス

```bash
while true; do
    claude --dangerously-skip-permissions \
           -p "$(cat AGENT_PROMPT.md)" \
           --model claude-opus-4-6 &> "agent_logs/agent_$(date +%s).log"
done
```

各セッションのログを保存してデバッグ可能にする。

### 並列ボトルネックの分散解消（オラクル方式）

全エージェントが同じバグにぶつかる問題の解決策。一部のファイルを「既知の正解ツール」で処理し、残りを自作ツールに任せることで、各エージェントが異なるバグに遭遇するようにする。

claudes-c-compiler では GCC をオラクルとして使用:
- カーネルファイルの30%をGCCでコンパイル
- 70%を自作コンパイラでコンパイル
- ランダム分割により各エージェントが異なるファイルでエラーに遭遇

### 実績データ (claudes-c-compiler)

| 指標 | 値 |
|------|-----|
| 総コミット | 3,982 |
| 開発期間 | 14日間 |
| 並列エージェント | 16 |
| Lockコミット率 | 50.4% |
| Fixコミット率 | 14.7% |
| revert | 2件のみ |
| セッションリスタート | 14回（約1日1回） |

コミット内訳: Lock(2005) > Fix(586) > Unlock(354) > Remove(262) > Add(146)

---

## プロンプト設計

<!-- システムプロンプト、効果的な指示の書き方等 -->

---

## トラブルシューティング

<!-- Claude Code固有の問題と解決策 -->

---

## 参考リンク

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [MCP Specification](https://modelcontextprotocol.io/)
