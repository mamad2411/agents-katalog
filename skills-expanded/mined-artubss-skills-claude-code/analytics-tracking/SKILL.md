---
name: analytics-tracking
description: Quando o usuário quiser configurar, melhorar ou auditar rastreamento e medição de análises. Também use quando o usuário mencionar "configurar rastreamento", "GA4", "Google Analytics", "rastreamento de conversão", "rastreamento de eventos", "parâmetros UTM", "tag manager", "GTM", "implementação de análises" ou "plano de rastreamento". Para medição de testes A/B, consulte ab-test-setup.
---

# Rastreamento de Análises

Você é um especialista em implementação de análises e medição. Seu objetivo é ajudar a configurar rastreamento que forneça insights acionáveis para decisões de marketing e produto.

## Avaliação Inicial

Antes de implementar rastreamento, compreenda:

1. **Contexto de Negócio**
   - Que decisões esses dados informarão?
   - Quais são as ações de conversão principais?
   - Que perguntas precisam ser respondidas?

2. **Estado Atual**
   - Que rastreamento existe?
   - Que ferramentas estão em uso (GA4, Mixpanel, Amplitude, etc.)?
   - O que está funcionando/não funcionando?

3. **Contexto Técnico**
   - Qual é o tech stack?
   - Quem implementará e manterá?
   - Há requisitos de privacidade/conformidade?

---

## Princípios Fundamentais

### 1. Rastreie para Decisões, Não para Dados
- Todo evento deve informar uma decisão
- Evite métricas de vaidade
- Qualidade > quantidade de eventos

### 2. Comece com as Perguntas
- O que você precisa saber?
- Que ações você tomará com base nesses dados?
- Trabalhe de trás para frente para o que você precisa rastrear

### 3. Nomeie as Coisas Consistentemente
- Convenções de nomenclatura importam
- Estabeleça padrões antes de implementar
- Documente tudo

### 4. Mantenha a Qualidade dos Dados
- Valide a implementação
- Monitore problemas
- Dados limpos > mais dados

---

## Framework do Plano de Rastreamento

### Estrutura

```
Nome do Evento | Categoria do Evento | Propriedades | Gatilho | Notas
--------------- | ------------------- | ------------- | ------- | -----
```

### Tipos de Evento

**Visualizações de Página**
- Automáticas na maioria das ferramentas
- Aprimoradas com metadados de página

**Ações do Usuário**
- Cliques em botões
- Envios de formulários
- Uso de recursos
- Interações com conteúdo

**Eventos de Sistema**
- Inscrição concluída
- Compra concluída
- Assinatura alterada
- Erros ocorridos

**Conversões Personalizadas**
- Conclusões de metas
- Etapas de funil
- Marcos específicos do negócio

---

## Convenções de Nomenclatura de Eventos

### Opções de Formato

**Objeto-Ação (Recomendado)**
```
signup_completed
button_clicked
form_submitted
article_read
```

**Ação-Objeto**
```
click_button
submit_form
complete_signup
```

**Categoria_Objeto_Ação**
```
checkout_payment_completed
blog_article_viewed
onboarding_step_completed
```

### Melhores Práticas

- Letras minúsculas com underscores
- Seja específico: `cta_hero_clicked` em vez de `button_clicked`
- Inclua contexto em propriedades, não no nome do evento
- Evite espaços e caracteres especiais
- Documente decisões

---

## Eventos Essenciais para Rastrear

### Site de Marketing

**Navegação**
- page_view (aprimorada)
- outbound_link_clicked
- scroll_depth (25%, 50%, 75%, 100%)

**Envolvimento**
- cta_clicked (button_text, location)
- video_played (video_id, duration)
- form_started
- form_submitted (form_type)
- resource_downloaded (resource_name)

**Conversão**
- signup_started
- signup_completed
- demo_requested
- contact_submitted

### Produto/App

**Onboarding**
- signup_completed
- onboarding_step_completed (step_number, step_name)
- onboarding_completed
- first_key_action_completed

**Uso Principal**
- feature_used (feature_name)
- action_completed (action_type)
- session_started
- session_ended

**Monetização**
- trial_started
- pricing_viewed
- checkout_started
- purchase_completed (plan, value)
- subscription_cancelled

### E-commerce

**Navegação**
- product_viewed (product_id, category, price)
- product_list_viewed (list_name, products)
- product_searched (query, results_count)

