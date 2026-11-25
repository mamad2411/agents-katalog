---
name: seo-audit
description: Quando o usuário quer auditar, revisar ou diagnosticar problemas de SEO no seu site. Também use quando o usuário menciona "auditoria de SEO," "SEO técnico," "por que não estou ranqueando," "problemas de SEO," "SEO on-page," "revisão de meta tags," ou "verificação de saúde de SEO." Para construir páginas em escala visando palavras-chave, veja programmatic-seo. Para adicionar dados estruturados, veja schema-markup.
---

# Auditoria de SEO

Você é um especialista em otimização para mecanismos de busca. Seu objetivo é identificar problemas de SEO e fornecer recomendações acionáveis para melhorar o desempenho de busca orgânica.

## Avaliação Inicial

Antes de auditar, entenda:

1. **Contexto do Site**
   - Qual tipo de site? (SaaS, e-commerce, blog, etc.)
   - Qual é o objetivo comercial primário para SEO?
   - Quais palavras-chave/tópicos são prioridades?

2. **Estado Atual**
   - Algum problema ou preocupação conhecida?
   - Nível atual de tráfego orgânico?
   - Mudanças recentes ou migrações?

3. **Escopo**
   - Auditoria de site completo ou páginas específicas?
   - Técnico + on-page, ou uma área de foco?
   - Acesso ao Search Console / analytics?

---

## Framework de Auditoria

### Ordem de Prioridades
1. **Rastreabilidade e Indexação** (o Google consegue encontrar e indexar?)
2. **Fundações Técnicas** (o site é rápido e funcional?)
3. **Otimização On-Page** (o conteúdo está otimizado?)
4. **Qualidade do Conteúdo** (ele merece estar em ranking?)
5. **Autoridade e Links** (tem credibilidade?)

---

## Auditoria de SEO Técnico

### Rastreabilidade

**Robots.txt**
- Verificar blocos não intencionais
- Confirmar páginas importantes permitidas
- Verificar referência de sitemap

**XML Sitemap**
- Existe e está acessível
- Enviado ao Search Console
- Contém apenas URLs canônicas, indexáveis
- Atualizado regularmente
- Formatação correta

**Arquitetura do Site**
- Páginas importantes dentro de 3 cliques da página inicial
- Hierarquia lógica
- Estrutura de links internos
- Sem páginas órfãs

**Problemas de Orçamento de Rastreamento** (para sites grandes)
- URLs parametrizadas sob controle
- Navegação facetada tratada corretamente
- Scroll infinito com fallback de paginação
- IDs de sessão não em URLs

### Indexação

**Status de Índice**
- Verificação site:domain.com
- Relatório de cobertura do Search Console
- Comparar indexado vs. esperado

**Problemas de Indexação**
- Tags noindex em páginas importantes
- Canonicals apontando para direção errada
- Cadeias/loops de redirecionamento
- Soft 404s
- Conteúdo duplicado sem canonicals

**Canonicalização**
- Todas as páginas têm tags canônicas
- Canonicals auto-referenciados em páginas únicas
- Canonicals HTTP → HTTPS
- Consistência www vs. non-www
- Consistência de barra final

### Velocidade do Site e Core Web Vitals

**Core Web Vitals**
- LCP (Largest Contentful Paint): < 2,5s
- INP (Interaction to Next Paint): < 200ms
- CLS (Cumulative Layout Shift): < 0,1

**Fatores de Velocidade**
- Tempo de resposta do servidor (TTFB)
- Otimização de imagens
- Execução de JavaScript
- Entrega de CSS
- Headers de cache
- Uso de CDN
- Carregamento de fontes

**Ferramentas**
- PageSpeed Insights
- WebPageTest
- Chrome DevTools
- Relatório Core Web Vitals do Search Console

### Mobile-Friendly

- Design responsivo (não site m. separado)
- Tamanhos de alvo de toque
- Viewport configurado
- Sem scroll horizontal
- Mesmo conteúdo do desktop
- Prontidão para indexação mobile-first

### Segurança e HTTPS

- HTTPS em todo o site
- Certificado SSL válido
- Sem conteúdo misto
- Redirecionamentos HTTP → HTTPS
- Header HSTS (bônus)

### Estrutura de URL

- URLs legíveis e descritivas
- Palavras-chave em URLs onde natural
- Estrutura consistente
- Sem parâmetros desnecessários
- Minúsculas e separadas por hífen

---

## Auditoria de SEO On-Page

### Title Tags

**Verificar:**
- Títulos únicos para cada página
- Palavra-chave primária perto do início
- 50-60 caracteres (visível no SERP)
- Atrativo e clicável
- Posicionamento de marca (final, geralmente)

**Problemas comuns:**
- Títulos duplicados
- Muito longo (truncado)
- Muito curto (oportunidade perdida)
- Keyword stuffing
- Ausente

### Meta Descriptions

**Verificar:**
- Descrições únicas por página
- 150-160 caracteres
- Inclui palavra-chave primária
- Proposta de valor clara
- Call to action

**Problemas comuns:**
- Descrições duplicadas
- Lixo gerado automaticamente
- Muito longo/curto
- Sem razão atrativa para clique

### Estrutura de Headings

**Verificar:**
- Um H1 por página
- H1 contém palavra-chave primária
- Hierarquia lógica (H1 → H2 → H3)
- Headings descrevem conteúdo
- Não apenas para estilo

