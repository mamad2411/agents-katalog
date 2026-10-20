---
name: hr-recruiting-pipeline
description: Acompanha e gerencia as etapas do pipeline de recrutamento da Evolution. Use quando precisar de atualização do pipeline, status de candidatos, métricas de hiring, ou ao discutir sourcing, triagem, entrevistas ou envio de ofertas. Gatilhos: "atualização do recrutamento", "pipeline de candidatos", "quantos candidatos", "status do hiring".
argument-hint: "<cargo ou ciclo de contratação>"
---

# HR — Recruiting Pipeline

Gerencie o pipeline de recrutamento do sourcing até a aceitação da oferta.

## Etapas do Pipeline

| Etapa | Descrição | Ações-Chave |
|-------|-----------|-------------|
| Sourced | Identificado e contatado | Outreach personalizado |
| Triagem | Screening por telefone/vídeo | Avaliar fit básico |
| Entrevista | Entrevistas em painel ou individuais | Avaliação estruturada |
| Debrief | Decisão do time | Calibrar feedback |
| Oferta | Envio da proposta | Pacote de remuneração, negociação |
| Aceito | Oferta aceita | Transição para onboarding |

## Métricas a Acompanhar

- **Pipeline velocity**: Dias por etapa
- **Conversion rates**: Drop-off entre etapas
- **Efetividade de fonte**: Quais canais geram contratações
- **Offer acceptance rate**: Ofertas enviadas vs. aceitas
- **Time to fill**: Dias da abertura da vaga até oferta aceita

## Canais de Sourcing — Evolution

| Canal | Tipo | Notas |
|-------|------|-------|
| LinkedIn | Ativo/Passivo | Principal canal para devs e PM |
| GitHub | Passivo | Busca por contribuidores open source |
| Comunidade Discord | Passivo | Usuários da Evolution API já engajados |
| Indicações internas | Passivo | Prioridade por alinhamento cultural |
| Programas de estágio | Ativo | Parceria com universidades BR |

## Gestão do Pipeline via Notion

Como não há ATS dedicado, use o **Notion MCP** para rastrear candidatos:

1. Crie uma database Notion com campos: Nome, Cargo, Etapa, Fonte, Entrevistador, Data da última atualização, Notas
2. Atualize o status após cada interação
3. Use filtros por etapa para ter visão do funil
4. Exporte relatórios de métricas quando necessário

```markdown
## Snapshot do Pipeline — [Cargo] — [Data]

### Funil Atual
| Etapa | Candidatos | Conv. da Etapa Anterior |
|-------|-----------|------------------------|
| Sourced | [X] | — |
| Triagem | [X] | [X]% |
| Entrevista | [X] | [X]% |
| Debrief | [X] | [X]% |
| Oferta | [X] | [X]% |
| Aceitos | [X] | [X]% |

### Tempo Médio por Etapa
| Etapa | Média (dias) | Meta |
|-------|-------------|------|
| Sourcing → Triagem | [X] | ≤ 3 |
| Triagem → Entrevista | [X] | ≤ 5 |
| Entrevista → Debrief | [X] | ≤ 2 |
| Debrief → Oferta | [X] | ≤ 3 |
| Oferta → Aceite | [X] | ≤ 5 |

### Candidatos Ativos
| Nome | Etapa Atual | Próximo Passo | Data |
|------|------------|---------------|------|
| [Nome] | [Etapa] | [Ação] | [Data] |

### Alertas
- [Candidatos parados há mais de X dias em alguma etapa]
- [Riscos de perda de candidato]
```

## Contexto Evolution

- Time pequeno (~10 pessoas) — cada contratação tem alto impacto
- Regime CLT para posições no Brasil; PJ aceito para freelancers
- Prioridade para candidatos com experiência em open source, Node.js, Go, ou integração WhatsApp/APIs
- Processo ágil: poucos rounds de entrevista, decisão rápida
- Comunicação com candidatos via Gmail MCP; atualizações internas via Discord

## Fluxo de Decisão

```
Sourcing → Triagem (30min, async OK)
        → Entrevista técnica (1h, com Danilo ou Gui)
        → Conversa cultural (30min, com Davidson)
        → Oferta → Aceite
```

## Após Atualização

Perguntar: "Quer que eu:
- Atualize o Notion com o status atual?
- Gere um relatório de métricas do pipeline?
- Prepare perguntas de entrevista para o próximo candidato?
- Rascunhe uma oferta para um candidato aprovado?"
