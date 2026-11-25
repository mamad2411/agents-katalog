---
name: cleanup-storage
description: Only use when the user explicitly invokes /cleanup-storage (or $cleanup-storage in Codex). Never auto-invoke. ローカルマシンのストレージ逼迫を解消するスキル。ディスク使用量を調査し、削除候補を安全度カテゴリ順に整理して提示し、カテゴリごとにユーザー承認を得てから削除し、空き容量の変化を報告する。
disable-model-invocation: true
metadata:
  tags: [storage, cleanup, maintenance, local-environment]
---

# Storage Cleanup（cleanup-storage）

ローカルマシンのストレージ逼迫を、調査 → 安全度分類 → カテゴリ別承認 → 削除 → 効果測定の順で解消するスキル。「うっかり消えた」を構造的に起こさないことを最優先にする。

## 原則（すべての Phase で有効）

- **承認なくして削除なし**: ユーザーが承認したカテゴリ以外に手を付けない。承認は Phase 3 のカテゴリ単位で得る
- **測ってから提案する**: 削除候補は必ず `du` で実測サイズを確認してから提示する。推測サイズで提案しない
- **生成物だけを削除する**: ツールが再生成・再取得できるものだけを削除対象にする。ユーザー作成物か生成物か判別できないものは L3（要確認）以上に分類する
- **削除後に効果を測る**: `df` の前後比較で回収量を報告する

## Phase 1: 全体調査

進捗追跡のため、次のチェックリストを応答に貼って進める。

```
- [ ] Phase 1: 全体調査（df + du ドリルダウン）
- [ ] Phase 2: 安全度分類（L1〜L4）
- [ ] Phase 3: カテゴリ別提案と承認（Gate）
- [ ] Phase 4: 承認カテゴリの削除実行
- [ ] Phase 5: 効果測定と報告
```

1. 全体像を記録する: `df -h /System/Volumes/Data`（macOS）/ `df -h /`（Linux）。この値が Phase 5 の比較基準になる
2. ホーム直下の内訳: `du -h -d 1 ~ 2>/dev/null | sort -rh | head -25`
3. 主要ディレクトリを個別測定する: `du -sh ~/Library ~/Downloads ~/Documents ~/Desktop <リポジトリ置き場> 2>/dev/null | sort -rh`（手順2だけでは欠落することがある。Gotchas 参照）
4. 大きいディレクトリを `du -h -d 1 <dir> 2>/dev/null | sort -rh | head -20` で再帰的にドリルダウンする（`-d 2` も有効）
5. リポジトリ置き場がある場合は生成物を横断集計する:

   ```bash
   find <repos> -type d -name node_modules -prune 2>/dev/null | xargs du -sk 2>/dev/null | awk '{s+=$1} END {printf "%.1f GB\n", s/1024/1024}'
   ```

## Phase 2: 安全度分類

Phase 1 で見つかった削除候補を4カテゴリに分類する。定番の対象・削減コマンド・削除後の影響は [references/known-cleanup-targets.md](references/known-cleanup-targets.md) を読んで突き合わせる。

| レベル | 定義 | 例 |
|---|---|---|
| L1 | 再生成可能キャッシュ。削除しても次回自動再生成され機能損失なし | pnpm store・Homebrew・Docker ビルドキャッシュ |
| L2 | 再構築可能な生成物。削除後の初回利用時に再構築コスト（ダウンロード・ビルド）がかかる | node_modules・Docker イメージ・Playwright ブラウザ・30日超のエージェントセッションログ |
| L3 | おそらく不要だが、用途がユーザーにしか分からないもの | インストーラー / ISO・使わなくなったツールのデータ・tmp/ のテスト残骸 |
| L4 | ユーザーデータ。**削除対象にしない**。退避（外部ストレージ・クラウド）の提案のみ行う | 撮影素材・レンダリング出力・Downloads 内の文書 |

## Phase 3: カテゴリ別の提案と承認（Gate）

1. L1 から順に、カテゴリごとに「対象パス・実測サイズ・使う削減コマンド・削除後の影響」を表で提示する
2. カテゴリ単位でユーザーの承認を得る（選択式の質問ツールが使えるなら使い、無ければテキストで明示回答を待つ）
3. **承認されたカテゴリだけ**を Phase 4 で削除する。回答を得るまで削除に着手しない
4. L4 は承認の対象にしない（退避の提案のみ）。ユーザーが個別に「これを削除して」と明示した項目だけ削除してよい

## Phase 4: 削除実行

- 公式の削減コマンドがあるものはそれを優先する（`pnpm store prune`・`docker image prune -a`・`brew cleanup` 等）。`rm` より安全で、使用中のものを壊さない
- `rm` を使う場合は `rm -r`（`-f` なし）を使う。`-f` は権限モードによって拒否される環境があり、自己所有ファイルの削除に必要になる場面もない
- 「古いものだけ削除」は `find <dir> -type f -mtime +30 -delete` の形にし、除外すべきサブパス（メモリ・恒久データ）を `-not -path` で明示してから実行する
- Git リポジトリ内のファイルを消す前に `git check-ignore` で追跡外であることを確認する（追跡中なら削除せずユーザーへ報告）

## Phase 5: 効果測定と報告

1. `df` を再実行し、Phase 1 の基準値との差分（回収量）を報告する
2. 実行した削除の一覧（対象・回収量・削除後に必要な操作）を表で示す
3. 削除しなかった大物（L3 未承認・L4）を「残る候補」として提示して終了する

## Gotchas

- `du -h -d 1 ~` は macOS の TCC 保護ディレクトリ（Downloads・Documents・Desktop・Library）を黙って欠落させることがある。上位が小さいドットディレクトリばかりなら欠落を疑い、主要ディレクトリを明示パスで個別測定する
- `~/.Trash` と `~/Library` の一部は、ターミナルに Full Disk Access が無いと読めない（Operation not permitted）。ゴミ箱は Finder で空にするようユーザーに促す
- 設定ディレクトリがリポジトリへの symlink のことがある（例: `~/.claude` → 設定管理リポジトリ）。その中のセッションログはリポジトリ側の実体を測り、`.gitignore` 済みであることを確認してから消す
- Playwright ブラウザキャッシュ（ms-playwright）を消したら、報告に「次回 E2E 実行前に `playwright install` での再取得が必要」と含める
- `pnpm store prune` は既存プロジェクトの node_modules に影響しない（実体が独立しているため）。削減量が大きくても異常ではなく、消えた分は次回 install 時に再取得される
- Docker の実容量は `docker system df` で確認する。OrbStack はイメージ削除後にディスクイメージを自動圧縮するため、ホスト側の実容量回収は少し遅れて反映される
