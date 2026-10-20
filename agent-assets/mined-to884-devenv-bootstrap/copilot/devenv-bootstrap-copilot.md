# GitHub Copilot 指示書 - Dev Environment Bootstrap

## プロジェクト概要

このリポジトリは、Linux環境でAnsibleを迅速にセットアップするためのブートストラップスクリプト群を提供します。クロスディストリビューション対応、防御的プログラミング、べき等性を重視した安全なインストールを実現します。

### 主要な目的

- Gitリポジトリクローン後の初回セットアップを自動化
- 複数のLinuxディストリビューション（Ubuntu/Debian、RHEL/CentOS/Fedora、Arch）で動作
- 様々な実行環境（WSL、Hyper-V、Azure VM、EC2、Docker）をサポート
- システムPythonを汚染しない仮想環境へのインストール
- 繰り返し実行しても安全なべき等性の保証

## コーディング規約

### 改行コード

- **LF (Line Feed)** を使用してください。CRLFは使用しないでください。

### Bashスクリプトの基本原則

**このプロジェクトは既存のAgent Skillに従います:**

- **`.agents/skills/bash-defensive-patterns/SKILL.md`** - 防御的プログラミングの全原則
  - 厳格モード (`set -Eeuo pipefail`)
  - エラートラップとクリーンアップ
  - 変数の安全な使用
  - 配列の安全な使用
  - 条件分岐の安全性
  
- **`.agents/skills/bash-pro/SKILL.md`** - プロフェッショナルなbashスクリプティング
  - プラットフォーム検出
  - ロギングパターン
  - エラーハンドリング

- **`.agents/skills/bash-scripting/SKILL.md`** - スクリプティングワークフロー

**これらのスキルで定義されているすべての原則を適用してください。**

### プロジェクト固有のパターン

#### プラットフォーム検出

このプロジェクトは3大Linuxディストリビューション系列をサポート:
- Ubuntu/Debian (apt)
- RHEL/CentOS/Fedora (dnf/yum)
- Arch Linux (pacman)

以下の実行環境で動作確認済み:
- WSL (Windows Subsystem for Linux) 1/2
- Hyper-V 仮想マシン
- Azure VM (Linux Virtual Machines)
- AWS EC2 (Linux instances)
- Docker コンテナ
- ベアメタル Linux サーバー

プラットフォーム検出は `/etc/os-release` を優先的に使用し、フォールバックを実装してください。
詳細なパターンは bash-pro スキルを参照。

#### Dry-Runモード

すべての破壊的操作は dry-run モードをサポートすること（実装パターンは bash-defensive-patterns スキル参照）:

**dry-run でも実行すべき操作**:
- 読み取り専用の検出処理（プラットフォーム、バージョン）
- 依存関係チェック
- 既存インストールの確認

**dry-run でスキップすべき操作**:
- ファイル・ディレクトリの作成/削除
- パッケージのインストール
- システム設定の変更

#### べき等性

すべてのインストール/セットアップスクリプトは繰り返し実行可能であること。
詳細なパターンは bash-defensive-patterns スキルの Pattern 8 を参照。

#### ロギング

```bash
log_info "処理を開始します"        # 一般的な情報
log_success "インストール完了"      # 成功メッセージ
log_error "失敗しました"            # エラーメッセージ
log_warning "警告: 推奨されません"  # 警告
log_debug "変数の値: $var"          # デバッグ情報（--verbose時のみ）
```

**重要**:
- すべてのメッセージは日本語で記述すること。例: `"インストール完了"`
- 例外：
  - ログ関数の引数は英語で記述しても構いませんが、出力されるメッセージは日本語でなければなりません。
  - "[dry-run]" タグは英語のままで構いません。


## ドキュメントと言語規約

### 日本語の使用（最重要）

このプロジェクトでは**すべてのドキュメント、コメント、ログメッセージを日本語で記述**します。

英語コメントは使用しないでください。

### スクリプトヘッダー

すべてのbashスクリプトには詳細な日本語ヘッダーを記述:

