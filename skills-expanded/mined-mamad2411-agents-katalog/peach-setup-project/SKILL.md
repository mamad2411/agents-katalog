---
name: peach-setup-project
description: |
  신규 프로젝트 모듈 구조 + _common 기본 구성 세팅 스킬.
  "프로젝트 세팅", "모듈 구조 잡아줘", "초기 구성", "프로젝트 초기화" 키워드로 트리거.
  DB 설계 완료 후, 최초 1회 실행.
---

# 프로젝트 모듈 구조 세팅 스킬

## 페르소나

```
당신은 피치솔루션 아키텍처 기반 프로젝트 구조 설계 전문가입니다.
- 모노레포(api/ + front/) 프로젝트 구조 마스터
- modules 분리 전략 설계 (도메인/권한/외부API)
- _common 기본 구성 배치 전문가
- test-data 가이드코드 연결
```

---

## 핵심 원칙

```
┌─────────────────────────────────────────────────────────────────┐
│  peach-setup-project의 역할                                      │
│                                                                 │
│  전제조건: DB 스키마 설계 완료 (peach-gen-db 실행 후)            │
│  실행 시점: 프로젝트 초기 1회                                   │
│  입력: 설계된 테이블 목록 + 시스템 성격                         │
│  출력: modules 구조 + _common 기본 구성 + 가이드코드 연결       │
│                                                                 │
│  ⚠️ "세팅"만 담당. 이후 모듈 생성은 peach-gen-*/peach-team이    │
│     자동 감지하여 적응합니다.                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 워크플로우

### 1단계: 현재 상태 확인

```bash
# 기존 modules 구조 확인
ls -d api/src/modules*/ 2>/dev/null

# _common 존재 여부
ls api/src/modules/_common/ 2>/dev/null

# 설계된 스키마 확인
ls api/db/schema/

# test-data 가이드코드 존재 확인
ls api/src/modules/test-data/ 2>/dev/null
ls front/src/modules/test-data/ 2>/dev/null
```

test-data 가이드코드가 없으면:
```
⚠️ test-data 가이드코드가 없습니다!
먼저 /peach-setup-harness를 실행하여 하네스 시스템을 설정하세요.
```

### 2단계: 시스템 분석 + AI 추천 (May Suggest)

> **이 단계는 생략 불가!** AI가 먼저 분석하고, 사용자가 최종 결정합니다.

**AI 분석:**
```bash
# 1. 도메인 디렉토리 구조 확인
ls api/db/schema/

# 2. 도메인별 테이블 수 확인
ls api/db/schema/*/

# 3. 스키마 내용 샘플링 (외부 연동, 권한 구분 단서 탐색)
head -20 api/db/schema/*/*.sql
```

분석 근거:
- **도메인 그룹**: `api/db/schema/` 하위 디렉토리명으로 판단
- **외부 연동**: 스키마에 외부 API URL, 토큰, 연동 로그 등 외부 시스템 관련 테이블이 있는지 확인
- **권한/조직 분리**: 스키마에 admin/branch/public 등 접속 권역 구분이 보이는지 확인

**증거 충분 시** 추천을 제시한다:
```
📋 AI 추천 분리 전략

테이블 분석:
- 총 테이블: [N]개
- 도메인 그룹: [그룹 목록]
- 외부 연동: [있음/없음] (근거: [테이블명])

추천: **[A~E 중 하나]**
이유: [1~2줄]

이 전략으로 진행할까요? 다른 전략을 원하면 A~E 중 선택해주세요.
```

**증거 불충분 시** (도메인 구분이 불명확하거나 테이블이 3개 이하):
```
⚠️ 스키마만으로 분리 전략을 판단하기 어렵습니다.
아래 A~E 중 선택해주세요.
```

사용자가 다른 전략을 선택하면 그대로 따른다.

**A~E 전략 선택지:**

| 전략 | 구조 | 적합한 경우 |
|------|------|-----------|
| **A. 단일** | `modules/` | 소규모, 테이블 10개 이하 |
| **B. 도메인 분리** | `modules/` + `modules-domain/` | 인프라와 비즈니스 분리 필요 |
| **C. 외부API 포함** | B + `modules-external/` | 외부 시스템 연동 있음 |
| **D. 권한/조직 분리** | `modules-admin/` + `modules-branch/` + `modules-public/` | 접속 권역별 로직 분리 |
| **E. 복합** | 위 전략 조합 | 대규모 시스템 |

선택해주세요 (A~E):

### 질문 3: _common 선택 구성
필수 구성(constants, file, log)은 자동 배치됩니다.
추가로 필요한 것을 선택해주세요:

- [ ] config (설정 관리)
- [ ] email (이메일 발송)
- [ ] slack (Slack 알림)
- [ ] sms (SMS 발송)
```

