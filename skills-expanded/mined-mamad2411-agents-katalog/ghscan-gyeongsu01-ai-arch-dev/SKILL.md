# SKILL.md — Enterprise AI Platform Rules & Tech Stack

> **Version**: 1.0.0  
> **Last Updated**: 2026-02-06  
> **Scope**: Local-K8s 기반 5-Layer AI Platform (RAG → Platform 고도화)

---

## 1. Project Philosophy

### 1.1 Core Principles

| # | Principle | Description |
|---|-----------|-------------|
| P1 | **Platform Engineering First** | 개별 스크립트가 아닌, 재사용 가능한 플랫폼 단위로 설계한다. 모든 기능은 플랫폼 서비스로 노출되어야 한다. |
| P2 | **Container-First** | 모든 컴포넌트(LLM Serving, Vector DB, API, Agent)는 컨테이너 이미지로 패키징하며, 로컬 프로세스 직접 실행을 지양한다. |
| P3 | **IaC (Infrastructure as Code)** | 인프라 설정은 코드(YAML/HCL)로 선언하고, 수동 `kubectl` 조작을 금지한다. 모든 변경은 Git에 커밋된 Manifest/Helm Chart를 통해 반영한다. |
| P4 | **Local-First, Cloud-Hybrid** | AWS 프리티어 비용 한계를 극복하기 위해 **Local K8s(k3d)**를 메인 실행 환경으로 사용하고, AWS 서비스는 최소 연결(Secrets Manager, S3 등)에 한정한다. |
| P5 | **Observability by Default** | 로깅·메트릭·트레이싱은 후속 추가가 아닌, 초기 설계 단계에서 내장한다. |
| P6 | **Immutable Deployments** | 배포된 컨테이너 이미지는 변경하지 않으며, 새 버전은 새 이미지 태그로 릴리스한다. `latest` 태그 사용을 금지한다. |

### 1.2 Design Tenets

```
"If it's not in Git, it doesn't exist."
"If it's not in a container, it doesn't ship."
"If it's not observable, it's not production-ready."
```

---

## 2. Architecture Overview — 5-Layer Model

```
┌─────────────────────────────────────────────────────┐
│  L5  Agent        │ LangGraph Workflow, Tool Use    │
├───────────────────┼─────────────────────────────────┤
│  L4  Service      │ API Gateway, PEP, Guardrails    │
├───────────────────┼─────────────────────────────────┤
│  L3  Data         │ ETL, Vector DB, Metadata Store  │
├───────────────────┼─────────────────────────────────┤
│  L2  Platform     │ K8s, LLM Serving, Cache, Queue  │
├───────────────────┼─────────────────────────────────┤
│  L1  Infra        │ Network, Secrets, CI/CD, Mon.   │
└─────────────────────────────────────────────────────┘
```

**의존성 방향**: L5 → L4 → L3 → L2 → L1 (상위 계층은 하위 계층에만 의존)  
**역방향 의존 금지**: L1이 L4를 직접 참조하는 등의 계층 역전을 허용하지 않는다.

---

## 3. Layer-Specific Rules

### L1 — Infra (기반 환경)

| 항목 | 규칙 |
|------|------|
| **Network** | k3d 클러스터 내 가상 네트워크 격리. Namespace 단위로 환경 분리 (`ai-platform`, `monitoring`, `data`). NetworkPolicy를 통한 Pod 간 트래픽 제어 필수. |
| **Secrets** | K8s `Secret` + `SealedSecrets`(Bitnami) 사용. `.env` 파일은 Git에 절대 커밋하지 않는다. AWS 연동 시 `ExternalSecrets Operator` 허용. |
| **CI/CD** | GitHub Actions를 메인 파이프라인으로 사용. 로컬 검증은 `act` 또는 `Taskfile`로 수행. Helm Chart lint → build → deploy 3단계 파이프라인 필수. |
| **Monitoring** | Prometheus + Grafana 스택을 `monitoring` Namespace에 배포. 모든 서비스는 `/metrics` 엔드포인트를 노출해야 한다. |
| **Logging** | 컨테이너 stdout/stderr → Fluent Bit → Loki 파이프라인. 구조화된 JSON 로그 포맷 강제. |

