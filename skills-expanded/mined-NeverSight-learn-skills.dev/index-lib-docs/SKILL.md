---
name: index-lib-docs
description: |
  Generates project-libs skill from all project dependencies automatically.
  Use when creating documentation skills for all libraries in a project, or when the user wants to set up library documentation for the current project.
  Can also be invoked directly with "index-lib-docs", "ライブラリドキュメント生成", "依存関係ドキュメント".
disable-model-invocation: true
argument-hint: "[プロジェクトパス（省略時はカレントディレクトリ）]"
allowed-tools: Bash(mkdir:*), Write
---

# プロジェクト依存関係ドキュメント自動生成

## 概要

プロジェクトの全依存ライブラリのドキュメントを自動生成し、`project-libs` スキルを作成する。

**生成されるスキル:**
- **project-libs**: ライブラリimport時に自動発動するドキュメントスキル

**出力先:**
```
{project}/.claude/skills/project-libs/
├── SKILL.md                    # メインスキル
└── references/
    ├── react.md               # 各ライブラリのドキュメントリンク集
    ├── next.md
    └── ...
```

## 実行フロー

```
┌─────────────────────────────────────────────────┐
│ Phase 1: パッケージマネージャー検出              │
├─────────────────────────────────────────────────┤
│ package.json / pyproject.toml / Cargo.toml /    │
│ go.mod を探索                                   │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ Phase 2: 依存関係抽出                           │
├─────────────────────────────────────────────────┤
│ - dependencies / devDependencies を解析         │
│ - バージョン情報を取得                          │
│ - ライブラリリストを作成                        │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ Phase 2.5: ユーザー確認                         │
├─────────────────────────────────────────────────┤
│ - 検出されたライブラリ一覧を提示                │
│ - 除外・追加の確認                              │
│ - 承認を待つ                                    │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ Phase 3: ドキュメントURL発見                    │
├─────────────────────────────────────────────────┤
│ - レジストリAPIからhomepage取得                 │
│ - /llms.txt の存在確認                          │
│ - ドキュメントURLを特定                         │
└─────────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────────┐
│ Phase 4: ファイル生成                           │
├─────────────────────────────────────────────────┤
│ - references/*.md を生成                        │
│ - SKILL.md を生成（全トリガー条件を含む）       │
└─────────────────────────────────────────────────┘
```

---

## Phase 1: パッケージマネージャー検出

プロジェクトルートを特定し、パッケージマネージャーを検出する。

### 検出ロジック

**詳細は [package-managers.md](references/package-managers.md) を参照。**

```bash
# 引数でプロジェクトパスが指定されていればそこを使用、なければカレントディレクトリ
PROJECT_ROOT="${1:-.}"

# 検出優先順位
if [ -f "$PROJECT_ROOT/package.json" ]; then
  PM="node"
elif [ -f "$PROJECT_ROOT/pyproject.toml" ] || [ -f "$PROJECT_ROOT/requirements.txt" ]; then
  PM="python"
elif [ -f "$PROJECT_ROOT/Cargo.toml" ]; then
  PM="rust"
elif [ -f "$PROJECT_ROOT/go.mod" ]; then
  PM="go"
else
  echo "Error: No supported package manager found"
  exit 1
fi
```

---

## Phase 2: 依存関係抽出

### Node.js (jqを使用)

```bash
# production dependencies（名前とバージョン範囲）
jq -r '.dependencies | to_entries[] | "\(.key) \(.value)"' package.json 2>/dev/null

# dev dependencies（名前とバージョン範囲）
jq -r '.devDependencies | to_entries[] | "\(.key) \(.value)"' package.json 2>/dev/null
```

**Note:** バージョンは package.json のバージョン範囲（例: `^18.2.0`）をそのまま使用。ドキュメント参照用途では範囲表記で十分であり、lock file解析の複雑さを回避できる。

### Python

```bash
# requirements.txt
grep -v '^#' requirements.txt | grep -v '^\s*$' | cut -d'=' -f1 | cut -d'>' -f1 | cut -d'<' -f1

# pyproject.toml (dependencies配列)
grep -E '^\s*"[^"]+' pyproject.toml | sed 's/.*"\([^"]*\)".*/\1/' | cut -d'>' -f1 | cut -d'=' -f1
```

### Rust / Go

**詳細は [package-managers.md](references/package-managers.md) を参照。**

---

## Phase 2.5: ユーザー確認（デフォルト全選択方式）

**デフォルト全選択方式**: 検出された全ライブラリをドキュメント化対象として提示し、除外したいものだけを入力してもらう。これにより、ライブラリの漏れを防止する。

```
以下の依存関係をすべてドキュメント化します:

react (^18.2.0), next (^14.2.0), jotai (^2.16.2), swr (^2.3.8),
axios (^1.13.2), tailwindcss (^3.4.19), react-markdown (^9.0.1),
streamdown (^1.6.11), typescript (^5.3.0), eslint (^8.56.0),
vitest (^1.2.0), ... （全ライブラリをカンマ区切りで1行表示）

合計: XX パッケージ (Production: YY, Dev: ZZ)

除外したいライブラリがあれば入力してください（カンマ区切り、空欄で続行）:
→ [フリーテキスト入力]
```

