---
name: project-foundation
description: Protocolo para gerar os arquivos de fundação de qualquer projeto (README, .env.example, SECURITY.md, docs/INDEX.md, ADR-000). Usado por new-project (Phase 2.05) e legacy-project (Phase 0.7). Context-aware para projetos novos vs legados.
---

# Skill: project-foundation

## Propósito

Garantir que todo projeto tenha a infraestrutura mínima de documentação **antes** de qualquer trabalho de feature ou análise. Um agente que abrir o projeto futuramente precisa de um ponto de entrada claro.

> [!IMPORTANT]
> Este skill é chamado automaticamente por workflows. Não pule nenhum dos 5 artefatos — todos são necessários para que agentes futuros funcionem corretamente.

---

## Contextos de Uso

| Contexto | Trigger | Comportamento |
|----------|---------|---------------|
| `new` | `new-project` Phase 2.05 | Gera todos os arquivos do zero a partir dos templates |
| `legacy` | `legacy-project` Phase 0.7 | Adapta ao que já existe: README existente é atualizado, `.env.example` é extraído das variáveis detectadas no código |

---

## Protocolo de Execução

### Passo 1: README.md

**Modo `new`:**
> Gerar do zero usando `readme-template.md`. Preencher stack, comandos de run/test/build e environments.

**Modo `legacy`:**
> 1. Verificar se `README.md` já existe
> 2. Se existe: atualizar seções desatualizadas (stack, comandos, envs) sem destruir conteúdo
> 3. Se não existe: gerar do zero como se fosse modo `new`

**Gate:** README deve ter no mínimo: descrição, stack, como rodar localmente, environments.

---

### Passo 2: .env.example

**Modo `new`:**
> Gerar do zero usando `env-template.md`. Preencher com as variáveis já conhecidas (DB, auth, ports).

**Modo `legacy`:**
> 1. Buscar variáveis de ambiente no código (`process.env.*`, `os.environ`, `config(*)`)
> 2. Buscar `.env`, `.env.local`, `.env.development` (se existirem e não estiverem no .gitignore, ler)
> 3. Gerar `.env.example` preenchido com as variáveis encontradas (valores = placeholders)
> 4. Anotar quais são REQUIRED vs OPTIONAL com base no uso

**Gate:** `.env.example` deve cobrir todas as variáveis usadas no código.

---

### Passo 3: SECURITY.md

**Ambos os modos:**
> Gerar usando `security-template.md`. Preencher:
> - Versões suportadas (detectar versão atual do projeto)
> - Email de segurança (perguntar ao usuário se não encontrado no repo)
> - Stack-specific items (ex: se Python → `pip-audit`; se Node → `npm audit`)

**Modo `legacy`:**
> Adicionar nota na seção "Security Practices" sobre dívida de segurança conhecida (a ser preenchida após Phase 5.6).

---

### Passo 4: docs/INDEX.md (Document Registry)

**Ambos os modos:**
> Criar `docs/INDEX.md` usando `docs-index-template.md`.

**Modo `new`:**
> INDEX começa com entries `pending` para todos os documentos que serão gerados pelo workflow.

**Modo `legacy`:**
> INDEX começa vazio (status = pending) e é preenchido incrementalmente conforme documentos são criados.
> Adicionar entry inicial:
> ```
> | LEGACY-ANALYSIS | Analysis | docs/LEGACY-PROGRESS.md | in_progress | - | - |
> ```

**Gate:** `docs/INDEX.md` criado e commitável (não vazio, com pelo menos a entry de foundation).

---

### Passo 5: docs/adr/ADR-000.md

**Modo `new`:**
> Criar `docs/adr/ADR-000-initial-setup.md` documentando as decisões de stack e arquitetura
> iniciais. Status: `accepted`.

**Modo `legacy`:**
> Criar `docs/adr/ADR-000-legacy-analysis.md` documentando a decisão de iniciar engenharia
> reversa. Preencher template com:
> - **Context:** Projeto existente sem documentação
> - **Decision:** Iniciar reverse engineering com `/legacy-project`
> - **Consequences:** Processo incremental por módulo, análise pode levar múltiplas sessões

---

## Checklist de Conclusão

```
[ ] README.md gerado/atualizado
[ ] .env.example gerado (todas as variáveis cobertas)
[ ] SECURITY.md gerado
[ ] docs/INDEX.md criado com entries iniciais
[ ] docs/adr/ADR-000.md criado
[ ] Skill document-registry carregado para registrar cada doc criado acima no INDEX
```

> [!CAUTION]
> **NÃO prosseguir para o próximo workflow step** sem todos os itens marcados.
> Se `docs/` não existir: criar o diretório antes de gerar os arquivos.
