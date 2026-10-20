---
name: cloud-k8s-provisioning
description: |
  Use when provisioning cloud Kubernetes clusters on GCP (GKE), Azure (AKS), or Oracle Cloud (OKE).

  Triggers for: setting up production Kubernetes infrastructure, deploying clusters with free tier credits,
  configuring cloud-managed K8s environments, or when user specifies GCP/Azure/Oracle Cloud deployment.

  NOT for: local Kubernetes (use Minikube/kind instead), bare metal clusters, or managed K8s
  platforms other than GKE/AKS/OKE.
---

# Cloud Kubernetes Provisioning

Automates provisioning of production-ready Kubernetes clusters on major cloud providers with post-setup infrastructure (Ingress, cert-manager, Dapr, Kafka, Monitoring).

## Supported Providers

1. **Google Cloud (GKE)** - $300 credit, 90 days
2. **Azure (AKS)** - $200 credit, 30 days
3. **Oracle Cloud (OKE)** - Always Free ⭐ Recommended

## Workflow

### 1. Choose Provider

Ask user to select provider:
- GCP (GKE) - Best for high-performance production
- Azure (AKS) - Best for enterprise integration
- Oracle Cloud (OKE) - Best for zero-cost dev/test

### 2. Provision Cluster

Run provider-specific script with user-supplied configuration:

**GKE:**
```bash
# Export configuration
export PROJECT_ID="my-project"
export CLUSTER_NAME="todo-cluster"
export REGION="us-central1"
export NODE_COUNT=3
export MIN_NODES=3
export MAX_NODES=10
export MACHINE_TYPE="n1-standard-2"

# Run provisioning
bash scripts/provision_gke.sh
```

**AKS:**
```bash
# Export configuration
export RESOURCE_GROUP="todo-rg"
export CLUSTER_NAME="todo-cluster"
export LOCATION="eastus"
export NODE_COUNT=3
export MIN_NODES=3
export MAX_NODES=10
export NODE_VM_SIZE="Standard_D2s_v3"

# Run provisioning
bash scripts/provision_aks.sh
```

**OKE (Always Free):**
```bash
# For OKE Always Free, use OCI Console (GUI-based)
bash scripts/provision_oke.sh  # Provides instructions
```

### 3. Post-Cluster Setup

After cluster provisioning completes, run post-setup to install:
- NGINX Ingress Controller
- cert-manager with Let's Encrypt
- Dapr runtime
- Kafka (Strimzi operator)
- Prometheus + Grafana monitoring

```bash
export EMAIL="your-email@example.com"
bash scripts/post_setup.sh
```

### 4. Create Secrets

```bash
export NAMESPACE="production"
bash scripts/create_secrets.sh
```

Prompts for:
- Database connection string
- Kafka bootstrap servers
- JWT secret
- OpenAI API key

### 5. Verify Cluster

```bash
bash scripts/verify_cluster.sh
```

Checks:
- Cluster connectivity
- Node readiness
- Ingress external IP
- cert-manager status
- Dapr installation
- Kafka cluster readiness
- Monitoring stack

### 6. Deploy Application

After verification, user can deploy application manifests:
```bash
kubectl apply -f k8s/deployments/
```

## Configuration Parameters

| Parameter | GKE | AKS | OKE | Default |
|-----------|-----|-----|-----|---------|
| Cluster Name | ✓ | ✓ | ✓ | `todo-cluster` |
| Region/Location | ✓ | ✓ | ✓ | `us-central1` / `eastus` |
| Node Count | ✓ | ✓ | ✓ | 3 |
| Min Nodes | ✓ | ✓ | - | 3 |
| Max Nodes | ✓ | ✓ | - | 10 |
| Machine Type | ✓ | ✓ | ✓ | `n1-standard-2` / `Standard_D2s_v3` / `VM.Standard.E2.1.Micro` |

## Cost Optimization

**GKE:**
- Use preemptible VMs for dev: `--preemptible`
- Enable autoscaler to scale down
- Delete cluster when not in use

**AKS:**
- Use B-series VMs for dev/test
- Enable cluster autoscaler
- Use spot instances for fault-tolerant workloads

**OKE (Always Free):**
- Use VM.Standard.E2.1.Micro shape
- Maximum 2 nodes (Always Free limit)
- Monitor resource usage to stay within limits

## Cleanup

```bash
export PROVIDER="gcp"  # or "azure" or "oracle"
bash scripts/cleanup.sh
```

**WARNING:** This permanently deletes the cluster and all resources.

## Verification Checklist

After running all scripts, verify:
- ✅ Cluster accessible via kubectl
- ✅ All nodes in Ready state
- ✅ Ingress controller has external IP
- ✅ cert-manager pods running
- ✅ ClusterIssuer configured
- ✅ Dapr control plane ready
- ✅ Kafka cluster in Ready state
- ✅ Monitoring stack operational
- ✅ Secrets created in target namespace

## Common Issues

**Ingress External IP Pending:**
- Wait 5-10 minutes for cloud load balancer provisioning
- Check: `kubectl get svc -n ingress-nginx`

**Kafka Not Ready:**
- Check Strimzi operator logs
- Verify storage provisioning
- May take 5-10 minutes to fully initialize

**cert-manager Challenges Failing:**
- Ensure DNS points to Ingress external IP
- Check: `kubectl get challenges`
- Verify ClusterIssuer configuration

## Next Steps

After cluster provisioning:
1. Configure DNS to point to Ingress external IP
2. Deploy application manifests
3. Create Ingress resources with TLS
4. Set up monitoring dashboards
5. Configure backup strategy

## Reference

See `references/provider_comparison.md` for detailed provider comparison and free tier details.
