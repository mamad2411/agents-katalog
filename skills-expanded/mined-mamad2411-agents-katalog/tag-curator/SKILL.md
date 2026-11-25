---
name: tag-curator
description: 블로그 글에 태그를 달거나, 태그 카탈로그를 점검·보완할 때 사용. 사용자가 "태그 정리", "태그 점검", "이 글에 태그 달아줘" 등을 요청하거나 /tag-audit 실행 시 발동. 카탈로그 동기화(파일 편집)는 scripts/tag-sync.py가 hook으로 자동 처리하므로 Claude는 직접 _tags.md나 index.md를 스캔·편집하지 않음.
---

# Tag Curator

태그 카탈로그 파일 편집은 `scripts/tag-sync.py`가 hook으로 자동 처리한다.
Claude의 역할은 **글 frontmatter에 올바른 태그를 고르는 것**뿐이며, 카탈로그 동기화는 스크립트에 위임한다.

## 역할 분담

| 주체 | 역할 |
|------|------|
| Claude (이 스킬) | 글의 주제에 맞는 태그 선택·추가 (frontmatter 편집) |
| `tag-sync.py` (hook) | Claude가 .md 편집할 때마다 자동 실행 → `_tags.md` 갱신 + `index.md` 재생성 |

## 태그 선택 절차

1. **`blog/_tags.md` 읽기** — 카테고리별 태그 목록과 설명 확인
2. **본문 주제와 매칭** — 가장 구체적인 태그 우선 (예: `topic/fastapi` > `topic/python`)
3. **`type/*` 태그 1개 보장** — `type/note` (학습/트러블슈팅) / `type/log` (사건/경험) / `type/idea` (아이디어)
4. **글 frontmatter에 태그 작성** — 이 편집이 hook을 트리거해 카탈로그를 자동 동기화

## 신규 태그가 필요한 경우

기존 태그로 분류하기 어려우면:
1. `topic/<영문-소문자-하이픈>` 형식으로 frontmatter에 직접 기재
2. 파일 저장 시 `tag-sync.py`가 자동으로 `_tags.md` "기타" 섹션에 등록
3. **보완 필요**: 자동 등록된 태그에는 "(자동 등록 — 설명 보완 필요)" 표시가 붙음
   - `/tag-audit` 호출 시 또는 다음 유사 글 작업 시 카테고리·설명을 정리

## `/tag-audit` 실행 시

정합성 점검이 필요할 때:
```bash
python 'C:/Users/SSAFY/Documents/Obsidian Vault/scripts/tag-sync.py' --dry
```
를 실행해 변경 없이 현황을 확인하거나, 인자 없이 실행해 자동 수정.
고아 태그(어디서도 안 쓰이는 항목)는 스크립트가 보고하지만 **자동 삭제하지 않음** — 사용자 확인 후 `_tags.md` 해당 행을 수동 삭제.

## 하지 말 것

- `_tags.md` 직접 편집 금지 (hook 순서와 충돌, 스크립트가 처리)
- `blog/index.md` `tags:` 배열 직접 편집 금지 (항상 스크립트가 재생성)
- 모든 .md 파일을 직접 grep해서 태그 집합 도출 금지 (토큰 낭비, 스크립트가 처리)
