# Repo Ref
- source: https://github.com/mamad2411/agents-katalog (path: skills-expanded/topic-ayutaz-piper-plus-watch-ci-patterns/SKILL.md, branch: master)
- mined: 2026-11-24
- desc: CI workflow の最近 run を集計し、 failure を「flake / drift / env / test bug」に自動分類する skill。 既存 `/watch-pr <PR>` の workflow-level 拡張。 引数なしで全 workflow の health check、 `--workflow <name>` で個別 workflow の最近失敗パターンを抽出
