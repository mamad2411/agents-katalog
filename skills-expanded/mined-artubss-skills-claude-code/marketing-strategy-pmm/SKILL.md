---
name: marketing-strategy-pmm
description: Marketing de produto, posicionamento, estratégia GTM e inteligência competitiva. Inclui definição de ICP, metodologia de posicionamento April Dunford, playbooks de lançamento, battlecards competitivas e guias de entrada em mercados internacionais. Use ao desenvolver posicionamento, planejar lançamentos de produtos, criar mensagens, analisar concorrentes, entrar em novos mercados, capacitar vendas ou quando o usuário menciona marketing de produto, posicionamento, GTM, go-to-market, análise competitiva, entrada em mercado ou capacitação de vendas.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: product-marketing
  updated: 2025-10-20
  frameworks: April-Dunford-positioning, ICP-definition, messaging-hierarchy
  target-market: B2B-SaaS, international-expansion, Series-A+
---

# Estratégia de Marketing & Marketing de Produto

Playbook de marketing de produto especializado para startups Series A+ expandindo internacionalmente com motion híbrida PLG/Sales-Led.

## Palavras-chave
marketing de produto, posicionamento, GTM, estratégia go-to-market, análise competitiva, inteligência competitiva, battlecards, ICP, perfil de cliente ideal, mensagem, proposta de valor, lançamento de produto, entrada em mercado, expansão internacional, capacitação de vendas, análise ganho/perda, PMM, gerente de marketing de produto, posicionamento no mercado, paisagem competitiva, treinamento de vendas

## Cobertura de Papéis

Esta habilidade atende:
- **Product Marketing Manager (PMM)** - Posicionamento, mensagem, inteligência competitiva, lançamentos
- **Head of Marketing** - Estratégia, orçamento, design organizacional, metas de pipeline
- **Head of Growth** - Experimentação, ativação, retenção, loops de crescimento
- **CMO/VP Marketing** - Estratégia executiva, relatórios para conselho, liderança de equipe

## KPIs Principais por Papel

**PMM**: Taxa de adoção de produto, taxa de vitória vs. concorrentes, velocidade de vendas, métricas de impacto de lançamento, taxa de vitória competitiva, crescimento de tamanho de deal

**Head of Marketing**: Pipeline originado por marketing em R$, taxa CAC/LTV, ROMI (meta 3:1+), aumento de awareness de marca, crescimento de market share

**Head of Growth**: Taxa de ativação, WAU/MAU, taxas de conversão ao longo do funnel, período de payback, coeficiente viral (PLG)

**CMO**: Crescimento de receita %, cobertura de pipeline (3-4x), produtividade de equipe, eficiência de orçamento, NPS/saúde de marca

## Integração de Tech Stack

**HubSpot** - CRM, rastreamento de deal, análise de perda competitiva, conteúdo de capacitação de vendas
**Google Analytics** - Uso de produto, funnels de ativação, adoção de features
**Gong/Chorus** - Análise de chamadas de vendas, inteligência competitiva, rastreamento de objeções
**Productboard** - Requisições de features, feedback de clientes, priorização de roadmap
**Notion/Confluence** - Wiki interno, documentos de posicionamento, battlecards competitivas

---

## 1. Fundação Estratégica

### 1.1 Framework de Estratégia de Empresa (Contexto Series A)

**Análise de Estado Atual**:
```
Estágio: Series A
Funding: R$25-75M levantados
Tamanho de equipe: 20-50 pessoas
Receita: R$5-25M ARR
Posição de mercado: Desafiante/Líder de nicho
Meta de taxa de crescimento: 3-5x YoY

Desafios principais:
- Provar product-market fit em escala
- Expandir de early adopters → mainstream
- Entrar em novos mercados (EU/US/Canada)
- Competir contra incumbentes
- Construir motion de vendas repetível
```

**Prioridades Estratégicas** (em ordem):
1. **Consolidar posicionamento** - Proposta de valor clara e diferenciada
2. **Escalar aquisição** - Canais repetíveis e eficientes
3. **Provar retenção** - Stickiness de produto, receita de expansão
4. **Expandir mercados** - Expansão geográfica + vertical
5. **Construir marca** - Awareness, confiança, liderança de categoria

### 1.2 Definição de ICP (Perfil de Cliente Ideal)

**Framework de ICP para B2B SaaS**:

