---
name: terraform-pitfalls
category: infrastructure
description: "Terraform 실전 Pitfalls — Terraform/OpenTofu 운영 중 발생하는 실전 함정. state 관리/모듈 설계/순환 의존/secret 노출. Use when working with infrastructure 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# Terraform 실전 Pitfalls

Terraform/OpenTofu 운영 중 발생하는 실전 함정. state 관리/모듈 설계/순환 의존/secret 노출.
2026-04-01 SG 삭제 사고, IP 고갈 사고 경험 기반.

---

## 1. Security Group Inline vs Separate Rule 충돌

### 문제
`aws_security_group` 내 inline `ingress` 블록과 별도 `aws_security_group_rule` 리소스가 동일 SG를 관리 → `terraform apply` 시 inline 규칙이 separate 규칙을 삭제.

### 원인
Terraform은 inline 규칙을 "SG의 전체 규칙 집합"으로 간주. `plan` 시 separate 규칙이 없으므로 삭제 대상으로 판단.

### 사고 (2026-04-01)
RDS SG에 inline ingress + separate `aws_security_group_rule` 혼용 → apply 시 RDS 접근 규칙 삭제 → 전체 서비스 DB 접근 불가.

### 해결
```hcl
# BAD: 혼용
resource "aws_security_group" "rds" {
  ingress { ... }  # inline
}
resource "aws_security_group_rule" "rds_app" { ... }  # separate

# GOOD: 신규 리소스만 사용
resource "aws_security_group" "rds" {
  # ingress/egress 블록 없음
}
resource "aws_vpc_security_group_ingress_rule" "rds_app" {
  security_group_id = aws_security_group.rds.id
  ...
}
```

### 마이그레이션
1. Inline 규칙을 `ingress = []`, `egress = []`로 비움
2. Separate `aws_vpc_security_group_*_rule` 리소스 생성
3. `terraform state rm` old separate rules → `terraform import` new rules
4. `terraform plan`으로 no-change 확인

---

## 2. ENI Prefix Delegation IP 계산

### 공식
```
노드당 IP 소모 = ENIs_per_instance × /28_prefixes × 16
서브넷 필요 IP = 노드수 × 노드당_IP + 시스템_예약(5)

예: m5.large, 20 노드
= 20 × (3 × 3 × 16) + 5
= 20 × 144 + 5 = 2,885 IPs
→ /20 서브넷 (4,096) 필요
```

### 인스턴스 타입별 ENI/IP

| Type | ENIs | IPs/ENI | Prefix 시 max-pods |
|------|------|---------|-------------------|
| m5.large | 3 | 10 | 434 (cap 250) |
| m5.xlarge | 4 | 15 | 898 (cap 250) |
| m6i.large | 3 | 10 | 434 (cap 250) |
| t3.medium | 3 | 6 | 242 (cap 250) |

실무: max-pods = 110 권장 (K8s 스케줄러 안정성).

---

## 3. create_before_destroy 패턴

### 사용 시점
- Zero-downtime 리소스 교체 필요 시
- Launch template / ASG 변경 시

```hcl
resource "aws_launch_template" "eks" {
  lifecycle {
    create_before_destroy = true
  }
}
```

### 주의
- S3 bucket, RDS 등 unique constraint 있는 리소스에는 사용 불가 (이름 충돌)
- `name_prefix` 사용으로 이름 충돌 회피 가능

---

## 4. ignore_changes 올바른 사용

### 적합한 경우
```hcl
# EKS managed node group: AWS가 자동 업데이트하는 필드
lifecycle {
  ignore_changes = [
    scaling_config[0].desired_size,  # autoscaler가 변경
  ]
}

# ArgoCD가 관리하는 K8s 리소스
lifecycle {
  ignore_changes = [
    metadata[0].annotations,  # ArgoCD가 추가하는 annotation
  ]
}
```

### 부적합한 경우 (안티패턴)
```hcl
# BAD: 보안 관련 설정을 ignore → drift 발생
lifecycle {
  ignore_changes = [
    ingress,  # SG 규칙 drift 숨김
    tags,     # 비용 추적 tag 유실
  ]
}
```

---

## 5. State 파일 보안

### 위험
Terraform state에는 **모든 리소스 속성이 평문 저장** — `sensitive = true`도 state에서는 평문.

```json
// terraform.tfstate 내부
"attributes": {
  "password": "actual-plaintext-password",
  "master_password": "actual-db-password"
}
```

### 필수 보호
```hcl
terraform {
  backend "s3" {
    bucket         = "company-terraform-state"
    key            = "env/prod/terraform.tfstate"
    region         = "ap-northeast-2"
    encrypt        = true
    kms_key_id     = "alias/terraform-state"
    dynamodb_table = "terraform-locks"
  }
}
```

### .gitignore 필수 항목
```
*.tfstate
*.tfstate.backup
*.tfvars        # 시크릿 포함 가능
.terraform/
```

### IAM 접근 제한
- State S3 bucket: terraform-admin role만 접근
- KMS key: terraform-admin role만 decrypt
- `terraform state pull` 출력을 로그/채팅에 공유 금지

---

## 6. 보안 체크리스트

### S3
```hcl
resource "aws_s3_bucket_public_access_block" "this" {
  bucket                  = aws_s3_bucket.this.id
  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
```

### RDS
```hcl
resource "aws_db_instance" "this" {
  publicly_accessible    = false          # MUST
  deletion_protection    = true           # MUST (prod)
  skip_final_snapshot    = false          # MUST (prod)
  storage_encrypted      = true           # MUST
  kms_key_id            = aws_kms_key.rds.arn
}
```

### EKS
```hcl
resource "aws_eks_cluster" "this" {
  # Public endpoint 비활성화 (private only) 또는 CIDR 제한
  vpc_config {
    endpoint_private_access = true
    endpoint_public_access  = true
    public_access_cidrs    = ["10.0.0.0/8"]  # VPN/사무실 CIDR만
  }
}
```
