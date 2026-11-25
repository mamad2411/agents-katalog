---
name: github-automation
description: "Automatize gerenciamento de repositórios GitHub, rastreamento de issues, workflows de pull requests, operações de branches e CI/CD por meio do toolkit GitHub do Composio. Gerencie fluxos de código, revise PRs, pesquise código e liide com deployments programaticamente."
risk: critical
source: community
date_added: "2026-02-27"
---

# Automação do GitHub via Rube MCP

Automatize gerenciamento de repositórios GitHub, rastreamento de issues, workflows de pull request, operações de branches e CI/CD através do toolkit GitHub do Composio.

## Pré-requisitos

- Rube MCP deve estar conectado (RUBE_SEARCH_TOOLS disponível)
- Conexão ativa com GitHub via `RUBE_MANAGE_CONNECTIONS` com toolkit `github`
- Sempre chame `RUBE_SEARCH_TOOLS` primeiro para obter os schemas das ferramentas atuais

## Configuração

**Obter Rube MCP**: Adicione `https://rube.app/mcp` como um servidor MCP na configuração do seu cliente. Sem necessidade de API keys — basta adicionar o endpoint e funciona.

1. Verifique se Rube MCP está disponível confirmando que `RUBE_SEARCH_TOOLS` responde
2. Chame `RUBE_MANAGE_CONNECTIONS` com toolkit `github`
3. Se a conexão não estiver ATIVA, siga o link de autenticação retornado para completar o OAuth do GitHub
4. Confirme se o status da conexão mostra ATIVA antes de executar qualquer workflow

## Workflows Principais

### 1. Criar e Gerenciar Issues

**Quando usar**: Usuário quer criar, listar ou gerenciar issues do GitHub

**Sequência de ferramentas**:
1. `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` - Encontrar repositório alvo se desconhecido [Pré-requisito]
2. `GITHUB_LIST_REPOSITORY_ISSUES` - Listar issues existentes (inclui PRs) [Obrigatório]
3. `GITHUB_CREATE_AN_ISSUE` - Criar uma nova issue [Obrigatório]
4. `GITHUB_CREATE_AN_ISSUE_COMMENT` - Adicionar comentários a uma issue [Opcional]
5. `GITHUB_SEARCH_ISSUES_AND_PULL_REQUESTS` - Pesquisar entre repositórios por palavra-chave [Opcional]

**Parâmetros principais**:
- `owner`: Proprietário do repositório (username ou org), insensível a maiúsculas
- `repo`: Nome do repositório sem extensão .git
- `title`: Título da issue (obrigatório para criação)
- `body`: Descrição da issue (suporta Markdown)
- `labels`: Array de nomes de labels
- `assignees`: Array de usernames do GitHub
- `state`: 'open', 'closed' ou 'all' para filtrar

**Armadilhas**:
- `GITHUB_LIST_REPOSITORY_ISSUES` retorna issues E pull requests; verifique o campo `pull_request` para distinguir
- Apenas usuários com acesso push podem definir assignees, labels e milestones; eles são silenciosamente descartados caso contrário
- Paginação: `per_page` máximo 100; itere páginas até ficar vazia

### 2. Gerenciar Pull Requests

**Quando usar**: Usuário quer criar, revisar ou fazer merge de pull requests

**Sequência de ferramentas**:
1. `GITHUB_FIND_PULL_REQUESTS` - Pesquisar e filtrar PRs [Obrigatório]
2. `GITHUB_GET_A_PULL_REQUEST` - Obter informações detalhadas do PR incluindo status de mergeabilidade [Obrigatório]
3. `GITHUB_LIST_PULL_REQUESTS_FILES` - Revisar arquivos alterados [Opcional]
4. `GITHUB_CREATE_A_PULL_REQUEST` - Criar um novo PR [Obrigatório]
5. `GITHUB_CREATE_AN_ISSUE_COMMENT` - Postar comentários de revisão [Opcional]
6. `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` - Verificar status de CI antes do merge [Opcional]
7. `GITHUB_MERGE_A_PULL_REQUEST` - Fazer merge após aprovação explícita do usuário [Obrigatório]

