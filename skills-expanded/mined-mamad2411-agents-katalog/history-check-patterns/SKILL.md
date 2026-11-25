---
name: history-check-patterns
description: Consulta de histórico de tasks antes de implementar. Aprende com bugs/features anteriores para evitar erros repetidos.
---

# History Check Patterns

> **Aprenda com o passado** antes de implementar algo novo.

---

## 🎯 PROPÓSITO

Garantir que antes de implementar:
1. **Consultamos** tasks anteriores relacionadas
2. **Identificamos** lições aprendidas
3. **Evitamos** repetir erros

---

## 🔍 QUANDO USAR

| Situação | Obrigatório? |
|----------|--------------|
| Bug em área já trabalhada | ✅ Sim |
| Feature em módulo existente | ✅ Sim |
| Refatoração | ✅ Sim |
| Feature completamente nova | ⚠️ Recomendado |

---

## 📋 PROCESSO DE CONSULTA

### Passo 1: Buscar Tasks Relacionadas

```
Use: Flyee API: list_tasks()
query: "{palavras-chave da demanda}"
filter: { "property": "object", "value": "page" }
```

### Passo 2: Buscar por Categoria (Bugs anteriores)

```
Use: Flyee API: list_tasks()
data_source_id: "{DATABASE_ID}"
filter: {
    "or": [
        { "property": "Categoria", "multi_select": { "contains": "Bug" } },
        { "property": "Categoria", "multi_select": { "contains": "Feature" } }
    ]
}
```

### Passo 3: Analisar Resultados

| Tipo | O que procurar |
|------|----------------|
| **Bugs Resolvidos** | Mesma área? Mesmo componente? |
| **Features Anteriores** | Já implementado algo similar? |
| **Comentários** | Problemas encontrados? Soluções aplicadas? |

---

## 📊 TEMPLATE DE RELATÓRIO

### Se Encontrar Histórico Relevante:

```markdown
📚 **Histórico Encontrado:**

| Task | Tipo | Data | Relevância |
|------|------|------|------------|
| [#123] Auth refactor | Feature | 2025-01-10 | Alta - mesmo módulo |
| [#98] Fix login erro | Bug | 2025-01-05 | Média - pode recorrer |

**Lições aprendidas:**
- Em #123: "Usar middleware novo, não o legado"
- Em #98: "Race condition no token refresh"

**Aplicar:**
- [ ] Verificar se solução de #98 ainda se aplica
- [ ] Seguir padrão estabelecido em #123
```

### Se NÃO Encontrar:

```markdown
✅ Nenhum histórico relevante encontrado para "{demanda}".
Prosseguindo com análise do zero.
```

---

## ✅ GATE DE SAÍDA

```markdown
[ ] Histórico consultado
[ ] Lições identificadas (se houver)
[ ] Checkpoints anteriores verificados
```

> [!CAUTION]
> **NÃO prossiga** para implementação sem completar este gate.

---

## 📝 INCLUIR NO COMENTÁRIO FINAL

Ao finalizar task, incluir seção:

```markdown
📚 **Histórico aplicado:**
- {lições de tasks anteriores usadas}
- {ou "Nenhum histórico relevante"}
```

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Fase |
|----------|------|
| `/new-task` | Fase -1 (HISTORY CHECK) |
| `/legacy-project` | Phase 7 (BREAKDOWN) |
