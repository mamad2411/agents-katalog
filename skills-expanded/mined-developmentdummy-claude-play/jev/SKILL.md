---
name: jev
description: Use when a decision needs fast, cheap, typed judgment instead of generated text — picking one action/option from a known set, rating something on ordered levels, or a yes/no gate — via Jev (TypeSafe System One). Covers the three call paths in ClaudePlay (MCP jev_ask, persona tool context.jev, panel/app __panelBridge.jev), question design rules, and how to use probabilities/confidence. Do not use when the output must be prose, dialogue, or creative text — that stays with the LLM.
---

# Jev — 빠른 판단 모델 (TypeSafe System One)

Jev는 글을 쓰지 않는다. `state`(판단 재료)와 **타입 있는 질문**을 받아 **확률이 붙은 답**을 돌려준다.
실측 약 0.2초, 요청당 수백 토큰(입력 백만 토큰당 $0.042, 출력 무료). LLM 턴을 쓰기엔 아까운 "지금 뭘 고를까" 판단에 쓴다.

**역할 분담**: Jev = 고르기·점수·예/아니오. LLM = 대사·서술·기억 정리. 대사를 Jev에게 시키지 마라.

## 세 가지 호출 경로

| 어디서 | 어떻게 |
|---|---|
| 세션/빌더 AI (지금 이 대화) | MCP `jev_ask({ state, questions, model? })` |
| 페르소나 도구 `tools/*.js` | `const r = await context.jev(state, questions)` |
| 패널·앱 화면 JS | `const r = await __panelBridge.jev(state, questions)` |

키는 서버에만 있다. 세 경로 모두 `/api/jev` → `src/lib/jev-client.ts` 하나를 거친다.

⚠️ **월드 엔진 `step()` 안에서 부르지 마라.** step은 200ms마다 도는 월드 시계다. 네트워크 왕복이 시계를 멈춘다.
판단은 step 밖(전용 액션, 스레드, 패널)에서 하고, 결과는 `submit` 의도로 넣어라.

## 질문 세 종류

```jsonc
{
  "state": { "actor": { "name": "Elena", "hunger": "high", "time_of_day": "evening" }, "nearby": ["campfire", "river"] },
  "questions": {
    // 하나 고르기 → choice + probabilities + confidence
    "next_action": {
      "type": "choice",
      "instructions": "What would `actor` most plausibly do next?",
      "criteria": {
        "eat": "Go eat at the campfire. Fits when hunger is high.",
        "fish": "Fish at the river. Fits when food stores are low and she is not exhausted.",
        "continue": "Keep doing the current activity. Fits when nothing pressing has changed."
      }
    },
    // 순서 있는 단계 위 위치 → score + confidence
    "mood": {
      "type": "score",
      "instructions": "How content is `actor` right now?",
      "criteria": ["Miserable: hungry, tired, and lonely", "Uneasy: one need unmet", "Content: needs met", "Delighted: needs met and something good just happened"]
    },
    // 예/아니오 확률 → noul (0~1)
    "wants_company": {
      "type": "noul",
      "instructions": "Would `actor` rather be with someone than alone right now?"
    }
  }
}
```

응답: `answers.next_action.choice`, `.probabilities`, `.confidence` / `answers.mood.score` / `answers.wants_company.noul`.

## 질문 설계 규칙 (정확도를 좌우한다)

1. **영어로 쓴다.** instructions와 criteria 모두. Jev는 영어가 주 학습 언어다. state의 고유명사·한국어 원문은 그대로 둬도 되지만, 판단 기준은 영어로.
2. **숫자는 코드에서 말로 바꿔 넘긴다.** `hunger: 72` ❌ → `hunger: "high"` ✅. Jev는 계산·비교·개수 세기를 못 한다. 시간 비교도 코드에서.
3. **모든 선택지에 "언제 맞는지" 기준을 쓴다.** Jev는 글자 그대로 읽는다. 뜻한 조건을 문장으로 명시하라. 틀린 답을 보고 "내 말은 ~였는데"라는 생각이 들면, 그 설명이 빠진 기준이다.
4. **"해당 없음 / 계속" 선택지를 넣는다.** 억지로 바꾸게 만들지 마라.
5. **한 질문엔 한 판단.** 독립적인 판단 여러 개는 **같은 state로 한 요청에 묶는다**(병렬 평가, 훨씬 싸고 빠름). 서로 답을 못 본다.
6. **state는 필요한 것만.** 관련 없는 큰 JSON은 정확도를 떨어뜨린다. 판단 대상의 주변 맥락만 추려라.
7. **state 필드는 백틱으로 가리킨다.** `` `actor.memory` ``처럼.

## 답을 쓰는 법

- **confidence는 "확신의 집중도"**다. 행동 권한이 아니다. 해롭지 않은 선호 선택이면 낮아도 쓸 수 있다.
- **다양성이 필요하면 probabilities로 샘플링하라.** 여러 캐릭터가 늘 같은 "정답"만 고르면 기계적으로 보인다. 확률 분포에서 뽑거나, `recent_actions`를 state에 넣고 "반복을 피하라"를 기준에 적어라.
- **noul 0.5 근처 = 예/아니오가 비슷**하다는 뜻이지 "중간 정도"가 아니다.
- 임계값은 실제 결과를 보며 정하라. 문서의 예시 수치는 출발점일 뿐이다.

## 실패 처리

에러 응답 상태: 400(질문 형식 — 메시지대로 고쳐라), 503(키 미설정), 429(요청 과다, 이미 재시도됨), 504(타임아웃).
Jev가 실패하면 **기존 규칙 기반 기본값으로 계속 진행**하라. Jev를 게임·세션이 멈추는 단일 실패점으로 만들지 마라.

## 참고

- 공식 문서: https://docs.typesafe.ai/llms.txt (Choice/Score/Noul, Confidence, Patterns)
- 코어 설계: `docs/specs/2026-10-01-jev-core-design.md`
