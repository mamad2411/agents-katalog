<!--
  [편집 가능 영역] 여기부터 마지막 --- 직전까지
  [자동 생성 영역] 마지막 --- 이후 (meta server가 인덱스 생성)

  주의:
  - --- 이후에 직접 작성하면 덮어씌워집니다.
  - ## Specs Index, ## Stages Index, ## Decisions Index 헤딩을 --- 위에 사용하지 마세요.
-->

# CLAUDE.md

## 메타 작업 트리거

| 키워드 | 진입점 | 작업 |
|--------|--------|------|
| "수신함 검토해줘" | `_meta/inbox.md` | inbox 내용 확인 → 적절한 문서에 반영 |
| "정리하자" / "기록해" | `_meta/GUIDE.md` | devlog 작성 또는 문서 정리 |
| "결정사항으로 남겨" | `_meta/GUIDE.md` | `decisions/`에 기록 |
| "플랜 업데이트" | `_meta/plan.md` | 계획 수정 |
| "지금 어디야?" | `_meta/plan.md` | 현재 stage 상태 확인 |
| "어디까지 했지?" | `_meta/devlog/` | 최신 devlog 2-3개 + `plan.md` + 현재 stage 확인 |
| "[주제]를 쉽게 설명하는 문서 만들어줘" | `_meta/explainers/__template__.md` | 개념/기술 설명 문서 작성 (친근하게) |
| "트러블슈팅 기록 남겨" | `_meta/troubleshooting/__template__.md` | 문제 해결 과정 기록 (간결하게) |

**흐름:** 트리거 감지 → 진입점 파일 읽기 → `_meta/GUIDE.md` 규칙대로 처리 → 결과 보고

---
