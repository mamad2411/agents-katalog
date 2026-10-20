---
name: ops-runbook
description: Criar ou atualizar runbook operacional para tarefa ou procedimento recorrente. Use quando documentar tarefa que o time de ops precisa rodar repetidamente, transformar conhecimento tribal em comandos passo a passo, adicionar troubleshooting e rollback a procedimento existente, ou escrever caminhos de escalação para quando algo der errado. Agente Clawdia.
argument-hint: "<nome do processo ou tarefa>"
---

# /ops-runbook

> Se encontrar placeholders desconhecidos ou precisar verificar quais ferramentas estão conectadas, consulte [CONNECTORS.md](../../CONNECTORS.md).

Cria runbook operacional passo a passo para tarefa ou procedimento recorrente.

## Agente

Clawdia — hub operacional, calendário, emails, tarefas, decisões.

## Output

````markdown
## Runbook: [Nome da Tarefa]
**Responsável:** [Time/Pessoa] | **Frequência:** [Diária/Semanal/Mensal/Conforme Necessário]
**Última Atualização:** [Data] | **Última Execução:** [Data]

### Objetivo
[O que esse runbook realiza e quando usar]

### Pré-requisitos
- [ ] [Acesso ou permissão necessária]
- [ ] [Ferramenta ou sistema necessário]
- [ ] [Dado ou input necessário]

### Procedimento

#### Etapa 1: [Nome]
```
[Comando exato, ação ou instrução]
```
**Resultado esperado:** [O que deve acontecer]
**Se falhar:** [O que fazer]

#### Etapa 2: [Nome]
```
[Comando exato, ação ou instrução]
```
**Resultado esperado:** [O que deve acontecer]
**Se falhar:** [O que fazer]

### Verificação
- [ ] [Como confirmar que a tarefa foi concluída com sucesso]
- [ ] [O que checar]

### Troubleshooting
| Sintoma | Causa Provável | Solução |
|---------|---------------|---------|
| [O que você vê] | [Por quê] | [O que fazer] |

### Rollback
[Como desfazer isso se algo der errado]

### Escalação
| Situação | Contato | Método |
|----------|---------|--------|
| [Quando escalar] | [Quem] | [Como contatar — Discord/WhatsApp/telefone] |

### Histórico
| Data | Executado por | Notas |
|------|--------------|-------|
| [Data] | [Pessoa] | [Issues ou observações] |
````

## Se Conectores Disponíveis

Se **Notion MCP** estiver conectado:
- Buscar runbooks existentes para atualizar em vez de criar do zero
- Publicar o runbook finalizado na wiki de ops do Notion

Se **Linear MCP** estiver conectado:
- Vincular o runbook a tipos de incident e change requests relacionados
- Referenciar issues de manutenção recorrentes

## Dicas

1. **Seja dolorosamente específico** — "Rodar o script" não é uma etapa. "Rodar `python sync.py --prod --dry-run` no servidor de ops" é.
2. **Inclua modos de falha** — O que pode dar errado em cada etapa e o que fazer a respeito.
3. **Teste o runbook** — Peça a alguém não familiarizado com o processo para segui-lo. Corrija onde travarem.
