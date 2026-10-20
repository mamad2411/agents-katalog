---
allowed-tools: Bash(*), Read, Write, Edit, Glob, Grep, AskUserQuestion
description: リモートのVercelとSupabaseをセットアップする
---

## タスク

Vercel と Supabase のリモート環境をセットアップし、本番デプロイ可能な状態にする。
CLI でできることは CLI で行い、ブラウザ操作が必要な箇所はユーザーに明確に案内する。

各ステップで **コマンドの存在確認・ログイン状態確認を行い、未準備なら案内する**。ユーザーには進捗を都度報告する。

---

### Step 1: Vercel CLI 確認

`pnpm vercel --version` を実行して確認する。

- **正常にバージョンが表示される** → 次のステップへ
- **エラーの場合** → `vercel` がプロジェクトの `devDependencies` に入っていない。`pnpm add -Dw vercel` でルートにインストールする

> Vercel CLI はプロジェクトの devDependencies で管理する。グローバルインストールは不要。以降のステップでは `pnpm vercel` で実行する。

### Step 2: Vercel ログイン

`pnpm vercel whoami` でログイン状態を確認する。未ログインの場合:

- 「Vercel にログインします。ブラウザが開くので認証を完了してください」と案内する
- `pnpm vercel login` を実行する
- アカウントを持っていない場合は「https://vercel.com/signup でアカウントを作成してから再度このコマンドを実行してください」と案内して **終了する**

### Step 3: Vercel プロジェクトのリンク

`.vercel/project.json` が存在するか確認する。

- **存在しない場合**: ユーザーに「新規プロジェクトを作成しますか？既存プロジェクトにリンクしますか？」と AskUserQuestion で確認する
  - 新規作成: `pnpm vercel project add {プロジェクト名}` でプロジェクトを作成した後 `pnpm vercel link` を実行する。プロジェクト名はリポジトリのディレクトリ名をデフォルトとして提案する
  - 既存リンク: `pnpm vercel link` を実行する（対話プロンプトでユーザーが選択）
- **存在する場合**: 「既に Vercel プロジェクトにリンク済みです」と報告してスキップ

### Step 4: Vercel プロジェクト設定

Vercel のプロジェクト設定を確認・更新する:

```bash
# Root Directory の設定
# pnpm vercel link 時に Root Directory を聞かれるので apps/webapp を指定する
# もし設定が漏れていたら Vercel ダッシュボードでの手動設定を案内する
```

ユーザーに以下の設定を確認・案内する:

| 項目 | 値 |
|---|---|
| Framework Preset | Next.js |
| Root Directory | `apps/webapp` |
| Build Command | `pnpm build:vercel` |
| Install Command | `pnpm install --frozen-lockfile` |

> これらは `pnpm vercel link` 時の対話で設定されるが、確認として表示する。もし変更が必要な場合は Vercel ダッシュボード (Settings → General) での変更を案内する。

### Step 5: Supabase CLI 確認

`pnpm supabase --version` を実行して確認する。

- **正常にバージョンが表示される** → 次のステップへ
- **エラーの場合** → ビルドスクリプトが未許可。ユーザーに「ターミナルで `pnpm approve-builds` を実行して、supabase にチェックを入れてください。完了後にもう一度このコマンドを実行してください」と案内して **終了する**

> `pnpm approve-builds` はインタラクティブなプロンプトのため、自動実行できない。

### Step 6: Supabase CLI ログイン

`pnpm supabase projects list` を実行してログイン状態を確認する。未ログインまたはエラーの場合:

- 「Supabase にログインします」と案内する
- `pnpm supabase login` を実行する（ブラウザでトークン認証）
- アカウントを持っていない場合は「https://supabase.com/dashboard でアカウントを作成してから再度このコマンドを実行してください」と案内して **終了する**

### Step 7: Supabase リモートプロジェクトのリンク

`supabase/config.toml` 内に `[remotes.production]` セクションがあるか、または `.supabase` ディレクトリにリンク情報があるか確認する。

