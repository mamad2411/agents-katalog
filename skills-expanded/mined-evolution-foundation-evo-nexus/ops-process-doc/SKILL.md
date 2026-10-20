---
name: ops-process-doc
description: Documentar um processo de negócio — fluxogramas, RACI e SOPs. Use quando formalizar um processo que vive na cabeça de alguém, construir RACI para deixar claro quem é dono de quê, escrever SOP para handoff ou auditoria, ou capturar exceções e edge cases de como o trabalho realmente acontece. Agente Clawdia.
argument-hint: "<nome ou descrição do processo>"
---

# /ops-process-doc

> Se encontrar placeholders desconhecidos ou precisar verificar quais ferramentas estão conectadas, consulte [CONNECTORS.md](../../CONNECTORS.md).

Documenta um processo de negócio como SOP (Standard Operating Procedure) completo.

## Agente

Clawdia — hub operacional, calendário, emails, tarefas, decisões.

## Como Funciona

Me explique o processo — descreva, cole docs existentes, ou só diga o nome e eu faço as perguntas certas. Produzirei um SOP completo.

## Output

```markdown
## Documento de Processo: [Nome do Processo]
**Responsável:** [Pessoa/Time] | **Última Atualização:** [Data] | **Cadência de Revisão:** [Trimestral/Anual]

### Objetivo
[Por que esse processo existe e o que ele realiza]

### Escopo
[O que está incluído e excluído]

### Matriz RACI
| Etapa | Responsável | Accountable | Consultado | Informado |
|-------|------------|-------------|-----------|----------|
| [Etapa] | [Quem faz] | [Quem é dono] | [Quem perguntar] | [Quem avisar] |

### Fluxo do Processo
[Fluxograma ASCII ou descrição passo a passo]

### Etapas Detalhadas

#### Etapa 1: [Nome]
- **Quem**: [Papel]
- **Quando**: [Gatilho ou timing]
- **Como**: [Instruções detalhadas]
- **Output**: [O que essa etapa produz]

#### Etapa 2: [Nome]
[Mesmo formato]

### Exceções e Edge Cases
| Cenário | O Que Fazer |
|---------|------------|
| [Exceção] | [Como lidar] |

### Métricas
| Métrica | Meta | Como Medir |
|---------|------|-----------|
| [Métrica] | [Meta] | [Método] |

### Documentos Relacionados
- [Link para processo ou política relacionada no Notion]
```

## Se Conectores Disponíveis

Se **Notion MCP** estiver conectado:
- Buscar documentação de processo existente para atualizar em vez de duplicar
- Publicar o SOP finalizado na wiki do Notion

Se **Linear MCP** estiver conectado:
- Vincular o processo a projetos e workflows relacionados
- Criar tarefas para action items de melhoria de processo

## Dicas

1. **Comece bagunçado** — Você não precisa de uma descrição perfeita. Me conte como funciona hoje e eu estruturo.
2. **Inclua as exceções** — "Normalmente fazemos X, mas às vezes Y" é a parte mais valiosa para documentar.
3. **Nomeie as pessoas** — Mesmo que os papéis mudem, saber quem faz o quê hoje ajuda a acertar o processo.
