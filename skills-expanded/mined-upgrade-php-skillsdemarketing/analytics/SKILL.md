---
name: analytics
description: Quando o usuário quiser configurar, melhorar ou auditar tracking e mensuração de analytics. Use também quando o usuário mencionar "configurar tracking," "GA4," "Google Analytics," "tracking de conversão," "tracking de evento," "parâmetros UTM," "tag manager," "GTM," "implementação de analytics," "plano de tracking," "como eu meço isso," "rastrear conversões," "Mixpanel," "Segment," "meus eventos estão disparando," ou "analytics não está funcionando." Use isso sempre que alguém perguntar como saber se algo está funcionando ou quiser medir resultados de marketing. Para escolher modelos de atribuição, comparar multi-touch/MMM/incrementalidade, ou reconciliar números conflitantes entre ferramentas, veja attribution. Para mensuração de teste A/B, veja ab-testing.
metadata:
  version: 2.0.1
---

# Tracking de Analytics

Você é um especialista em implementação de analytics e mensuração. Seu
objetivo é ajudar a configurar tracking que gera insights acionáveis para
decisões de marketing e produto.

## Avaliação inicial

**Primeiro, verifique se há contexto de produto:**
Se `.agents/product-marketing.md` existir (ou `.claude/product-marketing.md`,
ou o nome de arquivo legado `product-marketing-context.md`, em setups mais
antigos), leia-o antes de fazer perguntas. Use esse contexto e só pergunte o
que não estiver coberto ou for específico desta tarefa.

Antes de implementar o tracking, entenda:

1. **Contexto de negócio** - Que decisões esses dados vão informar? Quais são
   as conversões-chave?
2. **Estado atual** - Que tracking já existe? Que ferramentas estão em uso?
3. **Contexto técnico** - Qual é o stack técnico? Há requisitos de
   privacidade/compliance (no Brasil, a LGPD)?

---

## Princípios centrais

### 1. Rastreie para decisões, não para dados

- Todo evento deve informar uma decisão
- Evite métricas de vaidade
- Qualidade > quantidade de eventos

### 2. Comece pelas perguntas

- O que você precisa saber?
- Que ações você vai tomar com base nesses dados?
- Trabalhe de trás para frente até o que precisa rastrear

### 3. Nomeie as coisas de forma consistente

- Convenções de nomenclatura importam
- Estabeleça padrões antes de implementar
- Documente tudo

### 4. Mantenha a qualidade dos dados

- Valide a implementação
- Monitore problemas
- Dados limpos > mais dados

---

## Framework de plano de tracking

### Estrutura

```text
Nome do evento | Categoria | Propriedades | Gatilho | Notas
-------------- | --------- | ------------ | ------- | -----
```

### Tipos de evento

| Tipo | Exemplos |
|---|---|
| Pageviews | Automático, enriquecido com metadados |
| Ações do usuário | Cliques em botão, envio de formulário, uso de feature |
| Eventos de sistema | Cadastro concluído, compra, mudança de assinatura |
| Conversões customizadas | Conclusão de meta, estágios de funil |

**Para listas completas de evento**: veja
[references/event-library.md](references/event-library.md)

---

## Convenções de nomenclatura de evento

### Formato recomendado: Objeto-Ação

```text
cadastro_concluido
botao_clicado
formulario_enviado
artigo_lido
checkout_pagamento_concluido
```

### Boas práticas

- Minúsculo com underscore
- Seja específico: `cta_hero_clicado` em vez de `botao_clicado`
- Inclua contexto nas propriedades, não no nome do evento
- Evite espaços e caracteres especiais
- Documente as decisões

---

## Eventos essenciais

### Site de marketing

| Evento | Propriedades |
|---|---|
| cta_clicado | texto_botao, localizacao |
| formulario_enviado | tipo_formulario |
| cadastro_concluido | metodo, origem |
| demo_solicitada | - |

### Produto/App

| Evento | Propriedades |
|---|---|
| passo_onboarding_concluido | numero_passo, nome_passo |
| feature_usada | nome_feature |
| compra_concluida | plano, valor |
| assinatura_cancelada | motivo |

**Para a biblioteca completa de eventos por tipo de negócio**: veja
[references/event-library.md](references/event-library.md)

---

## Propriedades de evento

### Propriedades padrão

| Categoria | Propriedades |
|---|---|
| Página | page_title, page_location, page_referrer |
| Usuário | user_id, user_type, account_id, plan_type |
| Campanha | source, medium, campaign, content, term |
| Produto | product_id, product_name, category, price |

### Boas práticas

- Use nomes de propriedade consistentes
- Inclua contexto relevante
- Não duplique propriedades automáticas
- Evite PII (dados pessoais) nas propriedades — no Brasil, isso é regido
  pela LGPD

---

## Implementação do GA4

### Setup rápido

1. Crie a propriedade GA4 e o data stream
2. Instale o gtag.js ou o GTM
3. Ative a mensuração otimizada
4. Configure eventos customizados
5. Marque as conversões no Admin

### Exemplo de evento customizado

```javascript
gtag('event', 'cadastro_concluido', {
  'method': 'email',
  'plan': 'free'
});
```

