---
name: llm-model-reference
description: >
  Use this skill whenever writing, reviewing, or suggesting code that calls
  Gemini API, OpenAI API, or Anthropic Claude API — including any model string,
  SDK initialization, or model selection decision. Also triggers when the user
  asks which model to use for Gemini, OpenAI, or Claude. Do NOT use this skill
  for general AI theory questions unrelated to API code.
tags: [gemini, openai, claude, anthropic, llm, api, model]
---

# LLM Model Reference — 2026.03 기준

> 이 SKILL의 목적: 코드에서 LLM 모델명을 사용할 때 outdated/deprecated 모델이
> 들어가지 않도록 현행 모델 기준을 강제한다.
>
> ⚠️ 중요 원칙: 훈련 데이터 기반으로 모델명을 추론하지 말 것.
> 아래 테이블에 없는 모델명은 절대 코드에 사용하거나 추천하지 말 것.

---

## Google Gemini

### ✅ 현행 사용 가능 모델 (2026.03)

| 용도 | 모델 문자열 | 비고 |
|------|------------|------|
| 최고 성능 / 복잡한 추론 | `gemini-3.1-pro-preview` | preview, GA 예정 |
| 고성능 균형 (agentic) | `gemini-3-flash-preview` | preview, GA 예정 |
| 경량 / 고볼륨 / 저비용 | `gemini-3.1-flash-lite-preview` | preview |
| custom tool 우선 agentic | `gemini-3.1-pro-preview-customtools` | 3.1-pro 변형 |

### ❌ 사용 금지 (deprecated / shutdown)

| 모델 | 상태 |
|------|------|
| `gemini-3-pro-preview` | **shutdown (2026.03.09)** — 사용 시 오류 |
| `gemini-2.5-flash-lite-preview-09-2025` | shutdown (2026.03.31) |
| `gemini-2.0-flash`, `gemini-2.0-flash-lite` | **shutdown 예정 2026.06.01** |
| `gemini-2.5-flash`, `gemini-2.5-pro` | **shutdown 예정 2026.06.17** |
| `gemini-1.5-*`, `gemini-1.0-*` | 이미 종료, 404 반환 |

### 주의사항

- `gemini-3.1-flash` (일반) 는 **미출시** — 코드에 사용 금지
- `gemini-3-flash` deprecated 예정이라는 주장은 **근거 없음** (2026.03 기준)
- 모든 Gemini 3 계열은 현재 preview 상태 (GA 미완료)
- thinking 제어: `thinking_budget` 대신 `thinking_level` 파라미터 사용 (LOW/MEDIUM/HIGH)

### 예시 코드 (Python)

> ⚠️ **패키지 주의**: `google-genai` 패키지 사용 (`import google.genai`)
> `google-generativeai` (`import google.generativeai`) 는 **구형/deprecated — 절대 사용 금지**

```python
# ✅ 반드시 이 import 사용 (pip install google-genai)
import google.genai as genai

client = genai.Client(api_key="YOUR_API_KEY")

# 일반 요청
response = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents="..."
)
print(response.text)

# 경량 고볼륨 작업
response = client.models.generate_content(
    model="gemini-3.1-flash-lite-preview",
    contents="..."
)

# thinking 제어 (3.x 계열)
from google.genai import types

response = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents="...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_budget=8192)
    )
)

# ❌ 사용 금지 — 아래 패턴은 구형 SDK (google-generativeai)
# import google.generativeai as genai          ← 금지
# genai.configure(api_key=...)                 ← 금지
# genai.GenerativeModel("gemini-...")          ← 금지
# model.generate_content(...)                  ← 금지 (client 패턴 사용할 것)

# ❌ 사용 금지 모델명
# client.models.generate_content(model="gemini-2.5-flash", ...)   # 6월 종료 예정
# client.models.generate_content(model="gemini-1.5-pro", ...)     # 이미 종료
```

---

## OpenAI

### ✅ 현행 사용 가능 모델 (2026.03)

