---
name: github-actions-cloud
description: Deploy por GitHub Actions no Google Cloud e no Azure, sem chaves de longa duração — OIDC com Workload Identity Federation (GCP) e federated credentials (Azure) restritos ao repositório e ao environment, imagem no Artifact Registry/ACR com tag imutável, deploy no Cloud Run, GKE, Azure Container Apps e AKS com verificação e rollback, segredos no Secret Manager/Key Vault e aprovação para produção. Use quando o destino do deploy não for a AWS.
---

Antes de aplicar este pattern, leia também [`../github-actions/SKILL.md`](../github-actions/SKILL.md) (o CI: build, testes, segurança do pipeline), [`../docker-and-docker-compose/SKILL.md`](../docker-and-docker-compose/SKILL.md) e, para os destinos Kubernetes, [`../kubernetes/SKILL.md`](../kubernetes/SKILL.md) e [`../helm-charts/SKILL.md`](../helm-charts/SKILL.md). Na AWS, o equivalente é [`../github-actions-aws/SKILL.md`](../github-actions-aws/SKILL.md); por GitOps, [`../argocd/SKILL.md`](../argocd/SKILL.md).

# GitHub Actions → Google Cloud e Azure

O princípio é o mesmo de `github-actions-aws`: **nenhuma chave de longa duração no GitHub**. Nada de JSON de service account do GCP nem *client secret* do Azure em GitHub Secrets. O workflow recebe um **token OIDC** do GitHub por execução, a nuvem confia nele (com condições sobre o repositório e o environment) e entrega credenciais temporárias.

**Pergunte o destino e até onde o pipeline vai** (e salve): nuvem (GCP ou Azure), runtime (serverless de containers ou Kubernetes), e se há staging automático + produção com aprovação.

| | Google Cloud | Azure |
|---|---|---|
| Identidade federada | Workload Identity Federation (pool + provider OIDC) | Federated credential em uma app registration ou managed identity |
| Registry | Artifact Registry | Azure Container Registry (ACR) |
| Containers sem Kubernetes | **Cloud Run** | **Azure Container Apps** |
| Kubernetes gerenciado | GKE | AKS |
| Segredos da aplicação | Secret Manager | Key Vault |

---

## 1. Google Cloud

### Confiança (uma vez por projeto)
1. Crie um **workload identity pool** e um **provider OIDC** com issuer `https://token.actions.githubusercontent.com`, mapeando `attribute.repository = assertion.repository` e com a **condição de atributo** que restringe o repositório: `assertion.repository == 'minha-org/library-api'`. Sem a condição, qualquer repositório do GitHub poderia usar o provider.
2. Crie uma **service account** para o deploy, com o mínimo: `roles/artifactregistry.writer` no repositório do Artifact Registry e `roles/run.developer` (Cloud Run) ou `roles/container.developer` (GKE). Para o Cloud Run, também `roles/iam.serviceAccountUser` na service account de **runtime** do serviço.
3. Permita que o pool personifique a service account (`roles/iam.workloadIdentityUser`) **apenas** para o principal do repositório — e, para produção, use uma service account separada.

### Workflow (Cloud Run)
```yaml
  deploy-gcp:
    needs: build-test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      id-token: write
    env:
      REGION: us-central1
      IMAGE: us-central1-docker.pkg.dev/meu-projeto/apps/library-api:${{ github.sha }}
    steps:
      - uses: actions/checkout@v4
      - uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: projects/123456789/locations/global/workloadIdentityPools/github/providers/github
          service_account: deployer-prod@meu-projeto.iam.gserviceaccount.com
      - uses: google-github-actions/setup-gcloud@v2
      - name: Build and push
        run: |
          gcloud auth configure-docker "$REGION-docker.pkg.dev" --quiet
          docker build -t "$IMAGE" .
          docker push "$IMAGE"
      - name: Deploy
        run: |
          gcloud run deploy library-api \
            --image "$IMAGE" \
            --region "$REGION" \
            --service-account runtime-library-api@meu-projeto.iam.gserviceaccount.com \
            --set-secrets "DB_PASSWORD=library-db-password:latest" \
            --no-allow-unauthenticated
```
- **`--set-secrets`** injeta o valor do **Secret Manager** como variável de ambiente: a senha nunca passa pelo GitHub. Fixe a versão do segredo (`:3`) quando quiser deploys reprodutíveis.
- **Service account de runtime** própria, com só o que a aplicação usa (Cloud SQL Client, Secret Accessor) — não a service account padrão do Compute.
- **Rollback no Cloud Run:** cada deploy é uma *revision*. Se a verificação pós-deploy falhar, devolva o tráfego para a anterior: `gcloud run services update-traffic library-api --region "$REGION" --to-revisions PREVIOUS_REVISION=100`. Para canary, publique com `--no-traffic --tag canary` e mova o tráfego em etapas (`release-management`).
- Cloud Run escala por request e para em zero: ajuste `--min-instances` para evitar cold start da JVM em APIs sensíveis à latência (`jvm-performance`: CDS/AOT).

### GKE
Troque o passo de deploy por:
```yaml
      - uses: google-github-actions/get-gke-credentials@v2
        with:
          cluster_name: library
          location: us-central1
      - name: Deploy
        run: |
          cd k8s/overlays/prod
          kustomize edit set image library-api=${{ env.IMAGE }}
          kubectl apply -k .
          kubectl -n library rollout status deployment/library-api --timeout=300s
      - name: Roll back on failure
        if: failure()
        run: kubectl -n library rollout undo deployment/library-api
```
Dentro do cluster, os pods acessam APIs do Google com **Workload Identity do GKE** (Kubernetes service account ligada a uma service account do Google) — o equivalente ao IRSA da AWS; nunca uma chave montada como Secret.

