---
name: peer-review
description: "Kit sistemático de avaliação por pares. Avalie metodologia, estatística, desenho, reprodutibilidade, ética, integridade de figuras, padrões de relatório, para revisão de manuscritos e propostas de pesquisa em diferentes disciplinas."
allowed-tools: [Read, Write, Edit, Bash]
---

# Avaliação Crítica Científica e Revisão por Pares

## Visão Geral

Revisão por pares é um processo sistemático para avaliar manuscritos científicos. Avalie metodologia, estatística, desenho, reprodutibilidade, ética e padrões de relatório. Aplique esta habilidade para revisão de manuscritos e propostas de pesquisa em diferentes disciplinas com avaliação construtiva e rigorosa.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Conduzir revisão por pares de manuscritos científicos para periódicos
- Avaliar propostas de pesquisa e aplicações de financiamento
- Avaliar metodologia e rigor do desenho experimental
- Revisar análises estatísticas e padrões de relatório
- Avaliar reprodutibilidade e disponibilidade de dados
- Verificar conformidade com diretrizes de relatório (CONSORT, STROBE, PRISMA)
- Fornecer feedback construtivo sobre redação científica

## Aprimoramento Visual com Esquemáticos Científicos

**Ao criar documentos com esta habilidade, sempre considere adicionar diagramas e esquemáticos científicos para aprimorar a comunicação visual.**

Se seu documento ainda não contiver esquemáticos ou diagramas:
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade para publicação com IA
- Simplesmente descreva o diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará automaticamente o esquemático

**Para novos documentos:** Esquemáticos científicos devem ser gerados por padrão para representar visualmente conceitos-chave, fluxos de trabalho, arquiteturas ou relações descritas no texto.

