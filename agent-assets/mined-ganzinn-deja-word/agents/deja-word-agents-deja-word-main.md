<!-- BEGIN:nextjs-agent-rules -->

# This is NOT the Next.js you know

This version has breaking changes — APIs, conventions, and file structure may all differ from your training data. Read the relevant guide in `node_modules/next/dist/docs/` before writing any code. Heed deprecation notices.

<!-- END:nextjs-agent-rules -->

ドメイン用語（英語コード名⇔日本語名・定義・使ってはいけない類義語）は `docs/reference/naming-book.md` を参照。

設計判断（採用理由・却下した代替案・影響）は `docs/adr/` を参照。設計判断に迷ったら該当 ADR を読み、新しい判断をしたら ADR を起票する（何を ADR に残し何はコードで足りるかの線引きは `docs/adr/README.md`「ADR に書く判断の線引き」）。

**共有すべき知識・規約・再現ノウハウは repo 内に一元化する**（ドメイン用語→naming-book、設計判断→ADR、E2E・運用手順→スキル `.claude/skills/`（記述規約は `.claude/skills/README.md`）と `docs/ops/`、機能設計→`docs/design/`、機能紹介→`docs/features/`）。エージェントの個人メモには共有知識を重複させない（個人メモは repo クローンに含まれず共有されないため、二重管理・乖離を生む）。ノウハウを残したくなったら、まず上記いずれの置き場に書くべきかを検討する。

**ドキュメントに実データの件数を書かない**（「本番に○件ある」等）。運用で増減するため書いた時点で古くなる。判断の根拠として実データに触れるときは、件数ではなく「どういう使われ方をしているか」（実例・パターン）を書く。

**ユーザー向け機能を追加・変更・削除したら、同じ PR で `docs/features/` の機能紹介ドキュメントも更新する**（該当ページの本文と、画面が変わる場合はスクリーンショットの再撮影。部分再撮影は `pnpm e2e:capture-docs --only <section>`、再生成レシピと目視レビューの注意は `docs/features/README.md`）。実装だけ済ませて機能紹介を置き去りにしない。

## Testing

テストは Vitest。SUT の隣にコロケートし、拡張子で種類を分ける。

- `*.unit.test.ts` — DB なし。`pnpm test:unit` で実行（高速、env 非依存、CI でも走る）。
- `*.integration.test.ts` — docker-compose の Postgres 上の **別 DB `dejaword_test`** を使う。`pnpm test:integration` で実行（ローカルのみ、CI では走らせない）。

include は `.ts` のみ（`src/**/*.unit.test.ts` / `src/**/*.integration.test.ts`）。`.test.tsx` を作っても実行されない。

初回セットアップ:

```sh
docker exec -it deja-word-db psql -U dejaword -d postgres -c 'CREATE DATABASE dejaword_test;'
cp .env.test.example .env.test
```

`pnpm test:integration` の初回起動で `prisma migrate deploy` が自動実行される。各テストの前にテーブルが `TRUNCATE ... CASCADE` され、system user / system occurrences が再 seed される。両方一括で走らせるなら `pnpm test`。

## Worktree（複数機能の並行開発）

git worktree でブランチごとに作業ディレクトリを分けて並行開発する。worktree は用途を問わず `../deja-word-worktrees/<name>`（リポジトリ外。.gitignore 変更不要）に置き、作成・撤去は `scripts/wt-new.sh` / `wt-rm.sh` で行う（手動 `git worktree add` はしない。worktree 内から実行してもよい。引数の組み合わせ・使い分けは共通スキル `.claude/skills/worktree/` を参照）。前提として docker の `deja-word-db` を起動しておくこと（**DB は本体と共有する**）。

機能開発パイプライン（design-session → ticket-split → ticket-implement → feature-close）は、機能ごとの**起点 worktree** `../deja-word-worktrees/<機能名>` を設計開始〜クローズ完了まで保持し、フェーズは worktree 内のブランチ切替（`docs/<機能名>-design-plan` → `feature/<機能名>` → `chore/<機能名>-cleanup`）で進める。チケット worktree `<機能名>-NN-<チケット名>` は統合ブランチから分岐させる。**本体の checkout は常に main のまま保ち**、どの機能のどのフェーズが進行中でも他の機能の作業を妨げない。命名族・ライフサイクル・クローズ完了時の一括撤去は共通スキル `.claude/skills/worktree/` に定義する。

