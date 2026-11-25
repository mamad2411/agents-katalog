---
name: dependency-updater
description: Gerenciamento inteligente de dependências para qualquer linguagem. Auto-detecção de tipo de projeto, aplicação de atualizações seguras automaticamente, solicitação de confirmação para versões principais, diagnóstico e correção de problemas de dependências.
license: MIT
metadata:
  version: 1.0.0
---

# Atualizador de Dependências

Gerenciamento inteligente de dependências para qualquer linguagem com detecção automática e atualizações seguras.

---

## Início Rápido

```
update my dependencies
```

O skill detecta automaticamente o tipo de projeto e cuida do resto.

---

## Acionadores

| Acionador | Exemplo |
|---------|---------|
| Atualizar dependências | "update dependencies", "update deps" |
| Verificar desatualizados | "check for outdated packages" |
| Corrigir problemas de dependências | "fix my dependency problems" |
| Auditoria de segurança | "audit dependencies for vulnerabilities" |
| Diagnosticar deps | "diagnose dependency issues" |

---

## Linguagens Suportadas

| Linguagem | Arquivo de Pacote | Ferramenta de Atualização | Ferramenta de Auditoria |
|----------|--------------|-------------|------------|
| **Node.js** | package.json | `taze` | `npm audit` |
| **Python** | requirements.txt, pyproject.toml | `pip-review` | `safety`, `pip-audit` |
| **Go** | go.mod | `go get -u` | `govulncheck` |
| **Rust** | Cargo.toml | `cargo update` | `cargo audit` |
| **Ruby** | Gemfile | `bundle update` | `bundle audit` |
| **Java** | pom.xml, build.gradle | `mvn versions:*` | `mvn dependency:*` |
| **.NET** | *.csproj | `dotnet outdated` | `dotnet list package --vulnerable` |

---

## Referência Rápida

| Tipo de Atualização | Mudança de Versão | Ação |
|-------------|----------------|--------|
| **Fixo** | Sem `^` ou `~` | Pular (intencionalmente fixado) |
| **PATCH** | `x.y.z` → `x.y.Z` | Aplicar automaticamente |
| **MINOR** | `x.y.z` → `x.Y.0` | Aplicar automaticamente |
| **MAJOR** | `x.y.z` → `X.0.0` | Solicitar confirmação individual do usuário |

---

## Fluxo de Trabalho

```
Solicitação do Usuário
    │
    ▼
┌─────────────────────────────────────────────────────┐
│ Etapa 1: DETECTAR TIPO DE PROJETO                   │
│ • Verificar arquivos de pacote (package.json, go.mod...) │
│ • Identificar gerenciador de pacotes                │
├─────────────────────────────────────────────────────┤
│ Etapa 2: VERIFICAR PRÉ-REQUISITOS                   │
│ • Validar que ferramentas obrigatórias estão instaladas │
│ • Sugerir instalação se faltarem                    │
├─────────────────────────────────────────────────────┤
│ Etapa 3: PROCURAR POR ATUALIZAÇÕES                  │
│ • Executar verificação específica da linguagem      │
│ • Categorizar: MAJOR / MINOR / PATCH / Fixo        │
├─────────────────────────────────────────────────────┤
│ Etapa 4: APLICAR ATUALIZAÇÕES SEGURAS               │
│ • Aplicar MINOR e PATCH automaticamente             │
│ • Relatar o que foi atualizado                      │
├─────────────────────────────────────────────────────┤
│ Etapa 5: SOLICITAR ATUALIZAÇÕES PRINCIPAIS          │
│ • Fazer pergunta ao usuário para cada atualização MAJOR │
│ • Mostrar versão atual → nova versão                │
├─────────────────────────────────────────────────────┤
│ Etapa 6: APLICAR PRINCIPAIS APROVADAS               │
│ • Atualizar apenas pacotes aprovados                │
├─────────────────────────────────────────────────────┤
│ Etapa 7: FINALIZAR                                  │
│ • Executar comando de instalação                    │
│ • Executar auditoria de segurança                   │
└─────────────────────────────────────────────────────┘
```

---

## Comandos por Linguagem

### Node.js (npm/yarn/pnpm)

```bash
# Verificar pré-requisitos
scripts/check-tool.sh taze "npm install -g taze"

# Procurar por atualizações
taze

# Aplicar minor/patch
taze minor --write

# Aplicar majors específicos
taze major --write --include pkg1,pkg2

# Suporte a monorepo
taze -r  # recursive

# Segurança
npm audit
npm audit fix
```

