---
name: disaster-recovery-advanced
category: sre
description: "Disaster Recovery 고급 가이드 — 멀티 클러스터 DR, 데이터베이스 DR, 테스트 Use when working with sre 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Disaster Recovery 고급 가이드

멀티 클러스터 DR, 데이터베이스 DR, 테스트

## 멀티 클러스터 DR

### Active-Passive 구성

```yaml
# Primary 클러스터 백업 → Secondary 클러스터 복구
#
# Primary (ap-northeast-2)
#     │
#     │ Velero Backup
#     ▼
# S3 Bucket (교차 리전 복제)
#     │
#     │ Velero Restore
#     ▼
# Secondary (ap-northeast-1)
```

### Cross-Region 복제

```hcl
# S3 버킷 교차 리전 복제
resource "aws_s3_bucket_replication_configuration" "velero" {
  bucket = aws_s3_bucket.velero_primary.id
  role   = aws_iam_role.replication.arn

  rule {
    id     = "dr-replication"
    status = "Enabled"

    destination {
      bucket        = aws_s3_bucket.velero_dr.arn
      storage_class = "STANDARD"
    }
  }
}
```

### DR 클러스터 Standby 유지

```yaml
# DR 클러스터에 Velero BackupStorageLocation 설정
apiVersion: velero.io/v1
kind: BackupStorageLocation
metadata:
  name: primary-backup
  namespace: velero
spec:
  provider: aws
  default: true
  objectStorage:
    bucket: my-velero-backups
  config:
    region: ap-northeast-2  # Primary 리전
---
# 정기적으로 최신 백업 확인
# kubectl get backups -n velero
```

---

## 데이터베이스 DR

### RDS 교차 리전 복제

```hcl
# Read Replica in DR Region
resource "aws_db_instance" "replica" {
  provider                = aws.dr_region
  identifier              = "mydb-replica"
  replicate_source_db     = aws_db_instance.primary.arn
  instance_class          = "db.r6g.large"

  # 장애 시 Standalone으로 승격 가능
  # aws rds promote-read-replica --db-instance-identifier mydb-replica
}
```

### 애플리케이션 레벨 복제

```yaml
# ConfigMap으로 DB 연결 관리
apiVersion: v1
kind: ConfigMap
metadata:
  name: db-config
  namespace: production
data:
  # 정상 시
  DB_HOST: "primary-db.xxx.ap-northeast-2.rds.amazonaws.com"
  # DR 시 변경
  # DB_HOST: "replica-db.xxx.ap-northeast-1.rds.amazonaws.com"
```

---

## DR 테스트

### 정기 테스트 체크리스트

```markdown
## 월간 DR 테스트

### 백업 검증
- [ ] 백업 완료 확인
- [ ] 백업 크기 정상 확인
- [ ] 백업 메타데이터 검증

### 복구 테스트 (격리 환경)
- [ ] 테스트 네임스페이스에 복구
- [ ] 애플리케이션 기동 확인
- [ ] 데이터 무결성 검증
- [ ] 테스트 환경 정리

### 문서 업데이트
- [ ] 복구 시간 측정 (실제 RTO)
- [ ] 절차서 업데이트
- [ ] 담당자 연락처 확인
```

### 자동화된 복구 테스트

```yaml
# CronJob으로 복구 테스트 자동화
apiVersion: batch/v1
kind: CronJob
metadata:
  name: dr-test
  namespace: velero
spec:
  schedule: "0 3 * * 0"  # 매주 일요일 새벽 3시
  jobTemplate:
    spec:
      template:
        spec:
          containers:
            - name: dr-test
              image: velero/velero:latest
              command:
                - /bin/sh
                - -c
                - |
                  # 최신 백업으로 테스트 네임스페이스에 복구
                  BACKUP=$(velero backup get -o json | jq -r '.items[0].metadata.name')
                  velero restore create dr-test-$(date +%Y%m%d) \
                    --from-backup $BACKUP \
                    --namespace-mappings production:dr-test

                  # 검증 후 정리
                  sleep 300
                  kubectl delete namespace dr-test
          restartPolicy: OnFailure
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| 백업 테스트 안함 | 복구 실패 | 정기 복구 테스트 |
| 동일 리전에 백업 | 리전 장애 시 손실 | 교차 리전 복제 |
| RTO/RPO 미정의 | 복구 우선순위 혼란 | 서비스별 정의 |
| 수동 백업만 | 백업 누락 | 스케줄 백업 |
| DB 백업 누락 | 데이터 손실 | 별도 DB 백업 |
| 절차서 미비 | 복구 지연 | 상세 절차서 작성 |
| DR 테스트 미실시 | 실제 장애 시 실패 | 월간 테스트 |
| 단일 리전 DR | 리전 장애 대응 불가 | 멀티 리전 구성 |

---

## 체크리스트

### 멀티 클러스터
- [ ] DR 클러스터 구성 (다른 리전)
- [ ] S3 교차 리전 복제 설정
- [ ] Velero BackupStorageLocation 설정
- [ ] DNS 전환 계획 수립
- [ ] 네트워크 연결 확인

### 데이터베이스
- [ ] RDS Read Replica (교차 리전)
- [ ] 승격(Promote) 절차 문서화
- [ ] 애플리케이션 연결 전환 계획
- [ ] 데이터 정합성 검증 방법

### 테스트
- [ ] 월간 복구 테스트 자동화
- [ ] 복구 시간 측정 (실제 RTO vs 목표 RTO)
- [ ] 테스트 결과 문서화
- [ ] 절차서 정기 업데이트
- [ ] 담당자 교육 및 훈련

---

## Sources

- [Velero Documentation](https://velero.io/docs/)
- [AWS DR Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html)
- [Kubernetes Backup Best Practices](https://kubernetes.io/docs/concepts/cluster-administration/cluster-administration-overview/)

---

## 참조 스킬

- `/disaster-recovery` - DR 기본 가이드 (RTO/RPO, Velero, 백업/복구)
- `/sre-sli-slo` - SLI/SLO 기반 가용성 목표
- `/aws-eks` - EKS 클러스터 설정
- `/k8s-helm` - Helm 차트 관리
