---
name: marketing-demand-acquisition
description: Geração de demanda multi-canal, otimização de mídia paga, estratégia de SEO e programas de parcerias para startups Series A+. Inclui calculadora de CAC, playbooks de canal, integração com HubSpot e táticas de expansão internacional. Use ao planejar campanhas de geração de demanda, otimizar mídia paga, construir estratégias de SEO, estabelecer parcerias, ou quando o usuário menciona demand gen, anúncios pagos, LinkedIn ads, Google ads, CAC, aquisição, geração de leads ou pipeline.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: demand-generation
  updated: 2025-10-20
  python-tools: calculate_cac.py
  tech-stack: HubSpot, LinkedIn-Ads, Google-Ads, Meta-Ads, SEO-tools
  target-market: B2B-SaaS, Series-A+
---

# Marketing Demand & Acquisition

Playbook especializado em aquisição para startups Series A+ escalando internacionalmente (EU/US/Canadá) com modelo híbrido PLG/Sales-Led.

## Palavras-chave
geração de demanda, mídia paga, anúncios pagos, LinkedIn ads, Google ads, Meta ads, CAC, custo de aquisição de clientes, geração de leads, MQL, SQL, geração de pipeline, estratégia de aquisição, marketing de performance, paid social, paid search, parcerias, marketing de afiliados, estratégia de SEO, campanhas HubSpot, marketing automation, B2B marketing, SaaS marketing

## Cobertura de Funções

Esta competência atende:
- **Demand Generation Manager** - Campanhas multi-canal, geração de pipeline
- **Paid Media/Performance Marketer** - Otimização de paid search/social/display
- **SEO Manager** - Aquisição orgânica e SEO técnico
- **Affiliate/Partnerships Manager** - Co-marketing e parcerias de canal

## KPIs Principais por Função

**Demand Gen**: Volume de MQL/SQL, custo por oportunidade, pipeline gerado por marketing $, velocidade de pipeline, taxa de conversão MQL→SQL

**Paid Media**: CAC, ROAS, CPL, CPA, lift incremental, taxa de eficiência de canal

**SEO**: Sessões orgânicas, % tráfego não-branded, rankings de palavras-chave (P1-P3), conversões assistidas por orgânico, score de saúde técnica

**Partnerships**: Pipeline gerado por parceiro $, CAC de parceiro, novos logos via parceiros, ROI de co-marketing

## Integração de Tech Stack

**HubSpot CRM** - Rastreamento de campanhas, lead scoring, atribuição, workflows
**Google Analytics** - Análise de tráfego, rastreamento de conversão, otimização de funil
**Search Console** - Performance de palavras-chave, problemas técnicos, indexação
**LinkedIn Campaign Manager** - Paid social B2B
**Google Ads** - Search, Display, YouTube
**Meta Ads** - Facebook, Instagram

---

## 1. Framework de Geração de Demanda

### 1.1 Estratégia Full-Funnel (Melhores Práticas 2025)

**TOFU (Awareness)** → **MOFU (Consideration)** → **BOFU (Decision)** → **Handoff para Sales/Product**

#### Táticas TOFU
- Paid social (LinkedIn thought leadership, Meta awareness)
- Display advertising (programática, retargeting)
- Content syndication
- SEO (palavras-chave informacionais)
- Parcerias (co-webinars, guest content)
- Target: Brand lift, tráfego do site, engajamento inicial

#### Táticas MOFU
- Paid search (solution keywords)
- Campanhas de retargeting
- Conteúdo gated (eBooks, templates, webinars)
- Sequências de email nurture
- Comparison pages (SEO)
- Target: MQLs, demo requests, trial signups

#### Táticas BOFU
- Paid search (brand + competitor keywords)
- Campanhas de direct outreach
- Free trial CTAs
- Case studies & ROI calculators
- Intent-based retargeting
- Target: SQLs, demos agendados, pipeline $

### 1.2 Template de Planejamento de Campanha

**Campaign Brief** (use para cada campanha):

