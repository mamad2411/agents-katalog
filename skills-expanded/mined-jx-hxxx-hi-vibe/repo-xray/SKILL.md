---
name: repo-xray
description: >-
  Evidence-based repository structure analysis for Python and
  JavaScript/TypeScript (js/jsx/ts/tsx) projects. Runs a bundled scanner
  script and answers only from its JSON output — never from guessing. Use this skill whenever the user asks about
  duplicate code, unused/dead code, "does function X already exist?",
  cleaning up or refactoring the codebase, oversized files, or repo
  structure health — including Korean phrasings like "중복 코드 찾아줘",
  "안 쓰는 코드/죽은 코드 정리", "이런 함수 이미 있어?", "구조 분석해줘",
  "정리할 거 알려줘", "리팩토링 뭐부터 해?". Also use it before writing a
  new helper function when there is a real chance an equivalent one
  already exists in the repo.
user-invocable: false   # 사용자 표면은 /hi-vibe:* 명령 10개다. 스킬까지 슬래시 메뉴에 나오면 16개가 되어 "외울 게 적다"는 약속이 깨진다. Claude의 자동 호출은 그대로 유지된다.
---

# repo-xray

A repo evidence engine: a script produces machine evidence, and you turn
that evidence into short, kind, actionable advice. The reader may be new
to coding — plain words, no tool jargon, at most three suggestions at a
time unless they ask for a full report.

<HARD-GATE>
## Core Contract — the line that must not blur

```
NO STRUCTURAL CLAIM WITHOUT RUNNING THE SCRIPT
NO ABSENCE CLAIM WITHOUT STATING THE SCAN RANGE
A DEAD "CANDIDATE" IS NOT A VERDICT
```

If you have not run the script in this session, do not state counts
("unused functions: 12") or absence ("that function doesn't exist").
Run it first, read the JSON, then make the smallest true claim the
evidence supports. Cross this line and the tool becomes a confident
guesser — exactly the failure it exists to prevent.
</HARD-GATE>

## Commands

Run from anywhere; point `--root` at the repo being analyzed.

```bash
# Full structure scan -> writes <root>/.repo-xray/report.json
python3 <skill-path>/scripts/audit.py scan --root <repo>

# "Does X exist anywhere?" -> exact hits + similar names, prints JSON
python3 <skill-path>/scripts/audit.py find <name> --root <repo>
```

`<skill-path>` is this skill's directory — in plugin installs that is
`${CLAUDE_PLUGIN_ROOT}/skills/repo-xray`. The scan needs only Python 3
(stdlib) — no installs. Suggest adding `.repo-xray/` to `.gitignore`
once, the first time a scan runs in a repo.

### 실행 시간 — 느린 것 ≠ 멈춘 것

스캔은 저장소 크기에 따라 **수 초에서 수십 초**가 걸린다(함수가 많으면
near-duplicate 비교가 가장 오래 걸린다). 이건 정상이다. **짧은 타임아웃으로
끊고 다시 돌리지 마라** — 죽은 줄 알고 재실행하면 프로세스만 겹쳐 쌓여
머신이 포화되고 오히려 더 느려진다(관측된 실패 모드다). 오래 걸릴 것 같으면
**한 번만 백그라운드로 돌리고 완료를 기다린 뒤** `report.json`을 읽어라.
스캔은 끝나면 항상 리포트를 쓰므로, 리포트가 없으면 "아직 도는 중"이지
"고장"이 아니다. `near_duplicate_scan_truncated: true`가 보이면 near-dup만
시간 상한에 걸려 일부 생략된 것이고, 나머지 결과는 완전하다.

## Which command for which question

- "중복 코드 있어?", "정리할 것 알려줘", "구조 어때?", "안 쓰는 코드?"
  → `scan`, then read `report.json`.
- "X라는 함수/기능 이미 있어?", "어디서 쓰여?" → `find X`. If the user
  describes a behavior rather than a name ("환율 바꾸는 거"), run `find`
  on 2-3 plausible names (e.g. `exchange`, `usd_to_krw`, `convertRate`)
  and also check `similar_symbol_names` in the output.
- Before writing a new helper the repo might already have → `find` first.

## Reading the evidence honestly

The scanner counts name references across all scanned text files. That
means dynamic uses are invisible to it — and you must say so instead of
pretending certainty:

