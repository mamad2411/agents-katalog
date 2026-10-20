---
name: criar-pipeline-frontend
description: "Cria workflows de CI/CD de staging e produção para frontend React com Vite ou CRA. Use quando o dev-devops ou o dev-frontend vai configurar a esteira de um frontend."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: criar-pipeline-frontend

Cria os **dois workflows GitHub Actions** para um frontend React: `ci-cd-staging.yml` (build com variáveis de staging, deploy automático em branches de desenvolvimento) e `ci-cd-production.yml` (build com variáveis de produção, deploy em `main` com aprovação manual). Target padrão: **AWS ECS Fargate + ECR** (frontend entregue como imagem Docker Nginx).

**Agente:** dev-devops · dev-frontend  
**Guardrails aplicáveis:** `devops.md §1`, `devops.md §2`, `devops.md §3`, `devops.md §4`, `devops.md §9`, `operacional.md §4`, `seguranca.md`  
**Referências rápidas:** `Guidelines/devops/ecs-fargate.md`

---

## Quando usar

- Ao criar um novo frontend React que precisa de pipeline CI/CD
- Ao adicionar pipeline a frontend existente
- Frontend é entregue como imagem Docker Nginx

---

## Diferença em relação a `criar-pipeline-servico`

| Aspecto | Serviço Node.js | Frontend React |
| --- | --- | --- |
| Testes | Jest com cobertura | Jest + RTL com `--watchAll=false` |
| Build | `npm run build` (TypeScript) | `npm run build` (Vite/CRA — assets estáticos) |
| Imagem | Node.js runtime | Nginx com assets estáticos |
| Build args | Não usa (dump-env no container) | `VITE_*` / `REACT_APP_*` embutidos em build time |
| `.env` baked | Sim — via dump-env no job envfile | Não — vars públicas via `build-args` |

> **Atenção:** variáveis `VITE_*` / `REACT_APP_*` ficam embutidas na imagem em build time. Por isso staging e produção geram imagens separadas. Nunca usar `secrets.*` em `build-args` — ficam na camada da imagem e são inspecionáveis (`devops.md §1`).

---

## Pré-requisitos

- Repositório GitHub dedicado ao frontend
- Framework do frontend (Vite / Create React App / Next.js)
- URLs públicas de API por ambiente (`VITE_API_URL` de staging e produção)
- Infraestrutura AWS provisionada: ECR repo, ECS cluster, ECS service, task definition base, ALB
- Environments `staging` e `production` no GitHub

---

## Processo de execução

### Passo 1 — Confirmar variáveis de build e autenticação AWS

```text
1. Qual a URL da API de staging? (ex: https://api.staging.example.com)
2. Qual a URL da API de produção? (ex: https://api.example.com)
3. Há outras VITE_* que diferem entre ambientes?
4. Autenticação AWS:
   - OIDC (preferido): AWS_ROLE_ARN configurado
   - Access key: AWS_ACCESS_KEY_ID + AWS_SECRET_ACCESS_KEY
5. As variables ECS já estão configuradas?
   (AWS_REGION, ECR_REPOSITORY, ECS_CLUSTER, ECS_SERVICE)
```

### Passo 2 — Gerar `ci-cd-staging.yml`

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
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test -- --coverage --ci --watchAll=false

      - name: Build check
        run: npm run build
        env:
          VITE_API_URL: ${{ vars.STAGING_API_URL }}

  # ─────────────────────────────────────────────────────────
  release:
    needs: [test]
    runs-on: ubuntu-latest
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ vars.AWS_REGION }}
          # Para OIDC substituir pelas linhas abaixo:
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
          build-args: |
            VITE_API_URL=${{ vars.STAGING_API_URL }}
          cache-from: type=gha,scope=staging
          cache-to: type=gha,scope=staging,mode=max

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

```yaml
name: CI/CD - Build & Deploy to Production

on:
  push:
    branches:
      - main
  workflow_dispatch:

jobs:
  # ─────────────────────────────────────────────────────────
  release:
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

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
          build-args: |
            VITE_API_URL=${{ vars.PRODUCTION_API_URL }}
          cache-from: type=gha,scope=production
          cache-to: type=gha,scope=production,mode=max

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

> Frontend de produção não tem job `test` separado — o build check em staging já validou. Se o projeto exigir testes em produção também, adicionar job `test` com `needs: test` no `release`.

### Passo 4 — Documentar variáveis e secrets necessários

```markdown
## Pipeline CI/CD — Frontend

### GitHub Secrets (por environment)

| Secret | Descrição |
| --- | --- |
| `AWS_ACCESS_KEY_ID` | IAM access key com permissão ECR + ECS |
| `AWS_SECRET_ACCESS_KEY` | IAM secret key correspondente |

### GitHub Variables (por environment)

| Variable | Staging | Produção |
| --- | --- | --- |
| `AWS_REGION` | `us-east-1` | `us-east-1` |
| `ECR_REPOSITORY` | `<nome>-frontend` | `<nome>-frontend` |
| `ECS_CLUSTER` | `<cluster>-staging` | `<cluster>-production` |
| `ECS_SERVICE` | `<frontend>-staging` | `<frontend>-production` |
| `STAGING_API_URL` | `https://api.staging.example.com` | — |
| `PRODUCTION_API_URL` | — | `https://api.example.com` |
```

---

## Anti-padrões bloqueados

- Usar `secrets.*` em `build-args` — secrets ficam na camada da imagem (`devops.md §1`)
- Imagem única para staging e produção quando URLs diferem — `VITE_*` é baked em build time
- Arquivo único de workflow para staging e produção — impede controle de fluxo por branch
- Environment `production` sem reviewer obrigatório (`devops.md §4`)
- GHCR como registry para serviço ECS (`devops.md §9`)
- Deploy sem `wait services-stable` — pipeline reporta sucesso antes do serviço estar ativo

---

## Checklist de conclusão

- [ ] `ci-cd-staging.yml` criado com branches de desenvolvimento corretos
- [ ] `ci-cd-production.yml` criado com `branches: [main]`
- [ ] Job `test` no staging com `--watchAll=false` e build check com `VITE_*` de staging
- [ ] Job `release` autentica no ECR e faz push com SHA tag (`devops.md §2` e `§9`)
- [ ] `build-args` contém apenas valores públicos — nunca secrets (`devops.md §1`)
- [ ] Staging: imagem tagueada com `sha-<commit>-staging`
- [ ] Produção: imagem tagueada com `sha-<commit>` + `production`
- [ ] Job `deploy` usa `update-service --force-new-deployment` + `wait services-stable`
- [ ] Environment `production` com reviewer obrigatório (`devops.md §4`)
- [ ] Variables documentadas: `STAGING_API_URL`, `PRODUCTION_API_URL`, ECS vars por environment
