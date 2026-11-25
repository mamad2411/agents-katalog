---
name: publicist-brazil-lgpd-compliance
description: Brazil LGPD/ANPD compliance gate for earned media, journalist data handling, cross-border transfers, consent, DPO, ANPD enforcement. Use as mandatory compliance gate for all Brazil earned media activities.
license: MIT
metadata:
  version: "0.1.0"
  author: "shy-tangerine"
---

# Brazil LGPD/ANPD compliance, Brazil market

**Scope**. Mandatory compliance gate for ALL Brazil earned media activities. Pair with `publicist-brazil` + all Brazil platform skills.

---

## Legal framework (must recheck at task time)

| Law/Regulation | Scope | Key Requirement | Enforcement |
|---|---|---|---|
| **LGPD (Lei 13.709/2018)** | Personal data processing | Legal basis, rights, DPO, breach notification, international transfer | ANPD, fines up to 2% revenue (cap R$ 50M) |
| **Marco Civil (Lei 12.965/2014)** | Internet governance | Data retention 12 months, judicial order for removal | Judicial |
| **CDC (Lei 8.078/1990)** | Consumer protection | No misleading advertising, proof burden on advertiser | PROCON, judicial |
| **ANPD Resoluções** | Regulatory guidance | Cookie consent, DPO requirements, RIPD, international transfer clauses | ANPD |

---

## What constitutes personal data (LGPD art. 5)
In PR context, journalist data = **dado pessoal**.
- Nome, e-mail corporativo, telefone, veículo, editoria/beat
- Perfil LinkedIn/Twitter, histórico de matérias, preferências de pauta
- **Qualquer combinação que identifique** = dado pessoal

### Special category (LGPD art. 11), unlikely in PR but possible
- Dado sensível: origem racial, opinião política, filiação sindical, saúde, vida sexual, biométrico, genético
- **PR risk**. Political beat journalist's affiliation, health journalist's medical history

---

## Legal bases for journalist data (LGPD art. 7)

### For earned media: legitimate interest (Art. 7, IX), **primary**
```
Base: Legítimo interesse do controlador
Requisitos:
1. Finalidade legítima (relações com imprensa, earned media)
2. Necessidade (dado mínimo para contatar jornalista relevante)
3. Balanceamento (interesse do controlador ≠ direitos do titular)
4. Transparência (Política de Privacidade acessível)
5. Direito de oposição fácil (opt-out em toda comunicação)
```

### Alternative: consent (Art. 7, I), **rarely practical**
- Explicit, informed, free, specific, granular
- Hard to get at scale for journalist lists
- **Use only** for newsletters, marketing lists

---

## Cross-border transfer (LGPD art. 33-36 + ANPD)

### Trigger scenarios (common in PR)
| Scenario | Status | Required Mechanism |
|---|---|---|
| Salesforce/HubSpot/Pipedrive (US) com dados de jornalistas | **Transferência internacional** | Cláusulas contratuais padrão (ANPD) + TIA + Consentimento ou legítimo interesse documentado |
| Gmail/Outlook/ProtonMail (exterior) para contatos de imprensa | **Transferência internacional** | Cláusulas padrão + TIA + Base legal |
| OpenAI/Claude/Gemini API com perfis de jornalistas | **Transferência internacional** | Cláusulas padrão + TIA + Base legal |
| Meltwater/Cision/Muck Rack (exterior) monitoring | **Processador no exterior** | AVV + Cláusulas padrão + TIA (verificar se provedor já tem) |
| Notion/Airtable/Google Sheets (EUA) com lista de imprensa | **Transferência internacional** | Cláusulas padrão + TIA |
| Ferramentas nacionais (Nextcloud, Zoho BR, Azure BR, AWS SA) | **Sem transferência** | **Ponytail: local-first** (recomendado) |

### ANPD Mechanisms (Resolução CD/ANPD nº 19/2024)
1. **Cláusulas Contratuais Padrão (SCC)**, Modelo ANPD obrigatório
2. **TIA (Transfer Impact Assessment)**, Avaliação de risco do país destino
3. **Regra de Adequação**, País com nível adequado (não se aplica a EUA)
4. **Normas Corporativas Globais (BCR)**, Para grupos multinacionais
5. **Consentimento Específico**, Difícil para listas de imprensa

### Minimal compliance (ponytail: local-first)
> **Regra de ouro**. Mantenha dados de jornalistas **apenas em ferramentas brasileiras**. Isso evita transferência internacional e elimina complexidade SCC/TIA.

---

## ANPD enforcement (realidade 2023-2026)