**허용 기술**: k3d, kubectl, Helm, Kustomize, SealedSecrets, GitHub Actions, Prometheus, Grafana, Loki, Fluent Bit  
**금지 기술**: Terraform Cloud(비용), ArgoCD(Phase 2에서 도입 검토)

---

### L2 — Platform (실행 환경)

| 항목 | 규칙 |
|------|------|
| **K8s Cluster** | k3d 단일 클러스터, 최소 구성: Server 1 + Agent 2. `Traefik` Ingress는 k3d 기본 제공 사용 또는 별도 Ingress Controller 교체 가능. |
| **LLM Serving** | Ollama를 Host에서 실행하고 K8s에서 `ExternalService`로 연결하거나, Ollama 컨테이너를 K8s 내 `DaemonSet`으로 배포. 외부 API(OpenAI/Groq)는 `ConfigMap`으로 엔드포인트 전환 가능해야 한다. |
| **Embedding** | Ollama 임베딩 모델 또는 `sentence-transformers` 서빙 컨테이너. 임베딩 모델 변경 시 Vector DB 재인덱싱 파이프라인 자동 트리거. |
| **Cache** | Redis (Standalone, K8s Deployment). LLM 응답 캐싱 및 세션 상태 저장에 사용. TTL 기본값: 3600초. |
| **Queue** | RabbitMQ (K8s StatefulSet) 또는 Redis Pub/Sub. 비동기 작업(문서 인덱싱, 배치 추론)에 사용. Dead Letter Queue 설정 필수. |

**허용 기술**: k3d, Ollama, Redis, RabbitMQ, Traefik, Nginx Ingress  
**금지 기술**: AWS EKS(비용), 관리형 Redis/MQ(비용)

---

### L3 — Data (데이터 파이프라인)

| 항목 | 규칙 |
|------|------|
| **Vector DB** | ChromaDB를 K8s `Deployment`로 배포. PersistentVolume(hostPath 또는 local-path-provisioner) 필수. 컬렉션 네이밍: `{domain}_{version}` (e.g., `finance_v1`). |
| **ETL Pipeline** | Python 기반 ETL Job을 K8s `Job`/`CronJob`으로 실행. 문서 수집 → 청킹 → 임베딩 → Chroma Upsert 파이프라인. 청킹 전략: `RecursiveCharacterTextSplitter`, chunk_size=1000, overlap=200. |
| **Metadata Store** | SQLite(개발) 또는 PostgreSQL(운영)로 문서 메타데이터 관리. 메타데이터 스키마: `doc_id`, `source`, `chunk_count`, `indexed_at`, `embedding_model`. |
| **Data Versioning** | 데이터 변경 시 컬렉션 버전을 증가시키고, 이전 버전은 최소 1세대 유지 (Blue-Green 인덱싱). |

**허용 기술**: ChromaDB, SQLite, PostgreSQL, LangChain Document Loaders  
**금지 기술**: Pinecone/Weaviate(비용), Spark(오버스펙)

---

### L4 — Service (서비스 계층)

| 항목 | 규칙 |
|------|------|
| **API Gateway** | Kong DB-less 모드 (Declarative Config) 또는 Nginx Ingress Controller. Rate Limiting, Auth(API Key), Request/Response 로깅 필수. |
| **PEP (Policy Enforcement Point)** | OPA(Open Policy Agent) 사이드카 또는 Python 미들웨어로 정책 검증. 정책 정의: Rego 파일 또는 YAML 기반 룰 엔진. |
| **Guardrails** | LLM 입출력 필터링: 프롬프트 인젝션 탐지, PII 마스킹, 응답 길이 제한. Guardrails 위반 시 요청 차단 및 감사 로그 기록. |
| **Observability** | OpenTelemetry SDK로 분산 트레이싱 계측. Trace ID를 모든 요청/응답 헤더에 전파. |
| **API 설계** | RESTful API, OpenAPI 3.0 스펙 필수 작성. 버저닝: URI Path 방식 (`/api/v1/...`). |

