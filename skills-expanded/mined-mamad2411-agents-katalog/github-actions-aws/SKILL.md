---
name: github-actions-aws
description: Pipeline GitHub Actions para Spring Boot na AWS — build e testes com Testcontainers, OIDC sem access keys, imagem no ECR com tag imutável (git sha), deploy no EKS com verificação e rollback, environments com aprovação, cache, cobertura no PR e trust policy mínima. Use quando criar ou revisar CI/CD para a AWS.
---

Antes de aplicar este pattern, leia também [`../code-organization/SKILL.md`](../code-organization/SKILL.md), [`../code-style/SKILL.md`](../code-style/SKILL.md), [`../docker-and-docker-compose/SKILL.md`](../docker-and-docker-compose/SKILL.md), [`../kubernetes/SKILL.md`](../kubernetes/SKILL.md) e [`../aws-eks/SKILL.md`](../aws-eks/SKILL.md).

# GitHub Actions → ECR → EKS

**Pergunte até onde o pipeline vai** (e salve): só build + testes; + imagem no ECR; + deploy em staging; + deploy em produção com aprovação. O arquivo abaixo cobre tudo, em jobs separados para você remover o que não precisa.

## O princípio central: sem access keys

**Nunca** guarde `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` em GitHub Secrets. Use **OIDC**: o GitHub emite um token de curta duração por execução, a AWS confia nele (identity provider `token.actions.githubusercontent.com`) e o workflow *assume uma IAM role* com credenciais temporárias. Não há segredo de longa duração para vazar ou rotacionar.

### IAM — provider e role

1. Crie o **OIDC identity provider** na conta AWS: URL `https://token.actions.githubusercontent.com`, audience `sts.amazonaws.com` (uma vez por conta).
2. Crie uma role para o pipeline com esta **trust policy**, restringindo **repositório e branch/ambiente** — sem essa restrição, qualquer repositório do GitHub poderia assumir a role:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Federated": "arn:aws:iam::123456789012:oidc-provider/token.actions.githubusercontent.com" },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": { "token.actions.githubusercontent.com:aud": "sts.amazonaws.com" },
        "StringLike": { "token.actions.githubusercontent.com:sub": "repo:minha-org/library-api:environment:production" }
      }
    }
  ]
}
```
O `sub` pode ser `repo:org/repo:ref:refs/heads/main` (por branch) ou `...:environment:<nome>` (por *environment* do GitHub — o melhor para produção, porque junta a aprovação manual).
3. **Permissões da role (menor privilégio):** push no **seu** repositório ECR (`ecr:GetAuthorizationToken` em `*` — é obrigatório —, e `ecr:BatchCheckLayerAvailability`, `PutImage`, `InitiateLayerUpload`, `UploadLayerPart`, `CompleteLayerUpload` no ARN do repositório) e `eks:DescribeCluster` no cluster. Dentro do cluster, conceda à role um **EKS access entry** com policy restrita ao namespace (`aws eks create-access-entry` + `associate-access-policy`, veja `aws-eks`). Uma role por ambiente (staging/prod).

---

## Workflow

`.github/workflows/ci-cd.yml`:

```yaml
name: ci-cd

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

permissions:
  contents: read

concurrency:
  group: ci-cd-${{ github.ref }}
  cancel-in-progress: true

env:
  AWS_REGION: us-east-1
  ECR_REPOSITORY: library-api
  EKS_CLUSTER: library

jobs:
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: 25
          cache: maven
      - name: Build and test
        run: ./mvnw -B clean verify

  image:
    needs: build-test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read
    outputs:
      image: ${{ steps.meta.outputs.image }}
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-ecr-push
          aws-region: ${{ env.AWS_REGION }}
      - id: ecr
        uses: aws-actions/amazon-ecr-login@v2
      - id: meta
        run: echo "image=${{ steps.ecr.outputs.registry }}/${{ env.ECR_REPOSITORY }}:${{ github.sha }}" >> "$GITHUB_OUTPUT"
      - uses: docker/setup-buildx-action@v3
      - uses: docker/build-push-action@v6
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.image }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-prod:
    needs: image
    runs-on: ubuntu-latest
    environment: production
    permissions:
      id-token: write
      contents: read
    steps:
      - uses: actions/checkout@v4
      - uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789012:role/github-actions-eks-deploy-prod
          aws-region: ${{ env.AWS_REGION }}
      - run: aws eks update-kubeconfig --name ${{ env.EKS_CLUSTER }} --region ${{ env.AWS_REGION }}
      - name: Set image and apply
        run: |
          cd k8s/overlays/prod
          kustomize edit set image library-api=${{ needs.image.outputs.image }}
          kubectl apply -k .
      - name: Wait for rollout
        run: kubectl -n library rollout status deployment/library-api --timeout=300s
      - name: Roll back on failure
        if: failure()
        run: kubectl -n library rollout undo deployment/library-api
