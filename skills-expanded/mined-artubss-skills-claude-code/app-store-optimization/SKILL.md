---
name: app-store-optimization
description: Kit completo de App Store Optimization (ASO) para pesquisa, otimização e acompanhamento de desempenho de aplicativos móveis na Apple App Store e Google Play Store
---

# Skill de App Store Optimization (ASO)

Este skill abrangente fornece recursos completos de ASO para lançar e otimizar com sucesso aplicativos móveis na Apple App Store e Google Play Store.

## Capacidades

### Pesquisa e Análise
- **Pesquisa de Palavras-chave**: Analise volume de buscas, concorrência e relevância para descoberta de apps
- **Análise de Concorrentes**: Análise profunda de apps com melhor desempenho na sua categoria
- **Análise de Tendências de Mercado**: Identifique tendências emergentes e oportunidades na sua categoria
- **Análise de Sentimento de Reviews**: Extraia insights de avaliações de usuários para identificar pontos fortes e problemas
- **Análise de Categoria**: Avalie estratégias ótimas de posicionamento em categoria e subcategoria

### Otimização de Metadados
- **Otimização de Título**: Crie títulos atraentes com posicionamento ótimo de palavras-chave (limites de caracteres específicos por plataforma)
- **Otimização de Descrição**: Elabore descrições curtas e completas que convertam e ranqueiem
- **Subtitle/Texto Promocional**: Otimize o subtitle específico da Apple (30 caracteres) e texto promocional (170 caracteres)
- **Campo de Palavras-chave**: Maximize o campo de 100 caracteres da Apple com seleção estratégica
- **Seleção de Categoria**: Recomendações baseadas em dados para categorias primária e secundária
- **Boas Práticas de Ícone**: Diretrizes para design de ícones de apps com alta conversão
- **Otimização de Screenshots**: Estratégias para criar screenshots que impulsionam instalações
- **Vídeo Preview**: Boas práticas para vídeos de preview do app
- **Localização**: Estratégias de otimização multilíngue para alcance global

### Otimização de Conversão
- **Framework de A/B Testing**: Planeje e acompanhe experimentos de metadados para melhoria contínua
- **Teste de Ativos Visuais**: Teste ícones, screenshots e vídeos para máxima conversão
- **Otimização de Listing da Loja**: Otimização abrangente de página para conversão de impressões em instalações
- **Call-to-Action**: Otimize CTAs em descrições e materiais promocionais

### Gerenciamento de Ratings e Reviews
- **Monitoramento de Reviews**: Acompanhe e analise avaliações de usuários para insights acionáveis
- **Estratégias de Resposta**: Templates e boas práticas para responder a reviews
- **Melhoria de Rating**: Abordagens táticas para melhorar ratings de app organicamente
- **Identificação de Problemas**: Identifique problemas comuns e solicitações de features em reviews

### Estratégias de Lançamento e Atualização
- **Checklist Pré-Lançamento**: Validação completa antes de submeter às lojas
- **Timing de Lançamento**: Otimize tempo de lançamento para máxima visibilidade e downloads
- **Cadência de Atualização**: Planeje frequência ótima de atualização e rollouts de features
- **Anúncios de Features**: Elabore seções "Novidades" que reengajem usuários
- **Otimização Sazonal**: Aproveite tendências sazonais e eventos

### Analytics e Acompanhamento
- **Score de ASO**: Calcule score geral de saúde de ASO em múltiplos fatores
- **Rankings de Palavras-chave**: Acompanhe mudanças de posição de palavras-chave ao longo do tempo
- **Métricas de Conversão**: Monitore taxas de conversão de impressão para instalação
- **Velocidade de Downloads**: Acompanhe tendências e momentum de downloads
- **Benchmarking de Desempenho**: Compare contra médias de categoria e concorrentes

### Requisitos Específicos de Plataforma
- **Apple App Store**:
  - Título: 30 caracteres
  - Subtitle: 30 caracteres
  - Texto Promocional: 170 caracteres (editável sem atualização do app)
  - Descrição: 4.000 caracteres
  - Palavras-chave: 100 caracteres (separadas por vírgula, sem espaços)
  - Novidades: 4.000 caracteres
- **Google Play Store**:
  - Título: 50 caracteres (anteriormente 30, aumentado em 2021)
  - Descrição Curta: 80 caracteres
  - Descrição Completa: 4.000 caracteres
  - Sem campo de palavras-chave separado (palavras-chave extraídas de título e descrição)

## Requisitos de Input

### Pesquisa de Palavras-chave
```json
{
  "app_name": "MyApp",
  "category": "Productivity",
  "target_keywords": ["task manager", "productivity", "todo list"],
  "competitors": ["Todoist", "Any.do", "Microsoft To Do"],
  "language": "en-US"
}
```