**Para implementação detalhada do GA4**: veja
[references/ga4-implementation.md](references/ga4-implementation.md)

---

## Google Tag Manager

### Estrutura do container

| Componente | Propósito |
|---|---|
| Tags | Código que executa (GA4, pixels) |
| Gatilhos (Triggers) | Quando as tags disparam (pageview, clique) |
| Variáveis | Valores dinâmicos (texto do clique, data layer) |

### Padrão de data layer

```javascript
dataLayer.push({
  'event': 'formulario_enviado',
  'form_name': 'contato',
  'form_location': 'rodape'
});
```

**Para implementação detalhada do GTM**: veja
[references/gtm-implementation.md](references/gtm-implementation.md)

---

## Estratégia de parâmetros UTM

### Parâmetros padrão

| Parâmetro | Propósito | Exemplo |
|---|---|---|
| utm_source | Fonte de tráfego | google, newsletter |
| utm_medium | Meio de marketing | cpc, email, social |
| utm_campaign | Nome da campanha | promocao_verao |
| utm_content | Diferenciar versões | hero_cta |
| utm_term | Palavras-chave de busca paga | tenis+corrida |

### Convenções de nomenclatura

- Tudo minúsculo
- Use underscore ou hífen de forma consistente
- Seja específico mas conciso: `blog_rodape_cta`, não `cta1`
- Documente todas as UTMs em uma planilha

---

## Depuração e validação

### Ferramentas de teste

| Ferramenta | Use para |
|---|---|
| GA4 DebugView | Monitoramento de evento em tempo real |
| GTM Preview Mode | Testar gatilhos antes de publicar |
| Extensões de navegador | Tag Assistant, dataLayer Inspector |

### Checklist de validação

- [ ] Eventos disparando nos gatilhos corretos
- [ ] Valores de propriedade populando corretamente
- [ ] Sem eventos duplicados
- [ ] Funciona em diferentes navegadores e mobile
- [ ] Conversões registradas corretamente
- [ ] Sem vazamento de PII

### Problemas comuns

| Problema | Checar |
|---|---|
| Eventos não disparam | Configuração do gatilho, GTM carregado |
| Valores errados | Caminho da variável, estrutura do data layer |
| Eventos duplicados | Múltiplos containers, gatilho disparando duas vezes |

---

## Privacidade e compliance

### Considerações

- Consentimento de cookies obrigatório na UE/Reino Unido/Canadá — no Brasil,
  a **LGPD** (Lei Geral de Proteção de Dados) exige base legal para coleta e
  tratamento de dados pessoais, e consentimento é a base mais comum em
  analytics de marketing
- Sem PII nas propriedades de analytics
- Configurações de retenção de dados
- Capacidade de exclusão de dados do usuário

### Implementação

- Use consent mode (aguarde o consentimento)
- Anonimização de IP
- Colete só o que você precisa
- Integre com uma plataforma de gestão de consentimento

---

## Formato de saída

### Documento de plano de tracking

```markdown
# Plano de Tracking [Site/Produto]

## Visão geral
- Ferramentas: GA4, GTM
- Última atualização: [Data]

## Eventos

| Nome do evento | Descrição | Propriedades | Gatilho |
|---|---|---|---|
| cadastro_concluido | Usuário completa o cadastro | metodo, plano | Página de sucesso |

## Dimensões customizadas

| Nome | Escopo | Parâmetro |
|---|---|---|
| tipo_usuario | Usuário | user_type |

## Conversões

| Conversão | Evento | Contagem |
|---|---|---|
| Cadastro | cadastro_concluido | Uma vez por sessão |
```

---

## Perguntas específicas da tarefa

1. Que ferramentas você usa (GA4, Mixpanel, etc.)?
2. Que ações-chave você quer rastrear?
3. Que decisões esses dados vão informar?
4. Quem implementa — time de dev ou marketing?
5. Há requisitos de privacidade/consentimento (LGPD)?
6. O que já é rastreado hoje?

---

## Integrações de ferramentas

Para implementação, veja o [registro de ferramentas](../../tools/REGISTRY.md).
Principais ferramentas de analytics:

| Ferramenta | Melhor para | MCP | Guia |
|---|---|:---:|---|
| **GA4** | Web analytics, ecossistema Google | ✓ | [ga4.md](../../tools/integrations/ga4.md) |
| **Mixpanel** | Analytics de produto, tracking de evento | - | [mixpanel.md](../../tools/integrations/mixpanel.md) |
| **Amplitude** | Analytics de produto, análise de coorte | - | [amplitude.md](../../tools/integrations/amplitude.md) |
| **PostHog** | Analytics open-source, session replay | - | [posthog.md](../../tools/integrations/posthog.md) |
| **Segment** | Plataforma de dados de cliente, roteamento | - | [segment.md](../../tools/integrations/segment.md) |

---

## Skills relacionadas

- **ab-testing**: para tracking de experimento
- **attribution**: para modelos de atribuição, multi-touch/MMM/incrementalidade, e reconciliar números conflitantes entre ferramentas (depois que o tracking estiver ativo)
- **seo-audit**: para análise de tráfego orgânico
- **cro**: para otimização de conversão (usa esses dados)
- **revops**: para métricas de pipeline, tracking de CRM e atribuição de receita
