---
name: railway-environment
description: Consultar, preparar e aplicar alterações de configuração para ambientes Railway. Use para QUALQUER operação de variáveis ou env vars, configuração de serviço (fonte, configurações de build, configurações de deploy), ciclo de vida (deletar serviço) e aplicar mudanças. Prefira em relação à skill railway-status para qualquer consulta de configuração ou variáveis.
version: 1.0.0
author: Railway
license: MIT
tags: [Railway, Environment, Configuration, Variables, Build, Deploy, Infrastructure, Settings]
dependencies: [railway-cli]
allowed-tools: Bash(railway:*)
---

# Configuração de Ambiente

Consultar, preparar e aplicar alterações de configuração para ambientes Railway.

## Escape de Shell

**CRÍTICO:** Ao executar queries GraphQL via bash, você DEVE envolver em heredoc para evitar problemas de escape de shell:

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh 'query ...' '{"var": "value"}'
SCRIPT
```

Sem o wrapper heredoc, comandos multi-linha quebram e exclamações em tipos GraphQL não-nulos ficam escapadas, causando falhas de query.

## Quando Usar

- Usuário quer criar um novo ambiente
- Usuário quer duplicar um ambiente (ex: "copiar produção para staging")
- Usuário quer mudar para um ambiente diferente
- Usuário pergunta sobre configurações atuais de build/deploy, variáveis, réplicas, health checks, domínios
- Usuário pede para mudar a fonte do serviço (imagem Docker, branch, commit, diretório raiz)
- Usuário quer conectar um serviço a um repositório GitHub
- Usuário quer fazer deploy de um repositório GitHub (criar serviço vazio primeiro via skill railway-new, depois usar esta)
- Usuário pede para mudar comando de build ou start
- Usuário quer adicionar/atualizar/deletar variáveis de ambiente
- Usuário quer mudar contagem de réplicas ou configurar health checks
- Usuário pergunta para deletar um serviço, volume ou bucket
- Usuário diz "aplicar mudanças", "confirmar mudanças", "fazer deploy das mudanças"
- Auto-correção de erros de build detectados em logs

## Criar Ambiente

Criar um novo ambiente no projeto vinculado:

```bash
railway environment new <name>
```

Duplicar um ambiente existente:

```bash
railway environment new staging --duplicate production
```

Com variáveis específicas do serviço:

```bash
railway environment new staging --duplicate production --service-variable api PORT=3001
```

## Trocar Ambiente

Vincular um ambiente diferente ao diretório atual:

```bash
railway environment <name>
```

Ou por ID:

```bash
railway environment <environment-id>
```

## Obter Contexto

```bash
railway status --json
```

Extrair:

- `project.id` - para busca de serviço
- `environment.id` - para as mutações
- `service.id` - serviço padrão se usuário não especificar um

### Resolver ID do Serviço

Se usuário especificar um serviço por nome, consultar serviços do projeto:

```graphql
query projectServices($projectId: String!) {
  project(id: $projectId) {
    services {
      edges {
        node {
          id
          name
        }
      }
    }
  }
}
```

Corresponder o nome do serviço (case-insensitive) para obter o ID do serviço.

## Consultar Configuração

Buscar configuração atual do ambiente e mudanças preparadas.

```graphql
query environmentConfig($environmentId: String!) {
  environment(id: $environmentId) {
    id
    config(decryptVariables: false)
    serviceInstances {
      edges {
        node {
          id
          serviceId
        }
      }
    }
  }
  environmentStagedChanges(environmentId: $environmentId) {
    id
    patch(decryptVariables: false)
  }
}
```

Exemplo:

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'query envConfig($envId: String!) {
    environment(id: $envId) { id config(decryptVariables: false) }
    environmentStagedChanges(environmentId: $envId) { id patch(decryptVariables: false) }
  }' \
  '{"envId": "ENV_ID"}'
SCRIPT
```

### Estrutura de Resposta

O campo `config` contém a configuração atual:

