---
name: cloud-cli-safety
category: operations
description: "AWS / GCP 위험 CLI 명령 카탈로그 — 데이터 손실 / 권한 / 비용 폭증 위험. Use when 클라우드 destructive operation 검토 또는 install 받는 프로젝트의 cloud-cli-safety rule 활성화 시."
effort: xhigh
deprecated: false
---

# Cloud CLI Safety — 위험 명령 카탈로그

AI 코딩 어시스턴트가 실행해서는 안 되는 위험한 클라우드 CLI 명령 상세 카탈로그.
**모든 항목이 주석 처리**되어 있으며, 프로젝트에서 사용하는 서비스만 주석 해제하여 활성화한다.

> 활성화 방법: 해당 서비스 섹션의 `<!-- ... -->` 주석을 제거하고 [`.claude/rules/cloud-cli-safety.md`](../../rules/cloud-cli-safety.md) 에 복사 또는 본 skill 자체에서 활성화.
> 2026-03 기준 작성. 실제 사고 사례 기반.

---

## AWS 위험 CLI 명령

<!--
### CloudFront (Full Replace API)
- `aws cloudfront update-distribution` 실행 금지
  - full replace API — 누락된 필드는 기본값으로 초기화됨
  - flat-rate pricing plan 해제, WAF 연결 해제, 커스텀 에러 페이지 소실 위험
  - 대안: AWS 콘솔에서 수동 변경, 또는 `get-distribution-config` → 전체 JSON 수정 → ETag 포함 업데이트
- `aws cloudfront create-invalidation` 과다 호출 주의 — 1,000건/월 초과 시 건당 $0.005 과금
-->

<!--
### S3 (데이터 삭제)
- `aws s3 rm --recursive` 실행 금지 — 버킷 내 전체 객체 삭제, 확인 프롬프트 없음
- `aws s3 rb --force` 실행 금지 — 버킷 + 전체 내용 삭제
- `aws s3 sync --delete` 실행 전 반드시 `--dryrun` 먼저 — source/destination 뒤바뀌면 프로덕션 데이터 소실
-->

<!--
### EC2 (인스턴스 & 네트워크)
- `aws ec2 terminate-instances` 실행 금지 — 영구 삭제, instance store 데이터 복구 불가
- `aws ec2 modify-instance-attribute --groups` 주의 — 보안 그룹 **전체 교체**(additive 아님)
- `aws ec2 authorize-security-group-ingress --cidr 0.0.0.0/0` 금지 — 전체 인터넷 오픈
- `aws ec2 release-address` 주의 — Elastic IP 반납 후 재할당 불가
- `aws ec2 delete-snapshot` / `aws ec2 delete-volume` — 영구 삭제, 복구 불가
-->

<!--
### RDS (데이터베이스)
- `aws rds delete-db-instance --skip-final-snapshot` 실행 금지 — 백업 없이 DB 영구 삭제
- `aws rds modify-db-instance --db-instance-class` 주의 — 인스턴스 변경 시 다운타임 + 과금 급증 가능
- `aws rds modify-db-instance --apply-immediately` 주의 — 즉시 적용 = 즉시 다운타임
- `aws rds delete-db-cluster --skip-final-snapshot` 실행 금지 — Aurora 클러스터 전체 삭제
-->

<!--
### IAM (권한 & 보안)
- `aws iam put-role-policy` / `aws iam attach-role-policy` — `"Action": "*"` 또는 `AdministratorAccess` 부여 금지
- `aws iam create-policy-version --set-as-default` 주의 — 정책 문서 **전체 교체**
- `aws iam create-access-key` 주의 — 장기 자격증명 생성, 유출 위험
- `aws iam delete-role` / `aws iam delete-user` — 실행 중인 서비스 접근 즉시 중단
-->

