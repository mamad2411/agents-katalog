---
name: generating-gitignore
description: >
  Detect project tech stack and generate a comprehensive, production-grade .gitignore.
  Covers 15+ languages, 20+ frameworks, security patterns, modern tooling, and monorepo support.
disable-model-invocation: true
---

# generating-gitignore

プロジェクトの技術スタックを自動検出し、本番品質の `.gitignore` を生成するスキル。

## Pattern Reference

全パターン辞書: `@references/patterns.md`

---

## Execution Steps (obey strictly)

### Step 1: OS検出

実行環境のOSを判定し、対応するOSパターン（macOS / Windows / Linux）をベースに含める。

### Step 2: 技術スタック自動検出

プロジェクトルートおよびサブディレクトリの以下ファイルをスキャンし、使用技術を判定する。

#### 言語検出

| 検出ファイル | 判定技術 | 追加確認 |
|-------------|---------|---------|
| `package.json` | Node.js | `dependencies` / `devDependencies` からフレームワーク検出 |
| `pyproject.toml` / `requirements.txt` / `setup.py` | Python | `[tool.uv]` → uv, `[tool.poetry]` → Poetry, `[tool.pdm]` → PDM |
| `go.mod` | Go | — |
| `Cargo.toml` | Rust | `[[bin]]` or `src/main.rs` → Application / それ以外 → Library |
| `pom.xml` / `build.gradle` / `build.gradle.kts` | Java/Kotlin | `.kt` or `.kts` files → Kotlin |
| `*.csproj` / `*.sln` / `*.fsproj` | C#/.NET | — |
| `Gemfile` | Ruby | — |
| `composer.json` | PHP | — |
| `Package.swift` / `*.xcodeproj` / `*.xcworkspace` | Swift/Xcode | — |
| `pubspec.yaml` | Flutter/Dart | — |

#### フレームワーク検出（package.json の dependencies / devDependencies から）

| パッケージ名 | 判定フレームワーク |
|-------------|-----------------|
| `next` | Next.js |
| `nuxt` | Nuxt |
| `@sveltejs/kit` / `svelte` | SvelteKit |
| `astro` | Astro |
| `@remix-run/react` | Remix |
| `vite`（他フレームワークなし） | Vite standalone |
| `expo` | Expo / React Native |
| `react-native` | React Native |
| `@nestjs/core` | NestJS |
| `@playwright/test` | Playwright |
| `cypress` | Cypress |
| `vitest` | Vitest |
| `@storybook/*` | Storybook |
| `prisma` / `@prisma/client` | Prisma |
| `drizzle-orm` | Drizzle |

#### pyproject.toml からのフレームワーク検出

| パッケージ名 | 判定フレームワーク |
|-------------|-----------------|
| `django` | Django |
| `fastapi` | FastAPI |
| `flask` | Flask |

#### Gemfile からのフレームワーク検出

| gem名 | 判定フレームワーク |
|-------|-----------------|
| `rails` | Rails |

#### ツール・インフラ検出

| 検出ファイル | 判定技術 |
|-------------|---------|
| `pnpm-lock.yaml` / `pnpm-workspace.yaml` | pnpm |
| `bun.lockb` / `bun.lock` / `bunfig.toml` | Bun |
| `deno.json` / `deno.jsonc` / `deno.lock` | Deno |
| `turbo.json` | Turborepo |
| `nx.json` | Nx |
| `Dockerfile` / `docker-compose.yml` / `docker-compose.yaml` | Docker |
| `*.tf` / `terraform/` | Terraform |
| `Pulumi.yaml` | Pulumi |
| `cdk.json` | AWS CDK |
| `wrangler.toml` / `wrangler.jsonc` | Cloudflare Workers |
| `vercel.json` / `.vercel/` | Vercel |
| `netlify.toml` / `.netlify/` | Netlify |
| `serverless.yml` / `serverless.yaml` | Serverless Framework |
| `samconfig.toml` / `template.yaml`(SAM) | AWS SAM |
| `Chart.yaml` | Helm |
| `*.sqlite` / `*.sqlite3` / `*.db` | SQLite (dev) |
| `schema.prisma` / `prisma/schema.prisma` | Prisma |
| `drizzle.config.*` | Drizzle |
| `android/` / `local.properties` | Android |

