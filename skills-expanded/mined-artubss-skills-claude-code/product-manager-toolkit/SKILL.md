---
name: product-manager-toolkit
description: Kit de ferramentas completo para gerentes de produto, incluindo priorização RICE, análise de entrevistas com clientes, templates de PRD, frameworks de descoberta e estratégias de go-to-market. Use para priorização de features, síntese de pesquisa com usuários, documentação de requisitos e desenvolvimento de estratégia de produto.
---

# Kit de Ferramentas para Gerentes de Produto

Ferramentas e frameworks essenciais para gestão de produto moderna, da descoberta à entrega.

## Início Rápido

### Para Priorização de Features
```bash
python scripts/rice_prioritizer.py sample  # Create sample CSV
python scripts/rice_prioritizer.py sample_features.csv --capacity 15
```

### Para Análise de Entrevistas
```bash
python scripts/customer_interview_analyzer.py interview_transcript.txt
```

### Para Criação de PRD
1. Escolha um template em `references/prd_templates.md`
2. Preencha as seções com base no trabalho de descoberta
3. Revise com os stakeholders
4. Controle de versão na sua ferramenta de PM

## Fluxos de Trabalho Principais

### Processo de Priorização de Features

1. **Coleta de Solicitações de Features**
   - Feedback de clientes
   - Solicitações de vendas
   - Débito técnico
   - Iniciativas estratégicas

2. **Pontuação com RICE**
   ```bash
   # Create CSV with: name,reach,impact,confidence,effort
   python scripts/rice_prioritizer.py features.csv
   ```
   - **Reach**: Usuários afetados por trimestre
   - **Impact**: massive/high/medium/low/minimal
   - **Confidence**: high/medium/low
   - **Effort**: xl/l/m/s/xs (person-months)

3. **Analise o Portfólio**
   - Revise quick wins vs big bets
   - Verifique a distribuição de esforço
   - Valide em relação à estratégia

4. **Gere o Roadmap**
   - Planejamento de capacidade trimestral
   - Mapeamento de dependências
   - Alinhamento de stakeholders

### Processo de Descoberta com Clientes

1. **Conduza Entrevistas**
   - Use formato semi-estruturado
   - Foque em problemas, não em soluções
   - Grave com permissão

2. **Analise Insights**
   ```bash
   python scripts/customer_interview_analyzer.py transcript.txt
   ```
   Extrai:
   - Pontos de dor com severidade
   - Solicitações de features com prioridade
   - Jobs to be done
   - Análise de sentimento
   - Temas e citações principais

3. **Sintetize Descobertas**
   - Agrupe pontos de dor similares
   - Identifique padrões entre entrevistas
   - Mapeie para áreas de oportunidade

4. **Valide Soluções**
   - Crie hipóteses de solução
   - Teste com protótipos
   - Meça comportamento real vs esperado

### Processo de Desenvolvimento de PRD

1. **Escolha um Template**
   - **PRD Padrão**: Features complexas (6-8 semanas)
   - **PRD Uma Página**: Features simples (2-4 semanas)
   - **Feature Brief**: Fase de exploração (1 semana)
   - **Epic Ágil**: Entrega baseada em sprints

2. **Estruture o Conteúdo**
   - Problema → Solução → Métricas de Sucesso
   - Sempre inclua o que está fora de escopo
   - Critérios de aceitação claros

3. **Colabore**
   - Engenharia para viabilidade
   - Design para experiência
   - Vendas para validação de mercado
   - Suporte para impacto operacional

## Scripts Principais

### rice_prioritizer.py
Implementação avançada do framework RICE com análise de portfólio.

**Características**:
- Cálculo de pontuação RICE
- Análise de equilíbrio do portfólio (quick wins vs big bets)
- Geração de roadmap trimestral
- Planejamento de capacidade da equipe
- Múltiplos formatos de saída (text/json/csv)

**Exemplos de Uso**:
```bash
# Basic prioritization
python scripts/rice_prioritizer.py features.csv

# With custom team capacity (person-months per quarter)
python scripts/rice_prioritizer.py features.csv --capacity 20

# Output as JSON for integration
python scripts/rice_prioritizer.py features.csv --output json
```

### customer_interview_analyzer.py
Análise de entrevistas baseada em NLP para extrair insights acionáveis.

**Capacidades**:
- Extração de pontos de dor com avaliação de severidade
- Identificação e classificação de solicitações de features
- Reconhecimento de padrões de jobs-to-be-done
- Análise de sentimento
- Extração de temas
- Menções de concorrentes
- Identificação de citações principais

**Exemplos de Uso**:
```bash
# Analyze single interview
python scripts/customer_interview_analyzer.py interview.txt

# Output as JSON for aggregation
python scripts/customer_interview_analyzer.py interview.txt json
```

## Documentos de Referência

### prd_templates.md
Múltiplos formatos de PRD para diferentes contextos:

1. **Template PRD Padrão**
   - Formato abrangente com 11 seções
   - Melhor para features principais
   - Inclui especificações técnicas

2. **PRD Uma Página**
   - Formato conciso para alinhamento rápido
   - Foco em problema/solução/métricas
   - Bom para features menores

3. **Template Epic Ágil**
   - Entrega baseada em sprints
   - Mapeamento de user stories
   - Foco em critérios de aceitação