```
Campaign Name: [Q2-2025-LinkedIn-ABM-Enterprise]
Objective: [Gerar 50 SQLs de contas Enterprise ($50k+ ACV)]
Budget: [$15k/month]
Duration: [90 days]
Channels: [LinkedIn Ads, Retargeting, Email]
Audience: [Director+ em empresas SaaS, 500-5000 funcionários, EU/US]
Offer: [Relatório de Benchmark Gated]
Success Metrics:
  - Primary: 50 SQLs, <$300 CPO
  - Secondary: 500 MQLs, 10% taxa MQL→SQL, 40% email open rate
HubSpot Setup:
  - Campaign ID: [create in HubSpot]
  - Lead scoring: +20 para download, +30 para demo request
  - Attribution: First-touch + Multi-touch
Handoff Protocol:
  - Critério SQL: Title + Company size + Budget confirmado
  - Routing: Enterprise SDR team via HubSpot workflow
  - SLA: 4-hour response time
```

### 1.3 Configuração de Rastreamento de Campanha HubSpot

**Passo-a-passo**:

1. **Criar Campanha em HubSpot**
   - Marketing → Campaigns → Create Campaign
   - Name: `Q2-2025-LinkedIn-ABM-Enterprise`
   - Tag todos os assets (landing pages, emails, ads) com campaign ID

2. **Estrutura de Parâmetros UTM** (crítico para atribuição)
   ```
   utm_source={channel}       // linkedin, google, facebook
   utm_medium={type}          // cpc, display, email, organic
   utm_campaign={campaign-id} // q2-2025-linkedin-abm-enterprise
   utm_content={variant}      // ad-variant-a, email-1
   utm_term={keyword}         // [for paid search only]
   ```

3. **Configuração de Lead Scoring**
   - Navigate to: Settings → Marketing → Lead Scoring
   - Campaign engagement: +10-30 pontos baseado na profundidade de ação
   - Channel quality: LinkedIn +5, Google Search +10, Organic +15

4. **Relatórios de Atribuição**
   - Use atribuição multi-touch do HubSpot (W-shaped para motion híbrido)
   - First-touch: Crédito de awareness
   - Multi-touch: Crédito de jornada completa
   - Build custom report: Marketing → Reports → Attribution

### 1.4 Considerações de Expansão Internacional

**Entrada no Mercado EU**:
- Conformidade GDPR: Double opt-in para email, consentimento explícito rastreado em HubSpot
- Localização: Traduzir landing pages, ads, emails (prioridade: DE, FR, ES)
- Pagamento: Exibir preços em EUR
- Parcerias: Parceiros locais de co-marketing para credibilidade
- Canais pagos: LinkedIn mais eficaz para B2B EU, Google Ads em segundo

**Entrada no Mercado US/Canada**:
- Mensagem: Direto, focado em ROI, menos formal que EU
- Canais pagos: Google Ads + LinkedIn com prioridade igual
- Parcerias: Associações de indústria, sites de review (G2, Capterra)
- Conteúdo: Case studies com impacto $, não apenas features
- Sales alignment: Ciclos de vendas mais rápidos, need immediate lead follow-up

**Alocação de Budget** (Series A recomendado):
- EU: 40% LinkedIn, 25% Google, 20% SEO, 15% Partnerships
- US/CA: 35% Google, 30% LinkedIn, 20% SEO, 15% Partnerships

---

## 2. Otimização de Mídia Paga

### 2.1 Matriz de Estratégia de Canal

| Canal | Melhor Para | CAC Benchmark | Conversion Rate | Series A Priority |
|-------|-------------|---------------|-----------------|-------------------|
| **LinkedIn Ads** | B2B, Enterprise, ABM | $150-$400 | 0.5-2% | ⭐⭐⭐⭐⭐ |
| **Google Search** | High-intent, BOFU | $80-$250 | 2-5% | ⭐⭐⭐⭐⭐ |
| **Google Display** | Retargeting, awareness | $50-$150 | 0.3-1% | ⭐⭐⭐ |
| **Meta (FB/IG)** | SMB, consumer-like products | $60-$200 | 1-3% | ⭐⭐⭐ |
| **YouTube** | Product demos, brand | $100-$300 | 0.5-1.5% | ⭐⭐ |
| **Reddit/Twitter** | Technical audiences | $40-$180 | 0.5-2% | ⭐⭐ |

