---
name: coding-conventions
description: 코드를 작성·수정·리뷰할 때 적용하는 코딩 컨벤션. 네이밍, 주석, 매직 리터럴, git add, 테스트 단언, 인프라 클라이언트 부팅, finally 마스킹 등 실전에서 반복 검증된 규칙 모음. 코드 작성, 코드 리뷰, 리팩토링, 컨벤션 확인 시 사용.
---

# Coding Conventions

Rules distilled from recurring review findings and production incidents. Each rule carries a one-line WHY; heavier rules keep their mechanics and precedents in `references/`.

## How to apply

1. Before writing code, read the target module's existing patterns first — new code mirrors the module's standard pattern (rule §4).
2. While writing or reviewing, check the core rules below.
3. When a rule's short form isn't enough to judge, read its detail file in `references/` before making a verdict.

## Core rules (short form)

| § | Rule | Detail |
|---|---|---|
| 1 | No external metadata (ticket IDs, spec section numbers, volatile magic values) in code comments/names | `references/conventions-core.md` |
| 2 | No meta-words (`Value`, `Helper`, `Util`, `Manager`) in names — use domain nouns/intent verbs | same |
| 3 | No comments restating obvious code — comments are for non-obvious WHY only | same |
| 4 | New code mirrors the module's existing pattern | same |
| 5 | Explicit `git add` — never `-A`/`.` | same |
| 7 | Paired algorithmic constants: changing one requires re-verifying the other | same |
| 13 | Reuse existing infra/harness; existence is not effectiveness — prove it fires | `references/s13-existing-infra-reuse.md` |
| 14 | Re-verify inherited claims against HEAD before propagating | `references/s14-inherited-claims.md` |
| 16 | finally/catch side work must never mask the main flow's result | `references/s16-finally-masking.md` |
| 17 | Infra clients: boot-time synchronous connect and conditional bean consumption are deliberate contracts | `references/s17-infra-client-boot.md` |
| 19 | Strong negative verdicts ("impossible / converges to zero") need one runtime observation first | `references/s19-runtime-observation.md` |
| 22 | `rg -r` is `--replace`, not recursive — verify exact literals with `grep -n` or Read | `references/conventions-core.md` |
| 23 | New dependencies pass a review gate (stdlib first, maintenance, duplicate-role check) | `references/conventions-core.md` |

## References index

| File | Read when |
|---|---|
| `references/core-principles.md` | top-level behavior: evidence first, surgical changes, root cause, verification reporting |
| `references/conventions-core.md` | full rule text with WHY + anonymized precedents |
| `references/s13-existing-infra-reuse.md` | adding a cache/retry/alert path, or about to say "can't measure / doesn't exist" |
| `references/s14-inherited-claims.md` | copying a claim from an older doc/MR into a new artifact |
| `references/s16-finally-masking.md` | writing finally/catch blocks, instrumentation, or lock release |
| `references/s17-infra-client-boot.md` | adding/consuming an infra client bean (Redis, MQ, etc.) |
| `references/s19-runtime-observation.md` | about to conclude something is impossible/zero/unmeasurable |
| `references/readable-code.md` | naming, early-return/guard clauses, Tell-Don't-Ask, SOLID violation signals |
| `references/coding-conventions-java.md` | Java: enum↔DB mapping, magic literals |
| `references/domain-model-guidelines.md` | designing domain models / state-transition methods |
| `references/patterns.md` | common API response / repository / hook patterns |
