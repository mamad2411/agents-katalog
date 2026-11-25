# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: other/loop-ai-reviews/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: AI レビューの起動 → 完了待ち → 指摘への対応までを1周として実行する。引数で回数を渡せば、その回数を上限に繰り返す (省略時は1周)。ワークフローが失敗した周は成功にカウントせず再リクエストし、指摘ゼロになった時点で残りの周は消化しない。ユーザーが「AI レビュー回して」「AI レビューを N 周回して」「/loop-ai-reviews」等を指示したときに使う。