**Firmographics**:
- Tamanho da empresa: 50-5000 funcionários (sweet spot de Series A)
- Indústria: SaaS, Tech, Serviços Profissionais
- Geografia: US, Canada, UK, Germany, France (priorizar por TAM)
- Receita: R$25M-R$2.5B anual
- Estágio de funding: Seed to Growth (evitar pré-produto)

**Technographics**:
- Tech stack: Moderno (cloud-first, API-driven)
- Maturidade: Crescimento rápido, disposição de adotar novas ferramentas
- Ferramentas existentes: [Listar concorrentes + produtos complementares]
- Necessidades de integração: Deve integrar com [Salesforce, Slack, etc.]

**Psychographics**:
- Nível de dor: 7-10/10 (dor aguda, não nice-to-have)
- Motivação do comprador: Eficiência, redução de custos, crescimento de receita
- Processo de decisão: Ciclo de vendas de 2-6 meses
- Tolerância a risco: Early majority (não sangue nos olhos)

**Personas de Comprador** (3-5 personas máximo):

**Primário: Comprador Econômico** (assina contrato)
- Cargo: VP, Director, Head of [Departamento]
- Objetivos: ROI, produtividade de equipe, redução de custos
- Medos: Falha de implementação, resistência de equipe, desperdício de orçamento
- Mensagem: Resultados de negócio, ROI, estudos de caso

**Secundário: Comprador Técnico** (avalia produto)
- Cargo: Senior Engineer, Architect, Tech Lead
- Objetivos: Resolve problema técnico, integração fácil
- Medos: Débito técnico, lock-in de vendor, suporte fraco
- Mensagem: Capacidades técnicas, arquitetura, segurança

**Usuário/Campeão** (defende internamente)
- Cargo: Manager, Team Lead, Power User
- Objetivos: Facilita o trabalho deles, equipe adora
- Medos: Curva de aprendizado, mudança organizacional
- Mensagem: UX, facilidade de uso, quick wins

**Checklist de Validação de ICP**:
- [ ] 5+ clientes pagantes correspondem a este perfil
- [ ] Ciclos de vendas mais rápidos (< tempo mediano para fechar)
- [ ] LTV mais alto (> valor de cliente mediano)
- [ ] Churn mais baixo (< 5% anual)
- [ ] Engajamento de produto forte (uso diário/semanal)
- [ ] Referenciais (NPS 9-10, dispostos a fazer estudos de caso)

**Rastreamento de ICP no HubSpot**:
- Criar propriedade "ICP Fit": A (perfeito), B (bom), C (ok), D (fraco)
- Pontuar baseado em firmographics, engajamento, uso de produto
- Relatório: Taxa de vitória por pontuação de ICP, pipeline por pontuação de ICP
- Ação: Focar aquisição em ICP A/B, nutrir C, desqualificar D

### 1.3 Estratégia de Segmentação de Mercado

**Dimensões de Segmentação**:

**Por Tamanho de Empresa** (recomenda-se começar com um):
- **SMB** (10-200 funcionários) - PLG self-serve, low touch, R$500-R$10k ACV
- **Mid-Market** (200-2000 funcionários) - Híbrido, inside sales, R$10k-R$250k ACV
- **Enterprise** (2000+ funcionários) - Sales-led, field sales, R$250k+ ACV

**Por Vertical** (escolha 2-3 verticais de foco):
- Horizontal: Apelo amplo (ex: gerenciamento de projetos para qualquer indústria)
- Vertical: Específico da indústria (ex: CRM para healthcare, compliance para fintech)
- Abordagem: Comece horizontal, adicione verticais conforme dimensiona

**Por Caso de Uso** (mensagem varia):
- Caso de Uso A: [ex: Colaboração de equipe]
- Caso de Uso B: [ex: Gerenciamento de clientes]
- Caso de Uso C: [ex: Rastreamento de projetos]
- Cada caso de uso = página de destino diferente, mensagem, estudos de caso

**Por Geografia** (foco de Series A):
- **US/Canada**: Maior TAM, ciclos de vendas mais rápidos, disposição de pagamento mais alta
- **UK**: Inglês, gateway para EU, comportamento de compra similar ao US
- **Germany**: Maior economia da EU, altos padrões de privacidade de dados (líder GDPR)
- **France**: Segundo maior mercado da EU, localização crítica
- **Nordics**: Alta adoção de tech, proficiência em inglês, mercados menores