```bash
# ============================================================================
# [スクリプト名]
# ============================================================================
#
# 目的:
#   このスクリプトの目的を簡潔に説明
#
# 対応ディストリビューション:
#   - Ubuntu/Debian (apt)
#   - RHEL/CentOS/Fedora (dnf/yum)
#
# 使用方法:
#   ./script.sh [オプション]
#
# オプション:
#   -d, --dry-run   実際の変更を行わず、実行内容を表示
#
# 必要要件:
#   - Python 3.8 以上
#
# 終了コード:
#   0 - 成功
#   1 - エラー
#
# 使用例:
#   ./script.sh --dry-run
#
# ============================================================================
```

### README.md の構造

日本語でユーザーフレンドリーなREADMEを作成:

- 📋 概要
- ✨ 特徴（絵文字で視認性向上）
- 🚀 クイックスタート
- 📖 使用方法
- 📋 前提条件
- 🎯 インストール後の使用方法
- 🔍 トラブルシューティング
- 🔒 セキュリティ
- 📊 終了コード

## Git 規約

### Git Discipline Skill の遵守

このプロジェクトでは **`.github/skills/git-discipline/SKILL.md`** で定義されているすべてのGit規約を遵守します。

### ブランチ命名規則

ブランチ名は以下の形式に従うこと：

```
<type>/<short-description>
```

**許可される type:**
- ✨ feature - 新機能
- 🐛 fix - バグ修正
- 🚑 hotfix - 緊急修正
- ♻️ refactor - リファクタリング
- 🔧 chore - 雑務（ビルド、ツール等）
- 📝 docs - ドキュメント
- ✅ test - テスト

**例:**
- `feature/add-user-auth`
- `fix/handle-null-response`
- `docs/update-readme`

### Conventional Commits

すべてのコミットメッセージは Conventional Commits 形式に従い、**日本語で記述**すること：

```
<type>(<scope>): <日本語の説明>
```

**許可される type:**
- ✨ feat - 新機能
- 🐛 fix - バグ修正
- 📝 docs - ドキュメント変更
- 💄 style - フォーマット、リント
- ♻️ refactor - リファクタリング
- ⚡ perf - パフォーマンス改善
- ✅ test - テスト追加・修正
- 🔧 chore - ビルド、CI、ツール

**例:**
```
feat(ansible): Linuxbrewインストールロールを追加
fix(bootstrap): Python仮想環境の検出ロジックを修正
docs(readme): セットアップ手順を更新
chore(ci): ShellCheckワークフローを追加
```

### プルリクエスト

**タイトル:**
- Conventional Commits 形式に従うこと
- 日本語で記述すること

**説明:**
- 日本語で記述すること
- 以下の構造を推奨：

```markdown
## 変更対象
- 何を変更したか

## 変更理由
- なぜ変更が必要だったか

## 変更方法
- 実装の概要

## 関連
- 関連する issue やチケット（任意）
```

**例:**

タイトル: `feat(ansible): WSL環境の自動検出機能を追加`

説明:
```markdown
## 変更対象
- WSL環境の自動検出ロジックを追加
- wsl ロールにWSL固有の設定を追加

## 変更理由
- WSL特有の設定（WSLg、systemd）を自動的に適用するため

## 変更方法
- /proc/version から WSL を検出
- 環境変数 WSL_DISTRO_NAME を確認
```

## テストとバリデーション

### 必須テスト

1. **ShellCheck**: `shellcheck bootstrap.sh`
2. **Dry-Run**: `./bootstrap.sh --dry-run --verbose`
3. **べき等性**: 同じ環境で2回連続実行し、2回目が安全にスキップされることを確認
4. **クロスディストリビューション**: Docker で Ubuntu/Fedora/Arch でテスト
5. **実行環境テスト**: 可能であればWSL、Azure VM、EC2などの実環境でテスト

## プロジェクト固有のパターン

### Python仮想環境の管理

デフォルトパス: `${SCRIPT_DIR}/.ansible-venv` (リポジトリ直下)

```bash
VENV_PATH="${VENV_PATH:-${SCRIPT_DIR}/.ansible-venv}"

# べき等性: 既存チェック後に作成
if [[ ! -d "$VENV_PATH" ]]; then
    python3 -m venv "$VENV_PATH"
else
    log_info "仮想環境は既に存在します: $VENV_PATH"
fi
```

### バージョンチェック

Python 3.8以上を要求:

