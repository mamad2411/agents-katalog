---
name: logging-compliance
category: observability
description: "Compliance Logging Patterns — 결제, 개인정보, 법적 요구사항을 충족하는 로그 저장 가이드 Use when working with observability 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Compliance Logging Patterns

결제, 개인정보, 법적 요구사항을 충족하는 로그 저장 가이드

## Quick Reference (결정 트리)
```
로그 종류별 보존 기간
    ├─ 결제/거래 기록 ────> 5년 (전자금융거래법)
    ├─ 시스템 접근 로그 ──> 1년+ (전자금융감독규정)
    ├─ 중요원장 접근 ────> 5년 (금융규정)
    ├─ 개인정보 접속기록 ─> 1년+ (개인정보보호법)
    └─ 감사 로그 (PCI) ──> 1년 (3개월 즉시접근)
```

---

## CRITICAL: 티켓 예매 시스템 필수 로그

### 로그 종류별 요구사항
| 로그 종류 | 보존 기간 | 근거 법령 | 즉시 접근 |
|----------|----------|----------|----------|
| 결제 거래 기록 | 5년 | 전자금융거래법 §22 | - |
| 결제 시스템 로그 | 1년+ | 전자금융감독규정 §11 | - |
| 카드 정보 접근 | 1년 | PCI-DSS Req.10 | 3개월 |
| 회원정보 접속기록 | 1년+ | 개인정보보호법 | - |
| 민감정보 접근 | 2년+ | 개인정보보호법 | - |

---

## 결제 로그 (PCI-DSS + 전자금융거래법)

### 필수 기록 항목
```json
{
  "log_type": "payment",
  "timestamp": "2026-01-24T10:30:00Z",
  "transaction_id": "TXN-20260124-001",
  "user_id": "USR-12345",
  "action": "payment_request",

  "payment": {
    "amount": 150000,
    "currency": "KRW",
    "method": "card",
    "card_last4": "1234",
    "pg_provider": "nice_payments"
  },

  "result": {
    "status": "success",
    "pg_transaction_id": "NICE-ABC123",
    "approved_at": "2026-01-24T10:30:01Z"
  },

  "context": {
    "ip_address": "203.0.113.45",
    "device_fingerprint": "fp-abc123",
    "session_id": "sess-xyz789"
  }
}
```

### CRITICAL: 카드 정보 마스킹 (PCI-DSS)
```
✅ 저장 가능
─────────────
- 카드 끝 4자리 (1234)
- 카드 브랜드 (VISA, MC)
- 유효기간 (선택)

❌ 절대 저장 금지
─────────────────
- 전체 카드번호 (PAN)
- CVV/CVC
- PIN
- 전체 트랙 데이터
```

### 전자금융거래법 필수 기록
```json
{
  "log_type": "electronic_financial_transaction",
  "거래일시": "2026-01-24T10:30:00Z",
  "거래유형": "티켓구매",
  "거래금액": 150000,
  "거래수단": "신용카드",
  "거래결과": "승인",
  "오류내용": null,
  "이용자식별정보": "USR-12345",
  "접속IP": "203.0.113.45"
}
```

---

## 개인정보 접속기록 (개인정보보호법)

### 필수 기록 항목 (안전성 확보조치 기준)
```json
{
  "log_type": "personal_info_access",
  "timestamp": "2026-01-24T10:30:00Z",

  "접속자": {
    "식별자": "admin-001",
    "부서": "고객지원팀",
    "역할": "cs_agent"
  },

  "접속정보": {
    "접속일시": "2026-01-24T10:30:00Z",
    "접속지": "203.0.113.45",
    "접속수단": "admin_portal"
  },

  "처리내역": {
    "처리한_정보주체": "USR-12345",
    "수행업무": "회원정보조회",
    "조회항목": ["name", "phone", "email"]
  }
}
```

### 월간 점검 체크리스트
```
개인정보보호법 요구사항 (월 1회 이상 점검)
─────────────────────────────────────────
□ 비정상 대량 조회 탐지
□ 업무시간 외 접근 확인
□ 퇴직자 계정 접근 시도
□ 권한 외 데이터 접근
□ 다운로드/출력 이력 검토
```

### 개인정보 마스킹 규칙
```java
// 로그에 기록 시 마스킹 적용
public class PersonalInfoMasker {
    // 이메일: user***@domain.com
    public String maskEmail(String email) {
        return email.replaceAll("(?<=.{4}).(?=.*@)", "*");
    }

    // 전화번호: 010-****-5678
    public String maskPhone(String phone) {
        return phone.replaceAll("(\\d{3})-(\\d{4})-(\\d{4})", "$1-****-$3");
    }

    // 이름: 홍*동
    public String maskName(String name) {
        if (name.length() <= 2) return name.charAt(0) + "*";
        return name.charAt(0) + "*".repeat(name.length() - 2) + name.charAt(name.length() - 1);
    }
}
```

