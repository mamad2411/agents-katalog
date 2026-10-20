---
name: auditar-pipeline
description: "Revisa workflows de CI/CD quanto a corretude e conformidade de segurança. Use quando o dev-devops ou o tech-lead vai auditar um pipeline."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: auditar-pipeline

Revisa um workflow GitHub Actions existente verificando conformidade com `Guardrails/devops.md`: segurança de secrets, rastreabilidade de imagens, separação de environments, gate de produção e boas práticas de CI/CD.

**Agente:** dev-devops · tech-lead  
**Guardrails aplicáveis:** `devops.md`, `seguranca.md`

---

## Quando usar

- Ao revisar pipeline de um PR que modifica arquivos `.github/workflows/`
- Ao auditar pipelines existentes antes de um release crítico
- Ao integrar um repositório novo ao padrão do projeto
- Quando `revisar-pr` identifica mudança em workflow file

---

## Processo de execução

### Passo 1 — Ler o workflow antes de qualquer análise

Confirmar:

1. Qual o arquivo auditado? (caminho no repositório)
2. É pipeline de serviço Node.js, frontend, biblioteca ou outro?
3. Qual o target de deploy? (ECS Fargate — padrão · Kubernetes · VM)
4. O target é diferente de ECS? Se sim, verificar se há aprovação do arquiteto registrada (`devops.md §9`)

### Passo 2 — Verificar segurança de secrets (`devops.md §1`)

```yaml
# ⛔ secret hardcoded
- run: curl -u admin:senha123 https://registry.example.com

# ⛔ secret interpolado diretamente em run (não mascarado pelo GitHub se derivado)
- run: echo "token is ${{ secrets.API_TOKEN }}" > config.txt

# ⛔ secret em build-arg (fica na camada da imagem Docker — inspecionável)
- uses: docker/build-push-action@v5
  with:
    build-args: DATABASE_PASSWORD=${{ secrets.DB_PASSWORD }}

# ✅ secret em env var intermediária
- run: ./deploy.sh
  env:
    API_TOKEN: ${{ secrets.API_TOKEN }}

# ✅ secret via action dedicada (login, configure-credentials)
- uses: docker/login-action@v3
  with:
    password: ${{ secrets.REGISTRY_TOKEN }}
```

Checklist:
- [ ] Nenhum valor sensível hardcoded no arquivo
- [ ] Nenhum `${{ secrets.X }}` interpolado diretamente em `run:` sem env intermediária
- [ ] Nenhum secret em `build-args` do Docker
- [ ] Credenciais de cloud (AWS, GCP, Azure) via actions oficiais de cada provedor

### Passo 3 — Verificar rastreabilidade de imagens (`devops.md §2`)

```yaml
# ⛔ apenas latest — não é rastreável
tags: ${{ env.IMAGE_NAME }}:latest

# ⛔ tag semântica sem SHA — não identifica o commit exato
tags: ${{ env.IMAGE_NAME }}:v1.2.3

# ✅ SHA sempre presente (pode ter outras tags além)
tags: |
  type=sha,prefix=sha-
  type=raw,value=latest,enable={{is_default_branch}}
```

Checklist:
- [ ] `docker/metadata-action` com `type=sha,prefix=sha-` ou equivalente
- [ ] SHA do commit propagado do job de build para o job de deploy via `outputs`
- [ ] Deploy usa a tag SHA, não apenas `:latest`

### Passo 4 — Verificar separação de environments (`devops.md §3` e `devops.md §4`)

```yaml
# ⛔ deploy de produção sem dependência de staging
deploy-production:
  needs: build     # pula staging

# ⛔ environment de produção sem keyword environment:
deploy-production:
  runs-on: ubuntu-latest
  # sem environment: name: production

# ✅ dependência explícita e environment configurado
deploy-production:
  needs: deploy-staging
  environment:
    name: production
    url: ${{ vars.PRODUCTION_URL }}
```

Checklist:
- [ ] Job `deploy-production` tem `needs: deploy-staging` (ou array que inclua staging)
- [ ] Job `deploy-production` tem `environment: name: production`
- [ ] Job `deploy-staging` tem `environment: name: staging`
- [ ] Environments têm `url:` definida para rastreamento de deployments no GitHub

### Passo 5 — Verificar versões de actions (`devops.md §5`)

```yaml
# ⛔ tag mutável para action de terceiro
- uses: aws-actions/amazon-ecs-deploy-task-definition@master

# ⛔ sem versão
- uses: some-org/some-action

# ✅ SHA para action de terceiro
- uses: aws-actions/configure-aws-credentials@e3dd6a429d7300a6a4c196c26e071d42e0343502

# ✅ versão major para actions do github/docker
- uses: actions/checkout@v4
- uses: docker/build-push-action@v5
```

Checklist:
- [ ] Actions de terceiros (não `actions/` ou `docker/`) fixadas a SHA completo
- [ ] Actions do `actions/` e `docker/` fixadas à versão major mínimo (`@v4`, não `@v4.1.0` obrigatório)
- [ ] Nenhuma action sem versão (`uses: org/action` sem `@versao`)

### Passo 6 — Verificar escopo de triggers

```yaml
# ⛔ trigger muito amplo em monorepo — toda mudança dispara todos os pipelines
on:
  push:
    branches: [main]

# ✅ filtro por paths evita deploys desnecessários
on:
  push:
    branches: [main]
    paths:
      - 'services/order-service/**'
      - '.github/workflows/ci-cd-order-service.yml'
```