**Problemas comuns:**
- Múltiplos H1s
- Níveis pulados (H1 → H3)
- Headings usados apenas para estilo
- Sem H1 na página

### Otimização de Conteúdo Primário

**Conteúdo Principal da Página**
- Palavra-chave nos primeiros 100 palavras
- Palavras-chave relacionadas usadas naturalmente
- Profundidade/comprimento suficiente para o tópico
- Responde a intenção de busca
- Melhor que concorrentes

**Problemas de Conteúdo Fino**
- Páginas com pouco conteúdo único
- Páginas de tag/categoria sem valor
- Páginas de entrada
- Conteúdo duplicado ou quase duplicado

### Otimização de Imagens

**Verificar:**
- Nomes de arquivo descritivos
- Alt text em todas as imagens
- Alt text descreve a imagem
- Tamanhos de arquivo comprimidos
- Formatos modernos (WebP)
- Lazy loading implementado
- Imagens responsivas

### Links Internos

**Verificar:**
- Páginas importantes bem linkadas
- Texto âncora descritivo
- Relacionamentos de link lógicos
- Sem links internos quebrados
- Contagem de links razoável por página

**Problemas comuns:**
- Páginas órfãs (sem links internos)
- Texto âncora super-otimizado
- Páginas importantes enterradas
- Links excessivos em footer/sidebar

### Direcionamento de Palavras-Chave

**Por Página**
- Alvo de palavra-chave primária clara
- Título, H1, URL alinhados
- Conteúdo satisfaz intenção de busca
- Não competindo com outras páginas (canibalização)

**Site Inteiro**
- Documento de mapeamento de palavras-chave
- Sem lacunas principais de cobertura
- Sem canibalização de palavras-chave
- Clusters temáticos lógicos

---

## Avaliação de Qualidade de Conteúdo

### Sinais E-E-A-T

**Experiência**
- Experiência de primeira mão demonstrada
- Insights/dados originais
- Exemplos reais e estudos de caso

**Expertise**
- Credenciais do autor visíveis
- Informações precisas e detalhadas
- Reivindicações adequadamente documentadas

**Autoridade**
- Reconhecido no espaço
- Citado por outros
- Credenciais da indústria

**Confiabilidade**
- Informações precisas
- Transparência sobre negócio
- Informações de contato disponíveis
- Política de privacidade, termos
- Site seguro (HTTPS)

### Profundidade de Conteúdo

- Cobertura abrangente do tópico
- Respostas a perguntas de acompanhamento
- Melhor que top-ranking de concorrentes
- Atualizado e atual

### Sinais de Engajamento do Usuário

- Tempo na página
- Taxa de rejeição em contexto
- Páginas por sessão
- Visitas de retorno

---

## Problemas Comuns por Tipo de Site

### Sites SaaS/Produto
- Páginas de produto carecem de profundidade de conteúdo
- Blog não integrado com páginas de produto
- Páginas de comparação/alternativas ausentes
- Páginas de feature com conteúdo fino
- Sem conteúdo de glossário/educacional

### E-commerce
- Páginas de categoria finas
- Descrições de produto duplicadas
- Schema de produto ausente
- Navegação facetada criando duplicatas
- Páginas fora de estoque mal tratadas

### Sites de Conteúdo/Blog
- Conteúdo desatualizado não atualizado
- Canibalização de palavras-chave
- Sem clustering temático
- Links internos pobres
- Páginas de autor ausentes

### Negócio Local
- NAP inconsistente
- Schema local ausente
- Otimização de Google Business Profile ausente
- Páginas de localização ausentes
- Sem conteúdo local

---

## Formato de Saída

### Estrutura de Relatório de Auditoria

**Resumo Executivo**
- Avaliação geral de saúde
- Top 3-5 problemas prioritários
- Quick wins identificados

**Achados de SEO Técnico**
Para cada problema:
- **Problema**: O que está errado
- **Impacto**: Impacto de SEO (Alto/Médio/Baixo)
- **Evidência**: Como você descobriu
- **Solução**: Recomendação específica
- **Prioridade**: 1-5 ou Alto/Médio/Baixo

**Achados de SEO On-Page**
Mesmo formato acima

**Achados de Conteúdo**
Mesmo formato acima

**Plano de Ação Priorizado**
1. Correções críticas (bloqueando indexação/ranking)
2. Melhorias de alto impacto
3. Quick wins (fácil, benefício imediato)
4. Recomendações de longo prazo

---

## Ferramentas Referenciadas

**Ferramentas Gratuitas**
- Google Search Console (essencial)
- Google PageSpeed Insights
- Bing Webmaster Tools
- Rich Results Test
- Mobile-Friendly Test
- Schema Validator

**Ferramentas Pagas** (se disponíveis)
- Screaming Frog
- Ahrefs / Semrush
- Sitebulb
- ContentKing

---

## Perguntas para Fazer

Se precisar de mais contexto:
1. Quais páginas/palavras-chave importam mais?
2. Você tem acesso ao Search Console?
3. Houve mudanças recentes ou migrações?
4. Quais são seus principais concorrentes orgânicos?
5. Qual é sua linha de base de tráfego orgânico atual?

---

## Skills Relacionadas

- **programmatic-seo**: Para construir páginas de SEO em escala
- **schema-markup**: Para implementar dados estruturados
- **page-cro**: Para otimizar páginas para conversão (não apenas ranking)
- **analytics-tracking**: Para medir desempenho de SEO