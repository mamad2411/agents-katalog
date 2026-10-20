---
name: aws-eks-advanced
category: infrastructure
description: "AWS EKS 고급 가이드 — Karpenter 설정, 보안 강화, 운영 최적화 Use when working with infrastructure 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# AWS EKS 고급 가이드

Karpenter 설정, 보안 강화, 운영 최적화

## Karpenter 설정

```hcl
# karpenter.tf
module "karpenter" {
  source  = "terraform-aws-modules/eks/aws//modules/karpenter"
  version = "~> 20.0"

  cluster_name = module.eks.cluster_name

  enable_irsa                     = true
  irsa_oidc_provider_arn          = module.eks.oidc_provider_arn
  irsa_namespace_service_accounts = ["karpenter:karpenter"]

  node_iam_role_additional_policies = {
    AmazonSSMManagedInstanceCore = "arn:aws:iam::aws:policy/AmazonSSMManagedInstanceCore"
  }
}
```

```yaml
# karpenter-nodepool.yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: default
spec:
  template:
    spec:
      requirements:
        - key: kubernetes.io/arch
          operator: In
          values: ["amd64"]
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["spot", "on-demand"]
        - key: karpenter.k8s.aws/instance-category
          operator: In
          values: ["c", "m", "r"]
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default
  limits:
    cpu: 1000
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 30s
---
apiVersion: karpenter.k8s.aws/v1
kind: EC2NodeClass
metadata:
  name: default
spec:
  amiFamily: AL2023
  role: KarpenterNodeRole-${CLUSTER_NAME}
  subnetSelectorTerms:
    - tags:
        karpenter.sh/discovery: ${CLUSTER_NAME}
  securityGroupSelectorTerms:
    - tags:
        karpenter.sh/discovery: ${CLUSTER_NAME}
  blockDeviceMappings:
    - deviceName: /dev/xvda
      ebs:
        volumeSize: 100Gi
        volumeType: gp3
        encrypted: true
```

---

## 보안 설정

### 클러스터 보안

```hcl
# Private Endpoint만 사용 (보안 강화)
cluster_endpoint_public_access  = false
cluster_endpoint_private_access = true

# 또는 Public + IP 제한
cluster_endpoint_public_access       = true
cluster_endpoint_public_access_cidrs = ["10.0.0.0/8", "회사IP/32"]
```

### Pod Security Standards

```yaml
# 네임스페이스에 PSS 적용
apiVersion: v1
kind: Namespace
metadata:
  name: production
  labels:
    pod-security.kubernetes.io/enforce: restricted
    pod-security.kubernetes.io/enforce-version: latest
    pod-security.kubernetes.io/warn: restricted
    pod-security.kubernetes.io/audit: restricted
```

### Security Group for Pods

```yaml
apiVersion: vpcresources.k8s.aws/v1beta1
kind: SecurityGroupPolicy
metadata:
  name: db-access-policy
  namespace: production
spec:
  podSelector:
    matchLabels:
      app: backend
  securityGroups:
    groupIds:
      - sg-xxx  # RDS 접근 허용 SG
```

---

## Anti-Patterns

| 실수 | 문제 | 해결 |
|------|------|------|
| Node Role에 모든 권한 | 보안 취약 | IRSA 사용 |
| 작은 VPC CIDR | IP 고갈 | /16 이상 할당 |
| Public Endpoint만 | 보안 노출 | Private + VPN |
| Add-on 수동 관리 | 버전 불일치 | EKS 관리형 사용 |
| 단일 AZ | 가용성 저하 | 3 AZ 분산 |
| Karpenter limits 미설정 | 비용 폭증 | CPU/메모리 제한 설정 |
| Security Group 미사용 | 네트워크 노출 | Pod별 SG 적용 |

---

## 체크리스트

### Karpenter
- [ ] Karpenter IRSA 설정
- [ ] NodePool 정의 (Spot + On-Demand)
- [ ] EC2NodeClass 설정
- [ ] consolidation 정책 설정
- [ ] limits (CPU/메모리) 설정

### 보안
- [ ] Private Endpoint 활성화
- [ ] Pod Security Standards 적용
- [ ] Security Group for Pods 설정
- [ ] Network Policy 활성화
- [ ] 노드 IAM Role 최소 권한

### 운영
- [ ] 모니터링 설정 (CloudWatch, Prometheus)
- [ ] 로깅 활성화 (API, Audit)
- [ ] 클러스터 업그레이드 계획
- [ ] DR 계획 수립

---

## Sources

- [EKS Best Practices Guide](https://aws.github.io/aws-eks-best-practices/)
- [Karpenter Documentation](https://karpenter.sh/docs/)
- [EKS Security Best Practices](https://aws.github.io/aws-eks-best-practices/security/docs/)

---

## 참조 스킬

- `/aws-eks` - EKS 기본 가이드 (VPC, 클러스터, IRSA, Add-ons)
- `/k8s-autoscaling` - Autoscaling 가이드 (HPA, VPA, KEDA)
- `/k8s-security` - Kubernetes 보안
- `/terraform-security` - Terraform 보안 설정
