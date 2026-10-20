---
name: refinar-ideia
description: "Conduz ideação antes de comprometer uma direção — reformulação HMW, variações, suposições ocultas e one-pager com a lista do que NÃO será feito. Use quando o orquestrador ou o arquiteto ainda está explorando o problema."
author: "Pedro Andriow (https://github.com/Andriow)"
---

# Skill: refinar-ideia

Framework de ideação em 3 fases para expandir, avaliar e convergir em uma direção antes de comprometer com planejamento técnico ou implementação.

**Agente:** `orquestrador`, `arquiteto`  

---

## Quando usar

- Antes do planejamento técnico ou da criação de spec
- Quando a ideia original é muito ampla ou tem múltiplas interpretações válidas
- Quando há pressão para "só fazer" sem avaliar alternativas

---

## Processo

### Passo 1 — Reformular como pergunta "Como poderíamos…?" (HMW)
Transforme a ideia ou solicitação original em uma pergunta no formato "Como poderíamos [objetivo]?". Esse formato abre o problema em vez de fechá-lo prematuramente. A reformulação deve capturar o objetivo de negócio, não a solução técnica. Exemplo: em vez de "Refatorar o serviço de pagamento", reformule como "Como poderíamos tornar o processamento de pagamentos mais confiável e fácil de manter?"

### Passo 2 — Gerar 5 a 8 variações da ideia
A partir da pergunta HMW, gere entre 5 e 8 variações. As variações não são apenas implementações diferentes da mesma solução — são framings alternativos do problema. Inclua ao menos:
- Uma variação que questiona se o problema precisa ser resolvido agora
- Uma variação que resolve apenas o núcleo do problema (solução mínima viável)
- Uma variação que resolve o problema de forma radicalmente diferente da solução óbvia
- Uma variação que delega o problema para fora do sistema (ex.: terceirizar, configurar, remover a necessidade)

### Passo 3 — Selecionar 2 a 3 direções mais promissoras
Avalie as variações geradas e selecione as 2 ou 3 com maior potencial. Critérios de avaliação: impacto esperado, risco de execução, esforço estimado e reversibilidade. Documente brevemente por que cada variação foi selecionada ou descartada.

### Passo 4 — Listar as suposições ocultas de cada direção selecionada
Para cada direção selecionada, liste as suposições que precisam ser verdadeiras para ela funcionar. Exemplos de suposições ocultas: "O time tem domínio da tecnologia X", "O volume de dados vai continuar no patamar atual", "O contrato de API não vai mudar". Suposições não verificadas são os principais vetores de risco.

### Passo 5 — Identificar a direção com melhor relação impacto × risco × esforço
Com base nas suposições mapeadas, escolha a direção vencedora. A escolha deve ser explícita e justificada — não um consenso implícito. Se duas direções tiverem potencial similar, prefira a mais reversível (a que permite mudar de ideia com menor custo).

### Passo 6 — Produzir o one-pager da direção escolhida
Documente a direção vencedora em um one-pager com os seguintes elementos obrigatórios:

**O que faremos:** descrição concisa da solução escolhida.

**Por que esta direção e não as outras:** justificativa explícita comparando com as direções descartadas.

**O que NÃO faremos nesta entrega:** lista explícita de itens excluídos do escopo. Esta é a parte mais valiosa do one-pager — é onde o scope creep é bloqueado antes de começar.

**Critérios de sucesso mensuráveis:** métricas ou condições verificáveis que definem quando a entrega está concluída. Evitar critérios vagos como "o sistema vai ficar mais rápido" — preferir "latência p95 abaixo de 200ms em produção".

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "A ideia já está clara, posso ir direto para o planejamento" | Clareza prematura é armadilha. A ideação leva 15 minutos e pode salvar dias de retrabalho ao revelar suposições ocultas. |
| "Gerar variações é perda de tempo" | A primeira solução raramente é a melhor. Variações revelam suposições ocultas que você não saberia que tinha até tentar alternativas. |
| "A lista de 'O que não faremos' é óbvia" | Se é óbvia, escreva em 30 segundos. Se der trabalho, você encontrou exatamente onde o scope creep vai acontecer. |
| "Temos urgência, não há tempo para refinar" | Urgência é razão para refinar mais rápido, não para pular. Uma direção errada executada com urgência chega errado mais rápido. |
| "Já sei qual é a melhor direção" | Se já sabe, documente as suposições e o one-pager em 10 minutos. Se não conseguir, a certeza era prematura. |

---

## Anti-padrões bloqueados

- Gerar variações que são apenas detalhes técnicos diferentes da mesma abordagem
- Selecionar a direção sem documentar as suposições ocultas de cada uma
- Omitir a lista "O que NÃO faremos nesta entrega"
- Usar critérios de sucesso vagos ou não mensuráveis
- Pular a reformulação HMW e começar direto nas soluções
- Produzir um one-pager de mais de uma página

---

## Checklist de conclusão

- [ ] Ideia original reformulada como pergunta "Como poderíamos…?"
- [ ] Entre 5 e 8 variações geradas, incluindo variações que questionam o problema em si
- [ ] 2 a 3 direções selecionadas com justificativa de descarte das demais
- [ ] Suposições ocultas listadas para cada direção selecionada
- [ ] Direção vencedora escolhida com justificativa explícita de impacto × risco × esforço
- [ ] One-pager produzido com as 4 seções obrigatórias: o que faremos, por que esta direção, o que não faremos, critérios de sucesso
- [ ] Critérios de sucesso são mensuráveis e verificáveis
- [ ] One-pager aprovado antes de iniciar planejamento técnico ou spec
