---
description: receptron/mulmoclaude の `plans/` 直下にあるマージ済み plan を `plans/done/` にアーカイブし、コード/docs 内の全 stale 参照を `plans/done/<name>.md` に書き換えて PR を作成する。`plans` 整理、`plans の done を移動` 等で起動。PR #265 / PR #817 と同形式の sweep。
---

## Archive Shipped Plans

`plans/` 直下のマージ済み plan ファイルを `plans/done/` に移し、コード/docs/他 plan 内の `plans/<name>.md` 参照を全て `plans/done/<name>.md` に更新して PR にまとめる skill。

各 plan に対応する PR が **merge 済みか / いつ merge されたか** は LLM の知識・推測ではなく必ず `gh pr view <num> --json mergedAt` で実値を取得して判定する (LLM の日付推測は高確率で間違う)。

### Defaults

- repo: `receptron/mulmoclaude`
- branch: `chore/archive-shipped-plans-N` (N は連番、既存があればインクリメント)
- 対象: `plans/` 直下の `*.md` のみ (`plans/done/`, `plans/decisions/`, `plans/i18n-audit/`, `plans/log-audit/` は除外)

### Workflow

#### Step 1 — 直前 archival からの差分把握

直近の archival PR (`gh pr list --search "archive plans" --state merged`) を確認し、その後にマージされた PR の plan が今回の対象。

```bash
gh pr list --repo receptron/mulmoclaude --search "archive plans in:title" --state merged --limit 5 --json number,title,mergedAt
```

#### Step 2 — plan 一覧を triage

`ls plans/*.md` で全ファイルを列挙し、各々について done/active を判定する。

**完了日と PR 番号は LLM 推測禁止。必ず以下のコマンドで実値を取得:**

```bash
# ファイル名に番号 (例: feat-xxx-731.md) があるなら直接 PR を当てる
gh pr view <num> --repo receptron/mulmoclaude --json number,title,mergedAt,headRefName,body

# 番号がないなら slug 検索
gh pr list --repo receptron/mulmoclaude --search "<slug> in:title" --state all --json number,title,mergedAt,state --limit 5
```

**ファイル名末尾の番号** (例: `-731`, `-465`) は GitHub Issue/PR 番号のはず。それを起点に検索すると速い。

#### Step 3 — 多 phase plan / scope drift の精査

「PR がマージされた = plan の全範囲が完了」とは**限らない**。本文を Read して以下を確認:

- **ステータス節**: `**Status**: ... not yet implemented` などが冒頭にあれば即 active
- **Phase 構造**: `Phase 1/2/3` がある plan は、各 phase の実装状況を**ファイル/コード単位の証拠で**個別確認:
  - **acceptance criteria のチェックリスト** (例: 各 phase 末尾の `- [ ] ...` 節) を本文から抽出
  - 各項目に対応する実体 (実装ファイル / docs / package / CHANGELOG エントリ等) が repo に存在するか `ls` / `grep` で確認
  - 例: `feat-plugin-sdk-rollout.md` は Phase 2 acceptance に `docs/plugin-development.md exists` があるので `ls docs/plugin-development.md` で実体確認 → 不在なら active
  - 例: `feat-scheduler-phase3.md` はタイトル通り Phase 3 限定 plan で OK
  - 関連 issue が closed でも、acceptance 項目が repo 上で確認できないものは active 維持。**「umbrella issue closed = 全 phase done」と機械的に判定するのは禁止** — issue は administrative に閉じることが多い
