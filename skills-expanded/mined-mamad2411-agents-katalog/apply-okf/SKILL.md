---
name: apply-okf
description: OKF（Open Knowledge Format）知識バンドル内で文書を新規作成・更新・レビュー・廃止したときに、OKF の規約（フロントマターの type/title/description/generated、verified、status、stale_after、index.md・log.md の更新、適合性検証）を適用する日常運用スキル。「この設計書に OKF のフロントマターを付けて」「作った ADR をバンドルに登録して」「レビューしたので verified を付けて」「古い手順書を deprecated にして」「index.md と log.md を更新して」「OKF に適合しているか確認して」といった場面で発動する。他のスキル（creating-adr・analyzing-*・planning-releases・creating-journal など）が docs/ 配下に Markdown を書いた直後や、エージェントが生成した知識を人が確認した場面では、明示的な依頼が無くても積極的に使うこと。既存文書の一括移行や仕様バージョンアップは migrating-okf の担当。
---

# OKF 適用

OKF 知識バンドル（既定 `docs/`）に対する**日常の変更**に規約を適用する。一括移行は `migrating-okf`、本スキルは「1 つ書いた／直した／確認した／捨てた」たびに呼ぶ仕上げ工程。

仕様の日本語リファレンスは `docs/reference/OKF導入ガイド_V0.2.md`。§5（来歴・信頼・ライフサイクル）と §7（アクター規約）が本スキルの根拠。同じディレクトリに `PROJECT.md` があれば必ず読む（バンドルの場所・type 対応表・既定アクターはそこにある）。

## なぜ毎回適用するのか

バンドルの価値は「各文書が信頼してよい根拠を持っている」ことにある。1 つでもフロントマターの無い文書が混ざると `type` 必須の適合性が壊れ、`generated` が更新されない文書は「誰がいつ書いたか」を偽る。規約は移行時に一度守れば済むものではなく、書くたびに守って初めて意味を持つ。

## 4 つの操作

| 操作 | いつ | 何をするか |
| :--- | :--- | :--- |
| **apply** | 文書を新規作成・更新した直後 | フロントマター付与／`generated` 更新、`index.md` にエントリ追加、`log.md` に記録。エージェントが書いた新規文書は `status: draft`（未レビュー）、人が書いたものは `stable` |
| **verify** | 人またはプロセスが内容を確認した | `verified` に `{ by, at }` を追記。`draft` なら `stable` に昇格 |
| **deprecate** | 文書を置き換えた・不要になった | `status: deprecated`（後継があれば `replaced_by`）、`index.md` の該当エントリに「（廃止 → 後継）」を付記。削除はしない |
| **check** | 上記の後、コミット前 | `gulp okf:check`（または `migrating-okf/scripts/okf_check.py --check`）で ERROR 0 を確認 |

すべて同梱スクリプトで行う。手でフロントマターを書かない（タイムスタンプの形式や `verified` のリスト化などの細部を間違えやすい）。

```bash
S=.claude/skills/apply-okf/scripts/okf_apply.py
python $S apply     docs docs/adr/007-cache-strategy.md --by claude-code/claude-fable-5
python $S apply     docs --changed --by claude-code/claude-fable-5      # git で変更された .md をまとめて
python $S verify    docs docs/design/data-model.md --by human:alice
python $S deprecate docs docs/operation/old-deploy.md --replaced-by /operation/deploy.md
python $S status    docs docs/design/*.md
```

`--replaced-by` はバンドル相対パス。Git Bash（Windows）は `/operation/deploy.md` のような先頭 `/` を `C:/Program Files/Git/...` に変換してしまうので、先頭 `/` を付けずに `operation/deploy.md` と書く（スクリプトが `/` を補う）。

## 判断すべきこと（スクリプトは判断しない）

### 誰が書いたか（`--by`）

`generated.by` は「今の本文を書いた者」。自分（エージェント）が本文を書いた・書き換えたなら `claude-code/<model>` のような `<producer>/<version>`。人が書いた文書にフロントマターを付けるだけなら `human:<id>`（git の著者から）。スクリプトは本文が git HEAD から変わっていなければ `generated` を触らないので、フロントマターだけ直す作業で来歴が上書きされる心配はない。

### `verified` を付けてよいか

内容を人が読んで「正しい」と判断したとき、または自動プロセスが照合したときだけ。自分が書いた直後に自分で `verified` を付けない（信頼ティアが `human-reviewed` と `unverified` を区別できなくなる）。ユーザーから「確認した」「レビュー済み」「OK」と言われたら、そのユーザーのアクター（`human:<id>`）で `verify` する。

### `type`

親ディレクトリから推定される（`adr/`→`ADR`、`design/`→`Design`、`development/`→`Plan`、`operation/`→`Playbook` など）。推定が合わない、または新しいディレクトリなら `--type` で明示する。型の数は増やさない。1 ディレクトリ 1 型が目安。

### `stale_after`

「一定期間で見直さないと嘘になる」文書だけに `--stale-days` を付ける。環境構築手順・技術スタック・外部サービスの設定手順が典型。設計判断や記事には付けない。

### `description`

`index.md` と検索結果に出る 1 文。スクリプトは冒頭段落から推定するが、精度は本文次第。推定が弱い（空・自己言及的・冒頭が図やリスト）なら `--description` で書く。

## 他スキルとの連携

`docs/` に文書を書くスキルの最後に本スキルを組み込む。典型的な流れ：

1. `creating-adr` が `docs/adr/007-cache-strategy.md` を書く
2. `apply docs docs/adr/007-cache-strategy.md --by claude-code/<model>` → フロントマター付与、`adr/index.md` にエントリ、`log.md` に Creation
3. ユーザーがレビューして承認 → `verify ... --by human:<id>`
4. 置き換えた ADR-003 があれば `deprecate docs/adr/003-*.md --replaced-by /adr/007-cache-strategy.md`
5. `gulp okf:check` → ERROR 0 を確認してコミット

`index.md` のエントリはスクリプトが末尾に追加するだけなので、セクション分けされた `index.md` では適切な見出しの下へ移動する。`log.md` のメッセージは既定の自動文で足りるが、判断を伴う変更（廃止理由、大きな書き換え）は `--log` で理由を残す。

## 完了報告

```markdown
## OKF 適用結果

- 対象: <ファイル>（操作: apply / verify / deprecate）
- generated: <by, at>（更新した場合）
- index.md / log.md: 更新の有無
- 検証: ERROR 0 / WARN <N>
- 要確認: <description の推定が弱い、type を仮置きした、など>
```

## 関連スキル

- `migrating-okf` — 既存文書の一括移行・仕様バージョンアップ・検証スクリプト
- `creating-adr` / `creating-journal` / `analyzing-*` / `planning-releases` — 文書を生む側。書いた直後に本スキル
- `git-commit` — 検証後のコミット