**허용 기술**: Kong, Nginx, OPA, OpenTelemetry, FastAPI  
**금지 기술**: AWS API Gateway(비용), Istio(오버스펙)

---

### L5 — Agent (비즈니스 로직)

| 항목 | 규칙 |
|------|------|
| **Workflow Engine** | LangGraph를 Agent 워크플로우 엔진으로 사용. 각 워크플로우는 명확한 상태 머신(State Machine)으로 정의. Graph는 `app/agent/` 디렉토리에 모듈별로 분리. |
| **Tool Use** | Tool은 `app/service/actions/` 아래에 독립 모듈로 구현. 모든 Tool은 `registry.yaml`에 등록되어야 하며, 미등록 Tool 호출은 차단. Tool 실행 결과는 구조화된 `ToolResult` 타입으로 반환. |
| **Business Logic** | 도메인별 비즈니스 로직은 Agent Graph 내 노드(Node)로 캡슐화. 외부 서비스 호출은 반드시 L4 Service Layer를 경유. |
| **Testing** | 모든 Agent 워크플로우에 대해 단위 테스트(Mock LLM) + 통합 테스트(실제 LLM) 작성. 테스트 커버리지 목표: 80% 이상. |

**허용 기술**: LangGraph, LangChain, OpenAI SDK, Pydantic  
**금지 기술**: AutoGen(복잡도), CrewAI(벤더 종속)

---

## 4. Tech Stack Table

| Layer | Category | Technology | Deployment | Notes |
|-------|----------|-----------|------------|-------|
| **L1** | K8s Runtime | k3d (K3s in Docker) | Local | Server 1 + Agent 2 기본 구성 |
| **L1** | Secrets | SealedSecrets | K8s CRD | Bitnami SealedSecrets Controller |
| **L1** | CI/CD | GitHub Actions | Cloud | `act`으로 로컬 검증 |
| **L1** | Monitoring | Prometheus + Grafana | K8s (Helm) | `kube-prometheus-stack` Chart |
| **L1** | Logging | Fluent Bit + Loki | K8s (Helm) | JSON 구조화 로그 |
| **L2** | LLM Serving | Ollama | Host / K8s | `ExternalService` 또는 `DaemonSet` |
| **L2** | LLM API | OpenAI / Groq | External | `ConfigMap` 기반 엔드포인트 전환 |
| **L2** | Cache | Redis 7.x | K8s Deployment | Standalone 모드 |
| **L2** | Queue | RabbitMQ 3.x | K8s StatefulSet | Management Plugin 활성화 |
| **L3** | Vector DB | ChromaDB | K8s Deployment | PV 필수, `local-path-provisioner` |
| **L3** | Metadata | SQLite / PostgreSQL | K8s / Embedded | 개발: SQLite, 운영: PostgreSQL |
| **L3** | ETL | Python (LangChain) | K8s Job/CronJob | 문서 수집·청킹·인덱싱 |
| **L4** | API Gateway | Kong DB-less | K8s Deployment | Declarative Config (`kong.yaml`) |
| **L4** | Policy Engine | OPA | K8s Sidecar | Rego 기반 정책 정의 |
| **L4** | Tracing | OpenTelemetry | SDK + Collector | Jaeger 또는 Grafana Tempo 백엔드 |
| **L4** | API Framework | FastAPI | K8s Deployment | OpenAPI 3.0 자동 생성 |
| **L5** | Agent Framework | LangGraph | K8s Deployment | 상태 머신 기반 워크플로우 |
| **L5** | Tool Registry | Custom (YAML) | App-level | `registry.yaml` 기반 도구 관리 |
| **L5** | LLM SDK | LangChain / OpenAI | App-level | 멀티 프로바이더 지원 |

---

## 5. Coding Convention

### 5.1 Infrastructure (YAML / Helm)