**Matriz de Priorização de Segmentação**:
```
Segmento: Empresas SaaS de Mid-Market nos EUA (200-2000 funcionários)
Prioridade: 1 (Máxima)
Fundamentação:
  - Maior TAM (R$25B)
  - Ciclo de vendas mais rápido (60 dias média)
  - Taxa de vitória mais alta (35%)
  - Alinhamento forte com casos de uso
  - Base de clientes existentes (50% dos clientes)
Alocação de orçamento: 50% do gasto de marketing
```

---

## 2. Posicionamento & Mensagem

### 2.1 Framework de Posicionamento (Método April Dunford)

**Passo 1: Liste Suas Verdadeiras Alternativas Competitivas**

Não apenas concorrentes diretos - o que clientes fariam se seu produto não existisse?

```
Alternativas:
1. Concorrente A (direto)
2. Concorrente B (direto)
3. Planilhas + email (status quo)
4. Construir internamente (DIY)
5. Não fazer nada (ignorar problema)
```

**Passo 2: Isole Seus Atributos Únicos**

O que você tem que alternativas não têm?

```
Atributos únicos:
1. [Feature X que ninguém mais tem]
2. [Integração Y exclusiva]
3. [Abordagem Z diferenciada]
4. [Métrica de performance melhor que todos]
```

**Passo 3: Mapeie Atributos para Valor**

Que valor esses atributos provêm para clientes?

```
Atributo: [Colaboração em tempo real]
→ Valor: Equipes podem trabalhar simultaneamente
→ Resultado: Conclusão de projeto 50% mais rápida

Atributo: [Automação com IA]
→ Valor: Elimina entrada manual de dados
→ Resultado: Economiza 10 horas/semana por usuário
```

**Passo 4: Defina Seus Clientes Melhor Ajustados**

Quem mais se importa com este valor?

```
Melhor ajustado: Empresas SaaS de mid-market (200-1000 funcionários)
Por quê: Têm equipes distribuídas, precisam de colaboração em tempo real
Evidência: Ciclos de vendas mais rápidos, churn menor, NPS mais alto
```

**Passo 5: Consolide Sua Categoria de Mercado**

Em qual mercado você domina?

```
Opções:
- Frente a frente: Compete em categoria existente (ex: "CRM")
- Peixe grande, lagoa pequena: Domine um nicho (ex: "CRM para agências")
- Criar novo: Defina nova categoria (arriscado, caro)

Decisão: [Escolha baseado em força competitiva e orçamento]
```

**Passo 6: Sobreponha Tendências**

Quais tendências tornam este o momento certo para comprar?

```
Tendências:
- Explosão do trabalho remoto (2020-2025)
- Adoção de IA/ML em enterprise (2024-2025)
- Regulações de privacidade de dados (GDPR, CCPA)
```

### 2.2 Arquitetura de Mensagem

**Proposta de Valor (Uma frase)**:

Template: `[Produto] ajuda [Cliente-alvo] [Alcançar meta] ao [Abordagem única]`

Exemplo: "Acme ajuda equipes SaaS de mid-market a entregar 2x mais rápido automatizando workflows de projeto com IA"

**Hierarquia de Mensagem**:

```
NÍVEL 1: Proposta de valor (uma frase)
[Sua proposta aqui]

NÍVEL 2: Benefícios principais (3-5 bullet points)
- Benefício 1: [Velocidade] → Entregue produtos 2x mais rápido
- Benefício 2: [Qualidade] → Reduza bugs em 50%
- Benefício 3: [Colaboração] → Alinhe equipes em tempo real
- Benefício 4: [Custo] → Economize R$500k/ano em ferramentas

NÍVEL 3: Features (evidência de suporte)
- Feature → Benefício → Resultado
- Automação com IA → Elimina trabalho manual → Economiza 10 hrs/semana
- Sincronização em tempo real → Sem conflitos de versão → 50% menos erros
- Integrações → Conecte ferramentas existentes → 80% onboarding mais rápido

NÍVEL 4: Pontos de Comprovação
- Logos de clientes: [Microsoft, Shopify, Stripe]
- Stats: Usado por 10.000+ equipes, classificação 4.8/5 no G2
- Estudos de caso: Como [Cliente] alcançou [Resultado]
```

**Mensagem por Persona**:

**Comprador Econômico** (VP/Director):
- Preocupação primária: ROI, resultados de negócio
- Tom: Profissional, orientado a dados, focado em resultados
- Mensagem-chave: "Aumente receita em 25% enquanto reduz custos em R$1M/ano"
- Comprovação: Calculadora de ROI, estudos de caso com impacto em R$

**Comprador Técnico** (Engineer/Architect):
- Preocupação primária: Encaixe técnico, segurança, escalabilidade
- Tom: Técnico, detalhado, objetivo
- Mensagem-chave: "Arquitetura de nível enterprise com 99.99% uptime e conformidade SOC 2"
- Comprovação: Docs técnicos, whitepaper de segurança, diagrama de arquitetura

**Usuário Final** (Manager/Individual Contributor):
- Preocupação primária: Facilidade de uso, workflow diário
- Tom: Amigável, empático, prático
- Mensagem-chave: "Gaste menos tempo com trabalho repetitivo, mais com o que importa"
- Comprovação: Demo de produto, teste grátis, depoimentos de clientes

### 2.3 Teste & Iteração de Mensagem

**Framework de Teste de Mensagem**:

1. **Qualitativo** (entrevistas com clientes):
   - Pergunte a 10-15 clientes-alvo:
   - "Como você descreveria [Produto] para um colega?"
   - "Qual é o benefício principal que você recebe de [Produto]?"
   - "Por que nos escolheu em vez de [Concorrente]?"

2. **Quantitativo** (testes A/B):
   - Teste variações de mensagem em:
   - Headlines de página de destino
   - Copy de anúncio (LinkedIn, Google)
   - Linhas de assunto de email
   - Meça: CTR, taxa de conversão, requisições de demo

3. **Feedback de vendas** (análise ganho/perda):
   - Pergunte a equipe de vendas mensalmente:
   - "Qual mensagem ressoa mais com prospects?"
   - "Quais objeções estamos ouvindo?"
   - "Como comparamos ao [Concorrente] nos olhos do cliente?"

**Ciclo de Iteração**:
- Teste nova mensagem: 2-4 semanas
- Analise resultados: 1 semana
- Atualize docs de mensagem: 1 semana
- Treine equipe de vendas: 1 semana
- Repita trimestralmente

---

## 3. Inteligência Competitiva

### 3.1 Framework de Análise Competitiva

**Tier 1: Concorrentes Diretos** (frente a frente, mesma categoria)
- [Concorrente A]: Líder de mercado, R$500M+ ARR
- [Concorrente B]: Desafiante em crescimento rápido, Series B
- [Concorrente C]: Alternativa open-source

**Tier 2: Concorrentes Indiretos** (soluções adjacentes)
- [Solução Alternativa D]: Abordagem diferente, caso de uso sobreposto
- [Solução Alternativa E]: Plataforma mais ampla, inclui sua feature

**Tier 3: Status Quo** (o que clientes fazem hoje)
- Planilhas + email
- Construir internamente
- Não fazer nada

**Fontes de Inteligência Competitiva**:
1. **Testes de produto**: Inscreva-se em produtos de concorrentes, use ativamente
2. **Monitoramento de website**: Rastreie mudanças em preços, mensagem, features
3. **Entrevistas com clientes**: Pergunte "Quais alternativas você considerou?"
4. **Gravações de chamada de vendas** (Gong/Chorus): Ouça menções de concorrentes
5. **Sites de análise** (G2, Capterra): Leia análises de concorrentes (pros/cons)
6. **Postagens de emprego**: Contratações de concorrentes = insights de roadmap
7. **Filings financeiros** (se público): Receita, crescimento, estratégia
8. **Mídia social**: Siga executivos e equipes de produto de concorrentes
9. **Canais de parceiros**: Converse com parceiros de implementação compartilhados
10. **Relatórios de indústria**: Gartner, Forrester, IDC

### 3.2 Battlecards Competitivas

**Template de Battlecard** (crie um por concorrente):