```json
{
  "services": {
    "<serviceId>": {
      "source": { "repo": "...", "branch": "main" },
      "build": { "buildCommand": "npm run build", "builder": "NIXPACKS" },
      "deploy": {
        "startCommand": "npm start",
        "multiRegionConfig": { "us-west2": { "numReplicas": 1 } }
      },
      "variables": { "NODE_ENV": { "value": "production" } },
      "networking": { "serviceDomains": {}, "customDomains": {} }
    }
  },
  "sharedVariables": { "DATABASE_URL": { "value": "..." } }
}
```

O campo `patch` em `environmentStagedChanges` contém mudanças pendentes. A configuração efetiva é a `config` base mesclada com o `patch` preparado.

Para referência completa de campos, ver [reference/environment-config.md](../reference/environment-config.md).

Para sintaxe de variáveis e padrões de interconexão de serviço, ver [reference/variables.md](../reference/variables.md).

## Obter Variáveis Renderizadas

As queries GraphQL acima retornam variáveis **não renderizadas** - sintaxe de template como `${{shared.DOMAIN}}` é preservada. Isso é correto para gerenciamento/edição.

Para ver valores **renderizados** (resolvidos) como aparecem em tempo de execução:

```bash
# Serviço vinculado atual
railway variables --json

# Serviço específico
railway variables --service <service-name> --json
```

**Quando usar:**
- Depurar problemas de conexão (ver URLs/portas reais)
- Verificar se resolução de variáveis está correta
- Visualizar valores injetados por Railway (RAILWAY_*)

## Preparar Mudanças

Preparar alterações de configuração via mutação `environmentStageChanges`. Use `merge: true` para mesclar automaticamente com mudanças preparadas existentes.

```graphql
mutation stageEnvironmentChanges(
  $environmentId: String!
  $input: EnvironmentConfig!
  $merge: Boolean
) {
  environmentStageChanges(
    environmentId: $environmentId
    input: $input
    merge: $merge
  ) {
    id
  }
}
```

**Importante:** Sempre use variáveis (não input inline) porque IDs de serviço são UUIDs que não podem ser usados como chaves de objeto GraphQL sem aspas.

Exemplo:

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation stageChanges($environmentId: String!, $input: EnvironmentConfig!, $merge: Boolean) {
    environmentStageChanges(environmentId: $environmentId, input: $input, merge: $merge) { id }
  }' \
  '{"environmentId": "ENV_ID", "input": {"services": {"SERVICE_ID": {"build": {"buildCommand": "npm run build"}}}}, "merge": true}'
SCRIPT
```

### Deletar Serviço

Use `isDeleted: true`:

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation stageChanges($environmentId: String!, $input: EnvironmentConfig!, $merge: Boolean) {
    environmentStageChanges(environmentId: $environmentId, input: $input, merge: $merge) { id }
  }' \
  '{"environmentId": "ENV_ID", "input": {"services": {"SERVICE_ID": {"isDeleted": true}}}, "merge": true}'
SCRIPT
```

## Preparar e Aplicar Imediatamente

Para mudanças únicas que devem fazer deploy direto, use `environmentPatchCommit` para preparar e aplicar em uma chamada.

```graphql
mutation environmentPatchCommit(
  $environmentId: String!
  $patch: EnvironmentConfig
  $commitMessage: String
) {
  environmentPatchCommit(
    environmentId: $environmentId
    patch: $patch
    commitMessage: $commitMessage
  )
}
```

Exemplo:

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation patchCommit($environmentId: String!, $patch: EnvironmentConfig, $commitMessage: String) {
    environmentPatchCommit(environmentId: $environmentId, patch: $patch, commitMessage: $commitMessage)
  }' \
  '{"environmentId": "ENV_ID", "patch": {"services": {"SERVICE_ID": {"variables": {"API_KEY": {"value": "secret"}}}}}, "commitMessage": "add API_KEY"}'
