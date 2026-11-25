---
name: slack-admin-cli-skill
description: >-
  Slack Admin CLI (`sladm`) を使って Slack Admin API / SCIM API を操作する。
  チーム管理・ユーザー管理・チャンネル管理・アプリ管理・ワークフロー管理・招待リクエスト管理・関数管理・SCIMユーザー/グループ管理など、
  Slack ワークスペースの管理操作を行いたいときに使う。
---

# Slack Admin CLI (sladm)

Slack Enterprise Grid / Business+ ワークスペースの管理 CLI。
`admin.*` スコープの API を直接叩けるため、Web UI では面倒な一括操作やスクリプト化が可能。

## CLI の使い方を調べる

CLI はセルフドキュメンティング。推測せず、必ず `--help` で確認すること。

```bash
sladm --help                          # トップレベルのコマンド一覧
sladm conversations --help            # conversations グループのサブコマンド一覧
sladm conversations search --help     # 個別コマンドのオプション詳細
```

## インストール

```bash
# Bun でグローバルインストール
bun link

# または直接実行
bun run src/index.ts
```

## 認証

```bash
# プロファイルにトークンを登録（キーチェーンに保存）
sladm token add <PROFILE_NAME> <xoxp-...>

# 登録済みプロファイル一覧
sladm token list

# トークンの有効性を確認
sladm token status
```

トークンには `admin.*` スコープが必要。環境変数 `SLADM_PROFILE` でデフォルトプロファイルを指定可能。

## 出力形式

すべてのコマンドで3種類の出力形式をサポート:

- `--json` — JSON 形式（パイプ処理向き）
- `--plain` — タブ区切りテキスト（TSV、スクリプト向き）
- デフォルト — 整形済みテーブル表示

## プロファイル切り替え

```bash
sladm --profile production teams list
sladm --profile staging users list
```

## コマンドグループ

| グループ | 用途 | レシピ |
|---------|------|--------|
| `token` | プロファイル・トークン管理 | — |
| `teams` | チーム作成・設定・管理者一覧 | [teams](recipes/teams.md) |
| `users` | ユーザー招待・昇格・セッション管理 | [users](recipes/users.md) |
| `conversations` | チャンネル操作・一括処理・アクセス制御 | [conversations](recipes/conversations.md) |
| `apps` | アプリ承認・制限・設定 | [apps](recipes/apps.md) |
| `invite-requests` | ワークスペース招待の承認・拒否 | [invite-requests](recipes/invite-requests.md) |
| `workflows` | ワークフロー検索・権限・コラボレーター | [workflows](recipes/workflows.md) |
| `functions` | カスタム関数の一覧・権限設定 | [functions](recipes/functions.md) |
| `scim-users` | SCIM ユーザー管理（作成・更新・無効化） | [scim-users](recipes/scim-users.md) |
| `scim-groups` | SCIM グループ管理（作成・更新・削除） | [scim-groups](recipes/scim-groups.md) |

## トラブルシューティング

- **`Token not found`**: `sladm token add` でトークンを登録する
- **`not_authed` / `invalid_auth`**: トークンが無効。`sladm token status` で確認
- **`missing_scope`**: トークンに必要な `admin.*` スコープがない
- **`not_an_admin`**: Enterprise Grid / Business+ の管理者権限が必要
- **配列パラメータ**: カンマ区切りで指定（例: `--channel-ids C1,C2,C3`）