### Multas documentadas
| Ano | Caso | Sanção | Fonte |
|---|---|---|---|
| 2023 | Telecom em Vila Velha (ES): consentimento vago, ausência de DPO | Duas multas somando R$ 14,4 mil + advertência | [DOU/g1, 2023-07-06](https://g1.globo.com/tecnologia/noticia/2023/07/06/anpd-aplica-primeira-multa-por-infracao-a-lgpd.ghtml) |
| 2026 | Processo contra 21 empresas e órgãos públicos por falhas de encarregado de dados | Sanções em avaliação | [ANPD, 2026-08](https://www.gov.br/anpd/pt-br/assuntos/noticias/anpd-conclui-monitoramento-avaliar-sancao-empresas-orgaos-publicos) |

### ANPD focus areas (2024-2026)
1. **Consentimento válido**, Específico, informado, livre, inequívoco
2. **DPO nomeado**, Obrigatório para tratamento em larga escala
3. **RIPD (Relatório de Impacto)**, Alto risco (perfilamento, larga escala, sensíveis)
4. **Transferência internacional**, Cláusulas ANPD + TIA documentada
5. **Direitos do titular**, Atendimento em 15 dias (acesso, retificação, exclusão, oposição)

### PR-specific risk vectors
| Activity | Risk | Mitigation |
|---|---|---|
| Lista de jornalistas no HubSpot (EUA) | Transferência sem SCC | Migrar para CRM BR ou assinar SCC ANPD |
| Lista no Google Sheets (EUA) | Transferência sem base legal | Migrar para Nextcloud BR / Zoho BR |
| Enviar pauta via Gmail | Transferência de dados | Usar e-mail corporativo BR (Zoho, Locaweb, UOL Host) |
| Alimentar Claude/OpenAI com perfis | Transferência + profiling | **Não faça**. Use modelo local (llama.cpp) |
| Clipping no Meltwater (EUA) | Processador exterior | Verificar AVV + SCC do fornecedor |

---

## Practical compliance checklist (per pitch/activity)

### Pre-activity (setup)
- [ ] **Base legal documentada** para cada base de contatos (Legítimo Interesse = padrão)
- [ ] **Política de Privacidade** pública com seção "Imprensa/Contatos de Jornalistas"
- [ ] **DPO nomeado** e contatos publicados (se larga escala)
- [ ] **Ferramentas nacionais** para base de jornalistas (CRM BR, e-mail BR, planilha BR)
- [ ] **SCC ANPD assinadas** se qualquer ferramenta estrangeira inevitável
- [ ] **TIA documentada** para cada transferência internacional
- [ ] **Opt-out funcional** em 100% das comunicações comerciais

### Per communication
- [ ] **Opt-out visível** em 100% e-mails/WhatsApp ("Responda SAIR para não receber")
- [ ] **Identificação clara**, remetente, organização, CNPJ, endereço físico
- [ ] **Finalidade explícita**, "Contato para sugestão de pauta sobre X"
- [ ] **Dados mínimos**, só nome, veículo, editoria, contato
- [ ] **Honor opt-out imediato**, "SAIR" = delete em 24h + confirmação

### Data lifecycle
- [ ] **Retenção**. 2 anos após último contato (ou até oposição)
- [ ] **Exclusão automática** / processo manual documentado
- [ ] **Direitos do titular**. Processo 15 dias (acesso, retificação, exclusão, portabilidade, oposição)
- [ ] **Log de consentimento/oposição**, timestamp, canal, detalhes

### Breach response (LGPD art. 48)
- [ ] **Plano de resposta** documentado
- [ ] **Notificação ANPD** em até 2 dias úteis (se risco relevante)
- [ ] **Comunicação ao titular** se risco alto
- [ ] **Registro interno** completo (mesmo se não notificável)

---

## LGPD + WhatsApp (cross-reference)

### WhatsApp specific (via `publicist-brazil-whatsapp-pitch`)
- [ ] **Opt-out no 1º e-mail**. "Responda SAIR para não receber WhatsApp"
- [ ] **Legítimo interesse** documentado para WhatsApp
- [ ] **Dados mínimos**. nome, veículo, editoria, WhatsApp
- [ ] **Retenção**. 2 anos sem interação = delete
- [ ] **Opt-out imediato**. "SAIR" = delete + confirmação

---

## ANPD practical resources

### Official guides
- `https://www.gov.br/anpd/pt-br/assuntos/guias`, Guias oficiais
- `https://www.anpd.gov.br/cartilha-lgpd`, Cartilha LGPD
- `https://www.anpd.gov.br/transferencia-internacional`, Transferência internacional
- `https://www.anpd.gov.br/clausulas-contratuais-padrao`, Cláusulas padrão (SCC)

### Compliance tools
- `https://www.anpd.gov.br/relatorio-impacto`, RIPD guia
- `https://www.anpd.gov.br/dpo`, DPO requisitos
- `https://www.anpd.gov.br/fiscalizacao`, Fiscalização orientações

---

## Negative patterns (evite)
- ❌ "Journalist data is public, so LGPD doesn't apply", **Público ≠ livre**
- ❌ "We have consent in our TOS", **TOS ≠ consentimento LGPD válido**
- ❌ "HubSpot has SCC", **Você precisa assinar SCC ANPD, não do HubSpot**
- ❌ "We'll just use Gmail", **Gmail = transferência internacional**
- ❌ "No budget for local tools", **Risco de multa > custo de ferramenta BR**
- ❌ "One-time export to Excel", **Exportação = tratamento, requer base legal**

---

## References
- `https://www.gov.br/anpd/pt-br`, ANPD portal
- `https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/L13709.htm`, LGPD oficial
- `https://www.anpd.gov.br/clausulas-contratuais-padrao`, SCC ANPD
- `wiki/public-relations/brazil-data-and-lgpd.md`
- `skills/publicist-brazil/references/law-and-ethics.md`
- `skills/publicist-brazil-whatsapp-pitch/SKILL.md`, WhatsApp LGPD specifics

## What this skill does not do
- NG No legal advice (escalate to Brazil-qualified LGPD counsel)
- NG No automated compliance checker
- NG No MCP/CLI tools (reference only)
