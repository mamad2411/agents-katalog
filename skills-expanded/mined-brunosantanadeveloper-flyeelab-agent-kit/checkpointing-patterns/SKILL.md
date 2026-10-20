---
name: checkpointing-patterns
description: Sistema de checkpoint/resume para workflows longos. Persistência de estado, retomada de execução, gates de saída por fase.
---

# Checkpointing Patterns

> **Single Source of Truth** para workflows que precisam persistir estado e retomar execução.

---

## 🎯 PROPÓSITO

Garantir que workflows longos:
1. **Salvem progresso** a cada fase
2. **Retomem corretamente** de onde pararam
3. **Mantenham histórico** de ações

---

## 📁 ESTRUTURA DO ARQUIVO DE CHECKPOINT

**Padrão de nome:** `docs/{WORKFLOW}-PROGRESS.md`

| Workflow | Arquivo |
|----------|---------|
| `/new-task` | `docs/NEW-TASK-PROGRESS.md` |
| `/legacy-project` | `docs/LEGACY-PROGRESS.md` |
| `/new-project` | `docs/PROJECT-PROGRESS.md` |

---

## 📋 TEMPLATE PADRÃO

```markdown
# {Workflow} Progress - {nome}

> Arquivo de controle para retomar workflow.
> ⚠️ NÃO EDITAR MANUALMENTE - Atualizado automaticamente.

## 📊 Status Geral

| Campo | Valor |
|-------|-------|
| Nome | {nome} |
| Iniciado em | {data} |
| Última atualização | {data} |
| Status | 🟡 Em Progresso |
| Fase Atual | {N}/{Total} |

---

## 📝 Fases

### Fase 1: {Nome} ✅
- [x] Item 1
- [x] Item 2

### Fase 2: {Nome} 🟡
- [x] Item 1
- [ ] Item 2 ← pendente

### Fase 3: {Nome} ⏳
- [ ] Aguardando

---

## 📜 Histórico de Ações

| Data | Fase | Ação |
|------|------|------|
| {data} | 1 | {ação} |
| {data} | 2 | {ação} |
```

---

## 🔄 CICLO DE VIDA

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   INICIAR   │───►│   SALVAR    │───►│  ATUALIZAR  │
│  (Criar)    │    │  (Por fase) │    │    (Loop)   │
└─────────────┘    └─────────────┘    └──────┬──────┘
                                             │
                   ┌─────────────┐           │
                   │   RETOMAR   │◄──────────┘
                   │  (--resume) │
                   └─────────────┘
```

---

## 📋 OPERAÇÕES PADRÃO

### 1. Criar Checkpoint (Início)

```markdown
# Ao iniciar workflow:
1. Verificar se existe `docs/{WORKFLOW}-PROGRESS.md`
2. Se existe:
   - Perguntar: "Retomar ou reiniciar?"
3. Se não existe:
   - Criar arquivo com template padrão
   - Registrar data de início
```

### 2. Salvar Progresso (Por Fase)

```markdown
# Ao concluir CADA fase:
1. Atualizar `Fase Atual` no arquivo
2. Marcar itens como concluídos [x]
3. Adicionar linha no Histórico
4. Atualizar `Última atualização`
```

### 3. Retomar (--resume)

```markdown
# Ao executar --resume:
1. Carregar `docs/{WORKFLOW}-PROGRESS.md`
2. Identificar `Fase Atual`
3. Identificar itens pendentes na fase
4. Continuar execução
```

### 4. Finalizar

```markdown
# Ao concluir workflow:
1. Atualizar Status para "✅ Concluído"
2. Registrar data de conclusão
3. Opcionalmente: arquivar ou deletar
```

---

## ⚠️ GATES DE SAÍDA

> [!IMPORTANT]
> Cada fase deve ter um **Gate de Saída** - checklist que DEVE ser satisfeito antes de prosseguir.

### Formato do Gate

```markdown
**Gate de Saída - Fase {N}:**
- [ ] Item obrigatório 1
- [ ] Item obrigatório 2
- [ ] Item obrigatório 3

> **BLOQUEADOR:** Não prosseguir até que todos os itens estejam ✅
```

---

## 🔗 WORKFLOWS QUE USAM ESTA SKILL

| Workflow | Arquivo de Checkpoint |
|----------|----------------------|
| `/new-task` | `docs/NEW-TASK-PROGRESS.md` |
| `/legacy-project` | `docs/LEGACY-PROGRESS.md` |
| `/new-project` | `docs/PROJECT-PROGRESS.md` |
