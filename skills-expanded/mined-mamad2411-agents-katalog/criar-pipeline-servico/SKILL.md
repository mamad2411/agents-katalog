---
name: criar-pipeline-servico
description: "Cria workflows de CI/CD de staging e produção para serviços Node.js. Use quando o dev-devops ou um dev de backend vai configurar a esteira de um serviço."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: criar-pipeline-servico

Cria os **dois workflows GitHub Actions** para um serviço Node.js (backend, BFF ou worker de mensageria): `ci-cd-staging.yml` (deploy automático em branches de desenvolvimento) e `ci-cd-production.yml` (deploy em `main` com aprovação manual). Target padrão: **AWS ECS Fargate + ECR**.

**Agente:** dev-devops · dev-backend · dev-bff · dev-mensageria  
**Guardrails aplicáveis:** `devops.md §1`, `devops.md §2`, `devops.md §3`, `devops.md §4`, `devops.md §9`, `operacional.md §4`, `seguranca.md`  
**Referências rápidas:** `Guidelines/devops/ecs-fargate.md`

---

## Quando usar

- Ao criar um novo serviço Node.js que precisa de pipeline CI/CD
- Ao adicionar pipeline a serviço existente que ainda não tem
- Ao migrar pipeline de SSH/VM para ECS Fargate

---

## Pré-requisitos

- Nome do serviço (usado no ECR repo e no nome da imagem)
- Repositório GitHub dedicado ao serviço já criado
- Infraestrutura AWS provisionada: ECR repo, ECS cluster, ECS service, task definition base, ALB com health check
- Environments `staging` e `production` criados no GitHub (`configurar-environments-github`)
- `.env.example` no repositório com todas as chaves sem valores

Se infraestrutura não estiver pronta, verificar `Guidelines/devops/ecs-fargate.md §Pré-requisitos` antes de continuar.

---

## Processo de execução

### Passo 1 — Coletar informações do serviço

```text
1. Qual o nome do serviço? (usado no ECR repo e nome do workflow)
2. Autenticação AWS:
   - OIDC (preferido): AWS_ROLE_ARN configurado no GitHub
   - Access key (fallback): AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY
3. As variáveis AWS já estão configuradas nos GitHub environments?
   (AWS_REGION, AWS_ACCOUNT_ID, ECR_REPOSITORY, ECS_CLUSTER, ECS_SERVICE)
4. O target de deploy é diferente de ECS Fargate?
   (Se sim: escalar para arquiteto antes de gerar pipeline — devops.md §9)
```

### Passo 2 — Gerar `ci-cd-staging.yml`

Executa em **branches de desenvolvimento** (todas exceto `main`). Fluxo: test → envfile → release → deploy automático.

