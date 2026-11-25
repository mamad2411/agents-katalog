---
name: devops-core
description: "Guía principal de DevOps y SRE. Cubre principios DevOps, 12-factor app, GitOps, métricas DORA (deployment frequency, lead time, MTTR, change failure rate), SLO/SLI/SLA, cultura de incidentes blameless, y Platform Engineering. Actívala al diseñar pipelines, evaluar madurez DevOps, o implementar GitOps. Las sub-skills del kit profundizan en dominios específicos."
---

# DevOps Core Guide

Fundamentos DevOps y SRE modernos (2026). Principios que gobiernan todas las sub-skills.

---

## Los 4 indicadores DORA

| Métrica | Elite | High | Medium | Low |
|---------|-------|------|--------|-----|
| **Deployment Frequency** | On-demand (multiple per day) | Once per day to once per week | Once per week to once per month | Once per month or less |
| **Lead Time for Changes** | < 1 hour | 1 day to 1 week | 1 week to 1 month | > 1 month |
| **MTTR** (Mean Time to Restore) | < 1 hour | < 1 day | < 1 week | > 1 week |
| **Change Failure Rate** | < 5% | 5-10% | 10-15% | > 15% |

---

## 12-Factor App (modernizado 2026)

| Factor | Principio | Implementación |
|--------|-----------|----------------|
| **1. Codebase** | Un repo por app, múltiples deploys | Monorepo con Turborepo/Nx bien configurado |
| **2. Dependencies** | Declaradas y aisladas | `uv.lock`, `pnpm-lock.yaml`, `package-lock.json` |
| **3. Config** | En entorno, no en código | Pydantic Settings, Zod + dotenv, `appsettings.json` |
| **4. Backing services** | Recursos externos como URLs | Connection strings en env vars |
| **5. Build, release, run** | Separación estricta | Docker build → push → deploy (GitOps) |
| **6. Processes** | Stateless, share-nothing | Sin session en memoria. Redis para estado. |
| **7. Port binding** | Exportar vía puerto | `EXPOSE 3000`, health check `/health` |
| **8. Concurrency** | Escalar horizontalmente | Kubernetes HPA, réplicas múltiples |
| **9. Disposability** | Arranque rápido, shutdown graceful | SIGTERM handler, readiness probe |
| **10. Dev/prod parity** | Entornos similares | Docker Compose local ≈ producción |
| **11. Logs** | Streams de eventos | stdout/stderr → JSON (pino, structlog) |
| **12. Admin processes** | Tareas administrativas como one-off | `kubectl exec`, migraciones como Job |

---

## GitOps

```
Git Repository (single source of truth)
    │
    ▼
CI Pipeline (build + test + push image)
    │
    ▼
GitOps Agent (ArgoCD / Flux)
    │
    ├──► Dev Cluster
    ├──► Staging Cluster
    └──► Production Cluster
```

**Principio**: toda la configuración de infraestructura y aplicaciones vive en Git. El agente GitOps reconcilia el estado deseado (Git) con el estado real (cluster).

```yaml
# ArgoCD Application
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: miapp-api
spec:
  project: default
  source:
    repoURL: https://github.com/mi-org/infra
    path: apps/miapp-api/overlays/production
    targetRevision: main
  destination:
    server: https://kubernetes.default.svc
    namespace: miapp-prod
  syncPolicy:
    automated:
      prune: true        # Eliminar recursos huérfanos
      selfHeal: true     # Revertir cambios manuales
```

---

## SLO / SLI / SLA

| Término | Definición | Ejemplo |
|---------|-----------|---------|
| **SLI** (Service Level Indicator) | Métrica medida | % de requests con status 2xx / total requests |
| **SLO** (Service Level Objective) | Meta interna | 99.9% de requests exitosos en 30 días |
| **SLA** (Service Level Agreement) | Contrato con cliente (consecuencias) | 99.5% o crédito del 10% |

```yaml
# Error budget: 100% - SLO = presupuesto para fallos
# SLO 99.9% mensual → error budget = 0.1% = 43.2 minutos/mes de downtime permitido
# Si el error budget se agota → freeze de features, enfocar en reliability
```

---

## Platform Engineering

```
Internal Developer Platform (IDP)
    │
    ├── Backstage / Port (service catalog)
    ├── CI/CD templates (GitHub Actions reusable workflows)
    ├── Infrastructure templates (Helm charts, Terraform modules)
    ├── Observability (logs, metrics, traces out-of-the-box)
    └── Secrets (Vault injection automático)
```

**Objetivo**: que un developer despliegue un servicio nuevo en < 1 día sin conocer Kubernetes.

---

## Incidentes blameless

```
Incidente detectado
  → Declarar incidente (P1/P2/P3)
  → Resolver (MTTR es prioridad, no la causa raíz)
  → Postmortem blameless:
      - ¿Qué pasó? (timeline)
      - ¿Qué impacto tuvo?
      - ¿Cómo se detectó? (¿por qué no lo detectó el monitoring?)
      - ¿Cómo se resolvió?
      - Action items (no asignar culpa)
```

---

## Sub-skills del kit

> 📁 Cada sub-skill tiene su guía detallada en `./{nombre}/GUIDE.md`. Usa `read` para cargarla cuando el tema lo requiera.


| Skill | Cuándo cargarla |
|-------|-----------------|
| `devops-docker` | Docker v29, multi-stage, BuildKit, Kaniko, seguridad de imágenes |
| `devops-kubernetes` | K8s 1.36, Helm, ArgoCD, pods, networking |
| `devops-cicd` | GitHub Actions, progressive delivery, canary, blue-green |
| `devops-monitoring` | OpenTelemetry, Prometheus, Grafana, alerting, SLO |
| `devops-iac` | OpenTofu 1.12, Terraform, Pulumi, Bicep |
| `devops-security` | Cosign, Vault, Trivy, RBAC, network policies |
| `devops-cloud` | AWS/GCP/Azure, FinOps, serverless, cost optimization |

---

## Checklist DevOps

- [ ] DORA metrics visibles para el equipo
- [ ] 12-factor app: config en entorno, stateless, logs a stdout
- [ ] GitOps con ArgoCD o Flux (no `kubectl apply` manual)
- [ ] SLO definidos con error budget monitoreado
- [ ] CI/CD pipeline con lint → test → build → push → deploy automático
- [ ] Health checks (liveness + readiness) en todos los servicios
- [ ] Postmortems blameless documentados
- [ ] Codebase única por servicio (un repo = un deployable)