**Parâmetros principais**:
- `head`: Branch de origem com alterações (deve existir; para repositórios cruzados: 'username:branch')
- `base`: Branch alvo para merge (ex: 'main')
- `title`: Título do PR (obrigatório a menos que o número de `issue` seja fornecido)
- `merge_method`: 'merge', 'squash' ou 'rebase'
- `state`: 'open', 'closed' ou 'all'

**Armadilhas**:
- `GITHUB_CREATE_A_PULL_REQUEST` falha com 422 se base/head forem inválidos, idênticos ou já foram merged
- `GITHUB_MERGE_A_PULL_REQUEST` pode ser rejeitado se PR é draft, está fechado ou proteção de branch se aplica
- Sempre verifique o status de mergeabilidade com `GITHUB_GET_A_PULL_REQUEST` imediatamente antes de fazer merge
- Exija confirmação explícita do usuário antes de chamar MERGE

### 3. Gerenciar Repositórios e Branches

**Quando usar**: Usuário quer criar repositórios, gerenciar branches ou atualizar configurações do repositório

**Sequência de ferramentas**:
1. `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` - Listar repositórios do usuário [Obrigatório]
2. `GITHUB_GET_A_REPOSITORY` - Obter informações detalhadas do repositório [Opcional]
3. `GITHUB_CREATE_A_REPOSITORY_FOR_THE_AUTHENTICATED_USER` - Criar repositório pessoal [Obrigatório]
4. `GITHUB_CREATE_AN_ORGANIZATION_REPOSITORY` - Criar repositório de org [Alternativa]
5. `GITHUB_LIST_BRANCHES` - Listar branches [Obrigatório]
6. `GITHUB_CREATE_A_REFERENCE` - Criar novo branch a partir de SHA [Obrigatório]
7. `GITHUB_UPDATE_A_REPOSITORY` - Atualizar configurações do repositório [Opcional]

**Parâmetros principais**:
- `name`: Nome do repositório
- `private`: Booleano para visibilidade
- `ref`: Caminho de referência completo (ex: 'refs/heads/new-branch')
- `sha`: SHA do commit para apontar a nova referência
- `default_branch`: Nome do branch padrão

**Armadilhas**:
- `GITHUB_CREATE_A_REFERENCE` apenas cria NOVAS referências; use `GITHUB_UPDATE_A_REFERENCE` para existentes
- `ref` deve começar com 'refs/' e conter pelo menos duas barras
- `GITHUB_LIST_BRANCHES` pagina via `page`/`per_page`; itere até página vazia
- `GITHUB_DELETE_A_REPOSITORY` é permanente e irreversível; requer privilégios de administrador

### 4. Pesquisar Código e Commits

**Quando usar**: Usuário quer encontrar código, arquivos ou commits entre repositórios

**Sequência de ferramentas**:
1. `GITHUB_SEARCH_CODE` - Pesquisar conteúdo de arquivos e caminhos [Obrigatório]
2. `GITHUB_SEARCH_CODE_ALL_PAGES` - Pesquisa de código multi-página [Alternativa]
3. `GITHUB_SEARCH_COMMITS_BY_AUTHOR` - Pesquisar commits por autor/data/org [Obrigatório]
4. `GITHUB_LIST_COMMITS` - Listar commits para um repositório específico [Alternativa]
5. `GITHUB_GET_A_COMMIT` - Obter informações detalhadas do commit [Opcional]
6. `GITHUB_GET_REPOSITORY_CONTENT` - Obter conteúdo do arquivo [Opcional]

**Parâmetros principais**:
- `q`: Query de pesquisa com qualificadores (`language:python`, `repo:owner/repo`, `extension:js`)
- `owner`/`repo`: Para listagem de commits específico do repositório
- `author`: Filtrar por autor do commit
- `since`/`until`: Intervalo de datas ISO 8601 para commits

