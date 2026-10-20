# PR 템플릿

## PR 생성 시 사용할 템플릿

```markdown
## Summary

<!-- 변경 사항을 1-3개 bullet point로 요약 -->
-
-

## Type of Change

<!-- 해당하는 항목에 x 표시 -->
- [ ] feat: 새로운 기능
- [ ] fix: 버그 수정
- [ ] docs: 문서 변경
- [ ] refactor: 리팩토링
- [ ] test: 테스트 추가/수정
- [ ] chore: 기타 변경

## Breaking Change

<!-- Breaking change가 있다면 설명 -->
- [ ] Yes (하위 호환성 깨짐)
- [ ] No

<!-- Breaking change 상세 -->


## Related Documents

<!-- 관련 문서 링크 (자동 생성됨) -->
- PRD:
- Tech Spec:
- Progress:

## Related Issues

<!-- 관련 이슈 번호 -->
Closes #
Refs #

## Changes

### Added
-

### Changed
-

### Removed
-

## Test Plan

<!-- 테스트 방법 -->
- [ ] 단위 테스트 통과
- [ ] 통합 테스트 통과
- [ ] 수동 테스트 완료

### Test Commands
```bash
pytest tests/
```

## Checklist

<!-- 제출 전 확인 -->
- [ ] 코드가 프로젝트 스타일 가이드를 따름
- [ ] 셀프 리뷰 완료
- [ ] 주석 추가 (복잡한 로직)
- [ ] 문서 업데이트 (필요시)
- [ ] 테스트 추가/수정
- [ ] 모든 테스트 통과
- [ ] Breaking change 문서화 (해당시)

## Screenshots (Optional)

<!-- UI 변경이 있다면 스크린샷 첨부 -->

## Additional Notes

<!-- 리뷰어에게 전달할 추가 정보 -->


---
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## PR 제목 규칙

Conventional Commits 형식 사용:
```
<type>[optional scope]: <description>
```

### 예시
```
feat(auth): add OAuth2 login support
fix(api): handle null response gracefully
docs: update API documentation
refactor(db): optimize query performance
```

## PR 크기 가이드

| 크기 | 변경 라인 | 권장 |
|------|----------|------|
| XS | < 10 | ✅ 이상적 |
| S | 10-50 | ✅ 좋음 |
| M | 50-200 | ⚠️ 주의 |
| L | 200-500 | ⚠️ 분할 고려 |
| XL | > 500 | ❌ 분할 필요 |

## 리뷰어 지정 가이드

| 변경 영역 | 리뷰어 |
|----------|--------|
| API 변경 | Backend Lead |
| DB 스키마 | DBA |
| 보안 관련 | Security Team |
| UI 변경 | Frontend Lead |

## 자동 라벨링

| 변경 유형 | 라벨 |
|----------|------|
| Breaking Change | `breaking-change` |
| 긴급 수정 | `urgent` |
| 문서 변경 | `documentation` |
| 버그 수정 | `bug` |
| 새 기능 | `enhancement` |

## PR 설명 작성 팁

1. **왜(Why)** 이 변경이 필요한지 설명
2. **무엇(What)** 을 변경했는지 요약
3. **어떻게(How)** 테스트할 수 있는지 안내
4. **영향(Impact)** 범위 명시
