---
name: document-registry
description: Protocolo para manter docs/INDEX.md atualizado como fonte de verdade de todos os documentos do projeto. Obrigatório em toda fase que cria ou consome documentação. Usado por new-project, legacy-project, new-task e qualquer workflow que gere artefatos.
---

# Skill: document-registry

## Propósito

`docs/INDEX.md` é o **único ponto de entrada** para que agentes saibam o que existe no projeto sem precisar varrer o sistema de arquivos. Este skill define como mantê-lo correto.

> [!IMPORTANT]
> **REGRA DO AGENTE:** Antes de buscar qualquer documento, verificar `docs/INDEX.md`.
> Se o INDEX não existir → executar `project-foundation` primeiro.

---

## 1. Antes de Buscar Documentos (READ)

Ao iniciar qualquer fase ou task que precise de contexto:

```
1. Ler docs/INDEX.md
2. Identificar entries relevantes pelo tipo ou doc_id
3. Seguir o path listado — NÃO buscar o arquivo por nome em todo o fs
4. Verificar o status: draft | review | approved | superseded
   → draft: usar com cautela, não é fonte de verdade
   → review: aguardar aprovação antes de implementar
   → approved: implementar com confiança
   → superseded: NÃO usar — ver "replaced_by" no INDEX
```

---

## 2. Ao Criar um Documento (WRITE)

Toda vez que um documento for criado, adicionar uma entry no INDEX **imediatamente**:

### Formato da Entry

```markdown
| {doc_id} | {Type} | [{basename}]({relative-path}) | draft | {version} | — |
```

### Campos Obrigatórios

| Campo | Formato | Exemplo |
|-------|---------|---------|
| `doc_id` | `{TYPE}-{slug}` | `PRD-flyee`, `SDD-auth`, `FLOW-login` |
| `Type` | PRD, SDD, Design System, OpenAPI, Flow, ADR, Handover, Test Guide, Page Spec | `Flow` |
| Path | Relativo ao `/docs/` | `flows/auth/login.md` |
| Status | `draft` (default ao criar) | `draft` |
| Version | `"1.0"` ao criar | `"1.0"` |
| `approved_at` | `—` (vazio ao criar) | `—` |

### Tipos de Documentos e doc_id Padrão

| Tipo | doc_id padrão | Exemplo |
|------|--------------|---------|
| PRD | `PRD-{slug}` | `PRD-flyee` |
| SDD (Software Design Doc) | `SDD-{slug}-{módulo}` | `SDD-flyee-auth` |
| Design System | `DS-{slug}` | `DS-flyee` |
| OpenAPI Spec | `API-{slug}` | `API-flyee` |
| Flow documentation | `FLOW-{slug}` | `FLOW-login` |
| ADR | `ADR-{NNN}-{slug}` | `ADR-001-redis` |
| Handover | `HANDOVER-{escopo}` | `HANDOVER-auth` |
| Test Guide | `TESTGUIDE-{escopo}` | `TESTGUIDE-auth` |
| Page Spec | `PAGESPEC-{page}` | `PAGESPEC-dashboard` |
| Retrospective | `RETRO-{slug}-v{N}` | `RETRO-flyee-v1` |
| Security Policy | `SECURITY` | `SECURITY` |
| Legacy Analysis | `LEGACY-ANALYSIS` | `LEGACY-ANALYSIS` |

---

## 3. Ao Aprovar um Documento (STATUS UPDATE)

Quando o usuário aprovar um documento:

```
1. Abrir docs/INDEX.md
2. Localizar a entry pelo doc_id
3. Atualizar: status → approved, approved_at → YYYY-MM-DD
4. Se substituindo versão anterior: marcar antiga como superseded, adicionar campo replaced_by
```

---

## 4. Ao Superseder um Documento

```
1. Marcar entry antiga: status → superseded
2. Adicionar coluna implied "replaced_by: {novo_doc_id}"
3. Adicionar nova entry com nova versão
4. NÃO deletar a entry antiga do INDEX — histórico é valioso
```

---

## 5. Checklist por Fase

### Fases que CRIAM documentos (devem atualizar INDEX):
- `project-foundation` → README, .env.example, SECURITY, INDEX, ADR-000
- `new-project` Phase 1 → PRD
- `new-project` Phase 2 → SDD
- `new-project` Phase 2.5 → Design System
- `new-project` Phase 2.65 → Content docs
- `new-project` Phase 2.8 → Page Specs
- `legacy-project` Phase 4 (loop) → Flow docs
- `legacy-project` Phase 5 → SDD by module
- `legacy-project` Phase 5.5 → Design System
- `legacy-project` Phase 5.6 → Security ADR (se issues encontrados)
- `legacy-project` Phase 7.5 → ADRs
- `legacy-project` Phase 8 → Handover + Test Guide

### Fases que CONSOMEM documentos (devem ler INDEX primeiro):
- Qualquer fase de implementação
- `context-gathering-patterns` (verificar INDEX antes de buscar docs)
- `new-task` Fase -1 e Fase 1 (histórico + contexto)

---

## 6. Anti-Patterns

| ❌ Proibido | ✅ Correto |
|------------|-----------|
| Buscar `find docs/ -name "*.md"` para achar documentos | Ler `docs/INDEX.md` primeiro |
| Criar documento sem adicionar ao INDEX | Criar + entry no INDEX imediatamente |
| Usar documento com status `draft` como fonte de verdade | Verificar status antes de implementar |
| Deletar entries do INDEX | Marcar como `superseded` (nunca deletar) |
| Criar documento com `doc_id` duplicado | Verificar INDEX antes de criar |