```yaml
name: CI/CD - Build & Deploy to Staging

on:
  push:
    branches:
      - development
      - staging
      - chore/*
      - feature/*
      - fix/*
      - hotfix/*
      - release/*
  workflow_dispatch:

jobs:
  # ─────────────────────────────────────────────────────────
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests with coverage
        run: npm test -- --coverage --ci

    environment: staging

  # ─────────────────────────────────────────────────────────
  envfile:
    needs: [test]
    runs-on: ubuntu-latest
    environment: staging

    env:
      # Mapear secrets com prefixo _ (substituídos pelo dump-env)
      _APP_KEY:      ${{ secrets._APP_KEY }}
      _DB_HOST:      ${{ secrets._DB_HOST }}
      _DB_PASSWORD:  ${{ secrets._DB_PASSWORD }}
      # ... demais secrets com prefixo _
      # Vars sem prefixo _ (valores não sensíveis)
      _APP_URL:      ${{ vars._APP_URL }}
      # ... demais vars com prefixo _

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - name: Generate .env from template
        run: |
          pip install dump-env
          dump-env --template=.env.example --prefix='_' > env
      - uses: actions/upload-artifact@v4
        with:
          name: env-file
          path: env
          if-no-files-found: error

  # ─────────────────────────────────────────────────────────
  release:
    needs: [test, envfile]
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - name: Download .env artifact
        uses: actions/download-artifact@v4
        with:
          name: env-file
          path: .

      - name: Move .env to project root
        run: mv env .env

      - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ vars.AWS_REGION }}
          # Para OIDC substituir pelas linhas abaixo e remover as duas acima:
          # role-to-assume: ${{ secrets.AWS_ROLE_ARN }}
          # aws-region: ${{ vars.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@062b18b96a7aff071d4dc91bc00c4c1a7945b076

      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.login-ecr.outputs.registry }}/${{ vars.ECR_REPOSITORY }}:sha-${{ github.sha }}-staging

  # ─────────────────────────────────────────────────────────
  deploy:
    needs: release
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ vars.AWS_REGION }}

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster ${{ vars.ECS_CLUSTER }} \
            --service ${{ vars.ECS_SERVICE }} \
            --force-new-deployment

      - name: Wait for service stability
        run: |
          aws ecs wait services-stable \
            --cluster ${{ vars.ECS_CLUSTER }} \
            --services ${{ vars.ECS_SERVICE }}
```

### Passo 3 — Gerar `ci-cd-production.yml`

Executa **apenas em `main`**. Fluxo: envfile → release → deploy com aprovação obrigatória.

```yaml
name: CI/CD - Build & Deploy to Production

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  # ─────────────────────────────────────────────────────────
  envfile:
    runs-on: ubuntu-latest
    environment: production

    env:
      # Mapear secrets com prefixo _ (substituídos pelo dump-env)
      _APP_KEY:      ${{ secrets._APP_KEY }}
      _DB_HOST:      ${{ secrets._DB_HOST }}
      _DB_PASSWORD:  ${{ secrets._DB_PASSWORD }}
      # ... demais secrets com prefixo _
      # Vars sem prefixo _ (valores não sensíveis)
      _APP_URL:      ${{ vars._APP_URL }}
      # ... demais vars com prefixo _

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - name: Generate .env from template
        run: |
          pip install dump-env
          dump-env --template=.env.example --prefix='_' > env
      - uses: actions/upload-artifact@v4
        with:
          name: env-file
          path: env
          if-no-files-found: error

  # ─────────────────────────────────────────────────────────
  release:
    needs: [envfile]
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Download .env artifact
        uses: actions/download-artifact@v4
        with:
          name: env-file
          path: .

      - name: Move .env to project root
        run: mv env .env

      - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ vars.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@062b18b96a7aff071d4dc91bc00c4c1a7945b076

      - name: Build and push image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ steps.login-ecr.outputs.registry }}/${{ vars.ECR_REPOSITORY }}:sha-${{ github.sha }}
            ${{ steps.login-ecr.outputs.registry }}/${{ vars.ECR_REPOSITORY }}:production

  # ─────────────────────────────────────────────────────────
  deploy:
    needs: release
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ vars.AWS_REGION }}

      - name: Deploy to ECS
        run: |
          aws ecs update-service \
            --cluster ${{ vars.ECS_CLUSTER }} \
            --service ${{ vars.ECS_SERVICE }} \
            --force-new-deployment

      - name: Wait for service stability
        run: |
          aws ecs wait services-stable \
            --cluster ${{ vars.ECS_CLUSTER }} \
            --services ${{ vars.ECS_SERVICE }}
```

### Passo 4 — Documentar secrets e variables necessários

Criar ou atualizar `docs/pipeline.md` com:

