---
name: gatebound-verify
description: Verify the build against the completion contract using an independent read-only evaluator, then report a verdict per criterion and per E2E step. Korean triggers — "검증해줘", "다 됐는지 확인해줘", "완료 기준 통과했는지 봐줘", "E2E 돌려줘". English triggers — "verify it", "check if it is done", "run the completion contract", "did it pass the gate". NOT for fixing what the verification finds — route failures back to /gatebound:build — and NOT for grading code this same session just wrote without spawning the evaluator.
user-invocable: false
---

# gatebound-verify

Invoke `/gatebound:verify`, passing any criterion id the user named as the
argument.

Do not run the criteria and call that verification. `plugin/commands/verify.md`
is the execution instruction; this file only routes to it.

Producer is never evaluator: the command spawns a separate read-only agent, and
`unverified` stays `unverified` in the report.

Under a host without slash commands (Codex), `/gatebound:verify` does not exist:
read `commands/verify.md` two directories above this skill's folder and follow
it, applying `policy/codex.md` from the same plugin.
