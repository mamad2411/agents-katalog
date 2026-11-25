---
name: cs-customer-research
description: Pesquisa multi-fonte sobre pergunta ou tópico de cliente com atribuição de fontes. Use quando um cliente pergunta algo que precisa ser verificado, investigando se um bug foi reportado antes, verificando o que foi dito anteriormente a uma conta específica, ou coletando contexto antes de redigir uma resposta. / Multi-source research on a customer question or topic with source attribution. Use when a customer asks something you need to look up, investigating whether a bug has been reported before, checking what was previously told to a specific account, or gathering background before drafting a response.
argument-hint: "<pergunta ou tópico>"
---

# /cs-customer-research

> Se encontrar integrações não configuradas, verifique [CONNECTORS.md](../../CONNECTORS.md).

Pesquisa multi-fonte sobre uma pergunta de cliente, tópico de produto ou consulta relacionada à conta. Sintetiza achados de todas as fontes disponíveis com atribuição clara e pontuação de confiança.

## Usage

```
/cs-customer-research <pergunta ou tópico>
```

## Workflow

### 1. Parse da Solicitação de Pesquisa

Identificar que tipo de pesquisa é necessária:
- **Pergunta do cliente**: Algo que um cliente perguntou que precisa de resposta (ex: "Nosso produto suporta SSO com Okta?")
- **Investigação de problema**: Background sobre um problema reportado (ex: "Esse bug foi reportado antes? Qual é o workaround conhecido?")
- **Contexto de conta**: Histórico com um cliente específico (ex: "O que dissemos à Acme Corp da última vez que perguntaram sobre isso?")
- **Pesquisa de tópico**: Tópico geral relevante para trabalho de suporte (ex: "Boas práticas para lógica de retry de webhook")

Antes de buscar, esclarecer o que realmente precisa ser encontrado:
- É uma pergunta factual com resposta definitiva?
- É uma pergunta contextual que requer múltiplas perspectivas?
- É uma pergunta exploratória onde o escopo ainda está sendo definido?
- Quem é o público para a resposta (time interno, cliente, liderança)?

### 2. Buscar nas Fontes Disponíveis

Buscar sistematicamente pelos níveis de fonte abaixo, adaptando ao que está conectado. Não parar no primeiro resultado — cruzar referências entre fontes.

**Tier 1 — Fontes Internas Oficiais (maior confiança):**
- **Notion MCP**: docs de produto, runbooks, FAQs, documentos de política
- Roadmap de produto (interno): timelines de features, prioridades

**Tier 2 — Contexto Organizacional:**
- **int-evo-crm** (`/int-evo-crm`): notas de conta, histórico de atividades, respostas anteriores, detalhes de oportunidade
- **int-evo-crm** (tickets): resoluções anteriores, problemas conhecidos, workarounds
- Notas de reuniões: discussões, decisões, compromissos anteriores

**Tier 3 — Comunicações do Time:**
- **discord-get-messages** (`/discord-get-messages`): buscar o tópico em canais relevantes; verificar se membros do time discutiram ou responderam isso antes
- **int-whatsapp** (`/int-whatsapp`): buscar discussões sobre o tópico em grupos relevantes
- **Gmail MCP**: buscar correspondência anterior sobre esse tópico

**Tier 4 — Fontes Externas:**
- Busca na web: documentação oficial, posts de blog, fóruns da comunidade
- Bases de conhecimento públicas, help centers, release notes
- Documentação de terceiros: parceiros de integração, ferramentas complementares

**Tier 5 — Inferido ou Analógico (usar quando fontes diretas não trazem respostas):**
- Situações similares: como perguntas similares foram tratadas antes
- Clientes análogos: o que funcionou para contas comparáveis
- Boas práticas gerais: padrões e normas da indústria

### 3. Sintetizar Achados

Compilar resultados em um briefing de pesquisa estruturado:

