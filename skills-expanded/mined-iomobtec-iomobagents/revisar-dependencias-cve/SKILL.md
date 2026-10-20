---
name: revisar-dependencias-cve
description: "Verifica CVEs em package.json, lockfile e Dockerfiles e inspeciona scripts postinstall de novas dependências. Use quando o dev-security ou o dev-devops vai avaliar o risco de dependências."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: revisar-dependencias-cve

Verificação de CVEs e de scripts postinstall em dependências e imagens Docker alteradas em um PR.

**Agente:** `dev-security`, `dev-devops`  
**Output:** Seção "Dependências" do relatório de segurança, com lista de CVEs e ação recomendada.

---

## Quando usar

Sempre que `package.json`, `package-lock.json` ou `Dockerfile` forem alterados em um PR. Executar como parte da auditoria pré-merge junto com `auditar-seguranca`.

---

## Processo

### Passo 1 — Verificar se há mudança de dependências

```bash
# Verificar se package.json ou lockfile foram alterados no PR
git diff --name-only HEAD~1 | grep -E "package(-lock)?\.json|yarn\.lock|Dockerfile"
```

Se nenhum desses arquivos foi alterado, esta skill pode ser pulada. Registrar no relatório: "Dependências sem alteração neste PR — auditoria de CVE não aplicável."

### Passo 2 — Executar auditoria de dependências npm

```bash
# Audit com nível mínimo moderate (retorna CRITICAL, HIGH e MEDIUM)
npm audit --audit-level=moderate

# Saída detalhada em JSON para análise
npm audit --json > audit-report.json

# Verificar dependências desatualizadas
npm outdated
```

### Passo 3 — Executar auditoria de imagem Docker (se Dockerfile alterado)

```bash
# Com Trivy (se disponível na organização)
trivy image --severity HIGH,CRITICAL <imagem>:<tag>

# Com Docker Scout (se disponível)
docker scout cves <imagem>:<tag>

# Verificar se imagem base está versionada
grep "^FROM" Dockerfile
# Alerta se: FROM node:latest | FROM node:lts | FROM node (sem tag)
```

### Passo 4 — Verificar scripts de novas dependências

Para cada dependência adicionada no PR (nova entrada em `package.json`):

```bash
# Inspecionar scripts de instalação da nova dep
cat node_modules/<nova-dep>/package.json | grep -A 10 '"scripts"'

# Verificar se a dependência faz download de binário externo no postinstall
cat node_modules/<nova-dep>/package.json | grep -i "postinstall"
```

**Sinalizações de risco:**
- `postinstall` com `curl`, `wget`, `fetch`, `axios` ou `node-fetch` baixando conteúdo externo
- `postinstall` executando binário pré-compilado sem checksum
- Dependência apontando para repositório GitHub diretamente (não npm registry): `"dep": "github:user/repo"`

### Passo 5 — Verificar lockfile

```bash
# Verificar integridade do lockfile (deve passar sem erro)
npm ci --dry-run

# Verificar se lockfile está commitado e atualizado
git status package-lock.json
# NÃO deve aparecer como modificado fora do contexto do PR
```

### Passo 6 — Classificar e reportar

Para cada CVE encontrado, reportar:

```
<severidade emoji>
**CVE:** CVE-YYYY-NNNNN
**Pacote:** <nome>@<versão atual>
**Severidade CVSS:** <score> — <CRITICAL | HIGH | MEDIUM | LOW>
**Descrição:** <resumo do vetor de ataque>
**Fix disponível:** <versão corrigida | sem fix disponível>
**Ação:** <upgrade para X.Y.Z | remover dependência | aguardar fix — ver §6.3 do guideline>
**Afeta produção?** <Sim — dependência de runtime | Não — devDependency>
```

### Tabela de ação por severidade

| Severidade CVE | Afeta produção | Ação |
|---|---|---|
| CRITICAL | Sim | Bloqueia merge. Corrigir antes. Se sem fix: arquiteto aprova exceção. |
| CRITICAL | Não (dev only) | HIGH — registrar issue com prazo 7 dias. |
| HIGH | Sim | Bloqueia merge. Plano de correção com prazo ≤ 7 dias. |
| HIGH | Não (dev only) | MEDIUM — registrar issue com prazo 30 dias. |
| MEDIUM | Qualquer | Issue no repositório. Prazo ≤ 30 dias. Não bloqueia merge. |
| LOW | Qualquer | Issue no repositório. Próximo ciclo de manutenção. |

### Passo 7 — Emitir seção no relatório

```markdown
## Dependências e Supply Chain

### npm audit

| Pacote | CVE | CVSS | Afeta produção? | Fix | Ação |
|---|---|---|---|---|---|
| express@4.18.1 | CVE-2024-XXXX | 9.1 CRITICAL | Sim | 4.19.0 | Upgrade urgente — bloqueia merge |
| jest@29.0.0 | CVE-2024-YYYY | 6.5 MEDIUM | Não (dev) | 29.1.0 | Issue #XX — prazo 30 dias |

### Imagem Docker

| Item | Status |
|---|---|
| Imagem base versionada | ✅ `node:20.11-alpine3.19` |
| Scan de CVEs na imagem | 🟠 HIGH: libssl@3.0.1 (CVE-2024-ZZZ) — upgrade base image |

### Novas dependências (scripts inspecionados)

| Pacote | postinstall | Risco |
|---|---|---|
| `zod@3.22.4` | Nenhum | ✅ Seguro |
| `sharp@0.33.0` | Baixa binário pré-compilado | 🟡 Verificar checksum — ver issue #YY |

### Lockfile

| Verificação | Status |
|---|---|
| `npm ci` sem erro | ✅ |
| Lockfile commitado e atualizado | ✅ |
```

---

## Anti-padrões bloqueados

- Marcar CVE de dependência de runtime como "não afeta produção" sem verificar se é devDependency real
- Ignorar CVE CRITICAL alegando que "o vetor de exploit não se aplica" sem aprovação do arquiteto
- Não inspecionar scripts `postinstall` de dependências novas
- Reportar `npm audit` com `--audit-level=critical` apenas (omite HIGH e MEDIUM intencionalmente)
- Aceitar `FROM node:latest` sem registrar como finding
