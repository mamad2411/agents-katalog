---
name: ops-compliance-tracking
description: Rastrear requisitos de compliance e prontidão para auditoria. Use quando precisar de compliance, preparação para auditoria, LGPD, requisito regulatório, ou quando precisar rastrear, preparar ou documentar atividades de compliance. Framework primário: LGPD (operação brasileira). Agente Lex.
argument-hint: "<framework de compliance ou área a avaliar>"
---

# /ops-compliance-tracking

> Se encontrar placeholders desconhecidos ou precisar verificar quais ferramentas estão conectadas, consulte [CONNECTORS.md](../../CONNECTORS.md).

Rastreia requisitos de compliance, prepara para auditorias e mantém prontidão regulatória. Foco primário em LGPD para operação brasileira da Evolution API.

## Agente

Lex — jurídico, compliance, contratos, LGPD.

## Frameworks Relevantes

| Framework | Foco | Relevância para Evolution |
|-----------|------|--------------------------|
| **LGPD** | Privacidade de dados (Brasil) | **CRÍTICO** — operação 100% brasileira, lida com dados de usuários e mensagens WhatsApp |
| **SOC 2** | Organizações de serviço | Relevante para clientes enterprise e parcerias como HostGator |
| **ISO 27001** | Segurança da informação | Desejável para credibilidade no mercado B2B |
| **GDPR** | Privacidade de dados (UE) | Aplicável se houver clientes europeus do Evo AI |
| **PCI DSS** | Dados de cartão de pagamento | Aplicável ao pipeline de pagamentos via Stripe |
| **Marco Civil da Internet** | Direito digital brasileiro | Aplicável a logs e registros de acesso |

## LGPD — Checklist Primário

### Bases Legais (Art. 7 e 11 LGPD)

Para cada tipo de dado pessoal processado pela Evolution API:

| Dado | Base Legal | Documentado? | Revisão |
|------|-----------|-------------|---------|
| Número de telefone WhatsApp | Contrato / Legítimo interesse | [ ] | [Data] |
| Mensagens de usuários | Execução de contrato | [ ] | [Data] |
| Dados de pagamento (Stripe) | Contrato | [ ] | [Data] |
| Dados de analytics | Legítimo interesse / Consentimento | [ ] | [Data] |
| Email de usuários (Evo AI) | Contrato | [ ] | [Data] |

### Direitos dos Titulares (Art. 18 LGPD)

- [ ] Procedimento documentado para acesso a dados (prazo: 15 dias)
- [ ] Procedimento para retificação de dados
- [ ] Procedimento para exclusão / portabilidade
- [ ] Canal de atendimento ao titular identificado
- [ ] Responsável (DPO ou encarregado) designado

### Segurança e Incidentes (Art. 46 e 48 LGPD)

- [ ] Medidas técnicas de segurança documentadas
- [ ] Processo de resposta a incidentes definido
- [ ] Prazo de notificação à ANPD (72h para incidentes graves)
- [ ] Registro de incidentes mantido
- [ ] Avaliação de impacto (DPIA) para tratamentos de alto risco

### Contratos com Terceiros (Operadores LGPD)

- [ ] Cláusula de proteção de dados em contratos de fornecedores
- [ ] DPA (Data Processing Agreement) com vendors que processam dados pessoais
- [ ] Inventário de terceiros com acesso a dados pessoais

### Política de Privacidade

- [ ] Política de privacidade publicada e acessível
- [ ] Linguagem clara, sem juridiquês
- [ ] Atualizada (data visível)
- [ ] Cobre todos os tratamentos de dados realizados

## Componentes de Rastreamento de Compliance

### Inventário de Controles
- Mapear controles para requisitos do framework
- Documentar donos de controle e evidências
- Rastrear efetividade do controle

### Calendário de Auditoria
- Datas de auditoria e deadlines futuros
- Timelines de coleta de evidências
- Deadlines de remediação

### Gestão de Evidências
- Quais evidências são necessárias para cada controle
- Onde as evidências estão armazenadas (Notion, arquivos locais)
- Quando a evidência foi coletada pela última vez

### Análise de Gap
- Requisitos vs. estado atual
- Plano de remediação priorizado
- Timeline para compliance

## Output

```markdown
## Status de Compliance: [Framework] — [Data]
**Escopo:** [O que foi avaliado] | **Avaliado por:** [Nome]

### Dashboard de Status

| Framework | Status | Controles OK | Gaps | Críticos |
|-----------|--------|-------------|------|---------|
| LGPD | 🟢/🟡/🔴 | [X/Total] | [X] | [X] |
| [Outro] | 🟢/🟡/🔴 | [X/Total] | [X] | [X] |

### Análise de Gap — LGPD

| Requisito | Status | Evidência Existente | Ação Necessária | Responsável | Deadline |
|-----------|--------|--------------------|-----------------|-----------|---------| 
| Base legal documentada | 🟡 Parcial | [Onde está] | [O que falta] | [Nome] | [Data] |
| Política de privacidade | 🔴 Ausente | — | Criar e publicar | [Nome] | [Data] |
| Canal DPO/Encarregado | 🟢 OK | [Link] | — | — | — |

### Itens Críticos (Ação Imediata)

1. **[Item crítico]**
   - Risco: [O que pode acontecer se não for resolvido]
   - Ação: [O que fazer]
   - Responsável: [Quem]
   - Deadline: [Data]

### Plano de Remediação

| Prioridade | Item | Esforço | Responsável | ETA |
|-----------|------|---------|------------|-----|
| Alta | [Item] | [Baixo/Médio/Alto] | [Nome] | [Data] |

### Calendário de Compliance

| Evento | Data | Responsável | Status |
|--------|------|------------|--------|
| Revisão anual LGPD | [Data] | Lex / Vitor | [ ] |
| Renovação de DPA com vendors | [Data] | Thaís | [ ] |
| Atualização da Política de Privacidade | [Data] | Davidson | [ ] |

### Próxima Revisão
**Data:** [Data] | **Responsável:** [Nome]
```

## Se Conectores Disponíveis

Se **Notion MCP** estiver conectado:
- Buscar documentação de compliance existente para atualizar em vez de duplicar
- Publicar checklist e plano de remediação na wiki do Notion
- Criar database de controles com status e evidências

Se **Google Calendar MCP** estiver conectado:
- Agendar revisões periódicas de compliance
- Criar lembretes para deadlines de auditoria e renovação

Se **Gmail MCP** estiver conectado:
- Rascunhar comunicações com ANPD ou titulares de dados quando necessário

## Contatos-Chave

| Papel | Pessoa | Contexto |
|-------|--------|---------|
| Jurídico Etus | Vitor Lacerda | Questões legais LGPD |
| Jurídico Brius/Etus | Thaís Menezes | Contratos com cláusulas LGPD |
| Financeiro | Samara Ângela | NFs e contratos de vendors |

## Dicas

1. **LGPD primeiro** — Para a Evolution, LGPD é o framework mais urgente e de maior risco imediato.
2. **Evidências documentadas** — "Fazemos isso" não conta para auditoria. "Fazemos isso e aqui está o registro" conta.
3. **Revisão periódica** — Compliance não é um projeto, é um processo. Revisar trimestralmente no mínimo.
4. **Envolver jurídico** — Para decisões de base legal e contratos, sempre validar com Vitor ou Thaís.