```
## Pesquisa: [Pergunta/Tópico]

### Resposta
[Resposta clara e direta à pergunta — começar com a conclusão]

**Confiança:** [Alta / Média / Baixa]
[Explicar o que determina o nível de confiança]

### Achados Chave

**De [Fonte 1]:**
- [Achado com detalhe específico]
- [Achado com detalhe específico]

**De [Fonte 2]:**
- [Achado com detalhe específico]

### Contexto e Nuances
[Ressalvas, casos extremos, ou contexto adicional que importa]

### Fontes
1. [Nome/link da fonte] — [o que contribuiu]
2. [Nome/link da fonte] — [o que contribuiu]
3. [Nome/link da fonte] — [o que contribuiu]

### Lacunas e Incógnitas
- [O que não pôde ser confirmado]
- [O que pode precisar de verificação por um especialista]

### Próximos Passos Recomendados
- [Ação se a resposta precisa ir para um cliente]
- [Ação se pesquisa adicional é necessária]
- [Quem consultar para verificação se necessário]
```

### 4. Lidar com Fontes Insuficientes

Se nenhuma fonte conectada traz resultados:

- Realizar pesquisa na web sobre o tópico
- Pedir ao usuário por contexto interno:
  - "Não encontrei isso nas fontes conectadas. Você tem docs internos ou artigos da base de conhecimento sobre isso?"
  - "O time discutiu esse tópico antes? Há canais do Discord que eu deveria verificar?"
  - "Há um especialista no assunto que saberia a resposta?"
- Ser transparente sobre as limitações:
  - "Esta resposta é baseada apenas em pesquisa na web — verifique com sua documentação interna antes de compartilhar com o cliente."
  - "Encontrei uma possível resposta mas não pude confirmar de uma fonte interna autorizada."

### 5. Considerações para o Cliente

Se a pesquisa é para responder uma pergunta do cliente:

- Sinalizar se a resposta envolve roadmap de produto, preços, legal ou tópicos de segurança que podem precisar de revisão
- Anotar se a resposta difere do que pode ter sido comunicado anteriormente
- Sugerir ressalvas apropriadas para a resposta voltada ao cliente
- Oferecer para redigir a resposta ao cliente: "Quer que eu redija uma resposta para o cliente com base nesses achados?"

### 6. Captura de Conhecimento

Após a pesquisa ser concluída, sugerir capturar o conhecimento:

- "Devo salvar esses achados no Notion para referência futura?"
- "Quer que eu crie uma entrada de FAQ com base nessa pesquisa?"
- "Vale documentar isso — devo redigir uma entrada de runbook?"

Isso ajuda a construir conhecimento institucional e reduz esforço de pesquisa duplicada na equipe.

---

## Priorização de Fontes e Confiança

### Confiança por Tier de Fonte

| Tier | Tipo de Fonte | Confiança | Notas |
|------|-------------|------------|-------|
| 1 | Docs internos oficiais, KB, políticas | **Alta** | Confiar exceto se claramente desatualizado — verificar datas |
| 2 | int-evo-crm, tickets, notas de reuniões | **Média-Alta** | Pode ser subjetivo ou incompleto |
| 3 | Discord, WhatsApp, Gmail | **Média** | Informal, pode estar fora de contexto ou ser especulativo |
| 4 | Web, fóruns, docs de terceiros | **Baixa-Média** | Pode não refletir sua situação específica |
| 5 | Inferência, analogias, boas práticas | **Baixa** | Sinalizar claramente como inferência, não fato |

### Níveis de Confiança

Sempre atribuir e comunicar um nível de confiança:

**Alta Confiança:**
- Resposta confirmada por documentação oficial ou fonte autorizada
- Múltiplas fontes corroboram a mesma resposta
- Informação está atual (verificada em prazo razoável)
- "Estou confiante que isso é preciso com base em [fonte]."

