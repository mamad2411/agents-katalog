---
name: puttokei-project
description: Puttokei リポジトリで作業するときの前提をまとめた skill。docs/requirements/requirements.md を基準に、backend の FastAPI/Python、mobile の Expo/TypeScript、infra の Terraform、空ディレクトリの初期実装や構成整理を行うときに使う。
---

# Puttokei Project

## 概要

このリポジトリは backend と mobile の土台実装が進んでいる一方、infra は未作成。既存実装がある領域ではローカルの構成とテストを優先して確認し、未実装領域を作るときは `docs/requirements/requirements.md` を正として扱う。

## 使う場面

- `backend/` `mobile/` `infra/` を触る
- API、DB、認証、LLM 判定フローを決める
- ディレクトリ構成や土台コードを新しく作る
- 設計書どおりに実装を揃える

## 作業ルール

1. まず変更対象ディレクトリの現状を確認する
2. 既存コードがある場合は、その周辺の流儀を崩さずに合わせる
3. 未作成ディレクトリやプレースホルダーしかない領域は、設計書に沿って素直に土台を作る
4. 実装と設計書が食い違う場合は、変更箇所の一貫性を優先しつつ、最終報告で差分を明示する
5. 詳細が必要なときだけ `references/` と `.codex/rules/` を読む

## 使用アーキテクチャ

### backend

- FastAPI / Python 3.12 / SQLAlchemy / Alembic / Pydantic / Firebase Admin SDK
- 4 層のクリーンアーキテクチャを採用する
- 依存方向は `domain <- application <- infrastructure / presentation`
- `src.main` と `src.container` を Composition Root とし、依存の組み立てはここに集約する
- リポジトリ IF と外部サービス IF は `domain`、ユースケースと DTO は `application`
- Unit of Work IF は `application`、SQLAlchemy による実装は `infrastructure/persistence`
- DB、認証、キュー、LLM、通知など外部依存の実装は `infrastructure`
- HTTP 入出力、Pydantic schema、middleware、worker entrypoint は `presentation`

### mobile

- Expo + React Native + TypeScript
- Expo Router によるファイルベースルーティングを採用する
- `app/` は経路定義と layout だけに寄せ、画面実装を直接持たせない
- 画面実装や機能ロジックは `src/features/*` の feature-based structure に分ける
- 共通 UI、API client、Firebase、stores、types は `src/shared`
- ローカル状態は Zustand、サーバー状態は TanStack Query、フォームは React Hook Form + Zod、UI は Tamagui

### infra

- 現時点では `infra/` ディレクトリは存在しない
- Terraform + Google Cloud
- 再利用単位は `infra/modules`
- 環境差分は `infra/environments/{staging,production}`

## プロダクト上の制約

- 認証は Firebase Authentication を前提にする
- 学習フローは `input -> output -> break -> result`
- アウトプットの判定は Cloud Tasks 経由の非同期処理にする
- LLM の応答は JSON として検証・保存できる形を崩さない

## 参照先

- 構成と責務分離の概要は `references/architecture.md`
- 全体構成と infra の規則は `.codex/rules/project-architecture-rule.md`
- backend の詳細なディレクトリ構成とアーキテクチャ規則は `.codex/rules/backend-architecture-rule.md`
- mobile の詳細なディレクトリ構成とアーキテクチャ規則は `.codex/rules/mobile-architecture-rule.md`
- API / DB / 認証 / LLM / CI の期待値は `references/contracts.md`
- 正確な文言や完全な仕様が必要なときだけ `docs/requirements/requirements.md` を開く
