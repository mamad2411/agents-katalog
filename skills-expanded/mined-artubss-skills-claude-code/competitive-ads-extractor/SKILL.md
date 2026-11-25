---
name: competitive-ads-extractor
description: Extrai e analisa anúncios de concorrentes de bibliotecas de anúncios (Facebook, LinkedIn, etc.) para entender que mensagens, problemas e abordagens criativas estão funcionando. Ajuda a inspirar e melhorar suas próprias campanhas de anúncios.
---

# Extrator de Anúncios Competitivos

Essa skill extrai os anúncios de seus concorrentes de bibliotecas de anúncios e analisa o que está funcionando—os problemas que estão destacando, casos de uso que estão direcionando e copy/criação que está ressoando.

## Quando Usar Essa Skill

- Pesquisando estratégias de anúncios de concorrentes
- Encontrando inspiração para seus próprios anúncios
- Entendendo posicionamento de mercado
- Identificando padrões de anúncios bem-sucedidos
- Analisando mensagens que funcionam
- Descobrindo novos casos de uso ou pontos de dor
- Planejando campanhas de anúncios com conceitos comprovados

## O Que Essa Skill Faz

1. **Extrai Anúncios**: Coleta anúncios da Facebook Ad Library, LinkedIn, etc.
2. **Captura Screenshots**: Salva cópias visuais de todos os anúncios
3. **Analisa Mensagens**: Identifica problemas, casos de uso e propostas de valor
4. **Categoriza Anúncios**: Agrupa por tema, público ou formato
5. **Identifica Padrões**: Encontra abordagens bem-sucedidas comuns
6. **Oferece Insights**: Explica por que certos anúncios provavelmente têm bom desempenho

## Como Usar

### Extração Básica

```
Extract all current ads from [Competitor Name] on Facebook Ad Library
```

```
Scrape ads from [Company] and analyze their messaging
```

### Análise Específica

```
Get all ads from [Competitor] focusing on their messaging 
about [specific problem]. What pain points are they highlighting?
```

### Conjunto Competitivo

```
Extract ads from these 5 competitors: [list]. 
Compare their approaches and tell me what's working.
```

### Plataforma Específica

```
Get LinkedIn ads from [Competitor] and analyze their 
B2B positioning strategy
```

## Exemplo

**Usuário**: "Extract ads from Notion on Facebook Ad Library and tell me what messaging is working for them."

**Processo**:
```
Accessing Facebook Ad Library...
Searching for: Notion
Found: 23 active ads

Extracting screenshots...
[████████████████████] 100%

Saved to: competitor-ads/notion/
- ad-001-collaboration.png
- ad-002-productivity.png
- ad-003-templates.png
...

Analyzing messaging...
```

**Output**:
```
# Análise de Anúncios da Notion

## Visão Geral
- Anúncios Totais: 23 ativos
- Temas Primários: Produtividade (35%), Colaboração (30%), 
  Templates (20%), Recursos IA (15%)
- Formatos de Anúncio: Imagens estáticas (60%), Vídeo (40%)
- Padrões de CTA: "Experimente grátis", "Comece agora"

## Principais Problemas que Estão Destacando

1. **Informações Espalhadas** (8 anúncios)
   Copy: "Stop switching between 10 different tools"
   Por que funciona: Ponto de dor direto que muitos times enfrentam

2. **Sobrecarga de Reuniões** (5 anúncios)
   Copy: "Replace unnecessary meetings with async updates"
   Por que funciona: Ponto de dor do trabalho remoto pós-COVID

3. **Documentação Perdida** (4 anúncios)
   Copy: "Never ask 'where is that doc?' again"
   Por que funciona: Frustração universal do ambiente de trabalho

## Padrões Criativos Bem-Sucedidos

### Padrão 1: Dividido Antes/Depois
- Mostra paisagem caótica de ferramentas → Espaço de trabalho limpo da Notion
- Usado em 6 anúncios com alto desempenho
- Metáfora visual imediatamente clara

### Padrão 2: Demonstração de Recurso
- GIF do uso real do produto
- Mostra recurso específico em 5 segundos
- Usado para novos recursos (IA, templates)

### Padrão 3: Prova Social
- Mensagem "Junte-se a 20M de usuários"
- Logos de clientes
- Usado em 4 anúncios direcionando para empresa

## Copy Que Está Funcionando

Melhores Headlines:
1. "Your team's knowledge, finally in one place"
   → Focado em benefício, aborda ponto de dor diretamente
   
2. "The all-in-one workspace"
   → Posicionamento claro, apelo amplo
   
3. "AI that actually helps you work"
   → Aborda ceticismo em IA, ângulo prático

Padrões de Body Copy Melhores:
- Frases curtas (menos de 10 palavras)
- Foco em resultados não em recursos
- Inclua números específicos ("Cut meetings by 50%")

## Insights de Direcionamento de Público

Baseado em variações de anúncios:
- Founders startup: Ângulo de produtividade solo
- Team leads: Colaboração e alinhamento
- Empresa: Menções de segurança e conformidade
- Estudantes: Plano grátis, templates, organização

## Recomendações para Seus Anúncios

1. **Teste o ponto de dor "proliferação de ferramentas"**
   → Ressonância forte baseada na frequência de anúncios deles

2. **Use screenshots de produto em vez de visuais abstratos**
   → Todos os anúncios principais deles mostram UI real

3. **Comece com o problema, não a solução**
   → "Tired of X?" tem melhor desempenho que "Introducing Y"

4. **Mantenha copy abaixo de 100 caracteres**
   → Seus anúncios mais curtos parecem mais frequentes

5. **Teste formatos visuais antes/depois**
   → Padrão comprovado em sua criação

## Arquivos Salvos
- All ads: ~/competitor-ads/notion/
- Analysis: ~/competitor-ads/notion/analysis.md
- Best performers: ~/competitor-ads/notion/top-10/
```