| 용도 | 모델 문자열 | 비고 |
|------|------------|------|
| 최고 성능 flagship | `gpt-5.4` | 현재 최신 (snapshot: `gpt-5.4-2026-03-05`) |
| 고볼륨 / 저비용 | `gpt-5.4-mini` | snapshot: `gpt-5.4-mini-2026-03-17` |
| 초경량 단순 작업 | `gpt-5.4-nano` | compaction 지원, tool search 미지원 |
| agentic 코딩 특화 | `gpt-5.3-codex` | Codex + GPT-5 통합 모델 |
| 이전 세대 (여전히 유효) | `gpt-5.2` | deprecated 아님, 구세대 |

### ❌ 사용 금지

| 모델 | 상태 |
|------|------|
| `gpt-5.1` | ChatGPT에서 2026.03.11 종료 (API는 유지, 신규 사용 비권장) |
| `gpt-4o`, `gpt-4.1`, `gpt-4.5-preview` | deprecated 발표됨 |
| `gpt-4-*`, `gpt-3.5-*` | 구세대, 사용 금지 |

### 주의사항

- reasoning 제어: `reasoning_effort` 파라미터 — `"low"` / `"medium"` / `"high"` / `"xhigh"`
- `gpt-5.4`가 flagship; 신규 프로젝트는 `gpt-5.4` 또는 `gpt-5.4-mini`로 시작
- Responses API 권장 (Chat Completions API도 여전히 유효)

### 예시 코드 (Python)

```python
from openai import OpenAI

client = OpenAI()

# ✅ 현행 flagship
response = client.responses.create(
    model="gpt-5.4",
    input="...",
    reasoning={"effort": "high"}
)

# 고볼륨 경량 작업
response = client.responses.create(
    model="gpt-5.4-mini",
    input="..."
)

# ❌ 사용 금지
# model="gpt-4o"    # deprecated
# model="gpt-3.5-turbo"  # 구세대
```

---

## Anthropic Claude

### ✅ 현행 사용 가능 모델 (2026.03)

| 용도 | 모델 문자열 | 비고 |
|------|------------|------|
| 최고 성능 | `claude-opus-4-6` | 현재 최신 Opus |
| 일상 균형 (권장) | `claude-sonnet-4-6` | 성능/비용 균형 최적 |
| 경량 / 고속 | `claude-haiku-4-5-20251001` | 저비용 고속 |

### ❌ 사용 금지

| 모델 | 상태 |
|------|------|
| `claude-opus-4`, `claude-opus-4-1` | API에서 제거됨 (`4-6`으로 자동 마이그레이션) |
| `claude-3-5-sonnet-*`, `claude-3-*` | 구세대, 신규 사용 비권장 |
| `claude-2-*`, `claude-1-*` | 종료 |

### 주의사항

- Claude 4.6 패밀리: Opus 4.6 / Sonnet 4.6 / Haiku 4.5
- extended thinking: `thinking` 파라미터로 제어 (`budget_tokens` 설정)
- 1M 토큰 컨텍스트: Max/Team/Enterprise 플랜에서만 사용 가능

### 예시 코드 (Python)

```python
import anthropic

client = anthropic.Anthropic()

# ✅ 현행 모델
response = client.messages.create(
    model="claude-sonnet-4-6",  # 일반 권장
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}]
)

# 최고 성능 필요 시
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2048,
    messages=[{"role": "user", "content": "..."}]
)

# ❌ 사용 금지
# model="claude-3-5-sonnet-20241022"  # 구세대
```

---

## 모델 선택 가이드 (요약)

| 상황 | 추천 |
|------|------|
| 복잡한 추론, 고품질 우선 | `gemini-3.1-pro-preview` / `gpt-5.4` / `claude-opus-4-6` |
| 일반 개발, 균형 | `gemini-3-flash-preview` / `gpt-5.4-mini` / `claude-sonnet-4-6` |
| 고볼륨, 비용 민감 | `gemini-3.1-flash-lite-preview` / `gpt-5.4-nano` / `claude-haiku-4-5-20251001` |
| agentic 코딩 특화 | `gemini-3.1-pro-preview-customtools` / `gpt-5.3-codex` |

---

## 업데이트 주기

이 SKILL은 최소 월 1회 업데이트 권장.
공식 deprecation 확인 출처:
- Gemini: https://ai.google.dev/gemini-api/docs/deprecations
- OpenAI: https://platform.openai.com/docs/changelog
- Claude: https://docs.anthropic.com/en/docs/about-claude/models

> 마지막 업데이트: 2026.03.18