**Média Confiança:**
- Resposta encontrada em fontes informais (chat, email) mas não em docs oficiais
- Fonte única sem corroboração
- Informação pode estar ligeiramente desatualizada mas provavelmente ainda é válida
- "Com base em [fonte], parece ser esse o caso, mas recomendo confirmar com [time/pessoa]."

**Baixa Confiança:**
- Resposta é inferida a partir de informações relacionadas
- Fontes estão desatualizadas ou potencialmente não confiáveis
- Informações contraditórias encontradas em fontes
- "Não consegui encontrar uma resposta definitiva. Com base em [contexto], minha melhor avaliação é [resposta], mas isso deve ser verificado antes de compartilhar com o cliente."

**Incapaz de Determinar:**
- Nenhuma informação relevante encontrada em nenhuma fonte
- Pergunta requer conhecimento especializado não disponível nas fontes
- "Não encontrei informações sobre isso. Recomendo entrar em contato com [especialista/time sugerido] para uma resposta definitiva."

### Lidando com Contradições

Quando as fontes discordam:
1. Anotar a contradição explicitamente
2. Identificar qual fonte é mais autorizada ou mais recente
3. Apresentar ambas as perspectivas com contexto
4. Recomendar como resolver a discrepância
5. Se for para um cliente: usar a resposta mais conservadora/cautelosa até resolver

## Quando Escalar vs. Responder Diretamente

### Responder Diretamente Quando:
- A documentação oficial aborda claramente a pergunta
- Múltiplas fontes confiáveis corroboram a resposta
- A pergunta é factual e não sensível
- A resposta não envolve compromissos, timelines ou preços
- Perguntas similares foram respondidas antes com precisão confirmada

### Escalar ou Verificar Quando:
- A resposta envolve compromissos de roadmap de produto ou timelines
- Perguntas de preço, termos legais ou específicas de contrato
- Perguntas de segurança, compliance ou tratamento de dados (LGPD, etc.)
- A resposta pode criar precedente ou expectativas
- Foram encontradas informações contraditórias nas fontes
- A pergunta envolve configuração customizada de um cliente específico
- A resposta requer expertise especializada que você não tem
- O cliente está em risco e a resposta errada pode piorar a situação

### Caminho de Escalação:
1. **Especialista no assunto**: Para perguntas técnicas ou específicas de domínio
2. **Time de produto**: Para perguntas de roadmap, feature ou capacidade
3. **Jurídico/compliance**: Para termos, privacidade, segurança ou perguntas regulatórias
4. **Financeiro**: Para perguntas de preço, fatura ou pagamento
5. **Devs**: Para configurações customizadas, bugs ou causas raiz técnicas
6. **Davidson**: Para decisões estratégicas, exceções ou situações de alto risco

## Documentação de Pesquisa para Base de Conhecimento

Após concluir a pesquisa, capturar o conhecimento para uso futuro.

### Quando Documentar:
- A pergunta surgiu antes ou provavelmente surgirá novamente
- A pesquisa exigiu esforço significativo para compilar
- A resposta exigiu síntese de múltiplas fontes
- A resposta corrige um mal-entendido comum
- A resposta envolve nuances fáceis de errar

### Formato de Documentação:
```
## [Pergunta/Tópico]

**Última Verificação:** [data]
**Confiança:** [nível]

### Resposta
[Resposta clara e direta]

### Detalhes
[Detalhe de suporte, contexto e nuances]

### Fontes
[De onde essa informação veio]

### Perguntas Relacionadas
[Outras perguntas que isso pode ajudar a responder]

### Notas de Revisão
[Quando re-verificar, o que pode mudar essa resposta]
```

### Higiene da Base de Conhecimento:
- Datar todos os registros
- Sinalizar registros que referenciam versões ou features específicas do produto
- Revisar e atualizar registros trimestralmente
- Arquivar registros que não são mais relevantes
- Taguear registros para pesquisabilidade (por tópico, área de produto, segmento de cliente)
