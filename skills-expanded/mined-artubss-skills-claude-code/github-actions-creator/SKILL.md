---
name: github-actions-creator
description: "Use quando o usuário quiser criar, gerar ou configurar um workflow do GitHub Actions. Lida com pipelines CI/CD, testes, deployment, linting, scanning de segurança, automação de releases, builds Docker, tarefas agendadas e qualquer workflow customizado para qualquer linguagem ou framework."
---

# Criador de GitHub Actions

Você é um especialista em criar workflows do GitHub Actions. Quando o usuário pedir para criar uma GitHub Action, siga este processo estruturado para entregar um arquivo de workflow pronto para produção.

## Processo de Criação de Workflow

### Passo 1: Analisar o Projeto

Antes de escrever qualquer YAML, escaneie o projeto para entender a stack:

1. **Verifique indicadores de linguagem/framework:**
   - `package.json` → Node.js (verifique React, Next.js, Vue, Angular, Svelte, etc.)
   - `requirements.txt` / `pyproject.toml` / `setup.py` → Python
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `pom.xml` / `build.gradle` → Java/Kotlin
   - `Gemfile` → Ruby
   - `composer.json` → PHP
   - `pubspec.yaml` → Dart/Flutter
   - `Package.swift` → Swift
   - `*.csproj` / `*.sln` → .NET

2. **Verifique CI/CD existente:**
   - `.github/workflows/` → workflows existentes (evite conflitos)
   - `Dockerfile` → builds em container disponíveis
   - `docker-compose.yml` → setup multi-serviço
   - `vercel.json` / `netlify.toml` → alvo de deployment
   - `terraform/` / `pulumi/` → infrastructure as code

3. **Verifique tooling:**
   - `.eslintrc*` / `eslint.config.*` → ESLint configurado
   - `prettier*` → Prettier configurado
   - `jest.config*` / `vitest.config*` / `pytest.ini` → framework de testes
   - `.env.example` → variáveis de ambiente necessárias
   - `Makefile` → comandos de build disponíveis

### Passo 2: Fazer Perguntas de Esclarecimento (se necessário)

Se a solicitação do usuário for ambígua, faça UMA pergunta focada. Esclarecimentos comuns:

- **"Criar um pipeline CI"** → "Deve executar apenas testes, ou também lint e type-check?"
- **"Adicionar deployment"** → "Onde faz deploy? (Vercel, AWS, GCP, Docker Hub, etc.)"
- **"Configurar testes"** → "Testes devem rodar em PR apenas, ou também em push para main?"

Se a intenção for clara, pule este passo e prossiga.

### Passo 3: Gerar o Workflow

Crie o arquivo `.github/workflows/{nome}.yml` seguindo estas regras:

#### Nomeação de Arquivo
- Use nomes descritivos em kebab-case: `ci.yml`, `deploy-production.yml`, `release.yml`
- Para CI simples: `ci.yml`
- Para deployment: `deploy.yml` ou `deploy-{target}.yml`
- Para tarefas agendadas: `scheduled-{task}.yml`

#### Regras de Estrutura YAML

```yaml
name: Human-readable name        # Sempre inclua

on:                               # Use as triggers mais específicas
  push:
    branches: [main]              # Especifique branches explicitamente
    paths-ignore:                 # Ignore mudanças apenas de docs quando apropriado
      - '**.md'
      - 'docs/**'
  pull_request:
    branches: [main]

permissions:                      # Sempre defina permissões mínimas
  contents: read

concurrency:                      # Evite execuções duplicadas em PRs
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  job-name:
    runs-on: ubuntu-latest        # Padrão: ubuntu-latest
    timeout-minutes: 15           # Sempre defina um timeout
    steps:
      - uses: actions/checkout@v4 # Sempre fixe na versão major
```

## Padrões Principais por Caso de Uso

### CI (Teste + Lint)

**Trigger:** `pull_request` + `push` para main
**Jobs:** lint, test (paralelo quando possível)
**Recursos principais:** cache de dependências, testes em matriz para múltiplas versões

### Deployment

**Trigger:** `push` para main (ou tags de release)
**Jobs:** test → build → deploy (sequencial com `needs`)
**Recursos principais:** proteção de environment, secrets para credenciais, status checks

### Release / Publish

**Trigger:** `push` tags correspondendo a `v*` ou `workflow_dispatch`
**Jobs:** test → build → publish → criar GitHub Release
**Recursos principais:** geração de changelog, upload de artifacts, npm/PyPI/Docker publish

### Tarefas Agendadas

**Trigger:** `schedule` com expressão cron
**Jobs:** job único com a tarefa
**Recursos principais:** `workflow_dispatch` para trigger manual também, notificações de falha

### Security Scanning

**Trigger:** `pull_request` + `schedule` (semanalmente)
**Jobs:** auditoria de dependências, SAST, scanning de secrets
**Recursos principais:** upload SARIF para aba de segurança do GitHub, falhar em crítico

### Docker Build & Push

**Trigger:** `push` para main + tags
**Jobs:** build → push para registry
**Recursos principais:** builds multi-plataforma, cache de camadas, estratégia de tagging

## Referência de Actions Essenciais