```bash
check_python_version() {
    local python_version
    python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    
    local version_major version_minor
    version_major=$(echo "$python_version" | cut -d. -f1)
    version_minor=$(echo "$python_version" | cut -d. -f2)
    
    if [[ $version_major -lt 3 ]] || [[ $version_major -eq 3 && $version_minor -lt 8 ]]; then
        log_error "Pythonバージョン $python_version は古すぎます"
        exit 5
    fi
}
```

### 終了コード

標準化された終了コード:

- `0` - 成功
- `1` - 一般的なエラー
- `2` - 不正な引数
- `3` - サポート外のプラットフォーム
- `4` - 依存関係の不足
- `5` - Pythonバージョンが古い
- `6` - rootユーザーで実行（禁止）

## GitHub Copilot に期待する動作

### 必須スキルの適用

**コード生成時は必ず以下のスキルを参照してください:**

- **`.agents/skills/bash-defensive-patterns/SKILL.md`** - すべての防御的プログラミング技法
- **`.agents/skills/bash-pro/SKILL.md`** - プロフェッショナルなスクリプティングパターン
- **`.agents/skills/bash-scripting/SKILL.md`** - スクリプティングワークフロー

### プロジェクト固有の要件

上記のスキルに加えて、以下のプロジェクト固有の要件を適用:

#### コード生成時
1. **日本語でコメントとログを記述** （最重要）
2. **dry-run モードをサポート** - すべての破壊的操作で実装
3. **べき等性を考慮** - 繰り返し実行しても安全
4. **プラットフォーム検出パターンに従う** - 3大ディストリビューション対応

#### リファクタリング時
1. 既存のログ関数パターンを維持
2. コメントを日本語で充実
3. ShellCheck の警告をゼロに

#### 新機能追加時
1. 既存の `bootstrap.sh` のパターンに従う
2. README.md に日本語で説明を追加
3. dry-run と verbose モードをサポート
4. べき等性を保証
5. 終了コードを適切に設定

## Ansible プロジェクト構造

### ディレクトリ構成

Ansibleプロジェクトは環境別インベントリ構造を採用しています:

```
ansible/
├── ansible.cfg                      # Ansible設定
├── site.yml                         # メインエントリーポイント
├── group_vars/
│   └── all.yml                      # グローバル変数
├── inventories/                     # 環境別インベントリ
│   ├── wsl/hosts                    # WSL環境
│   ├── azure-vm/hosts               # Azure VM環境
│   ├── ec2/hosts                    # EC2環境
│   ├── hyperv/hosts                 # Hyper-V環境
│   ├── baremetal/hosts              # ベアメタル環境
│   └── docker/hosts                 # Docker環境
├── playbooks/
│   ├── bootstrap.yml                # メインブートストラップ
│   └── containers.yml               # コンテナ専用
└── roles/
    ├── sudo/                        # sudoers設定
    ├── common/                      # 共通パッケージ + Linuxbrew
    ├── ssh/                         # SSH設定
    └── {環境名}/                    # 環境固有ロール
```

### Ansible コーディング規約

#### YAML ファイル

- **インデント**: スペース2個
- **コメント**: 日本語で記述
- **name属性**: すべてのタスクに日本語の説明的な名前を付ける
- **tags**: 適切なタグを付与（sudo, security, common, packages, 等）

#### Playbook ヘッダー

すべてのPlaybookには日本語のヘッダーコメントを記述:

```yaml
---
# ============================================================================
# [Playbook名]
# ============================================================================
#
# 目的:
#   このPlaybookの目的を簡潔に説明
#
# 使用方法:
#   ansible-playbook -i inventories/wsl/hosts playbooks/example.yml
#
# Dry-run:
#   ansible-playbook -i inventories/wsl/hosts playbooks/example.yml --check
#
# ============================================================================
```

#### ロールの構造

- **タスク**: `roles/{role_name}/tasks/main.yml`
- **べき等性**: すべてのタスクは繰り返し実行しても安全であること
- **条件分岐**: `when` を使用して環境やディストリビューションに応じた処理

#### Homebrewパッケージのインストール

Linuxbrewを使用したパッケージインストールには、**`community.general.homebrew`モジュールを使用すること**。

**推奨される方法:**