**Armadilhas**:
- Pesquisa de código indexa apenas arquivos menores que 384KB no branch padrão
- Máximo de 1000 resultados retornados da pesquisa de código
- `GITHUB_SEARCH_COMMITS_BY_AUTHOR` requer keywords além de qualificadores; queries apenas com qualificadores não são permitidas
- `GITHUB_LIST_COMMITS` retorna 409 em repositórios vazios

### 5. Gerenciar CI/CD e Deployments

**Quando usar**: Usuário quer visualizar workflows, verificar status de CI ou gerenciar deployments

**Sequência de ferramentas**:
1. `GITHUB_LIST_REPOSITORY_WORKFLOWS` - Listar workflows do GitHub Actions [Obrigatório]
2. `GITHUB_GET_A_WORKFLOW` - Obter detalhes do workflow por ID ou nome de arquivo [Opcional]
3. `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT` - Disparar manualmente um workflow [Obrigatório]
4. `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` - Verificar status de CI para um commit/branch [Obrigatório]
5. `GITHUB_LIST_DEPLOYMENTS` - Listar deployments [Opcional]
6. `GITHUB_GET_A_DEPLOYMENT_STATUS` - Obter status do deployment [Opcional]

**Parâmetros principais**:
- `workflow_id`: ID numérico ou nome de arquivo (ex: 'ci.yml')
- `ref`: Referência Git (branch/tag) para dispatch do workflow
- `inputs`: String JSON de inputs do workflow correspondendo a `on.workflow_dispatch.inputs`
- `environment`: Filtrar deployments por nome de ambiente

**Armadilhas**:
- `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT` requer que o workflow tenha o trigger `workflow_dispatch` configurado
- O caminho completo `.github/workflows/main.yml` é automaticamente reduzido para apenas `main.yml`
- Inputs máximo 10 pares chave-valor; devem corresponder às definições de `on.workflow_dispatch.inputs` do workflow

### 6. Gerenciar Usuários e Permissões

**Quando usar**: Usuário quer verificar colaboradores, permissões ou proteção de branch

**Sequência de ferramentas**:
1. `GITHUB_LIST_REPOSITORY_COLLABORATORS` - Listar colaboradores do repositório [Obrigatório]
2. `GITHUB_GET_REPOSITORY_PERMISSIONS_FOR_A_USER` - Verificar acesso de usuário específico [Opcional]
3. `GITHUB_GET_BRANCH_PROTECTION` - Inspecionar regras de proteção de branch [Obrigatório]
4. `GITHUB_UPDATE_BRANCH_PROTECTION` - Atualizar configurações de proteção [Opcional]
5. `GITHUB_ADD_A_REPOSITORY_COLLABORATOR` - Adicionar/atualizar colaborador [Opcional]

**Parâmetros principais**:
- `affiliation`: 'outside', 'direct' ou 'all' para filtro de colaboradores
- `permission`: Filtrar por 'pull', 'triage', 'push', 'maintain', 'admin'
- `branch`: Nome do branch para regras de proteção
- `enforce_admins`: Se a proteção se aplica a administradores

**Armadilhas**:
- `GITHUB_GET_BRANCH_PROTECTION` retorna 404 para branches desprotegidos; trate como sem regras de proteção
- Determine capacidade de push a partir de `permissions.push` ou `role_name`, não rótulos de exibição
- `GITHUB_LIST_REPOSITORY_COLLABORATORS` pagina; itere todas as páginas
- `GITHUB_GET_REPOSITORY_PERMISSIONS_FOR_A_USER` pode ser inconclusivo para não-colaboradores

## Padrões Comuns

