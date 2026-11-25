---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verificação Antes da Conclusão

## Visão Geral

Afirmar que o trabalho está completo sem verificação é desonestidade, não eficiência.

**Princípio central:** Evidência antes de afirmações, sempre.

**Violar a letra desta regra é violar o espírito da regra.**

## A Lei de Ferro

```
SEM AFIRMAÇÕES DE CONCLUSÃO SEM EVIDÊNCIA DE VERIFICAÇÃO RECENTE
```

Se você não executou o comando de verificação nesta mensagem, você não pode afirmar que passa.

## A Função de Controle

```
ANTES de afirmar qualquer status ou expressar satisfação:

1. IDENTIFIQUE: Qual comando prova esta afirmação?
2. EXECUTE: Execute o comando COMPLETO (recente, íntegro)
3. LEIA: Saída completa, verifique código de saída, conte falhas
4. CONFIRME: A saída confirma a afirmação?
   - Se NÃO: Declare status real com evidência
   - Se SIM: Declare afirmação COM evidência
5. APENAS ENTÃO: Faça a afirmação

Pular qualquer etapa = mentir, não verificar
```

## Falhas Comuns

| Afirmação | Requer | Insuficiente |
|-----------|--------|--------------|
| Testes passam | Saída de teste: 0 falhas | Execução anterior, "deveria passar" |
| Linter limpo | Saída de linter: 0 erros | Verificação parcial, extrapolação |
| Build bem-sucedido | Comando de build: saída 0 | Linter passando, logs parecem bons |
| Bug corrigido | Teste do sintoma original: passa | Código alterado, assumir corrigido |
| Teste de regressão funciona | Ciclo vermelho-verde verificado | Teste passa uma vez |
| Agent completou | Diff do VCS mostra mudanças | Agent relata "sucesso" |
| Requisitos atendidos | Checklist linha por linha | Testes passando |

## Sinais de Alerta - PARE

- Usar "deveria", "provavelmente", "parece"
- Expressar satisfação antes da verificação ("Ótimo!", "Perfeito!", "Pronto!", etc.)
- Prestes a fazer commit/push/PR sem verificação
- Confiar em relatórios de sucesso do agent
- Depender de verificação parcial
- Pensar "só desta vez"
- Cansado e querendo terminar o trabalho
- **QUALQUER redação implicando sucesso sem ter executado verificação**

## Prevenção de Racionalizações

| Desculpa | Realidade |
|----------|-----------|
| "Deveria funcionar agora" | EXECUTE a verificação |
| "Tenho certeza" | Certeza ≠ evidência |
| "Só dessa vez" | Sem exceções |
| "Linter passou" | Linter ≠ compilador |
| "Agent disse sucesso" | Verifique independentemente |
| "Estou cansado" | Cansaço ≠ desculpa |
| "Verificação parcial é suficiente" | Parcial não prova nada |
| "Palavras diferentes então a regra não se aplica" | Espírito acima da letra |

## Padrões-Chave

**Testes:**
```
✅ [Execute comando de teste] [Ver: 34/34 passam] "Todos os testes passam"
❌ "Deveria passar agora" / "Parece correto"
```

**Testes de regressão (TDD Vermelho-Verde):**
```
✅ Escrever → Executar (passa) → Reverter correção → Executar (DEVE FALHAR) → Restaurar → Executar (passa)
❌ "Escrevi um teste de regressão" (sem verificação vermelho-verde)
```

**Build:**
```
✅ [Execute build] [Ver: saída 0] "Build passa"
❌ "Linter passou" (linter não verifica compilação)
```

**Requisitos:**
```
✅ Releia plano → Crie checklist → Confirme cada → Reporte lacunas ou conclusão
❌ "Testes passam, fase completa"
```

**Delegação para agent:**
```
✅ Agent relata sucesso → Verifique diff do VCS → Valide mudanças → Reporte estado real
❌ Confiar em relatório do agent
```

## Por Que Isso Importa

De 24 memórias de falha:
- seu parceiro humano disse "Não acredito em você" - confiança quebrada
- Funções indefinidas foram enviadas - causariam travamento
- Requisitos ausentes foram enviados - funcionalidades incompletas
- Tempo desperdiçado em conclusão falsa → redirecionamento → retrabalhp
- Viola: "Honestidade é um valor central. Se você mentir, será substituído."

## Quando Aplicar

**SEMPRE antes de:**
- QUALQUER variação de afirmações de sucesso/conclusão
- QUALQUER expressão de satisfação
- QUALQUER declaração positiva sobre o estado do trabalho
- Fazer commit, criar PR, completar tarefa
- Passar para próxima tarefa
- Delegar para agents

**Regra se aplica a:**
- Frases exatas
- Paráfrases e sinônimos
- Implicações de sucesso
- QUALQUER comunicação sugerindo conclusão/correção

## O Essencial

**Sem atalhos para verificação.**

Execute o comando. Leia a saída. DEPOIS afirme o resultado.

Isso é inegociável.