---
name: k8s-troubleshoot-trees
category: kubernetes
description: "K8s Troubleshooting Decision Trees — 실전 트러블슈팅 기록 기반 K8s 디버깅 의사결정 트리. CrashLoopBackOff / ImagePullBackOff / 503 / DNS / NetworkPolicy / Istio AuthZ. Use when working with kubernetes 도메인의 패턴 / 구현 선택."
effort: xhigh
deprecated: false
---

# K8s Troubleshooting Decision Trees

실전 트러블슈팅 기록 기반 K8s 디버깅 의사결정 트리. CrashLoopBackOff / ImagePullBackOff / 503 / DNS / NetworkPolicy / Istio AuthZ.
CrashLoopBackOff 1.5시간 낭비(2026-03-20), ImagePullBackOff 4시간(2026-03-22) 경험 기반.

---

## 1. CrashLoopBackOff

```
Pod CrashLoopBackOff 감지
│
├─ STEP 1: kubectl describe pod → lastState.terminated.reason 확인
│  │
│  ├─ OOMKilled
│  │  ├─ resources.limits.memory 확인
│  │  ├─ OTel Java Agent 사용? → 최소 768Mi 필요
│  │  ├─ 해결: limits 증가 (로그 분석 불필요)
│  │  └─ 반복 시: heap dump 분석 (메모리 누수 의심)
│  │
│  ├─ Error (exitCode 1)
│  │  ├─ kubectl logs --previous 확인
│  │  ├─ 환경변수 누락? ConfigMap/Secret 마운트 확인
│  │  ├─ DB 연결 실패? → NetworkPolicy egress 확인
│  │  └─ 의존 서비스 미준비? → initContainer 또는 startup probe 확인
│  │
│  ├─ Error (exitCode 137)
│  │  ├─ OOMKilled 아닌 SIGKILL → node eviction 또는 preemption
│  │  ├─ kubectl get events --sort-by='.lastTimestamp' 확인
│  │  └─ node memory pressure? kubectl top nodes
│  │
│  └─ Error (exitCode 143)
│     ├─ SIGTERM → graceful shutdown 실패
│     ├─ terminationGracePeriodSeconds 확인 (기본 30s)
│     └─ preStop hook 타임아웃 확인
│
├─ STEP 2: 최근 변경 확인
│  ├─ ArgoCD sync 이력 확인
│  ├─ ConfigMap/Secret 변경 여부
│  └─ Image tag 변경 여부
│
└─ STEP 3: 리소스 상태 확인
   ├─ kubectl top pod (CPU/Memory 사용량)
   ├─ kubectl get events -n <ns> --sort-by='.lastTimestamp'
   └─ node 리소스 압박: kubectl describe node | grep -A5 Conditions
```

---

## 2. ImagePullBackOff

```
ImagePullBackOff 감지
│
├─ kubectl describe pod → Events 확인
│  │
│  ├─ "401 Unauthorized" / "403 Forbidden"
│  │  ├─ ECR: imagePullSecrets 확인, CronJob으로 토큰 갱신 중인지 확인
│  │  ├─ Harbor: Cloudflare WAF 차단? DNS 해석 경로 확인
│  │  └─ Private registry: dockerconfigjson Secret 유효성 확인
│  │
│  ├─ "not found" / "manifest unknown"
│  │  ├─ 이미지 태그 존재 확인: aws ecr describe-images
│  │  ├─ 레포지토리 이름 오타 확인
│  │  └─ kubectl 직접 수정으로 인한 drift? ArgoCD Application 상태 확인
│  │
│  └─ "timeout" / "i/o timeout"
│     ├─ NetworkPolicy egress 확인 (443 port 허용?)
│     ├─ DNS 해결 가능? → nslookup from pod
│     └─ VPC endpoint 또는 NAT Gateway 문제?
│
└─ GitOps drift 확인
   ├─ kubectl 직접 수정 이력? (2026-03-22 사고)
   ├─ ArgoCD sync status: OutOfSync?
   └─ 해결: ArgoCD 기준으로 복원 (kubectl 수정 금지)
```

---

## 3. Pending Pod

