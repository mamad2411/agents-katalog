---
name: gatebound-doctor
description: Diagnose the gatebound install across eight axes — plugin files, hook registration, project state, spec set, contract freshness, workers, python, Codex host layer — and offer the printed fixes. Korean triggers — "닥터 돌려줘", "설치 점검해줘", "훅이 안 먹는 것 같아", "게이트킷 상태 확인". English triggers — "run doctor", "diagnose gatebound", "why are my hooks not firing", "check the install". NOT for fixing the spec or approving a gate file, and NOT for reporting an unverified axis as if it passed.
user-invocable: false
---

# gatebound-doctor

Invoke `/gatebound:doctor`, passing `--json` through when the user asked for
machine output.

Do not diagnose by reading files yourself. `plugin/commands/doctor.md` is the
execution instruction; this file only routes to it.

Exit code 0 means nothing failed, not that everything was checked. An
`unverified` axis was not checked; report it that way.

Under a host without slash commands (Codex), `/gatebound:doctor` does not exist:
read `commands/doctor.md` two directories above this skill's folder and follow
it, applying `policy/codex.md` from the same plugin.