- **Non-goals 節**: `feat-agent-cancel-button.md` の "(#731, partial)" は plan のスコープ限定の意味であって、plan 自体は完了
- **`docs:` PR は plan のみ merge の可能性**: `gh pr view <num> --json title` でタイトルが "docs: plan for ..." なら plan を入れただけ。実装ファイルが存在するか追加チェックすること
  - 例: `test-top-page-regression-e2e.md` (PR #672) → e2e/ に該当 spec が無く、active のまま

**Manual active 候補 (PR 関係なく残す)**:

- Canonical reference docs (`mulmo_claude.md`, `routines.md`, `security_without_docker.md` 等)
- Audit roadmap (`audit-journal-subsystem.md` など、本文で "Status: audit + roadmap, not yet implemented" 明記)
- 未実施ローンチ (`launch-product-hunt*.md`)
- 進行中 feature plan (untracked または最近編集が多いファイル、本文で "実装は未着手" 等明記)

#### Step 4 — triage 結果をユーザーに提示

done / active の表 (file / 完了日 / PR# / 根拠) を出してユーザー承認を得る。**承認なしで mv に進まない。**

#### Step 5 — ブランチ作成 + git mv

```bash
git branch --show-current   # main にいることを確認
git checkout -b chore/archive-shipped-plans-N

# done 各ファイルを個別 git mv (CLAUDE.md: never git add . / directory)
for f in <file1.md> <file2.md> ...; do
  git mv "plans/$f" "plans/done/$f"
done
```

#### Step 6 — 全 stale 参照の sweep (★ここが最重要)

リポジトリ全体で `plans/<name>.md` 参照を grep し、`<name>` が `plans/done/` に存在するものを抽出する。

**`grep -r --exclude-dir` のフィルタには罠があるので避ける**: `--exclude-dir` でファイル**パス**を除外しても、フィルタ後の `grep -v 'plans/done/'` がパス側にも target 参照側にも当たって除外しすぎる。

**正しいやり方** (`find + xargs + grep`):

```bash
find . -type f \( -name '*.ts' -o -name '*.tsx' -o -name '*.vue' -o -name '*.js' -o -name '*.md' -o -name '*.json' \) \
  -not -path './node_modules/*' -not -path './.git/*' -not -path './dist/*' -print0 \
  | xargs -0 grep -nHE 'plans/[a-z0-9_-]+\.md' 2>/dev/null \
  | grep -oE '[^:]+:[0-9]+:[^ ]*plans/[a-z0-9_-]+\.md' \
  | awk -F: '{print $1, $2, $NF}' \
  | while read file lineno ref; do
      [[ "$ref" == plans/done/* ]] && continue
      name=$(echo "$ref" | sed 's|.*plans/||;s|\.md$||')
      if [ -f "plans/done/$name.md" ]; then
        echo "STALE: $file:$lineno → $name"
      fi
    done | sort -u
```

これは:

- コード/docs (.ts/.tsx/.vue/.js/.md/.json)
- **`plans/done/*.md` ファイル内の cross-reference** (←過去に見落としあり)
- **plan 自己参照** (`- plans/<name>.md (this file)` のような行)

の全てを拾う。

#### Step 7 — 各参照を Edit で書き換え

並列で全 Edit を実行。各 old_string は **行全体の context** で unique にする (短い fragment だと複数マッチでエラー)。

#### Step 8 — sweep 再実行 (zero-stale 確認)

Step 6 の sweep を再実行し、**結果が空** (無視できる untracked file 以外) であることを確認する。

#### Step 9 — stage + commit

stage と commit は CLAUDE.md の git ルールに従う (`git add` 個別、commit message 英語 prefix 付き、pre-commit hook を skip しない 等)。

この skill 固有の commit message 雛形 (本体は archive のみなら `chore:`、参照修正を別 commit にするなら `fix:`):

```text
chore(plans): archive N shipped plans under plans/done/

N plans whose primary PRs have shipped (all merged YYYY-MM-DD to YYYY-MM-DD).
Code/docs comments referencing `plans/<name>.md` updated to `plans/done/<name>.md`.

Active plans remaining in plans/: M.
```

#### Step 10 — push 依頼 → PR 作成

ここからは CLAUDE.md の git/PR ルールに従う (Claude は push しない、PR title 英語 / body 日本語、AI 生成 PR の Summary + Items to Confirm セクションを冒頭に置く 等)。

この skill 固有で PR description に必ず含めたい情報:

- アーカイブ表 (File / 完了日 mergedAt UTC / PR#)
- アクティブのまま残した一覧 (File / 残置理由)
- Test plan: `ls plans/` / `ls plans/done/` / `plans/done/<name>.md` リンクが GitHub 上で辿れる / stale 参照ゼロ

PR push 後のボットレビュー対応 (CodeRabbit / Codex 等) は `coderabbit-review` / `codex-cross-review` 等の別 skill 担当。この skill のスコープは PR 作成まで。

### よくある落とし穴

| 罠 | 対処 |
|---|---|
| LLM が完了日を勝手に推定 | 必ず `gh pr view <num> --json mergedAt` で実値取得 |
| ファイル名カウントの整合性 | `git ls-files plans/ \| grep -v plans/done/` で実 tracked 件数を確認 |
| untracked ファイルを active にカウント | `git status` の `??` を確認、PR description には含めない |
| `grep -r --exclude-dir` のフィルタ漏れ | `find + xargs + grep` を使う |
| `plans/done/*.md` 内の cross-reference | 必ず sweep 対象に含める |
| `(this file)` `(self-reference)` の自己参照 | mv 後は `plans/done/<name>.md (this file)` に更新 |
| 多 phase plan を全部 done と早合点 | 本文の Phase 節を Read、関連 issue の `state` も確認 |
| `docs: plan for ...` PR を実装と勘違い | 実装ファイル (e2e spec、関数等) の存在を追加確認 |
| Phase 2 が plan 通りに実装されていない | issue closed なら maintainer 判断「完了」、PR description に scope drift を明記 |

### Anti-patterns

- ❌ Plan 本文を読まずに「PR がマージされてれば done」と判定
- ❌ コード参照 sweep を `grep -r` だけで済ませる (フィルタバグで漏れる)
- ❌ `plans/done/*.md` 自体を sweep 対象から外す
- ❌ untracked ファイルを active 件数に含めて PR description に書く
