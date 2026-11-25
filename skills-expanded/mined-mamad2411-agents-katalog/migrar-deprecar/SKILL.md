---
name: migrar-deprecar
description: "Conduz deprecação estruturada com padrões Strangler, Adapter e Feature Flag, Churn Rule e resolução de código zumbi. Use quando o arquiteto ou o tech-lead vai remover ou substituir código legado."
author: "Pedro Andriow (https://github.com/Andriow)"
disable-model-invocation: true
---

# Skill: migrar-deprecar

Processo estruturado para deprecar código, APIs ou dependências sem quebrar consumidores. A deprecação é inevitável — o que varia é se ela é feita com planejamento ou com incidentes.

**Agente:** `arquiteto`, `tech-lead`  

---

## Quando usar

- Ao remover API, endpoint ou módulo com consumidores ativos
- Ao atualizar dependência com breaking changes
- Ao substituir implementação legada por nova abordagem

---

## Processo

### Passo 1 — Inventariar consumidores
Antes de qualquer outra ação, mapear todos os consumidores do que será deprecado. Buscar por: importações diretas, chamadas de API (logs de produção + código), referências em configuração, dependências transitivas.

Nenhuma deprecação começa sem esse inventário completo. Deprecar sem saber quem consome é garantia de incidente.

### Passo 2 — Classificar consumidores
Categorizar cada consumidor encontrado:

| Categoria | Definição | Ação |
|---|---|---|
| Consumidor com dono identificado | Time responsável conhecido | Comunicar e coordenar migração |
| Consumidor sem dono (código zumbi) | Sem time responsável, mas com uso ativo | Escalar para encontrar dono — não pode ficar em limbo |
| Sem consumidores | Nenhuma referência ativa encontrada | Pode remover diretamente, sem cerimônia |

**Código Zumbi** (sem dono identificado com consumidores ativos) é o caso mais perigoso. Não pode ser ignorado. Deve ser resolvido: encontrar o dono, migrar, ou remover após análise de impacto formal com aprovação do tech-lead.

### Passo 3 — Escolher o padrão de migração
Selecionar o padrão adequado com base no tipo de mudança:

**Padrão Strangler** — preferido para APIs e serviços:
1. Criar nova implementação em paralelo com a antiga
2. Rotear tráfego incrementalmente: 1% → 10% → 50% → 100%
3. Manter a implementação antiga funcionando até 0% de tráfego
4. Desligar a antiga somente após período de observação (mínimo 7 dias em 0%)

**Padrão Adapter** — preferido para mudanças de interface interna:
1. Manter a interface antiga como wrapper da nova implementação
2. Marcar a interface antiga com `@deprecated` e indicar a nova como alternativa
3. Definir prazo de remoção vinculado a uma major version futura
4. Nunca remover sem major version bump — remoção silenciosa quebra contratos

**Padrão Feature Flag** — preferido para mudanças comportamentais:
1. Implementar novo comportamento atrás de feature flag desligada por padrão
2. Migrar consumidores um a um, ativando a flag por consumidor
3. Remover flag e código antigo somente após todos os consumidores migrarem
4. Flag nunca vira permanente — tem data de remoção definida na criação

### Passo 4 — Criar ADR documentando a deprecação
Criar um ADR (Architecture Decision Record) com: o que está sendo deprecado, por que está sendo deprecado, qual é a alternativa, e qual é o prazo. Usar a skill `documentar-decisoes` para o formato correto.

Deprecação sem ADR não tem rastreabilidade. Quando alguém perguntar "por que esse código foi removido?", a resposta deve estar no ADR, não no Slack.

### Passo 5 — Comunicar consumidores antes de deprecar
Notificar cada consumidor identificado com antecedência suficiente para a migração. Os canais de comunicação, em ordem de permanência:

1. Issue no repositório com label `deprecation` e prazo
2. Comentário `@deprecated` no código apontando para a alternativa
3. Entrada no CHANGELOG marcando a versão de deprecação e a versão planejada de remoção
4. Mensagem no canal do time (Slack) — complementar, não substituto dos itens acima

Slack some. Issue, comentário e CHANGELOG ficam.

### Passo 6 — Executar a migração incremental
Migrar consumidores com monitoramento ativo em cada etapa. Para cada consumidor migrado: verificar métricas de erro, confirmar que o comportamento está correto na nova implementação, aguardar período de observação antes do próximo consumidor.

**Churn Rule:** Quem depreca é responsável por migrar os consumidores. Não é aceitável deprecar e deixar os consumidores para se virarem. Se você é dono da infraestrutura sendo deprecada, você migra os consumidores — ou coordena ativamente a migração com os times donos, com prazo acordado.

### Passo 7 — Remover o código antigo
Remover somente após:
- Confirmação de 0 consumidores ativos (verificar logs de produção, não apenas código)
- Período de observação mínimo de 7 dias com 0 uso
- ADR atualizado com data de remoção efetiva
- CHANGELOG atualizado marcando a remoção na versão correta

---

## Racionalizações bloqueadas

| Racionalização | Rebate |
|---|---|
| "Vou só marcar @deprecated e avisar no Slack" | Aviso no Slack some em dias. ADR + issue + comentário no código + PR de migração com prazo — esses ficam e são rastreáveis. |
| "Os consumidores que se virem" | Churn Rule. Você depreca, você migra. Isso não é negociável. |
| "Código zumbi não incomoda ninguém" | Código zumbi acumula débito técnico, confunde novos devs e vai quebrar na próxima atualização de dependência — geralmente em produção, de madrugada. |
| "Posso remover assim que criar a nova implementação" | A migração é a parte difícil. Novo código pronto não significa consumidores migrados. Remover antes de migrar é incidente garantido. |
| "É só uma mudança interna, não precisa comunicar" | A Lei de Hyrum garante que alguém depende do comportamento que você acha que é "detalhe interno". Comunicar sempre. |

---

## Anti-padrões bloqueados

- Iniciar deprecação sem inventário completo de consumidores
- Remover código antes do período de observação em 0% de uso
- Usar Slack como único canal de comunicação de deprecação
- Deprecar sem ADR documentando a alternativa e o prazo
- Deixar código zumbi em estado indefinido por mais de 2 sprints
- Misturar deprecação com outras mudanças no mesmo PR (impossibilita rollback isolado)
- Feature flag que nunca tem data de remoção definida

---

## Checklist de conclusão

- [ ] Inventário completo de consumidores realizado antes de qualquer ação
- [ ] Consumidores classificados (com dono / sem dono / sem consumidores)
- [ ] Código zumbi resolvido — nenhum consumidor em estado indefinido
- [ ] Padrão de migração escolhido e justificado (Strangler / Adapter / Feature Flag)
- [ ] ADR criado documentando deprecação, alternativa e prazo
- [ ] Todos os consumidores comunicados via issue + comentário no código + CHANGELOG
- [ ] Migração executada incrementalmente com monitoramento em cada etapa
- [ ] Churn Rule aplicada — quem deprecou coordenou a migração de todos os consumidores
- [ ] Remoção do código antigo feita somente após 0 consumidores + período de observação
- [ ] ADR e CHANGELOG atualizados com data de remoção efetiva