**Como gerar esquemáticos:**
```bash
python scripts/generate_schematic.py "sua descrição de diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Acessibilidade garantida (amigável para daltônicos, alto contraste)
- Saída salva no diretório figures/

**Quando adicionar esquemáticos:**
- Diagramas de fluxo de trabalho de revisão por pares
- Árvores de decisão de critérios de avaliação
- Fluxogramas do processo de revisão
- Estruturas de avaliação de metodologia
- Visualizações de avaliação de qualidade
- Diagramas de conformidade com diretrizes de relatório
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemáticos, consulte a documentação da habilidade scientific-schematics.

---

## Fluxo de Trabalho de Revisão por Pares

Conduza revisão por pares sistematicamente através dos seguintes estágios, adaptando profundidade e foco baseado no tipo de manuscrito e disciplina.

### Estágio 1: Avaliação Inicial

Comece com uma avaliação de alto nível para determinar o escopo, novidade e qualidade geral do manuscrito.

**Questões-chave:**
- Qual é a questão de pesquisa central ou hipótese?
- Quais são os principais achados e conclusões?
- O trabalho é cientificamente sólido e significativo?
- O trabalho é apropriado para o local de publicação pretendido?
- Há alguma falha maior óbvia que impediria a publicação?

**Saída:** Resumo breve (2-3 frases) capturando a essência do manuscrito e impressão inicial.

### Estágio 2: Revisão Detalhada Seção por Seção

Conduza uma avaliação minuciosa de cada seção do manuscrito, documentando preocupações e forças específicas.

#### Resumo e Título
- **Precisão:** O resumo reflete com precisão o conteúdo e conclusões do estudo?
- **Clareza:** O título é específico, preciso e informativo?
- **Completude:** Os achados e métodos principais são resumidos apropriadamente?
- **Acessibilidade:** O resumo é compreensível para um público científico amplo?

#### Introdução
- **Contexto:** As informações de background são adequadas e atuais?
- **Justificativa:** A questão de pesquisa é claramente motivada e justificada?
- **Novidade:** A originalidade e significância do trabalho são claramente articuladas?
- **Literatura:** Estudos anteriores relevantes são apropriadamente citados?
- **Objetivos:** Os objetivos/hipóteses de pesquisa são claramente declarados?

#### Métodos
- **Reprodutibilidade:** Outro pesquisador conseguiria replicar o estudo a partir da descrição fornecida?
- **Rigor:** Os métodos são apropriados para abordar as questões de pesquisa?
- **Detalhe:** Protocolos, reagentes, equipamentos e parâmetros são suficientemente descritos?
- **Ética:** As aprovações éticas, consentimento e gerenciamento de dados são apropriadamente documentados?
- **Estatística:** Os métodos estatísticos são apropriados, claramente descritos e justificados?
- **Validação:** Controles, replicatas e abordagens de validação são adequados?

**Elementos críticos a verificar:**
- Tamanhos de amostra e cálculos de poder
- Procedimentos de aleatorização e cegamento
- Critérios de inclusão/exclusão
- Protocolos de coleta de dados
- Métodos computacionais e versões de software
- Testes estatísticos e correção para comparações múltiplas

#### Resultados
- **Apresentação:** Os resultados são apresentados de forma lógica e clara?
- **Figuras/Tabelas:** As visualizações são apropriadas, claras e adequadamente rotuladas?
- **Estatística:** Os resultados estatísticos são apropriadamente relatados (tamanhos de efeito, intervalos de confiança, valores-p)?
- **Objetividade:** Os resultados são apresentados sem sobre-interpretação?
- **Completude:** Todos os resultados relevantes são incluídos, incluindo resultados negativos?
- **Reprodutibilidade:** Dados brutos ou estatísticas resumidas são fornecidos?

**Problemas comuns a identificar:**
- Relatório seletivo de resultados
- Testes estatísticos inadequados
- Barras de erro ou medidas de variabilidade faltantes
- Sobre-ajuste ou análise circular
- Efeitos de lote ou variáveis de confundimento
- Controles ou experimentos de validação faltantes

#### Discussão
- **Interpretação:** As conclusões são apoiadas pelos dados?
- **Limitações:** As limitações do estudo são reconhecidas e discutidas?
- **Contexto:** Os achados são apropriadamente contextualizados na literatura existente?
- **Especulação:** A especulação é claramente distinguida das conclusões apoiadas por dados?
- **Significância:** As implicações e importância são claramente articuladas?
- **Direções futuras:** Próximos passos ou questões em aberto são discutidos?

**Sinais de alerta:**
- Conclusões exageradas
- Ignorar evidências contraditórias
- Afirmações causais de dados correlacionais
- Discussão inadequada de limitações
- Afirmações mecanísticas sem evidência mecanística

#### Referências
- **Completude:** Os principais artigos relevantes são citados?
- **Atualidade:** Estudos importantes recentes estão incluídos?
- **Equilíbrio:** Pontos de vista contrários são apropriadamente citados?
- **Precisão:** As citações são precisas e apropriadas?
- **Auto-citação:** Há auto-citação excessiva ou inadequada?

### Estágio 3: Rigor Metodológico e Estatístico

Avalie a qualidade técnica e rigor da pesquisa com atenção particular a armadilhas comuns.

**Avaliação Estatística:**
- Pressupostos estatísticos são atendidos (normalidade, independência, homocedasticidade)?
- Tamanhos de efeito são relatados junto com valores-p?
- Correção para testes múltiplos é aplicada apropriadamente?
- Intervalos de confiança são fornecidos?
- O tamanho da amostra é justificado com análise de poder?
- Testes paramétricos vs. não-paramétricos são escolhidos apropriadamente?
- Dados faltantes são tratados apropriadamente?
- Análises exploratórias vs. confirmatórias são distinguidas?

**Desenho Experimental:**
- Controles são apropriados e adequados?
- Replicação é suficiente (biológica e técnica)?
- Possíveis variáveis de confundimento são identificadas e controladas?
- Aleatorização é apropriadamente implementada?
- Procedimentos de cegamento são adequados?
- O desenho experimental é ideal para a questão de pesquisa?

**Computacional/Bioinformática:**
- Métodos computacionais são claramente descritos e justificados?
- Versões de software e parâmetros são documentados?
- Código é disponibilizado para reprodutibilidade?
- Algoritmos e modelos são apropriadamente validados?
- Pressupostos de métodos computacionais são atendidos?
- Correção de lote é aplicada apropriadamente?

### Estágio 4: Reprodutibilidade e Transparência

Avalie se a pesquisa atende aos padrões modernos para reprodutibilidade e ciência aberta.

**Disponibilidade de Dados:**
- Dados brutos são depositados em repositórios apropriados?
- Números de acesso são fornecidos para bancos de dados públicos?
- Restrições de compartilhamento de dados são justificadas (ex: privacidade de pacientes)?
- Formatos de dados são padrão e acessíveis?

**Código e Materiais:**
- Código de análise é disponibilizado (GitHub, Zenodo, etc.)?
- Materiais únicos são disponibilizados ou descritos suficientemente para recreação?
- Protocolos são detalhados em profundidade suficiente?

**Padrões de Relatório:**
- O manuscrito segue diretrizes de relatório específicas da disciplina (CONSORT, PRISMA, ARRIVE, MIAME, MINSEQE, etc.)?
- Veja `references/reporting_standards.md` para diretrizes comuns
- Todos os elementos da lista de verificação apropriada são abordados?

### Estágio 5: Apresentação de Figuras e Dados

Avalie a qualidade, clareza e integridade da visualização de dados.

**Verificações de Qualidade:**
- As figuras têm alta resolução e são claramente rotuladas?
- Os eixos estão apropriadamente rotulados com unidades?
- Barras de erro estão definidas (DP, EPM, IC)?
- Indicadores de significância estatística são explicados?
- Esquemas de cores são apropriados e acessíveis (amigáveis para daltônicos)?
- Barras de escala estão incluídas para imagens?
- A visualização de dados é apropriada para o tipo de dados?

**Verificações de Integridade:**
- Há sinais de manipulação de imagem (duplicações, emendas)?
- Western blots e géis são apropriadamente apresentados?
- Imagens representativas são verdadeiramente representativas?
- Todas as condições são mostradas (sem apresentação seletiva)?

**Clareza:**
- As figuras conseguem ficar sozinhas com suas legendas?
- A mensagem de cada figura é imediatamente clara?
- Há figuras ou painéis redundantes?
- Os dados seriam melhor apresentados como tabelas ou figuras?

### Estágio 6: Considerações Éticas

Verifique se a pesquisa atende aos padrões e diretrizes éticas.

**Sujeitos Humanos:**
- Aprovação de IRB/ética é documentada?
- Consentimento informado é descrito?
- Populações vulneráveis são apropriadamente protegidas?
- Privacidade de pacientes é adequadamente protegida?
- Conflitos de interesse potenciais são divulgados?

**Pesquisa Animal:**
- Aprovação de IACUC ou equivalente é documentada?
- Procedimentos são humanitários e justificados?
- Os 3Rs (reposição, redução, refinamento) são considerados?
- Métodos de eutanásia são apropriados?

**Integridade de Pesquisa:**
- Há preocupações com fabricação ou falsificação de dados?
- Autoria é apropriada e justificada?
- Interesses concorrentes são divulgados?
- Fonte de financiamento é divulgada?
- Há preocupações com plágio ou publicação duplicada?

### Estágio 7: Qualidade de Redação e Clareza

Avalie clareza, organização e acessibilidade do manuscrito.

**Estrutura e Organização:**
- O manuscrito é logicamente organizado?
- As seções fluem coerentemente?
- As transições entre ideias são claras?
- A narrativa é convincente e clara?

**Qualidade de Redação:**
- A linguagem é clara, precisa e concisa?
- Jargão e acrônimos são minimizados e definidos?
- Gramática e ortografia estão corretas?
- As frases são desnecessariamente complexas?
- A voz passiva é excessivamente usada?

**Acessibilidade:**
- Um não-especialista consegue entender os achados principais?
- Termos técnicos são explicados?
- A significância é clara para um público amplo?

## Estruturando Relatórios de Revisão por Pares

Organize feedback em uma estrutura hierárquica que prioriza questões e fornece orientação acionável.

### Declaração de Resumo

Forneça uma avaliação geral concisa (1-2 parágrafos):
- Sinopse breve da pesquisa
- Recomendação geral (aceitar, revisões menores, revisões maiores, rejeitar)
- Principais forças (2-3 pontos de bala)
- Principais fraquezas (2-3 pontos de bala)
- Avaliação final de significância e solidez

### Comentários Maiores

Liste questões críticas que impactam significativamente a validade, interpretabilidade ou significância do manuscrito. Numere esses sequencialmente para referência fácil.

**Comentários maiores tipicamente incluem:**
- Falhas metodológicas fundamentais
- Análises estatísticas inadequadas
- Conclusões não apoiadas ou exageradas
- Controles ou experimentos críticos faltantes
- Preocupações graves de reprodutibilidade
- Lacunas principais na cobertura de literatura
- Preocupações éticas

**Para cada comentário maior:**
1. Declare claramente a questão
2. Explique por que é problemática
3. Sugira soluções específicas ou experimentos adicionais
4. Indique se abordar é essencial para publicação

### Comentários Menores

Liste questões menos críticas que melhorariam clareza, completude ou apresentação. Numere esses sequencialmente.

**Comentários menores tipicamente incluem:**
- Rótulos ou legendas de figuras pouco claros
- Detalhes metodológicos faltantes
- Erros tipográficos ou gramaticais
- Sugestões para apresentação de dados melhorada
- Problemas menores de relatório estatístico
- Análises complementares que fortaleceriam conclusões
- Pedidos de clarificação

**Para cada comentário menor:**
1. Identifique a localização específica (seção, parágrafo, figura)
2. Declare a questão claramente
3. Sugira como abordá-la

### Comentários Específicos Linha-por-Linha (Opcional)

Para manuscritos que requerem feedback detalhado, forneça comentários específicos da seção ou linha-por-linha:
- Referencie números específicos de página/linha ou seções
- Observe erros factuais, declarações pouco claras ou citações faltantes
- Sugira edições específicas para clareza

### Questões para Autores

Liste questões específicas que necessitam clarificação:
- Detalhes metodológicos que não estão claros
- Resultados aparentemente contraditórios
- Informações faltantes necessárias para avaliar o trabalho
- Pedidos de dados ou análises adicionais

## Tom e Abordagem

Mantenha um tom construtivo, profissional e colegiado ao longo da revisão.

**Melhores Práticas:**
- **Seja construtivo:** Formule a crítica como oportunidades de melhoria
- **Seja específico:** Forneça exemplos concretos e sugestões acionáveis
- **Seja equilibrado:** Reconheça forças bem como fraquezas
- **Seja respeitoso:** Lembre-se de que autores investiram esforço significativo
- **Seja objetivo:** Foque na ciência, não nos cientistas
- **Seja minucioso:** Não negligencie questões, mas priorize apropriadamente
- **Seja claro:** Evite crítica ambígua ou vaga

**Evite:**
- Ataques pessoais ou linguagem dismissiva
- Sarcasmo ou condescendência
- Crítica vaga sem exemplos específicos
- Solicitar experimentos desnecessários além do escopo
- Exigir conformidade com preferências pessoais vs. melhores práticas
- Revelar sua identidade se a revisão for duplo-cega

## Considerações Especiais por Tipo de Manuscrito

### Artigos de Pesquisa Original
- Enfatize rigor, reprodutibilidade e novidade
- Avalie significância e impacto
- Verifique se conclusões são orientadas por dados
- Verifique para métodos completos e controles apropriados

### Revisões e Meta-análises
- Avalie abrangência da cobertura de literatura
- Avalie estratégia de busca e critérios de inclusão/exclusão
- Verifique abordagem sistemática e falta de viés
- Verifique análise crítica vs. mera sumarização
- Para meta-análises, avalie abordagem estatística e heterogeneidade

### Artigos de Métodos
- Enfatize validação e comparação com métodos existentes
- Avalie reprodutibilidade e disponibilidade de protocolos/código
- Avalie melhorias sobre abordagens existentes
- Verifique para detalhe suficiente para implementação

### Relatórios Breves/Cartas
- Adapte expectativas para brevidade
- Garanta que achados principais ainda sejam rigorosos e significativos
- Verifique se formato é apropriado para achados

### Pré-impressos
- Reconheça que esses não passaram por revisão por pares formal
- Podem ser menos polidos que submissões para periódicos
- Ainda aplique padrões rigorosos para validade científica
- Considere fornecer feedback construtivo para ajudar autores a melhorar antes de submissão para periódico

### Apresentações e Decks de Slides

**⚠️ CRÍTICO: Para apresentações, NUNCA leia o PDF diretamente. SEMPRE converta para imagens primeiro.**

Ao revisar apresentações científicas (PowerPoint, Beamer, decks de slides):

#### Fluxo de Trabalho de Revisão Obrigatório Baseado em Imagens

**NUNCA tente ler PDFs de apresentações diretamente** - isso causa erros de overflow de buffer e não mostra problemas de formatação visual.

**Processo Obrigatório:**
1. Converta PDF para imagens usando Python:
   ```bash
   python skills/scientific-slides/scripts/pdf_to_images.py presentation.pdf review/slide --dpi 150
   # Cria: review/slide-001.jpg, review/slide-002.jpg, etc.
   ```
2. Leia e inspecione CADA arquivo de imagem de slide sequencialmente
3. Documente questões com números de slide específicos
4. Forneça feedback sobre formatação visual e conteúdo

**Imprima ao iniciar revisão:**
```
[HH:MM:SS] PEER REVIEW: Apresentação detectada - convertendo para imagens para revisão
[HH:MM:SS] PDF REVIEW: NUNCA lendo PDF diretamente - usando inspeção baseada em imagem
```

#### Critérios de Avaliação Específicos para Apresentação

**Design Visual e Legibilidade:**
- [ ] Texto é grande o suficiente (mínimo 18pt, idealmente 24pt+ para texto corpo)
- [ ] Alto contraste entre texto e background (4.5:1 mínimo, 7:1 preferível)
- [ ] Esquema de cores é profissional e acessível para daltônicos
- [ ] Design visual consistente em todos os slides
- [ ] Espaço em branco é adequado (não apertado)
- [ ] Fontes são claras e profissionais

**Layout e Formatação (Verificar CADA Imagem de Slide):**
- [ ] Sem overflow ou truncamento de texto nas bordas do slide
- [ ] Sem sobreposição de elementos (texto sobre imagens, formas sobrepostas)
- [ ] Títulos estão consistentemente posicionados
- [ ] Conteúdo está apropriadamente alinhado
- [ ] Bullets e texto não estão cortados
- [ ] Figuras cabem dentro dos limites do slide
- [ ] Legendas e rótulos estão visíveis e legíveis

**Qualidade do Conteúdo:**
- [ ] Uma ideia principal por slide (não sobrecarregado)
- [ ] Texto mínimo (máximo 3-6 bullets por slide)
- [ ] Pontos de bala são concisos (5-7 palavras cada)
- [ ] Figuras são simplificadas e claras (não copiar-colar de artigos)
- [ ] Visualizações de dados têm rótulos grandes e legíveis
- [ ] Citações estão presentes e apropriadamente formatadas
- [ ] Slides de resultados/dados dominam a apresentação (40-50% do conteúdo)

**Estrutura e Fluxo:**
- [ ] Arco narrativo claro (introdução → métodos → resultados → discussão)
- [ ] Progressão lógica entre slides
- [ ] Contagem de slides apropriada para duração da palestra (~1 slide por minuto)
- [ ] Slide de título inclui autores, afiliação, data
- [ ] Introdução cita literatura de background relevante (3-5 artigos)
- [ ] Discussão cita artigos de comparação (3-5 artigos)
- [ ] Slide de conclusões resume achados principais
- [ ] Slide de agradecimentos/financiamento no final

**Conteúdo Científico:**
- [ ] Questão de pesquisa está claramente declarada
- [ ] Métodos adequadamente sumarizados (não excesso de detalhe)
- [ ] Resultados apresentados logicamente com visualizações claras
- [ ] Significância estatística indicada apropriadamente
- [ ] Conclusões apoiadas por dados mostrados
- [ ] Limitações reconhecidas onde apropriado
- [ ] Direções futuras ou impacto mais amplo discutido

**Problemas Comuns em Apresentação a Sinalizar:**

**Questões Críticas (Devem Ser Corrigidas):**
- Overflow de texto tornando conteúdo ilegível
- Tamanhos de fonte muito pequenos (<18pt)
- Sobreposição de elementos obscurecendo dados
- Contraste insuficiente (texto difícil de ler)
- Figuras muito complexas ou ilegíveis
- Sem citações (afirmações completamente não apoiadas)
- Contagem de slides drasticamente inadequada para duração

**Questões Maiores (Deveriam Ser Corrigidas):**
- Design inconsistente entre slides
- Muito texto (blocos de texto, não bullets)
- Figuras mal simplificadas (rótulos de eixos muito pequenos)
- Layout apertado com espaço em branco insuficiente
- Elementos estruturais-chave faltantes (sem slide de conclusão)
- Escolhas de cores inadequadas (não seguras para daltônicos)
- Conteúdo de resultados mínimo (<30% de slides)

**Questões Menores (Sugestões de Melhoria):**
- Poderia usar mais visuais/diagramas
- Alguns slides ligeiramente texto-pesados
- Pequenas inconsistências de alinhamento
- Poderia se beneficiar de mais espaço em branco
- Citações adicionais fortaleceriam afirmações
- Esquema de cores poderia ser mais moderno

#### Formato de Relatório de Revisão para Apresentações

**Declaração de Resumo:**
- Impressão geral da qualidade de apresentação
- Apropriação para audiência alvo e duração
- Principais forças (design visual, conteúdo, clareza)
- Principais fraquezas (problemas de formatação, lacunas de conteúdo)
- Recomendação (pronto para apresentar, revisões menores, revisões maiores)

**Problemas de Layout e Formatação (Por Número de Slide):**
```
Slide 3: Overflow de texto - ponto de bala 4 se estende além da margem direita
Slide 7: Sobreposição de elementos - figura sobrepõe texto de legenda
Slide 12: Tamanho de fonte - rótulos de eixos muito pequenos para ler à distância
Slide 18: Alinhamento - título não centralizado
```

**Feedback de Conteúdo e Estrutura:**
- Adequação de contexto de background e citações
- Clareza de questão de pesquisa e objetivos
- Qualidade de sumarização de métodos
- Eficácia de apresentação de resultados
- Força de conclusões e implicações

**Design e Acessibilidade:**
- Apelo visual geral e profissionalismo
- Contraste de cor e legibilidade
- Acessibilidade para daltônicos
- Consistência entre slides

**Timing e Escopo:**
- Se contagem de slides corresponde à duração pretendida
- Nível apropriado de detalhe para tipo de palestra
- Equilíbrio entre seções

#### Exemplo de Processo de Revisão Baseado em Imagem

```
[14:30:00] PEER REVIEW: Iniciando revisão de apresentação
[14:30:05] PEER REVIEW: Apresentação detectada - convertendo para imagens
[14:30:10] PDF REVIEW: Executando pdf_to_images.py em presentation.pdf
[14:30:15] PDF REVIEW: 25 slides convertidos para imagens no diretório review/
[14:30:20] PDF REVIEW: Inspecionando slide 1/25 - slide de título
[14:30:25] PDF REVIEW: Inspecionando slide 2/25 - introdução
...
[14:35:40] PDF REVIEW: Inspecionando slide 25/25 - agradecimentos
[14:35:45] PDF REVIEW: Revisão baseada em imagem concluída
[14:35:50] PEER REVIEW: Encontrados 8 problemas de layout, 3 problemas de conteúdo
[14:35:55] PEER REVIEW: Gerando feedback estruturado por número de slide
```

**Lembre-se:** Para apresentações, a inspeção visual via imagens é OBRIGATÓRIA. Nunca tente ler PDFs de apresentações como texto - falhará e perderá todos os problemas de formatação visual.

## Recursos

Esta habilidade inclui materiais de referência para apoiar revisão por pares abrangente:

### references/reporting_standards.md
Diretrizes para principais padrões de relatório em disciplinas (CONSORT, PRISMA, ARRIVE, MIAME, STROBE, etc.) para avaliar completude de relatório de métodos e resultados.

### references/common_issues.md
Catálogo de questões metodológicas e estatísticas frequentes encontradas em revisão por pares, com orientação sobre identificação e abordagem.

## Lista de Verificação Final

Antes de finalizar a revisão, verifique:

- [ ] Declaração de resumo claramente transmite avaliação geral
- [ ] Preocupações maiores são claramente identificadas e justificadas
- [ ] Revisões sugeridas são específicas e acionáveis
- [ ] Questões menores são anotadas mas apropriadamente categorizadas
- [ ] Métodos estatísticos foram avaliados
- [ ] Reprodutibilidade e disponibilidade de dados avaliadas
- [ ] Considerações éticas verificadas
- [ ] Figuras e tabelas avaliadas para qualidade e integridade
- [ ] Qualidade de redação avaliada
- [ ] Tom é construtivo e profissional ao longo
- [ ] Revisão é minuciosa mas proporcional ao escopo do manuscrito
- [ ] Recomendação é consistente com questões identificadas