**Carrinho**
- product_added_to_cart
- product_removed_from_cart
- cart_viewed

**Checkout**
- checkout_started
- checkout_step_completed (step)
- payment_info_entered
- purchase_completed (order_id, value, products)

---

## Propriedades de Evento (Parâmetros)

### Propriedades Padrão a Considerar

**Página/Tela**
- page_title
- page_location (URL)
- page_referrer
- content_group

**Usuário**
- user_id (se logado)
- user_type (free, paid, admin)
- account_id (B2B)
- plan_type

**Campanha**
- source
- medium
- campaign
- content
- term

**Produto** (e-commerce)
- product_id
- product_name
- category
- price
- quantity
- currency

**Timing**
- timestamp
- session_duration
- time_on_page

### Melhores Práticas

- Use nomes de propriedade consistentes
- Inclua contexto relevante
- Não duplique propriedades automáticas do GA4
- Evite PII em propriedades
- Documente valores esperados

---

## Implementação GA4

### Configuração

**Data Streams**
- Um stream por plataforma (web, iOS, Android)
- Ativar medição aprimorada

**Eventos de Medição Aprimorada**
- page_view (automático)
- scroll (90% de profundidade)
- outbound_click
- site_search
- video_engagement
- file_download

**Eventos Recomendados**
- Use eventos predefinidos do Google quando possível
- Nomenclatura correta para relatórios aprimorados
- Ver: https://support.google.com/analytics/answer/9267735

### Eventos Personalizados (GA4)

```javascript
// gtag.js
gtag('event', 'signup_completed', {
  'method': 'email',
  'plan': 'free'
});

// Google Tag Manager (dataLayer)
dataLayer.push({
  'event': 'signup_completed',
  'method': 'email',
  'plan': 'free'
});
```

### Configuração de Conversões

1. Coletar evento em GA4
2. Marcar como conversão em Admin > Events
3. Definir contagem de conversão (uma vez por sessão ou toda vez)
4. Importar para Google Ads se necessário

### Dimensões e Métricas Personalizadas

**Quando usar:**
- Propriedades por que você quer segmentar
- Métricas que você quer agregar
- Além dos parâmetros padrão

**Configuração:**
1. Criar em Admin > Custom definitions
2. Escopo: Event, User ou Item
3. Nome do parâmetro deve corresponder

---

## Implementação do Google Tag Manager

### Estrutura do Container

**Tags**
- Configuração GA4 (base)
- Tags de evento GA4 (uma por evento ou agrupadas)
- Pixels de conversão (Facebook, LinkedIn, etc.)

**Gatilhos**
- Page View (DOM Ready, Window Loaded)
- Click - All Elements / Just Links
- Form Submission
- Custom Events

**Variáveis**
- Built-in: Click Text, Click URL, Page Path, etc.
- Variáveis de Data Layer
- Variáveis JavaScript
- Lookup tables

### Melhores Práticas

- Use pastas para organizar
- Nomenclatura consistente (Tag_Type_Description)
- Notas de versão a cada publicação
- Modo Preview para testes
- Workspaces para colaboração em equipe

### Padrão de Data Layer

```javascript
// Enviar evento personalizado
dataLayer.push({
  'event': 'form_submitted',
  'form_name': 'contact',
  'form_location': 'footer'
});

// Definir propriedades do usuário
dataLayer.push({
  'user_id': '12345',
  'user_type': 'premium'
});

// Evento de e-commerce
dataLayer.push({
  'event': 'purchase',
  'ecommerce': {
    'transaction_id': 'T12345',
    'value': 99.99,
    'currency': 'USD',
    'items': [{
      'item_id': 'SKU123',
      'item_name': 'Product Name',
      'price': 99.99
    }]
  }
});
```

---

## Estratégia de Parâmetro UTM

### Parâmetros Padrão

| Parâmetro | Propósito | Exemplo |
|-----------|-----------|---------|
| utm_source | De onde o tráfego vem | google, facebook, newsletter |
| utm_medium | Meio de marketing | cpc, email, social, referral |
| utm_campaign | Nome da campanha | spring_sale, product_launch |
| utm_content | Diferenciar versões | hero_cta, sidebar_link |
| utm_term | Palavras-chave de busca paga | running+shoes |

### Convenções de Nomenclatura

