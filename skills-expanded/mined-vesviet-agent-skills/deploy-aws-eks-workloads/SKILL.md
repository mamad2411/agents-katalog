---
name: deploy-aws-eks-workloads
description: Deploy, scale, and govern cloud-native application workloads on Amazon EKS using SOTA 2026-2027 AWS standards. Use when configuring Karpenter v1.0+ declarative NodePools, EKS Pod Identity associations, AWS VPC Lattice Gateway API routes, ADOT telemetry pipelines, ECR image verification, and GitOps delivery pipelines on AWS.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
version: "1.0.0"
---

# Deploy AWS EKS Workloads

Use this skill when deploying, configuring, and governing production Kubernetes workloads on Amazon EKS in accordance with 2026–2027 AWS Cloud-Native standards.

## When to Use

- deploying containerized applications and microservices to Amazon EKS via GitOps
- configuring declarative node autoscaling via Karpenter v1.0+ (`NodePool` and `EC2NodeClass`)
- establishing IAM credentials for pods using AWS EKS Pod Identity (replacing legacy IRSA)
- setting up sidecarless cross-VPC service communication with AWS VPC Lattice and Kubernetes Gateway API
- synchronizing application secrets from AWS Secrets Manager using External Secrets Operator (ESO)
- instrumenting EKS workloads with AWS Distro for OpenTelemetry (ADOT) and CloudWatch Application Signals
- enforcing supply chain security with Amazon ECR immutable tags, Inspector v2 SBOMs, and AWS Signer

## Core Rules

- **Mandate EKS Pod Identity**: use cluster-level Pod Identity associations (`aws eks create-pod-identity-association`) for all workload ServiceAccounts; eliminate legacy IRSA OIDC trust policy overhead and STS scaling bottlenecks.
- **Karpenter v1.0+ Declarative Autoscaling**: declare workload node requirements using `karpenter.sh/v1` `NodePool` and `karpenter.k8s.aws/v1` `EC2NodeClass`; configure consolidation policy `WhenEmptyOrUnderutilized`, disruption budgets (`budgets: [{nodes: "10%"}]`), Graviton4 (`c8g`, `m8g`), and specialized accelerators (`trn2`, `inf2`, `g6`).
- **Sidecarless VPC Lattice Mesh**: route service traffic through the AWS Gateway API Controller for VPC Lattice (`GatewayClass: amazon-vpc-lattice`) using Kubernetes Gateway API `HTTPRoute` objects; enforce IAM authorization without proxy sidecar overhead.
- **ECR Supply Chain & Immutable Tags**: pull images exclusively from KMS-encrypted Amazon ECR repositories with immutable tags (`imageTagMutability: IMMUTABLE`); enforce Kyverno admission policies verifying Cosign/AWS Signer signatures and Inspector v2 vulnerability attestations.
- **Declarative Secret Synchronization**: synchronize credentials from AWS Secrets Manager using External Secrets Operator (`ClusterSecretStore` / `ExternalSecret`) authenticated via EKS Pod Identity; never store plaintext or base64 secrets in Git.
- **Standardized ADOT Observability**: deploy AWS Distro for OpenTelemetry (ADOT) Collector with OpenTelemetry GenAI semantic conventions, X-Ray trace context propagation, and CloudWatch Application Signals.
- refer to `references/aws-eks-workload-guide.md` for production YAML manifests, Karpenter CRD configurations, and VPC Lattice gateway specs.

## Suggested Process

### 1. Configure EKS Pod Identity
Bind the target Kubernetes ServiceAccount to an AWS IAM Role via EKS Pod Identity:
```bash
aws eks create-pod-identity-association \
  --cluster-name production-eks-cluster \
  --namespace checkout \
  --service-account checkout-service-sa \
  --role-arn arn:aws:iam::123456789012:role/CheckoutServiceWorkloadRole
```

### 2. Declare Karpenter v1.0 NodePool & EC2NodeClass
Define workload compute provisioning with automated consolidation and disruption limits:
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata:
  name: checkout-workloads
spec:
  template:
    spec:
      nodeClassRef:
        group: karpenter.k8s.aws
        kind: EC2NodeClass
        name: default-al2023
      requirements:
        - key: karpenter.sh/capacity-type
          operator: In
          values: ["on-demand", "spot"]
        - key: kubernetes.io/arch
          operator: In
          values: ["arm64", "amd64"]
        - key: karpenter.k8s.aws/instance-family
          operator: In
          values: ["c8g", "m8g", "c7g", "m7g"]
  disruption:
    consolidationPolicy: WhenEmptyOrUnderutilized
    consolidateAfter: 1m
    budgets:
      - nodes: 10%
```

### 3. Synchronize Secrets via External Secrets Operator
Declare an `ExternalSecret` retrieving credentials from AWS Secrets Manager using the Pod Identity-backed SecretStore:
```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: checkout-database-credentials
  namespace: checkout
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secretsmanager-pod-id
    kind: ClusterSecretStore
  target:
    name: checkout-db-secret
    creationPolicy: Owner
  data:
    - secretKey: DB_PASSWORD
      remoteRef:
        key: production/checkout/database
        property: password
```

### 4. Deploy Workload via GitOps & ArgoCD
Commit Kustomize overlays and workload manifests to the GitOps repository. Deploy via ArgoCD enforcing Server-Side Apply (`syncOptions: [ServerSideApply=true]`).

### 5. Expose Workload via VPC Lattice HTTPRoute
Expose microservice endpoints across VPCs without sidecars using Kubernetes Gateway API:
```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: checkout-route
  namespace: checkout
