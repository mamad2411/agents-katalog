---
name: english-study
description: "Generate a daily advanced English connected-speech study note covering natural American speech, reductions, slang, and accents, saved to ~/obsidian-vault/english-study/YYYY-MM-DD.md. Use when the user asks for English listening practice, connected speech, or an english-study note."
---

# English Connected Speech Study Skill

매일 아침 30분 학습용 — 실전 상황에서의 연음, 축약, 슬랭, 사투리를 분석하는 영어 학습 노트를 생성한다.

## Invocation

- Claude Code: `/english-study`
- Codex: `$english-study`

## Instructions

### 대상

미국에서 생활하는 AI/ML 개발자. Tech college 5년 다녀서 유창하지만, 빠른 속도의 자연스러운 영어에서 connected speech, 슬랭, 사투리 때문에 이해가 어려운 부분을 집중 학습한다. 교과서적 영어가 아닌 **실제로 들리는 영어** 기준.

### 상황 선택

1. 사용자가 상황/맥락을 지정하면 (`/english-study "게임하면서 팀원과 voice chat"` in Claude Code, `$english-study "게임하면서 팀원과 voice chat"` in Codex) 그 상황을 사용
2. 지정하지 않으면 아래 예시 중 하나를 랜덤 선택 (매번 다른 상황):

   **직장 / Tech 업계:**
   - Tech standup에서 빠르게 말하는 동료
   - 회사 점심시간 잡담 (동료들과 cafeteria에서)
   - Sprint retro에서 팀원들이 불만 쏟아내는 상황
   - 1:1 미팅에서 매니저와 솔직한 피드백 주고받기
   - Tech conference 네트워킹 — 처음 만난 사람과 small talk
   - Slack huddle에서 빠르게 디버깅하는 대화
   - 온콜 장애 대응 — 새벽에 급하게 통화
   - 면접관끼리 candidate debrief하는 대화
   - Happy hour에서 동료들과 회사 뒷담화
   - 퇴사하는 동료 farewell에서 나누는 대화
   - PR review 하면서 화면 공유하며 나누는 대화

   **미국 일상생활:**
   - 부동산 에이전트와 집 보러 다니기
   - 의사 진료실에서 증상 설명하고 질문하기
   - 공항에서 비행기 놓칠 뻔한 상황
   - DMV에서 면허 갱신하면서 직원과 대화
   - 자동차 정비소에서 mechanic이 문제 설명
   - 은행에서 mortgage/계좌 관련 상담
   - Home Depot 직원에게 DIY 프로젝트 질문
   - 이웃과 fence/noise 문제로 대화
   - 보험회사 고객센터와 전화 통화
   - Costco 계산대에서 캐셔와 짧은 잡담
   - 아파트 관리사무소에 maintenance 요청

   **사교 / 취미:**
   - Bar에서 친구들과 수다
   - 스포츠 경기 보면서 흥분한 대화
   - 게임하면서 팀원과 voice chat
   - BBQ 파티에서 친구 소개받는 상황
   - 헬스장에서 옆 사람과 짧은 대화
   - Meetup/동호회에서 새로운 사람과 대화
   - 캠핑/하이킹 중 trail에서 만난 사람과 대화

   **다양한 억양 / 사투리:**
   - 남부 사투리 할머니와 대화
   - 뉴욕 택시 기사와 대화
   - 보스턴 출신 동료와 대화
   - 시카고 출신 uber 기사와 대화
   - 건설 현장에서 작업 지시
   - 경찰이 교통 위반 단속할 때
   - 스탠드업 코미디 공연
   - 패스트푸드 드라이브스루 주문

### 콘텐츠 생성

선택된 상황에 대해 다음을 생성:

1. **Dialogue**: 해당 상황에서 벌어질 법한 자연스러운 네이티브 대화. 빠르게 말하는 기준으로, 축약/슬랭/연음을 그대로 반영. 발음이 변하는 부분은 **bold** 처리.
2. **Breakdown**: 대화에서 나온 모든 connected speech, 슬랭, 사투리를 하나씩 분석. 가능하면 IPA 표기 포함.
3. **More Examples**: 오늘 배운 패턴이 들어간 추가 문장 5-8개. 각각 자연스러운 버전 → 풀어쓴 버전 → 한국어 의미.
4. **오늘의 한 줄**: 가장 기억할 만한 인사이트 한 줄 (한국어).

### 출력 포맷

`~/obsidian-vault/english-study/YYYY-MM-DD.md`에 저장:

```markdown
---
tags:
  - english-study
date: YYYY-MM-DD
situation: "{상황 한 줄 설명}"
---

# {Situation Title}

## Scene
<!-- 상황 설명 (한국어). 누가, 어디서, 어떤 맥락인지. -->

## Dialogue
<!-- 자연스러운 네이티브 대화. 빠른 말투, 축약, 슬랭 그대로 반영. -->
<!-- 발음이 변하는 부분은 bold 처리. -->
<!-- 예: "I **shoulda** told **'em** we **weren't gonna** make it." -->

## Breakdown
<!-- 대화에서 나온 모든 connected speech / 슬랭 / 사투리 분석 -->
<!-- 각 항목: -->
<!-- - **shoulda** → should have — /ʃʊdə/ — 과거 후회 표현 -->
<!-- - **'em** → them — 빠른 발화에서 th 탈락 -->
<!-- 가능하면 IPA 표기 포함 -->

## More Examples
<!-- 오늘 배운 패턴이 들어간 추가 문장 5-8개 -->
<!-- 각 문장: 자연스러운 버전 → 풀어쓴 버전 → 한국어 의미 -->

## 오늘의 한 줄
<!-- 오늘 학습에서 가장 기억할 만한 인사이트 한 줄 (한국어) -->
```

### 중요 규칙

- 설명은 한국어, 대화/예문은 영어
- 수준은 높게 — 이미 유창한 사람 기준
- 교과서적 영어가 아닌 **실제로 들리는 영어** 중심
- 슬랭, 사투리, 세대별 표현 적극 포함
- `english-study/` 디렉토리 없으면 자동 생성
- 동일 날짜 파일 존재 시 사용자 확인
- 파일명의 `YYYY-MM-DD`는 오늘 날짜 사용
