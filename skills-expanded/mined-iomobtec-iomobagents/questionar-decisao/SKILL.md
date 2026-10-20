---
name: questionar-decisao
description: "Revisão adversarial de decisões de alto impacto, com revisor cego à justificativa, enviesado a refutar, em no máximo 3 ciclos. Use quando o arquiteto ou o tech-lead quer estressar uma decisão crítica."
author: "Pedro Andriow (https://github.com/Andriow)"
---

# Skill: questionar-decisao

Técnica de revisão adversarial para decisões arquiteturais ou técnicas de alto impacto, usando um revisor estruturalmente separado da justificativa original para eliminar o viés de confirmação.

**Agente:** `arquiteto`, `tech-lead`  

---

## Quando usar

- Antes de commitar uma decisão arquitetural de alto impacto
- Quando há pressão para escolher entre duas abordagens radicalmente diferentes
- Quando a decisão vai ser difícil ou cara de reverter

---

## Processo

### Passo 1 — CLAIM: Definir a decisão e sua justificativa
Articule com precisão a decisão sendo tomada. A declaração deve conter: (a) o que está sendo decidido, (b) as alternativas que foram consideradas e rejeitadas, (c) a justificativa para a escolha feita. Esta justificativa será usada apenas internamente — ela NÃO será passada ao revisor adversarial.

### Passo 2 — EXTRACT: Extrair o artefato e o contrato
Separe da justificativa dois elementos:

**Artefato:** o objeto concreto da decisão — código, diagrama, spec, estrutura de dados, contrato de API. Deve ser auto-contido e legível sem a justificativa.

**Contrato:** o que esta decisão deve garantir — requisitos funcionais e não-funcionais que a decisão precisa satisfazer. Exemplos: "deve suportar 10.000 requisições por segundo", "deve ser deployável sem downtime", "deve ser reversível em menos de 1 hora".

### Passo 3 — DOUBT: Apresentar ao revisor adversarial apenas o artefato e o contrato
O revisor adversarial recebe APENAS o artefato e o contrato — nunca a justificativa. Isso é deliberado: a justificativa ativa o viés de confirmação, fazendo o revisor buscar evidências de que a decisão está correta em vez de buscar razões para ela estar errada.

O revisor é "biased to disprove, not approve". Ele deve investigar ativamente:
- Casos de borda que o artefato não cobre
- Suposições implícitas que podem não ser verdadeiras
- Alternativas que não foram consideradas e que satisfariam o contrato igualmente ou melhor
- Consequências de longo prazo que a decisão não antecipa
- Pontos de falha únicos introduzidos pela decisão

### Passo 4 — RECONCILE: Decidir o destino de cada objeção
Para cada objeção levantada pelo revisor, tome uma das três decisões abaixo — e documente qual foi escolhida e por quê:

**(a) Incorporar:** a objeção revela um problema real; a decisão será modificada para endereçá-la.

**(b) Rejeitar com justificativa:** a objeção não se aplica ao contexto específico desta decisão — documente o motivo explicitamente. "Não se aplica" sem justificativa não é aceitável.

**(c) Abrir issue:** a objeção é válida mas está fora do escopo desta decisão; registrar como item de acompanhamento com dono e prazo.

### Passo 5 — STOP: Encerrar após convergência ou após 3 ciclos
Repita os Passos 3 e 4 até que nenhuma objeção nova surja, ou até completar no máximo 3 ciclos. Se após 3 ciclos ainda houver objeções não reconciliadas, o sinal é que a decisão precisa ser simplificada — não debatida mais. Uma decisão que não resiste a 3 ciclos de questionamento adversarial é complexa demais para ser considerada segura.

**Output final obrigatório:**
- Decisão original (possivelmente modificada após reconciliação)
- Lista de objeções com o destino de cada uma (incorporada / rejeitada com justificativa / issue aberta)
- Lista de issues abertas com dono e prazo

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Já pensei bastante, não preciso de revisor adversarial" | O viés de confirmação é invisível para quem o tem. A revisão adversarial não é desconfiança — é metodologia. Quem pensa bastante numa direção fica melhor em defender essa direção, não em questioná-la. |
| "Isso vai atrasar a decisão" | 3 ciclos de 15 minutos cada totalizam 45 minutos. Decisão arquitetural errada pode atrasar meses e exigir reescrita. O tradeoff é assimétrico. |
| "Se eu apresentar a justificativa, o revisor vai entender melhor" | Exatamente o oposto — o revisor precisa ser "cego" à justificativa para encontrar os pontos cegos. Justificativa apresentada ao revisor transforma a revisão em validação. |
| "As objeções levantadas são óbvias, já pensei nelas" | Se são óbvias, documente a reconciliação em 5 minutos. Se der trabalho justificar por que não se aplicam, elas não eram tão óbvias assim. |
| "Mais de 3 ciclos vai nos dar mais segurança" | Mais ciclos não aumentam segurança — aumentam paralisia. Após 3 ciclos, ou a decisão está boa o suficiente, ou ela precisa ser simplificada. |

---

## Anti-padrões bloqueados

- Passar a justificativa ao revisor adversarial junto com o artefato e o contrato
- Rejeitar objeções sem documentar a justificativa explícita da rejeição
- Fazer mais de 3 ciclos sem encerrar ou simplificar a decisão
- Usar "não se aplica" como resposta sem explicar por que não se aplica no contexto específico
- Omitir o output final (lista de objeções reconciliadas e issues abertas)
- Iniciar o processo sem um artefato concreto — decisões abstratas sem artefato não podem ser revisadas objetivamente
- Confundir revisão adversarial com ataque pessoal — o revisor questiona o artefato, não o autor

---

## Checklist de conclusão

- [ ] Decisão articulada com o que foi decidido, alternativas rejeitadas e justificativa
- [ ] Artefato concreto extraído (código, diagrama, spec, contrato de API)
- [ ] Contrato definido com requisitos verificáveis que a decisão deve satisfazer
- [ ] Revisor adversarial recebeu apenas artefato + contrato, sem a justificativa
- [ ] Cada objeção recebeu uma das três respostas: incorporada, rejeitada com justificativa ou issue aberta
- [ ] Máximo de 3 ciclos respeitado
- [ ] Output final produzido: decisão (revisada se necessário) + lista de objeções reconciliadas + issues abertas com dono e prazo
- [ ] Issues abertas registradas no sistema de rastreamento do time
