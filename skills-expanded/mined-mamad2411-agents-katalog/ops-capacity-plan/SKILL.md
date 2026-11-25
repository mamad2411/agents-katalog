---
name: ops-capacity-plan
description: Planejar capacidade da equipe — análise de carga de trabalho e previsão de utilização por pessoa. Use quando estiver entrando em planejamento de sprint ou trimestre, o time parece sobrecarregado e você precisa dos números, decidindo contratar ou despriorizar, ou verificando se os projetos planejados cabem nas pessoas disponíveis. Agente Atlas.
argument-hint: "<equipe ou escopo do projeto>"
---

# /ops-capacity-plan

> Se encontrar placeholders desconhecidos ou precisar verificar quais ferramentas estão conectadas, consulte [CONNECTORS.md](../../CONNECTORS.md).

Analisa a capacidade da equipe Evolution e planeja alocação de recursos com base na estrutura real do time.

## Agente

Atlas — projetos, status, milestones, blockers, Linear, GitHub.

## O Que Preciso de Você

- **Equipe e papéis**: Quem temos? (ex: Guilherme — backend, Nickolas — dev, Danilo — PM)
- **Carga atual**: No que estão trabalhando? (cole da Linear ou descreva)
- **Trabalho futuro**: O que vem no próximo sprint/trimestre?
- **Restrições**: Budget, prazo de contratação, requisitos de skill

## Estrutura de Equipe Evolution

| Pessoa | Papel | Time |
|--------|-------|------|
| Davidson | CEO / Dev Open Source | Etus / Liderança |
| Danilo Leone | Tech / PM (cria issues no Linear) | Brius |
| Guilherme Gomes | Dev Backend | Brius |
| Nickolas Oliveira | Dev | Brius |
| Wanderson Santos | Dev | Brius |
| Willian Capovilla | Freelancer (Design) | OrionDesign |

## Dimensões de Planejamento

### Pessoas
- Headcount disponível e skills
- Alocação atual e utilização (via issues no Linear)
- Contratações planejadas e timeline
- Capacidade de freelancers e prestadores

### Budget
- Budget operacional por categoria
- Budgets específicos por projeto
- Tracking de variância
- Forecast vs. real

### Tempo
- Timelines de projeto e dependências
- Análise de caminho crítico
- Buffer e contingência
- Gestão de deadlines

## Targets de Utilização

| Tipo de Papel | Utilização Target | Notas |
|---------------|-------------------|-------|
| Dev / Especialista | 75-80% | Deixar espaço para trabalho reativo e crescimento |
| PM / Tech Lead | 60-70% | Overhead de gestão, reuniões, alinhamentos |
| On-call / Suporte | 50-60% | Trabalho por interrupção é imprevisível |

## Erros Comuns

- Planejar para 100% de utilização (sem buffer para surpresas)
- Ignorar carga de reuniões e custos de troca de contexto
- Não contabilizar férias, feriados e dias de saúde
- Tratar todas as horas como iguais (trabalho criativo ≠ trabalho administrativo)

## Output

```markdown
## Capacity Plan: [Equipe/Projeto]
**Período:** [Intervalo de datas] | **Tamanho do Time:** [X]

### Utilização Atual
| Pessoa/Papel | Capacidade | Alocado | Disponível | Utilização |
|-------------|----------|---------|------------|------------|
| [Nome/Papel] | [hrs/sem] | [hrs/sem] | [hrs/sem] | [X]% |

### Resumo de Capacidade
- **Capacidade total**: [X] horas/semana
- **Atualmente alocado**: [X] horas/semana ([X]%)
- **Disponível**: [X] horas/semana ([X]%)
- **Sobrealoc.**: [X pessoas acima de 100%]

### Demanda Futura
| Projeto/Iniciativa | Início | Fim | Recursos Necessários | Gap |
|--------------------|--------|-----|---------------------|-----|
| [Projeto] | [Data] | [Data] | [X FTEs] | [Coberto/Gap] |

### Gargalos
- [Skill ou papel sobrecarregado]
- [Período com crunch]

### Recomendações
1. [Contratar / Terceirizar / Repriorizar / Atrasar]
2. [Ação específica]

### Cenários
| Cenário | Resultado |
|---------|-----------|
| Não fazer nada | [O que acontece] |
| Contratar [X] | [O que muda] |
| Despriorizar [Y] | [O que libera] |
```

## Se Conectores Disponíveis

Se **Linear MCP** estiver conectado:
- Puxar carga atual e atribuições de issues automaticamente via `int-linear-review`
- Mostrar compromissos do sprint ou trimestre por pessoa

Se **Google Calendar MCP** estiver conectado:
- Considerar férias, feriados e carga de reuniões recorrentes
- Calcular horas realmente disponíveis por pessoa

## Dicas

1. **Inclua todo o trabalho** — BAU, projetos, suporte, reuniões. Pessoas não estão 100% disponíveis para projetos.
2. **Planeje com buffer** — Target de 80% de utilização. 100% significa nenhuma margem para surpresas.
3. **Atualize regularmente** — Capacity plans ficam desatualizados rápido. Revisar a cada sprint.
