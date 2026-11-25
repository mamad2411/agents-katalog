# Repo Ref
- source: https://github.com/kewton/commandmate (path: .agents/skills/cmate-verify/SKILL.md, branch: main)
- mined: 2026-11-23
- desc: リポジトリの検証ゲート（lint / typecheck / test / build 等）を .commandmate/verify.yaml に宣言し、worktree の cwd で逐次実行して exit code で合否を判定する。verify.yaml が無いリポジトリでは CI 定義から起案する。作業完了を主張する前の検証や、並列ワーカーの完了判定に使う。
