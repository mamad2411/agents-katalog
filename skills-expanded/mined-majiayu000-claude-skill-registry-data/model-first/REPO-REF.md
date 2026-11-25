# Repo Ref
- source: https://github.com/majiayu000/claude-skill-registry-data (path: other/model-first/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: 相互依存ルール＋状態＋関与が多いシステムを実装する前に、モデル（実体・不変条件・語彙）を明示して固定する front-load。暗黙モデルの連鎖破綻（多実体の整合が silent に崩れる型）を loud な不変条件に変える。ゲーム/シミュレータ/スケジューラ/パーサ/プロトコル等、局所変更が全体に波及しうる実装の着手前に起動。引数 = <これから作るシステムの1行>
