---
description: TypeScript開発のための詳細なルールとベストプラクティス
globs:
  - "**/*.ts"
  - "**/*.tsx"
alwaysApply: true
---

# TypeScript開発ルール

## 基本設定
- TypeScript 5.x系の最新安定版を使用
- 厳密モード（strict: true）を有効にする
- noImplicitAnyを有効にする
- noUnusedLocalsとnoUnusedParametersを有効にする

## 型定義
- interfaceよりtypeエイリアスを優先使用
- 型名はPascalCaseで記述
- ジェネリクスは意味のある名前を使用（T, U, Vは避ける）
- 型ガードを活用してtype narrowingを実装

## 変数と関数
- constアサーションを活用
- 関数の戻り値の型は明示的に記述
- 非同期関数はPromise型を明示
- オプショナルプロパティは?を使用

## エラーハンドリング
- anyの使用は禁止（unknownを使用）
- エラーオブジェクトは適切な型を定義
- try-catch文では具体的なエラー型を処理
- Result型パターンの活用を推奨

## ユーティリティ型
- Partial, Required, Pick, Omitを活用
- 条件付き型を適切に使用
- Mapped Typesを活用
- Template Literal Typesを活用

## モジュールシステム
- ES6モジュールを使用（CommonJSは使用しない）
- 名前付きエクスポートを優先
- デフォルトエクスポートはコンポーネントのみ
- 循環依存を避ける

## 型安全性
- 型アサーション（as）の使用は最小限に
- non-null assertion（!）の使用は避ける
- 型ガードを適切に実装
- 実行時の型チェックを実装

## パフォーマンス
- 型計算の複雑さを避ける
- 大きなUnion型は分割
- 型の再帰は適度に制限
- コンパイル時間を監視

## ドキュメント
- JSDocコメントを日本語で記述
- 複雑な型定義にはコメントを追加
- 型の使用例を記述
- 変更理由を記録

## テスト
- 型レベルのテストを実装
- expect-typeライブラリを使用
- 型エラーのテストも実装
- 型の互換性をテスト

## リンティング
- @typescript-eslint/eslint-pluginを使用
- 推奨ルールセットを適用
- カスタムルールを必要に応じて追加
- 型チェックを自動化

## ビルド設定
- tsconfig.jsonを適切に設定
- パス解決を設定
- 出力ディレクトリを指定
- ソースマップを生成

## 開発ツール
- TypeScript Language Serverを活用
- 型情報の表示を有効化
- 自動インポートを設定
- リファクタリングツールを活用