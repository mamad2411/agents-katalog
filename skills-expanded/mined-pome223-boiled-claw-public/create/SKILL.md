---
name: create-skill
description: boiled-claw の新しいスキルを対話的に作成する。skills/ と .claude/skills/ の両方に SKILL.md を生成する。
disable-model-invocation: true
---

# create-skill

boiled-claw に新しいスキルを追加するジェネレーター。
ユーザーとの対話から SKILL.md を生成し、適切なディレクトリに配置する。

## 手順

### 1. ユーザーからヒアリング

以下を確認する（未指定の項目は提案して確認を取る）:

- **スキル名**: kebab-case（例: `web-research`, `auto-deploy`）
- **何をするスキルか**: 1-2 文の説明
- **使うツール/CLI**: run_shell, write_file, browser_*, 外部 CLI など
- **ワークフロー**: 大まかな手順（ユーザーが口頭で説明したものを整理）
- **生成先**: 以下から選択（デフォルト: 両方）
  - `skills/<name>/SKILL.md` — boiled-claw エージェント用
  - `.claude/skills/<name>/SKILL.md` — Claude Code 用（`/name` で起動）
  - 両方

### 2. boiled-claw 版を生成（skills/）

以下のテンプレートで `skills/<name>/SKILL.md` を作成する:

```markdown
---
name: {name}
description: {description}
version: 1.0.0
author: boiled-claw
tags:
  - {tag1}
  - {tag2}
---

# {Title} Skill

{1行の役割説明}

## Runtime Requirements

This skill is designed for **root agent execution** — it requires built-in tools
({必要なツール列挙}) that are available to the root agent.
Use `skill_execute("{name}")` to load the instructions, then follow them
with the root agent's tools.

> **Note:** `skill_spawn` creates dynamic agents with MCP toolsets only, which
> do not include built-in tools. Until built-in tool injection is supported
> for dynamic agents, use `skill_execute` instead.

## Workflow

### 1. {Step 1 title}
{手順}

### 2. {Step 2 title}
{手順}

...

## Guardrails

- {安全性に関する制約}

## Usage Examples

```
skill_execute("{name}")
# then: "{利用例}"
```
```

### 3. Claude Code 版を生成（.claude/skills/）

以下のテンプレートで `.claude/skills/<name>/SKILL.md` を作成する:

```markdown
---
name: {name}
description: {description（日本語）}
disable-model-invocation: true
---

# {name}

{1行の役割説明（日本語）}

## 手順

### 1. {ステップ1}
{具体的なコマンドやアクション}

### 2. {ステップ2}
{具体的なコマンドやアクション}

...
```

**Claude Code 版の特徴:**
- 日本語で記述
- `disable-model-invocation: true` を付ける
- bash コマンドはパイプ・リダイレクト OK（Claude Code の Bash ツールはシェル経由）
- `run_shell` の制約（subprocess_exec）を気にしなくてよい

### 4. 生成後の確認

スキルが正しくロードされることを確認する:

```bash
python3 -c "
import asyncio
from src.skills.runtime import ensure_skills_loaded
from src.skills.base import get_skill_registry

async def main():
    # リロードのためキャッシュクリア
    import src.skills.runtime as rt
    rt._loaded = False
    await ensure_skills_loaded()
    registry = get_skill_registry()
    names = sorted(m.name for m in registry.list_skills())
    print(f'Loaded {len(names)} skills: {names}')

asyncio.run(main())
"
```

- 新スキルが一覧に含まれていること
- YAML frontmatter のパースエラーがないこと

### 5. 結果を報告

```
## スキル作成完了

| 項目 | 値 |
|------|-----|
| スキル名 | {name} |
| boiled-claw 版 | skills/{name}/SKILL.md |
| Claude Code 版 | .claude/skills/{name}/SKILL.md |
| ロード確認 | OK |

`/name` で Claude Code から直接起動できます。
```

## ガイドライン

- スキル名は kebab-case で統一する
- 既存スキルと名前が被らないか確認する
- boiled-claw 版は英語、Claude Code 版は日本語で書く
- boiled-claw 版には Runtime Requirements セクションを必ず含める
- tags は 2-5 個、スキルの機能を端的に表すもの
- 外部 CLI を使うスキルは `skills/_utils/run_ai_cli.py` の利用を検討する
- `.env` やシークレットに関するガードレールを必ず含める