**実装方法**: `AskUserQuestion` ツールを使用し、ユーザーにフリーテキストで除外リストを入力してもらう。

**ポイント**:
- 「このリストでOK?」ではなく「**すべて**ドキュメント化します」と明示
- 全ライブラリをカンマ区切りで表示（見落とし防止）
- 合計数を表示（抜けがないか確認しやすい）
- 空欄入力（Other で何も入力しない）で全選択のまま続行

---

## Phase 3: ドキュメントURL発見

### Step 1: レジストリAPIから取得

**詳細は [registry-apis.md](references/registry-apis.md) を参照。**

**npm:**
```bash
# homepageまたはrepository.urlを取得
curl -s "https://registry.npmjs.org/{package}" | jq -r '.homepage // .repository.url // empty'
```

**スコープ付きパッケージ:**
```bash
# @tanstack/react-query → %40tanstack%2Freact-query
ENCODED=$(echo "@tanstack/react-query" | sed 's/@/%40/g; s/\//%2F/g')
curl -s "https://registry.npmjs.org/$ENCODED"
```

### Step 2: WebSearchによるドキュメントサイト検索

レジストリAPIでドキュメントURLが見つからない、またはGitHubリポジトリしか見つからない場合、WebSearchで公式ドキュメントサイトを検索する:

```
WebSearch(query="{package} documentation official site")
```

**検索結果の優先順位:**
1. 公式ドキュメントサイト（`*.dev`, `docs.*.com`等）
2. 公式ウェブサイト
3. GitHubリポジトリのREADME

**例:**
- "zod documentation" → zod.dev
- "tanstack query documentation" → tanstack.com/query
- "prisma documentation" → prisma.io/docs

### Step 3: llms.txt確認

```bash
# ドキュメントサイトでllms.txtを確認
DOCS_URL="https://tanstack.com/query/latest"
if curl -sI "$DOCS_URL/llms.txt" 2>/dev/null | grep -q "200"; then
  LLMS_TXT="$DOCS_URL/llms.txt"
fi
```

---

## Phase 4: ファイル生成

### 重要ルール

- **1ライブラリ1ファイル**: 各ライブラリは必ず個別の `references/{lib-name}.md` ファイルとして生成する
- 複数ライブラリを1ファイルにまとめない（`other-libs.md` のような統合ファイルは作成禁止）
- ドキュメントが見つからないライブラリも個別ファイルを作成し、GitHubリポジトリのREADMEリンクを記載する

### 出力ディレクトリ

```bash
mkdir -p "$PROJECT_ROOT/.claude/skills/project-libs/references"
```

### 各ライブラリファイル生成

**テンプレートは [templates/library-entry.md](templates/library-entry.md) を参照。**

各ライブラリについて `references/{lib-name}.md` を生成:

```markdown
# {Library}

> Version: {version}
> Docs: {docs_url}
> llms.txt: {llms_txt_url or "Not available"}

## Documentation Links

### Getting Started
- [Quick Start]({docs_url}/getting-started): 基本的な使い方

### API Reference
- [API]({docs_url}/api): API一覧
...
```

### SKILL.md生成

**テンプレートは [templates/project-skill.md](templates/project-skill.md) を参照。**

全ライブラリのトリガー条件を含むSKILL.mdを生成:

```yaml
---
name: project-libs
description: |
  Provides documentation for project dependencies.
  Use when working with code that imports "react", "next", "@tanstack/react-query", "zod", ...
  (検出された全ライブラリ名を列挙)
context: fork
agent: Explore
allowed-tools: WebFetch, WebSearch, Read
---
```

---

## 並列処理

ライブラリ数が多い場合、Taskエージェントを並列起動してドキュメントURL発見を高速化:

```
Task(subagent_type="Explore", prompt="以下のnpmパッケージのドキュメントURLとllms.txt有無を調査: [パッケージリストA]")
Task(subagent_type="Explore", prompt="以下のnpmパッケージのドキュメントURLとllms.txt有無を調査: [パッケージリストB]")
```

---

## 完了メッセージ

生成完了後、以下を表示:

```
project-libs スキルを生成しました:
  {project}/.claude/skills/project-libs/

生成されたファイル:
- SKILL.md (トリガー条件: {n}ライブラリ)
- references/ ({n}ファイル)

スキルは以下の場合に自動発動します:
- react, next, @tanstack/react-query, ... のimport時
- "useQuery", "useState", ... などのAPI使用時

手動で呼び出す場合: /project-libs [質問]
```

---

## トラブルシューティング

### jqがインストールされていない

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq
```

### スコープ付きパッケージの処理

`@scope/package` 形式は適切にURLエンコードする必要がある。
ファイル名は `scope-package.md` のようにスラッシュをハイフンに変換。

### ドキュメントURLが見つからない

- GitHubリポジトリのREADMEを代替として使用
- WebSearchでドキュメントサイトを検索