```
CONCORRENTE: [Concorrente A]

VISÃO GERAL:
- Fundado: 2015
- Funding: Series C, R$375M levantados
- HQ: São Francisco
- Tamanho: 200 funcionários
- Clientes: 5.000+ empresas
- Preços: R$250-R$2.5k/usuário/mês

POSICIONAMENTO:
- Dizem: "Plataforma all-in-one para equipes modernas"
- Realidade: Amplo mas superficial, não profundo em nenhum caso de uso

PONTOS FORTES PRINCIPAIS (O que fazem bem):
1. Reconhecimento forte de marca (líder de categoria)
2. Grande conjunto de features (amplitude sobre profundidade)
3. Integrações extensas (2.000+ apps)

PONTOS FRACOS PRINCIPAIS (Onde ficam aquém):
1. UI complexa (curva de aprendizado acentuada)
2. Caro (2x nosso preço em escala)
3. Suporte fraco (NPS baixo em análises)
4. Arquitetura legada (desempenho lento)

NOSSAS VANTAGENS:
1. 10x mais fácil de usar (time-to-value em minutos vs. dias)
2. 50% menos caro em 100+ usuários
3. Desempenho superior (2x carregamento mais rápido)
4. Onboarding white-glove (CSM dedicado)

QUANDO VENCER:
- Cliente valoriza facilidade de uso sobre features
- Budget-conscious (não enterprise)
- Precisa rápido time-to-value (<1 semana)
- Experiência fraca com concorrente (switching)

QUANDO PERDER:
- Enterprise (>5000 funcionários) com requisitos complexos
- Precisa de Feature X que ainda não temos
- Integração profunda com ecossistema de concorrente
- Já investiu muito em concorrente (custo evitável)

TALK TRACKS:

Objeção: "Já estamos usando [Concorrente A]"
Resposta: "Ótimo - muitos de nossos clientes vieram de [Concorrente A]. O que te levou a explorar alternativas? [Ouça dores] Tipicamente equipes mudam para nós por [facilidade de uso / custo / desempenho]. Seria útil ver uma comparação lado a lado?"

Objeção: "[Concorrente A] tem mais features"
Resposta: "Verdade - estão há mais tempo e têm feature set mais amplo. Aqui está o que descobrimos: a maioria das equipes usa 20% daquelas features. Nossos clientes amam que focamos em fazer [caso de uso central] excepcionalmente bem em vez de tentar fazer tudo. Quais features são mais críticas para sua equipe?"

PONTOS DE COMPROVAÇÃO:
- Estudo de caso: "[Cliente] mudou de [Concorrente A], reduziu custos em 60%"
- Comparação de análises: "[4.8 vs. 4.2 G2 rating em 'Facilidade de Uso']"
- Taxa de vitória: "35% taxa de vitória em deals competitivos"

PAISAGEM COMPETITIVA:
[Link para mapa de posicionamento competitivo]
[Link para matriz de comparação de features]
```

**Distribuição de Battlecard**:
- Armazene em: Notion, Confluence ou plataforma de capacitação de vendas
- Frequência de atualização: Mensal (ou quando concorrente lança feature maior)
- Acesso: Equipes de vendas, CS, produto, marketing
- Treinamento: Chamadas de atualização competitiva mensais com vendas

### 3.3 Análise de Ganho/Perda

**Processo de Entrevista de Ganho/Perda**:

**Objetivos**:
- Entenda por que você ganhou/perdeu
- Valide posicionamento e mensagem
- Identifique gaps de produto
- Rastreie tendências competitivas

**Processo**:
1. **Identifique deals** (fechados ganhos ou perdidos nos últimos 30 dias)
2. **Solicite entrevista** (email ou workflow HubSpot)
3. **Realize entrevista** (30-45 min, grave com permissão)
4. **Analise dados** (temas, padrões, tendências)
5. **Compartilhe insights** (relatório mensal para produto, vendas, marketing)

**Perguntas de Entrevista** (escolha 8-10):

**Para Ganhos**:
- Qual problema você estava tentando resolver?
- Quais alternativas você avaliou?
- Por nos escolheu em vez de [Concorrente]?
- O que quase te fez escolher outra pessoa?
- O que poderíamos melhorar?

**Para Perdas**:
- Qual problema você estava tentando resolver?
- Quem você escolheu em vez de nós? Por quê?
- O que fizemos bem no processo de vendas?
- O que poderíamos ter feito diferente?
- Você nos consideraria no futuro? Quando?

**Rastreamento de Dados** (em HubSpot ou planilha):

| Deal | Resultado | Razão | Concorrente | Fator de Preço | Gap de Produto | Problema de Mensagem |
|------|-----------|--------|------------|--------------|-------------|-----------------|
| Acme Corp | Ganho | Melhor ajuste de produto | Concorrente A | Não | Não | Não |
| Beta Inc | Perda | Preço | Concorrente B | Sim | Não | Não |
| Gamma LLC | Perda | Feature X faltando | Construído internamente | Não | Sim | Não |

