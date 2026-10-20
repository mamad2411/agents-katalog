# scripts/e2e (ブラウザ E2E ハーネス)

ここは **ブラウザ E2E 検証ヘルパ**であり、`scripts/CLAUDE.md` の DB ops スクリプト規約（既定ドライラン・`--execute` で書込み等）は**適用しない**。実行は `pnpm e2e:*`（検証本体は tsx、dev サーバの待ち合わせ・停止は shell）。使い方の全体像は skill `e2e-verify`（`.claude/skills/e2e-verify/SKILL.md`）を参照。

- dev サーバのプロセス補助は shell に置く（`wait-for-dev.sh` = 起動待ち / `stop-dev.sh` = ポート指定停止）。**待ち合わせ・停止をコマンド列で手書きしない**（コマンド置換・未許可コマンドが承認プロンプトになる）。同種の定型が増えたらここへ足し、`pnpm e2e:*` から呼ぶ。

- ブラウザ操作は `playwright-core` + システムの Google Chrome（`chromium.launch({ channel: "chrome" })`）。ブラウザ実体はリポジトリに同梱しない。CI では動かさない（integration テスト同様ローカル専用）。
- アプリ本体には **HTTP（ブラウザ）経由**でのみ触れる。`@/` エイリアスやサービス関数は import しない。
- DB に触れるのは **ユーザー用意（`ensureUser`）と後始末（`cleanupWordsByPrefix` / `deleteUserByEmail`）だけ**。`db.ts` は `scripts/create-user.ts` と同じ相対 import 規約（`../../src/generated/prisma/client` + `@prisma/adapter-pg`、接続文字列 `DIRECT_URL → DATABASE_URL_UNPOOLED → DATABASE_URL`）に従う。
- 後始末はアプリ層の削除ガードを迂回して DB 直削除する（cascade で子行も落とす）。テストデータは必ず `e2e-*` 前置きの headword / email にして、prefix 掃除で回収できるようにする。
- 一般ユーザーは `test1@example.com` を**既定**にして使い回し（事前データも test1@example.com で作る）、**削除しない**。使い捨てユーザー（`e2e-throwaway-*`）は**新規ユーザーの観点が本質的に必要なとき**だけ作り、検証後に削除する（ユーザー削除検証での残骸チェックも同様の副次用途）。
