---
name: ops-change-request
description: Criar solicitação de mudança com análise de impacto e plano de rollback. Use quando propor mudança de sistema ou processo que precisa de aprovação, documentar risco e passos de rollback antes de um deploy, ou planejar comunicação com stakeholders para um rollout. Agente Atlas.
argument-hint: "<descrição da mudança>"
---

# /ops-change-request

> Se encontrar placeholders desconhecidos ou precisar verificar quais ferramentas estão conectadas, consulte [CONNECTORS.md](../../CONNECTORS.md).

Cria uma solicitação de mudança estruturada com análise de impacto, avaliação de risco e plano de rollback.

## Agente

Atlas — projetos, status, milestones, blockers, Linear, GitHub.

## Framework de Gestão de Mudança

Aplique o framework avaliar-planejar-executar-sustentar ao construir a solicitação:

### 1. Avaliar
- O que está mudando?
- Quem é afetado?
- Qual a significância da mudança? (Baixa / Média / Alta)
- Que resistência devemos esperar?

### 2. Planejar
- Plano de comunicação (quem, o quê, quando, como)
- Plano de treinamento (quais skills são necessários, como entregar)
- Plano de suporte (champions, FAQs)
- Timeline com milestones

### 3. Executar
- Anunciar e explicar o "porquê"
- Treinar e dar suporte
- Monitorar adoção
- Endereçar resistências

### 4. Sustentar
- Medir adoção e efetividade
- Reforçar novos comportamentos
- Endereçar issues remanescentes
- Documentar lições aprendidas

## Princípios de Comunicação

- Explicar o **porquê** antes do **o quê**
- Comunicar cedo e com frequência
- Usar múltiplos canais (Discord, Gmail, reuniões)
- Reconhecer o que está sendo perdido, não só o que está sendo ganho
- Fornecer caminho claro para perguntas e preocupações

## Output

```markdown
## Change Request: [Título]
**Solicitante:** [Nome] | **Data:** [Data] | **Prioridade:** [Crítica/Alta/Média/Baixa]
**Status:** Rascunho | Aprovação Pendente | Aprovado | Em Progresso | Concluído

### Descrição
[O que está mudando e por quê]

### Justificativa de Negócio
[Por que essa mudança é necessária — economia, eficiência, redução de risco]

### Análise de Impacto
| Área | Impacto | Detalhes |
|------|---------|---------|
| Usuários | [Alto/Médio/Baixo/Nenhum] | [Quem é afetado e como] |
| Sistemas | [Alto/Médio/Baixo/Nenhum] | [Quais sistemas são afetados] |
| Processos | [Alto/Médio/Baixo/Nenhum] | [Quais workflows mudam] |
| Custo | [Alto/Médio/Baixo/Nenhum] | [Impacto no budget] |

### Avaliação de Risco
| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| [Risco] | [A/M/B] | [A/M/B] | [Como mitigar] |

### Plano de Implementação
| Etapa | Responsável | Timeline | Dependências |
|-------|------------|----------|-------------|
| [Etapa] | [Pessoa] | [Data] | [Do que depende] |

### Plano de Comunicação
| Audiência | Mensagem | Canal | Timing |
|-----------|---------|-------|--------|
| [Quem] | [O que contar] | [Como — Discord/Gmail/Reunião] | [Quando] |

### Plano de Rollback
[Plano passo a passo para reverter a mudança se necessário]
- Gatilho: [Quando fazer rollback]
- Passos: [Como reverter]
- Verificação: [Como confirmar que o rollback funcionou]

### Aprovações Necessárias
| Aprovador | Papel | Status |
|-----------|-------|--------|
| [Nome] | [Papel] | Pendente |
```

## Se Conectores Disponíveis

Se **Linear MCP** estiver conectado:
- Criar issue de change request no Linear automaticamente
- Vincular às tarefas de implementação e dependências relacionadas
- Acompanhar progresso da mudança contra milestones

Se **Discord** estiver disponível:
- Rascunhar notificações para stakeholders conforme plano de comunicação
- Postar updates da mudança nos canais relevantes da equipe

Se **Gmail MCP** estiver conectado:
- Enviar comunicações formais para stakeholders externos via email

## Dicas

1. **Seja específico sobre impacto** — "Todos" não é uma avaliação de impacto. "Time de backend, 4 devs" é.
2. **Sempre tenha plano de rollback** — Mesmo que esteja confiante, planeje para a falha.
3. **Comunique cedo** — Surpresas criam resistência. Pré-alinhamentos criam adesão.