spec:
  parentRefs:
    - name: vpc-lattice-gateway
      sectionName: http
  rules:
    - matches:
        - path:
            type: PathPrefix
            value: /api/v1/checkout
      backendRefs:
        - name: checkout-service
          port: 8080
```

### 6. Verify Deployment & Observability
Check pod status, Pod Identity credential mounts (`AWS_CONTAINER_CREDENTIALS_FULL_URI`), ADOT trace exports in AWS X-Ray, and CloudWatch Application Signals SLO metrics.

## Checklist

- [ ] Verify EKS Pod Identity association is created for the target ServiceAccount (`aws eks create-pod-identity-association`)
- [ ] Confirm Karpenter v1.0+ NodePool specifies `WhenEmptyOrUnderutilized` consolidation and disruption budget
- [ ] Ensure ExternalSecret targets Secrets Manager via Pod Identity SecretStore with zero credentials in Git
- [ ] Validate container image is pulled from KMS-encrypted ECR with immutable tags and Kyverno verification
- [ ] Verify Kubernetes Gateway API HTTPRoute is bound to VPC Lattice gateway without proxy sidecar injection
- [ ] Confirm ADOT Collector is exporting traces to AWS X-Ray and emitting CloudWatch Application Signals metrics

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/deployment-plan.json** — Required fields: `contract_type`, `version` (deployed manifest revision), `environments[]`, `steps[]` (each with `order`, `action`, `is_destructive` — Pod Identity association, NodePool apply, GitOps sync, HTTPRoute exposure), and `rollback_plan`. Populate `gitops_compliance` with the ArgoCD `ServerSideApply=true` sync options and `supply_chain_security` with the ECR immutable-tag and Kyverno/Cosign verification state.
- Include credential-mount, HTTPRoute binding, and ADOT/X-Ray export evidence in the `verification` field so SRE and Technical Lead can validate the rollout without re-probing the cluster.
- Skip emission for local dry runs that do not cross a role boundary.

## Failure Modes

- **IRSA fallback**: a workload falls back to legacy IRSA OIDC annotations, reintroducing STS scaling bottlenecks. Mitigation: create an EKS Pod Identity association for every workload ServiceAccount; reject manifests carrying `eks.amazonaws.com/role-arn` annotations.
- **Secret committed to Git**: a database password lands as plaintext or base64 in a Kustomize overlay. Mitigation: synchronize only via `ExternalSecret` backed by the Pod Identity-authenticated `ClusterSecretStore`; scan the GitOps repo for secret material.
- **Karpenter disruption storm**: `WhenEmptyOrUnderutilized` consolidation without a disruption budget evicts a large share of nodes at once under spot churn. Mitigation: declare `budgets: [{nodes: "10%"}]` and a `consolidateAfter` delay in every NodePool.
- **Mutable image tag**: a workload references `:latest` or a mutable ECR tag, so rollback cannot reproduce the running artifact. Mitigation: enforce `imageTagMutability: IMMUTABLE`, pin image digests, and gate admission on Kyverno Cosign/AWS Signer verification.
- **Over-privileged Pod Identity role**: the association grants a broad managed policy far beyond the workload's actual AWS calls. Mitigation: scope each role to the minimum actions of its workload; audit association role ARNs during review.
- **Client-side apply conflict**: ArgoCD syncs without `ServerSideApply=true`, clobbering fields managed by Karpenter and other controllers. Mitigation: set `syncOptions: [ServerSideApply=true]` on the ArgoCD application.
- **Telemetry gap**: ADOT is deployed but X-Ray receives no traces and Application Signals shows no SLO metrics, yet the deploy is reported done. Mitigation: verify trace export and SLO metrics in the verification step before closing the rollout.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: a Pod Identity association grants the workload ServiceAccount an IAM role broader than its actual AWS calls. Mitigation: least-privilege roles per ServiceAccount; review every `create-pod-identity-association` role ARN for scope creep.
- **ASI04 Supply Chain**: images pulled from outside the KMS-encrypted, immutable-tag ECR repositories, or lacking signatures. Mitigation: pull exclusively from ECR with `imageTagMutability: IMMUTABLE`; enforce Kyverno `verifyImages` checks on Cosign/AWS Signer signatures and Inspector v2 attestations.
- **ASI05 RCE Guard**: GitOps renders manifests from repository content, so untrusted PR templates or injected env values become cluster state. Mitigation: validate rendered manifests against Kyverno policies and CEL rules before sync; never render manifest fields directly from unreviewed external input.
- **ASI07 Inter-Agent Communication**: the rollout is consumed by Project Manager, SRE, and Technical Lead. Mitigation: emit the schema-validated `deployment-plan.json` with `gitops_compliance` and `verification` populated so downstream roles validate without cluster access.
- **ASI08 Cascading Failures**: Karpenter node consolidation concurrent with a GitOps rollout cascades into a partial outage reported as healthy. Mitigation: disruption budgets plus ArgoCD sync waves; declare rollout failure explicitly to the coordinator instead of propagating partial state.
- **ASI09 Human-Agent Trust Exploitation**: declaring the deploy green from `kubectl get pods` alone while credential-mount or spot-disruption issues remain. Mitigation: show Pod Identity credential-mount, HTTPRoute binding, and Application Signals evidence; surface spot capacity risk honestly.

## Related Skills

- **setup-deployment**: GitOps delivery pipelines and ArgoCD application manifests
- **aws-infrastructure**: Provisioning foundational AWS resources (VPC, control planes, IAM roles)
- **debug-runtime-platform**: Diagnosing pod crash loops, networking issues, and ephemeral debugging
- **manage-secrets**: Enterprise secret management workflows and credential rotation
- **add-telemetry-instrumentation**: OpenTelemetry Collector pipelines and distributed tracing