### Resolução de ID
- **Nome do repositório -> owner/repo**: `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER`
- **Número do PR -> Detalhes do PR**: `GITHUB_FIND_PULL_REQUESTS` depois `GITHUB_GET_A_PULL_REQUEST`
- **Nome do branch -> SHA**: `GITHUB_GET_A_BRANCH`
- **Nome do workflow -> ID**: `GITHUB_LIST_REPOSITORY_WORKFLOWS`

### Paginação
Todos os endpoints de listagem usam paginação baseada em página:
- `page`: Número da página (começa em 1)
- `per_page`: Resultados por página (máximo 100)
- Itere até que a resposta retorne menos resultados que `per_page`

### Segurança
- Sempre verifique o status de mergeabilidade do PR antes de fazer merge
- Exija confirmação explícita do usuário para operações destrutivas (merge, delete)
- Verifique o status de CI com `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` antes de fazer merge

## Armadilhas Conhecidas

- **Issues vs PRs**: `GITHUB_LIST_REPOSITORY_ISSUES` retorna ambos; verifique o campo `pull_request`
- **Limites de paginação**: `per_page` máximo 100; sempre itere páginas até ficar vazia
- **Criação de branch**: `GITHUB_CREATE_A_REFERENCE` falha com 422 se a referência já existe
- **Guardas de merge**: Merge pode falhar devido a proteção de branch, checks falhando ou status draft
- **Limites de pesquisa de código**: Apenas arquivos <384KB no branch padrão; máximo 1000 resultados
- **Pesquisa de commit**: Requer keywords de texto de pesquisa além de qualificadores
- **Ações destrutivas**: Exclusão de repositório é irreversível; merge não pode ser desfeito
- **Descartes silenciosos de permissão**: Labels, assignees, milestones silenciosamente descartados sem acesso push

## Referência Rápida

| Tarefa | Tool Slug | Parâmetros Principais |
|--------|-----------|----------------------|
| Listar repositórios | `GITHUB_LIST_REPOSITORIES_FOR_THE_AUTHENTICATED_USER` | `type`, `sort`, `per_page` |
| Obter repositório | `GITHUB_GET_A_REPOSITORY` | `owner`, `repo` |
| Criar issue | `GITHUB_CREATE_AN_ISSUE` | `owner`, `repo`, `title`, `body` |
| Listar issues | `GITHUB_LIST_REPOSITORY_ISSUES` | `owner`, `repo`, `state` |
| Encontrar PRs | `GITHUB_FIND_PULL_REQUESTS` | `repo`, `state`, `author` |
| Criar PR | `GITHUB_CREATE_A_PULL_REQUEST` | `owner`, `repo`, `head`, `base`, `title` |
| Fazer merge em PR | `GITHUB_MERGE_A_PULL_REQUEST` | `owner`, `repo`, `pull_number`, `merge_method` |
| Listar branches | `GITHUB_LIST_BRANCHES` | `owner`, `repo` |
| Criar branch | `GITHUB_CREATE_A_REFERENCE` | `owner`, `repo`, `ref`, `sha` |
| Pesquisar código | `GITHUB_SEARCH_CODE` | `q` |
| Listar commits | `GITHUB_LIST_COMMITS` | `owner`, `repo`, `author`, `since` |
| Pesquisar commits | `GITHUB_SEARCH_COMMITS_BY_AUTHOR` | `q` |
| Listar workflows | `GITHUB_LIST_REPOSITORY_WORKFLOWS` | `owner`, `repo` |
| Disparar workflow | `GITHUB_CREATE_A_WORKFLOW_DISPATCH_EVENT` | `owner`, `repo`, `workflow_id`, `ref` |
| Verificar CI | `GITHUB_LIST_CHECK_RUNS_FOR_A_REF` | `owner`, `repo`, ref |
| Listar colaboradores | `GITHUB_LIST_REPOSITORY_COLLABORATORS` | `owner`, `repo` |
| Proteção de branch | `GITHUB_GET_BRANCH_PROTECTION` | `owner`, `repo`, `branch` |

## Quando Usar
Esta skill é aplicável para executar o workflow ou ações descritos na visão geral.