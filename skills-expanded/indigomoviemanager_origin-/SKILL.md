# IndigoMovieManager — Cursor 向けリポジトリルール

## Git コミットメッセージ（自動生成時）

Cursor が Source Control の「コミットメッセージ生成」や関連の AI 提案を行うときは、**必ず日本語**で書く。

- 文体: 簡潔な1行（必要なら2行まで）。体言止めや英語の説明文は避ける
- 接頭辞: 必要に応じて `feat:` / `fix:` / `ci:` / `refactor:` / `docs:` / `test:` を付ける
- 内容: 変更の「なぜ・何が変わるか」を優先し、ファイル名の羅列は避ける
- 例:
  - `feat: ステータスバーで進捗を常時表示する`
  - `fix: MessageBoxEx の長文が右端で切れる問題を修正`
  - `ci: リリース用 publish 出力先を artifacts に固定`

直近のコミットが英語でも、このリポジトリでは日本語を優先する。

## main マージとリリースノート

ユーザーが **main へのマージ** を指示した場合:

1. **すぐにはマージしない。** まず前回 GitHub Release タグ以降のコミットから「主な変更点」を **3〜7 行の日本語箇条書き**で下書き提示する（`ci:` / バージョン更新 / merge コミットは除外。ユーザー向けの文言にし、`feat:` 等の接頭辞は外す）。
2. ユーザーが編集するか、そのまま承認するまで待つ。
3. 「リリースノート承認」「マージ開始」など **承認とマージ開始が同じ指示に含まれる**ときだけ、`docs/release-notes-changes.md` に箇条書きを書き込み、その変更を含めて main へマージする。
4. `docs/` / `.github/` / `tools/` のみの変更ではバージョンは上がらない（CI の paths-filter）。アプリ本体と一緒にマージするときだけ Release が走る。

手書きソース: `docs/release-notes-changes.md`（`- ` 行のみ本文へ）。テンプレ: `docs/release-notes-template.md`。プレビュー: `.\tools\Build-ReleaseNotes.ps1 -Version <ver>`。