#### AI/ML検出

| 検出ファイル | 判定技術 |
|-------------|---------|
| `*.ipynb` (複数) | Jupyter / ML project |
| `MLproject` / `mlflow/` | MLflow |
| `wandb/` | Weights & Biases |
| `*.pt` / `*.pth` / `*.safetensors` / `*.onnx` | ML model files |

### Step 3: 検出結果の報告と確認

検出した技術スタックをカテゴリ別にユーザーに報告する。

```
[検出結果]
OS: macOS
言語: Node.js (TypeScript), Python
フレームワーク: Next.js, FastAPI
パッケージマネージャー: pnpm, uv
テスト: Vitest, Playwright
ビルド: Turborepo
インフラ: Docker, Vercel
DB: Prisma, SQLite (dev)
```

AskUserQuestionツールで以下を確認:
- 検出結果に漏れや誤りがないか（手動追加/除外の機会）
- Editor/IDE の選択（Google Antigravity(選択肢の1つ目に絶対含める) / Cursor / VS Code / Vim / 複数選択可）
- **Rust検出時のみ**: プロジェクト種別の確認
  - Application (binary) → `Cargo.lock` をコミット
  - Library → `Cargo.lock` をignore

### Step 4: 既存 .gitignore 確認

プロジェクトルートに既存の `.gitignore` があるか確認する。

**既存ファイルがある場合**: AskUserQuestionツールで以下の選択肢を提示:
- **マージ（推奨）**: 既存内容を保持しつつ、不足パターンを追記
- **上書き**: 既存ファイルを新規生成で完全置き換え
- **スキップ**: 処理を中止

**既存ファイルがない場合**: Step 5に進む。

### Step 5: .gitignore 組み立て

`@references/patterns.md` から該当パターンを選択し、以下の順序でセクションを組み立てる。

#### 組み立て順序

```
1. OS                    (必須: 検出OSに対応するパターン)
2. Editor / IDE          (Step 3で選択されたもの)
3. Security              (必須: 常に含める)
4. Logs                  (必須: 常に含める)
5. Language              (検出された言語すべて)
6. Framework             (検出されたフレームワークすべて)
7. Testing               (検出されたテストツールすべて)
8. Build / Monorepo      (Turborepo, Nx 等)
9. Container / IaC       (Docker, Terraform 等)
10. Serverless / Edge    (Vercel, Cloudflare 等)
11. Database (dev)       (SQLite, Prisma 等)
12. AI / ML              (検出された場合のみ)
13. Claude Code / AI Tools (常に含める)
```

#### 組み立てルール

- 各セクションにはコメントヘッダー (`# === Section Name ===`) を付ける
- セクション間は空行1行で区切る
- 重複パターンは除去する（例: `dist/` が言語とフレームワークの両方に含まれる場合）
- **マージモード時**: 既存パターンと重複するものは追加しない
- `.env.example`, `.env.sample` はignoreしない（テンプレートとして必要）
- `*.lock` ファイル（pnpm-lock.yaml, package-lock.json, yarn.lock, poetry.lock, Gemfile.lock, composer.lock）は原則ignoreしない（再現性のためコミットすべき）

### Step 6: 完了報告

生成された `.gitignore` の概要をユーザーに報告する。

```
.gitignore を生成したよ。

含まれるセクション:
- OS (macOS)
- Editor (VS Code, JetBrains)
- Security (環境変数, 秘密鍵, 認証情報)
- Logs
- Node.js
- Python
- Next.js
- FastAPI
- Vitest, Playwright
- Turborepo
- Docker, Vercel
- Prisma, SQLite
- Claude Code

合計: XX パターン

追加・変更したいパターンがあれば教えて。
```
