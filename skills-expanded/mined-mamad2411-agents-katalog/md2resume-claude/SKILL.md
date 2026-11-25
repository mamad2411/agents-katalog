# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## プロジェクト概要

**md2resume** - Markdown形式の職務経歴書をプロフェッショナルなPDFに変換するCLIツール。Node.js + TypeScript + Puppeteerで実装。

**対象ユーザー**: 日本のソフトウェアエンジニア向けの職務経歴書作成

## アーキテクチャ

### コアコンポーネント

1. **src/convert.ts** - メイン変換ロジック
   - Markdownファイルを読み込み
   - `marked`を使ってMarkdown → HTML変換
   - `templates/resume.css`からCSSテンプレートを読み込み
   - Puppeteerで特定の余白設定（左右15mm、上下20mm）でPDF生成

2. **bin/md2resume.ts** - CLIエントリーポイント
   - `commander`でCLI引数をパース
   - `<input>` と `<output>` のファイルパスを受け取る
   - エラーハンドリングとユーザーフィードバック

3. **templates/resume.css** - プロフェッショナルな履歴書スタイリング
   - 日本の職務経歴書に最適化
   - Google FontsのNoto Sans JPを使用
   - ATS（採用管理システム）対応の構造
   - NotionやTechResumeに近いモダンなデザイン

### 技術スタック

- **ランタイム**: Node.js >=18.0.0 (ES modules)
- **言語**: TypeScript 5.x
- **PDF生成**: Puppeteer (ヘッドレスChromium)
- **Markdownパース**: marked
- **CLIフレームワーク**: commander

### ビルドシステム

- TypeScriptコンパイル: `src/**/*.ts` と `bin/**/*.ts` → `dist/`
- ES2022モジュール、strictモード有効
- 出力はディレクトリ構造を保持

## 開発コマンド

### ビルド
```bash
npm run build
```
TypeScriptファイルを`dist/`ディレクトリにコンパイル

### 開発モード（ウォッチ）
```bash
npm run dev
```
TypeScriptコンパイラをウォッチモードで実行

### 変換テスト
```bash
npm run build
node dist/bin/md2resume.js example.md output.pdf
```
サンプルMarkdownファイルからPDFを生成

### 依存パッケージのインストール
```bash
npm install
```
注意: Puppeteerは初回インストール時にChromium（約100MB）をダウンロード

## 重要な設計決定

1. **ES Modules**: `"type": "module"`でモダンなJavaScriptモジュールシステムを使用
2. **余白**: 日本の履歴書基準に合わせて左右15mm、上下20mmに設定
3. **フォント**: プロフェッショナルな日本語表示のためGoogle FontsのNoto Sans JPを使用
4. **ATS対応**: セマンティックなHTMLタグ（h1, h2, h3, sectionなど）でATS解析に対応
5. **CSSカスタマイズ**: 全スタイルを`templates/resume.css`に分離し、カスタマイズを容易に

## ファイル構造

```
md2resume/
├── src/
│   └── convert.ts          # コア変換ロジック
├── bin/
│   └── md2resume.ts        # CLIエントリーポイント
├── templates/
│   └── resume.css          # PDFスタイリング用CSSテンプレート
├── dist/                   # ビルド出力（.gitignore対象）
├── example.md              # Markdown形式のサンプル職務経歴書
├── package.json
├── tsconfig.json
└── README.md
```

## 実装上の重要ポイント

### PDF生成オプション

`src/convert.ts`を修正する際、PDF生成は以下のオプションを使用：
- フォーマット: A4
- 背景印刷: 有効（CSS背景のため）
- 待機条件: networkidle0（Google Fonts読み込み完了を保証）

### CSSテンプレート

`templates/resume.css`で定義されている内容：
- タイポグラフィ階層（h1-h4）
- カスタム箇条書き記号（▸）のリストスタイル
- スキル・経験テーブルに最適化されたテーブルスタイル
- ページブレーク用の印刷専用スタイル
- 青系アクセントカラー（#2563eb）のカラースキーム

### モジュール解決

このプロジェクトはES modulesを使用するため：
- import文には`.js`拡張子を含める必要あり（例: `'../src/convert.js'`）
- `__dirname`と`__filename`は`import.meta.url`から導出

## よくある問題と解決策

### Puppeteerのインストール失敗
Chromiumダウンロードが原因の場合：
```bash
PUPPETEER_SKIP_DOWNLOAD=true npm install
npx puppeteer browsers install chrome
```

### フォント読み込み
Google Fontsはインターネット接続が必要。オフライン使用時はCSSをシステムフォントに変更。

### TypeScriptビルドエラー
ES module互換性のため、全てのimportに`.js`拡張子が必要。

## 将来の拡張機能

- 複数のCSSテーマサポート
- ページサイズと余白のCLIオプション
- カスタムフォントサポート
- npmパッケージとして公開