4. **Feature Brief**
   - Exploração leve
   - Orientado por hipótese
   - Fase pré-PRD

## Frameworks de Priorização

### Framework RICE
```
Score = (Reach × Impact × Confidence) / Effort

Reach: # de usuários/trimestre
Impact: 
  - Massive = 3x
  - High = 2x
  - Medium = 1x
  - Low = 0.5x
  - Minimal = 0.25x
Confidence:
  - High = 100%
  - Medium = 80%
  - Low = 50%
Effort: Person-months
```

### Matriz Valor vs Esforço
```
         Baixo Esforço  Alto Esforço
         
Alto     QUICK WINS    BIG BETS
Valor    [Priorize]     [Estratégico]
         
Baixo    FILL-INS      TIME SINKS
Valor    [Talvez]       [Evite]
```

### Método MoSCoW
- **Must Have**: Crítico para lançamento
- **Should Have**: Importante mas não crítico
- **Could Have**: Seria legal ter
- **Won't Have**: Fora de escopo

## Frameworks de Descoberta

### Guia de Entrevista com Clientes
```
1. Perguntas de Contexto (5 min)
   - Cargo e responsabilidades
   - Workflow atual
   - Ferramentas utilizadas

2. Exploração de Problemas (15 min)
   - Pontos de dor
   - Frequência e impacto
   - Workarounds atuais

3. Validação de Solução (10 min)
   - Reação a conceitos
   - Percepção de valor
   - Disposição para pagar

4. Fechamento (5 min)
   - Outros pensamentos
   - Indicações
   - Permissão para follow-up
```

### Template de Hipótese
```
Acreditamos que [construir esta feature]
Para [esses usuários]
Vai [alcançar este resultado]
Saberemos que estamos certos quando [métrica]
```

### Árvore de Oportunidade-Solução
```
Resultado
├── Oportunidade 1
│   ├── Solução A
│   └── Solução B
└── Oportunidade 2
    ├── Solução C
    └── Solução D
```

## Métricas e Análise

### Framework de North Star Metric
1. **Identifique o Valor Principal**: Qual é o valor #1 para os usuários?
2. **Torne-o Mensurável**: Quantificável e rastreável
3. **Garanta que seja Acionável**: As equipes podem influenciá-lo
4. **Verifique Leading Indicator**: Prediz sucesso dos negócios

### Template de Análise de Funnel
```
Aquisição → Ativação → Retenção → Receita → Indicação

Métricas Principais:
- Taxa de conversão em cada etapa
- Pontos de abandono
- Tempo entre etapas
- Variações por coorte
```

### Métricas de Sucesso de Feature
- **Adoção**: % de usuários usando a feature
- **Frequência**: Uso por usuário por período
- **Profundidade**: % de capacidade da feature utilizada
- **Retenção**: Uso contínuo ao longo do tempo
- **Satisfação**: NPS/CSAT para a feature

## Melhores Práticas

### Escrevendo Ótimos PRDs
1. Comece com o problema, não a solução
2. Inclua métricas de sucesso claras antecipadamente
3. Declare explicitamente o que está fora de escopo
4. Use visuais (wireframes, flows)
5. Mantenha detalhes técnicos no apêndice
6. Controle de versão das mudanças

### Priorização Efetiva
1. Misture quick wins com apostas estratégicas
2. Considere o custo de oportunidade
3. Leve em conta dependências
4. Deixe margem para trabalho inesperado (20%)
5. Revise trimestralmente
6. Comunique decisões com clareza

### Dicas de Descoberta com Clientes
1. Pergunte "por que" 5 vezes
2. Foque em comportamento passado, não intenções futuras
3. Evite perguntas tendenciosas
4. Entreviste no ambiente deles
5. Procure por reações emocionais
6. Valide com dados

### Gestão de Stakeholders
1. Identifique RACI para decisões
2. Atualizações assíncronas regulares
3. Demo em vez de documentação
4. Aborde preocupações cedo
5. Celebre vitórias publicamente
6. Aprenda com fracassos abertamente

## Armadilhas Comuns a Evitar

1. **Pensar Primeiro em Solução**: Pular para features antes de entender problemas
2. **Paralisia por Análise**: Pesquisar demais sem lançar
3. **Feature Factory**: Lançar features sem medir impacto
4. **Ignorar Débito Técnico**: Não alocar tempo para saúde da plataforma
5. **Surpresa de Stakeholders**: Não comunicar cedo e frequentemente
6. **Theater de Métricas**: Otimizar métricas de vaidade em vez de valor real

## Pontos de Integração

Este kit se integra com:
- **Analytics**: Amplitude, Mixpanel, Google Analytics
- **Roadmapping**: ProductBoard, Aha!, Roadmunk
- **Design**: Figma, Sketch, Miro
- **Development**: Jira, Linear, GitHub
- **Research**: Dovetail, UserVoice, Pendo
- **Communication**: Slack, Notion, Confluence

## Cheat Sheet de Comandos Rápidos

```bash
# Prioritization
python scripts/rice_prioritizer.py features.csv --capacity 15

# Interview Analysis
python scripts/customer_interview_analyzer.py interview.txt

# Create sample data
python scripts/rice_prioritizer.py sample

# JSON outputs for integration
python scripts/rice_prioritizer.py features.csv --output json
python scripts/customer_interview_analyzer.py interview.txt json
```