```
Pod Pending 감지
│
├─ kubectl describe pod → Events 확인
│  │
│  ├─ "Insufficient cpu/memory"
│  │  ├─ kubectl top nodes → 노드 리소스 여유 확인
│  │  ├─ requests 값 과도? → 적정 수준으로 조정
│  │  └─ 노드 수 부족? → autoscaler 확인 (Karpenter/CA)
│  │
│  ├─ "didn't match Pod's node affinity/selector"
│  │  ├─ nodeSelector 또는 nodeAffinity 확인
│  │  └─ taint/toleration 매칭 확인
│  │
│  ├─ "didn't find available persistent volumes"
│  │  ├─ PVC bound 상태 확인
│  │  ├─ StorageClass provisioner 정상?
│  │  └─ AZ 불일치? (PV와 Pod이 다른 AZ)
│  │
│  └─ "0/N nodes are available: N Unschedulable"
│     ├─ 모든 노드 cordon 상태? kubectl get nodes
│     └─ Kyverno webhook 차단? (kyverno#11122)
│
└─ EKS 특이사항
   ├─ IP 고갈? → WARM_IP_TARGET / WARM_PREFIX_TARGET 확인
   ├─ 서브넷 IP 부족? → /24 서브넷에 prefix delegation 활성화 시 발생
   └─ max-pods 한계? → Bottlerocket user_data 확인
```

---

## 4. NetworkPolicy 트러블슈팅

```
통신 차단 의심
│
├─ STEP 1: NetworkPolicy 존재 확인
│  └─ kubectl get networkpolicy -n <ns>
│     (없으면 NetworkPolicy가 원인 아님)
│
├─ STEP 2: 현재 정책 분석
│  ├─ kubectl describe networkpolicy <name>
│  ├─ ingress 규칙: source pod/namespace 매칭?
│  └─ egress 규칙: destination CIDR/port 매칭?
│
├─ STEP 3: 연결 테스트 (pod 내부에서)
│  ├─ wget -qO- --timeout=3 http://<target>:<port>
│  ├─ nc -zv <target> <port>
│  └─ bash 아닌 sh 환경: /dev/tcp 사용 불가
│
├─ STEP 4: 흔한 누락
│  ├─ kube-api 접근: kubernetes.default.svc ClusterIP + nodePort
│  ├─ DNS: UDP/TCP 53 to kube-dns (CoreDNS)
│  ├─ 외부 DB: ipBlock으로 IP 지정 (호스트명 불가)
│  └─ IMDS: 169.254.169.254 의도적 차단 확인
│
└─ STEP 5: Istio 환경 추가 확인
   ├─ AuthorizationPolicy 차단? → istioctl x authz check <pod>
   ├─ PeerAuthentication mTLS 불일치?
   └─ Envoy stats: kubectl exec <pod> -c istio-proxy -- curl localhost:15000/stats
```

---

## 5. DNS 해결 실패

```
DNS 해결 실패
│
├─ CoreDNS 상태 확인
│  ├─ kubectl get pods -n kube-system -l k8s-app=kube-dns
│  ├─ kubectl logs -n kube-system <coredns-pod> --tail=50
│  └─ CoreDNS OOMKilled? → limits 증가
│
├─ Pod resolv.conf 확인
│  ├─ kubectl exec <pod> -- cat /etc/resolv.conf
│  ├─ ndots 값 확인 (기본 5 → 외부 도메인 해결 시 5회 search 후 시도)
│  └─ 외부 도메인 빈번 시: dnsConfig.options ndots=2 설정 권장
│
├─ NetworkPolicy DNS 허용 확인
│  └─ egress: kube-dns(CoreDNS) namespace + port 53 (UDP+TCP)
│
└─ Istio 환경
   ├─ VirtualService ServiceEntry 필요? (외부 도메인)
   └─ DNS proxy 활성화 여부: istio-proxy가 DNS 가로채는 경우
```

---

## 6. IMDS 접근 검증 (보안)

EKS 환경에서 IMDS(Instance Metadata Service) 차단 확인:

```bash
# Pod 내부에서 테스트
kubectl exec <pod> -n <ns> -- wget -qO- --timeout=3 http://169.254.169.254/latest/meta-data/

# 차단 성공: timeout 또는 connection refused
# 차단 실패: IAM role 정보 노출 → NetworkPolicy egress 추가 필요
```

IMDS v2 강제 + hop limit 1 설정도 병행 권장 (Terraform `http_tokens = "required"`, `http_put_response_hop_limit = 1`).
