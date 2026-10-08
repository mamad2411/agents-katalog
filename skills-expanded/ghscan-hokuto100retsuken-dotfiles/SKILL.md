---
name: dotfiles-expert
description: この dotfiles リポジトリの管理と拡張に特化した知識を提供します。シェル設定 (fish)、ターミナル設定 (ghostty)、エディタ設定 (nvim) の変更、または新しい設定のシンボリックリンク追加時に使用します。
---

# Dotfiles Expert

このスキルは、この特定のリポジトリの構造と規約を理解するのに役立ちます。

## リポジトリ構造

- `config/`: 主要な設定ファイル。ツール別（fish, nvim, ghosttyなど）に整理されています。
- `scripts/setup-dotfiles.sh`: シンボリックリンク作成用の主要スクリプト。`create_symlink` 関数を使用します。
- `claude/`, `gemini/`: ツール固有のスキルディレクトリ。
- `git/`, `tmux/`, `docker/`, `vscode/`: 各ツールセットアップ用の `install.sh` を含むディレクトリ。

## 基本規約

- **シンボリックリンク**: すべての設定はリポジトリから `~/.config/` または `$HOME` へリンクされます。
- **Fish Shell**: プロジェクト名、Git ユーザー/ブランチ、ツールバージョン（Node, Rubyなど）を表示するカスタム `fish_prompt.fish` を使用します。
- **カラー**: "Carbonfox 風" の配色を優先します。
- **モジュール化**: ツールの設定はそれぞれの `config/<tool>` ディレクトリ内に分離して保持します。

## 共通ワークフロー

1. **新しい設定の追加**:
   - `config/` またはルートにディレクトリを作成。
   - スタンドアロンセットアップ用の `install.sh` を追加。
   - `scripts/setup-dotfiles.sh` に `create_symlink` の呼び出しを追加。
2. **Fish プロンプトの更新**:
   - `config/fish/functions/fish_prompt.fish` を修正。
   - カラー定数が Carbonfox テーマと一致していることを確認。
3. **Neovim の変更**:
   - 設定は `config/nvim/lua/my/` にあります。
   - プラグインは Lazy.nvim で管理されています。

詳細なコーディング基準やカラーコードについては、[references/conventions.md](references/conventions.md) を参照してください。
