# AI Robotics 미션 — 로봇 간병인 서비스 기획서

## 프로젝트 개요

- **과제**: 코디세이 AI 올인원 텀 프로젝트 1주 과제
- **도메인**: AI Robotics (7대 도메인 중)
- **산출물**: 서비스 기획서(Markdown) + 발표 자료(PPT/PDF)
- **제출**: 이번 주
- **미션 원문**: [docs/MISSION.md](docs/MISSION.md)

## 채택 아이디어

**"로봇 간병인 서비스"** — 팀원 김도희 제안, 어제 팀 회의에서 채택
- 원안: [docs/로보틱스 아이디어_김도희.md](docs/로보틱스%20아이디어_김도희.md) §#2
- 핵심: 환자 거동 보조 + AI 실시간 보행/안색 분석 + 이상징후 시 병원·보호자 알림 + 복약 확인 + 재활 동작 교정
- 수혜자: 독거노인, 수술 후 회복 환자, 재활 치료 환자
- 근거: 초고령사회 진입(2025), 간병비 월 200~300만원 부담, 기존 AI 간병기기는 알림형이라 물리 보조 부재

## 진행 단계

- [x] 도메인 리서치 (14개 영역)
- [x] 후보 6개 정리, 본인 추천안 2개(B·D) 작성, 팀 피치
- [x] 팀 회의 → 김도희 #2 채택
- [x] docs 정리 — 채택 안 된 본인 산출물 `docs/archive/`로 이동, 의료/돌봄 리서치만 `RESEARCH-CARE.md`로 추출
- [x] 김도희 원안의 마크다운 escape(`\#`, `\-`, `&#x09;`) 정리
- [x] 기획서 작성 — [docs/서비스기획서.md](docs/서비스기획서.md), §4.3 8개 항목 포함 (2026-04-21)
- [ ] 발표 자료 작성

## docs 구조

**활성 (기획서 작성 시 참조)**
- [docs/서비스기획서.md](docs/서비스기획서.md) — **제출 산출물 본체**. 모심로봇(MOSIM), §4.3 8항목, Mermaid 시스템 구성도 포함
- [docs/MISSION.md](docs/MISSION.md) — 미션 정의, §4.3에 기획서 양식 8항목
- [docs/로보틱스 아이디어_김도희.md](docs/로보틱스%20아이디어_김도희.md) — 채택 아이디어 원문 (#2만 유지, escape 정리 완료)
- [docs/RESEARCH-CARE.md](docs/RESEARCH-CARE.md) — 의료/수술/재활(A-4) + 서비스(A-5) + 가정/케어(A-7) 발췌 + VLA·FM·Embodied AI·Sim-to-Real cross-cutting 기술
- [docs/research-drafts/group2-medical-service-agri.md](docs/research-drafts/group2-medical-service-agri.md) — 의료/서비스/농업 영역 상세 출처 드래프트
- `docs/Term-Project 기획안 양식 (예시).pdf` — 양식 참고

**아카이브 (참조 빈도 낮음)**
- `docs/archive/RESEARCH.md` — 14개 영역 전체 리서치 원본
- `docs/archive/IDEAS.md`, `PROPOSAL-B.md`, `PROPOSAL-D.md`, `TEAM-PITCH.md`, `TEAM-PITCH-SHARE.md` — 채택되지 않은 본인 산출물(회고용)
- `docs/archive/research-drafts/group1-industrial-logistics-delivery.md` — 산업/물류/배달 리서치

## 기획서 양식 ([docs/MISSION.md](docs/MISSION.md) §4.3)

| 항목 | 설명 |
|------|------|
| 문제 정의 | 해결하고자 하는 문제와 그 배경, 주제 선택 이유 |
| 타겟 사용자 | 서비스의 주요 사용자 정의, 사용자 니즈 분석 |
| 서비스 개요 | 서비스 이름, 핵심 기능, 기존 서비스 대비 차별점 |
| AI 기술 적용 | 적용할 AI/ML 기술, 기술 선택 이유 |
| 시스템 구성 | 간략한 아키텍처 (다이어그램 권장) |
| 기대 효과 | 사용자 관점, 비즈니스 관점의 기대 효과 |
| 향후 발전 방향 | 서비스 확장 계획, 로드맵 |
| 팀 역할 분담 | 각 팀원의 담당 영역과 기여 내용 |

## 작성 시 주의사항

- **시장 규모 수치**: IFR 공식 지표(설치 대수·밀도) 우선. 민간 리서치펌(SNS Insider, MarketsandMarkets 등)은 편차 2배 이상 — 추정치임을 명시.
- **VLA/FM 단계 구분**: π0.5, GR00T N1, Helix, RoboNurse-VLA 등은 다수가 **연구·오픈소스 시연** 단계. 실 운용 KPI 미공개. "이미 상용화됨"으로 오기재 금지.
- **반복 지연 제품**: Samsung Ballie는 2024 이후 3회 지연(2026 타깃), Tesla Optimus V3는 2026 여름 지연. "예고 시점"과 "실제 출시" 구분.
- **도메인 중첩**: 의료로봇(A-4)은 Healthcare 도메인과 중첩되지만, 본 프로젝트는 **로봇 개체의 인지·의사결정·행동**(Robotics) 관점에서 다룸.
- **김도희 원안 인용 시**: escape 문자 정리 후 사용. 원본 출처는 본인이 아니므로 인용 표기 필요.
