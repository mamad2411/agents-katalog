# src/lib (サービス層)

構造: UseCase は `src/lib/*.ts` 直下フラット (`words-*.ts` / `quiz-*.ts` / `drill-*.ts` 等)、機能サブディレクトリ (`words/` / `quiz/`) は handler・純関数・クエリの置き場。UseCase が `prisma.$transaction` を張り、handler は受け取った `tx` を使う (handler 内でトランザクションを張らない)。

- サービス層はカスタム Error クラスを throw する。Result 型に畳むのは Action 層の責務。
- Prisma のユニーク制約違反は `prisma-errors.ts` の `isUniqueConstraintOn(e, "Model")` で判定する (driver adapter 構成では P2002 の meta が modelName 形式のため)。
- ユーザー向け読み取りは `scopedOwnerIds(userId)` (`system-user.ts`) で system + 本人の行を引く。`ownerId: userId` 単独では共有マスタが欠ける。
- 書き込み系 UseCase の中に `scopedOwnerIds` が現れるのは重複・衝突チェックなどの**読み取り**用。所有検証は素の `ownerId: userId` で行う（読み書き非対称が原則）。例外として純 per-user 設定（`occurrence-preset-settings.ts` 等）は書き込み先が本人行のみなので、対象の掲載箇所を scoped 検証して system 掲載箇所も指定できるのが仕様。
- `src/lib` 直下には client-safe モジュール（`utils.ts` / `speech.ts`）もある。「サービス層 = 全部 server」ではないので、`server-only` を機械的に付けない（付けると components からの import が壊れる）。
- 単語の書き込みは正規パス (`createWordForUser` 等 → `writeWordChildren`) を通す。`tx.word.create` 等での迂回は row-policy と書き込み順序の契約を壊す。
- 入力バリデーションの zod スキーマは `src/lib/schema/` に置き client と共用する (Action ファイル内に書かない)。
- `src/lib/mock/` は品詞などの本番用定数定義。テストダブルではない。
- drill のラウンド送信は `Drill.roundCount` の compare-and-swap で冪等化している (`quiz/handlers/drill-round-handler.ts` の `updateMany`、where に期待値)。楽観ロックや素の update に書き換えない (docs/adr/0033-drill-round-count-cas.md)。
- TG 例文形式の出題適格判定は「意味 1 件以上」の AND ではなく述語ごと置換 (`quiz/queries/quiz-source.ts`)。意味未登録の単語が TG 形式で出題されるのは仕様 (docs/adr/0027-meaningless-words-excluded-tg-exception.md)。

## ops ツール用コアモジュール (tsx から呼ぶもの)

`scripts/*.ts` から import されるモジュール (`occurrence-purge.ts` / `bulk-word-import.ts` が手本) は次を守る。tsx は `import "server-only"` と `@/` エイリアスの実行時 import を解決できず、破ると import 時点で落ちる。

- `server-only` を付けない。`prisma` (必要なら `blob`) は引数注入し、`@/lib/prisma` シングルトンを import しない。
- `@/` 参照は `import type` のみ。実行時に値が要るものは相対 import し、その依存先も同条件を満たすこと。`./prisma-errors` は `@/generated` を実行時 import するため使えない。
- 書き込みは正規パスを再利用できないぶん、`prisma/seed.ts` の raw ネスト create を手本に最小限を書く。
- `occurrence-purge.ts` の read / delete に owner 条件が無いのは**管理者 CLI 専用コアの仕様**（system 行も対象にできる）。Web の action / handler から import しないことが前提条件であり、テナント分離 (B1/B2) の違反として「修正」しない。
- インポート系（`bulk-word-import.ts` / `related-word-import.ts`）が単語 1 件ずつ commit する非原子性は意図的（本番 Neon への往復遅延で長大トランザクションを避ける）。中断時のリカバリ手順は `docs/ops/import-words.md` / `import-related-words.md` に文書化済み。全体 `$transaction` 化の「修正」をしない。