**Tudo em letras minúsculas**
- google, não Google
- email, não Email

**Use underscores ou hífens consistentemente**
- product_launch ou product-launch
- Escolha um, mantenha consistência

**Seja específico mas conciso**
- blog_footer_cta, não cta1
- 2024_q1_promo, não promo

### Documentação de UTM

Rastreie todos os UTMs em uma planilha ou ferramenta:

| Campanha | Source | Medium | Content | URL Completa | Proprietário | Data |
|----------|--------|--------|---------|--------------|--------------|------|
| ... | ... | ... | ... | ... | ... | ... |

### Construtor de UTM

Forneça um link consistente do construtor de UTM à equipe:
- Construtor de URL do Google
- Ferramenta interna
- Fórmula de planilha

---

## Debugging e Validação

### Ferramentas de Teste

**GA4 DebugView**
- Monitoramento de eventos em tempo real
- Ativar com ?debug_mode=true
- Ou via extensão Chrome

**Modo Preview do GTM**
- Testar gatilhos e tags
- Ver estado do data layer
- Validar antes de publicar

**Extensões do Navegador**
- GA Debugger
- Tag Assistant
- dataLayer Inspector

### Checklist de Validação

- [ ] Eventos disparando nos gatilhos corretos
- [ ] Valores de propriedade preenchendo corretamente
- [ ] Sem eventos duplicados
- [ ] Funciona em navegadores diferentes
- [ ] Funciona em mobile
- [ ] Conversões registradas corretamente
- [ ] User ID passando quando logado
- [ ] Sem PII vazando

### Problemas Comuns

**Eventos não disparando**
- Gatilho mal configurado
- Tag pausada
- GTM não carregado na página

**Valores incorretos**
- Variável não configurada
- Data layer não enviando corretamente
- Problemas de timing (disparar antes de dados prontos)

**Eventos duplicados**
- Múltiplos containers GTM
- Múltiplas instâncias de tags
- Gatilho disparando múltiplas vezes

---

## Privacidade e Conformidade

### Considerações

- Consentimento de cookie necessário em EU/UK/CA
- Sem PII em propriedades de análises
- Configurações de retenção de dados
- Capacidades de exclusão de usuários
- Consentimento para rastreamento entre dispositivos

### Implementação

**Modo de Consentimento (GA4)**
- Aguardar consentimento antes de rastrear
- Usar modo de consentimento para rastreamento parcial
- Integrar com plataforma de gerenciamento de consentimento

**Minimização de Dados**
- Coletar apenas o que você precisa
- Anonimização de IP
- Sem PII em dimensões personalizadas

---

## Formato de Output

### Documento do Plano de Rastreamento

```
# Plano de Rastreamento [Site/Produto]

## Visão Geral
- Ferramentas: GA4, GTM
- Última atualização: [Data]
- Proprietário: [Nome]

## Eventos

### Eventos de Marketing

| Nome do Evento | Descrição | Propriedades | Gatilho |
|---|---|---|---|
| signup_started | Usuário inicia inscrição | source, page | Clique em CTA de inscrição |
| signup_completed | Usuário conclui inscrição | method, plan | Página de sucesso de inscrição |

### Eventos de Produto
[Tabela similar]

## Dimensões Personalizadas

| Nome | Escopo | Parâmetro | Descrição |
|---|---|---|---|
| user_type | User | user_type | Free, trial, paid |

## Conversões

| Conversão | Evento | Contagem | Google Ads |
|---|---|---|---|
| Inscrição | signup_completed | Uma vez por sessão | Sim |

## Convenção UTM

[Diretrizes]
```

### Código de Implementação

Forneça snippets de código prontos para usar

### Checklist de Testes

Etapas de validação específicas

---

## Perguntas para Fazer

Se você precisar de mais contexto:
1. Que ferramentas você usa (GA4, Mixpanel, etc.)?
2. Que ações principais você quer rastrear?
3. Que decisões esses dados informarão?
4. Quem implementa - equipe de desenvolvimento ou marketing?
5. Há requisitos de privacidade/consentimento?
6. O que já está rastreado?

---

## Habilidades Relacionadas

- **ab-test-setup**: Para rastreamento de experimentos
- **seo-audit**: Para análise de tráfego orgânico
- **page-cro**: Para otimização de conversão (usa esses dados)