```markdown
## Pipeline CI/CD — <nome-do-servico>

### GitHub Secrets (por environment)

| Secret | Descrição |
| --- | --- |
| `AWS_ACCESS_KEY_ID` | IAM access key com permissão ECR + ECS |
| `AWS_SECRET_ACCESS_KEY` | IAM secret key correspondente |
| `_<NOME>` | Cada secret da aplicação com prefixo `_` |

### GitHub Variables (por environment)

| Variable | Staging | Produção |
| --- | --- | --- |
| `AWS_REGION` | `us-east-1` | `us-east-1` |
| `AWS_ACCOUNT_ID` | `<id-staging>` | `<id-prod>` |
| `ECR_REPOSITORY` | `<nome>` | `<nome>` |
| `ECS_CLUSTER` | `<cluster>-staging` | `<cluster>-production` |
| `ECS_SERVICE` | `<servico>-staging` | `<servico>-production` |
| `_<NOME>` | valor staging | valor produção |
```

### Passo 5 — Variantes para targets alternativos (não-padrão)

> Usar apenas se o arquiteto aprovou explicitamente target diferente de ECS (`devops.md §9`).

#### Kubernetes (kubectl)

```yaml
- name: Deploy to Kubernetes
  run: |
    echo "$KUBECONFIG_B64" | base64 -d > /tmp/kubeconfig
    kubectl --kubeconfig /tmp/kubeconfig \
      set image deployment/<nome-do-servico> \
      app=${{ vars.AWS_ACCOUNT_ID }}.dkr.ecr.${{ vars.AWS_REGION }}.amazonaws.com/${{ vars.ECR_REPOSITORY }}:sha-${{ github.sha }} \
      -n ${{ vars.K8S_NAMESPACE }}
    kubectl --kubeconfig /tmp/kubeconfig \
      rollout status deployment/<nome-do-servico> \
      -n ${{ vars.K8S_NAMESPACE }} --timeout=120s
  env:
    KUBECONFIG_B64: ${{ secrets.KUBECONFIG }}
```

#### Docker Compose em VM via SSH

```yaml
- name: Deploy via SSH
  run: |
    echo "$SSH_PRIVATE_KEY" > /tmp/deploy_key
    chmod 600 /tmp/deploy_key
    scp -i /tmp/deploy_key -o StrictHostKeyChecking=no \
      ./docker-compose.yml ${{ vars.DEPLOY_USER }}@${{ vars.DEPLOY_HOST }}:~/
    ssh -i /tmp/deploy_key -o StrictHostKeyChecking=no \
      ${{ vars.DEPLOY_USER }}@${{ vars.DEPLOY_HOST }} \
      "docker compose pull && docker compose up -d --no-build"
  env:
    SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
```

---

## Anti-padrões bloqueados

- `devops.md §1` — secret hardcoded no workflow ou em `build-args` Docker
- `devops.md §2` — imagem tagueada apenas com `:latest` sem SHA
- `devops.md §4` — environment `production` sem reviewer obrigatório no GitHub
- `devops.md §9` — GHCR como registry para serviço ECS (requer credencial extra na task definition)
- Deploy sem `wait services-stable` — pipeline reporta sucesso antes do serviço estar ativo
- Arquivo único de workflow para staging e produção — impede controle de fluxo por branch

---

## Checklist de conclusão

- [ ] `ci-cd-staging.yml` criado com branches de desenvolvimento corretos
- [ ] `ci-cd-production.yml` criado com `branches: [main]`
- [ ] Job `test` presente no staging
- [ ] Job `envfile` com `dump-env` e todos os secrets/vars mapeados com prefixo `_`
- [ ] Job `release` baixa artifact `.env`, autentica no ECR e faz push (`devops.md §9`)
- [ ] Staging: imagem tagueada com `sha-<commit>-staging`
- [ ] Produção: imagem tagueada com `sha-<commit>` + `production` (`devops.md §2`)
- [ ] Job `deploy` usa `update-service --force-new-deployment` + `wait services-stable`
- [ ] Environment `production` com reviewer obrigatório (`devops.md §4`)
- [ ] Secrets e variables documentados em `docs/pipeline.md`
- [ ] `.env.example` no repositório com todas as chaves sem valores
