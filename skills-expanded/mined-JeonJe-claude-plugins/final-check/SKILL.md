---
name: final-check
description: 산출물을 외부(리뷰어·평가자·팀·오픈소스)에 전달하기 직전의 최종 게이트. 요구사항 커버리지 매핑, 클린 클론 재현성, README 검증, 커밋 히스토리 점검, 시크릿/절대경로/개인정보 스윕을 증거 기반으로 수행한다. "최종 점검", "제출 전 확인", "전달 전 체크", "final check", "마지막 검토" 시 사용.
argument-hint: "<전달할 대상 디렉토리/레포 + (있으면) 원 요구사항 문서>"
---

# Final Check

Deliverable-side quality gate, run **after** implementation and review are done and **before** the work leaves your machine. The reader on the other side has none of your context — this gate verifies the artifact stands alone.

Every check produces evidence (command output, file citation). A check without evidence is ❓, never ✅.

## Phase 1 — Requirements coverage map

Take the original requirement source (spec document, issue, request message) and build the coverage table **from the requirements side, not from what you built**:

| # | Stated requirement | Where implemented (file/symbol) | Where verified (test/manual evidence) | Status |
|---|---|---|---|---|

- Status: `COVERED` / `PARTIAL` (state what's missing) / `NOT COVERED` (state why — deliberate descope needs one line of reasoning the reader will see) / `EXTRA` (built but never asked — flag it; unrequested scope reads as not understanding the ask).
- Ambiguous requirements you interpreted: record the interpretation and where it's documented for the reader.
- No requirement source available → reconstruct the implied checklist from the deliverable's own README/claims, and verify the artifact delivers what it promises.

## Phase 2 — Clean-clone reproducibility

The single highest-failure gate. Verify in an **isolated copy**, not your working tree:

```bash
git clone <repo> /tmp/final-check-clone && cd /tmp/final-check-clone
# then follow README literally, top to bottom
```

- Execute the README's setup/run/test instructions **exactly as written** — no steps from memory. Every command you must run that the README doesn't mention is a README bug.
- Check declared prerequisites vs reality: language/runtime version, package manager, required env vars (is there an `.env.example`?), external services (DB, docker) — can the reader actually satisfy them?
- Run the test suite from the clean clone and record the fresh output. "It passed earlier in my working tree" is not evidence.
- If a step cannot be run in your environment, mark it ❓ with the reason — do not silently assume it works.

## Phase 3 — README as the reader's entry point

The README is read before any code. Verify it answers, in order:

1. **What this is** — one paragraph, no jargon the reader doesn't have yet.
2. **How to run it** — verified in Phase 2.
3. **How it's structured** — enough of a map that the reader knows where to look first.
4. **Key decisions and trade-offs** — why this approach over alternatives; known limitations stated honestly (an honest limitation reads far better than a discovered one). Code shows *how*; only the doc shows *why* — a reviewer grades intent from this section, not from code.
5. **What's tested and how to run the tests.**
6. **Testability affordances** — a health-check endpoint (or equivalent readiness signal) and seed/sample data instructions, so a stranger (or an evaluation agent) can verify the system without asking you.

Additionally, when the work was built with an AI coding agent and the reader may evaluate that collaboration: keep an **AI collaboration record** (key prompts or agent instructions, and the decisions you made *against* or *beyond* the AI's suggestions). What you asked for is judged as part of the engineering — an absent or AI-retouched summary reads as "delegated without understanding". Keep decision records as **one shared document** for both human and AI readers (split docs drift): humans grade intent from it, and the AI reads it next session to avoid re-litigating settled decisions.

## Phase 4 — Commit history

The history is part of the deliverable — a reader often walks it to see how you work:

- Commits tell a coherent story (setup → feature A → feature B → hardening), not "wip / fix / fix2".
- No commit mixes unrelated concerns; messages state intent, not just what changed.
- No leftover debugging commits, commented-out blocks, or dead files from abandoned directions.
- If history is messy and the branch is private, consider an interactive cleanup **before** sharing; if already shared, leave it — rewriting published history is worse.

## Phase 5 — Leak and hygiene sweep

Run against the full tree, and treat every hit as guilty until proven a false positive:

```bash
# secrets and credentials
grep -rniE '(api[_-]?key|secret|token|passwd|password)\s*[:=]\s*['\''"][^'\''"]{8,}' . --exclude-dir=.git
# absolute personal paths and machine-local config
grep -rnE '/Users/[a-z]+|/home/[a-z]+|C:\\\\Users' . --exclude-dir=.git
# TODO/FIXME left for the reader to find
grep -rnE 'TODO|FIXME|HACK|XXX' . --exclude-dir=.git
```

- `.env`, credentials, and local config files are gitignored **and absent from history** (`git log --all --diff-filter=A -- '*.env*'`).
- Personal identifiers (emails, internal hostnames, other projects' names) appear nowhere unless intended.
- Dependencies: lockfile committed; no dependency added for a single trivial call.
- Repo size sanity: no build artifacts, `node_modules`, IDE dirs, or large binaries tracked.

## Phase 6 — Verdict

```markdown
## Final check: {target}

| Phase | Result | Evidence |
|---|---|---|
| Requirements coverage | n/m COVERED, k PARTIAL | coverage table |
| Clean-clone run | PASS/FAIL | fresh command output |
| README | PASS/gaps listed | section-by-section |
| Commit history | PASS/notes | log summary |
| Leak sweep | CLEAN/hits resolved | grep outputs |

VERDICT: READY | READY-WITH-NOTES | NOT READY
```

- `READY`: every phase has evidence; PARTIAL/NOT COVERED items are documented for the reader, not hidden.
- `NOT READY`: any unresolved leak-sweep hit, a failing clean-clone run, or an undocumented requirement gap. Fix and re-run the affected phase — do not hand-wave a red phase into notes.

## Anti-patterns

- Verifying reproducibility in the working tree where your global tools and env vars mask missing steps.
- Writing the coverage map from the code ("what did I build") instead of the spec ("what was asked") — misses silent omissions, which are the most expensive kind.
- Marking README steps ✅ from memory without executing them.
- Treating the leak sweep as done after one grep pattern — run all three families.