### Otimização de Metadados
```json
{
  "platform": "apple" | "google",
  "app_info": {
    "name": "MyApp",
    "category": "Productivity",
    "target_audience": "Professionals aged 25-45",
    "key_features": ["Task management", "Team collaboration", "AI assistance"],
    "unique_value": "AI-powered task prioritization"
  },
  "current_metadata": {
    "title": "Current Title",
    "subtitle": "Current Subtitle",
    "description": "Current description..."
  },
  "target_keywords": ["productivity", "task manager", "todo"]
}
```

### Análise de Reviews
```json
{
  "app_id": "com.myapp.app",
  "platform": "apple" | "google",
  "date_range": "last_30_days" | "last_90_days" | "all_time",
  "rating_filter": [1, 2, 3, 4, 5],
  "language": "en"
}
```

### Cálculo de Score de ASO
```json
{
  "metadata": {
    "title_quality": 0.8,
    "description_quality": 0.7,
    "keyword_density": 0.6
  },
  "ratings": {
    "average_rating": 4.5,
    "total_ratings": 15000
  },
  "conversion": {
    "impression_to_install": 0.05
  },
  "keyword_rankings": {
    "top_10": 5,
    "top_50": 12,
    "top_100": 18
  }
}
```

## Formatos de Output

### Relatório de Pesquisa de Palavras-chave
- Lista de palavras-chave recomendadas com estimativas de volume de buscas
- Análise de nível de concorrência (baixa/média/alta)
- Scores de relevância para cada palavra-chave
- Recomendações estratégicas para palavras-chave primárias vs. secundárias
- Oportunidades de palavras-chave long-tail

### Pacote de Metadados Otimizados
- Título específico de plataforma (com validação de contagem de caracteres)
- Subtitle/texto promocional (Apple)
- Descrição curta (Google)
- Descrição completa (ambas plataformas)
- Campo de palavras-chave (Apple - 100 caracteres)
- Validação de contagem de caracteres para todos os campos
- Análise de densidade de palavras-chave
- Comparação antes/depois

### Relatório de Análise de Concorrentes
- Top 10 concorrentes na categoria
- Suas estratégias de metadados
- Análise de sobreposição de palavras-chave
- Avaliação de ativos visuais
- Comparação de volume de ratings e reviews
- Gaps e oportunidades identificadas

### Score de Saúde de ASO
- Score geral (0-100)
- Breakdown por categoria:
  - Qualidade de Metadados (0-25)
  - Ratings e Reviews (0-25)
  - Desempenho de Palavras-chave (0-25)
  - Métricas de Conversão (0-25)
- Recomendações específicas de melhoria
- Itens de ação prioritários

### Plano de A/B Test
- Hipótese e variáveis de teste
- Recomendações de duração de teste
- Definição de métricas de sucesso
- Cálculos de tamanho de amostra
- Limiares de significância estatística

### Checklist de Lançamento
- Validação pré-submissão (todos os ativos e metadados necessários)
- Verificação de conformidade com lojas
- Checklist de testes (dispositivos, versões de SO)
- Itens de preparação de marketing
- Plano de monitoramento pós-lançamento

## Como Usar

### Pesquisa de Palavras-chave
```
Hey Claude—I just added the "app-store-optimization" skill. Can you research the best keywords for a productivity app targeting professionals? Focus on keywords with good search volume but lower competition.
```

### Otimizar Listing da App Store
```
Hey Claude—I just added the "app-store-optimization" skill. Can you optimize my app's metadata for the Apple App Store? Here's my current listing: [provide current metadata]. I want to rank for "task management" and "productivity tools".
```

### Analisar Estratégia de Concorrente
```
Hey Claude—I just added the "app-store-optimization" skill. Can you analyze the ASO strategies of Todoist, Any.do, and Microsoft To Do? I want to understand what they're doing well and where there are opportunities.
```

### Análise de Sentimento de Reviews
```
Hey Claude—I just added the "app-store-optimization" skill. Can you analyze recent reviews for my app (com.myapp.ios) and identify the most common user complaints and feature requests?
```

### Calcular Score de ASO
```
Hey Claude—I just added the "app-store-optimization" skill. Can you calculate my app's overall ASO health score and provide specific recommendations for improvement?
```

### Planejar A/B Test
```
Hey Claude—I just added the "app-store-optimization" skill. I want to A/B test my app icon and first screenshot. Can you help me design the test and determine how long to run it?
```

### Checklist Pré-Lançamento
```
Hey Claude—I just added the "app-store-optimization" skill. Can you generate a comprehensive pre-launch checklist for submitting my app to both Apple App Store and Google Play Store?
```

## Scripts