### 3단계: modules 구조 생성

사용자 답변에 따라 디렉토리를 생성합니다.

**전략 A (단일):**
```
api/src/modules/         ← 이미 존재 (test-data, _common, sign, system)
front/src/modules/       ← 이미 존재
```

**전략 B (도메인 분리):**
```bash
mkdir -p api/src/modules-domain/
mkdir -p front/src/modules-domain/
```

**전략 C (외부API 포함):**
```bash
mkdir -p api/src/modules-domain/
mkdir -p api/src/modules-external/
mkdir -p front/src/modules-domain/
```

**전략 D (권한/조직 분리):**
```bash
mkdir -p api/src/modules-admin/
mkdir -p api/src/modules-branch/
mkdir -p api/src/modules-public/
mkdir -p front/src/modules-admin/
mkdir -p front/src/modules-branch/
mkdir -p front/src/modules-public/
```

**전략 E (복합):** 사용자와 추가 대화로 조합 결정.

### 4단계: _common 기본 구성 배치

**필수 (자동):**

```
api/src/modules/_common/
├── constants/system.constants.ts     # SystemId (System, Excel, API, Batch, TDD)
├── file/
│   ├── service/file-upload-local.service.ts
│   ├── service/file-upload-s3.service.ts
│   ├── dao/file.dao.ts
│   ├── type/file.type.ts
│   └── test/file.test.ts
└── log/
    ├── service/common-log.service.ts
    ├── dao/common-log.dao.ts
    └── type/common-log.type.ts
```

```
front/src/modules/_common/
├── components/           # 공용 UI 컴포넌트
├── services/             # API 호출 서비스
├── store/                # Pinia 글로벌 스토어
└── type/                 # 공용 타입 정의
```

> _common 파일은 피치솔루션 기본 프로젝트(test-data 가이드코드가 있는)의
> `_common/` 구조를 참조하여 배치합니다.

**선택 (사용자 답변에 따라):**
- config/ → `_common/config/`
- email/ → `_common/email/`
- slack/ → `_common/slack/`
- sms/ → `_common/sms/`

### 5단계: server.ts 컨트롤러 등록 확인

```bash
cat api/src/server.ts | grep -A5 controllers
```

modules-* 디렉토리를 추가한 경우, controllers glob 패턴에 해당 경로를 등록합니다:

```typescript
// 예: modules-domain 추가 시
controllers: [
  join(__dirname, 'modules', '**', '*.controller.*'),
  join(__dirname, 'modules-domain', '**', '*.controller.*'),  // 추가
]
```

### 6단계: 완료 보고

```
✅ 프로젝트 모듈 구조 세팅 완료!

분리 전략: [선택된 전략]

생성된 구조:
api/src/
├── modules/          (인프라: _common, test-data, sign, system)
├── modules-domain/   (비즈니스 도메인)
└── modules-external/ (외부 API 연동)

front/src/
├── modules/          (인프라: _common, test-data)
└── modules-domain/   (비즈니스 도메인)

_common 구성:
✅ constants/ (필수)
✅ file/ (필수)
✅ log/ (필수)
[✅/❌] config/ (선택)
[✅/❌] email/ (선택)

다음 단계:
→ /peach-team [모듈명] mode=fullstack 실행하여 첫 모듈 생성
```

---

## Bounded Autonomy

### Must Follow (절대 준수)
- modules/ 에는 인프라 모듈만 (_common, test-data, sign, system)
- _common 필수 3개 (constants, file, log) 반드시 배치
- front↔api 1:1 매칭 (동일한 modules-* 경로)
- server.ts controllers glob 패턴에 새 경로 등록

### May Adapt (분석 후 보완)
- _common 선택 구성 (프로젝트 성격에 따라)
- modules-* 네이밍 (시스템 성격에 맞게)
- 복합 전략의 세부 조합

---

## 참조

- **가이드 코드**: `api/src/modules/test-data/`, `front/src/modules/test-data/`
- **하네스 설정**: `/peach-setup-harness` (CLAUDE.md, AGENTS.md 설정)
