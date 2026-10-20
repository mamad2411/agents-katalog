---
name: ops-vendor-review
description: Avaliar um fornecedor — análise de custo, avaliação de risco e recomendação. Use quando revisar proposta de novo vendor, decidindo renovar ou substituir contrato, comparando dois vendors lado a lado, ou construindo breakdown de TCO e pontos de negociação antes da aprovação. Agente Nex.
argument-hint: "<nome do vendor ou proposta>"
---

# /ops-vendor-review

> Se encontrar placeholders desconhecidos ou precisar verificar quais ferramentas estão conectadas, consulte [CONNECTORS.md](../../CONNECTORS.md).

Avalia um vendor com análise estruturada cobrindo custo, risco, performance e fit para o contexto da Evolution API.

## Agente

Nex — sales, pipeline, propostas, qualificação.

## O Que Preciso de Você

- **Nome do vendor**: Quem está avaliando?
- **Contexto**: Avaliação de novo vendor, decisão de renovação ou comparação?
- **Detalhes**: Termos de contrato, precificação, documento de proposta ou dados de performance atual

## Framework de Avaliação

### Análise de Custo (Total Cost of Ownership)
- Custo total de propriedade (não apenas taxas de licença)
- Custos de implementação e migração
- Custos de treinamento e onboarding
- Suporte e manutenção contínuos
- Custos de saída (migração de dados, rescisão de contrato)

### Avaliação de Risco
- Estabilidade financeira do vendor
- Postura de segurança e compliance (LGPD, SOC 2)
- Risco de concentração (dependência de vendor único)
- Lock-in contratual e termos de saída
- Continuidade de negócio e disaster recovery

### Métricas de Performance
- Conformidade com SLA
- Tempo de resposta do suporte
- Uptime e confiabilidade
- Cadência de entrega de features
- Satisfação dos clientes (reviews, referências)

### Matriz de Comparação
Ao comparar vendors, produzir matriz lado a lado cobrindo: precificação, features, integrações, segurança, suporte, termos de contrato e referências.

### Considerações Específicas Evolution

Para vendors de tecnologia/SaaS avaliados pela Evolution API, considerar também:

| Critério | Por Que Importa |
|---------|----------------|
| API disponível | Time técnico pequeno — automação é essencial |
| Integração com stack atual | Node.js, Go, PostgreSQL, Docker |
| Suporte em português ou BR | Operação remota no Brasil |
| Modelo de preço por uso | Startup — evitar custos fixos altos |
| LGPD compliance | Operação brasileira — obrigatório |
| Faturamento em BRL | Reduz complexidade cambial |

## Output

```markdown
## Avaliação de Vendor: [Nome do Vendor]
**Data:** [Data] | **Tipo:** [Novo / Renovação / Comparação]

### Resumo
[2-3 frases de recomendação]

### Análise de Custo
| Componente | Custo Anual | Notas |
|-----------|------------|-------|
| Licença/assinatura | R$ [X] | [Por seat, flat, baseado em uso] |
| Implementação | R$ [X] | [Único] |
| Suporte/manutenção | R$ [X] | [Incluído ou add-on] |
| **Total Ano 1** | **R$ [X]** | |
| **Total 3 Anos** | **R$ [X]** | |

### Avaliação de Risco
| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| [Risco] | Alta/Média/Baixa | Alta/Média/Baixa | [Mitigação] |

### Pontos Fortes
- [Ponto forte 1]
- [Ponto forte 2]

### Preocupações
- [Preocupação 1]
- [Preocupação 2]

### Recomendação
[Prosseguir / Negociar / Recusar] — [Justificativa]

### Pontos de Negociação
- [Ponto de alavancagem 1]
- [Ponto de alavancagem 2]

### Checklist de Due Diligence
- [ ] Verificar LGPD compliance (onde dados são armazenados?)
- [ ] Verificar uptime histórico e SLA garantido
- [ ] Checar cláusula de rescisão e portabilidade de dados
- [ ] Conferir se há faturamento em BRL ou apenas USD
- [ ] Verificar referências de clientes similares (B2B, SaaS)
- [ ] Confirmar suporte durante horário comercial BRT
```

## Se Conectores Disponíveis

Se **Notion MCP** estiver conectado:
- Buscar avaliações de vendor existentes, contratos e reviews de performance
- Puxar políticas de contratação e limites de aprovação

Se o workflow de contratação for manual:
- Gerar checklist de aprovação para compartilhar com Davidson e Samara (financeiro)
- Documentar resultado da avaliação em arquivo local em `workspace/projects/`

## Dicas

1. **Faça upload da proposta** — Posso extrair preços, termos e SLAs de documentos de vendor.
2. **Compare vendors** — "Comparar Vendor A vs Vendor B" gera análise lado a lado.
3. **Inclua gasto atual** — Para renovações, saber o que paga hoje ajuda a avaliar mudanças de preço.