### keyword_analyzer.py
Analisa palavras-chave para volume de buscas, concorrência e relevância. Fornece recomendações estratégicas para palavras-chave primárias e secundárias.

**Funções Principais:**
- `analyze_keyword()`: Analise métricas de palavras-chave individual
- `compare_keywords()`: Compare múltiplas palavras-chave
- `find_long_tail()`: Descubra oportunidades de palavras-chave long-tail
- `calculate_keyword_difficulty()`: Avalie nível de concorrência

### metadata_optimizer.py
Otimiza títulos, descrições e campos de palavras-chave com validação de limite de caracteres específica de plataforma.

**Funções Principais:**
- `optimize_title()`: Crie títulos atraentes e ricos em palavras-chave
- `optimize_description()`: Gere descrições focadas em conversão
- `optimize_keyword_field()`: Maximize o campo de 100 caracteres da Apple
- `validate_character_limits()`: Garanta conformidade com limites de plataforma
- `calculate_keyword_density()`: Analise uso de palavras-chave em metadados

### competitor_analyzer.py
Analisa estratégias de ASO de principais concorrentes e identifica oportunidades.

**Funções Principais:**
- `get_top_competitors()`: Identifique líderes de categoria
- `analyze_competitor_metadata()`: Extraia e analise palavras-chave de concorrentes
- `compare_visual_assets()`: Avalie ícones e screenshots
- `identify_gaps()`: Encontre oportunidades competitivas

### aso_scorer.py
Calcula score abrangente de saúde de ASO em múltiplas dimensões.

**Funções Principais:**
- `calculate_overall_score()`: Compute score de ASO 0-100
- `score_metadata_quality()`: Avalie qualidade de título, descrição, palavras-chave
- `score_ratings_reviews()`: Avalie qualidade e volume de ratings
- `score_keyword_performance()`: Analise posições de ranking
- `score_conversion_metrics()`: Avalie taxas de impressão para instalação
- `generate_recommendations()`: Forneça itens de ação priorizados

### ab_test_planner.py
Planeja e acompanha A/B testes para metadados e ativos visuais.

**Funções Principais:**
- `design_test()`: Crie hipótese e variáveis de teste
- `calculate_sample_size()`: Determine duração necessária de teste
- `calculate_significance()`: Avalie significância estatística
- `track_results()`: Monitore desempenho de teste
- `generate_report()`: Resuma resultados de teste

### localization_helper.py
Gerencia estratégias de otimização de ASO multilíngue.

**Funções Principais:**
- `identify_target_markets()`: Recomende prioridades de localização
- `translate_metadata()`: Gere metadados localizados
- `adapt_keywords()`: Pesquise palavras-chave específicas de locale
- `validate_translations()`: Verifique limites de caracteres por idioma
- `calculate_localization_roi()`: Estime impacto de localização

### review_analyzer.py
Analisa reviews de usuários para sentimento, problemas e solicitações de features.

**Funções Principais:**
- `analyze_sentiment()`: Calcule ratios positivo/negativo/neutro
- `extract_common_themes()`: Identifique tópicos frequentemente mencionados
- `identify_issues()`: Identifique bugs e reclamações de usuários
- `find_feature_requests()`: Extraia features desejadas
- `track_sentiment_trends()`: Monitore sentimento ao longo do tempo
- `generate_response_templates()`: Crie rascunhos de resposta a reviews

### launch_checklist.py
Gera checklists abrangentes pré-lançamento e de atualização.

**Funções Principais:**
- `generate_prelaunch_checklist()`: Validação completa de submissão
- `validate_app_store_compliance()`: Verifique diretrizes da Apple
- `validate_play_store_compliance()`: Verifique políticas do Google
- `create_update_plan()`: Planeje cadência e features de atualização
- `optimize_launch_timing()`: Recomende datas de lançamento
- `plan_seasonal_campaigns()`: Identifique oportunidades sazonais

## Boas Práticas

### Pesquisa de Palavras-chave
1. **Volume vs. Concorrência**: Equilibre palavras-chave de alto volume com rankings alcançáveis
2. **Relevância em Primeiro Lugar**: Segmente apenas palavras-chave genuinamente relevantes ao seu app
3. **Estratégia Long-Tail**: Inclua frases de 3-4 palavras com concorrência menor
4. **Pesquisa Contínua**: Tendências de palavras-chave mudam—pesquise trimestralmente
5. **Palavras-chave de Concorrentes**: Não copie cegamente; garanta relevância às suas features

