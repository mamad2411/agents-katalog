---
name: verificar-antes-de-enviar
description: Use when about to claim work is complete, fixed, or passing, before committing, pushing, or updating Track status — requires running verification commands and confirming output before any success claims
---

# Verificar Antes de Enviar

## Visão geral

Roubado do Superpowers `verification-before-completion`.

Declarar pronto sem evidência é desonestidade, não eficiência.

**Princípio:** evidência antes de claims, sempre.

**Anuncie:** "Usando verificar-antes-de-enviar."

## Lei de ferro

```
NENHUM CLAIM DE SUCESSO SEM EVIDÊNCIA FRESCA DE VERIFICAÇÃO
```

Se você não rodou o comando de verificação **nesta** mensagem (ou ciclo imediato legível), não pode dizer que passou.

Violar a letra é violar o espírito.

## Função gate

Antes de qualquer status positivo ou satisfação:

1. **IDENTIFICAR:** qual comando prova o claim?
2. **RODAR:** comando completo, fresco
3. **LER:** output inteiro, exit code, contagem de falhas
4. **VERIFICAR:** o output confirma?
   - NÃO → reporte o estado real com evidência
   - SIM → claim **com** evidência
5. **SÓ ENTÃO** diga que passou / está pronto

Pular passo = mentir, não verificar.

## O que rodar (descobrir no repo)

Ordem típica (adapte ao `package.json` / CI do projeto):

1. Lint / typecheck (`yarn lint`, `yarn lint:check`, `tsc`, etc.)
2. Testes relevantes (`yarn test`, suite da área)
3. Build se o CI exige antes do push (`yarn build`)
4. Audit CI se o repo bloqueia high/critical (`yarn audit:ci`)

Se for monorepo Hous3 Track:

- Frontend (`hous3-track-frontend/app`): lint + test + build (+ audit:ci se for o gate)
- Backend (`hous3-track-backend/app`): lint:check + test + build (+ audit:ci)

**Acceptance MCP:** checklist item a item do `get_agent_execution_context` — gaps bloqueiam o envio.

## Falhas comuns

| Claim | Exige | Não basta |
|-------|-------|-----------|
| Testes passam | Output: 0 failures | Run anterior, "deve passar" |
| Lint limpo | Output: 0 errors | Check parcial |
| Build ok | exit 0 | Só lint |
| Bug corrigido | Sintoma original: passa | "Mudei o código" |
| Requirements ok | Checklist linha a linha | "Testes passaram" |

## Sinais vermelhos — PARE

- "Should", "probably", "parece", "deve estar"
- Satisfação antes de verificar ("Pronto!", "Perfeito!")
- Commit/push/`in_review` sem verificação
- Confiar em relatório de subagente sem olhar diff/output
- "Só dessa vez"
- Cansaço como desculpa

## Racionalizações

| Desculpa | Realidade |
|----------|-----------|
| "Deve funcionar agora" | RODE a verificação |
| "Estou confiante" | Confiança ≠ evidência |
| "Lint passou" | Lint ≠ compile ≠ testes |
| "Agente disse success" | Verifique independente |
| "Check parcial chega" | Parcial não prova |

## Depois do verde

Só então invoque `fechar-task`.

Se vermelho: **não** push, **não** `update_dev_task` para `in_review`. Corrija e re-verifique.
