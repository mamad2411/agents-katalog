---
name: configurar-environments-github
description: "Configura environments do GitHub, secrets e workflows de aprovação. Use quando o dev-devops vai preparar os ambientes de deploy de um repositório."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: configurar-environments-github

Configura os **environments `staging` e `production`** no repositório GitHub com as protection rules corretas, secrets e variables por ambiente — habilitando o gate de aprovação manual para produção.

**Agente:** dev-devops  
**Guardrails aplicáveis:** `devops.md §4`, `devops.md §7`, `seguranca.md`

---

## Quando usar

- Ao criar pipeline CI/CD em repositório que ainda não tem environments configurados
- Ao revisar environments existentes que não têm protection rules adequadas
- Como pré-requisito para `criar-pipeline-servico` e `criar-pipeline-frontend`

---

## Processo de execução

### Passo 1 — Verificar environments existentes

```bash
gh api repos/:owner/:repo/environments --jq '.environments[].name'
```

Se `staging` e `production` já existirem, verificar se têm protection rules adequadas antes de recriar.

### Passo 2 — Criar environment staging

Staging não tem gate de aprovação — deploy é automático após o build. O único requisito é restringir a branch de origem.

```bash
# Via gh CLI
gh api repos/{owner}/{repo}/environments/staging \
  --method PUT \
  --field wait_timer=0 \
  --field deployment_branch_policy='{"protected_branches":false,"custom_branch_policies":true}'

# Restringir para branch main
gh api repos/{owner}/{repo}/environments/staging/deployment-branch-policies \
  --method POST \
  --field name='main' \
  --field type='branch'
```

Via UI: Settings → Environments → New environment → `staging`:
- Deployment branches: Selected branches → `main`
- Reviewers: nenhum (staging é automático)

### Passo 3 — Criar environment production com gate de aprovação

```bash
# Obter ID do usuário ou time revisor
gh api repos/{owner}/{repo}/collaborators --jq '.[] | select(.login == "<login>") | .id'

# Criar environment production com wait timer e reviewer obrigatório
gh api repos/{owner}/{repo}/environments/production \
  --method PUT \
  --field wait_timer=5 \
  --field 'reviewers=[{"type":"User","id":<user-id>}]' \
  --field deployment_branch_policy='{"protected_branches":false,"custom_branch_policies":true}'

# Restringir para branch main
gh api repos/{owner}/{repo}/environments/production/deployment-branch-policies \
  --method POST \
  --field name='main' \
  --field type='branch'
```

Via UI: Settings → Environments → New environment → `production`:
- Required reviewers: adicionar ao menos 1 pessoa ou time
- Wait timer: 5 minutos (dá tempo para cancelar um deploy acidental)
- Deployment branches: Selected branches → `main`

### Passo 4 — Adicionar secrets por environment

Secrets de banco de dados, credenciais de cluster e tokens de acesso devem ser separados por environment — nunca como repository secrets (`devops.md §7`):

```bash
# Secrets de staging
gh secret set DATABASE_URL \
  --env staging \
  --body "postgresql://user:senha@staging-db.internal:5432/app"

gh secret set KUBECONFIG \
  --env staging \
  --body "$(cat ~/.kube/config-staging | base64)"

# Secrets de produção
gh secret set DATABASE_URL \
  --env production \
  --body "postgresql://user:senha@prod-db.internal:5432/app"

gh secret set KUBECONFIG \
  --env production \
  --body "$(cat ~/.kube/config-production | base64)"
```

> **Atenção:** O comando acima usa valores reais apenas como exemplo de formato. Em ambiente real, os valores são fornecidos pela equipe de infraestrutura fora do terminal de desenvolvimento — nunca digitados ou colados em logs.

### Passo 5 — Adicionar variables por environment

Variables (valores não sensíveis) também devem ser separadas por environment:

```bash
# Variables de staging
gh variable set STAGING_URL --env staging --body "https://staging.example.com"
gh variable set K8S_NAMESPACE --env staging --body "staging"
gh variable set ECS_CLUSTER --env staging --body "cluster-staging"

# Variables de produção
gh variable set PRODUCTION_URL --env production --body "https://example.com"
gh variable set K8S_NAMESPACE --env production --body "production"
gh variable set ECS_CLUSTER --env production --body "cluster-production"
```

### Passo 6 — Verificar configuração final

```bash
# Listar environments e suas protection rules
gh api repos/{owner}/{repo}/environments \
  --jq '.environments[] | {name: .name, reviewers: .reviewers, wait_timer: .wait_timer}'

# Listar secrets de cada environment (apenas os nomes — valores não são recuperáveis)
gh secret list --env staging
gh secret list --env production
```

### Passo 7 — Documentar para o time

Criar ou atualizar `docs/pipeline.md` com a lista de secrets e variables necessários, para que qualquer membro da equipe possa reconfigurar o repositório:

```markdown
## Configuração de Environments GitHub

### Environment: staging
Protection: branch `main` apenas — sem reviewer obrigatório

**Secrets necessários:**
| Nome | Descrição |
|---|---|
| `DATABASE_URL` | Connection string PostgreSQL de staging |
| `KUBECONFIG` | kubeconfig do cluster de staging (base64) |

**Variables necessárias:**
| Nome | Exemplo |
|---|---|
| `STAGING_URL` | `https://staging.example.com` |
| `K8S_NAMESPACE` | `staging` |

### Environment: production
Protection: reviewer obrigatório + wait timer 5 minutos + branch `main` apenas

**Secrets necessários:**
| Nome | Descrição |
|---|---|
| `DATABASE_URL` | Connection string PostgreSQL de produção |
| `KUBECONFIG` | kubeconfig do cluster de produção (base64) |

**Variables necessárias:**
| Nome | Exemplo |
|---|---|
| `PRODUCTION_URL` | `https://example.com` |
| `K8S_NAMESPACE` | `production` |
```

---

## Anti-padrões bloqueados

- Repository secrets para valores que diferem entre staging e produção (`devops.md §7`) — usar environment secrets
- Environment `production` sem reviewer obrigatório (`devops.md §4`)
- Sem restrição de branch — qualquer branch poderia fazer deploy em produção

---

## Checklist de conclusão

- [ ] Environment `staging` criado, restrito à branch `main`, sem reviewer
- [ ] Environment `production` criado com reviewer obrigatório + wait timer mínimo 5 min
- [ ] Secrets específicos de cada ambiente configurados em environment secrets (não repository secrets)
- [ ] Variables de URL e namespace configuradas por environment
- [ ] Documentação de secrets e variables criada em `docs/pipeline.md`