---

## 로그 저장 아키텍처

### 보존 기간별 스토리지 티어링
```
┌─────────────────────────────────────────────────┐
│           Hot Storage (SSD/EBS)                 │
│           최근 3개월 - 즉시 접근                  │
│           PCI-DSS 감사 대비                      │
└─────────────────────┬───────────────────────────┘
                      │ 3개월 후
                      ▼
┌─────────────────────────────────────────────────┐
│           Warm Storage (S3 Standard)            │
│           3개월 ~ 1년                            │
│           시스템/접근 로그                        │
└─────────────────────┬───────────────────────────┘
                      │ 1년 후
                      ▼
┌─────────────────────────────────────────────────┐
│           Cold Storage (S3 Glacier)             │
│           1년 ~ 5년                              │
│           결제 거래 기록 (법적 보존)              │
└─────────────────────────────────────────────────┘
```

### S3 Lifecycle 정책
```yaml
# s3-lifecycle.yaml
Rules:
  - ID: compliance-log-tiering
    Status: Enabled
    Filter:
      Prefix: compliance-logs/
    Transitions:
      - Days: 90
        StorageClass: STANDARD_IA
      - Days: 365
        StorageClass: GLACIER
    Expiration:
      Days: 1825  # 5년

  - ID: access-log-retention
    Status: Enabled
    Filter:
      Prefix: access-logs/
    Expiration:
      Days: 400  # 1년 + 여유
```

---

## 로그 분리 전략

### Fluent Bit 라우팅
```yaml
# 결제 로그 → 별도 스토리지 (5년 보관)
[FILTER]
    Name rewrite_tag
    Match kube.*
    Rule $log_type ^payment$ payment.$TAG true

# 개인정보 접근 로그 → 별도 스토리지
[FILTER]
    Name rewrite_tag
    Match kube.*
    Rule $log_type ^personal_info_access$ pii_access.$TAG true

[OUTPUT]
    Name s3
    Match payment.*
    bucket compliance-logs-5year
    region ap-northeast-2

[OUTPUT]
    Name s3
    Match pii_access.*
    bucket pii-access-logs-2year
    region ap-northeast-2
```

---

## 감사 대응

### PCI-DSS 감사 시 제출 항목
```
요구사항 10 (로깅 및 모니터링)
─────────────────────────────
□ 카드 데이터 접근 로그 1년치
□ 최근 3개월 즉시 조회 가능 증빙
□ 로그 무결성 검증 (해시/서명)
□ 시간 동기화 증빙 (NTP)
□ 로그 백업 및 복구 테스트
```

### 로그 무결성 보장
```yaml
# 로그 해시 생성 (일별)
apiVersion: batch/v1
kind: CronJob
metadata:
  name: log-integrity-hash
spec:
  schedule: "0 0 * * *"
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: hasher
            image: alpine
            command:
            - /bin/sh
            - -c
            - |
              DATE=$(date -d "yesterday" +%Y-%m-%d)
              sha256sum /logs/${DATE}/*.log > /hashes/${DATE}.sha256
              # 해시를 변조 불가 스토리지에 저장
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 카드번호 전체 저장 | PCI-DSS 위반 | 마스킹/토큰화 |
| 단일 보존 기간 | 비용 낭비/규정 위반 | 로그별 티어링 |
| 로그 무결성 미검증 | 감사 부적합 | 해시/WORM 스토리지 |
| 접속기록 미점검 | 개인정보법 위반 | 월간 자동 리포트 |
| 즉시 접근 불가 | PCI 감사 실패 | Hot 스토리지 3개월 |

---

## 체크리스트

### 결제 (PCI-DSS + 전자금융)
- [ ] 카드정보 마스킹 적용
- [ ] 거래기록 5년 보관 설정
- [ ] 감사로그 1년 (3개월 즉시접근)
- [ ] 로그 무결성 검증

### 개인정보
- [ ] 접속기록 1년+ 보관
- [ ] 월간 점검 자동화
- [ ] 개인정보 마스킹 적용

### 인프라
- [ ] 스토리지 티어링 구성
- [ ] S3 Lifecycle 정책
- [ ] 백업 및 복구 테스트

**관련 skill**: `/monitoring-logs`, `/logging-security`

---

## 참고 자료
- [PCI DSS 한국어 문서](https://www.pcisecuritystandards.org/pdfs/pci_dss_korean.pdf)
- [전자금융거래법](https://www.law.go.kr/LSW/lsInfoP.do?lsiSeq=218909)
- [개인정보 안전성 확보조치 기준](https://www.law.go.kr/admRulLsInfoP.do?chrClsCd=010202&admRulSeq=2100000229672)
