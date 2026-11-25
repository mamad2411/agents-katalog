---
name: cdsa-lecture-wiki
description: CDSA 강의안, 강의 메시지, 개념, 사례, 실습과 모듈 카드를 로컬 온톨로지에서 검색하고 대상·시간·난이도·주제에 맞는 강의안을 조합한다. 공공기관 AI 교육, 강사양성, AI 리더십, 문서·데이터·자동화·에이전트 교육의 강의 구성, 커리큘럼 재조립, 관련 사례 회수, 원고 근거 확인과 실제 HTML·PPTX 강의안 제작 요청에 사용한다. 강의안 파일 제작 시 함께 설치된 lecture-deck, ssjhtml3, ssjppt1 중 산출물에 맞는 스킬로 연결한다.
---

# CDSA 강의 지식 위키

번들된 `data/knowledge-base.json`을 전부 프롬프트에 읽지 말고 스크립트로 필요한 노드만 회수한다. 모든 결과에 노드 ID와 `source_refs`를 유지한다.

## 작업 흐름

1. 요청에서 주제, 대상, 총 시간, 난이도, 원하는 산출물을 추출한다.
2. 단일 주제·사례·메시지 질문이면 `scripts/query.mjs`를 실행한다.
3. 시간표나 전체 강의안 요청이면 `scripts/compose.mjs`로 모듈 후보를 조합한다.
4. 선택된 핵심 노드를 다시 `query.mjs --hop`으로 확장해 관련 개념·사례·실습을 얻는다.
5. 개요·원고 요청이면 회수된 내용으로 작성한다. 실제 슬라이드 파일 요청이면 아래 제작 스킬 선택 규칙을 따른다.
6. 완성본 마지막 또는 별도 출처 메모에 사용한 노드 ID와 원본 위치를 적는다.
7. 검색 결과가 약하면 표현을 짧게 바꾸거나 `--type`, `--audience`, `--difficulty` 필터를 완화한다. 찾지 못한 내용을 저장소에 있다고 추측하지 않는다.

스크립트 경로는 이 `SKILL.md`가 있는 폴더를 기준으로 해석한다. Windows에서도 Node.js만 있으면 실행된다.

## 지식 검색

```powershell
node scripts/query.mjs "중간관리자가 AI 시대에 해야 할 일" --limit 5 --hop
node scripts/query.mjs "RAG 대안" --type concept
node scripts/query.mjs "공공기관 환각 검증" --audience 공공기관
```

반환 JSON의 `results`가 직접 검색 결과이고, `context`가 1-hop 관계 맥락이다. 긴 `content` 필드는 기본 출력에서 제외된다.

## 과정 조합

```powershell
node scripts/compose.mjs "문서작성과 업무자동화" --audience "공공기관 실무자" --duration 120
node scripts/compose.mjs "AI 리더십" --audience "기관 관리자" --duration 180 --difficulty 초급
```

총 시간은 분 단위다. 결과의 `remaining_minutes`가 크면 관련 검색 결과를 검토해 오프닝·정리 모듈을 보완한다. 자동 조합을 그대로 확정하지 말고 학습 흐름, 선수 지식, 실습 가능 환경을 점검한다.
글로벌 리더 강의의 개별 장표까지 시간표 후보에 넣을 때만 `--include-slides`를 추가한다.

## 강의안 제작 스킬 선택

슬라이드 파일 제작을 요청받으면 지식 검색과 과정 조합을 먼저 끝낸 뒤 다음 중 하나만 선택한다. 선택한 형제 스킬의 `SKILL.md`를 전부 읽고 그 제작·검증 절차를 따른다.

- 기본 교육용 HTML 강의안, 원본 문장·사례·실습 누락 방지가 중요함 → `../lecture-deck/SKILL.md`
- 원장·임원 키노트, 중간·최종보고, 관계형 도식과 의사결정 메시지가 중요함 → `../ssjhtml3/SKILL.md`
- 사용자가 편집 가능한 PowerPoint `.pptx`를 명시함 → `../ssjppt1/SKILL.md`

산출물 형식이 지정되지 않은 일반적인 “강의안 만들어줘”는 `lecture-deck`을 기본으로 한다. 같은 결과물에 세 제작 스킬을 혼용하지 않는다. 제작 스킬이 설치되어 있지 않으면 검색·개요까지만 제공하고 누락된 스킬 이름을 알린다.

제작 스킬에 넘길 강의 원장은 다음 항목을 포함한다.

```text
강의 제목 / 대상 / 총 시간 / 난이도
학습목표 / 시간표 / 선택 모듈
장표별 핵심 메시지 / 근거 / 사례 / 실습 / 도구
사용 노드 ID / source_refs
```

## 작성 규칙

- 원본 표현을 길게 복제하지 말고 검색된 노드의 메시지를 대상과 시간에 맞게 재구성한다.
- `status: reviewed`는 저장소 내부 검수 상태이지 외부 사실의 최신성을 보장하지 않는다.
- 제품명, 출시일, 통계 등 시점에 민감한 사실은 강의 직전에 별도 확인한다.
- 출처는 `node.id — source_refs.path, source_refs.locator` 형식으로 남긴다.
- 중복 모듈은 `overlaps_with` 관계를 확인해 하나만 선택한다.
- 스키마와 관계 의미가 필요할 때만 `references/ontology.md`를 읽는다.
