---
name: managing-diagrams
description: |
  Use when generating cloud architecture diagrams as code — creating, modifying,
  or reviewing infrastructure diagrams using the Python Diagrams library.
  Covers AWS, Azure, GCP, Kubernetes, on-premises, and SaaS provider nodes.
  Generates PNG/SVG architecture diagrams from Python code with Graphviz rendering.
connection_type: diagrams
preload: false
---

# Diagrams — Architecture as Code

Generate cloud architecture diagrams programmatically using Python. Supports 15+ providers including AWS, Azure, GCP, Kubernetes, and on-premises infrastructure.

**Repository**: [github.com/mingrammer/diagrams](https://github.com/mingrammer/diagrams)

## Prerequisites

```bash
# Check installation
python3 -c "import diagrams; print(f'diagrams {diagrams.__version__}')" 2>/dev/null || echo "NOT INSTALLED"
dot -V 2>/dev/null || echo "Graphviz NOT INSTALLED"

# Install if needed
pip install diagrams
# macOS: brew install graphviz
# Ubuntu: apt-get install graphviz
```

## Decision Matrix

| Need | Approach | Example |
|------|----------|---------|
| Simple 3-tier architecture | Single Diagram context | `with Diagram("Web App"):` |
| Grouped components | Cluster context | `with Cluster("VPC"):` |
| Multiple environments | Nested Clusters | `with Cluster("Prod"): with Cluster("AZ-1"):` |
| Data flow direction | Edge operators | `web >> cache >> db` |
| Bidirectional flow | Double edge | `web >> Edge(label="gRPC") << api` |
| Multiple outputs | Edge from list | `[svc1, svc2] >> lb` |
| Custom styling | Edge attributes | `Edge(color="red", style="dashed")` |

## Phase 1 — Discovery

Identify what architecture to diagram:

```python
#!/usr/bin/env python3
"""List all available node providers and categories."""
import diagrams
from diagrams import aws, azure, gcp, k8s, onprem, saas, generic, programming, c4

# List available providers
providers = {
    "aws": dir(aws),
    "azure": dir(azure),
    "gcp": dir(gcp),
    "k8s": dir(k8s),
    "onprem": dir(onprem),
    "saas": dir(saas),
    "generic": dir(generic),
    "programming": dir(programming),
    "c4": dir(c4),
}

for provider, modules in providers.items():
    categories = [m for m in modules if not m.startswith("_")]
    print(f"{provider}: {', '.join(categories[:10])}...")
```

## Phase 2 — Generate Diagram

### AWS Architecture Example

```python
#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, Lambda
from diagrams.aws.database import RDS, ElastiCache
from diagrams.aws.network import ELB, CloudFront, Route53
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.security import WAF

with Diagram("Production Architecture", show=False, direction="LR"):
    dns = Route53("DNS")
    cdn = CloudFront("CDN")
    waf = WAF("WAF")

    with Cluster("VPC"):
        lb = ELB("ALB")

        with Cluster("Application Tier"):
            svc = [ECS("service-1"), ECS("service-2"), ECS("service-3")]

        with Cluster("Data Tier"):
            db = RDS("PostgreSQL")
            cache = ElastiCache("Redis")

        with Cluster("Async Processing"):
            queue = SQS("task-queue")
            worker = Lambda("processor")
            events = SNS("notifications")

    storage = S3("assets")

    dns >> cdn >> waf >> lb >> svc
    svc >> cache >> db
    svc >> queue >> worker >> events
    cdn >> storage
```

### Kubernetes Architecture Example

```python
#!/usr/bin/env python3
from diagrams import Diagram, Cluster
from diagrams.k8s.compute import Pod, Deploy, RS
from diagrams.k8s.network import Ingress, Service
from diagrams.k8s.storage import PV, PVC
from diagrams.k8s.podconfig import ConfigMap, Secret

with Diagram("K8s Deployment", show=False):
    ingress = Ingress("ingress")

    with Cluster("Namespace: production"):
        svc = Service("api-svc")

        with Cluster("Deployment"):
            pods = [Pod("pod-1"), Pod("pod-2"), Pod("pod-3")]

        config = ConfigMap("config")
        secret = Secret("credentials")
        pvc = PVC("data-vol")

    pv = PV("persistent-volume")

    ingress >> svc >> pods
    [config, secret] >> pods
    pvc >> pv
```

### Multi-Cloud / Hybrid Example

```python
#!/usr/bin/env python3
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS
from diagrams.gcp.compute import GKE
from diagrams.azure.compute import AKS
from diagrams.onprem.network import Nginx
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.generic.network import Firewall

with Diagram("Multi-Cloud Architecture", show=False, direction="TB"):
    with Cluster("On-Premises"):
        lb = Nginx("Load Balancer")
        fw = Firewall("Firewall")
        monitoring = [Prometheus("metrics"), Grafana("dashboards")]

    with Cluster("AWS"):
        aws_app = ECS("api-service")

    with Cluster("GCP"):
        gcp_app = GKE("ml-pipeline")

    with Cluster("Azure"):
        az_app = AKS("data-service")

    fw >> lb >> [aws_app, gcp_app, az_app]
    [aws_app, gcp_app, az_app] >> Edge(style="dashed") >> monitoring[0]
```

## Available Providers

| Provider | Import | Key Categories |
|----------|--------|----------------|
| AWS | `diagrams.aws` | compute, database, network, storage, security, integration, analytics, ml |
| Azure | `diagrams.azure` | compute, database, network, storage, security, integration, analytics, ml |
| GCP | `diagrams.gcp` | compute, database, network, storage, security, analytics, ml |
| Kubernetes | `diagrams.k8s` | compute, network, storage, podconfig, rbac, ecosystem |
| On-Premises | `diagrams.onprem` | compute, database, network, monitoring, queue, ci, container |
| SaaS | `diagrams.saas` | alerting, analytics, chat, identity, logging, media, social |
| Generic | `diagrams.generic` | compute, database, network, os, storage, place |
| Programming | `diagrams.programming` | framework, language, runtime |
| C4 | `diagrams.c4` | SystemBoundary, Container, Database, Person, Relationship |

## Diagram Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `name` | required | Diagram title (also used as filename) |
| `show` | `True` | Auto-open after generation. Set `False` for scripts |
| `direction` | `"LR"` | Layout: `LR`, `RL`, `TB`, `BT` |
| `filename` | from name | Override output filename |
| `outformat` | `"png"` | `png`, `jpg`, `svg`, `pdf`, `dot` |
| `graph_attr` | `{}` | Graphviz graph attributes |
| `node_attr` | `{}` | Graphviz node attributes |
| `edge_attr` | `{}` | Graphviz edge attributes |

## Anti-Hallucination Rules

- **NEVER** import a node class without verifying it exists — use `dir(diagrams.aws.compute)` to check
- **NEVER** assume provider category names — they differ across providers (e.g., `aws.integration` vs `gcp.api`)
- **ALWAYS** set `show=False` in scripts/automation to prevent auto-opening
- **ALWAYS** verify Graphviz is installed before generating — diagrams silently fails without it

## Output Format

```
Diagrams Report
═══════════════
Generated: [filename].png
Provider: [aws/gcp/azure/k8s/multi-cloud]
Components: [count] nodes, [count] clusters
Layout: [direction]

File: [absolute path to generated image]
```

## Common Pitfalls

- **Missing Graphviz**: `pip install diagrams` does NOT install Graphviz — install separately
- **show=True in CI**: Will fail in headless environments — always use `show=False`
- **Large diagrams**: Use `direction="LR"` and clusters to keep readable
- **Node naming**: Node labels appear in diagram — keep short and descriptive
- **Edge direction**: `>>` means left-to-right flow; `<<` means reverse; order matters