**Relatório Mensal de Insights**:
```
Resumo de Ganho/Perda (Março 2025):
- Total de deals analisados: 20 (12 ganhos, 8 perdas)
- Taxa de vitória: 60%
- Top motivos de ganho:
  1. Facilidade de uso (8 menções)
  2. Melhor suporte (6 menções)
  3. Preço (4 menções)
- Top motivos de perda:
  1. Feature X faltando (4 menções)
  2. Preço (3 menções)
  3. Relacionamento com concorrente (2 menções)

Itens de Ação:
- Produto: Priorize feature X (perdemos 4 deals)
- Vendas: Atualize battlecard do Concorrente A (ganhamos 5 deals competitivos)
- Marketing: Crie estudo de caso no tema "facilidade de uso"
```

---

## 4. Estratégia Go-To-Market (GTM)

### 4.1 Tipos de Motion GTM

**PLG (Product-Led Growth)**:
- Entrada: Teste grátis ou freemium
- Comprador: Usuário final → Manager → VP
- Vendas: Low touch ou self-serve
- ACV: <R$50k
- Exemplo: Slack, Notion, Figma

**Sales-Led Growth**:
- Entrada: Requisição de demo → Qualificação de vendas
- Comprador: VP → C-level
- Vendas: High touch, consultativo
- ACV: R$125k+
- Exemplo: Salesforce, Workday, SAP

**Híbrida (PLG + Sales)**:
- Entrada: Teste grátis para SMB, demo para Enterprise
- Comprador: Usuário final (PLG) ou Executivo (Sales-Led)
- Vendas: Self-serve → Assistida → Enterprise
- ACV: R$25k-R$500k
- Exemplo: HubSpot, Atlassian, Zoom

**Recomendação Series A**: Comece com **Híbrida**
- Razão: Aprendizado mais rápido, TAM mais amplo, scaling eficiente
- Abordagem:
  - Bottom-up (PLG): Teste grátis → Plano pago em equipe → Upgrade para Enterprise
  - Top-down (Sales): Outbound para Enterprise → Demo → POC → Fechar

### 4.2 Playbook de Lançamento GTM (Plano de 90 dias)

**Pré-Lançamento (Dias -90 a -30)**:

Semana 1-4: Fundação
- [ ] Defina ICP e personas de comprador
- [ ] Desenvolva posicionamento e mensagem
- [ ] Crie battlecards competitivas
- [ ] Defina métricas de sucesso (pipeline R$, MQLs, taxa de vitória)

Semana 5-8: Conteúdo & Capacitação
- [ ] Construa páginas de website (homepage, produto, preços)
- [ ] Crie deck de vendas e script de demo
- [ ] Produza ativos de lançamento (one-pager, estudos de caso, FAQs)
- [ ] Desenvolva sequências de nutrição por email
- [ ] Treine equipe de vendas em posicionamento e talk tracks

Semana 9-12: Configuração de Canal
- [ ] Lance campanhas pagas (LinkedIn, Google)
- [ ] Configure rastreamento HubSpot e atribuição
- [ ] Publique conteúdo SEO (posts de blog, guias)
- [ ] Ative parcerias (planos de co-marketing)
- [ ] Teste funnels de conversão (página de destino → inscrição)

**Lançamento (Dias 1-30)**:

Semana 1: Awareness
- [ ] Distribuição de comunicado à imprensa
- [ ] Email de anúncio para banco de dados existente
- [ ] Campanha de mídia social (LinkedIn, Twitter)
- [ ] Anúncios pagos ao vivo (campanhas de awareness)
- [ ] Blitz de vendas outbound (top 100 contas)

Semana 2-4: Ativação
- [ ] Monitore taxas de conversão (diariamente)
- [ ] Teste A/B páginas de destino e copy de anúncio
- [ ] Follow-up de vendas em leads inbound (<4h SLA)
- [ ] Entrevistas com clientes (feedback em posicionamento)
- [ ] Ajuste mensagem baseado em sinais iniciais

**Pós-Lançamento (Dias 31-90)**:

Semana 5-8: Otimização
- [ ] Analise dados ganho/perda (por que ganhamos/perdemos?)
- [ ] Otimize canais com desempenho fraco (pausa ou pivô)
- [ ] Escale canais vencedores (aumento de 20% de orçamento semanal)
- [ ] Publique estudos de caso pós-l