```

Pontos que importam:
- **`permissions` mínimas**: o default do workflow é `contents: read`; `id-token: write` **só** nos jobs que falam com a AWS.
- **Testes com Testcontainers funcionam no `ubuntu-latest`** (Docker já vem instalado) — `./mvnw verify` roda unit + integration (`maven-config`: não há split unit/integration). Gradle: `./gradlew build` e `cache: gradle` no `setup-java`; no Linux o wrapper precisa do bit executável (`git add --chmod=+x`, veja `scaffold`).
- **Pull request** roda só `build-test`: nenhum acesso à AWS, nenhum segredo exposto a código de fork.
- **Tag da imagem = `github.sha`**: imutável, rastreável do commit até o pod. Combina com ECR `IMMUTABLE` (`aws-eks`). Para releases, adicione também a tag semântica (`v1.4.2`) num job disparado por tag.
- **`environment: production`** com *required reviewers* configurado nas settings do repositório = **aprovação manual** antes do deploy e escopo do `sub` da trust policy.
- **`rollout status` + `rollout undo`**: o job só termina verde se o rollout completou (as probes passaram); se falhar, reverte automaticamente. `kubectl` e `kustomize` já estão no runner do GitHub; fixe a versão se o seu cluster exigir.
- **`concurrency`** evita dois deploys simultâneos e cancela execuções obsoletas de PR.
- Para **Helm** troque o passo de deploy por: `helm upgrade --install library chart/library-api -n library -f chart/library-api/values-prod.yaml --set image.tag=${{ github.sha }} --atomic --wait --timeout 5m` (`helm-charts`).

## Alternativa: GitOps com Argo CD (o CI não toca o cluster)

O job `deploy-prod` acima é **push**: o CI precisa de acesso ao cluster (role IAM + EKS access entry). É simples e adequado a poucos serviços. Com **vários serviços/ambientes**, auditoria ou drift, prefira **GitOps** (`argocd`): o CI só **publica a imagem** e **commita a nova tag** no repositório de configuração; o **Argo CD, dentro do cluster, aplica**. Vantagens: nenhuma credencial do cluster no CI, estado desejado no Git, rollback por `git revert`, detecção de drift. Substitua o job de deploy pelo job `promote-*` descrito na skill `argocd` (seção 7) — o resto do pipeline (build, testes, OIDC, push para o ECR) **não muda**.

---

## Qualidade e segurança no pipeline

- **Fixe as actions por SHA** (`uses: actions/checkout@<sha>`) em repositórios sensíveis, e use Dependabot (`.github/dependabot.yml`, ecosystem `github-actions`, `maven`, `docker`) para atualizá-las: uma action comprometida roda com as suas permissões. As tags `@v4` do exemplo são por legibilidade — confirme as versões mais recentes.
- **Cobertura como gate no pull request** (`test-coverage`): o `./mvnw -B clean verify` do job `build-test` já falha se o `check` do JaCoCo (**90% de linha e de branch**) for violado; publique o `target/site/jacoco/` como artefato e o `jacoco.xml` no Codecov/SonarQube para o **PR mostrar a cobertura do código novo**. Prefira **diff coverage + catraca** a uma meta global. Mutation testing (PIT) vai em **job agendado/incremental**, não em todo commit.
- **Escaneie a imagem** antes do deploy (Trivy no workflow, ou o resultado do `scanOnPush` do ECR) e **as dependencies** (Dependabot alerts / `dependency-check`).
- **Não imprima segredos**: o GitHub mascara os `secrets.*`, mas não valores derivados; nunca `echo` credenciais nem faça `set -x` perto delas.
- **Deploy de ambiente de staging** automático em `main` e produção com aprovação é um bom default; branches de feature não fazem deploy.
- `workflow_dispatch` com input de `image tag` permite **reimplantar/rollback manual** de uma versão anterior sem novo build.

---

## Regras principais

- **OIDC, nunca access keys** em GitHub Secrets; trust policy restrita ao repositório **e** ao environment/branch.
- `permissions` mínimas por job; `id-token: write` só onde a AWS é usada; PRs não tocam a AWS.
- Tag da imagem = `github.sha` (imutável), ECR `IMMUTABLE`; nunca `latest`.
- Os testes (incluindo Testcontainers) rodam no CI **antes** de qualquer push de imagem.
- Produção atrás de um `environment` com aprovação; uma role IAM por ambiente, menor privilégio (ECR do repositório + EKS access entry por namespace).
- Deploy termina com `rollout status` e faz `rollout undo` se falhar.
- Actions fixadas/atualizadas por Dependabot; imagem e dependencies escaneadas.