- `dead_candidates` means "no reference found in the scanned CODE files",
  never "safe to delete". Check each candidate's `decorated` flag:
  decorated Python functions are usually route handlers or hooks that
  frameworks call by registration, not by name — do not suggest deleting
  those; at most mention they *look* unreferenced.
- **Check each candidate's `looks_wip` flag FIRST.** A `looks_wip: true`
  symbol is unfinished (pass/`...`/NotImplementedError/TODO) — its zero
  references mean "not wired up YET", not "dead". **Never suggest deleting
  it**; ask if it's still under development. This is the "죽은 코드 vs 아직
  안 만든 코드" distinction (FP-07) — the scan can't tell them apart by
  references, so this flag is the guard.
- Doc mentions don't rescue: a name that appears only in `.md`/`.css`
  files stays a dead candidate, with those files listed in
  `doc_mentions`. If the user deletes the code, remind them to fix the
  listed docs in the same turn (docs-keeper contract).
- Names built dynamically (`getattr`, string keys, template strings,
  event names in HTML attributes outside scanned files) will not show up
  as references. When recommending deletion, always phrase it as "the
  scan found no references in N files — worth double-checking X before
  removing".
- `duplicate_functions` matches identical logic (same AST with function
  name AND local variable names normalized away). These are strong
  evidence — safe to present as real duplicates.
- `near_duplicate_functions` are pairs ≥90% similar after the same
  normalization — the typical AI failure of re-implementing something
  "almost the same". WEAKER evidence: read both functions before
  claiming duplication; present as "비슷한 구현 의심 — 두 함수를 같이
  보세요", never as a verdict. This list SHOWS only the most-similar few;
  `near_duplicate_total` is how many were actually found. If
  `near_duplicate_total` > the shown count, say "상위 N개 (총 M개)" — do
  not imply the shown pairs are all of them.
- JS/TS symbol extraction is regex-based (no parser): class methods and
  exotic declaration forms may be missed. Say so when a TS-heavy repo
  question depends on completeness.
- For absence answers, quote the scan range from the JSON:
  "backend/frontend의 N개 파일을 스캔했는데 없었어요" — not "없어요".

Before presenting any dead/duplicate/collision finding, screen it against
`references/false-positive-index.md` — known ways this scanner gets
fooled, each with the softer phrasing to use. Translate matches into
plain-language reasons **in the user's language**; don't cite FP ids
unless asked for proof.

### 하다 만 흔적 버킷 (정리 대상과 다른 성격)

`swallowed_errors`·`todos`·`test_coverage`는 "지울 것"이 아니라 **"마저 할
것"**이다. 같은 목록에 섞지 말고 따로 묶어 보여줘라.

- `swallowed_errors` — 저장소 전체의 에러 삼킴. 훅은 **새로 쓰는 코드만**
  보므로, 훅을 깔기 전 코드와 남이 짠 코드는 여기서 처음 검사된다. 판정
  규칙은 PostToolUse 훅과 같은 정의를 공유한다.
- `todos` — 남겨둔 TODO/FIXME. 본인이 적은 메모라 근거가 확실하지만,
  테스트 픽스처 안의 문자열처럼 진짜 할 일이 아닌 것도 걸린다(검증 필요).
- `test_coverage` — 모듈 수 대비 테스트 파일 수 **요약만**. 파일별로
  나열하지 않는다 — 테스트 없는 프로젝트에서 모든 파일을 후보로 올리는 건
  발견이 아니라 소음이다.
- `scan.unavailable`이 비어 있지 않으면 **무엇을 못 봤는지 그대로 밝혀라.**
  못 돌린 검사를 침묵으로 넘기면 "깨끗하다"로 잘못 읽힌다.

### `hardcoded_secrets` — 다른 버킷과 다르게 다뤄라

이건 "마저 할 것"도 "검토 후보"도 아니다. **있으면 지금 조치해야 하는
것**이라 위 버킷들과 섞지 말고 **맨 위에 따로** 올려라.

- 0건이면 줄을 만들지 마라. 있을 때만 눈에 띄게.
- **값을 절대 출력하지 마라.** 리포트에도 파일·줄·종류만 담겨 있다
  (대화창이 키 유출 통로가 되면 안 된다). "무슨 키인지" 궁금해하면
  사용자가 직접 그 줄을 열어 보게 안내한다.
