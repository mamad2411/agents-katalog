---
name: tdd-validation
description: Validação de Technical Design Documents. Verifica completude, identifica gaps e cruza com arquitetura do projeto.
allowed-tools: Read, Glob, Grep
---

# TDD Validation Skill

> Valida Technical Design Documents antes da implementação.

---

## 1. Overview

Este skill permite validar TDDs (Technical Design Documents) para garantir que estão completos e prontos para implementação.

### Quando Usar
- Antes de aprovar um TDD para implementação
- Quando o `/tdd validate` é executado
- Como parte do pipeline de revisão

---

## 2. Validation Categories

### 2.1 Estrutura (Seções Obrigatórias)

| Seção | Obrigatória? | Peso |
|-------|--------------|------|
| Informações Gerais | ✅ Sim | 5% |
| Contexto e Motivação | ✅ Sim | 10% |
| Glossário | ✅ Sim | 10% |
| Recursos e APIs Externas | 🟡 Se aplicável | 10% |
| Fluxo Técnico - MVP | ✅ Sim | 20% |
| Detalhamento da Solução | ✅ Sim | 20% |
| **Environment Strategy** | ✅ Sim ⭐ | 5% |
| Riscos e Mitigação | ✅ Sim | 10% |
| Roadmap | ✅ Sim | 5% |
| Checklist de Validação | ✅ Sim | 5% |

### 2.2 Conteúdo (Qualidade)

| Verificação | Critério |
|-------------|----------|
| **MVP Definido** | Pelo menos 1 item marcado como `✅ DEFINIDO` |
| **Sem Bloqueadores** | Nenhum `⚠️ INDEFINIDO` em tasks críticas |
| **Fluxo Documentado** | Diagrama mermaid presente |
| **APIs Mapeadas** | Endpoints listados se houver integração |
| **Riscos Mitigados** | Cada risco tem ação de mitigação |
| **Ambientes Separados** ⭐ | Seção `Environment Strategy` define dev vs prod |

### 2.3 Alinhamento Arquitetural

| Verificação | Fonte |
|-------------|-------|
| **Stack Compatível** | Cruza com `CODEBASE.md` ou `package.json` |
| **Padrões Seguidos** | Cruza com `ARCHITECTURE.md` |
| **Dependências Válidas** | Bibliotecas existem e são compatíveis |

---

## 3. Validation Algorithm

```
FUNCTION validate_tdd(file_path):
    tdd = READ(file_path)
    score = 0
    issues = []
    
    # 1. Check structure
    FOR section IN required_sections:
        IF section NOT IN tdd:
            issues.append(MISSING: section)
        ELSE:
            score += section.weight
    
    # 2. Check MVP items
    defined_items = COUNT(tdd, status="DEFINIDO")
    undefined_items = COUNT(tdd, status="INDEFINIDO")
    
    IF defined_items == 0:
        issues.append(BLOCKER: "No MVP items defined")
    
    IF undefined_items > 0:
        FOR item IN undefined_items:
            IF item.is_critical:
                issues.append(BLOCKER: item)
            ELSE:
                issues.append(WARNING: item)
    
    # 3. Check architecture alignment
    IF EXISTS("ARCHITECTURE.md"):
        arch = READ("ARCHITECTURE.md")
        mismatches = COMPARE(tdd.tech_stack, arch.tech_stack)
        issues.extend(mismatches)
    
    # 4. Calculate readiness
    readiness = score / max_score * 100
    IF any(issues.type == BLOCKER):
        status = "NOT_READY"
    ELIF readiness >= 80:
        status = "READY"
    ELSE:
        status = "NEEDS_WORK"
    
    RETURN ValidationReport(score, issues, status)
```

---

## 4. Output Format

### Validation Report Structure

```markdown
# TDD Validation Report

**File:** docs/design/TDD-{name}.md
**Date:** YYYY-MM-DD
**Status:** [READY | NEEDS_WORK | NOT_READY]
**Score:** XX%

---

## ✅ Passed Checks

- [x] Contexto e Motivação presente
- [x] Glossário definido
- [x] MVP com 5 itens DEFINIDO

---

## ⚠️ Warnings

- [ ] Tratamento de Erros marcado como INDEFINIDO
- [ ] Roadmap sem datas específicas

---

## ❌ Blockers

- [ ] Seção "Riscos e Mitigação" ausente
- [ ] Nenhum diagrama de fluxo

---

## 📊 Summary

| Categoria | Status |
|-----------|--------|
| Estrutura | 80% |
| Conteúdo | 70% |
| Arquitetura | 100% |
| **Total** | **83%** |

---

## 🎯 Recommendations

1. **P0:** Adicionar seção de Riscos
2. **P1:** Criar diagrama mermaid do fluxo
3. **P2:** Definir datas no Roadmap
```

---

## 5. Status Definitions

| Status | Significado | Ação |
|--------|-------------|------|
| `READY` | TDD completo e pronto | Pode aprovar |
| `NEEDS_WORK` | Pequenos ajustes necessários | Corrigir warnings |
| `NOT_READY` | Bloqueadores críticos | Resolver antes de prosseguir |

---

## 6. Integration Points

### Com Outros Skills
| Skill | Integração |
|-------|------------|
| `brainstorming` | Validação invoca se TDD incompleto |
| `plan-writing` | Recebe TDD validado para breakdown |
| `architecture` | Cruza TDD com padrões do projeto |

### Com Agentes
| Agente | Papel |
|--------|-------|
| `tdd-reviewer` | Executa validação |
| `project-planner` | Recebe resultado para planning |

---

## 7. Best Practices

### Para Quem Escreve TDD
1. **Preencha todas as seções** - Não deixe placeholders
2. **Seja explícito sobre MVP** - Marque status de cada item
3. **Documente riscos** - Mesmo os óbvios
4. **Use diagramas** - Mermaid para fluxos

### Para Validação
1. **Não auto-aprovar** - Sempre revisão humana
2. **Bloqueador = Stop** - Não prosseguir com blockers
3. **Warnings são importantes** - Resolver antes de implementar
4. **Re-validar após mudanças** - TDD é vivo até aprovação

---

## 8. Checklist Rápido

```markdown
## Quick Validation Checklist

### Estrutura
- [ ] Título e metadados preenchidos
- [ ] Contexto explica o "porquê"
- [ ] Glossário define termos de domínio
- [ ] Fluxo técnico com diagrama
- [ ] Tarefas com status (DEFINIDO/INDEFINIDO)
- [ ] Riscos com mitigações
- [ ] Roadmap com datas

### MVP
- [ ] Pelo menos 3 itens DEFINIDO
- [ ] Nenhum INDEFINIDO crítico
- [ ] Fora de escopo marcado

### Qualidade
- [ ] Revisado por Tech Lead
- [ ] Revisado por PM
- [ ] Alinhado com arquitetura

### Environment Strategy ⭐
- [ ] Ambientes listados (dev/staging/prod)
- [ ] Serviços externos mapeados por ambiente
- [ ] Arquivos `.env` documentados
- [ ] `.env.local` ≠ produção
```

---

> **Lembre-se:** Um TDD bem validado economiza horas de retrabalho na implementação.
