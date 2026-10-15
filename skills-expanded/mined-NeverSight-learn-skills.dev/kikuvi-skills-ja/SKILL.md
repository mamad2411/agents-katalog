---
name: kikuvi-skills-ja
description: >-
  Use Kikuvi to create, manage, and analyze interviews. Activate when the user
  wants to "create an interview design", "run an interview session", "analyze
  interview results", "generate a report", or is working with the Kikuvi
  platform.
metadata:
  author: Kikuvi-Inc
  version: "0.1.0"
---

# Kikuvi Skills

## Kikuvi とは
Kikuvi は AI ヒアリングエージェント。AI が対話形式でインタビュー（ヒアリング）を自動実施し、回答を収集・分析・レポート化する。

## エンティティ構造

- **Organization**（組織）: 請求・メンバー管理の最上位単位
  - **Project**（プロジェクト）: テーマ別のヒアリンググループ
    - **Design**（ヒアリング設計）: 1ヒアリングの設計書（質問・対象者を定義）
      - **Section**（セクション）: 質問をテーマ別にグループ化
        - **定性質問**: 定性的な情報を集めたい場合
        - **定量質問**: 定量的データを集めたい場合（選択・数値・スライダー等）
      - **Session**（セッション）: 対象者1人=1セッション（実際の会話）
        - **SessionReport**: セッション完了時に自動生成
      - **DesignReport**: 全セッション完了後に自動生成
    - **ProjectReport**: 生成toolをcallして生成

## MCP が使えない場合
MCP が設定されていない場合は、ユーザーに即座に伝えて MCP のみのセットアップを案内すること。

**1. APM の存在チェック**
`apm --version` を Bash で実行する。コマンドが見つからない場合のみ、以下のインストール手順をユーザーに案内する：

macOS / Linux
```bash
curl -sSL https://aka.ms/apm-unix | sh
```

Windows
```
irm https://aka.ms/apm-windows | iex
```

**2. Kikuvi MCP サーバーをインストール**
```bash
apm install --mcp kikuvi --transport http --url https://api.kikuvi.com/mcp
```
初回接続時にブラウザが開き、Kikuvi アカウントへの OAuth サインインが完了する。

**3. 使用しているクライアントに反映する**
```bash
apm compile --target <client>
```
`<client>` は使用している AI クライアントに合わせて指定する（例: `claude`, `codex`, `cursor`, `copilot`, etc.）

## Critical Rule: Kikuvi の API 仕様はモデルの記憶を信じない
Kikuvi の API は継続的に進化している。モデルの学習データは作成された時点で古くなっており、存在しないツールを呼び出したり廃止された引数を渡したりする原因になる。
- ツール名・引数・スキーマを記憶から決め打ちしない
- Tool を実行する前に必ず MCP でスキーマを確認する
- MCP からエラーが返ったときも、ツール名や引数を決め打ちせず MCP のスキーマを再確認してから修正する

## Guideline: 必要な情報はユーザーに質問して収集する
操作の目的・背景・対象者などTool Callに必要な情報を推測するのではなく、必要な情報はすべて対話形式でユーザーに質問して収集する。

## Checklist: 操作前チェックリスト
- 内部IDはユーザーに見せない — 常に名前で表示する
- Tool callに必要なID（designId, sessionId など）は list 系ツールで取得し、内部で保持する

## ヒアリング設計作成

### どちらのアプローチを使うか
| 状況 | アプローチ |
|------|-----------|
| デフォルト（基本的にはこちらを採用） | 対話的に設計 |
| ユーザーが「自動生成」「すぐ作って」「任せる」など自動生成を明示した場合のみ | AI 自動生成 |

### 対話的に設計
**MANDATORY: `references/interview-design-creation.md` を読みその内容に従うこと。** 

### AI 自動生成
ユーザーが明示的に自動生成を要求した場合のみ使用する。who / what / how / why などの情報を渡し、`design_generate` で AI がセクション・質問を自動生成する。