```yaml
- name: パッケージをインストール
  community.general.homebrew:
    name: package-name
    state: present
    path: /home/linuxbrew/.linuxbrew/bin/brew
  environment:
    PATH: "/home/linuxbrew/.linuxbrew/bin:{{ ansible_env.PATH }}"
```

**非推奨（使用しない）:**

```yaml
# ❌ brewコマンドを直接呼び出さないこと
- name: パッケージをインストール
  ansible.builtin.command: /home/linuxbrew/.linuxbrew/bin/brew install package-name
```

**理由:**
- ✅ **べき等性の自動保証** - モジュールが既存インストールを自動チェック
- ✅ **changed状態の正確な報告** - インストール済みなら`changed=false`
- ✅ **エラーハンドリングの改善** - 適切なエラーメッセージと失敗処理
- ✅ **Ansibleのベストプラクティス** - コマンドより専用モジュールを優先

#### Git設定の管理

Git設定の変更には、**`community.general.git_config`モジュールを使用すること**。

**推奨される方法:**

```yaml
- name: Git に設定を追加
  community.general.git_config:
    name: user.name
    scope: global
    value: "Your Name"
  become: no
```

**非推奨（使用しない）:**

```yaml
# ❌ git configコマンドを直接呼び出さないこと
- name: Git に設定を追加
  ansible.builtin.command: git config --global user.name "Your Name"
```

**理由:**
- ✅ **べき等性の自動保証** - 既存の設定値をチェックし、変更が必要な場合のみ更新
- ✅ **changed状態の正確な報告** - 設定が既に同じ値ならば`changed=false`
- ✅ **スコープの明示的な管理** - `global`, `system`, `local`を明確に指定可能
- ✅ **Ansibleのベストプラクティス** - コマンドより専用モジュールを優先

#### pipパッケージのインストール

Pythonパッケージのインストールには、**`ansible.builtin.pip`モジュールを使用し、ユーザースコープでインストールすること**。

**推奨される方法:**

```yaml
- name: Python パッケージをインストール
  ansible.builtin.pip:
    name:
      - package-name
      - another-package
    state: present
    executable: pip3
    extra_args: --user
  become: no
```

**非推奨（使用しない）:**

```yaml
# ❌ システムスコープでインストールしないこと
- name: Python パッケージをインストール
  ansible.builtin.pip:
    name: package-name
    state: present
    executable: pip3
  become: yes

# ❌ pipコマンドを直接呼び出さないこと
- name: Python パッケージをインストール
  ansible.builtin.command: pip3 install package-name
```

**理由:**
- ✅ **システム汚染の回避** - システムのPythonパッケージを汚染しない
- ✅ **権限不要** - sudo権限が不要で、セキュリティリスクを低減
- ✅ **ユーザー独立性** - ユーザーごとに独立した環境を維持
- ✅ **べき等性の自動保証** - モジュールが既存インストールを自動チェック
- ✅ **Ansibleのベストプラクティス** - コマンドより専用モジュールを優先

**注意:**
- 仮想環境（venv）内でインストールする場合は `extra_args: --user` は不要です
- システム全体で必要なパッケージの場合のみ、明示的な理由とともに `become: yes` を使用してください

#### 環境固有の処理

- **インベントリ変数**: `environment_type`, `cloud_provider` などを使用
- **ホストグループ**: 環境ごとにグループを定義（wsl, azure_vm, ec2, 等）
- **条件付きロール**: playbook内で環境に応じてロールを適用

### Ansible ベストプラクティス

1. **コマンド実行の確認**: `ansible-playbook --syntax-check` で構文チェック
2. **Dry-run**: `--check` フラグで実行前確認
3. **タグ活用**: 部分実行を可能にするタグ設定
4. **セキュリティ**: sudoers編集は `visudo -c` で検証
5. **ログ**: ansible.cfg でログを有効化

### Ansible プロジェクトへの変更時

1. **新規ロール作成時**:
   - `roles/{role_name}/tasks/main.yml` を作成
   - 日本語のタスク名とコメント
   - 適切なタグを付与
   - べき等性を確保

2. **新規環境追加時**:
   - `inventories/{env_name}/hosts` を作成
   - `roles/{env_name}/tasks/main.yml` を作成
   - `playbooks/bootstrap.yml` にplayを追加

3. **README更新**:
   - `ansible/README.md` に日本語で説明を追加
   - 使用例とコマンドを含める
