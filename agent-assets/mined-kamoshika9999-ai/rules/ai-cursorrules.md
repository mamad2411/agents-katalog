VBA.txt は **生産管理_AI配台テスト.xlsm** に貼り付ける VBA のテキストバックアップ（Python 起動・LOG・結果_* / 個人_* 取り込み・フォント・ボタン等）。

出勤簿.txt は **master.xlsm** に貼り付ける VBA のテキストバックアップ（〇月カレンダー→メンバー出勤簿・条件付き書式の実体化・かっこいいボタン等）。

**データの役割**: `planning_core.MASTER_FILE` は `master.xlsm`（skills / need / メンバー別勤怠）。段階2で VBA が `TASK_INPUT_WORKBOOK` に **配台ブック（ThisWorkbook）** を渡し、その中の「加工計画DATA」等を読む。Python のカレントは `main.py` 所在フォルダ（通常は `master.xlsm` と同じディレクトリ想定）。

**VBA.txt・結果シート取り込み（次回以降の修正の前提）**
- `Set ws = ThisWorkbook.Sheets(Sheets.Count)` だけだと、末尾が VeryHidden の **`_FontPick`（SCRATCH_SHEET_FONT）** 等の固定シートのとき **コピー直後の「結果_*」ではなく誤参照**する。`結果シート_列幅_AutoFit安定` の `targetWs.Name` が `_FontPick` になる現象の原因になり得る。
- 対策: **`取込ブック内のコピー先シートを取得(wb, expectedSheetName)`** — ① `wb.Sheets(取り込み元と同名)` を優先 ② だめなら `Sheets(Count)`（末尾が `_FontPick` でなければ採用）③ 末尾が `_FontPick` なら同名シートを総当たり。7a production_plan 取り込み・7b 個人シート新規コピーで `Sheets(Count)` の代わりに使用。
- **列オートフィット** `結果シート_列幅_AutoFit安定`: 引数は **`targetWs`**（呼び出し元 `ws` とデバッガで混同しない）。**`targetWs` が `_FontPick` なら Exit Sub**。処理は一時 **`Application.ScreenUpdating = True`** のうえ **`targetWs.Activate` → `DoEvents` → `Cells.Select` → `DoEvents` → `Cells.EntireColumn.AutoFit`**、最後に元の ScreenUpdating を復帰（取り込み中 False のままだと Select が確定前に AutoFit が走る問題の対策）。
- 計画結果の **列幅は Python（openpyxl）では設定せず**、取り込み時の上記 VBA に任せる方針。

あなたはエクセルVBAの専門家です

---

## Git: AI によるコミットメッセージ（ソース管理の Generate）

- **必ず日本語**で書く。英語だけの件名・本文は出さない。
- 1行目は変更内容が一目で分かる短い要約（目安 50 文字以内）。必要なら空行のあとに箇条書きで詳細。
- 例: `修正: output を .gitignore に追加し Git 追跡を解除` / `追加: EC 行が無い依頼では検査のロール上限をかけない`
- Conventional Commits 形式を使う場合も **説明は日本語**（例: `feat: ログイン画面を追加`）。

Generate commit messages in Japanese only. Never use English-only commit message subjects.

---

## Git: ソース変更前のローカルコミット

正本: リポジトリ直下 **`.cursor/rules/pre-edit-git-commit-push.mdc`**（`alwaysApply: true`）。

- **ローカルコミットは、ソースコード等の変更前に実行する**（編集ツール使用前に `git status` → 対象があればコミット。作業ツリーがクリーンなら省略）。
- **コミットメッセージは、そのターンのユーザーのチャットメッセージの先頭から最大 300 文字**とする。
- **`git push` は自動では実行しない**。

---

## 配台ロジック変更時のドキュメント

正本: リポジトリ直下 **`.cursor/rules/dispatch-docs-sync.mdc`**（`alwaysApply: true`）。

**`細川/GoogleAIStudio/テストコード/python/planning_core.py` をはじめ配台ロジックを変えたときは、必ず `細川/GoogleAIStudio/テストコード/配台ルール.md` と `細川/GoogleAIStudio/テストコード/配台ルール.html` を同じ変更内容に合わせて更新する。**
