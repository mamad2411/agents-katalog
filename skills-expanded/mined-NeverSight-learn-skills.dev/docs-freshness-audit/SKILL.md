---
name: docs-freshness-audit
description: "Periodically audit a repository's docs for staleness against the implementation: run a cheap mechanical scan (dead source-path references, dead links, leftover DEPRECATED/TBD banners, doc-vs-code freshness gap, git-invisible ignored leftovers, completed-but-undeleted plan files), then dispatch parallel read-only agents to verify only the suspicious docs against source, and finally propose update / delete / migrate-to-ADR dispositions for user approval. Use on a monthly or quarterly docs review, after large refactors or renames, or when asked whether docs are stale."
metadata:
  short-description: "docs の陳腐化を機械スキャン→並列実装照合→更新/削除/ADR移送の処遇提案まで定期監査する。"
dependencies: []
---

# Docs Freshness Audit

docs が実装と乖離していないかを監査し、「更新 / 削除 / ADR 移送」の処遇まで導く手順書。
バナー付きで放置された仕様書・実在しないモジュールを記述し続ける spec・merge 済みなのに
残っている計画ファイルは、残しておくと逆に混乱の元になる。

## Step 0: 導入先設定の確認

skill 本体は手順とプロンプトのみを持つ。以下を導入先の CLAUDE.md / rules /
ドキュメント保守ポリシーから拾ってから開始する (無ければユーザーに確認):

| 項目 | 例 |
|---|---|
| docs 検証コマンド | `make docs-okf`, `python scripts/validate_docs.py` |
| 監査除外 | ADR/デザイン等のバンドル (各自の管理規約に委ねる)、生成物 |
| 計画・設計出力ディレクトリ | `docs/plans/`, `docs/superpowers/plans|specs/` |
| 保守履歴の追記先 | `docs/documentation-maintenance.md` |
| 削除の運用 | docs chore の push 先ルール (直 push 可否) |

## Phase 1: 機械スキャン (安価・毎回実行)

各スキャンは bash で完結する。結果を「容疑ファイル一覧 (根拠つき)」に集約する。

1. **死んだソースパス参照**: docs 中のソースパス風文字列を抽出し実在をチェック

   ```bash
   git ls-files docs | grep "\.md$" | while read doc; do
     grep -oE "src/[A-Za-z0-9_/.-]+\.[a-z]+" "$doc" | sort -u | while read p; do
       [ -e "$p" ] || echo "$doc -> $p"
     done
   done
   ```

2. **死んだ内部リンク**: markdown 相対リンク (`](path)`) の参照先実在チェック
3. **自己申告バナー検出**: `DEPRECATED` / `Superseded` / `要確認` / `TBD` / `未解決` /
   `確認事項` を grep。バナーが付いたまま放置された文書は「既知の混乱源」として容疑化
4. **鮮度ギャップ**: doc の最終 commit 日と、記述対象コードの直近 churn を比較

   ```bash
   git log -1 --format=%ad --date=short -- "$doc"   # doc 側
   git log --since="$doc_date" --oneline -- "$src_area" | wc -l   # コード側の乖離量
   ```

5. **git から見えない残骸**: 監査対象ツリーの ignored / untracked ファイルを列挙。
   `git rm` は tracked しか消さないため、削除したつもりの生成物が disk に残る

   ```bash
   git status --ignored --porcelain docs/ | grep "^!!\|^??"
   ```

6. **消し忘れ計画ファイル**: 計画出力ディレクトリの各ファイルから Issue/PR 番号を抽出し
   `gh` で状態照会。**全て closed/merged なら「完了済み計画の残置」として削除候補**。
   番号参照の無い計画は経過日数で容疑化して Phase 2 送り

   ```bash
   grep -oE "#[0-9]+" "$plan" | sort -u | while read n; do
     gh issue view "${n#\#}" --json state --jq .state 2>/dev/null \
       || gh pr view "${n#\#}" --json state --jq .state
   done
   ```

## Phase 2: 意味監査 (容疑ファイルのみ・並列 read-only agent)

Phase 1 の容疑ファイルに対し、read-only agent を並列 dispatch して doc vs 実装を照合する。
機械スキャンでは「使われていない旧アルゴリズムを正として記述している」類の乖離は
検出できないため、このフェーズを省略しない (深監査時)。

プロンプトテンプレート:

```
<repo> で、ドキュメント <doc> (最終更新 <date>) と現在の実装の乖離を監査してください。

手順:
1. <doc> を全文読む
2. doc が言及するモジュール/クラス/関数/ウィジェットを現在の <src candidates> で確認
3. 乖離を列挙: (a) doc に書かれているが実装に存在しない要素、
   (b) 実装にあるが doc に無い主要要素、(c) 名前・シグネチャ・アルゴリズムの不一致
4. 同領域をカバーしうる live ドキュメント (<live doc candidates>) の有無を確認

出力: 乖離項目の箇条書き (doc 行番号 + 実装 file:line)。最後に判定を1つ:
「概ね正確 / 部分修正で足りる / 全面書き直しが必要 / 削除可 (live docs がカバー)」+ 根拠 1-2 文。
```

注意: agent の「参照されていない」報告は tracked/ignored の別まで自分で再検証する
(生成物が実は git 追跡されているケースの見逃しが実例としてある)。

## Phase 3: 処遇と実行 (ユーザー承認ゲート必須)

判定マトリクス:

| 状態 | 処遇 |
|---|---|
| live docs / 実装が同領域をカバー済み・固有価値なし | 削除 (git 履歴が保存する) |
| 現行機能の仕様だが記述が古い | 更新 (実装照合結果を反映) |
| 設計判断の記録としてのみ価値がある | ADR へ移送して原本削除 |
| 実装と一致 | 監査確認注記 (日付つき) を追記して維持 |
| 完了済み計画ファイル | 削除 |

- 候補一覧を根拠つきでユーザーに提示し、**承認を得てから**実行する (勝手に消さない)。
  グループ分け (確実な削除 / 要判断 / ローカルのみ) して複数選択で聞くと速い
- 実行後は Step 0 の検証コマンドを実行し、保守履歴に監査記録 (何を何故消した/直した) を残す
- ツールのデフォルト出力先 (skill が自動で書き込むディレクトリ等) は「散らかって見えても
  消さない」— 消してもツールが再生成する。代わりに役割分担をドキュメント保守ポリシーに明記する

## 実行モード

- **軽監査 (月次目安)**: Phase 1 のみ → 容疑ゼロなら記録して終了、あれば報告
- **深監査 (四半期目安 / 大規模リファクタ・リネーム後)**: Phase 1 + 2 + 3 フルセット

定期性は導入先の運用に委ねる (例: 月次 dependency review と同枠で人が起動)。
