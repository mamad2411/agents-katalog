---
name: init-project
description: リポジトリを新規プロジェクトの標準構成（README / LICENSE / CONTRIBUTING / AGENTS.md / CLAUDE.md / .gitignore / .gitattributes / .editorconfig / docs/public / docs/internal/adr / .claude）と突き合わせ、無いファイルだけを作る。GitHub か GitLab か、SECURITY.md・CHANGELOG.md・issue / PR テンプレートなどの要否は質問で選ぶ。新しいリポジトリを始めるとき、既存のリポジトリに足りない標準ファイルを揃えたいとき、「init-project」「雛形」「標準構成」に言及したときに使う。
compatibility: Designed for Claude Code
---

リポジトリを標準構成と突き合わせ、**無いファイルだけ**を作る。既存のファイルは上書きしない。標準構成の定義は
依存パッケージ `project-layout`（SKILL.md と `layout.json`）にあり、このスキルはそれを読んで作る。作成は同梱の
スクリプトが行い、このスキルは入力を集めて結果を報告する。

## 手順

1. **入力を集める。** 対象は作業ディレクトリ。プロジェクト名はディレクトリ名、著作権者は `git config user.name`。
   取れなければ聞く。
2. **ADR の置き場を決める。** `project-layout` スキルの「置き場の決め方」に従う。既存の置き場に ADR があれば、
   スクリプトは 0001 を作らない。
3. **AskUserQuestion で 3 問を 1 回で聞く。** 2 問目と 3 問目は `multiSelect: true`。選択肢は `layout.json` の
   `optional`（キー・`label`・`purpose`）と同じ。
   - ホスティング: GitHub / GitLab
   - 文書: `SECURITY.md`（脆弱性の報告先）/ `CODE_OF_CONDUCT.md`（行動規範）/ `SUPPORT.md`（質問の窓口）/
     `CHANGELOG.md`（リリースの変更履歴）
   - ホスティングの設定: issue テンプレート / PR（MR）テンプレート / `CODEOWNERS`
4. **スクリプトを実行する。** `<skill-dir>` は、このスキルの起動時に示される Base directory。

   ```bash
   python3 -I <skill-dir>/scripts/init_project.py --target . --hosting <github|gitlab> \
     --with <選んだもの> --adr-dir <手順 2> --name <名前> --holder <著作権者>
   ```

   `--with` には、選んだものの `optional` のキーをカンマ区切りで渡す。置き場はスクリプトがホスティングに応じて
   `layout.json` から選ぶ。スクリプトは隣の `project-layout/layout.json` を読み、見つからなければ止まる。
5. **結果を報告する。** スクリプトは JSON（`created` / `existing` / `warnings`）を出す。
   - 作ったファイルと、既にあったので触らなかったファイルを分けて示す。
   - `<!-- ... -->` の埋め残しがあるファイル（README・CONTRIBUTING・SECURITY など）を挙げ、埋める内容を聞く。
   - `warnings` に AGENTS.md / CLAUDE.md が挙がったら、足す内容（「置き場の規約」節、`@AGENTS.md` の行）を示し、
     承認を得てから既存ファイルを編集する。
   - git リポジトリでなければ、そのことを伝える（`git init` はしない）。コミットもしない。
