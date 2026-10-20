# src/lib/words

- `handlers/index.ts` の子エンティティ書き込み順序は旧実装と同一に保つ契約 (ファイル内コメント参照)。並べ替え・並列化をしない。
- 認可は 2 層: `policy/editor-context.ts` が「誰として書くか」、`policy/row-policy.ts` が「行ごとの可否」。認可の変更は row-policy に集約し、handler 内に条件分岐を書かない。
- pass-through は「完全な無変更」ではない: 一般ユーザーは system 行の**維持・並べ替え (sortOrder 更新)・自分の子行の付加**まではでき、本文の改変・削除はできない。handler が pass-through 分岐で `update({ data: { sortOrder } })` するのは規約違反ではなく仕様。
- `words-update.ts` が更新前の子行を owner 条件なしで `findMany` するのは意図的。row-policy の pass-through・削除禁止・孤児化防止の判定には**全 owner の行**が必要で、この read は認可ではなく policy への入力（読み取りスコープ B1/B2 の違反ではない）。
- フォーム値の `ownerId` / `pronunciationAudioUrl` は mass assignment ではない: `ownerId` は UI 表示制御と DB 突合用で、更新パスでは `assertRowsAllowed` が DB の実 owner と照合して不一致を拒否する。`pronunciationAudioUrl` は handler が書き込みに使わない読み取り専用フィールド。schema から除去する「修正」をしない。
- `handlers/allowed-ids.ts` が `@/lib/prisma` シングルトンを import するのは、UseCase が `$transaction` を張る**前**に許可 ID 集合を解決する意図的な事前読み取り（tx 注入規約の唯一の例外。ファイル内コメント参照）。
