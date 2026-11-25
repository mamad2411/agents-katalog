---
name: gitops-workflow
description: "Guia completo para implementar workflows GitOps com ArgoCD e Flux para deployments automatizados em Kubernetes."
risk: critical
source: community
date_added: "2026-02-27"
---

# Workflow GitOps

Guia completo para implementar workflows GitOps com ArgoCD e Flux para deployments automatizados em Kubernetes.

## Propósito

Implementar entrega contínua declarativa baseada em Git para Kubernetes usando ArgoCD ou Flux CD, seguindo os princípios do OpenGitOps.

## Use essa habilidade quando

- Configurar GitOps para clusters Kubernetes
- Automatizar deployments de aplicações a partir do Git
- Implementar estratégias de entrega progressiva
- Gerenciar deployments multi-cluster
- Configurar políticas de sincronização automática
- Configurar gerenciamento de secrets em GitOps

## Não use essa habilidade quando

- Você precisa de um deployment manual único
- Você não consegue gerenciar acesso ao cluster ou permissões de repositório
- Você não está fazendo deploy para Kubernetes

## Instruções

1. Defina layout de repositório e convenções de estado desejado.
2. Instale ArgoCD ou Flux e conecte clusters.
3. Configure políticas de sincronização, ambientes e fluxo de promoção.
4. Valide rollbacks e manipulação de secrets.

## Segurança

- Evite auto-sync para produção sem aprovações.
- Mantenha secrets fora do Git e use sealed secrets ou gerenciadores de secrets externos.

## Princípios do OpenGitOps

1. **Declarativo** - Sistema inteiro descrito declarativamente
2. **Versionado e Imutável** - Estado desejado armazenado em Git
3. **Puxado Automaticamente** - Agentes de software puxam estado desejado
4. **Continuamente Reconciliado** - Agentes reconciliam estado atual vs estado desejado

## Configuração do ArgoCD

### 1. Instalação

```bash
# Create namespace
kubectl create namespace argocd

# Install ArgoCD
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

# Get admin password
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```

**Referência:** Consulte `references/argocd-setup.md` para configuração detalhada

### 2. Estrutura de Repositório

```
gitops-repo/
├── apps/
│   ├── production/
│   │   ├── app1/
│   │   │   ├── kustomization.yaml
│   │   │   └── deployment.yaml
│   │   └── app2/
│   └── staging/
├── infrastructure/
│   ├── ingress-nginx/
│   ├── cert-manager/
│   └── monitoring/
└── argocd/
    ├── applications/
    └── projects/
```

### 3. Criar Aplicação

```yaml
# argocd/applications/my-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo
    targetRevision: main
    path: apps/production/my-app
  destination:
    server: https://kubernetes.default.svc
    namespace: production
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
    - CreateNamespace=true
```

### 4. Padrão App of Apps

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: applications
  namespace: argocd
spec:
  project: default
  source:
    repoURL: https://github.com/org/gitops-repo
    targetRevision: main
    path: argocd/applications
  destination:
    server: https://kubernetes.default.svc
    namespace: argocd
  syncPolicy:
    automated: {}
```

## Configuração do Flux CD

### 1. Instalação

```bash
# Install Flux CLI
curl -s https://fluxcd.io/install.sh | sudo bash

# Bootstrap Flux
flux bootstrap github \
  --owner=org \
  --repository=gitops-repo \
  --branch=main \
  --path=clusters/production \
  --personal
```

### 2. Criar GitRepository

```yaml
apiVersion: source.toolkit.fluxcd.io/v1
kind: GitRepository
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 1m
  url: https://github.com/org/my-app
  ref:
    branch: main
```

### 3. Criar Kustomization

```yaml
apiVersion: kustomize.toolkit.fluxcd.io/v1
kind: Kustomization
metadata:
  name: my-app
  namespace: flux-system
spec:
  interval: 5m
  path: ./deploy
  prune: true
  sourceRef:
    kind: GitRepository
    name: my-app
```

## Políticas de Sincronização

### Configuração de Auto-Sync

**ArgoCD:**
```yaml
syncPolicy:
  automated:
    prune: true      # Delete resources not in Git
    selfHeal: true   # Reconcile manual changes
    allowEmpty: false
  retry:
    limit: 5
    backoff:
      duration: 5s
      factor: 2
      maxDuration: 3m
```

**Flux:**
```yaml
spec:
  interval: 1m
  prune: true
  wait: true
  timeout: 5m
```

**Referência:** Consulte `references/sync-policies.md`

## Entrega Progressiva

### Canary Deployment com ArgoCD Rollouts

```yaml
apiVersion: argoproj.io/v1alpha1
kind: Rollout
metadata:
  name: my-app
spec:
  replicas: 5
  strategy:
    canary:
      steps:
      - setWeight: 20
      - pause: {duration: 1m}
      - setWeight: 50
      - pause: {duration: 2m}
      - setWeight: 100
```

### Deployment Blue-Green

```yaml
strategy:
  blueGreen:
    activeService: my-app
    previewService: my-app-preview
    autoPromotionEnabled: false
```

## Gerenciamento de Secrets

### External Secrets Operator

```yaml
apiVersion: external-secrets.io/v1beta1
kind: ExternalSecret
metadata:
  name: db-credentials
spec:
  refreshInterval: 1h
  secretStoreRef:
    name: aws-secrets-manager
    kind: SecretStore
  target:
    name: db-credentials
  data:
  - secretKey: password
    remoteRef:
      key: prod/db/password
```

### Sealed Secrets

```bash
# Encrypt secret
kubeseal --format yaml < secret.yaml > sealed-secret.yaml

# Commit sealed-secret.yaml to Git
```

## Melhores Práticas

1. **Use repositórios ou branches separados** para diferentes ambientes
2. **Implemente RBAC** para repositórios Git
3. **Habilite notificações** para falhas de sincronização
4. **Use health checks** para recursos customizados
5. **Implemente approval gates** para produção
6. **Mantenha secrets fora do Git** (use External Secrets)
7. **Use padrão App of Apps** para organização
8. **Marque releases com tags** para rollback fácil
9. **Monitore status de sincronização** com alertas
10. **Teste mudanças** em staging primeiro

## Solução de Problemas

**Falhas de sincronização:**
```bash
argocd app get my-app
argocd app sync my-app --prune
```

**Status fora de sincronização:**
```bash
argocd app diff my-app
argocd app sync my-app --force
```

## Habilidades Relacionadas

- `k8s-manifest-generator` - Para criar manifests
- `helm-chart-scaffolding` - Para empacotar aplicações