### Python

```bash
# Verificar desatualizados
pip list --outdated

# Atualizar tudo (cuidado!)
pip-review --auto

# Atualizar específico
pip install --upgrade package-name

# Segurança
pip-audit
safety check
```

### Go

```bash
# Verificar desatualizados
go list -m -u all

# Atualizar tudo
go get -u ./...

# Arrumar
go mod tidy

# Segurança
govulncheck ./...
```

### Rust

```bash
# Verificar desatualizados
cargo outdated

# Atualizar dentro de semver
cargo update

# Segurança
cargo audit
```

### Ruby

```bash
# Verificar desatualizados
bundle outdated

# Atualizar tudo
bundle update

# Atualizar específico
bundle update --conservative gem-name

# Segurança
bundle audit
```

### Java (Maven)

```bash
# Verificar desatualizados
mvn versions:display-dependency-updates

# Atualizar para a mais recente
mvn versions:use-latest-releases

# Segurança
mvn dependency:tree
mvn dependency-check:check
```

### .NET

```bash
# Verificar desatualizados
dotnet list package --outdated

# Atualizar específico
dotnet add package PackageName

# Segurança
dotnet list package --vulnerable
```

---

## Modo Diagnóstico

Quando as dependências quebram, execute o diagnóstico:

### Problemas Comuns e Soluções

| Problema | Sintomas | Solução |
|-------|----------|-----|
| **Conflito de Versão** | "Cannot resolve dependency tree" | Limpeza completa, usar overrides/resolutions |
| **Peer Dependency** | "Peer dependency not satisfied" | Instalar versão requerida de peer dependency |
| **Vulnerabilidade de Segurança** | `npm audit` mostra problemas | `npm audit fix` ou atualização manual |
| **Deps Não Utilizadas** | Bundle inchado | Executar `depcheck` (Node) ou equivalente |
| **Deps Duplicadas** | Múltiplas versões instaladas | Executar `npm dedupe` ou equivalente |

### Correções de Emergência

```bash
# Node.js - Reset completo
rm -rf node_modules package-lock.json
npm cache clean --force
npm install

# Python - Limpar virtualenv
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Go - Resetar módulos
rm go.sum
go mod tidy
```

---

## Auditoria de Segurança

Execute verificações de segurança para qualquer projeto:

```bash
# Node.js
npm audit
npm audit --json | jq '.metadata.vulnerabilities'

# Python
pip-audit
safety check

# Go
govulncheck ./...

# Rust
cargo audit

# Ruby
bundle audit

# .NET
dotnet list package --vulnerable
```

### Resposta por Severidade

| Severidade | Ação |
|----------|--------|
| **Crítica** | Corrigir imediatamente |
| **Alta** | Corrigir em 24h |
| **Moderada** | Corrigir em 1 semana |
| **Baixa** | Corrigir na próxima release |

---

## Anti-padrões

| Evitar | Por Quê | No Lugar Disso |
|-------|-----|---------|
| Atualizar versões fixas | Intencionalmente fixadas | Pular |
| Auto-aplicar MAJOR | Mudanças quebradoras | Solicitar ao usuário |
| Agrupar prompts de MAJOR | Perder contexto | Solicitar individualmente |
| Pular arquivo de lock | Builds não reproduzíveis | Sempre fazer commit do arquivo de lock |
| Ignorar alertas de segurança | Vulnerabilidades | Endereçar por severidade |

---

## Checklist de Verificação

Após atualizações:

- [ ] Atualizações verificadas sem erros
- [ ] MINOR/PATCH auto-aplicadas
- [ ] Atualizações MAJOR solicitadas individualmente
- [ ] Versões fixas intactas
- [ ] Arquivo de lock atualizado
- [ ] Comando de instalação executado
- [ ] Auditoria de segurança passou (ou problemas foram observados)

---

<details>
<summary><strong>Aprofundamento: Detecção de Projeto</strong></summary>

O skill detecta automaticamente o tipo de projeto verificando arquivos de pacote:

| Arquivo Encontrado | Linguagem | Gerenciador de Pacotes |
|------------|----------|-----------------|
| `package.json` | Node.js | npm/yarn/pnpm |
| `requirements.txt` | Python | pip |
| `pyproject.toml` | Python | pip/poetry |
| `Pipfile` | Python | pipenv |
| `go.mod` | Go | go modules |
| `Cargo.toml` | Rust | cargo |
| `Gemfile` | Ruby | bundler |
| `pom.xml` | Java | Maven |
| `build.gradle` | Java/Kotlin | Gradle |
| `*.csproj` | .NET | dotnet |