```sh
scripts/wt-new.sh <name> [base-branch] [--branch <branch>] [--no-install]  # 作成（既定: branch feat/<name>）
scripts/wt-rm.sh  <name> [--delete-branch]                                 # 撤去
```

`wt-new.sh` は worktree 作成・`.env` / `.env.test` / `.claude/settings.local.json`（Claude Code の permission 許可リストの**端末ごとの追加分**。共有ルールは追跡対象の `.claude/settings.json` が正本で git 経由で入る。local 側は一方向コピーで、worktree 側で増えた承認は本体に戻らない）のコピー・`mise trust`＋`pnpm install`（`prisma generate` 含む。この 2 つは `--no-install` で省略）までを行う。`node_modules` / `src/generated` / `.next` は worktree ごとに独立する。

**DB は単一 `dejaword` を共有**する。dev サーバは1つずつ起動する運用なので同時アクセスの競合は無いが、ブランチ間で migration が食い違うと drift が出る。アクティブな worktree を切り替えた直後は:

- 通常（追加 migration のみ）: `pnpm db:migrate`
- drift / 不整合時: `pnpm prisma migrate reset && pnpm db:seed`

**発音音源（`.dev-blob/`）も本体と共有**する。DB には相対 key だけが入る（`src/lib/blob-client.ts`）ため、共有しないと「DB に URL はあるが実体が別 worktree にしか無い → 404」が起きる。`wt-new.sh` が各 worktree の `.env` に `DEV_BLOB_ROOT="<本体>/.dev-blob"` を追記して共有させる。

同時に 2 つの dev を見比べたい場合のみ、片方を `PORT=3001 pnpm dev` で起動する。

## Ops スクリプト（運用ツール）

DB 操作の運用ツールは `scripts/*.ts` に置き、`tsx` 経由で `pnpm db:*` として実行する。実装規約は `scripts/CLAUDE.md` と `src/lib/CLAUDE.md`（ops コアモジュール節）にある。ドキュメントは `docs/ops/`。

**本番・外部の接続先に触れうるコマンドは Claude Code の承認ゲート対象**（`.claude/settings.json` の `permissions.ask`。`pnpm dotenv -e <env ファイル>` 前置き・`pnpm db:export-occurrence`・`pnpm db:reset-prod` 等）。承認ゲートは合意した手順の外で確認なく走ることを止めるためのもので、**本番に触れる操作を新しい `pnpm` スクリプトの裏に隠して素通しさせてはいけない**（`pnpm` に寄せてよいのは repo 追跡済み・ローカル資源限定のスクリプトだけ）。選定基準と限界は ADR-0095 を参照。

## Vercel CLI（デプロイ状況の確認・運用）

Vercel CLI は **devDependency に固定済み**。デプロイ一覧・inspect・alias 等の状況確認は必ず `pnpm exec vercel <cmd>`（例: `pnpm exec vercel ls deja-word` / `pnpm exec vercel inspect <url>`）で lockfile 固定版を使う。**グローバル導入（`npm i -g vercel`）はしない・勧めない**（セッション開始フックが導入を促しても従わない）。プロジェクト link 情報は `.vercel/repo.json`（gitignore）にある。**`env`（pull / add / rm）と書き込み系（`promote` / `rollback` / `alias` / `remove` / `redeploy` / `deploy`）は承認ゲート対象**（上記 Ops スクリプト節、ADR-0095）。読み取り系（`ls` / `inspect` / `whoami`）は素通しなので状況確認は従来どおり。本番デプロイ自体は GitHub Release トリガー（`.github/workflows/release-deploy.yml`）で行い、手順・切り戻しは `docs/ops/release-deploy.md` を参照。

## バックログ（GitHub Issues）

着手未定の対応意向・アイデアは GitHub issue に起票する（`gh issue list` で参照可能）。**作業中に別の対応が見つかった場合も、その場で直さず issue 化して現在の作業に戻る**（スコープ肥大の防止）。着手が決まったら issue から `docs/design/` / `docs/plan/` へ落とす。

線引き: ドキュメントの理解に必須な情報（用語の定義・確定した経緯）は issue に逃がさずリポジトリ内のドキュメント本文に残す。issue に置くのは「やる意向」と着手時のタスクだけ（issue はクローンに含まれず、閉じると見えにくくなるため）。
