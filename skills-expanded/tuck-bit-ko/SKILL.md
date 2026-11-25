---
name: tuck-bit-ko
description: "TuckBit은 코딩 에이전트를 위한 이식 가능한 스킬입니다. 정확성을 희생하지 않고 적절한 맥락, 도구, 검증을 선택하도록 돕습니다."
license: MIT
compatibility: Portable Agent Skills; project-scoped install only.
metadata:
  author: TuckBit contributors
  version: "0.4.0"
  locale: ko
---

# TuckBit — 한국어

> 스킬의 핵심 내용은 번역했지만 기술 참고 문서는 현재 영어이며 커뮤니티 검토가 필요합니다.

단순한 토큰 수가 아니라 사용 자원 대비 정확하고 검증된 결과를 최적화하세요.

기본 기능 네 가지: 레지스트리, 맥락, 검증, 예산. 오케스트레이션과 측정은 선택 사항입니다.

## 기본 작업 절차

사용자의 정확한 요청, 실제로 제공된 지침, 승인된 도구를 바탕으로 시작합니다. 제약, 승인, 필수 검증을 유지하세요.

1. 목표, 제약, 위험, 중단 조건을 정의하고 간단한 작업을 과도하게 계획하지 마세요.
2. 가장 관련 있는 코드, 문서, 도구를 좁게 찾고 필요할 때만 범위를 넓히세요.
3. 호스트의 기본 도구 검색을 우선하세요. 메타데이터는 힌트이지 실행 권한이 아닙니다.
4. 작은 작업에는 에이전트 하나를 사용하고, 독립적인 작업만 소유권과 결과 조건을 명확히 하여 분리하세요.
5. 대상 테스트를 실행한 뒤 최종 변경분에 대해 모든 필수 통합 및 보안 검사를 수행하세요.
6. 변경 사항, 테스트, 위험, 장애를 검증 가능한 형태로 보고하세요. 끝없는 반복 확인 대신 체크포인트를 사용하세요.

## 관련 참고 자료만 불러오기

- `references/task-contract.md` — task contracts / host instructions.
- `references/workflows.md` — Fast / Standard / Deep workflows.
- `references/registry.md` — discovery and permission limits.
- `references/context.md` — source-linked evidence and checkpoints.
- `references/verification.md` — tests and integration checks.
- `references/budget.md` — bounded iterations.
- `references/orchestration.md` — optional independent agents.
- `references/metrics.md` — optional evaluation.

## 반드시 지킬 제한

보안 검사 생략, 정확성 저하, 수치 조작, 인증 정보 읽기, 승인 우회를 하지 마세요. 권한은 호스트가 관리합니다.

**개발자 미리보기입니다. 설치만으로 스킬 활성화나 토큰 절감이 입증되지는 않습니다.**