Checklist:
- [ ] Em monorepo: `paths` configurado para limitar trigger ao serviço do pipeline
- [ ] Incluir o próprio arquivo de workflow em `paths` (mudança no pipeline deve disparar o pipeline)
- [ ] Sem `workflow_dispatch` desnecessário que permita deploy manual sem rastreabilidade

### Passo 7 — Verificar separação de responsabilidades entre jobs

```yaml
# ⛔ job único faz tudo — impossível re-executar apenas o deploy
jobs:
  ci-cd:
    steps:
      - run: npm test
      - run: docker build
      - run: kubectl apply

# ✅ jobs separados — re-run granular, falha isolada
jobs:
  test:      # roda apenas em PR
  build:     # roda apenas em push para main
  deploy-staging:    # depende de build
  deploy-production: # depende de deploy-staging
```

Checklist:
- [ ] Separação entre jobs de CI (teste) e CD (deploy)
- [ ] Job de teste roda apenas em PRs; deploy apenas em push para `main`
- [ ] Cache Docker configurado (`cache-from/cache-to: type=gha`)

### Passo 8 — Verificar conformidade com ECS Fargate (`devops.md §9`)

Aplicar apenas quando o target de deploy é ECS:

```yaml
# ⛔ GHCR como registry para serviço ECS
- uses: docker/login-action@v3
  with:
    registry: ghcr.io                     # requer credencial extra na task definition

# ✅ ECR — integração nativa com ECS
- uses: aws-actions/amazon-ecr-login@062b18b96a7aff071d4dc91bc00c4c1a7945b076

# ⛔ deploy sem verificação de estabilização
- run: aws ecs update-service --cluster ... --service ... --force-new-deployment
  # sem wait — pipeline reporta sucesso antes do serviço estar ativo

# ✅ deploy com wait obrigatório
- run: |
    aws ecs update-service --cluster ... --service ... --force-new-deployment
- run: |
    aws ecs wait services-stable --cluster ... --services ...
```

Checklist ECS:

- [ ] Registry é ECR (não GHCR) — `devops.md §9.1`
- [ ] Autenticação via `aws-actions/configure-aws-credentials` com SHA fixo
- [ ] Login via `aws-actions/amazon-ecr-login` com SHA fixo
- [ ] Job `deploy` inclui `wait services-stable` após `update-service` — `devops.md §9.2`
- [ ] Variables ECS presentes por environment: `AWS_REGION`, `ECR_REPOSITORY`, `ECS_CLUSTER`, `ECS_SERVICE` — `devops.md §9.3`
- [ ] Target diferente de ECS tem aprovação do arquiteto registrada — `devops.md §9`

### Passo 9 — Emitir parecer

```markdown
## Auditoria de Pipeline — <nome-do-arquivo>

**Resultado:** ✅ Aprovado | ⚠️ Aprovado com ressalvas | ⛔ Bloqueado

---

### Bloqueadores (devem ser corrigidos antes do merge)
- ⛔ <linha X> — <descrição> — `devops.md §<n>`
  Correção: <como corrigir>

### Ressalvas (não bloqueiam, mas devem ser tratadas)
- ⚠️ <descrição> — sugestão: <o que fazer>

### Pontos positivos
- ✅ <o que está correto>

### Checklist de conformidade

- [x/⛔] Secrets sem hardcode (`devops.md §1`)
- [x/⛔] Images com SHA (`devops.md §2`)
- [x/⛔] Staging precede produção (`devops.md §3`)
- [x/⛔] Gate de aprovação em produção (`devops.md §4`)
- [x/⛔] Actions de terceiros fixadas a SHA (`devops.md §5`)
- [x/⛔] Logs sem dados sensíveis (`devops.md §6`)
- [x/⛔] Secrets por environment, não repository (`devops.md §7`)
- [x/⛔] Registry ECR + deploy ECS com wait (`devops.md §9`) — se aplicável
```

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "O pipeline já funciona, não precisa de auditoria" | Pipeline funcionando não é pipeline seguro. Secret exposto em log só aparece quando auditado — não quando o deploy ocorre. |
| "Vou verificar só os secrets, o resto está ok" | Auditoria parcial sem declarar escopo é mais perigosa que nenhuma — cria falsa sensação de conformidade. Actions sem SHA, deploy sem gate de produção: cada item tem consequência própria. |
| "Esse pipeline é igual ao do outro serviço, deve estar correto" | Cópia preserva bugs. Actions de terceiros fixadas a SHA, paths de trigger, environments — cada serviço tem particularidades que divergem na cópia. |
| "Produção sem approval gate é temporário" | Temporário em infraestrutura vira permanente. Gate de aprovação em produção é obrigatório por `devops.md §4` — não é configuração opcional que pode esperar. |
| "As actions que uso são populares, não precisam de SHA fixo" | Popularidade não é segurança. Actions de terceiros sem SHA fixo são vetor de supply chain attack — um tag mutável pode ser reescrito por atacante com acesso ao repositório da action. |

---

## Checklist de conclusão

- [ ] Todos os guardrails de `devops.md` verificados (§1–§7 sempre; §9 quando target é ECS)
- [ ] Parecer emitido com resultado claro
- [ ] Bloqueadores têm referência ao guardrail e ação de correção específica