### 2.2 Playbook LinkedIn Ads (Primary B2B Channel)

**Estrutura de Campanha**:
```
Account
└─ Campaign Group: [Q2-2025-Enterprise-ABM]
   ├─ Campaign 1: [Awareness - Thought Leadership]
   │  ├─ Ad Set: [CTO/VP Eng, US, Tech Companies]
   │  └─ Creatives: [3 carousel posts, 2 video ads]
   ├─ Campaign 2: [Consideration - Product Education]
   │  ├─ Ad Set: [Engaged audience, retargeting]
   │  └─ Creatives: [2 lead gen forms, 1 landing page]
   └─ Campaign 3: [Conversion - Demo Requests]
      ├─ Ad Set: [Website visitors, content downloaders]
      └─ Creatives: [Direct demo CTA, case study]
```

**Melhores Práticas de Targeting**:
- **Company Size**: 50-5000 funcionários (sweet spot Series A)
- **Job Titles**: Director+, VP+, C-level (use LinkedIn's precise targeting)
- **Industries**: Software, SaaS, Tech Services
- **Matched Audiences**: Website retargeting (install Insight Tag), uploaded email lists
- **Budget**: Comece $50/day por campanha, scale 20% semanalmente se CAC < target

**Frameworks Criativos**:
1. **Thought Leadership** - Industry insights, sem product pitch
2. **Social Proof** - Customer logos, testimonials, case study snippets
3. **Problem-Solution** - Pain point + sua solução em 3 segundos
4. **Demo-First** - Show product immediately, skip fluff

**LinkedIn Lead Gen Forms vs. Landing Pages**:
- **Lead Gen Forms**: Conversão mais alta (2-3x), qualidade menor, use para TOFU/MOFU
- **Landing Pages**: Conversão menor, qualidade maior, use para BOFU/demo requests
- **HubSpot Sync**: Conecte LinkedIn Lead Gen Forms via integração nativa

### 2.3 Playbook Google Ads (Captura de High-Intent)

**Prioridade de Tipos de Campanha**:
1. **Search - Brand** (highest priority, protect brand terms)
2. **Search - Competitor** (steal market share)
3. **Search - Solution** (problem-aware buyers)
4. **Search - Product Category** (earlier stage)
5. **Display - Retargeting** (re-engage warm traffic)

**Estrutura de Campanha Search**:
```
Campaign: [Search-Solution-Keywords]
├─ Ad Group: [project management software]
│  ├─ Keywords:
│  │  - "project management software" [Phrase]
│  │  - "best project management tool" [Phrase]
│  │  - +project +management +solution [Broad Match Modifier]
│  └─ Ads: [3 responsive search ads com 15 headlines, 4 descriptions]
│
├─ Ad Group: [team collaboration tools]
   ├─ Keywords: [5-10 tightly themed keywords]
   └─ Ads: [3 responsive search ads]
```

**Estratégia de Palavras-chave**:
- **Brand Terms**: Exact match, bid high, protect brand
- **Competitor Terms**: "[Competitor] alternative", "[Competitor] vs [You]"
- **Solution Terms**: "best [category] software", "top [category] tools"
- **Problem Terms**: "how to [solve problem]"
- **Negative Keywords**: Mantenha lista de 100+ (free, cheap, jobs, career, reviews)

**Bid Strategy** (melhores práticas 2025):
- Novas campanhas: Comece Manual CPC para controle
- Depois de 50+ conversões: Mude para Target CPA
- Depois de 100+ conversões: Teste Maximize Conversions com tCPA
- Mercados EU: Bid 15-20% maior para mesma qualidade

**Framework Ad Copy** (Responsive Search Ads):
```
Headlines (15 required):
- H1-3: Value props (Save 10 hours/week, Trusted by 500+ teams)
- H4-6: Features (AI-powered, Real-time sync, Mobile app)
- H7-9: Social proof (4.8★ G2 rating, Used by Microsoft)
- H10-12: CTAs (Start free trial, Book demo, See pricing)
- H13-15: Keywords pinned (Dynamic insertion)

Descriptions (4 required):
- D1: Primary value prop + CTA (30-60 chars)
- D2: Feature list + differentiator (60-90 chars)
- D3: Social proof + urgency (45-90 chars)
- D4: Backup generic (60-90 chars)
```

### 2.4 Playbook Meta Ads (SMB/Lower ACV)

**Quando Usar Meta**:
- ✅ Product ACV <R$50k
- ✅ Produto visual (UI, consumer-facing)
- ✅ Audiência SMB/prosumer
- ✅ Campanhas de broader awareness
- ❌ Enterprise/high ACV (use LinkedIn)

**Configuração de Campanha**:
```
Campaign Objective: [Conversions]
├─ Ad Set 1: [Lookalike - 1% de converters]
│  └─ Placement: [Feed + Stories, Auto]
├─ Ad Set 2: [Interest - Business Software]
│  └─ Placement: [Feed only]
└─ Ad Set 3: [Retargeting - Website 30d]
   └─ Placement: [All placements]
```

**Estratégia de Audiência**:
1. **Core Audiences**: Interests (business tools, productivity, startups)
2. **Lookalike**: 1% de purchasers/high-value leads
3. **Retargeting**: Website visitors últimos 30d, video viewers (75%+)

**Melhores Práticas Criativas**:
- Use video (1:1 ou 9:16 para Stories)
- Primeiros 3 segundos = hook (problem ou result)
- Show product UI em ação
- Add captions (85% assistem muted)
- Test 3-5 creative variants por campanha

### 2.5 Alocação de Budget & Scaling

**Budget Inicial** (Series A, $30k-50k/month total):
```
Canal              Budget    Resultados Esperados
─────────────────────────────────────────────────
LinkedIn Ads       $15k      50 MQLs, 10 SQLs, $1.5k CAC
Google Search      $12k      80 MQLs, 20 SQLs, $600 CAC
Google Display     $5k       120 MQLs, 5 SQLs, $1k CAC
Meta Ads           $5k       100 MQLs, 8 SQLs, $625 CAC
Partnerships       $3k       20 MQLs, 5 SQLs, $600 CAC
─────────────────────────────────────────────────
TOTAL              $40k      370 MQLs, 48 SQLs, $833 CAC avg
```

**Regras de Scaling**:
1. Se CAC <target → Aumentar budget 20% semanalmente
2. Se CAC >target → Pausar, otimizar, relançar
3. Se conversion rate cai >20% → Verificar landing page, offer fatigue
4. Scale winners, kill losers rápido (minimum 2-week test)

**HubSpot ROI Dashboard**:
- Marketing → Reports → Create Custom Report
- Metrics: Spend, Leads, MQLs, SQLs, CAC, ROAS, Pipeline $
- Dimensions: Campaign, Channel, Region
- Frequency: Daily review, weekly optimization

---

## 3. Estratégia de SEO

### 3.1 Fundação de SEO Técnico (Must-Have)

**Checklist Pre-Launch**:
- [ ] XML sitemap submetido a Search Console
- [ ] Robots.txt configurado (allow crawling)
- [ ] HTTPS habilitado (SSL certificate)
- [ ] Page speed >90 mobile (Google PageSpeed Insights)
- [ ] Core Web Vitals passando (LCP, FID, CLS)
- [ ] Structured data (Organization, Product, FAQ schema)
- [ ] Canonical tags em todas as páginas
- [ ] Hreflang tags para internacional (en-US, en-GB, de-DE, etc.)

**Auditoria Técnica** (trimestral):
```
1. Rastrear site com Screaming Frog
2. Verificar:
   - 404 errors (fix ou redirect)
   - Redirect chains (consolidate)
   - Duplicate content (canonicalize)
   - Missing meta descriptions
   - Slow pages (>3s load time)
   - Mobile usability issues
3. Corrigir issues em ordem de prioridade: Critical → High → Medium
```

### 3.2 Framework de Estratégia de Palavras-chave

**Processo de Pesquisa de Palavras-chave**:
1. **Seed Keywords** - Sua categoria de produto (ex: "software de gestão de projetos")
2. **Use Tools** - Ahrefs, SEMrush, ou free: Google Keyword Planner + Search Console
3. **Analyze** - Volume, difficulty, intent, SERP features
4. **Prioritize** - Quick wins (low difficulty, high intent)

**Tiers de Palavras-chave**:

**Tier 1: High-Intent BOFU** (target first)
- "best [product category]"
- "[product category] for [use case]"
- "[competitor] alternative"
- Volume: 100-1k/mo, Difficulty: Medium, Intent: Commercial

**Tier 2: Solution-Aware MOFU**
- "how to [solve problem]"
- "[problem] solution"
- "[use case] tools"
- Volume: 500-5k/mo, Difficulty: Medium-High, Intent: Informational-Commercial

**Tier 3: Problem-Aware TOFU**
- "what is [concept]"
- "[problem] examples"
- "[industry] challenges"
- Volume: 1k-10k/mo, Difficulty: High, Intent: Informational

**Pesquisa de Palavras-chave Internacional**:
- Use Ahrefs/SEMrush com language filters
- Traduza palavras-chave, não apenas localize (nuances culturais importam)
- EU: Maior confiança em conteúdo localizado (domain.de > domain.com/de)
- UK: Use British spelling (optimise vs. optimize)

### 3.3 Template On-Page SEO

**Checklist de Otimização de Página**:
```
URL: [/best-project-management-software]
Title Tag (60 chars): [Best Project Management Software 2025 | YourBrand]
Meta Description (155 chars): [Compare top 10 PM tools. Features, pricing, reviews. Find the perfect fit for your team. Free trials available.]

H1 (60 chars): [Best Project Management Software in 2025]
H2s (structure):
  - What is Project Management Software?
  - Top 10 PM Tools Compared
  - Key Features to Look For
  - Pricing & Plans
  - How to Choose
  - FAQ

Content:
  - Length: 2000-3000 words (comprehensive)
  - Keyword density: 1-2% (natural)
  - Internal links: 3-5 páginas relevantes
  - External links: 2-3 fontes autorizadas
  - Images: 3-5 com alt text
  - Schema: Product, FAQ, HowTo

CTA:
  - Above fold: [Start Free Trial]
  - Mid-content: [Compare Plans]
  - End: [Book Demo]
```

**Cronograma de Content Refresh**:
- Páginas Tier 1: Atualizar trimestralmente (rankings, pricing, features)
- Páginas Tier 2: Atualizar semestralmente
- Páginas Tier 3: Atualizar anualmente
- Todas as páginas: Monitorar Search Console para ranking drops, refresh imediatamente

### 3.4 Estratégia de Link Building (Melhores Práticas 2025)

**Táticas de Aquisição de Links** (em ordem de prioridade):

**1. Digital PR** (highest ROI)
- Publicar pesquisa/dados originais
- Criar relatórios de indústria
- Pitch jornalistas (use HARO, Terkel, Featured)
- Target: Industry blogs, tech publications

**2. Guest Posting** (quality over quantity)
- Target: Domain Authority (DA) 40+ sites
- Avoid: Link farms, PBNs, paid links (Google penalty risk)
- Anchor text: Branded (70%), topical (20%), exact match (10%)

**3. Partnerships & Co-Marketing**
- Parceiro com complementary SaaS tools
- Criar co-branded content
- Trocar homepage links (footer ou partner section)

**4. Community Engagement**
- Responder perguntas em Reddit, Quora
- Participar em industry forums
- Criar tools/calculators → natural backlinks

**5. Broken Link Building**
- Encontrar broken links em competitor sites
- Oferecer seu conteúdo como replacement
- Tools: Ahrefs' Broken Backlinks report

**Link Velocity** (evitar penalties):
- Natural: 5-10 links/month para novos sites
- Aggressive: 20-30 links/month após 6 meses
- Monitorar: Google Search Console para manual actions

### 3.5 Estratégia de Conteúdo para SEO

**Tipos de Conteúdo por Estágio do Funil**:

**TOFU (Awareness)**:
- Blog posts: "Ultimate Guide to [Topic]"
- Listicles: "Top 10 [Category]"
- Industry reports: "[Industry] State of 2025"
- Target: Broad keywords, thought leadership

**MOFU (Consideration)**:
- Comparison pages: "[Your Product] vs [Competitor]"
- Best of lists: "Best [Category] for [Use Case]"
- How-to guides: "How to [Solve Problem] with [Product]"
- Target: Solution keywords, product education

**BOFU (Decision)**:
- Product pages: "[Product] Features & Pricing"
- Case studies: "How [Customer] Achieved [Result]"
- Landing pages: "Start Free Trial"
- Target: Brand keywords, high-intent searches

**Content Calendar** (Series A minimum):
- TOFU: 4 posts/month (1 per week)
- MOFU: 2 posts/month
- BOFU: 1 post/month
- Refresh: 2 existing posts/month

### 3.6 Local SEO (Para Regional Offices)

**Google Business Profile Setup** (por localização):
- Complete all fields: Name, address, phone, hours, category
- Upload photos: Office, team, product (10+ images)
- Coletar reviews: Ask customers, automate via HubSpot workflow
- Post updates: Weekly posts sobre company news, events

**Local Citations** (US/Canada/EU):
- Submit to: Yelp, Yellow Pages, local directories
- NAP consistency: Name, Address, Phone idêntico everywhere
- Industry directories: Software review sites (G2, Capterra)

---

## 4. Partnerships & Programas de Afiliados

### 4.1 Tipos de Partnership & Estratégia

**Tiers de Partnership**:

**Tier 1: Strategic Partnerships** (high impact, low volume)
- Target: Complementary SaaS tools com overlapping ICPs
- Structure: Co-marketing, product integrations, revenue share
- Examples: Slack ↔ Asana, Shopify ↔ Klaviyo
- Effort: High (6-12 months para estabelecer)
- ROI: Muito alto (100+ leads/month após ramp)

**Tier 2: Affiliate Partners** (escalável)
- Target: Bloggers, review sites, industry influencers
- Structure: Commission per sale (10-30% primeiro ano)
- Platform: Use PartnerStack, Impact, ou Rewardful
- Effort: Medium (setup once, ongoing management)
- ROI: Medium-High (depends on partner quality)

**Tier 3: Referral Partners** (customer-driven)
- Target: Seus clientes existentes
- Structure: Referral bonus ($500-$1k per SQL)
- Platform: Built into HubSpot ou standalone (Friendbuy)
- Effort: Low (automate via workflows)
- ROI: Medium (5-10% de clientes referem)

**Tier 4: Marketplace Listings** (distribution)
- Target: Shopify App Store, Salesforce AppExchange, HubSpot Marketplace
- Structure: Free listing + revenue share
- Effort: Medium (initial listing, ongoing updates)
- ROI: Low-Medium (brand visibility + discovery)

### 4.2 Playbook de Partnership

**Step 1: Identificar Partners**
```
Critérios:
- Similar ICP (overlapping audience, no direct competition)
- Product fit (complementary, not substitute)
- Scale (similar company size, funding stage)
- Values alignment (culture, brand positioning)

Pesquisa:
- Tools: BuiltWith, SimilarWeb, LinkedIn Sales Nav
- Look for: Integration pages, partner pages, co-marketing history
```

**Step 2: Template de Outreach**
```
Subject: [YourBrand] ↔ [TheirBrand] Partnership Idea

Hi [Name],

I'm [Your Name] at [YourBrand] - we help [ICP] with [value prop].

I noticed [TheirBrand] serves a similar audience, and I think our customers would benefit from an integration between [YourProduct] and [TheirProduct].

Would you be open to exploring a partnership? I'm thinking:
- Product integration (bi-directional sync)
- Co-marketing (joint webinar, case study)
- Revenue share (referral fees)

Let me know if you'd like to chat. Happy to send more details.

Best,
[Your Name]
```

**Step 3: Partnership Agreement**
- Define scope (integration depth, marketing commitment)
- Revenue model (rev share %, referral fees, co-selling)
- Success metrics (leads, pipeline, revenue)
- Term (12-24 months, com renewal)
- Exit clause (90-day notice)

**Step 4: Activation & Enablement**
- Criar co-branded assets (landing page, webinar deck, one-pager)
- Treinar partner sales team (product demo, pitch deck, objection handling)
- Setup tracking (UTM parameters, partner portal em HubSpot)

**Step 5: Ongoing Management**
- Quarterly business reviews (QBRs)
- Monthly check-ins (pipeline, blockers)
- Co-marketing calendar (1-2 activities/quarter)
- Reporting (HubSpot dashboard para partner-sourced pipeline)

### 4.3 Configuração de Programa de Afiliados

**Seleção de Platform**:
- **PartnerStack** - Melhor para B2B SaaS, native integrations
- **Impact** - Enterprise-grade, high control
- **Rewardful** - Lightweight, Stripe integration
- **FirstPromoter** - Budget-friendly, good analytics

**Estrutura de Comissão** (Series A típico):
```
Tier 1: Influencers/Publishers
- 30% recurring por 12 months
- Ou: $500 flat per SQL
- Bonus: $1k para 10+ referrals/quarter

Tier 2: Bloggers/Content Creators
- 20% recurring por 12 months
- Ou: $300 flat per SQL

Tier 3: Customers (Referral Program)
- $500 per closed deal
- Ou: 1 month free para referrer + referee
```

**Estratégia de Recruitment**:
1. **Outbound**: Encontrar industry bloggers, YouTubers, newsletter writers
2. **Inbound**: "Become an Affiliate" page, promote em product
3. **Events**: Recruitar em conferences, meetups
4. **Communities**: Reddit, LinkedIn groups, Slack communities

**Affiliate Enablement Kit**:
- Brand assets (logos, product screenshots)
- Pre-written content (blog post templates, social posts)
- Tracking links (unique UTM codes per affiliate)
- Sales collateral (one-pagers, case studies, demo videos)

### 4.4 Campanhas de Co-Marketing

**Playbook de Joint Webinar**:
```
Planning (6 weeks antes):
- Define topic (audience pain point, não product pitch)
- Assign roles (host, co-host, Q&A moderator)
- Criar landing page (co-branded, dual logos)
- Design promo assets (social graphics, email templates)

Promotion (4 weeks antes):
- Email: 3 sends (announcement, reminder, last chance)
- Social: 8-10 posts per partner (LinkedIn, Twitter)
- Paid: $2k budget para LinkedIn ads → landing page
- Partners: Cross-promote para cada um's audiences

Execution (day of):
- 60-min format: 5min intro, 40min content, 15min Q&A
- Gravar para on-demand
- Polls/CTAs: Mid-webinar poll, end com demo CTA

Follow-up (1 week depois):
- Send recording a todos os registrants
- Nurture sequence: 3 emails em 2 weeks
- Split leads: Cada partner owns their referred leads
- Report: Attendees, pipeline gerado, next steps
```

**Other Co-Marketing Tactics**:
- **Co-branded Content**: eBook, report, guide
- **Case Study**: Joint customer success story
- **Bundle Offer**: "Buy [YourProduct] + [TheirProduct