---
name: blind-spot-pass
version: 1.0.0
description: Use *before* starting work in a domain you don't know well, to surface the "unknown unknowns" — the things you don't even know to ask about — and learn just enough to prompt and decide well. Implements the "blind spot pass" pattern from Anthropic's Fable "finding your unknowns" field guide. Triggers when you say "I'm new to this", "I don't know what to ask", "teach me before we start", "blind spot pass", "unknown unknowns", "find my unknowns", or the Korean "내가 뭘 모르는지 알려줘" / "이 분야 처음인데" / "먼저 가르쳐줘" / "블라인드 스팟", or when you hand off a task while admitting you're a non-expert in that field (color grading, video editing, legal, tax, finance, design, an unfamiliar codebase, etc.). Do NOT use for simple factual questions, domains you already know, or directly-actionable work — answer those directly or route to planner / architect.
last_updated: 2026-07-08
---

# blind-spot-pass — surface your unknown unknowns before you start
# (착수 전 나의 맹점 발굴 + 사전 학습)

> **Analogy.** Before asking for directions in an unfamiliar city, a good local guide first tells you "what to watch out for here, what's worth seeing, the words people use." Only then do you know what to ask. This skill gives you that "local briefing" right before you hand off work in a domain you don't know well.
>
> **비유.** 낯선 도시에서 길을 묻기 전에, 현지 가이드가 먼저 "이 동네에서 조심할 것, 꼭 봐야 할 것, 여기 사람들이 쓰는 말"을 짚어준다. 그러면 이제 무엇을 물어야 할지 스스로 알게 된다. 이 스킬은 낯선 분야의 작업을 맡기기 직전, 그 "현지 브리핑"을 해주는 역할이다.

## Why it matters (왜 필요한가)

Since Fable-class models, the bottleneck on output quality is no longer model capability — it's **how well you surface what you don't know**. When you hand off work in an unfamiliar domain, you *don't even know what to ask* (unknown unknowns). Prompt too vaguely and the model silently applies some industry default; prompt too specifically and it follows your wrong turn off a cliff. This skill drains that blind spot **before real work starts**, because discovering it mid-build is expensive to undo (cost asymmetry / shift-left).

한글: Fable 이후 결과물 품질의 병목은 모델 성능이 아니라 **"내가 무엇을 모르는지"를 얼마나 짚어내느냐**다. 낯선 분야를 맡길 때는 무엇을 물어야 할지조차 모르는 상태(unknown unknowns)라, 너무 막연하면 모델이 업계 표준을 임의로 갖다 쓰고, 너무 구체적이면 틀린 방향도 고집한다. 이 스킬은 **착수 전에** 사각지대를 값싸게 드러낸다 — 구현 중에 발견하면 되돌리기 비싸기 때문이다.

The real deliverable is not a "list of questions" — it's a **method that surfaces blind spots and teaches the minimum**. If it degrades into "let me ask you some questions", it just duplicates `planner`. Don't let it. (진짜 산출물은 질문 목록이 아니라 *사각지대를 드러내고 최소한만 가르치는 방법*이다.)

## The three kinds of unknowns (세 가지 불확실성)

| Kind | What it is | Handled by |
|------|-----------|-----------|
| Known knowns | what you wrote in the prompt (프롬프트에 적은 것) | just instruct |
| Known unknowns | undecided, but you know you don't know (모른다는 건 아는 미결정) | `planner` interview / `/plan` |
| Unknown knowns | so obvious you didn't say it — tacit taste, "I know it when I see it" (너무 당연해 안 적은 암묵지) | `/explore` references · lightweight prototype |
| **Unknown unknowns** | never even considered — an unfamiliar domain (아예 고려조차 못 한 것) | **this skill** |

See `rules/unknowns-lens.md` for the full 4-quadrant lens and routing. (짝 룰: 4사분면 렌즈 + 라우팅.)

## When it triggers (언제 호출되는가)

- "blind spot pass", "unknown unknowns", "find my unknowns"
- "I don't know what to ask", "I'm new to this field", "teach me before we start (so I can prompt well)"
- 한글: "내가 뭘 모르는지 알려줘", "이 분야 처음인데 뭘 물어야 할지 모르겠어", "먼저 가르쳐줘", "블라인드 스팟"
- When you hand off unfamiliar-domain work **while admitting you're a non-expert** (e.g. "I don't really know color grading, but fix the tone of this video").

## When NOT — route elsewhere (경계 — 오발동 방지)

| Situation | Right path |
|-----------|-----------|
| Simple factual question (단순 사실 질문) | Answer directly |
| A domain you already know (이미 아는 분야) | Start the work |
| "Which approach is better?" divergence (발산·옵션 비교) | brainstorm (`/explore`, or `superpowers:brainstorming` if installed) |
| Requirements clear, need an implementation plan (구현 계획) | `planner` / `/plan` |
| System design / architecture trade-offs (아키텍처 판단) | `architect` |
| Building a curriculum to teach *others* (남 가르칠 교안) | out of scope |

Core test: if it's **filling your own knowledge blind spot before you prompt**, use this skill; otherwise route up. No unfamiliar-domain signal → don't fire. (핵심 구분: *본인의 지식 사각지대를 메우는 사전 학습*이면 이 스킬, 그 외는 위로 라우팅.)