### Otimização de Metadados
1. **Front-Load de Palavras-chave**: Coloque palavras-chave mais importantes no início de título/descrição
2. **Linguagem Natural**: Escreva para humanos primeiro, SEO em segundo
3. **Benefícios de Features**: Foque em benefícios do usuário, não apenas features
4. **A/B Teste Tudo**: Teste títulos, descrições, screenshots sistematicamente
5. **Atualize Regularmente**: Atualize metadados a cada atualização importante
6. **Limites de Caracteres**: Use cada caractere—não desperdice espaço valioso
7. **Campo de Palavras-chave da Apple**: Sem plurais, duplicatas ou espaços entre vírgulas

### Ativos Visuais
1. **Ícone**: Deve ser reconhecível em tamanhos pequenos (60x60px)
2. **Screenshots**: Primeiros 2-3 são críticos—maioria dos usuários não scrolleia
3. **Legendas**: Use legendas em screenshots para contar sua história de valor
4. **Consistência**: Combine estilo visual com design do app
5. **A/B Teste Ícones**: Ícone é o elemento visual mais importante

### Reviews e Ratings
1. **Responda Rápido**: Responda a reviews em 24-48 horas
2. **Tom Profissional**: Sempre cortês, até com reviews negativos
3. **Aborde Problemas**: Mostre que você está corrigindo problemas reportados
4. **Agradeça Apoiadores**: Reconheça reviews positivos
5. **Solicite Estrategicamente**: Peça ratings após experiências positivas

### Estratégia de Lançamento
1. **Soft Launch**: Considere lançar em mercados menores primeiro
2. **Timing de PR**: Coordene cobertura de imprensa com lançamento
3. **Atualize Frequentemente**: Atualizações iniciais sinalizam desenvolvimento ativo
4. **Monitore Próximo**: Acompanhe métricas diariamente nas primeiras 2 semanas
5. **Itere Rapidamente**: Corrija problemas críticos imediatamente

### Localização
1. **Priorize Mercados**: Comece com inglês, espanhol, chinês, francês, alemão
2. **Falantes Nativos**: Use tradutores profissionais, não tradução automática
3. **Adaptação Cultural**: Algumas features ressoam diferentemente por cultura
4. **Teste Localmente**: Peça a falantes nativos que revejam antes de publicar
5. **Meça ROI**: Acompanhe downloads por locale para avaliar impacto

## Limitações

### Dependências de Dados
- Estimativas de volume de busca de palavras-chave são aproximadas (sem dados oficiais da Apple/Google)
- Dados de concorrentes podem ser incompletos para apps privados
- Análise de reviews limitada a reviews públicos (não consegue acessar feedback privado)
- Dados históricos podem não estar disponíveis para apps novos

### Restrições de Plataforma
- Mudanças de palavras-chave da Apple App Store exigem submissão de app (exceto Texto Promocional)
- Mudanças de metadados do Google Play Store levam 1-2 horas para indexar
- A/B testing requer tráfego significativo para significância estatística
- Algoritmos das lojas são proprietários e mudam sem aviso

### Variabilidade da Indústria
- Benchmarks de ASO variam significativamente por categoria (games vs. utilitários)
- Sazonalidade afeta diferentes categorias de forma diferente
- Mercados geográficos têm cenários competitivos diferentes
- Preferências culturais impactam o que funciona em diferentes países

### Limites de Escopo
- Não inclui estratégias pagas de aquisição de usuários (Apple Search Ads, Google Ads)
- Não cobre desenvolvimento de app ou otimização de UI/UX
- Não inclui implementação de analytics de app (use Firebase, Mixpanel, etc.)
- Não trata de problemas técnicos de submissão de app (provisioning profiles, certificados)

### Quando NÃO Usar Este Skill
- Para web apps (estratégias de SEO diferentes se aplicam)
- Para apps enterprise não em lojas públicas
- Para apps em beta/TestFlight apenas
- Se você precisa de estratégias de publicidade paga (use skills de marketing em vez disso)

## Integração com Outros Skills

Este skill funciona bem com:
- **Content Strategy Skills**: Para criar descrições de app e copy de marketing
- **Analytics Skills**: Para analisar dados de download e engagement
- **Localization Skills**: Para gerenciar conteúdo multilíngue
- **Design Skills**: Para criar ativos visuais otimizados
- **Marketing Skills**: Para coordenar campanhas de lançamento mais amplas

## Versão e Atualizações

Este skill é baseado em requisitos atuais da Apple App Store e Google Play Store a partir de novembro de 2025. Políticas de lojas e boas práticas evoluem—verifique requisitos atuais antes de lançamentos importantes.

**Atualizações Chave para Monitorar:**
- Atualizações de Apple App Store Connect (apple.com/app-store/review/guidelines)
- Atualizações do Google Play Console (play.google.com/console/about/guides/releasewithconfidence)
- Taxas de adoção de versão iOS/Android (afeta testes de dispositivo)
- Mudanças de algoritmo de loja (siga blogs e comunidades de ASO)