- 훅은 Write/Edit로 **새로 쓰는** 코드만 본다. Bash(heredoc·`sed -i`·생성
  스크립트)로 들어온 키는 훅을 통과하므로 **이 스캔이 유일한 그물**이다.
  그래서 "훅이 잡아줬을 텐데"라고 넘기지 마라.
- 조치는 사용자가 정한다. 의도한 것(공개 예제 키·테스트 픽스처)이면
  그 줄에 `hi-vibe: allow-secret` 주석을 달면 훅·스캔 양쪽에서 빠진다.

### 후보를 던지지 말고 검증해서 줄여라 (proof-eyes)

스캔이 끝나면 **`proof-eyes` 에이전트를 Agent 도구로 소환한다.** 기본값이지
옵션이 아니다. 스캐너는 놓치지 않는 대신 헛짚으므로, 후보 20건을 그대로
내밀면 사용자는 뭐가 진짜인지 몰라 전부 무시한다.

- 전달할 것: ①저장소 경로 ②`report.json`의 후보 묶음(또는 그 일부).
- 에이전트가 하는 일: **후보 자리의 실제 코드를 열어** 진짜인지 판정하고,
  오탐 계열을 거르고, 정리 방향까지 한 줄로 준다. 지우지는 않는다.
- 후보가 많으면 버킷별로 나눠 여러 개를 병렬 소환한다. 고르라고 묻지 말고,
  그렇게 한다는 것과 토큰을 더 쓴다는 것을 한 줄로 알리고 진행한다.
- 판정이 돌아오면 요약해 전하되, **버린 것도 숫자로 밝힌다** — "후보 12건 중
  진짜 3건, 오탐 9건". 조용히 줄이면 스캐너가 못 찾은 것처럼 읽힌다.

**생략하는 경우**: 후보가 0건일 때뿐이다. 그때는 "스캔 범위 N개 파일에서
후보 없음"으로 끝낸다. 사용자가 "빠르게/목록만"이라고 했으면 원본 목록을
주되, **검증을 안 거쳤다는 사실을 밝힌다** — 끄는 건 플래그가 아니라 말로 한다.

Full field-by-field JSON guide: read `references/report-format.md` when
you need to interpret a field not covered above.

## Answer shape

Default voice: everyday words, headline-level compression, file:line
kept visible. Lead with the direct answer, then up to three concrete
next steps, each backed by evidence (`file:line`, counts, scan range).
Offer the full list ("전체 목록 보여드릴까요?") instead of dumping it.
Expand raw JSON only when the user asks for proof or detail.

## hi-vibe catch — 반사실적 발견에만 공을 밝힌다

스캔이 **사용자가 몰랐던 것을 드러냈을 때만**(예: 자기도 잊고 있던 죽은 코드,
모르고 두 번 짠 중복 함수) 답변 맨 끝에 한 줄을 더한다. 세 조건을 **모두**
만족할 때: ① 이 스캔이 찾았다(사용자가 자발적으로 짚은 게 아니다) ② 진짜
정리 대상·구조 문제다(스타일이 아니다) ③ 스캔 전엔 레이더 밖이었다 —
안 돌렸으면 놓쳤을 것이다.

형식(문구는 사용자 언어로, `👋 hi-vibe` 접두사는 고정 — 나중에 grep 가능하게):
`👋 hi-vibe가 방금 <무엇>을 잡았어요 — repo-xray 스캔.`

**과장 금지(핵심):** 셋 중 하나라도 아니면 넣지 마라. `dead_candidates`처럼
"확인이 더 필요한 후보"에 확정처럼 공을 붙이지 말고, 사용자가 이미 알던 것에도
붙이지 마라 — 조용히 일하는 스캐너의 신뢰가 깨진다. 이 표기는 자화자찬이 아니라
스캐너가 실제로 무엇을 살렸는지를 보이게 하는 창이다.

## Red flags — stop and re-run instead

- about to state a count without a scan in this session
- about to say "없어요/no such function" without naming the scan range
- about to recommend deleting a `decorated` candidate
- about to present a finding without screening it against
  `references/false-positive-index.md`
- reusing a stale `report.json` after the code has changed this session
