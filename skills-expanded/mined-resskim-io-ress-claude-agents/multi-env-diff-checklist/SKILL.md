---
name: multi-env-diff-checklist
category: kubernetes
description: dev / staging / prod 환경 manifest의 차이를 자동 검증하는 체크리스트. hardcoded 값과 환경별 override 누락을 사전에 검출. 멀티 클라우드(AWS/GCP) 분기까지 포함.
---

# Multi-Environment Diff Checklist

여러 환경(dev / staging / prod, 또는 AWS / GCP 같은 멀티 클라우드)에서 manifest / values / config 파일을 운영할 때, **환경 간 의도된 diff와 실수 diff를 구분하는 체크리스트**.

> ⚠️ 이 체크리스트가 없으면 dev에서 동작하던 코드가 prod에서 zero-value / IAM 권한 거부 / 잘못된 endpoint 호출로 실패한다. 가장 흔한 실패 카테고리.

## 적용 시점

- 신규 환경 추가 (예: prod-gcp 신규 생성, staging 분기)
- 환경별 values 파일 (`values-dev.yaml` vs `values-prod.yaml`) 수정
- 멀티 클라우드 도입 (AWS → GCP 추가, hybrid 등)
- IaC 모듈 복제로 새 환경 생성

---

## 4 카테고리 체크리스트

### 1. 의도된 diff (반드시 환경별로 달라야 하는 값)

| 카테고리 | 예시 | 검증 |
|---------|------|------|
| 리소스 한도 | replicas, resources.limits | prod ≥ staging ≥ dev |
| 외부 endpoint | DB host, Redis host, S3 bucket | 환경별 endpoint 매핑 표 유지 |
| 시크릿 참조 | ExternalSecrets, SealedSecrets | 환경별 secret backend 경로 |
| 이미지 태그 | image.tag | dev=latest 허용, prod=고정 SHA |
| Ingress / Domain | host, TLS issuer | 환경별 도메인 + cert-manager issuer |
| ArgoCD project / sync wave | project, syncPolicy | prod는 manual sync 또는 PreSync hook 추가 |

### 2. 의도하지 않은 diff (모든 환경에서 동일해야 함 — drift 의심)

| 카테고리 | 검증 방법 |
|---------|----------|
| selector label | matchLabels는 환경 불문 동일 키 사용 |
| 컨테이너 args 구조 | 옵션 이름은 동일, 값만 환경별 |
| RBAC 권한 | role / clusterRole 정의는 동일, namespace만 다름 |
| Helm chart 버전 | dev에서 검증된 버전이 staging/prod와 다르면 drift |
| 라이브러리 버전 | Application 이미지 안의 라이브러리는 모든 환경 동일 |

### 3. 멀티 클라우드 분기 (AWS / GCP 등)

| 항목 | AWS | GCP |
|------|-----|-----|
| 노드 archtype | amd64 / arm64 (Graviton) | amd64 / arm64 (Tau T2A) — node selector 다름 |
| 스토리지 클래스 | gp3, io2 (EBS) | pd-balanced, pd-ssd (PD) — `storageClassName` 다름 |
| IAM | IRSA (`eks.amazonaws.com/role-arn`) | Workload Identity (`iam.gke.io/gcp-service-account`) — annotation 키 다름 |
| 시크릿 manager | AWS Secrets Manager | GCP Secret Manager — provider 설정 다름 |
| DB 매니지드 superuser | RDS `postgres` 사용자 | Cloud SQL `cloudsqlsuperuser` (OS-level superuser 아님) |
| Container Registry | ECR (`*.dkr.ecr.<region>.amazonaws.com`) | Artifact Registry (`<region>-docker.pkg.dev`) — pull secret 다름 |

### 4. 외부 시스템 종속 (환경별 분리 필수)

| 외부 시스템 | 환경별 분리 |
|----------|------------|
| DNS / CDN | dev/staging은 별도 서브도메인 + 별도 Cloudflare zone or origin |
| 결제 PG | dev는 sandbox, prod는 production — API key 분리 필수 |
| 소셜 로그인 | redirect URI 환경별 등록 |
| 알림 채널 | dev는 #alerts-dev, prod는 #alerts-prod |
| 이벤트 발행 | dev는 dev-events-topic, prod는 events-topic |

---

## 자동화 스크립트 (CI 검출)

### Helm values diff
```bash
# 환경별 values의 의도된 / 의도하지 않은 diff 검출
diff <(yq 'del(.image.tag, .replicas, .resources)' values-dev.yaml) \
     <(yq 'del(.image.tag, .replicas, .resources)' values-prod.yaml)
# 0 diff 기대 — 출력 발생 시 unexpected drift
```

### Kustomize overlay diff
```bash
# 베이스 + overlay 후 환경 간 일관성 비교
diff <(kustomize build overlays/dev | yq 'del(.metadata.namespace)') \
     <(kustomize build overlays/prod | yq 'del(.metadata.namespace)')
```

### 멀티 클라우드 매핑 검증
```bash
# IAM annotation 환경별 매칭 확인
yq '.serviceAccount.annotations' values-prod-aws.yaml | grep -q 'eks.amazonaws.com/role-arn'
yq '.serviceAccount.annotations' values-prod-gcp.yaml | grep -q 'iam.gke.io/gcp-service-account'
```

---

## 실제 사고 패턴

| 사고 | 원인 | 방지 |
|------|------|------|
| dev 동작, prod CrashLoop | hardcoded dev endpoint | category 1 — endpoint override 매트릭스 유지 |
| GCP 신규 환경에서 image pull 실패 | ECR 경로가 그대로 | category 3 — registry 분기 |
| Cloud SQL extension 설치 실패 | "postgres" 사용자로 시도 | category 3 — superuser 차이 인지 |
| prod에서 secret 빈 값 | secret 이름 prefix 누락 | category 1 — secret 경로 환경별 |
| staging에서 prod 알림 발송 | webhook URL 미override | category 4 — 외부 시스템 분기 |

---

## PR 작성 시 자기 점검

신규 환경 또는 환경별 manifest 수정 PR 작성 후 다음을 확인:

- [ ] 4 카테고리 모두 통과했는가?
- [ ] CI에 환경 간 diff 자동화 스크립트가 등록됐는가?
- [ ] 환경별 endpoint / IAM 매핑 표가 `docs/architecture/` 에 갱신됐는가?
- [ ] secret backend / KMS 키가 환경별로 분리됐는가?
- [ ] 멀티 클라우드 시 archtype / storage class / IAM annotation 분기 확인됐는가?
