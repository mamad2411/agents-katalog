---
name: "seo-analitica"
description: "Skills para otimização de SEO técnico, análise de dados, criação de dashboards e inteligência de negócio para empresas brasileiras. Use quando precisar auditar SEO, configurar GA4, criar relatórios de dados, definir KPIs ou garantir conformidade com LGPD na coleta de dados."
version: 1.0.0
license: MIT
tags:
  - seo
  - analytics
  - dados
  - metricas
  - relatorios
  - bi
  - ga4
  - lgpd-dados
agents:
  - claude-code
  - codex
  - cursor
  - windsurf
  - openclaw
platforms:
  claude-code: "/read /caminho/seo-analitica/SKILL.md"
  cursor: "Cole o conteúdo do SKILL.md no .cursorrules ou .cursor/rules/seo-analitica.md"
  codex: "Inclua no AGENTS.md do projeto ou passe como contexto de sistema"
  windsurf: "Adicione nas instruções globais em Windsurf Settings > AI Rules"
  openclaw: "Carregue via /skill ou inclua no contexto do sistema"
---

# SEO, Analítica & Dados (Nível PODEROSO)

Skills para otimização de SEO técnico, análise de dados, construção de dashboards e inteligência de negócio voltados para o mercado brasileiro. Cobrindo desde a auditoria técnica de um site até a criação de relatórios executivos e conformidade com LGPD na coleta e uso de dados.

Ideal para gestores de marketing digital, analistas de dados, fundadores e profissionais de SEO que precisam transformar dados em decisões de negócio no Brasil.

---

## Início Rápido

### Claude Code
```
/read /caminho/seo-analitica/SKILL.md
> Crie um checklist de auditoria SEO técnica para um e-commerce de moda com 500 páginas de produto no Brasil
```

### Cursor
Adicione ao `.cursor/rules/seo-analitica.md` e use:
```
@seo-analitica Preciso estruturar um relatório mensal de marketing digital com GA4 e Search Console para um cliente de serviços financeiros
```

### Codex
Inclua no `AGENTS.md`:
```
Contexto de SEO e Analytics: use as diretrizes de seo-analitica para tarefas 
que envolvam otimização de busca, análise de dados, dashboards e métricas de negócio.
```

### Windsurf
Em **Settings > AI Rules**, adicione o conteúdo de `SKILL.md` e então:
```
Com base nas skills de seo-analitica, crie uma estratégia de keyword research 
para um blog de finanças pessoais voltado ao público brasileiro classe C/D
```

---

## Visão Geral das Skills

| Skill | Pasta | Foco |
|-------|-------|------|
| SEO Técnico | `seo-tecnico/` | Auditoria: Core Web Vitals, indexação, schema markup |
| Pesquisa de Palavras-Chave | `pesquisa-de-palavras-chave/` | Pesquisa de palavras-chave para busca BR com volume real |
| Google Analytics | `google-analytics/` | Configuração e análise no GA4 com eventos customizados |
| Google Search Console | `google-search-console/` | GSC para diagnóstico e oportunidades de ranking |
| Relatório de Dados | `relatorio-dados/` | Relatórios e dashboards executivos com dados reais |
| BI e Indicadores | `bi-indicadores/` | KPIs e indicadores de negócio para PMEs |
| Rastreamento UTM | `rastreamento-utm/` | Estratégia de UTMs, rastreamento e atribuição |
| Análise de Coortes | `analise-de-coortes/` | Análise de coortes, retenção e LTV de usuários |
| Testes A/B | `testes-ab/` | Planejamento e análise estatística de testes A/B |
| Dados e LGPD | `dados-lgpd/` | Coleta e uso de dados em conformidade com LGPD |

---

## Exemplos de Uso

### SEO Técnico
```
Faça uma auditoria SEO técnica do meu site de SaaS B2B. Os problemas que 
estou vendo: tempo de carregamento acima de 4s no mobile, páginas de produto 
sem meta description, e 200+ imagens sem alt text. Crie um plano de ação 
priorizado com impacto estimado e esforço de implementação.
```

### Keyword Research
```
Crie uma estratégia de keywords para um consultório de psicologia em São Paulo 
que quer atrair clientes via busca orgânica. Foco em: terapia cognitiva, 
ansiedade e depressão. Inclua: volume estimado (BR), intenção de busca, 
dificuldade e sugestão de tipo de conteúdo para cada cluster.
```

### Google Analytics / GA4
```
Configurei o GA4 no meu e-commerce mas só estou rastreando pageviews. 
Liste os 10 eventos customizados mais importantes para e-commerce de moda 
no GA4, com o código de implementação via gtag.js e o que cada evento 
significa para o negócio.
```

### Relatório de Dados
```
Preciso de um template de relatório mensal de marketing digital para apresentar 
para o CEO. Métricas disponíveis: GA4, Meta Ads, Google Ads e Search Console. 
Crie a estrutura do relatório com: resumo executivo, principais KPIs, 
análise de canais, destaques e próximos passos. Formato: apresentação de 8 slides.
```

