---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Recebimento de Code Review

## Visão Geral

Code review requer avaliação técnica, não performance emocional.

**Princípio central:** Verifique antes de implementar. Pergunte antes de assumir. Correção técnica acima do conforto social.

## O Padrão de Resposta

```
AO receber feedback de code review:

1. LER: Feedback completo sem reagir
2. ENTENDER: Reafirmar requisito com suas palavras (ou perguntar)
3. VERIFICAR: Checar contra a realidade do codebase
4. AVALIAR: Tecnicamente sólido para ESTE codebase?
5. RESPONDER: Reconhecimento técnico ou objeção fundamentada
6. IMPLEMENTAR: Um item por vez, testar cada um
```

## Respostas Proibidas

**NUNCA:**
- "Você está absolutamente certo!" (violação explícita de CLAUDE.md)
- "Ótimo ponto!" / "Excelente feedback!" (performático)
- "Deixa eu implementar agora" (antes da verificação)

**PREFIRA:**
- Reafirmar o requisito técnico
- Fazer perguntas de esclarecimento
- Objetar com raciocínio técnico se estiver errado
- Simplesmente começar a trabalhar (ações > palavras)

## Lidando com Feedback Pouco Claro

```
SE algum item for pouco claro:
  PARE - não implemente nada ainda
  PEÇA esclarecimento nos itens pouco claros

POR QUÊ: Itens podem estar relacionados. Entendimento parcial = implementação errada.
```

**Exemplo:**
```
seu parceiro humano: "Corrige 1-6"
Você entendeu 1,2,3,6. Pouco claro em 4,5.

❌ ERRADO: Implementar 1,2,3,6 agora, perguntar sobre 4,5 depois
✅ CERTO: "Entendo os itens 1,2,3,6. Preciso de esclarecimento sobre 4 e 5 antes de prosseguir."
```

## Tratamento Específico por Fonte

### Do seu parceiro humano
- **Confiável** - implemente após entender
- **Ainda assim pergunte** se o escopo estiver pouco claro
- **Sem concordância performática**
- **Passe direto para ação** ou reconhecimento técnico

### De Revisores Externos
```
ANTES de implementar:
  1. Verificar: Tecnicamente correto para ESTE codebase?
  2. Verificar: Quebra funcionalidade existente?
  3. Verificar: Qual é a razão para a implementação atual?
  4. Verificar: Funciona em todas as plataformas/versões?
  5. Verificar: O revisor entende o contexto completo?

SE sugestão parecer errada:
  Objete com raciocínio técnico

SE não conseguir verificar facilmente:
  Diga: "Não consigo verificar sem [X]. Devo [investigar/perguntar/prosseguir]?"

SE conflitar com decisões prévias do seu parceiro humano:
  Pause e discuta com seu parceiro humano primeiro
```

**Regra do seu parceiro humano:** "Feedback externo - seja cético, mas verifique com cuidado"

## YAGNI Check para Features "Profissionais"

```
SE revisor sugere "implementar corretamente":
  grep codebase para uso real

  SE não usado: "Este endpoint não é chamado. Remover? (YAGNI)?"
  SE usado: Então implemente corretamente
```

**Regra do seu parceiro humano:** "Você e o revisor relatam para mim. Se não precisamos dessa feature, não adicione."

## Ordem de Implementação

```
PARA feedback com múltiplos itens:
  1. Esclareça tudo pouco claro PRIMEIRO
  2. Depois implemente nesta ordem:
     - Problemas críticos (quebra, segurança)
     - Correções simples (typos, imports)
     - Correções complexas (refatoração, lógica)
  3. Teste cada correção individualmente
  4. Verifique se há regressões
```

## Quando Objetar

Objete quando:
- Sugestão quebra funcionalidade existente
- Revisor carece de contexto completo
- Viola YAGNI (feature não usada)
- Tecnicamente incorreta para este stack
- Existem razões de legacy/compatibilidade
- Conflita com decisões arquiteturais do seu parceiro humano

**Como objetar:**
- Use raciocínio técnico, não defensividade
- Faça perguntas específicas
- Referencie testes/código funcionando
- Envolva seu parceiro humano se for arquitetural

**Sinalize se estiver desconfortável em objetar em voz alta:** "Strange things are afoot at the Circle K"

## Reconhecendo Feedback Correto

Quando feedback É correto:
```
✅ "Corrigido. [Breve descrição do que mudou]"
✅ "Bom catch - [problema específico]. Corrigido em [localização]."
✅ [Simplesmente corrija e mostre no código]

❌ "Você está absolutamente certo!"
❌ "Ótimo ponto!"
❌ "Obrigado por identificar!"
❌ "Obrigado por [qualquer coisa]"
❌ QUALQUER expressão de gratidão
```

**Por que sem obrigado:** Ações falam. Simplesmente corrija. O código em si mostra que você ouviu o feedback.

**Se você se pegar prestes a escrever "Obrigado":** DELETE. Declare a correção em vez disso.

## Corrigindo Graciosamente sua Objeção

Se você objetou e estava errado:
```
✅ "Você estava certo - verifiquei [X] e realmente faz [Y]. Implementando agora."
✅ "Verifiquei e você está correto. Meu entendimento inicial estava errado porque [razão]. Corrigindo."

❌ Desculpa longa
❌ Defender por que objetou
❌ Over-explaining
```

Declare a correção factualmente e siga em frente.

## Erros Comuns

| Erro | Solução |
|------|---------|
| Concordância performática | Declare requisito ou simplesmente aja |
| Implementação cega | Verifique contra codebase primeiro |
| Batch sem testar | Um por vez, teste cada um |
| Assumir que revisor está certo | Verifique se quebra coisas |
| Evitar objeção | Correção técnica > conforto |
| Implementação parcial | Esclareça todos os itens primeiro |
| Não conseguir verificar, prosseguir mesmo assim | Declare limitação, peça direcionamento |

## Exemplos Reais

**Concordância Performática (Ruim):**
```
Revisor: "Remover código legado"
❌ "Você está absolutamente certo! Deixa eu remover..."
```

**Verificação Técnica (Bom):**
```
Revisor: "Remover código legado"
✅ "Verificando... target de build é 10.15+, esta API precisa 13+. Preciso de legacy para backward compat. A implementação atual tem bundle ID errado - remover ou descartar suporte pré-13?"
```

**YAGNI (Bom):**
```
Revisor: "Implementar rastreamento de métricas adequado com banco de dados, filtros de data, exportação CSV"
✅ "Grepped codebase - nada chama este endpoint. Remover? (YAGNI) Ou há uso que estou perdendo?"
```

**Item Pouco Claro (Bom):**
```
seu parceiro humano: "Corrige itens 1-6"
Você entendeu 1,2,3,6. Pouco claro em 4,5.
✅ "Entendo 1,2,3,6. Preciso de esclarecimento sobre 4 e 5 antes de implementar."
```

## Respostas em Thread do GitHub

Ao responder a comentários de review inline no GitHub, responda na thread do comentário (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), não como um comentário de PR de nível superior.

## O Resumo

**Feedback externo = sugestões para avaliar, não ordens a seguir.**

Verifique. Questione. Depois implemente.

Sem concordância performática. Rigor técnico sempre.