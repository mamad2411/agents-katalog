---
name: content-creator
description: Crie conteúdo de marketing otimizado para SEO com voz de marca consistente. Inclui analisador de voz de marca, otimizador de SEO, frameworks de conteúdo e templates de redes sociais. Use ao escrever posts em blog, criar conteúdo de redes sociais, analisar voz de marca, otimizar SEO, planejar calendários de conteúdo, ou quando o usuário menciona criação de conteúdo, voz de marca, otimização de SEO, marketing em redes sociais ou estratégia de conteúdo.
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  domain: content-marketing
  updated: 2025-10-20
  python-tools: brand_voice_analyzer.py, seo_optimizer.py
  tech-stack: SEO, social-media-platforms
---

# Content Creator

Análise profissional de voz de marca, otimização de SEO e frameworks de conteúdo específicos por plataforma.

## Palavras-chave
criação de conteúdo, posts em blog, SEO, voz de marca, redes sociais, calendário de conteúdo, conteúdo de marketing, estratégia de conteúdo, marketing de conteúdo, consistência de marca, otimização de conteúdo, marketing em redes sociais, planejamento de conteúdo, escrita de blog, frameworks de conteúdo, diretrizes de marca, estratégia de redes sociais

## Início Rápido

### Para Desenvolvimento de Voz de Marca
1. Execute `scripts/brand_voice_analyzer.py` no conteúdo existente para estabelecer baseline
2. Revise `references/brand_guidelines.md` para selecionar atributos de voz
3. Aplique a voz escolhida consistentemente em todo o conteúdo

### Para Criação de Conteúdo em Blog
1. Escolha um template de `references/content_frameworks.md`
2. Pesquise palavras-chave para o tema
3. Escreva o conteúdo seguindo a estrutura do template
4. Execute `scripts/seo_optimizer.py [arquivo] [palavra-chave-principal]` para otimizar
5. Aplique as recomendações antes de publicar

### Para Conteúdo em Redes Sociais
1. Revise as melhores práticas de plataforma em `references/social_media_optimization.md`
2. Use o template apropriado de `references/content_frameworks.md`
3. Otimize com base nas diretrizes específicas da plataforma
4. Agende usando `assets/content_calendar_template.md`

## Workflows Principais

### Estabelecendo Voz de Marca (Configuração Inicial)

Ao criar conteúdo para uma marca ou cliente novo:

1. **Analise Conteúdo Existente** (se disponível)
   ```bash
   python scripts/brand_voice_analyzer.py existing_content.txt
   ```
   
2. **Defina Atributos de Voz**
   - Revise arquétipos de personalidade de marca em `references/brand_guidelines.md`
   - Selecione arquétipos primários e secundários
   - Escolha 3-5 atributos de tom
   - Documente nas diretrizes de marca

3. **Crie Amostra de Voz**
   - Escreva 3 peças de amostra na voz escolhida
   - Teste a consistência usando o analisador
   - Refine com base nos resultados

### Criando Posts de Blog Otimizados para SEO

1. **Pesquisa de Palavras-chave**
   - Identifique palavra-chave primária (volume de busca 500-5000/mês)
   - Encontre 3-5 palavras-chave secundárias
   - Liste 10-15 palavras-chave LSI

2. **Estrutura de Conteúdo**
   - Use o template de blog de `references/content_frameworks.md`
   - Inclua a palavra-chave no título, primeiro parágrafo e 2-3 H2s
   - Apunte para 1.500-2.500 palavras para cobertura abrangente

3. **Verificação de Otimização**
   ```bash
   python scripts/seo_optimizer.py blog_post.md "palavra-chave principal" "palavras,chave,secundárias"
   ```

4. **Aplique Recomendações de SEO**
   - Ajuste a densidade de palavras-chave para 1-3%
   - Garanta estrutura adequada de headings
   - Adicione links internos e externos
   - Otimize meta description

### Criação de Conteúdo para Redes Sociais

1. **Seleção de Plataforma**
   - Identifique plataformas primárias com base no público
   - Revise diretrizes específicas de plataforma em `references/social_media_optimization.md`

2. **Adaptação de Conteúdo**
   - Comece com o post do blog ou mensagem principal
   - Use a matriz de repurposing de `references/content_frameworks.md`
   - Adapte para cada plataforma seguindo os templates

3. **Checklist de Otimização**
   - Comprimento apropriado para plataforma
   - Horário de postagem ideal
   - Dimensões de imagem corretas
   - Hashtags específicas da plataforma
   - Elementos de engajamento (pesquisas, perguntas)

