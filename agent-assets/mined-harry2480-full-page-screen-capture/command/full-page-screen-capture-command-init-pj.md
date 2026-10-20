---
allowed-tools: Bash(*), Read, Write, Edit, Glob, Grep
description: プロジェクトの初期セットアップ（前提ツールのインストールからDB構築まで）
---

## タスク

Mac をクリーンインストールした直後の人でもプロジェクトを動かせるよう、前提ツールの確認・インストールからDB構築・開発サーバー起動までを一気通貫で行う。

各ステップで **コマンドの存在確認を行い、未インストールなら案内またはインストールする**。ユーザーには進捗を都度報告し、何をやっているか分かるようにする。

---

### Step 1: Homebrew

`brew --version` で確認する。未インストールの場合:

- 「Homebrew がインストールされていません。インストールしますか？」とユーザーに確認する
- 了承を得たら `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"` を実行する
- インストール後、シェルのパスが通っているか `brew --version` で再確認する。パスが通っていなければ `eval "$(/opt/homebrew/bin/brew shellenv)"` を案内する

### Step 2: Node.js

`node --version` で確認する。未インストール、または v22 未満の場合:

- `brew install node@22` でインストールする
- インストール後 `node --version` で v22 以上であることを確認する

### Step 3: pnpm

`pnpm --version` で確認する。未インストールの場合:

- `corepack enable && corepack prepare pnpm@latest --activate` でインストールする
- corepack が使えない場合は `npm install -g pnpm` にフォールバックする

### Step 4: Docker

`docker info` で確認する。Docker デーモンが起動していない、または未インストールの場合:

- **未インストール**: 「Docker Desktop をインストールしてください: https://www.docker.com/products/docker-desktop/ 」と案内して、インストール完了後に再度このコマンドを実行するよう伝えて **終了する**
- **インストール済みだが未起動**: 「Docker Desktop を起動してください」と案内して **終了する**

> Docker Desktop は GUI インストールが必要なため、自動インストールは行わない。

### Step 5: 依存パッケージのインストール

`node_modules/` が存在するか確認する。なければ `pnpm install` を実行する。

インストール後、`pnpm supabase --version` を実行して Supabase CLI が使えるか確認する。
エラーになる場合はビルドスクリプトが未許可なので、ユーザーに以下を案内して **終了する**:

- 「ターミナルで `pnpm approve-builds` を実行して、supabase にチェックを入れてください。完了後にもう一度このコマンドを実行してください」

> `pnpm approve-builds` はインタラクティブなプロンプトのため、自動実行できない。

### Step 6: Supabase の初期化と起動

1. `supabase/config.toml` が存在しない場合のみ `pnpm supabase init` を実行する（対話プロンプトにはすべて N で回答）
2. `project_id` の設定: リポジトリのディレクトリ名から自動でプロジェクト名を提案し、ユーザーに確認する（AskUserQuestion を使う）。
   - 例: ディレクトリ名が `my-awesome-app` なら「プロジェクト名を `my-awesome-app` にしますか？変更する場合は入力してください」と聞く
   - 確定した名前で `supabase/config.toml` の `project_id` を更新する
   - `project_id` は英数字とハイフンのみ（スペースやアンダースコアはハイフンに変換する）
3. `pnpm supabase start` を実行する。ポート競合エラーが出た場合は:
   - `supabase/config.toml` 内の全ポートを **+1000** ずつオフセットする（例: 54321 → 55321）
   - 対象ポート: `[api] port`, `[db] port`, `[db] shadow_port`, `[db.pooler] port`, `[studio] port`, `[inbucket] port`, `[analytics] port`, `[edge_runtime] inspector_port`
   - 再度 `pnpm supabase start` を試みる（最大3回）

### Step 7: `.env.local` の生成

`apps/webapp/.env.local` を作成する。DB ポートは `supabase/config.toml` の `[db] port` の値を使う。

```
DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:{db_port}/postgres"
DIRECT_URL="postgresql://postgres:postgres@127.0.0.1:{db_port}/postgres"
```

既に `.env.local` が存在する場合は、`DATABASE_URL` と `DIRECT_URL` の行だけ更新し、他の環境変数（`ANTHROPIC_API_KEY` 等）は保持する。

### Step 8: マイグレーション実行

環境変数を export してから実行する。

```bash
export DATABASE_URL="postgresql://postgres:postgres@127.0.0.1:{db_port}/postgres"
export DIRECT_URL="postgresql://postgres:postgres@127.0.0.1:{db_port}/postgres"
cd apps/webapp && pnpm prisma migrate dev --name init
```

既にマイグレーション済みの場合は `pnpm prisma migrate dev` のみ（`--name` なし）で差分適用する。

### Step 9: シード投入

同じ環境変数を export した状態で実行する。

```bash
pnpm prisma db seed
```

### Step 10: 動作確認

`pnpm dev` を起動して http://localhost:3000 にアクセスできることを確認する。

---

### 完了報告

以下をユーザーに報告する:

- インストールしたツールの一覧（新規インストールしたもののみ）
- Supabase Studio の URL（例: http://127.0.0.1:55323）
- アプリの URL（http://localhost:3000）
- DB ポート番号
- 「`pnpm dev` で開発サーバーを起動できます」という案内
