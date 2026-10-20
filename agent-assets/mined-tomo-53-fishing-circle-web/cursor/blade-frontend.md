---
description: Blade / Tailwind / Alpine / Vite のフロントエンド規約（ビュー・CSS・JS 編集時に適用）
globs: src/resources/views/**/*.blade.php,src/resources/css/**/*.css,src/resources/js/**/*.js,src/tailwind.config.js
alwaysApply: false
---

# Blade / フロントエンド規約

Blade テンプレート・CSS・JS を編集するときに適用する。

## Blade

- レイアウトは `x-app-layout` / `x-guest-layout` コンポーネントを使う（Breeze 構成）。
- ユーザー入力の出力は `{{ }}`（自動エスケープ）を使う。`{!! !!}` は信頼できる内容のみ、原則使わない（XSS対策）。
- フォームには必ず `@csrf` を含める。メソッド偽装は `@method('PATCH'|'DELETE')`。
- 認可による表示制御は `@can` / `@auth` で行うが、**サーバ側の認可の代替にはしない**（表示制御＋サーバ側認可の二重で守る）。
- バリデーションエラーは `@error` ディレクティブで表示する。

## Tailwind / CSS

- スタイルは Tailwind ユーティリティクラスを優先。独自 CSS は最小限。
- 色・余白などは既存ページのトーンに合わせる。新規の派手な装飾を勝手に足さない。
- レスポンシブ対応（`sm: md: lg:`）を意識する。

## JS / Alpine / Vite

- 軽量なインタラクションは Alpine.js（`x-data` など）で実装する。
- アセットは Vite 経由（`@vite([...])`）。ビルドは `npm run build`、開発は `npm run dev`。
- インラインの大きな JS は避け、`resources/js/` に置く。

## デザイン品質・アクセシビリティ

- 凝った UI の新規作成は `frontend-design`、既存の磨き込みは `ui-polish`、色・余白・コンポーネントの統一は `design-system`、画面の型紙は `interface-patterns`、演出は `ui-motion` スキルを参照する。
- アクセシビリティ必須観点（`accessibility` スキル）: 入力には `label` を関連付ける（`for`/`id`）、エラーは `aria-describedby` で紐づける、キーボードだけで操作でき**フォーカスリングを消さない**、本文・ボタンのコントラストは WCAG AA（4.5:1）を満たす。
- 変更後は `ui-reviewer` エージェントでのレビューを推奨。