**A ordem de detecção importa para monorepos:**
1. Verificar diretório atual primeiro
2. Depois verificar padrões de workspace/monorepo
3. Oferecer executar recursivamente se aplicável

</details>

<details>
<summary><strong>Aprofundamento: Node.js com taze</strong></summary>

### Pré-requisitos

```bash
# Instalar taze globalmente (recomendado)
npm install -g taze

# Ou usar npx
npx taze
```

### Fluxo de Atualização Inteligente

```bash
# 1. Verificar todas as atualizações
taze

# 2. Aplicar atualizações seguras (minor + patch)
taze minor --write

# 3. Para cada major, solicitar ao usuário:
#    "Update @types/node from ^20.0.0 to ^22.0.0?"
#    Se sim, adicionar à lista aprovada

# 4. Aplicar majors aprovadas
taze major --write --include approved-pkg1,approved-pkg2

# 5. Instalar
npm install  # or pnpm install / yarn
```

### Lista de Auto-Aprovação

Alguns pacotes têm bumps de major frequentes mas são retrocompatíveis:

| Pacote | Motivo |
|---------|--------|
| `lucide-react` | Biblioteca de ícones, majors são aditivos |
| `@types/*` | Definições de tipos, geralmente seguras |

</details>

<details>
<summary><strong>Aprofundamento: Estratégias de Versionamento</strong></summary>

### Semantic Versioning

```
MAJOR.MINOR.PATCH (ex: 2.3.1)

MAJOR: Mudanças quebradoras - requer alterações de código
MINOR: Novas funcionalidades - retrocompatível
PATCH: Correções de bug - retrocompatível
```

### Especificadores de Intervalo

| Especificador | Significado | Exemplo |
|-----------|---------|---------|
| `^1.2.3` | Minor + Patch OK | `>=1.2.3 <2.0.0` |
| `~1.2.3` | Apenas Patch | `>=1.2.3 <1.3.0` |
| `1.2.3` | Exato (fixo) | Apenas `1.2.3` |
| `>=1.2.3` | Pelo menos | Qualquer `>=1.2.3` |
| `*` | Qualquer | Mais recente (perigoso) |

### Estratégia Recomendada

```json
{
  "dependencies": {
    "critical-lib": "1.2.3",      // Exato para crítico
    "stable-lib": "~1.2.3",       // Apenas patch para estável
    "modern-lib": "^1.2.3"        // Minor OK para ativo
  }
}
```

</details>

<details>
<summary><strong>Aprofundamento: Resolução de Conflitos</strong></summary>

### Conflitos do Node.js

**Diagnóstico:**
```bash
npm ls package-name      // Ver árvore de dependências
npm explain package-name // Por que foi instalado
yarn why package-name    // Equivalente Yarn
```

**Resolução com overrides:**
```json
// package.json
{
  "overrides": {
    "lodash": "^4.18.0"
  }
}
```

**Resolução com resolutions (Yarn):**
```json
{
  "resolutions": {
    "lodash": "^4.18.0"
  }
}
```

### Conflitos do Python

**Diagnóstico:**
```bash
pip check
pipdeptree -p package-name
```

**Resolução:**
```bash
# Usar ambiente virtual
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Ou usar constraints
pip install -c constraints.txt -r requirements.txt
```

</details>

---

## Referência de Script

| Script | Finalidade |
|--------|---------|
| `scripts/check-tool.sh` | Validar se ferramenta está instalada |
| `scripts/run-taze.sh` | Executar taze com flags apropriadas |

---

## Ferramentas Relacionadas

| Ferramenta | Linguagem | Finalidade |
|------|----------|---------|
| [taze](https://github.com/antfu-collective/taze) | Node.js | Atualizações inteligentes de dependências |
| [npm-check-updates](https://github.com/raineorshine/npm-check-updates) | Node.js | Alternativa ao taze |
| [pip-review](https://github.com/jgonggrijp/pip-review) | Python | Atualizações interativas de pip |
| [cargo-edit](https://github.com/killercup/cargo-edit) | Rust | Gerenciamento de dependências Cargo |
| [bundler-audit](https://github.com/rubysec/bundler-audit) | Ruby | Auditoria de segurança |