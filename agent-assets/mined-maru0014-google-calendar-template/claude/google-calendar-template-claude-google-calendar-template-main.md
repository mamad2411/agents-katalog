# CLAUDE.md

## AI Agent Instructions
このプロジェクトに関する詳細な開発ルール、コーディングスタイル、DOM操作のベストプラクティス、コミット規約などは、すべてルートディレクトリの [AGENTS.md](AGENTS.md) に定義されています。

**Claude Code (および他のAIエージェント) は、開発や修正を行う前に必ず [AGENTS.md](AGENTS.md) を読み込み、その指示に従ってください。**

---

## Setup & Build Commands
- 依存関係のインストール: `npm install`
- 開発サーバーの起動: `npm run dev`
- プロジェクト全体のビルド: `npm run build`
- Content Script のみビルド: `npm run build:content`
- Popup UI のみビルド: `npm run build:popup`
- 静的アセットのコピー: `npm run copy:assets`
