---
name: encerrar
description: Protocolo de encerramento de sessão — checklist, log no TAREFAS.md, sincronização do KANBAN e resumo. Ativar quando Luiz disser "encerrar", "encerrar sessão", "/encerrar" ou ao finalizar uma feature.
---

# Skill: encerrar

Protocolo de encerramento. Garante que nada fica pendente sem documentação antes do reset de contexto.

## Fase 1 — Checklist de Entrega

Perguntar sobre cada item (pode responder tudo de uma vez):

**O que foi feito nesta sessão?**
- Qual feature/tarefa foi trabalhada?
- Está entregue ou parcialmente concluída?

**Verificações:**
- [ ] Commit foi feito com as mudanças da sessão?
- [ ] Spec da feature foi atualizada com log de implementação?
- [ ] ADR criado se houve decisão técnica relevante?
- [ ] CLAUDE.md do projeto atualizado se mudou algo estrutural?

Se algum item não foi feito, perguntar se quer fazer agora ou registrar como pendente.

## Fase 2 — Atualizar TAREFAS.md

Adicionar log no `99_System/TAREFAS.md`:

**Se feature concluída** — mover tarefa para seção "Concluídas" ou marcar status:
```
### T-[EQ]-NNN · [Título]
- **Status:** ✅ Concluída
- **Concluído em:** YYYY-MM-DD
- **Entregue:** [descrição do que foi implementado]
```

**Se parcialmente concluída** — adicionar log:
```
### T-[EQ]-NNN · [Título]
- **Status:** 🔵 Ativa (em progresso)
- **Sessão YYYY-MM-DD:** [o que foi feito + o que falta]
```

## Fase 3 — Sincronizar KANBAN

Abrir `99_System/KANBAN.md` e verificar:

- Se feature concluída → mover card de `🔵 Ativa` para `✅ Concluída`
- Se parcialmente concluída → manter em `🔵 Ativa` sem mudança

## Fase 4 — Atualizar Paperclip (se feature concluída)

```
PATCH http://127.0.0.1:3100/api/issues/[issue-id]
Authorization: Bearer $env:PAPERCLIP_API_KEY
Content-Type: application/json

{
  "status": "done"
}
```

Se não souber o ID do issue, pular e avisar para atualizar manualmente.

## Fase 5 — Resumo Final

Exibir resumo formatado:

```
## Sessão encerrada — YYYY-MM-DD

**O que foi feito:**
- [item 1]
- [item 2]

**Status:**
- [Feature X]: ✅ Concluída / 🔵 Em progresso

**Próximos passos:**
- [próxima feature/tarefa sugerida]

**Contexto para próxima sessão:**
> Leia: [CLAUDE.md do projeto] + [spec da próxima feature se existir]
```

## Fase 6 — Gravar Session Summary

Criar arquivo `99_System/logs/session-YYYYMMDD-HHMM.md` com o conteúdo da Fase 5:

```markdown
---
data: YYYY-MM-DD
hora: HH:MM
dominio: [domínio trabalhado — extraído do contexto de sessão ou perguntar]
tipo: session-summary
---

# Sessão YYYY-MM-DD

## O que foi feito
- [item 1 — copiado do resumo da Fase 5]
- [item 2]

## Decisões tomadas
- [decisão + justificativa curta — se houver]

## Status das tarefas
- [T-XXX-NNN]: ✅ Concluída / 🔵 Em progresso

## Próximos passos
- [próxima tarefa sugerida da Fase 5]
- [ponto que ficou pendente]

## Contexto para próxima sessão
Ler: [[caminho/do/projeto/CLAUDE]] + [[spec da próxima feature se existir]]
```

Se não souber o domínio, perguntar: "Qual domínio trabalhamos? (dev / direito / comercial / pessoal / geral)"

## Referências Vault (sugerir ao completar)

Ao encerrar, sugerir o que ler na próxima sessão:
- Se feature em progresso: `[[04_Projects/[projeto]/specs/feature-[nome]]]` — spec da próxima etapa
- Se ADR relevante foi tomado: `[[07_Decisions/ADR-NNN]]` para referenciar no próximo contexto
- Sempre: `[[14_Indexes/IDX-[dominio]]]` como ponto de partida para a próxima sessão

## Restrições

- NUNCA marcar feature como concluída sem commit confirmado
- NUNCA encerrar sem atualizar TAREFAS.md
- Se Paperclip offline, registrar no vault e avisar
- Não encerrar sessão se spec da feature não foi criada antes da implementação (violação SDD)
