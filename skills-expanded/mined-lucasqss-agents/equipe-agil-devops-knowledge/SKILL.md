---
name: equipe-agil-devops-knowledge
description: Conhecimento específico do DevOps da Equipe Backend Ágil Kanban+XP. Cobre CI/CD em trunk (GitHub Actions / GitLab CI) aplicado à hierarquia pr-* → feature/* do time, build de container e nativo Quarkus (Jib, UBI, multi-stage), Infrastructure as Code (Terraform), GitOps (ArgoCD/Flux), feature flags (Unleash/Togglz/FF4j), Kubernetes patterns essenciais (Deployment/Service/Ingress/HPA/PDB/NetworkPolicy/probes), secrets em CI, Team Topologies (Skelton & Pais), modelo "golden path / paved road" para plataforma interna, deployment patterns (blue/green, canary, rolling). Owner do pipeline da equipe — respeitando que jobs do time só rodam em branches do time. Skill autossuficiente — todo o conteúdo necessário está aqui; não consultar fontes externas.
---

# DevOps — Conhecimento específico

Skill carregada pelo agente `equipe-agil-devops` depois de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`. Cobre o conhecimento necessário para construir e operar o **pipeline da equipe** e a **plataforma de execução** em Java 21 + Quarkus 3, respeitando a hierarquia `pr-*` → `feature/<funcionalidade>` (e o limite de que **integração `feature/*` → `develop` está fora do escopo do time** — vide `xp-baseline` §1.6).

## 1. Conceitos centrais

### 1.1 Mandato do DevOps na equipe

- **Owner técnico do pipeline da equipe** (A/R): commit stage na `pr-*`, acceptance + quality stages na `feature/*`, deploy progressivo em ambiente de feature/preview.
- **Owner técnico da infraestrutura que o time gerencia** (containers, IaC dos ambientes do time, secrets em CI, observabilidade do pipeline).
- **Não confunde com SRE**: DevOps cuida do **fluxo de mudança até o release** (build, integração, deploy). SRE cuida do **comportamento em produção** (SLO, error budget, incidente, capacity). Ambos colaboram no deploy.
- **Não confunde com AppSec**: DevOps **operacionaliza** controles de segurança no pipeline (SAST/SCA/secret scan/IaC scan/container scan), AppSec **define** os controles.
- RACI: A/R em CI/CD da equipe, IaC dos ambientes do time, feature flags ops, golden path interno; C em arquitetura distribuída, observabilidade, segurança.

### 1.2 Stack default

- **CI/CD**: GitHub Actions ou GitLab CI (escolhido pela plataforma corporativa). Pipeline em arquivo declarativo no repo.
- **Build de container**: Jib (`quarkus-container-image-jib`) para JVM; build nativo via `quarkus-maven-plugin` + UBI base image (`registry.access.redhat.com/ubi9-minimal`).
- **Registry**: Harbor / Artifactory / GHCR / GitLab Registry — conforme corporativo.
- **IaC**: Terraform (HCL) para infra cloud; Helm charts ou Kustomize para Kubernetes.
- **GitOps**: ArgoCD ou Flux — estado desejado em git, reconciliado por controller.
- **Feature flags**: Unleash (open source, recomendado) ou Togglz/FF4j para flags in-process.
- **Kubernetes**: a plataforma de execução default (corporativa).
- **Observabilidade do pipeline**: métricas de DORA por job; coletor padrão (Prometheus + dashboard).

### 1.3 Pipeline da equipe — anatomia detalhada

```
┌─────────────────────────────────────────────────────────────────┐
│  ESCOPO DO TIME (branches que o time criou)                     │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  [push em pr-<id>-<slug>]                                       │
│       │                                                          │
│       ▼                                                          │
│  COMMIT STAGE (≤ 10 min — Ten-Minute Build do XP)               │
│   ├── checkout + cache Maven                                    │
│   ├── compile (JVM)                                             │
│   ├── unit tests (JUnit 5 + AssertJ)                            │
│   ├── lint (Checkstyle/Spotless/Sortpom)                        │
│   ├── SAST rápido (Semgrep diff-only)                           │
│   ├── SCA (Dependency-Check / Trivy fs)                         │
│   ├── secret scan no diff (gitleaks)                            │
│   └── ArchUnit                                                  │
│       │ (verde → permite merge na feature/*)                    │
│       ▼                                                          │
│  [merge: pr-* → feature/<funcionalidade>] (squash + rebase)     │
│       │                                                          │
│       ▼                                                          │
│  ACCEPTANCE STAGE                                               │
│   ├── integration tests (Testcontainers Postgres + Kafka)       │
│   ├── REST in-process (RestAssured)                             │
│   ├── contract tests (Pact provider verify)                     │
│   ├── component / e2e da feature                                │
│   ├── build de container (Jib)                                  │
│   ├── container scan (Trivy image)                              │
│   ├── SBOM (CycloneDX) versionado                               │
│   └── IaC scan se aplicável (Checkov/tfsec/Trivy iac)           │
│       │                                                          │
│       ▼                                                          │
│  QUALITY STAGES (paralelos)                                     │
│   ├── perf smoke (Gatling/JMeter — SLA p95)                     │
│   ├── DAST (OWASP ZAP em ambiente de feature)                   │
│   ├── mutation (PIT diff-only nos módulos tocados)              │
│   └── headers de segurança validados                            │
│       │                                                          │
│       ▼                                                          │
│  DEPLOY em AMBIENTE DE FEATURE / PREVIEW                        │
│   ├── push para registry com tag = SHA + feature                │
│   ├── ArgoCD reconcilia manifests do ambiente preview           │
│   ├── feature flags off-by-default em preview                   │
│   └── smoke pós-deploy                                          │
│                                                                  │
│  ╔══════════════════════════════════════════════════════════╗  │
│  ║  feature/<funcionalidade> → develop está FORA do escopo  ║  │
│  ║  do time. Pipeline da equipe NÃO dispara em develop,     ║  │
│  ║  release/*, hotfix/* ou feature/* alheias.               ║  │
│  ╚══════════════════════════════════════════════════════════╝  │
└─────────────────────────────────────────────────────────────────┘
```

**Regra inegociável**: triggers do pipeline da equipe são restritos a `pr-*` e `feature/*` que o time gerencia. Para outras branches, o owner externo é responsável (vide `xp-baseline` §1.6).

### 1.4 GitHub Actions — esqueleto do pipeline do time

```yaml
# .github/workflows/team-pipeline.yml
name: equipe-aco pipeline

on:
  push:
    branches:
      - 'pr-*'
      - 'feature/*'
  pull_request:
    branches:
      - 'feature/*'

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  commit-stage:
    if: startsWith(github.ref_name, 'pr-')
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21', cache: maven }
      - run: ./mvnw -B -ntp -T1C verify -Pcommit-stage
      - run: ./mvnw -B -ntp archunit:check
      - uses: gitleaks/gitleaks-action@v2
      - uses: aquasecurity/trivy-action@master
        with: { scan-type: 'fs', severity: 'CRITICAL,HIGH', exit-code: '1' }

  acceptance-stage:
    if: startsWith(github.ref_name, 'feature/')
    runs-on: ubuntu-latest
    timeout-minutes: 30
    services:
      docker: { image: docker:dind }
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: '21', cache: maven }
      - run: ./mvnw -B -ntp verify -Pacceptance
      - run: ./mvnw -B -ntp cyclonedx:makeAggregateBom
      - run: ./mvnw -B -ntp package -Dquarkus.container-image.build=true
      - uses: aquasecurity/trivy-action@master
        with: { image-ref: ${{ env.IMAGE }}, severity: 'CRITICAL', exit-code: '1' }
```

### 1.5 Build de imagem Quarkus

**JVM mode (default da equipe — boot ~1s, footprint razoável)**:
```properties
quarkus.container-image.builder=jib
quarkus.container-image.group=aco
quarkus.container-image.name=pedidos
quarkus.container-image.tag=${quarkus.application.version}
quarkus.jib.base-jvm-image=registry.access.redhat.com/ubi9/openjdk-21-runtime:latest
quarkus.jib.jvm-arguments=-XX:+UseG1GC,-XX:MaxRAMPercentage=75
```

**Native mode (cold-start crítico, FaaS, escala 0→1)**:
- Custo: build longo (~5-10 min), debug mais difícil, alguns frameworks não suportam.
- Compensa em serverless ou serviços com SLA agressivo de cold-start.
- Comando: `./mvnw package -Pnative -Dquarkus.native.container-build=true`.
- Base UBI mínima: `quarkus.native.builder-image=mandrel` + `quarkus.container-image.builder=docker`.

**Heurística**: default JVM com Jib; native apenas com ASR explícito.

### 1.6 Infrastructure as Code — Terraform

- **Estado**: backend remoto (S3 + DynamoDB lock; GCS; Terraform Cloud). Nunca state local em prod.
- **Estrutura recomendada**:
  ```
  /infra/terraform/
  ├── modules/         ← reusáveis (rds, kafka-topic, k8s-namespace)
  ├── envs/
  │   ├── feature/     ← workspace por feature do time
  │   ├── staging/
  │   └── prod/        ← geralmente fora do escopo do time
  └── pipelines/       ← jobs CI dedicados
  ```
- **Workflow em CI**:
  - `terraform fmt -check` + `terraform validate` no commit stage.
  - `terraform plan` no PR (output como comentário); revisão obrigatória.
  - `terraform apply` apenas após aprovação + merge.
- **Boas práticas**:
  - Módulos pequenos, com input/output declarado.
  - `for_each` em vez de `count` quando possível (resiste melhor a reordenação).
  - Variáveis sensíveis via Vault/SSM, nunca em `.tfvars` versionado.
  - Drift detection periódico (`terraform plan` agendado).

### 1.7 GitOps com ArgoCD/Flux

- **Princípio**: estado desejado da infra (manifests Kubernetes / Helm / Kustomize) vive em git; controller no cluster **reconcilia** continuamente o estado real para o desejado.
- **Benefícios**: auditoria completa via git, rollback = `git revert`, deploy reproduzível, divergência detectada automaticamente.
- **Estrutura**:
  - Repo de **app** (código + Dockerfile + Jib config).
  - Repo de **manifests** (deployment/service/configmap por ambiente) — pode ser o mesmo repo ou separado.
  - Pipeline da `feature/*` faz **bump de tag** no repo de manifests do ambiente preview; ArgoCD detecta e aplica.
- **ApplicationSet** no ArgoCD para multi-ambiente.
- **Sync waves**: ordenar reconciliação (configmap antes do deployment, etc.).

### 1.8 Kubernetes patterns essenciais

| Recurso | O que é | Quando usar |
|---------|---------|-------------|
| **Deployment** | Pods stateless gerenciados | App default Quarkus |
| **StatefulSet** | Pods com identidade estável e PVC | Banco, broker (com cuidado) |
| **Service (ClusterIP)** | Endpoint interno estável | Comunicação intra-cluster |
| **Ingress** | HTTP entry-point | Exposição externa via gateway |
| **HorizontalPodAutoscaler** | Escala horizontal por métrica | CPU/mem/custom metric |
| **PodDisruptionBudget** | Mínimo de pods up em manutenção | `minAvailable: 1` em prod |
| **NetworkPolicy** | Firewall L3/L4 entre pods | Zero-trust intra-cluster |
| **ConfigMap / Secret** | Config / segredo | Config externa; secret via Vault/CSI |
| **PersistentVolumeClaim** | Storage persistente | Stateful workloads |

**Probes Quarkus (obrigatórias)**:
```yaml
livenessProbe:
  httpGet: { path: /q/health/live, port: 8080 }
  initialDelaySeconds: 10
readinessProbe:
  httpGet: { path: /q/health/ready, port: 8080 }
  initialDelaySeconds: 5
startupProbe:
  httpGet: { path: /q/health/started, port: 8080 }
  failureThreshold: 30
  periodSeconds: 2
```

Para nativos: `initialDelaySeconds` menor (boot < 1s).

### 1.9 Deployment patterns (orquestrados pelo time no ambiente de feature)

- **Rolling update** (default Kubernetes) — pods substituídos gradualmente; sem downtime se readiness probe correta. Risco: dois versões coexistem por minutos.
- **Blue/Green** — duas pilhas paralelas; switch instantâneo via Service selector; rollback rápido. Custo: 2× recursos.
- **Canary** — % do tráfego ao novo; aumenta gradualmente; observa métricas. Excelente com Istio/Linkerd ou Argo Rollouts.
- **Shadow / Mirror** — réplica de tráfego para a versão nova sem afetar usuário; só para validação.
- **Feature flag + dark launch** — código em prod desligado por flag; ativa por usuário/percentual em runtime.

Vide `arquiteto-sis-knowledge` §1.18 para uso desses patterns inter-serviço.

### 1.10 Feature flags — operação

**Tipos (recap do `xp-baseline` §1.7)**:
- *Release toggle* — short-lived, separar deploy de release.
- *Experiment toggle* — A/B test.
- *Ops toggle* — kill switch para feature instável.
- *Permission toggle* — entitlement por usuário/tenant.

**Operacionalização**:
- Cada flag tem owner + data de remoção; flag morta vira tarefa de remoção.
- Coverage de teste obrigatório nos **dois caminhos** (on e off).
- Toggle config em ferramenta externa (Unleash) ou via ConfigMap quando trivial.
- Métrica: número de flags ativas; idade da flag mais antiga.

**Quarkus + Togglz exemplo**:
```java
public enum FeatureToggles implements Feature {
    @Label("Novo motor de aprovação")
    NOVO_APROVADOR_PEDIDO;
    public boolean isActive() { return FeatureContext.getFeatureManager().isActive(this); }
}

if (FeatureToggles.NOVO_APROVADOR_PEDIDO.isActive()) {
    novoServico.aprovar(pedido);
} else {
    servicoLegado.aprovar(pedido);
}
```

### 1.11 Secret management no pipeline

- **Nunca** secret em arquivo de pipeline ou variável `env:` versionada.
- GitHub Actions: `secrets.*` (org/repo-level), com proteção por ambiente (environment protection rules).
- GitLab CI: variáveis CI/CD masked + protected.
- Vault: autenticação via OIDC do runner (GitHub OIDC → Vault role).
- Kubernetes: secret via External Secrets Operator ou Vault CSI driver (sem secret em git, mesmo encriptado).
- Rotação: automática para credenciais de banco/cloud (Vault dynamic credentials).

### 1.12 Team Topologies (Skelton & Pais) — perspectiva DevOps

Quatro tipos de time:
- **Stream-aligned** — entrega valor diretamente (a equipe que esta skill serve).
- **Enabling** — coach que ajuda stream-aligned a adquirir capability.
- **Complicated-subsystem** — domínio especialista (ML, criptografia, performance).
- **Platform** — provê **golden path / paved road** para stream-aligned consumir como self-service.

Três modos de interação:
- **Collaboration** — alta-frequência, alto-acoplamento; temporário.
- **X-as-a-Service** — plataforma consome via API/portal; baixo acoplamento.
- **Facilitating** — temporário; enabling team facilita stream-aligned.

**Heurística do DevOps**:
- Não construir plataforma para um time (vira time terceirizado).
- Consumir plataforma corporativa quando existe (golden path).
- Quando plataforma é insuficiente: facilitar evolução dela (collaboration breve), não construir plataforma paralela.

### 1.13 Golden path / paved road

- **Definição**: caminho idiomático, suportado, com tooling completo, que cobre 80% dos casos do time.
- **Características**: docs claros, exemplos copiáveis, atualizações automáticas, suporte humano (canal/owner).
- **Anti-padrão**: forçar uso (vira coerção); caminho difícil de seguir (vira contorno).
- **Boa plataforma**: golden path **fácil**, customização **possível** mas com custo claro.

### 1.14 DORA + DevOps

- **Deployment Frequency** — quantos deploys/dia no ambiente da `feature/*`.
- **Lead Time for Changes** — do commit em `pr-*` ao deploy em preview.
- **Change Failure Rate** — % de deploys em preview que precisam revert/fix.
- **MTTR** — tempo para restaurar `feature/*` verde quando pipeline quebra.

Coletar **por pipeline da equipe**; tendência > valor pontual.

## 2. Práticas e heurísticas operacionais

### 2.1 Como o DevOps atua no Replenishment

- Item que adiciona dependência cloud nova → DevOps C (módulo Terraform, custo, IAM).
- Item que muda padrão de deploy → DevOps R (atualiza pipeline + manifest).
- Item que adiciona feature flag → DevOps R (provisiona em Unleash + monitoração).
- Item que toca CI → DevOps R com Eng Coach.

### 2.2 Como o DevOps atua no Risk Review

- Flaky steps do pipeline (top-N por job).
- Tempo do commit stage (alvo: ≤ 10 min; tendência).
- Tempo do acceptance stage (alvo: ≤ 30 min).
- CVE críticos pendentes (com AppSec).
- Drift Terraform detectado.
- Flags ativas > 30 dias sem owner.
- Custo de ambiente preview (FinOps básico).

### 2.3 Anti-padrões frequentes

- ❌ **Pipeline disparando em branch alheia** — viola fronteira de responsabilidade do time.
- ❌ **Build > 10 min no commit stage** — XP §1.6; quebra disciplina de feedback rápido.
- ❌ **`terraform apply` automático sem revisão** em ambiente compartilhado.
- ❌ **Secret em `application.properties` versionado** ou em `env:` do workflow.
- ❌ **Imagem `latest` em deploy** — sem versão imutável, não há rollback determinístico.
- ❌ **Container rodando como root** — `runAsNonRoot: true` + `readOnlyRootFilesystem: true`.
- ❌ **Sem readiness probe** — tráfego entra antes do app estar pronto.
- ❌ **HPA sem PDB** — escala bem mas downtime em rolling.
- ❌ **Pipeline duplicado por ambiente** — preferir um pipeline parametrizado.
- ❌ **Helm template gigante sem teste** — adotar `helm lint` + `kubeconform` no CI.
- ❌ **Construir plataforma paralela** quando golden path corporativo existe.
- ❌ **`kubectl apply` manual em ambiente reconciliado por GitOps** — drift garantido.

### 2.4 Pipeline de Terraform (resumo)

```yaml
on:
  pull_request:
    paths: ['infra/terraform/**']

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: hashicorp/setup-terraform@v3
      - run: terraform fmt -check -recursive
      - run: terraform init -backend-config=envs/feature/backend.tfvars
      - run: terraform validate
      - run: terraform plan -var-file=envs/feature/terraform.tfvars -out=tfplan
      - uses: aquasecurity/tfsec-action@v1
      - uses: bridgecrewio/checkov-action@master
      - run: terraform show -json tfplan > plan.json
      # comentário do plan no PR
```

### 2.5 Healthcheck e shutdown gracioso (Quarkus)

```properties
quarkus.shutdown.timeout=30s   # tempo para drenar requests
quarkus.smallrye-health.root-path=/q/health
quarkus.smallrye-openapi.path=/q/openapi
```

Configurar SIGTERM handler do K8s (`terminationGracePeriodSeconds: 45`, > shutdown timeout).

### 2.6 Colaboração com outros papéis

- **Eng Coach** — métricas DORA do pipeline; saúde do trunk-equivalente do time.
- **Tech Lead** — config Quarkus, native build quando relevante.
- **Quality Engineer** — estágios de teste no pipeline; tempo dos stages.
- **AppSec** — controles de segurança no pipeline; gates.
- **SRE** — handoff de readiness para produção; observabilidade.
- **Arquiteto Sis** — topologia de deploy; service mesh; ingress.
- **Data Engineer** — pipeline de migration Flyway (gate antes do deploy).

## 3. Templates e checklists

### 3.1 Checklist de readiness do pipeline da equipe

- [ ] Triggers restritos a `pr-*` e `feature/*` do time.
- [ ] Commit stage ≤ 10 min.
- [ ] Acceptance stage ≤ 30 min.
- [ ] Cache de Maven/Gradle ativo.
- [ ] Paralelização onde possível.
- [ ] Gates de segurança (SAST/SCA/secret/container/IaC).
- [ ] SBOM gerado e versionado por build de acceptance.
- [ ] Tag de imagem = SHA imutável (nunca `latest` em deploy).
- [ ] Deploy em preview automático após acceptance verde.
- [ ] Métricas de pipeline (duração, falhas) coletadas.

### 3.2 Checklist de manifest Kubernetes (deployment Quarkus)

- [ ] `runAsNonRoot: true`, `readOnlyRootFilesystem: true`, capabilities drop ALL.
- [ ] Resource requests + limits (CPU/memória) declarados.
- [ ] Liveness + Readiness + Startup probes apontando para `/q/health/*`.
- [ ] `terminationGracePeriodSeconds` > `quarkus.shutdown.timeout`.
- [ ] `imagePullPolicy: IfNotPresent` com tag imutável.
- [ ] Labels padrão (`app`, `version`, `component`, `team`).
- [ ] PDB se réplicas > 1 em produção.
- [ ] HPA com métrica adequada (não só CPU).
- [ ] NetworkPolicy restritiva (deny-all + allow-list).
- [ ] Service account dedicada (sem default).

### 3.3 Template de Dockerfile multi-stage para Quarkus (alternativa ao Jib)

```dockerfile
# Build stage
FROM registry.access.redhat.com/ubi9/openjdk-21:latest AS build
WORKDIR /app
COPY pom.xml .
COPY .mvn .mvn
COPY mvnw .
RUN ./mvnw -B dependency:go-offline
COPY src src
RUN ./mvnw -B package -DskipTests

# Runtime stage
FROM registry.access.redhat.com/ubi9/openjdk-21-runtime:latest
ENV LANG='en_US.UTF-8' LANGUAGE='en_US:en'
COPY --chown=185 --from=build /app/target/quarkus-app/lib/ /deployments/lib/
COPY --chown=185 --from=build /app/target/quarkus-app/*.jar /deployments/
COPY --chown=185 --from=build /app/target/quarkus-app/app/ /deployments/app/
COPY --chown=185 --from=build /app/target/quarkus-app/quarkus/ /deployments/quarkus/
USER 185
EXPOSE 8080
ENTRYPOINT ["java","-jar","/deployments/quarkus-run.jar"]
```

(Default da equipe é Jib — Dockerfile usado apenas quando Jib não atende.)

### 3.4 Política de tags e versionamento de imagem

```
<repo>/<componente>:<versao>-<sha-curta>

Ex.:
  harbor.aco/pedidos:1.7.0-a1b2c3d
  harbor.aco/pedidos:feature-aprovacao-pedido-a1b2c3d   (em preview)
```

- Nunca `:latest` em deploy.
- Tag de feature inclui slug da branch para rastreio.
- Promotion entre ambientes = re-tag, sem rebuild.

### 3.5 Quando escalar

- **Plataforma corporativa quebra continuamente** → enabling team / arquitetura corporativa.
- **Pipeline > 10 min insolúvel** → Eng Coach + Tech Lead (split de módulo, paralelização).
- **Custo de ambiente preview explodindo** → SRE + FinOps + PO (priorização).
- **Falha de gate de segurança recorrente** → AppSec (revisão de threshold ou de código).

## 4. Como esta skill é usada pelo agente

Carregada **exclusivamente** pelo agente `equipe-agil-devops`, **depois** de `equipe-agil-xp-baseline` + `equipe-agil-kanban-method`.

O DevOps usa esta skill para:
- Desenhar/manter o pipeline `pr-*` → `feature/*` da equipe.
- Construir e empacotar artefatos (Jib, container, SBOM).
- Provisionar IaC dos ambientes do time (Terraform).
- Operar GitOps (ArgoCD/Flux) para deploy reproduzível.
- Implantar/operar feature flags com AppSec/Eng Coach.
- Garantir secrets seguros no pipeline.
- Apoiar Tech Lead em decisões de build (JVM vs native).

DevOps **não toca** branches alheias (`develop`, `release/*`, `feature/*` de outras equipes). Quando integração externa é necessária, escala ao owner.

## References

Bibliografia da seção 3.9 do prompt (apenas crédito — todo o conteúdo necessário já está nas seções 1–3 acima; **não consultar online**):

- *Continuous Delivery* — Humble & Farley
- *The DevOps Handbook* — Kim, Humble, Debois & Willis
- *Accelerate* — Forsgren, Humble & Kim
- *Team Topologies* — Skelton & Pais
- *Infrastructure as Code* (2ª ed.) — Morris
- *Terraform: Up & Running* (3ª ed.) — Brikman
- *Kubernetes Patterns* — Ibryam & Huß
- *Kubernetes in Action* (2ª ed.) — Lukša
- *GitOps and Kubernetes* — Yuen, Matyushentsev, Ekenstam & Suen
- *Feature Management with LaunchDarkly / Effective Feature Management* — Hodgson
- *The Phoenix Project* / *The Unicorn Project* — Kim
- *Quarkus Deployment & Container Image Guides* — Red Hat