## Workflow (워크플로우)

### Phase 1 — Calibrate (출발점 파악)

What to teach depends on what you *already* know. Use `AskUserQuestion` to check only what's needed:

- How much do you know here? (first time / picked up bits / know the concepts)
- What do you ultimately want out of this? (one line)
- (optional) Any reference or "something like this" example?

Fewer questions if the answers are already clear. The goal is calibrating the teaching level, not interrogation. (심문이 아니라 가르칠 눈높이 맞추기.)

### Phase 2 — Ground (근거 확보, optional)

If the field is technical or needs current facts, delegate to `/explore` (for the local codebase) or a web/research pass to lock down correct vocabulary, standards, and pitfalls. Skip for common-knowledge domains.

### Phase 3 — Write the Blind Spot Map (핵심 산출물)

Produce the map in the template below. Apply the teaching-style rules — analogy first, conclusion first, gloss hard terms on first use.

### Phase 4 — Hand off (핸드오프)

- **Show an improved prompt** → "now instruct it like this" and start the real work.
- More divergence → brainstorm; implementation plan → `planner` / `/plan`; code references → `/explore`; parallel work → `/orchestrate`.
- This skill **teaches and hands off — it is not a gate.** If the user says "skip it, just do it", proceed immediately. (가르치고 넘겨줄 뿐, 승인 관문이 아니다. "바로 해"에 즉시 양보.)

### Show, don't tell — for unknown knowns (보고 반응 — 암묵지 끌어내기)

Some standards are tacit ("I know it when I see it"): document tone, screen layout, data shape. Don't ask about these in words — **make a cheap throwaway artifact and let the user react**: a one-page outline, a sample line of output, mock data, a straw-man in pseudocode, or (for UI) a quick mockup. Provide real source/reference instead of a description. Keep it a *throwaway* — never let this grow into starting the actual build (that would betray shift-left). (말론 애매한 취향은 버리는 견본을 만들어 "보고 반응"으로 끌어낸다.)

### Auto-surfacing (선택 — 룰 기반 자동)

The paired always-on rule `rules/unknowns-lens.md` names this skill as the **first move for unfamiliar-domain work**, so it can surface automatically without a manual call. It's a nudge, not a hard gate. (짝 룰이 낯선 도메인 작업의 첫 수로 이 스킬을 지정 — 강제가 아닌 권장.)

## Output — Blind Spot Map template (산출물 형식)

```
# [Domain] Blind Spot Map  ([분야] 블라인드 스팟 맵)

## Bottom line first — what you must know for this task
   (결론 먼저 — 이 작업에서 꼭 아셔야 할 것. 한두 문장. 비유 하나면 더 좋음.)

## Minimum vocabulary — only what you need  (이 분야 최소 어휘)
| Term | Plain meaning (쉬운 풀이) |
|------|--------------------------|

## The 3–5 decisions that actually matter   ← the heart of the blind spot
   (진짜 갈리는 결정 3~5개 — 여기가 사각지대의 핵심)
1. [Decision] — option A vs B, what's good/bad about each (trade-off)
   → In your situation, usually: ...

## Common traps / how this goes wrong  (흔한 함정 / 이렇게 하면 망한다)
- ...

## What "good" looks like  ("좋은 결과"는 어떻게 생겼나)
- (Criteria / examples, so you can judge the result yourself.)

## → Now prompt it like this  (→ 이제 이렇게 프롬프트하시면 됩니다)
"(a ready-to-use, improved instruction that reflects the blind spots)"
```

Three decisions or fewer → only that many. **Don't write a textbook** — teach only enough to *prompt and judge*. (교과서를 쓰지 말 것 — 프롬프트하고 판단할 만큼만.)

## Teaching style (CRITICAL)

- **Analogy first**: a sentence or two of analogy before the technical explanation. (비유 먼저)
- **Conclusion first**: the first line of each section is the point. (결론 먼저)
- **Gloss hard terms on first use**: "color grading (adjusting a video's color/contrast toward an intended mood)". Assume a non-expert reader. (어려운 용어는 첫 등장 시 괄호 풀이 — 독자는 비전문가다.)
- Don't stack dense tables/acronyms. Understanding over density.

## Never do (절대 하지 말 것)

- ❌ Degrade into a generic "let me ask you questions" wrapper — that duplicates `planner`. This skill's whole justification is *blind-spot surfacing + right-level teaching*.
- ❌ Fire on a domain the user already knows — unfamiliar-domain signal only.
- ❌ Turn teaching into a *gate* — it's pre-learning, not an approval checkpoint. Yield to "just do it".
- ❌ Textbook-length essays — only the minimum needed to prompt and judge.

## Related

- `rules/unknowns-lens.md` — the 4-quadrant unknowns lens + cost-asymmetry rule (names this skill as the first move for unfamiliar domains).
- `rules/interaction.md` — extends "state your assumptions before coding" from *the model's* assumptions to *your own* knowledge.
- `planner` · `architect` · `/explore` · `/plan` · `/orchestrate` — Phase 4 routing targets.
- Source: Anthropic — "A field guide to Claude Fable 5: Finding your unknowns" (Thariq Shihipar, 2026).