SCRIPT
```

**Quando usar:** Mudança única, sem necessidade de agrupar, usuário quer deploy imediato.

**Quando NÃO usar:** Múltiplas mudanças relacionadas para agrupar, ou usuário diz "preparar apenas" / "não fazer deploy ainda".

## Aplicar Mudanças Preparadas

Confirmar mudanças preparadas e disparar deployments.

**Nota:** Não existe comando CLI `railway apply`. Use a mutação abaixo ou direcione usuários para a UI web.

### Mutação Aplicar

**Nome da mutação: `environmentPatchCommitStaged`**

```graphql
mutation environmentPatchCommitStaged(
  $environmentId: String!
  $message: String
  $skipDeploys: Boolean
) {
  environmentPatchCommitStaged(
    environmentId: $environmentId
    commitMessage: $message
    skipDeploys: $skipDeploys
  )
}
```

Exemplo:

```bash
bash <<'SCRIPT'
${CLAUDE_PLUGIN_ROOT}/skills/lib/railway-api.sh \
  'mutation commitStaged($environmentId: String!, $message: String) {
    environmentPatchCommitStaged(environmentId: $environmentId, commitMessage: $message)
  }' \
  '{"environmentId": "ENV_ID", "message": "add API_KEY variable"}'
SCRIPT
```

### Parâmetros

| Campo           | Tipo    | Padrão | Descrição                                      |
| --------------- | ------- | ------ | ---------------------------------------------- |
| `environmentId` | String! | -      | ID do ambiente a partir de status             |
| `message`       | String  | null   | Descrição curta das mudanças                   |
| `skipDeploys`   | Boolean | false  | Pular deployments (apenas se usuário solicitar) |

### Mensagem de Commit

Manter muito curta - máximo uma frase. Exemplos:

- "set build command to fix npm error"
- "add API_KEY variable"
- "increase replicas to 3"

Deixar vazio se não houver descrição significativa.

### Comportamento Padrão

**Sempre fazer deploy** a menos que usuário solicite explicitamente pular. Apenas defina `skipDeploys: true` se usuário disser "aplicar sem fazer deploy", "confirmar mas não fazer deploy", ou "pular deployments".

Retorna um ID de workflow (string) em sucesso.

## Comportamento Auto-Aplicar

Por padrão, **aplicar mudanças imediatamente**.

### Fluxo

**Mudança única:** Use `environmentPatchCommit` para preparar e aplicar em uma chamada.

**Múltiplas mudanças ou agrupamento:** Use `environmentStageChanges` com `merge: true` para cada mudança, depois `environmentPatchCommitStaged` para aplicar.

### Quando NÃO Auto-Aplicar

- Usuário explicitamente diz "preparar apenas", "não fazer deploy ainda", ou similar
- Usuário está fazendo múltiplas mudanças relacionadas que devem fazer deploy juntas

**Quando você não auto-aplica, diga ao usuário:**

> Mudanças preparadas. Aplique em: https://railway.com/project/{projectId}
> Ou peça-me para aplicá-las.

Obter `projectId` de `railway status --json` → `project.id`

## Tratamento de Erros

### Serviço Não Encontrado

```
Service "foo" not found in project. Available services: api, web, worker
```

### Nenhuma Mudança Preparada

```
No patch to apply
```

Não há mudanças preparadas para confirmar. Prepare mudanças primeiro.

### Configuração Inválida

Problemas comuns:

- `buildCommand` e `startCommand` não podem ser idênticos
- `buildCommand` válido apenas com builder NIXPACKS
- `dockerfilePath` válido apenas com builder DOCKERFILE

### Sem Permissão

```
You don't have permission to modify this environment. Check your Railway role.
```

### Nenhum Projeto Vinculado

```
No project linked. Run `railway link` to link a project.
```

## Composição

- **Criar serviço**: Use skill railway-service
- **Visualizar logs**: Use skill railway-deployment
- **Adicionar domínios**: Use skill railway-domain
- **Fazer deploy de código local**: Use skill railway-deploy