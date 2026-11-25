---
name: planning
description: Crie e gerencie arquivos de planejamento markdown persistentes para execução estruturada de tarefas. Use quando o usuário pedir para "criar um plano", "acompanhar progresso", "iniciar um projeto de pesquisa", ou quando uma tarefa exigir mais de 5 chamadas de ferramenta e precisar de rastreamento de fases estruturado para manter o foco e evitar desvio de objetivo.
---

# AI Maestro Planning

Resolva o problema de execução -- manter o foco durante tarefas complexas e com múltiplas etapas. Usa arquivos markdown persistentes para rastrear objetivos, descobertas e progresso para que você nunca perca o contexto. Parte do pacote [AI Maestro](https://github.com/23blocks-OS/ai-maestro).

## Quando Usar

- Tarefas com múltiplas etapas (3+)
- Projetos de pesquisa
- Construção de features exigindo >5 chamadas de ferramenta
- Qualquer tarefa onde você possa perder o rastro do objetivo

## O Padrão de 3 Arquivos

Crie em `docs_dev/` (ou `$AIMAESTRO_PLANNING_DIR`):

| Arquivo | Propósito | Atualize Quando |
|---------|-----------|-----------------|
| `task_plan.md` | Objetivos, fases, decisões, erros | Após cada fase |
| `findings.md` | Pesquisa, descobertas, recursos | Durante pesquisa |
| `progress.md` | Log de sessão, resultados de testes | Durante a sessão |

## Início Rápido

```bash
PLAN_DIR="${AIMAESTRO_PLANNING_DIR:-docs_dev}"
mkdir -p "$PLAN_DIR"
```

Então crie `task_plan.md` com:
```markdown
# Tarefa: [Objetivo]

## Fases
- [ ] Fase 1: Pesquisa
- [ ] Fase 2: Design
- [ ] Fase 3: Implementação
- [ ] Fase 4: Teste

## Decisões
| Decisão | Lógica | Data |
|---------|--------|------|

## Erros Encontrados
| Erro | Tentativa | Resolução |
|------|-----------|-----------|
```

## As 6 Regras

1. **Crie o plano primeiro** -- Nunca comece trabalho complexo sem `task_plan.md`
2. **Leia antes de decidir** -- Releia o plano antes de qualquer decisão importante
3. **Atualize após agir** -- Marque fases como completas, registre o que mudou
4. **Regra dos 2 passos** -- Após cada 2 operações de busca/navegação, salve descobertas em `findings.md`
5. **Registre todos os erros** -- Todo erro entra no plano com número de tentativa e resolução
6. **Nunca repita falhas** -- Se uma ação falhou, mude sua abordagem

## O Protocolo dos 3 Erros

| Erro | Ação |
|------|------|
| 1º | Diagnostique a causa raiz, aplique correção direcionada |
| 2º | Tente uma abordagem completamente diferente |
| 3º | Questione suposições, procure por problemas similares |
| Após 3º | Escale para o usuário com todas as tentativas documentadas |

## O Reinício das 5 Perguntas

Perdido? Responda estas a partir de seus arquivos de planejamento:

1. Onde estou? (fase atual em `task_plan.md`)
2. Para onde vou? (fases restantes)
3. Qual é o objetivo? (seção de objetivo)
4. O que aprendi? (`findings.md`)
5. O que fiz? (`progress.md`)

## Experiência Completa com AI Maestro

Esta skill funciona de forma independente sem dependências. Para a experiência completa incluindo **busca de memória**, **busca de docs**, **consulta de gráfico**, **mensagens de agente** e **gerenciamento de agente**, instale a plataforma [AI Maestro](https://github.com/23blocks-OS/ai-maestro) completa.