<!--
### EKS / ECS (컨테이너)
- `aws eks delete-cluster` 주의 — LB/VPC 리소스 고아화(orphan) → 지속 과금
- `aws eks delete-nodegroup` — 모든 워커 노드 + Pod 즉시 삭제
- `aws ecs delete-service --force` — 드레인 없이 즉시 종료
- `aws ecs update-service --desired-count 0` — 서비스 사실상 중단
-->

<!--
### Route 53 (DNS)
- `aws route53 delete-hosted-zone` 실행 금지 — 전체 DNS 레코드 소실, 도메인 접속 불가
- `aws route53 change-resource-record-sets` DELETE/UPSERT 주의 — 잘못된 값으로 트래픽 하이재킹 가능
-->

<!--
### KMS (암호화 키)
- `aws kms schedule-key-deletion` 실행 금지 — 키 삭제 시 암호화된 **모든 데이터 영구 복구 불가**
- 대안: `aws kms disable-key` (가역적) 사용, 대기 기간 내 `cancel-key-deletion` 가능
-->

<!--
### DynamoDB
- `aws dynamodb delete-table` 실행 금지 — 테이블 + 전체 아이템 영구 삭제
- `aws dynamodb update-table --billing-mode PROVISIONED` 주의 — 높은 RCU/WCU 설정 시 과금 급증
-->

<!--
### ElastiCache
- `aws elasticache delete-replication-group` 실행 금지 — 즉시 비가역적 삭제, 취소 불가
- 대안: `--retain-primary-cluster true` + `--final-snapshot-identifier` 사용
-->

<!--
### CloudFormation
- `aws cloudformation delete-stack` 실행 금지 — 스택 내 **모든 리소스** 삭제 (terraform destroy 동급)
-->

<!--
### Lambda
- `aws lambda put-function-concurrency --reserved-concurrent-executions 0` — 함수 사실상 비활성화
- `aws lambda update-function-configuration --memory-size` 주의 — 메모리 증가 = 호출당 비용 증가
-->

---

## GCP 위험 gcloud 명령

<!--
### 프로젝트 (Nuclear Option)
- `gcloud projects delete` 실행 금지 — 프로젝트 전체 종료, 30일 복구 기간 있으나 일부 리소스는 즉시 삭제
- `gcloud services disable --force` 주의 — 의존 서비스 연쇄 중단
-->

<!--
### Compute Engine
- `gcloud compute instances delete` 실행 금지 — VM 영구 삭제, 부트 디스크도 기본 삭제 (`--keep-disks` 미지정 시)
- `gcloud compute disks delete` — 디스크 + 스냅샷 영구 삭제
- `gcloud compute instances create --accelerator` 주의 — A100 GPU ~$2.93/hr, H100은 더 높음
-->

<!--
### GKE (Kubernetes Engine)
- `gcloud container clusters delete` 실행 금지 — 마스터 + 노드 + Pod 전체 삭제, 외부 LB/PD는 고아화 → 지속 과금
- `gcloud container node-pools delete` — 노드풀 전체 삭제, 워크로드 재스케줄 불가 시 서비스 중단
-->

<!--
### Cloud SQL
- `gcloud sql instances delete` 실행 금지 — DB 영구 삭제, 4일 내 Cloud Care 연락해야 복구 가능
- `gcloud sql instances patch --tier` 주의 — 머신 타입 변경 시 재시작 + 과금 변경
- `gcloud sql instances patch --database-flags` 주의 — 일부 플래그 변경 시 강제 재시작
-->

<!--
### Cloud Storage
- `gcloud storage rm -r gs://BUCKET/**` 실행 금지 — 전체 객체 재귀 삭제
- `gcloud storage rm --all-versions` 주의 — 버저닝 보호 무력화, 모든 버전 삭제
- `gcloud storage buckets delete` — 버킷 영구 삭제
-->

<!--
### IAM
- `gcloud iam service-accounts delete` 주의 — 해당 SA 사용하는 모든 워크로드 즉시 인증 실패
- `gcloud projects add-iam-policy-binding --role=roles/owner` 금지 — 전체 프로젝트 제어권 부여
- `gcloud projects remove-iam-policy-binding` 주의 — 잘못된 바인딩 제거 시 관리자 잠금(lockout)
-->

