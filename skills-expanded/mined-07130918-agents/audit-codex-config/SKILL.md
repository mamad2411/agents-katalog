---
name: audit-codex-config
description: 既存の Codex 設定ファイル(AGENTS.md / .Codex/skills/*/SKILL.md / .Codex/agents/*.md / .Codex/commands/*.md)を公式ベストプラクティス(AGENTS.md <200行、progressive disclosure、skills優先、anti-pattern除去)に沿って監査・リファクタする。引数なしで現在の作業ディレクトリ全体、引数にディレクトリやファイルパスを指定するとそれだけを最適化する。「AGENTS.mdが長すぎる」「skillを整理したい」「設定を公式準拠にしたい」「commandsをskillsに統合したい」「Codex設定を最適化」等のリクエスト時に使用。新規 skill の発見・追加は `discover-skills` を使う。
argument-hint: ディレクトリ | AGENTS.md | SKILL.md | agent.md
disable-model-invocation: true
allowed-tools: Read Edit Write Glob Grep Bash(wc *) Bash(ls *) Bash(mkdir *) Bash(rm *) Bash(find *) WebFetch
---

# audit-codex-config

この skill の詳細手順は `~/.agents/references/audit-ai-cli-config.md` に集約しています。

この skill が発火したら、作業前に必ず上記の参照ファイルを読み、実行中の CLI に対応する手順・チェックリスト・注意事項に従ってください。
