---
name: resource-summary-resolve-override-template
description: 리소스 상세 화면의 "요약" 탭에서 `OVERRIDE → TEMPLATE → NONE` 순으로 대시보드를 결정하는 서버-클라이언트 패턴. 오버라이드 엔티티, resolve API, 상태별 UI 드롭다운 규칙까지 포함.
category: arch
tags: [resource-detail, dashboard, override, template, resolve, widget, summary]
triggers:
  - resource summary
  - 리소스 요약
  - resolve override template
  - dashboard override
  - resourceSummary
  - composition override
version: 1.0.0
---

# Resource Summary — Resolve (Override → Template → None)

## Purpose

리소스 상세 화면에 "요약" 탭을 붙일 때, **공용 템플릿 대시보드** 와 **리소스별 개별 편집(override)** 을 하나의 resolve 로직으로 관리하는 패턴. 템플릿 원본을 훼손하지 않고 개별 리소스 맞춤이 가능하게 한다.

## When to Activate

- 리소스 상세에 "요약" 탭/대시보드 추가 요구
- 특정 리소스만 대시보드를 다르게 보여주고 싶지만 공용 템플릿은 유지해야 할 때
- "리소스 삭제 후에도 오버라이드 잔재가 남는다" 류 이슈

## Backend Shape

엔티티 / API / 서비스 핵심 구조:

```
Entity: SummaryComposition
  - confId (리소스 식별자)
  - loginId (사용자별 오버라이드면 함께 키)
  - (confId, loginId) unique
  - tenant isolation (예: @MongoDBIsolationCollection)

Controller: /api/<widget>/resource-summary
  POST   /resolve              # 대시보드 결정 (조회)
  POST   /override             # override 저장 (upsert)
  DELETE /override/{confId}    # override 삭제
  POST   /cleanup              # 고아 매핑 정리

Service.resolve(confId, confType):
  1) override 테이블 lookup       → OVERRIDE
  2) 공용 template (confType 기준) → TEMPLATE
  3) 없으면                        → NONE

confType 규약:
  - template 의 domain 문자열과 동일 (예: "<domain>.<Entity>")

고아 데이터:
  - 리소스 삭제 이벤트(Kafka 등) 리스너로 override 자동 정리
  - event payload 의 리소스 식별자 필드명 확인 (resourceId vs confId 등)
```

## Frontend Shape

```
Step 1. 도메인별 menu config 에 'summary' 키 추가
        - shared config 가 있는 도메인: <domain>DetailMenuList.ts
        - inline enum 쓰는 도메인(APM/KCM 스타일): 해당 enum/리터럴에 추가
Step 2. host 메뉴 항목에 "요약" 텍스트 추가 (보통 "성능" 위)
Step 3. endpoint 상수 + service 메서드 (resolve / override / delete)
Step 4. Drawer/Layout 의 switch 에 ResourceSummary 분기 추가
Step 5. 공용 컴포넌트 4개:
        - ResourceSummary.tsx        # resolve 후 상태 분기 렌더
        - SummaryHeader.tsx          # 배지(파랑=TEMPLATE, 초록=OVERRIDE) + Dropdown
        - CopyEditDialog.tsx         # "이 리소스에 맞게 편집" — copy→override→편집
        - DashboardSelectDialog.tsx  # 다른 대시보드 연결 (검색 + 2열 카드)
```

## 상태별 드롭다운 활성화 규칙

| 메뉴 | TEMPLATE | OVERRIDE | NONE |
|---|---|---|---|
| 기본 템플릿 사용 | 비활성 | **활성** | 비활성 |
| 이 리소스에 맞게 편집 | **활성** | **활성** | 비활성 |
| 다른 대시보드 연결 | **활성** | **활성** | 비활성 |
| 편집 | **활성** | **활성** | 비활성 |

- NONE 상태에서는 "대시보드 선택" CTA 하나만 노출
- "기본 템플릿 사용" 은 OVERRIDE 를 지우는 DELETE 호출로 매핑

## 도메인 매핑 표 (예시)

| 도메인 | confType 예 | confId 소스 | 메뉴 구조 |
|---|---|---|---|
| 서버 | `<domain>.<Entity>` | basicInfo.confId | shared config + summaryGroup/summary |
| 네트워크 | 동일 규칙 | dataInfo.confId | shared config |
| DB | 엔진별 `<engine>.<Entity>` | resourceData.confId | shared config (특정 엔진은 별도 Layout) |
| APM | `apm.<Entity>` | serviceInfo.confId | inline menuTabs 리터럴 |
| KCM | `kcm.<Entity>` | paramDatas.resourceId | 자체 MenuSubKeys enum |

## Pitfalls

- **TEMPLATE 원본 편집 허용 금지**: "편집" 진입 시 현재가 TEMPLATE 이면 자동 copy→override 경로로 유도
- **resolve 호출에 confType 불일치**: template 도메인 문자열과 정확히 동일해야 매칭됨 (오타·대소문자 주의)
- **삭제 이벤트 미구독**: 리소스 삭제됐는데 override 만 남아 목록에 유령 항목 발생 → cleanup 엔드포인트 주기 실행 + 삭제 이벤트 구독 둘 다 권장
- **도메인별 confId 소스 불일치**: APM 은 serviceInfo, KCM 은 resourceId 등 이름이 다르므로 공용 컴포넌트엔 prop 으로 주입

## Checklist

- [ ] SummaryComposition 엔티티 + unique 제약
- [ ] resolve / override / delete / cleanup 4 endpoint
- [ ] resolve 우선순위: OVERRIDE > TEMPLATE > NONE
- [ ] 리소스 삭제 이벤트 → override 자동 정리
- [ ] FE: menu config, host 메뉴, endpoint/service, Drawer case, 4 컴포넌트
- [ ] 상태별 드롭다운 활성화 표대로 구현
- [ ] TEMPLATE 원본 편집 차단, copy→override 경로만 편집 허용