### BI e Indicadores
```
Tenho uma PME de serviços B2B com 8 funcionários e faturamento mensal de R$ 200k. 
Quais são os 10 KPIs mais importantes que devo monitorar? Para cada um: 
fórmula de cálculo, benchmark do setor de serviços BR e como coletar 
sem um time de dados dedicado.
```

### Dados e LGPD
```
Meu site usa Google Analytics 4, Meta Pixel, cookies de sessão e captura 
e-mails via formulário. Crie um plano de adequação à LGPD com: 
banner de cookies compliant, política de privacidade, registros de 
consentimento e o que posso e não posso fazer com os dados coletados.
```

---

## Contexto Brasileiro

- **LGPD (Lei 13.709/2018)**: toda coleta de dados de usuários brasileiros está sujeita à LGPD — consentimento, finalidade e transparência são obrigatórios; multas chegam a R$ 50M ou 2% do faturamento
- **ANPD**: Autoridade Nacional de Proteção de Dados regula e fiscaliza o cumprimento da LGPD — regulamentações são atualizadas frequentemente
- **Google Analytics no Brasil**: após decisões da UE e impactos no Brasil, sempre orientar sobre coleta de dados de IP e anonimização
- **SEO local BR**: buscas em português BR têm particularidades — "moto" vs "motorcycle", "carro" vs "car"; regionalismo afeta muito as keywords
- **Buscadores**: Google domina >95% do mercado BR de busca; Bing irrelevante; YouTube é o segundo buscador mais usado
- **Velocidade de internet**: internet móvel no Brasil ainda é lenta em regiões fora das capitais — Core Web Vitals devem ser auditados com simulação de rede 3G/4G
- **Mercado de ads BR**: Google Ads e Meta Ads são os principais; TikTok Ads crescendo; CPCs em PT-BR tendem a ser mais baixos que EN-US
- **NF-e e dados fiscais**: empresas BR têm obrigações de armazenamento de dados fiscais que interagem com políticas de retenção de dados pessoais

---

## Configuração de Harness

### Claude Code (CLAUDE.md)
```markdown
## SEO, Analítica & Dados
Ao lidar com tarefas de SEO, analytics e dados:
- Use a skill seo-analitica para estrutura e frameworks
- Sempre mencionar conformidade com LGPD em qualquer estratégia de coleta de dados
- Para SEO: priorizar impacto x esforço, começar pelos quick wins técnicos
- Para relatórios: separar dados de insights — CEO quer insights, não tabelas
```

### Cursor (.cursorrules)
```
# SEO, Analítica & Dados Rules
- Para auditorias SEO: usar checklist técnico + priorização por impacto
- Para GA4: sempre especificar eventos customizados além de pageviews
- Para relatórios: estrutura executiva com resumo + detalhes sob demanda
- Sempre incluir conformidade com LGPD em estratégias de dados
```

### Codex (AGENTS.md)
```markdown
## Agente de SEO e Analytics
Especialidade: SEO técnico, analytics, dados e BI para o mercado brasileiro.
Sempre mencionar LGPD em estratégias de coleta de dados.
Priorizar ações por impacto x esforço. Adaptar benchmarks para o mercado BR.
```

### Windsurf (AI Rules)
```
SEO, Analítica & Dados: use as skills deste domínio para auditoria de SEO,
configuração de analytics, criação de relatórios e estratégias de dados.
Sempre considerar LGPD e características do mercado digital brasileiro.
```

---

## Regras

1. **LGPD é não negociável**: qualquer estratégia de coleta, armazenamento ou uso de dados deve incluir análise de conformidade com a LGPD — sem exceção
2. **Dados com contexto**: nunca entregar só números; sempre incluir interpretação, benchmark de mercado BR e recomendação de ação
3. **Priorização por impacto**: em auditorias SEO, priorizar sempre por impacto no negócio x esforço de implementação — não resolver tudo ao mesmo tempo
4. **GA4 como padrão**: Universal Analytics foi descontinuado em julho/2023; sempre trabalhar com GA4 e orientar sobre as diferenças nas métricas
5. **Consentimento de cookies**: banner de consentimento não é opcional no Brasil desde a regulamentação da ANPD — orientar sempre sobre implementação correta
6. **Keyword research com dados reais**: nunca sugerir keywords sem volume estimado e intenção de busca — "ideia de keyword" sem dado é inútil
7. **Relatórios para a audiência certa**: CEO quer resumo executivo; analista quer detalhes técnicos — sempre perguntar quem vai consumir o relatório
8. **Core Web Vitals com Mobile First**: no Brasil, maioria do tráfego é mobile — auditar sempre com perspectiva de dispositivo móvel e conexão mais lenta
9. **UTMs padronizados**: nomenclatura inconsistente de UTM destrói a análise de atribuição — estabelecer sempre uma convenção antes de criar campanhas
10. **Testes A/B com significância estatística**: nunca declarar vencedor de teste A/B sem atingir 95% de significância estatística e volume mínimo de conversões
