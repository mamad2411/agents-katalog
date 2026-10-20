# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Communication

- 日本語で会話する。英語は技術用語のみ許可
- タメ口で話す。敬語禁止
- 出力は端的に最小限。冗長な説明・前置き・言い訳は不要
- 聞かれたことだけ答える。勝手に話を広げない

---

## Architecture

モノレポ構成。4つのパッケージで構成:

| Package | Stack | Purpose |
|---------|-------|---------|
| `apps/web` | Next.js 16 (App Router) + TypeScript + Tailwind v4 | LP + ダッシュボード |
| `apps/api` | FastAPI + Python 3.11+ | REST API、Stripe決済、ジョブ管理 |
| `apps/worker` | Python 3.11 + PyTorch + Transformers 5.x + TRL | GPU学習ワーカー（Modal Serverless） |
| `packages/shared` | TypeScript | 型定義・定数 |

### Key Flows

**決済→学習フロー:**
1. `/payments/checkout` → Stripe Checkout Session作成（880円、JPY zero-decimal）
2. Stripe Webhook (`checkout.session.completed`) → 金額検証 → training_jobs作成 → Modal Webhook投入
3. `/train` エンドポイントは決済確認済みのプロジェクトのみ実行可

**i18n 2系統:**
- LP: cookie + Next.js middleware (`src/i18n/translations.ts`)
- ダッシュボード: React Context + `useLocale()` (`src/lib/i18n.tsx`)

### Infrastructure

- Deploy: Vercel (web) / Render (api) / Modal Serverless (worker)
- DB: Supabase (PostgreSQL + Auth + Storage)
- Payment: Stripe (inline price_data, JPY zero-decimal)

---

## Build & Dev Commands

### Web (apps/web)
```bash
cd apps/web
npm run dev      # dev server (turbopack)
npm run build    # production build
npm run lint     # eslint
npx tsc --noEmit # type check
```

### API (apps/api)
```bash
cd apps/api
uvicorn app.main:app --reload     # dev server
pytest                             # run tests
pytest --cov=app --cov-report=term # with coverage
```

### Worker (apps/worker)
```bash
cd apps/worker
modal deploy modal_app.py  # deploy to Modal
```

---

## Core Principles

- **Simplicity First**: 変更は可能な限りシンプルに。影響範囲を最小化する
- **No Laziness**: 根本原因を探す。一時的な修正禁止。シニアエンジニア基準
- **Staff Engineer Test**: 「スタッフエンジニアがこれを承認するか？」を常に自問する

### Safety Gate
- 本番環境への変更は「本番デプロイ承認」の明示的な承認が必要
- 不可逆な操作（DB マイグレーション、本番デプロイ等）は必ず確認を取る

---

## Important Notes

- Next.js 16は破壊的変更あり。`apps/web/AGENTS.md`参照。コード書く前に`node_modules/next/dist/docs/`のガイドを読むこと
- Stripe金額はJPY zero-decimal（880 = 880円）。cents換算しない
- unslothは使わない。vanilla transformers 5.x + peft + trl（バージョンピン不要）
- Modal A100-40GB使用。LoRA rank: Gemma r=4 all-linear, Qwen r=8 attention-only
- `apps/api/.env`は`.gitignore`に含まれている。秘密情報はRender環境変数で管理
