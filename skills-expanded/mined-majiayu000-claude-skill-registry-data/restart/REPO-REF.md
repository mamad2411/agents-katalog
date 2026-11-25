# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: design/restart/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 手詰まりが見えている session/project を「連鎖破綻」と判定し、パッチを止めて再モデル化から建て直す recovery。局所バグなら fix へ routing し建て直さない（過剰 restart 防止）。診断→salvage→意図再接地→再モデル化→建て直しの順。引数 = <手詰まりの症状＋対象 project（あれば継承元 session id）>
