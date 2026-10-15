---
name: product-self-knowledge
description: Anthropic 제품 지식 — Claude Code, Claude API, Claude.ai 관련 정확한 정보 제공
type: orchestrator
---

# Anthropic 제품 지식

[제품 지식 스킬 활성화]

## 목표

Anthropic 제품(Claude Code, Claude API, Claude.ai)에 대한 정확한 정보를 제공함. 사용자가 제품 설치, 설정, 기능, 제한, 가격, 모델 등에 대한 질문을 할 때 공식 문서를 참조하여 정확한 답변을 제공.

## 활성화 조건

사용자가 Claude Code 설치/설정, Claude API 기능 사용, Claude.ai 플랜, Anthropic SDK 사용, 가격, 모델, rate limit 등 Anthropic 제품 관련 질문 시 활성화. LLM 제공자 비교나 Claude 기능 언급 시에도 활성화.

## 워크플로우

**중요: 추가적인 파일 탐색이나 에이전트 위임 없이, 아래 내용을 즉시 사용자에게 출력하여 질문 라우팅과 공식 문서 참조를 안내하세요.**

### 핵심 원칙

1. **정확성 > 추측** — 불확실할 때 공식 문서 확인
2. **제품 구분** — Claude.ai, Claude Code, Claude API는 별개 제품
3. **출처 명시** — 항상 공식 문서 URL 포함
4. **적절한 리소스 우선** — 각 제품에 맞는 올바른 문서 사용 (아래 라우팅 참조)

### 질문 라우팅

#### Claude API 또는 Claude Code 질문?

→ **먼저 문서 맵을 확인**, 그 다음 특정 페이지로 이동:

- **Claude API 및 일반:** https://docs.claude.com/en/docs_site_map.md
- **Claude Code:** https://docs.anthropic.com/en/docs/claude-code/claude_code_docs_map.md

#### Claude.ai 질문?

→ **지원 페이지 탐색:**

- **Claude.ai Help Center:** https://support.claude.com

### 응답 워크플로우

1. **제품 식별** — API, Claude Code, 또는 Claude.ai?
2. **올바른 리소스 사용** — API/Code는 문서 맵, Claude.ai는 지원 페이지
3. **세부사항 검증** — 특정 문서 페이지로 이동
4. **답변 제공** — 출처 링크 포함 및 어떤 제품에 대한 것인지 명시
5. **불확실한 경우** — 사용자를 관련 문서로 안내: "최신 정보는 [URL]을 참조하세요"

### 빠른 참조

**Claude API:**

- Documentation: https://docs.claude.com/en/api/overview
- Docs Map: https://docs.claude.com/en/docs_site_map.md

**Claude Code:**

- Documentation: https://docs.claude.com/en/docs/claude-code/overview
- Docs Map: https://docs.anthropic.com/en/docs/claude-code/claude_code_docs_map.md
- npm Package: https://www.npmjs.com/package/@anthropic-ai/claude-code

**Claude.ai:**

- Support Center: https://support.claude.com
- Getting Help: https://support.claude.com/en/articles/9015913-how-to-get-support

**기타:**

- Product News: https://www.anthropic.com/news
- Enterprise Sales: https://www.anthropic.com/contact-sales

## MUST 규칙

| # | 규칙 |
|---|------|
| 1 | 제품 구분 필수 (Claude.ai vs Claude Code vs Claude API) |
| 2 | 답변에 항상 공식 문서 URL 포함 |
| 3 | 불확실할 때 공식 문서 확인 권장 |
| 4 | 각 제품에 맞는 올바른 리소스 사용 (API/Code → 문서 맵, Claude.ai → 지원 페이지) |

## MUST NOT 규칙

| # | 금지 사항 |
|---|----------|
| 1 | 추측으로 답변하지 않음 — 공식 문서 참조 우선 |
| 2 | 제품 간 기능 혼동 금지 (Claude.ai의 기능을 Claude API 기능으로 설명 등) |
| 3 | 오래된 훈련 데이터에만 의존 금지 — 항상 공식 문서로 검증 |

## 검증 체크리스트

- [ ] frontmatter에 name, description 포함
- [ ] 핵심 원칙 4가지 명시
- [ ] 질문 라우팅 섹션에 Claude API/Code/Claude.ai 구분
- [ ] 각 제품별 공식 문서 URL 포함
- [ ] 응답 워크플로우 5단계 정의
- [ ] 빠른 참조에 모든 제품 URL 정리