**Inspirado por:** Caso de uso de Sumant Subrahmanya da Lenny's Newsletter

## O Que Você Pode Aprender

### Análise de Mensagens
- Que problemas eles enfatizam
- Como se posicionam contra concorrência
- Propostas de valor que ressoam
- Segmentos de público-alvo

### Padrões Criativos
- Estilos visuais que funcionam
- Desempenho de vídeo vs. imagem estática
- Esquemas de cores e marca
- Padrões de layout

### Fórmulas de Copy
- Estruturas de headline
- Padrões de call-to-action
- Comprimento e tom
- Disparadores emocionais

### Estratégia de Campanha
- Campanhas sazonais
- Abordagens de lançamento de produto
- Táticas de anúncio de recurso
- Padrões de retargeting

## Boas Práticas

### Legal & Ético
✓ Use apenas para pesquisa e inspiração
✓ Não copie anúncios diretamente
✓ Respeite propriedade intelectual
✓ Use insights para informar criação original
✗ Não plagie copy ou roube designs

### Dicas de Análise
1. **Procure por padrões**: Que temas se repetem?
2. **Rastreie ao longo do tempo**: Salve anúncios mensalmente para ver evolução
3. **Teste hipóteses**: Adapte padrões bem-sucedidos para sua marca
4. **Segmente por público**: Diferentes mensagens para públicos diferentes
5. **Compare plataformas**: Mensagens LinkedIn vs Facebook diferem

## Recursos Avançados

### Rastreamento de Tendências
```
Compare [Competitor]'s ads from Q1 vs Q2. 
What messaging has changed?
```

### Análise de Múltiplos Concorrentes
```
Extract ads from [Company A], [Company B], [Company C]. 
What are the common patterns? Where do they differ?
```

### Benchmarks da Indústria
```
Show me ad patterns across the top 10 project management 
tools. What problems do they all focus on?
```

### Análise de Formato
```
Analyze video ads vs static image ads from [Competitor]. 
Which gets more engagement? (if data available)
```

## Fluxos de Trabalho Comuns

### Planejamento de Campanha de Anúncios
1. Extrai anúncios de concorrentes
2. Identifica padrões bem-sucedidos
3. Anota lacunas na mensagem deles
4. Brainstorm ângulos únicos
5. Esboça variações de teste de anúncio

### Pesquisa de Posicionamento
1. Obtenha anúncios de 5 concorrentes
2. Mapeie o posicionamento deles
3. Encontre ângulos pouco explorados
4. Desenvolva mensagem diferenciada
5. Teste contra abordagens deles

### Inspiração Criativa
1. Extrai anúncios por tema
2. Analisa padrões visuais
3. Anota tendências de cor e layout
4. Adapta padrões bem-sucedidos
5. Cria variações originais

## Dicas para o Sucesso

1. **Monitoramento Regular**: Verifique mensalmente por mudanças
2. **Pesquisa Ampla**: Procure também em concorrentes adjacentes
3. **Salve Tudo**: Construa uma biblioteca de referência
4. **Teste Insights**: Execute seus próprios experimentos
5. **Rastreie Desempenho**: Teste A/B conceitos inspirados
6. **Mantenha Originalidade**: Use para inspiração, não cópia
7. **Múltiplas Plataformas**: Compare Facebook, LinkedIn, TikTok, etc.

## Formatos de Output

- **Screenshots**: Todos os anúncios salvos como imagens
- **Relatório de Análise**: Resumo em Markdown de insights
- **Planilha**: CSV com copy de anúncio, CTAs, temas
- **Apresentação**: Deck visual de melhores performers
- **Biblioteca de Padrões**: Categorizada por abordagem

## Casos de Uso Relacionados

- Escrever melhor copy de anúncio para suas campanhas
- Entender posicionamento de mercado
- Encontrar lacunas de conteúdo em sua mensagem
- Descobrir novos casos de uso para seu produto
- Planejar estratégia de product marketing
- Inspirar conteúdo de mídia social