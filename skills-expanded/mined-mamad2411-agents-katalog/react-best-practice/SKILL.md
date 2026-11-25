---
name: react-best-practice
description: React や TypeScript の実装・レビュー・リファクタで使う。プロダクション品質の React コードを書くために、状態設計、Effect 衛生、コンポーネント設計、TypeScript 品質、パフォーマンス判断、アクセシビリティ、React 19 系のモダン API 選定を確認しながら実装する。
---

# React Best Practice

React のコードを新規実装・修正・レビューするときに使う。
目的は「動く」ではなく、「ship できる」React コードに寄せること。

## 最初に確認すること

1. UI の振る舞いを state と derived value に分ける
2. `useEffect` が本当に外部同期かを確認する
3. 責務の境界ごとに component / custom hook を切る
4. a11y と HTML semantics を仕様の一部として扱う

## 実装ルール

- 派生値を state に保存しない。レンダー時計算か、重い計算だけ `useMemo` を使う
- `useEffect` は購読、timer、DOM/外部 API 同期、永続化のような真の副作用に限定する
- form 検証や disabled 判定のような UI ロジックを effect で同期しない
- props と state の責務を混ぜない。共有状態は適切に持ち上げるか custom hook に閉じ込める
- `any`、雑な assertion、場当たり的な `as` を避け、型を設計の一部として扱う
- `useMemo` / `useCallback` / `memo` は必要性が説明できる場合だけ使う
- クリック可能要素は `button` / `a` を優先し、`div onClick` を避ける
- 入力には `label`、必要なら `aria-describedby`、複合 UI には適切な role と keyboard 操作を用意する

## React 19 系 API の選定

- async データ取得では、手動の `isLoading` 管理より Suspense と `use()` を先に検討する
- 外部ストア購読では `useSyncExternalStore` を優先する
- effect 内の callback が最新値だけ読みたいなら `useEffectEvent` を検討する
- 入力追従を保ったまま重い一覧や検索結果を遅延させたいときは `useDeferredValue` を検討する

## 作業フロー

1. まず [checklist](references/checklist.md) を読んで設計ミスを潰す
2. 外部同期や描画性能が絡む場合は [modern-react-apis](references/modern-react-apis.md) も読む
3. 実装後は次をセルフレビューする
   - 不要 state がないか
   - effect が副作用だけに限定されているか
   - component の責務が大きすぎないか
   - semantic HTML / keyboard / screen reader 対応があるか
4. レビュー依頼時は「どの設計判断を選び、何を捨てたか」を短く説明する
