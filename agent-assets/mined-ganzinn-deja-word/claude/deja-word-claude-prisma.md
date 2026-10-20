# prisma

スキーマ規約 (新モデル・カラム追加時):

- コンテンツ系テーブル (Word 系・Occurrence・Drill 系・QuizAnswer) は全行 `ownerId` を持ち、`"system"` 行が全ユーザー共有マスタになる。ユーザー単位の設定系は `userId` を主キーにし ownerId は持たない。
- 例外: `DrillWord`（`@@id([drillId, wordId])`）は `ownerId` を持たない。owner は常に親 `Drill.ownerId` と一致し、drill に system 共有行が存在しないため。Word 系子テーブルの ownerId 非正規化は pass-through（system 親に自分の子を付加）の要件によるもので、DrillWord にはその要件が無い。ownerId 追加の migration を提案しない。
- `onDelete: Cascade` が既定。`QuizDefaultSetting.occurrenceId` と `RelatedWord.linkedWordId` の SetNull は意図的 (従属関係が逆 / 参照だけ外す)。Cascade への「修正」をしない。
- 既存テーブルは変更せず side table の加算で拡張する (docs/adr/0008-side-table-addition.md)。
- QuizFormat の enum 値追加時は、既存ユーザーへ推奨デフォルト制限時間を backfill する migration を伴う (前例: `migrations/20260704025822_backfill_tg_format_default_timeouts`、`ON CONFLICT DO NOTHING`)。
- Prisma 7 の `migrate reset` は seed を自動実行しない。reset 後は `pnpm db:seed` を実行する。
- `seed.ts` は tsx 実行のため `../src/generated/prisma/client` を相対 import する (`@/` は使えない)。