- **未リンクの場合**: ユーザーに「新規プロジェクトを作成しますか？既存プロジェクトにリンクしますか？」と AskUserQuestion で確認する
  - **新規作成**:
    1. 「Supabase ダッシュボード https://supabase.com/dashboard/new にアクセスして新しいプロジェクトを作成してください」と案内する
    2. 「作成時に設定した **DB パスワード** を控えておいてください（後で環境変数に使います）」と注意する
    3. 「プロジェクトの作成が完了したら、Settings → General にある **Reference ID** を教えてください」と AskUserQuestion で聞く
    4. 教えてもらった Reference ID で `pnpm supabase link --project-ref {ref}` を実行する
  - **既存リンク**:
    1. `pnpm supabase projects list` でプロジェクト一覧を表示する
    2. ユーザーにリンク先のプロジェクトを AskUserQuestion で確認する
    3. `pnpm supabase link --project-ref {ref}` を実行する
- **リンク済みの場合**: 「既に Supabase プロジェクトにリンク済みです」と報告してスキップ

### Step 8: リモート DB マイグレーション

リモート DB にマイグレーションを適用する。

1. ユーザーに「リモート DB にマイグレーションを適用しますか？」と AskUserQuestion で確認する
2. 了承を得たら、リモートの DATABASE_URL を取得する:
   - `pnpm supabase projects list` と `pnpm supabase link` の情報から接続先を特定する
   - ユーザーに「Supabase ダッシュボード → Settings → Database → Connection string (URI) から接続文字列を教えてください（パスワード部分は実際の DB パスワードに置き換えたもの）」と AskUserQuestion で聞く
3. 接続文字列を使って Prisma マイグレーションを実行する:

```bash
cd apps/webapp && DATABASE_URL="{接続文字列}" DIRECT_URL="{接続文字列}" pnpm prisma migrate deploy
```

> `migrate deploy` は本番環境用コマンド。`migrate dev` と異なり新規マイグレーションの生成は行わない。

### Step 9: Vercel 環境変数の設定

Vercel に必要な環境変数を設定する。

1. `pnpm vercel env ls` で現在の環境変数を確認する
2. 未設定の環境変数をユーザーに案内し、設定する:

| 変数名 | 説明 | 設定方法 |
|---|---|---|
| `DATABASE_URL` | Supabase 接続文字列（Pooler / Transaction mode） | Step 8 で取得した接続文字列を使用 |
| `DIRECT_URL` | Supabase 直接接続文字列（Session mode） | Supabase ダッシュボードから取得 |

- 接続文字列を AskUserQuestion でユーザーに確認する（Step 8 で既に取得済みなら再利用）
- **DATABASE_URL** は Supabase ダッシュボードの Connection string で **Transaction mode (port 6543)** のものを使用する
- **DIRECT_URL** は **Session mode (port 5432)** のものを使用する
- `pnpm vercel env add DATABASE_URL production` で設定する（stdin からの値入力）
- `pnpm vercel env add DIRECT_URL production` で設定する
- その他の環境変数（`ANTHROPIC_API_KEY` 等）があれば、ユーザーに追加で設定が必要かを確認する

> **注意**: 環境変数の値にはパスワードが含まれるため、コマンド実行時に値が表示されることをユーザーに伝える。

### Step 10: デプロイ確認

1. ユーザーに「初回デプロイを実行しますか？」と AskUserQuestion で確認する
2. 了承を得たら `pnpm vercel deploy --prod` を実行する
3. デプロイが完了したら、表示された URL をユーザーに報告する
4. もしデプロイエラーが出た場合は、`pnpm vercel logs` でログを確認し、原因を報告する

---

### 完了報告

以下をユーザーに報告する:

- Vercel プロジェクト URL（ダッシュボードリンク）
- 本番デプロイ URL
- Supabase プロジェクト Reference ID
- 設定した環境変数の一覧（値は伏せる）
- 「以降は main ブランチへの push で自動デプロイされます」という案内
- 「PR を作成すると Preview デプロイが自動生成されます」という案内