<!--
### KMS (암호화 키)
- `gcloud kms keys versions destroy` 실행 금지 — 키 파괴 시 암호화된 **모든 데이터 영구 복구 불가**
- 대안: 30~120일 예약 파괴 기간 내 `gcloud kms keys versions restore`로 취소 가능
-->

<!--
### VPC / 네트워크
- `gcloud compute networks delete` 실행 금지 — VPC + 서브넷 + 라우트 + 방화벽 전체 삭제, 연쇄 장애
- `gcloud compute firewall-rules delete` 주의 — allow 규칙 삭제 시 트래픽 차단, deny 규칙 삭제 시 노출
-->

<!--
### DNS
- `gcloud dns managed-zones delete` 실행 금지 — 전체 DNS 존 + 레코드 삭제
- `gcloud dns record-sets delete` 주의 — A/CNAME 삭제 시 서비스 접속 불가, DNS 전파 지연으로 복구 지연
-->

<!--
### Pub/Sub
- `gcloud pubsub topics delete` — 구독 고아화, 미전달 메시지 소실
- `gcloud pubsub subscriptions delete` — 미확인(unacked) 메시지 영구 소실, 재생성해도 복구 불가
-->

<!--
### BigQuery
- `bq rm -r -f DATASET` 실행 금지 — 데이터셋 + 전체 테이블 강제 삭제
- `bq query` 대량 스캔 주의 — on-demand 모드에서 PB급 테이블 `SELECT *` 시 수천 달러 과금
  - 대안: `--maximum_bytes_billed` 플래그 필수 사용
-->

<!--
### Cloud Functions / Cloud Run
- `gcloud functions delete` / `gcloud run services delete` — 영구 삭제, 복원 불가
-->

---

## 공통 위험 패턴

<!--
### Full Replace API (PUT 패턴)
다음 API는 부분 업데이트가 아닌 **전체 교체** — 누락 필드가 기본값으로 초기화됨:
- AWS: `cloudfront update-distribution`, `ec2 modify-instance-attribute --groups`, `iam create-policy-version`
- GCP: 대부분 `patch` 명령은 partial update이나, 일부 nested 필드는 전체 교체
-->

<!--
### --force / --quiet 플래그
- AWS `--force`: 의존성 체크 우회 (예: `ecs delete-service --force`)
- GCP `--quiet` / `-q`: 확인 프롬프트 생략 — delete 명령과 조합 시 무확인 삭제
- 두 플래그 모두 AI 어시스턴트가 자동으로 추가하면 안 됨
-->

<!--
### 과금 폭증 명령
- GPU/TPU 인스턴스 생성 (A100 ~$2.93/hr, H100 ~$12/hr)
- 대형 인스턴스 타입 변경 (n2-megamem-416 ~$28/hr)
- DynamoDB/BigQuery 프로비저닝 용량 급증
- CloudFront 무효화(invalidation) 과다 호출
- AI 어시스턴트가 리소스 생성/변경 시 반드시 **예상 비용을 사용자에게 고지**
-->

---

## 활성화 시 본 rule 과의 관계

- 기본 룰: [`.claude/rules/cloud-cli-safety.md`](../../rules/cloud-cli-safety.md) — 활성화 가이드 + 분류 (rule 자동 로드)
- 본 skill: 상세 명령 카탈로그 (on-demand 로드)
- 활성화 절차: skill 의 해당 섹션 주석 제거 → rule 에 복사 (rule 자동 적용) 또는 skill 자체 활성화 (Claude Code discovery)

## 관련 문서

- [`rules/cloud-cli-safety.md`](../../rules/cloud-cli-safety.md) — 활성화 가이드 (자동 로드)
- [`rules/user-approval.md`](../../rules/user-approval.md) — 외부 작업 사전 승인 룰
- [`rules/security.md`](../../rules/security.md) — 시크릿 / 입력 검증