```yaml
# ── 파일 네이밍 ──
# K8s Manifest:  {resource}-{name}.yaml       (e.g., deployment-chromadb.yaml)
# Helm Values:   values-{env}.yaml            (e.g., values-local.yaml)
# Kustomize:     kustomization.yaml           (표준명 고정)

# ── YAML 스타일 ──
# - 들여쓰기: 2 spaces (탭 금지)
# - 주석: 리소스 목적·의존성 명시
# - Label 필수:
#     app.kubernetes.io/name: <name>
#     app.kubernetes.io/component: <layer>     # l1-infra | l2-platform | l3-data | l4-service | l5-agent
#     app.kubernetes.io/managed-by: helm
#     app.kubernetes.io/version: <semver>
```

**Helm Chart 구조** (표준):

```
helm/
├── ai-platform/                  # Umbrella Chart
│   ├── Chart.yaml
│   ├── values.yaml               # 기본값
│   ├── values-local.yaml         # 로컬 오버라이드
│   └── templates/
│       ├── _helpers.tpl
│       ├── namespace.yaml
│       └── ...
├── charts/                       # Sub-Charts
│   ├── chromadb/
│   ├── redis/
│   ├── rabbitmq/
│   ├── kong/
│   └── app/
```

**K8s Manifest 규칙**:

| 규칙 | 설명 |
|------|------|
| Resource Limits | 모든 Pod에 `requests`/`limits` 명시 필수 |
| Health Checks | `livenessProbe` + `readinessProbe` 필수 |
| Security Context | `runAsNonRoot: true`, `readOnlyRootFilesystem: true` 기본 적용 |
| Image Tag | `latest` 금지, SemVer 또는 SHA 태그 사용 |
| ConfigMap vs Secret | 민감 정보는 반드시 `Secret`, 설정값은 `ConfigMap` |

---

### 5.2 Backend (Python)

```python
# ── 기본 설정 ──
# Python Version: 3.11+
# Package Manager: uv (pyproject.toml)
# Formatter: ruff format
# Linter: ruff check
# Type Checker: pyright (strict mode)

# ── 스타일 가이드 ──
# - PEP 8 준수 (ruff 기본 룰셋)
# - Line Length: 120자
# - Import 순서: stdlib → third-party → local (isort 호환)
# - Docstring: Google Style
# - Type Hints: 모든 함수 시그니처에 필수

# ── 예시 ──
from typing import Any

from pydantic import BaseModel, Field


class ToolResult(BaseModel):
    """Tool 실행 결과를 캡슐화하는 표준 모델."""

    tool_name: str = Field(..., description="실행된 Tool 이름")
    success: bool = Field(default=True, description="실행 성공 여부")
    data: dict[str, Any] = Field(default_factory=dict, description="결과 데이터")
    error: str | None = Field(default=None, description="에러 메시지")
```

**Python 프로젝트 룰**:

| 규칙 | 설명 |
|------|------|
| Config 관리 | `pydantic-settings`로 환경별 설정 로드. 하드코딩 금지. |
| 에러 처리 | 도메인별 커스텀 Exception 정의. bare `except` 금지. |
| 로깅 | `structlog` 사용, JSON 포맷 출력. `print()` 디버깅 금지. |
| 비동기 | I/O 바운드 작업은 `asyncio` 기반. FastAPI 라우터는 `async def` 기본. |
| 테스트 | `pytest` + `pytest-asyncio`. Fixture로 의존성 주입. |
| 의존성 주입 | FastAPI `Depends()` 또는 `dependency-injector` 패턴 활용. |

---

### 5.3 Directory Structure (Target)

