# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: other/rebase-stack/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: スタックした PR (下段の上に上段を積む構成) を、下段の変更に追随させて上段へ rebase 伝播し、各段を検証して push する。下段がマージされた・衝突した・リモートが消えた等の分岐を判定しながら段を上がる。ユーザーが「スタックを積み直して」「rebase を伝播して」「/rebase-stack」等を指示したときに使う。
