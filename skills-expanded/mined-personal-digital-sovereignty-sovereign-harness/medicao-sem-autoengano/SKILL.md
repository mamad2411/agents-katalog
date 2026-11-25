---
name: medicao-sem-autoengano
description: Como medir comportamento de modelo e de agente (tool-calling, aderência a contrato, classificação, desempenho) sem que o número minta — fixture que apodrece, placar desalinhado com o produto, silêncio como modo de falha, poder estatístico, regime que mudou, agregado que esconde classe em 0%, e espera que nunca termina. Carregar antes de rodar/interpretar qualquer bench ou placar de trials, e antes de decidir algo com base num número de modelo.
---

# Medir sem se enganar — o instrumento erra antes do produto

Um placar de trials é um instrumento, e instrumento descalibrado mente com a mesma confiança com que mede. Caso de origem: uma pergunta trivial ("adicionar 2 tools degrada o tool-calling?") levou quatro rodadas até um número confiável — todos os tropeços foram na medição, e três defeitos reais de produto só apareceram porque a medição foi feita direito.

## Regras

1. **Fixture que cita dado vivo apodrece em silêncio.** Resolva a referência em runtime e aborte com explicação se a precondição não existir. Sub-teste que zera por completo (0/N) quase nunca é o modelo piorando — modelo degrada em gradiente; zero absoluto cheira a precondição quebrada.
2. **O mesmo modelo emite o mesmo argumento em formas diferentes** (objeto, string serializada, lista). Capture a forma bruta antes de concluir.
3. **O placar aceita o que o PRODUTO aceita.** Pontuação e execução são a mesma decisão em dois lugares; mudou uma, muda a outra no mesmo commit.
4. **Silêncio é o pior modo de falha, e costuma ser comportamento correto sem instrução.** Toda proibição num prompt vem com a alternativa ("não invente X — diga que não achou e ofereça Y").
5. **Poder estatístico.** Sub-teste saturado não informa. n=6 não separa 5/6 de 4/6. Concentre trials no que discrimina — e separe ruído de mecanismo: "não detectável na amostra, MAS existe este custo específico" é o relato honesto.
6. **Número histórico foi medido noutro regime.** Antes de usar baseline do CHANGELOG, confirme dados, modelos, fixture e contexto iguais; senão, re-meça o baseline agora.
7. **Hipótese refutada fica escrita**, inclusive quando a mudança é mantida por outro motivo ("contenção de custo, não conserto").
8. **Agregado esconde classe em 0%.** Todo placar de classificação sai desdobrado por classe e por origem do dado; confira quantas classes o conjunto realmente cobre. Caso de origem: 84% global com uma classe inteira em 0/8 e 14 de 25 classes sem nenhum dado.
9. **Mudou o número de classes, o conjunto ou a forma do prompt: os baselines viraram história.** Menos classes é tarefa mais fácil.
10. **Medir o agente de ponta a ponta**: o harness de medição tem de fazer o que o usuário faria (responder diálogos, parar no prazo), senão mede o próprio travamento. Confira quem escreveu cada turno antes de acreditar num placar por turno. Placar de tool-calling num papel não transfere para outro.
11. **Desempenho**: compare decode com decode e prefill com prefill; cache de prefixo e throttling térmico são variáveis experimentais — controle ou registre.

## Higiene de processo

- Nunca espere por `pgrep -f` (casa o próprio comando → espera infinita). Use arquivo-marcador escrito pelo próprio job, e confirme que o job NASCEU antes de armar a espera.
- O sumário de um test runner é texto colorido: tire a cor (`\x1b\[[0-9;]*[A-Za-z]`) antes de filtrar e cruze com o artefato em disco.

## Ritual

1. Derrubar processos órfãos; confirmar porta livre e o binário certo em execução.
2. Confirmar precondições de dado de cada fixture, em runtime.
3. Medir o baseline agora.
4. Concentrar trials no sub-teste discriminante.
5. Capturar a forma bruta das falhas.
6. Desdobrar por classe e origem.
7. Registrar número, mecanismo dos erros e hipóteses refutadas.
