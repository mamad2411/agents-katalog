---
name: 3ai-plan
description: |
  Claude, Gemini CLI, Codex CLI 3개 AI가 각자의 강점으로 플랜을 검토하고 종합하여 더 구체적이고 실행 가능한 작업 계획서를 작성합니다.
  "3AI 플랜", "3AI 협업", "멀티 AI 리뷰", "Gemini+Codex 검토" 요청에 트리거됩니다.
  복잡한 설계나 중요한 아키텍처 결정을 앞두고 있다면, 단일 AI보다 3개 AI의 교차 검토가 더 신뢰할 수 있는 결과를 만듭니다.
---

# 3-AI 협업 플랜 생성

## 개요

Claude, Gemini CLI, Codex CLI 3개 AI가 각자의 강점으로 플랜을 검토하고 종합하여
더 구체적이고 실행 가능한 작업 계획서를 작성한다.

## 왜 3-AI 협업인가?

단일 AI는 자신의 편향을 발견하기 어렵습니다. Claude는 맥락과 규칙 준수에 강하고, Gemini는 사용자 관점과 리스크 감지에 뛰어나며, Codex는 코드베이스 탐색과 기술적 정확성에 특화되어 있습니다.
세 AI의 교차 검토를 거치면 각자의 사각지대를 보완하여 실행 가능성이 높은 플랜이 나옵니다.

## AI 역할 분담

| AI | 역할 | 강점 |
|----|------|------|
| **Claude** | 종합 설계, 맥락 이해, 최종 판단 | 긴 컨텍스트, 프로젝트 규칙 준수 |
| **Gemini** | 표현/톤, 리스크 분석, 창의적 대안 | 자연어 품질, 사용자 관점 |
| **Codex** | 기술 정확성, 구조 분석, 검증 전략 | 코드베이스 탐색, 자동화 |

## 사용법

### Step 1: 컨텍스트 수집

프로젝트 현황을 파악한다:
- 현재 디렉토리/파일 구조 (`ls -R`)
- 핵심 파일 내용 읽기
- 기존 플랜이 있으면 읽기 (.claude/docs/req.md, .claude/docs/WORK-SPEC.html 등)
- 확인된 문제점 정리

### Step 2: Gemini + Codex 병렬 실행

두 AI에게 동일한 컨텍스트 + 각자 역할에 맞는 프롬프트를 전달한다.
**반드시 병렬로 실행**하여 시간을 절약한다.

> ⏱️ **Timeout 정책 (필수)**:
> - **Bash 호출** (`gemini -p`, `codex exec -`): **Bash 도구 `timeout: 240000` (4분) 필수 명시 + `2>&1 \|\| echo "FAIL"` 패턴**
> - **Codex Plugin Skill 사용 금지** (`/codex:rescue` 등): Bash timeout 미적용으로 무기한 hang 위험. 반드시 `codex exec -` (Bash CLI)만 사용
> - **3ai-plan은 가장 비싼 호출**이므로 timeout이 특히 중요. 어느 한 AI라도 hung되면 즉시 중단하고 나머지 결과로 진행
> - 상세: CLAUDE.md "Codex 협업" 섹션 참조

```bash
# Gemini: 표현/리스크/사용자 관점
# ⚠️ Bash 도구 호출 시 timeout: 240000 명시 필수
cat << 'EOF' | gemini -p - 2>&1 || echo "GEMINI_FAIL"
{컨텍스트 + 현황 + 기존 플랜}

다음 관점에서 플랜을 검토하고 개선안을 제시해주세요:
1. 사용자/운영 관점에서 빠진 고려사항
2. 리스크 관리 및 롤백 전략
3. 실행 순서와 의존성 최적화
4. 표현/네이밍/구조의 일관성

[현재 → 문제 → 개선 제안 → 구체적 실행 방안] 형식으로 답변.
한국어로 답변해주세요.
EOF
```

**Codex: 기술 정확성/구조/검증 (Bash CLI 단독 사용, Plugin Skill 금지)**

```bash
# ⚠️ Bash 도구 호출 시 반드시 timeout: 240000 (4분) 명시
# ⚠️ Plugin Skill (/codex:rescue 등)은 사용 금지 — hang 위험
cat << 'EOF' > /tmp/codex_prompt.txt
{컨텍스트 + 현황 + 기존 플랜}

기술적/구조적 관점에서 플랜을 검토하고 개선안을 제시해주세요:
1. 데이터 무결성과 검증 전략
2. 자동화 가능 구간 식별
3. 단계별 의존성과 최적 실행 순서
4. 기술적 정확성과 Trade-off

[현재 → 문제 → 개선 제안] 형식으로 답변.
한국어로 답변해주세요.
EOF
cat /tmp/codex_prompt.txt | codex exec - --full-auto 2>&1 || echo "CODEX_FAIL"
```

**Gemini CLI 문법**: `cat << 'EOF' | gemini -p -` 또는 `gemini -p "프롬프트"`
**Codex CLI 문법**: `cat file | codex exec - --full-auto` (Bash CLI 단독, Plugin Skill 금지)
**필수**: Bash 도구 호출 시 `timeout: 240000` 명시. `*_FAIL` 검출 시 즉시 다음 단계 진행.

### Step 3: Claude 종합

두 AI의 결과를 분석하고 종합한다:

1. **공통 지적사항** 추출 (3개 AI 모두 동의하는 점)
2. **AI별 고유 제안** 분류
3. **충돌하는 제안** 비교 후 최적안 선택
4. **종합 비교표** 작성

```markdown
| 관점 | Gemini | Codex | Claude (종합) |
|------|--------|-------|---------------|
| 항목1 | 제안A | 제안B | 최종 결정 + 근거 |
```

### Step 4: 최종 플랜 작성

종합 결과를 반영하여 플랜 문서를 작성한다.

**필수 포함 섹션:**
- 현황 분석 (3-AI 공통 진단)
- Phase별 작업 + 목표 + 검증
- 파일 변경 목록
- 리스크 관리
- 실행 순서 요약

**플랜 헤더 형식:**
```markdown
# {제목} (v{버전} - 3-AI 협업 검토 반영)
> **검토 AI**: Claude (종합) + Gemini (표현/리스크) + Codex (구조/검증)
> **최종 업데이트**: {날짜}
```

## 입출력

| 입력 | 출력 |
|------|------|
| 기존 플랜 또는 요구사항 | 3-AI 종합 플랜 (.claude/docs/req.md 또는 .claude/docs/WORK-SPEC.html) |
| 프로젝트 현황 | AI별 비교표 (종합 근거) |

## 체크리스트

- [ ] Gemini CLI 실행 완료
- [ ] Codex CLI 실행 완료
- [ ] 3-AI 공통 지적사항 추출
- [ ] AI별 고유 제안 분류
- [ ] 충돌 제안 비교/결정
- [ ] 종합 비교표 작성
- [ ] 최종 플랜에 Phase별 검증 포함
- [ ] 리스크 관리 섹션 포함

## 관련 스킬

- `/work-plan`: req.md 기반 WORK-SPEC.html 작성 (단일 AI)
- `/sync-check`: 동기화 상태 검증
