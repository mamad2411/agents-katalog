# src/app (Server Action・UI)

- Server Action は throw せず Result 型 `{ ok: true, ... } | { ok: false, error, message }` を返す。サービス層が throw するカスタム Error は error-map (`src/lib/words/error-map.ts` / `src/lib/quiz/error-map.ts`) で Result に変換する。message はユーザー向けの日本語。
- セッション取得は `getCurrentSession()` (`src/lib/session.ts`)。`src/app/api/words/` 配下の 2 つの Route Handler が `auth.api.getSession` を直接呼んでいるのと、`api/dev-blob/` にセッションチェックが無い（本番は `NODE_ENV` ガードで 404、mp3 は opaque な public blob 前提）のは既存の例外で、修正対象のバグではない。
- 管理者判定は `session.user.id === SYSTEM_USER_ID` (`src/lib/system-user.ts`)。role カラムや admin フラグは存在しない。
- ルート内専用のコンポーネントは `_components/`、ヘルパは `_lib/`。横断共有は `src/components/`。
- フォームの定型: `"use client"` + `useForm` + `zodResolver` (スキーマは `src/lib/schema/` を server と共用) → Server Action を await → `result.ok` で分岐 → `sonner` の toast。
- クイズの出題形式を追加するときは `src/lib/quiz/CLAUDE.md` のチェックリストに従う (`question-<format>.tsx` と `quiz-flow.tsx` の追加を含む)。
- 一般ユーザーが system 所有単語の編集ページ (`words/[id]/edit`) を開けて更新アクションを実行できるのは仕様（pass-through 編集: 共有行を維持しつつ自分の子行を追加・編集する。ADR-0019）。`canEdit` / `headwordReadOnly` 等の props は**表示制御専用**で、実認可はサーバ側の row-policy が強制する。page 層に notFound ガードを足す「修正」をしない。
- quiz デフォルト設定 (`settings/quiz-defaults`) は保存時に出題成立可否（対象件数・形式適格性）を検証しない。成立可否は保存後のデータ変化で変わるため、開始画面のプレビューが毎回再検証する設計（掲載箇所 id の権限検証だけはサーバで行う）。保存時バリデーションを足す「修正」をしない。