### Setup Actions (sempre fixe na versão major)
| Action | Propósito |
|--------|---------|
| `actions/checkout@v4` | Clonar repositório |
| `actions/setup-node@v4` | Node.js com cache |
| `actions/setup-python@v5` | Python com cache |
| `actions/setup-go@v5` | Go com cache |
| `actions/setup-java@v4` | Java/Kotlin |
| `dtolnay/rust-toolchain@stable` | Rust toolchain |
| `ruby/setup-ruby@v1` | Ruby com bundler cache |
| `actions/setup-dotnet@v4` | .NET SDK |

### Build & Deploy Actions
| Action | Propósito |
|--------|---------|
| `docker/build-push-action@v6` | Docker builds multi-plataforma |
| `docker/login-action@v3` | Autenticação de registry Docker |
| `aws-actions/configure-aws-credentials@v4` | Autenticação AWS |
| `google-github-actions/auth@v2` | Autenticação GCP |
| `azure/login@v2` | Autenticação Azure |
| `cloudflare/wrangler-action@v3` | Deploy Cloudflare Workers |
| `amondnet/vercel-action@v25` | Deploy Vercel |

### Quality & Security Actions
| Action | Propósito |
|--------|---------|
| `github/codeql-action/analyze@v3` | CodeQL SAST scanning |
| `aquasecurity/trivy-action@master` | Scan vulnerabilidade de container |
| `codecov/codecov-action@v4` | Upload de cobertura |
| `actions/dependency-review-action@v4` | Auditoria de dependências em PRs |

### Utility Actions
| Action | Propósito |
|--------|---------|
| `actions/cache@v4` | Cache genérico |
| `actions/upload-artifact@v4` | Armazenar artifacts de build |
| `actions/download-artifact@v4` | Recuperar artifacts entre jobs |
| `softprops/action-gh-release@v2` | Criar GitHub Releases |
| `slackapi/slack-github-action@v2` | Notificações Slack |
| `peter-evans/create-pull-request@v7` | Criação automatizada de PR |

## Melhores Práticas de Segurança (SEMPRE siga)

1. **Permissões mínimas:** Sempre declare `permissions` em nível de workflow ou job
2. **Fixe actions na versão major:** Use `@v4` não `@main` ou SHA completo para legibilidade
3. **Nunca exiba secrets:** Secrets são mascarados mas evite `echo ${{ secrets.X }}`
4. **Use environments:** Para deploys em produção, use GitHub Environments com regras de proteção
5. **Valide inputs:** Para `workflow_dispatch`, valide valores de input
6. **Evite script injection:** Nunca use `${{ github.event.*.body }}` diretamente em `run:` — passe via variáveis de ambiente
7. **Use GITHUB_TOKEN:** Prefira `${{ secrets.GITHUB_TOKEN }}` sobre PATs quando possível
8. **Controles de concorrência:** Use `concurrency` para evitar deploys paralelos

```yaml
# ERRADO - vulnerabilidade de script injection
- run: echo "${{ github.event.issue.title }}"

# CORRETO - passe através de variável de ambiente
- run: echo "$ISSUE_TITLE"
  env:
    ISSUE_TITLE: ${{ github.event.issue.title }}
```

## Estratégias de Cache

### Node.js
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'npm'  # ou 'yarn' ou 'pnpm'
```

### Python
```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.12'
    cache: 'pip'  # ou 'poetry' ou 'pipenv'
```

### Go
```yaml
- uses: actions/setup-go@v5
  with:
    go-version: '1.22'
    cache: true
```

### Rust
```yaml
- uses: actions/cache@v4
  with:
    path: |
      ~/.cargo/bin/
      ~/.cargo/registry/index/
      ~/.cargo/registry/cache/
      target/
    key: ${{ runner.os }}-cargo-${{ hashFiles('**/Cargo.lock') }}
```

### Docker
```yaml
- uses: docker/build-push-action@v6
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Padrões de Testes em Matriz

### Múltiplas versões Node.js
```yaml
strategy:
  matrix:
    node-version: [18, 20, 22]
  fail-fast: false
```

### Múltiplos SOs
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, macos-latest, windows-latest]
runs-on: ${{ matrix.os }}
```

### Matriz complexa com exclusões
```yaml
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest]
    node-version: [18, 20]
    exclude:
      - os: windows-latest
        node-version: 18
```

## Referência Rápida de Sintaxe Cron

| Agendamento | Cron |
|----------|------|
| A cada hora | `0 * * * *` |
| Diariamente à meia-noite UTC | `0 0 * * *` |
| Dias úteis às 9am UTC | `0 9 * * 1-5` |
| Semanalmente no domingo | `0 0 * * 0` |
| Mensalmente no 1º | `0 0 1 * *` |

## Formato de Saída

Depois de criar o arquivo de workflow, forneça:

1. **O que o workflow faz** — resumo de um parágrafo
2. **Secrets necessários** — liste qualquer secret que o usuário precisa configurar em Settings > Secrets
3. **Permissões necessárias** — se o workflow precisa de permissões não-padrão do repositório
4. **Como testar** — como disparar o workflow (push, criar PR, dispatch manual)

## Padrões Comuns para Combinar

Quando o usuário pedir algo genérico como "configurar CI/CD", crie um workflow único com múltiplos jobs:

```yaml
jobs:
  lint:        # Feedback rápido
  test:        # Validação principal
  build:       # Certifique-se que compila/bundla
    needs: [lint, test]
  deploy:      # Apenas após tudo passar
    needs: build
    if: github.ref == 'refs/heads/main'
```

Mantenha workflows focados. Prefira um workflow por concern sobre um workflow massivo, a menos que os jobs estejam fortemente acoplados.