# src/lib/quiz

- server-only の線引き: `payload.ts` / `default-settings.ts` / `spelling.ts` / `generation/` はクライアントからも import されるため `server-only` を付けない。`handlers/` / `queries/` は付ける。
- handler のシグネチャは `(tx, userId, ...)`。words の EditorContext / row-policy は使わない。quiz は system 共有行に書き込まないための意図的な相違 (docs/adr/0019-two-layer-write-authorization.md)。
- 出題生成は RNG (`() => number`) を引数注入する純関数。unit テストは `tests/setup/seeded-rng.ts` を注入して決定化する。シードは永続化しない (中断 = 破棄)。
- **出題順の決定は `generation/build-quiz.ts` の `buildQuiz` に集約する**。形式ビルダー (`generation/<format>.ts`) は常に Fisher–Yates で組み立て、掲載番号順 (docs/adr/0072-quiz-order-by-occurrence-number.md) は生成後に `generation/order.ts` で並べ替える。ビルダー側へ出題順の分岐を戻すと**設定によって RNG の消費列が変わり**、シード付きテストが設定ごとに二重化する。並べ替えの対象は出題順だけで、選択肢のシャッフルは常にランダム。
- 同名ファイルに注意: `quiz/default-settings.ts` (client-safe 定数) と `src/lib/quiz-default-settings.ts` (server-only UseCase)、`quiz/spelling.ts` (採点) と `quiz/generation/spelling.ts` (出題生成) は別物。
- `error-map.ts` に `server-only` が無いのは、import する Error クラスの定義元が server-only 付きのため**推移的に保護されている**既存様式（words 側も同じ）。
- 空白のみの `Example.meaning` を「使える TG 例文」と判定し JS 側でも trim しないのは意図的（SQL count 述語と JS 選抜の完全一致 = プレビュー件数と実出題数の一致を優先。`queries/quiz-source.ts` のコメント参照）。**片側だけ trim を足すと件数が乖離する**。
- `quizRangeInputSchema` / `saveQuizDefaultsInputSchema` が `rangeFrom > rangeTo` をスキーマで拒否しないのは意図的。逆転範囲は下流の `partitionMaterial` / `checkFormatAvailability` が「対象 0 件 = 成立しない」として一元処理する（スキーマ拒否だと quiz 開始とデフォルト保存でエラー体験が分岐する）。クロスフィールド refine を足す「修正」をしない。

## 出題形式の追加チェックリスト

カラム追加・テーブル変更は不要 (enum 値追加のみ)。触る箇所:

1. `prisma/schema.prisma` の QuizFormat enum
2. `generation/<format>.ts` (出題生成)
3. `payload.ts` の union メンバ
4. `format-options.ts` の FORMAT_GROUPS / JA_TO_EN_FORMATS / TG_EXAMPLE_FORMATS (コンパイルエラーにならず最も漏れやすい)
5. `default-settings.ts` の timeoutByFormat (全形式キー必須、コンパイルが強制)
6. `src/app/quiz/_components/` の `question-<format>.tsx` と `quiz-flow.tsx` の分岐

`build-quiz.ts` と `quiz-flow.tsx` の exhaustive switch (never チェック) を通し、既存ユーザーへ推奨デフォルト制限時間を backfill する migration を書く (前例: `prisma/migrations/20260704025822_backfill_tg_format_default_timeouts`)。