---

## 2. Azure

### Confiança (uma vez por ambiente)
1. Crie uma **app registration** (ou uma **user-assigned managed identity**) para o deploy.
2. Adicione uma **federated credential**: issuer `https://token.actions.githubusercontent.com`, audience `api://AzureADTokenExchange`, subject restrito, por exemplo `repo:minha-org/library-api:environment:production` (ou `repo:minha-org/library-api:ref:refs/heads/main`). Uma identidade por ambiente.
3. Atribua o mínimo: `AcrPush` no ACR; para Container Apps, `Contributor` **só** no resource group da aplicação (ou um papel customizado); para AKS, `Azure Kubernetes Service Cluster User Role` mais RBAC do Kubernetes restrito ao namespace.

Os três identificadores (client id, tenant id, subscription id) **não são segredos** — guarde-os como *variables* do environment (`vars.*`).

### Workflow (Container Apps)
```yaml
  deploy-azure:
    needs: build-test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    permissions:
      contents: read
      id-token: write
    env:
      IMAGE: libraryacr.azurecr.io/library-api:${{ github.sha }}
    steps:
      - uses: actions/checkout@v4
      - uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
      - name: Build and push
        run: |
          az acr login --name libraryacr
          docker build -t "$IMAGE" .
          docker push "$IMAGE"
      - name: Deploy
        run: |
          az containerapp update \
            --name library-api \
            --resource-group rg-library-prod \
            --image "$IMAGE"
```
- A Container App usa uma **managed identity** para puxar do ACR (`AcrPull`) e ler o **Key Vault** — segredos referenciados pela app (`keyvaultref:`), nunca valores passados pelo workflow.
- **Rollback:** com *revision mode* múltiplo, cada deploy cria uma revision; devolva o tráfego para a anterior com `az containerapp ingress traffic set --revision-weight <revisão-anterior>=100`.
- ACR com *admin user* **desligado** — acesso só por identidade.

### AKS
```yaml
      - name: Deploy
        run: |
          az aks get-credentials --resource-group rg-library-prod --name library-aks
          cd k8s/overlays/prod
          kustomize edit set image library-api=${{ env.IMAGE }}
          kubectl apply -k .
          kubectl -n library rollout status deployment/library-api --timeout=300s
      - name: Roll back on failure
        if: failure()
        run: kubectl -n library rollout undo deployment/library-api
```
Com AKS integrado ao Entra ID, o `kubectl` pode precisar do `kubelogin` para usar o token do workflow (`kubelogin convert-kubeconfig -l azurecli`). Pods acessam recursos do Azure com **Workload Identity do AKS**, não com segredos.

---

## 3. Em qualquer nuvem

- **A imagem é a do CI:** o deploy usa o mesmo SHA que passou no `build-test` (`github-actions`). Os exemplos fazem o build no job de deploy por simplicidade; em pipelines maiores, construa uma vez e promova a mesma imagem entre registries/ambientes.
- **Tag imutável** (`github.sha`); registries com tags imutáveis quando o provedor oferece; nunca `latest`.
- **`environment: production`** com *required reviewers* = aprovação manual e escopo da identidade federada.
- **`id-token: write` só no job de deploy**; pull requests não fazem deploy nem recebem credenciais.
- **Verificação pós-deploy:** `rollout status` (Kubernetes) ou um smoke test HTTP contra a nova revision (`postman-newman`, pasta de smoke) antes de considerar o deploy concluído; rollback automático se falhar.
- **Migrations do Flyway** rodam antes do tráfego chegar à versão nova e são compatíveis com a anterior (`flyway-migrations`: expand → contract; no Kubernetes, um Job ou hook — `kubernetes`, `argocd`).
- **Infra como código:** os recursos (pool/identidades, registry, serviço) declarados em Terraform — os providers `google` e `azurerm` seguem as mesmas práticas de `aws-terraform` (estado remoto, plan no PR, apply com aprovação).
- **GitOps** como alternativa em Kubernetes: o CI só atualiza a tag no repositório de configuração e o Argo CD aplica (`argocd`) — o workflow não precisa de acesso ao cluster.

---

## Regras principais

- **OIDC, nunca chaves de longa duração:** Workload Identity Federation no GCP, federated credential no Azure — com condição sobre o repositório **e** o environment/branch.
- Uma identidade por ambiente, com o menor papel possível (push no registry + deploy no serviço/namespace).
- `id-token: write` só no job de deploy; produção atrás de `environment` com aprovação.
- Tag da imagem = `github.sha`; o deploy usa a imagem que passou no CI.
- Segredos da aplicação no Secret Manager/Key Vault, lidos pela identidade de runtime — nunca passados pelo workflow.
- Identidade de runtime própria para a aplicação (Workload Identity no GKE/AKS, managed identity no Container Apps, service account dedicada no Cloud Run).
- Todo deploy termina com verificação e tem rollback (revisions no Cloud Run/Container Apps, `rollout undo` no Kubernetes).
- Actions fixadas e atualizadas pelo Dependabot; confirme as versões mais recentes das actions.