### Planejamento de Calendário de Conteúdo

1. **Planejamento Mensal**
   - Copie `assets/content_calendar_template.md`
   - Defina metas e KPIs mensais
   - Identifique campanhas/temas principais

2. **Distribuição Semanal**
   - Siga a proporção de pilares de conteúdo 40/25/25/10
   - Equilibre plataformas ao longo da semana
   - Alinhe com horários de postagem ideais

3. **Criação em Lote**
   - Crie todo o conteúdo semanal em uma sessão
   - Mantenha voz consistente em todas as peças
   - Prepare todos os ativos visuais juntos

## Scripts Principais

### brand_voice_analyzer.py
Analisa conteúdo de texto quanto a características de voz, legibilidade e consistência.

**Uso**: `python scripts/brand_voice_analyzer.py <arquivo> [json|text]`

**Retorna**:
- Perfil de voz (formalidade, tom, perspectiva)
- Pontuação de legibilidade
- Análise de estrutura de sentenças
- Recomendações de melhoria

### seo_optimizer.py
Analisa conteúdo para otimização de SEO e fornece recomendações acionáveis.

**Uso**: `python scripts/seo_optimizer.py <arquivo> [palavra_chave_principal] [palavras_chave_secundárias]`

**Retorna**:
- Pontuação de SEO (0-100)
- Análise de densidade de palavras-chave
- Avaliação de estrutura
- Sugestões de meta tags
- Recomendações específicas de otimização

## Guias de Referência

### Quando Usar Cada Referência

**references/brand_guidelines.md**
- Configuração de nova voz de marca
- Garantia de consistência em conteúdo
- Treinamento de novos membros da equipe
- Resolução de questões de voz/tom

**references/content_frameworks.md**
- Início de qualquer novo conteúdo
- Estruturação de diferentes tipos de conteúdo
- Criação de templates de conteúdo
- Planejamento de repurposing de conteúdo

**references/social_media_optimization.md**
- Otimização específica por plataforma
- Desenvolvimento de estratégia de hashtags
- Compreensão de fatores de algoritmo
- Configuração de rastreamento de analytics

## Melhores Práticas

### Processo de Criação de Conteúdo
1. Sempre comece com necessidade/ponto de dor do público
2. Pesquise antes de escrever
3. Crie outline usando templates
4. Escreva primeiro rascunho sem editar
5. Otimize para SEO
6. Edite para voz de marca
7. Revise e verifique fatos
8. Otimize para plataforma
9. Agende estrategicamente

### Indicadores de Qualidade
- Pontuação de SEO acima de 75/100
- Legibilidade apropriada para público
- Voz de marca consistente ao longo do texto
- Proposta de valor clara
- Conclusões acionáveis
- Formatação visual adequada
- Otimizado para plataforma

### Armadilhas Comuns a Evitar
- Escrever sem pesquisar palavras-chave
- Ignorar requisitos específicos da plataforma
- Voz de marca inconsistente
- Otimização excessiva para SEO (keyword stuffing)
- Ausência de CTAs claros
- Publicar sem revisar
- Ignorar feedback de analytics

## Métricas de Desempenho

Rastreie estes KPIs para sucesso de conteúdo:

### Métricas de Conteúdo
- Crescimento de tráfego orgânico
- Tempo médio na página
- Taxa de rejeição
- Compartilhamentos sociais
- Backlinks conquistados

### Métricas de Engajamento
- Comentários e discussões
- Taxas de clique em email
- Taxa de engajamento em redes sociais
- Downloads de conteúdo
- Submissões de formulário

### Métricas de Negócio
- Leads gerados
- Taxa de conversão
- Custo de aquisição de cliente
- Atribuição de receita
- ROI por peça de conteúdo

## Pontos de Integração

Esta skill funciona melhor com:
- Plataformas de analytics (Google Analytics, insights de redes sociais)
- Ferramentas de SEO (para pesquisa de palavras-chave)
- Ferramentas de design (para conteúdo visual)
- Plataformas de agendamento (para distribuição de conteúdo)
- Sistemas de email marketing (para conteúdo de newsletter)

## Comandos Rápidos

```bash
# Analise voz de marca
python scripts/brand_voice_analyzer.py content.txt

# Otimize para SEO
python scripts/seo_optimizer.py article.md "palavra-chave principal"

# Verifique conteúdo contra diretrizes de marca
grep -f references/brand_guidelines.md content.txt

# Crie calendário mensal
cp assets/content_calendar_template.md this_month_calendar.md
```