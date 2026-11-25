---
name: disciplina-de-validacao
description: A regra sem exceção do método — validação declarada é validação executada, erro encontrado é erro corrigido, e limite de ambiente é hipótese até ser medido. Cataloga as quatro saídas de emergência que um agente inventa sob pressão de escopo. Carregar no INÍCIO de qualquer tarefa que vá terminar em push, e SEMPRE antes de escrever "não foi possível validar", "fica registrado como GAP" ou "falha conhecida".
---

# Disciplina de validação — o que fazer quando o certo dá trabalho

Esta skill não ensina a testar. Ensina a não desviar. Os desvios não aparecem como preguiça: aparecem como pragmatismo, com justificativa escrita.

A regra, como o dono do projeto de origem a formulou: validações são seguidas; se há erros, são corrigidos.

## As quatro saídas de emergência

### 1. "Não é possível validar neste ambiente"

Caso de origem: um PR registrou "sem validação em browser: a sandbox não tem os browsers" e seguiu. A instalação passava com uma variável de ambiente. Quando o teste rodou, achou na primeira execução uma exceção que ocorria em toda abertura da tela.

Limite de ambiente é hipótese até ser medido. Antes de escrever "não dá": leia o erro exato, procure a flag/variável que o contorna, verifique se outro repositório já resolveu. Se o limite for real, vira GAP com o erro exato colado — nunca uma frase no PR. E quando a validação que falta é a única capaz de exercitar o caminho que você mexeu, ela não é opcional.

### 2. "O gate reprovou, mas é dívida alheia"

| Desfecho | Aceitável? |
|---|---|
| o gate está certo → corrija o que ele apontou | sim |
| o gate está errado → corrija o gate | sim |
| pular o gate porque "não é meu" | não, salvo exceção consciente registrada no ato |

### 3. "Encontrei um bug, mas é pré-existente / fora de escopo"

Pré-existente não é "não é meu problema agora". Se o diagnóstico está na mão e a correção cabe num commit próprio: corrija, separado, com o A/B que prova que é pré-existente. Se é grande ou depende de decisão: GAP no registro de pendências **no ato**, com o mecanismo medido. Achado que fica só no relatório, no commit ou no PR some do radar — relatório é registro histórico, não fila de trabalho.

### 4. "O teste está verde" (sem olhar o que ele testa)

Um verificador que nunca reprova não vale nada. Prove que ele reprova rodando-o contra o estado quebrado, de propósito. E a quebra tem de atingir o caminho que o teste exercita: caso de origem, um teste passou com o fix removido porque montava o próprio objeto em vez de chamar a função de produção.

Técnica barata: teste de mutação manual. Desligue a regra/fix numa cópia, rode a suíte, confirme que reprova com o sintoma esperado (não com erro de compilação), restaure.

## Checklist antes de declarar pronto

1. A validação que declarei, executei? Cole a saída, não o resumo.
2. O que mexi está coberto pelo que rodei? Mudança de runtime não é validada por type-check; componente visual não é validado por teste em jsdom.
3. Todo gate que reprovou terminou em correção (do código ou do gate), e não em skip?
4. Todo bug encontrado no caminho está corrigido ou virou GAP escrito, agora?
5. Todo verificador que escrevi foi provado no sentido negativo?
6. O que não consegui validar está escrito com o erro exato, em vez de omitido?

## Como relatar

Relate o que aconteceu, não o que deveria ter acontecido. Teste falhou: qual e por quê. Passo pulado: diga. Quebrou e consertou: as duas partes. Erro escondido vira erro repetido — e há mais de um agente trabalhando na mesma árvore.