```
ai-arch-dev/
├── Rules/
│   └── SKILL.md                  # 본 문서
├── app/                          # L5 Agent + L4 Service 소스 코드
│   ├── agent/                    # LangGraph 워크플로우
│   ├── common/                   # 공통 타입, 유틸
│   ├── data/                     # L3 Data 접근 계층
│   ├── infra/                    # L2 인프라 클라이언트 (Redis, Queue 등)
│   ├── platform/                 # 감사, 정책 엔진
│   ├── service/                  # L4 서비스 라우팅, 도구 레지스트리
│   └── main.py                   # FastAPI 엔트리포인트
├── helm/                         # Helm Charts (IaC)
│   ├── ai-platform/              # Umbrella Chart
│   └── charts/                   # Sub-Charts
├── k8s/                          # Raw K8s Manifests (Kustomize)
│   ├── base/                     # 기본 리소스
│   └── overlays/                 # 환경별 오버레이 (local, staging)
├── scripts/                      # 클러스터 부트스트랩, 유틸 스크립트
│   ├── bootstrap-cluster.sh      # k3d 클러스터 생성
│   └── seed-data.sh              # 초기 데이터 로드
├── tests/                        # 테스트
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker/                       # Dockerfile 모음
│   ├── app.Dockerfile
│   └── etl.Dockerfile
├── .github/
│   └── workflows/                # CI/CD 파이프라인
├── pyproject.toml
└── Taskfile.yaml                 # 로컬 태스크 러너
```

---

## 6. Decision Records (Quick Reference)

| Decision | Choice | Rationale |
|----------|--------|-----------|
| K8s Distribution | k3d (K3s in Docker) | 로컬 환경에서 경량, 빠른 클러스터 생성/삭제. Docker-in-Docker 불필요. |
| LLM Runtime | Ollama (Host) | GPU 직접 접근, K8s GPU passthrough 복잡도 회피. ExternalService로 연결. |
| Vector DB | ChromaDB | 기존 코드베이스 호환, 경량, 로컬 개발 용이. K8s Deployment로 전환 용이. |
| Queue | RabbitMQ | Dead Letter Queue, 메시지 지속성, Management UI 제공. Redis Pub/Sub 대비 안정성. |
| API Gateway | Kong DB-less | 선언적 설정, 플러그인 생태계, K8s Ingress Controller 호환. |
| Agent Framework | LangGraph | 상태 머신 기반 제어 흐름, LangChain 생태계 호환, 디버깅 용이. |
| Package Manager | uv | pip 대비 10~100× 빠른 의존성 해결. `pyproject.toml` 네이티브 지원. |

---

## 7. Anti-Patterns (금지 사항)

| # | Anti-Pattern | Why |
|---|-------------|-----|
| A1 | 수동 `kubectl apply` 반복 | IaC 원칙 위반. Helm/Kustomize를 통해 배포해야 한다. |
| A2 | `.env` 파일 Git 커밋 | Secrets 유출 위험. SealedSecrets 또는 ExternalSecrets 사용. |
| A3 | `latest` 이미지 태그 | 재현 불가능한 배포. SemVer 또는 Git SHA 태그 사용. |
| A4 | 계층 간 직접 의존 (L5 → L2 bypass) | 계층 격리 위반. 반드시 인접 계층을 경유해야 한다. |
| A5 | `print()` 디버깅 | 구조화된 로깅(`structlog`)으로 대체해야 한다. |
| A6 | 하드코딩된 URL/포트 | `ConfigMap` 또는 `pydantic-settings`로 외부화해야 한다. |
| A7 | 테스트 없는 Agent 워크플로우 배포 | 최소 단위 테스트(Mock LLM) 통과 후 머지 허용. |

---

## 8. Glossary

| Term | Definition |
|------|-----------|
| **PEP** | Policy Enforcement Point — 정책 검증 지점 |
| **IaC** | Infrastructure as Code — 코드 기반 인프라 관리 |
| **k3d** | K3s-in-Docker — Docker 컨테이너 내에서 K3s 클러스터를 실행하는 도구 |
| **OPA** | Open Policy Agent — 범용 정책 엔진 |
| **Guardrails** | LLM 입출력에 대한 안전성 검증 레이어 |
| **SealedSecrets** | 암호화된 K8s Secret으로, Git 커밋이 안전한 형태 |
| **Blue-Green Indexing** | 새 인덱스를 별도 컬렉션에 빌드한 뒤 트래픽을 전환하는 무중단 인덱싱 전략 |

## 9. Installation Log (Local-K8s)
- **Cluster**: `k3d cluster create ai-cluster --servers 1 --agents 2`
- **Namespace**: `kubectl create namespace ai-platform`
