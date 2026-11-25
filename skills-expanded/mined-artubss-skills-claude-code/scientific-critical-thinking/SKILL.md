---
name: scientific-critical-thinking
description: "Avalie o rigor da pesquisa. Avalie metodologia, desenho experimental, validade estatística, vieses, confundimento e qualidade da evidência (GRADE, Cochrane ROB) para análise crítica de afirmações científicas."
allowed-tools: [Read, Write, Edit, Bash]
---

# Pensamento Crítico Científico

## Visão Geral

O pensamento crítico é um processo sistemático para avaliar o rigor científico. Avalie metodologia, desenho experimental, validade estatística, vieses, confundimento e qualidade da evidência usando frameworks GRADE e Cochrane ROB. Aplique essa habilidade para análise crítica de afirmações científicas.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:
- Avaliar metodologia de pesquisa e desenho experimental
- Avaliar validade estatística e qualidade da evidência
- Identificar vieses e confundimento em estudos
- Revisar afirmações científicas e conclusões
- Conduzir revisões sistemáticas ou meta-análises
- Aplicar avaliações GRADE ou Cochrane de risco de viés
- Fornecer análise crítica de artigos de pesquisa

## Aprimoramento Visual com Esquemáticos Científicos

**Ao criar documentos com essa habilidade, sempre considere adicionar diagramas e esquemáticos científicos para melhorar a comunicação visual.**

Se seu documento ainda não contém esquemáticos ou diagramas:
- Use a habilidade **scientific-schematics** para gerar diagramas de qualidade para publicação com inteligência artificial
- Simplesmente descreva seu diagrama desejado em linguagem natural
- Nano Banana Pro gerará automaticamente, revisará e refinará o esquemático

**Para novos documentos:** Esquemáticos científicos devem ser gerados por padrão para representar visualmente conceitos-chave, workflows, arquiteturas ou relacionamentos descritos no texto.

**Como gerar esquemáticos:**
```bash
python scripts/generate_schematic.py "sua descrição de diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação adequada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltonismo, alto contraste)
- Salvamento de saídas no diretório figures/

**Quando adicionar esquemáticos:**
- Diagramas de framework de pensamento crítico
- Árvores de decisão para identificação de vieses
- Fluxogramas de avaliação de qualidade da evidência
- Diagramas de metodologia de avaliação GRADE
- Frameworks de avaliação de risco de viés
- Visualizações de avaliação de validade
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemáticos, consulte a documentação da habilidade scientific-schematics.

---

## Capacidades Principais

### 1. Crítica de Metodologia

Avalie metodologia de pesquisa quanto ao rigor, validade e falhas potenciais.

**Aplique quando:**
- Revisar artigos de pesquisa
- Avaliar desenhos experimentais
- Avaliar protocolos de estudo
- Planejar nova pesquisa

**Framework de avaliação:**

1. **Avaliação do Desenho do Estudo**
   - O desenho é apropriado para a questão de pesquisa?
   - O desenho pode sustentar as afirmações causais sendo feitas?
   - Os grupos de comparação são apropriados e adequados?
   - Considere se o desenho experimental, quase-experimental ou observacional é justificado

2. **Análise de Validade**
   - **Validade interna:** Podemos confiar na inferência causal?
     - Verifique a qualidade da randomização
     - Avalie o controle de confundimento
     - Avalie viés de seleção
     - Revise padrões de atrito/abandono
   - **Validade externa:** Os resultados se generalizam?
     - Avalie representatividade da amostra
     - Considere validade ecológica do cenário
     - Avalie se as condições correspondem à aplicação alvo
   - **Validade de construto:** As medidas capturam os construtos pretendidos?
     - Revise validação de medida
     - Verifique definições operacionais
     - Avalie se as medidas são diretas ou proxies
   - **Validade de conclusão estatística:** As inferências estatísticas são válidas?
     - Verifique poder adequado/tamanho de amostra
     - Verifique conformidade com suposições
     - Avalie adequação do teste

3. **Controle e Cegamento**
   - A randomização foi implementada corretamente (geração de sequência, ocultação de alocação)?
   - O cegamento era viável e foi implementado (participantes, provedores, avaliadores)?
   - Os grupos controle são apropriados (placebo, controle ativo, sem tratamento)?
   - O viés de desempenho ou detecção poderia afetar resultados?

4. **Qualidade de Medição**
   - Os instrumentos são validados e confiáveis?
   - As medidas são objetivas quando possível, ou subjetivas com limitações reconhecidas?
   - A avaliação de desfecho é padronizada?
   - Múltiplas medidas são usadas para triangular achados?

**Referência:** Veja `references/scientific_method.md` para princípios detalhados e `references/experimental_design.md` para checklist abrangente de desenho.

### 2. Detecção de Vieses

Identifique e avalie fontes potenciais de viés que poderiam distorcer achados.

**Aplique quando:**
- Revisar pesquisa publicada
- Desenhar novos estudos
- Interpretar evidência conflitante
- Avaliar qualidade da pesquisa

**Revisão sistemática de viés:**

1. **Vieses Cognitivos (Pesquisador)**
   - **Viés de confirmação:** Apenas achados apoiadores são destacados?
   - **HARKing:** Hipóteses foram afirmadas a priori ou formadas após ver resultados?
   - **Viés de publicação:** Resultados negativos faltam na literatura?
   - **Cherry-picking:** Evidência é selecionada para relatório?
   - Verifique preregistro e transparência do plano de análise

2. **Vieses de Seleção**
   - **Viés de amostragem:** A amostra é representativa da população alvo?
   - **Viés de voluntário:** Participantes se autosselecionam de formas sistemáticas?
   - **Viés de atrito:** O abandono é diferencial entre grupos?
   - **Viés de sobrevivência:** Apenas "sobreviventes" são visíveis na amostra?
   - Examine diagramas de fluxo de participantes e compare características basais

3. **Vieses de Medição**
   - **Viés do observador:** Expectativas poderiam influenciar observações?
   - **Viés de recordação:** Relatos retrospectivos são sistematicamente imprecisos?
   - **Deseabilidade social:** As respostas são enviesadas para aceitabilidade?
   - **Viés de instrumento:** Ferramentas de medição sistematicamente erram?
   - Avalie cegamento, validação e objetividade de medição

4. **Vieses de Análise**
   - **P-hacking:** Múltiplas análises foram conduzidas até significância emergir?
   - **Troca de desfecho:** Desfechos não significativos foram substituídos por significativos?
   - **Relatório seletivo:** Todas as análises planejadas são relatadas?
   - **Pesca por subgrupos:** Análises de subgrupo foram conduzidas sem correção?
   - Verifique registro de estudo e compare com desfechos publicados

5. **Confundimento**
   - Que variáveis poderiam afetar tanto exposição quanto desfecho?
   - Os confundidores foram medidos e controlados (estatisticamente ou por desenho)?
   - O confundimento não medido poderia explicar achados?
   - Existem explicações alternativas plausíveis?

**Referência:** Veja `references/common_biases.md` para taxonomia abrangente de viés com estratégias de detecção e mitigação.

### 3. Avaliação de Análise Estatística

Avalie criticamente métodos, interpretação e relatório estatísticos.

**Aplique quando:**
- Revisar pesquisa quantitativa
- Avaliar afirmações orientadas por dados
- Avaliar resultados de ensaios clínicos
- Revisar meta-análises

**Checklist de revisão estatística:**

1. **Tamanho de Amostra e Poder**
   - Uma análise de poder a priori foi conduzida?
   - O tamanho é adequado para detectar efeitos significativos?
   - O estudo é sub-alimentado (problema comum)?
   - Resultados significativos de amostras pequenas levantam questões sobre tamanhos de efeito inflados?

2. **Testes Estatísticos**
   - Os testes são apropriados para tipo de dado e distribuição?
   - As suposições do teste foram verificadas e atendidas?
   - Testes paramétricos são justificados, ou alternativas não-paramétricas deveriam ser usadas?
   - A análise é correspondida ao desenho do estudo (ex.: pareado vs. independente)?

3. **Comparações Múltiplas**
   - Múltiplas hipóteses foram testadas?
   - Correção foi aplicada (Bonferroni, FDR, outro)?
   - Desfechos primários se distinguem de secundários/exploratórios?
   - Achados poderiam ser falsos positivos de múltiplos testes?

4. **Interpretação de Valor-P**
   - Valores-p são interpretados corretamente (probabilidade de dados se nulo é verdadeiro)?
   - Não-significância é incorretamente interpretada como "sem efeito"?
   - Significância estatística é confundida com importância prática?
   - Valores-p exatos são relatados, ou apenas "p < .05"?
   - Existe agrupamento suspeito logo abaixo de .05?

5. **Tamanhos de Efeito e Intervalos de Confiança**
   - Tamanhos de efeito são relatados junto com significância?
   - Intervalos de confiança são fornecidos para mostrar precisão?
   - O tamanho do efeito é significativo em termos práticos?
   - Tamanhos de efeito padronizados são interpretados com contexto específico do campo?

6. **Dados Faltantes**
   - Quanto dado falta?
   - O mecanismo de dados faltantes é considerado (MCAR, MAR, MNAR)?
   - Como dados faltantes são tratados (deleção, imputação, máxima verossimilhança)?
   - Dados faltantes poderiam enviesear resultados?

7. **Regressão e Modelagem**
   - O modelo é overfitted (muitos preditores, sem validação cruzada)?
   - Predições são feitas fora do intervalo dos dados (extrapolação)?
   - Problemas de multicolinearidade são endereçados?
   - Suposições do modelo são verificadas?

8. **Armadilhas Comuns**
   - Correlação tratada como causalidade
   - Ignorar regressão à média
   - Negligência de taxa base
   - Falácia do atirador do Texas (busca de padrão em ruído)
   - Paradoxo de Simpson (confundimento por subgrupos)

**Referência:** Veja `references/statistical_pitfalls.md` para armadilhas detalhadas e práticas corretas.

### 4. Avaliação de Qualidade da Evidência

Avalie sistematicamente a força e qualidade da evidência.

**Aplique quando:**
- Pesar evidência para decisões
- Conduzir revisões de literatura
- Comparar achados conflitantes
- Determinar confiança em conclusões

**Framework de avaliação de evidência:**

1. **Hierarquia de Desenho de Estudo**
   - Revisões sistemáticas/meta-análises (maior para efeitos de intervenção)
   - Ensaios clínicos randomizados
   - Estudos de coorte
   - Estudos caso-controle
   - Estudos transversais
   - Séries de casos/relatos
   - Opinião de especialista (menor)

   **Importante:** Desenhos de nível mais alto nem sempre são melhor qualidade. Um estudo observacional bem-desenhado pode ser mais forte que um RCT mal conduzido.

2. **Qualidade Dentro do Tipo de Desenho**
   - Avaliação de risco de viés (use ferramenta apropriada: Cochrane ROB, Newcastle-Ottawa, etc.)
   - Rigor metodológico
   - Completude de transparência e relatório
   - Conflitos de interesse

3. **Considerações GRADE (se aplicável)**
   - Comece com tipo de desenho (RCT = alto, observacional = baixo)
   - **Rebaixe por:**
     - Risco de viés
     - Inconsistência entre estudos
     - Indiretude (população/intervenção/desfecho errados)
     - Imprecisão (intervalos de confiança amplos, amostras pequenas)
     - Viés de publicação
   - **Eleve por:**
     - Tamanhos de efeito grandes
     - Relacionamentos dose-resposta
     - Confundidores que reduziriam (não aumentariam) efeito

4. **Convergência de Evidência**
   - **Mais forte quando:**
     - Múltiplas replicações independentes
     - Diferentes grupos de pesquisa e cenários
     - Diferentes metodologias convergem para mesma conclusão
     - Evidência mecanicista e empírica se alinham
   - **Mais fraca quando:**
     - Estudo único ou grupo de pesquisa
     - Achados contraditórios na literatura
     - Viés de publicação evidente
     - Nenhuma tentativa de replicação

5. **Fatores Contextuais**
   - Plausibilidade biológica/teórica
   - Consistência com conhecimento estabelecido
   - Temporalidade (causa precede efeito)
   - Especificidade do relacionamento
   - Força da associação

**Referência:** Veja `references/evidence_hierarchy.md` para hierarquia detalhada, sistema GRADE e ferramentas de avaliação de qualidade.

### 5. Identificação de Falácia Lógica

Detecte e nomeie erros lógicos em argumentos e afirmações científicas.

**Aplique quando:**
- Avaliar afirmações científicas
- Revisar seções de discussão/conclusão
- Avaliar comunicação de ciência popular
- Identificar raciocínio falho

**Falácias comuns em ciência:**

1. **Falácias de Causalidade**
   - **Post hoc ergo propter hoc:** "B seguiu A, então A causou B"
   - **Correlação = causalidade:** Confundir associação com causalidade
   - **Causalidade reversa:** Confundir causa com efeito
   - **Falácia de causa única:** Atribuir desfechos complexos a um fator

2. **Falácias de Generalização**
   - **Generalização precipitada:** Conclusões amplas de amostras pequenas
   - **Falácia anedótica:** Histórias pessoais como prova
   - **Cherry-picking:** Seleção apenas de evidência de apoio
   - **Falácia ecológica:** Padrões de grupo aplicados a indivíduos

3. **Falácias de Autoridade e Fonte**
   - **Apelo à autoridade:** "Especialista disse, então é verdadeiro" (sem evidência)
   - **Ad hominem:** Atacar pessoa, não argumento
   - **Falácia genética:** Julgar pela origem, não méritos
   - **Apelo à natureza:** "Natural = bom/seguro"

4. **Falácias Estatísticas**
   - **Negligência de taxa base:** Ignorar probabilidade anterior
   - **Atirador do Texas:** Encontrar padrões em dados aleatórios
   - **Comparações múltiplas:** Não corrigir por múltiplos testes
   - **Falácia do promotor:** Confundir P(E|H) com P(H|E)

5. **Falácias Estruturais**
   - **Falsa dicotomia:** "Ou A ou B" quando mais opções existem
   - **Deslocamento de meta:** Mudar padrões de evidência após atendê-los
   - **Petição de princípio:** Raciocínio circular
   - **Espantalho:** Malrepresentar argumentos para atacá-los

6. **Falácias Específicas de Ciência**
   - **Apelo a Galileu:** "Riram de Galileu, então minha ideia fringe está correta"
   - **Argumento da ignorância:** "Não comprovado falso, então verdadeiro"
   - **Falácia do Nirvana:** Rejeitar soluções imperfeitas
   - **Infalsabilidade:** Fazer afirmações não testáveis

**Ao identificar falácias:**
- Nomeie a falácia específica
- Explique por que o raciocínio é falho
- Identifique que evidência seria necessária para inferência válida
- Note que raciocínio falacioso não prova a conclusão falsa—apenas que este argumento não a sustenta

**Referência:** Veja `references/logical_fallacies.md` para catálogo abrangente de falácias com exemplos e estratégias de detecção.

### 6. Orientação sobre Desenho de Pesquisa

Forneça orientação construtiva para planejar estudos rigorosos.

**Aplique quando:**
- Ajudar a desenhar novos experimentos
- Planejar projetos de pesquisa
- Revisar propostas de pesquisa
- Melhorar protocolos de estudo

**Processo de desenho:**

1. **Refinamento de Questão de Pesquisa**
   - Garanta que a questão seja específica, respondível e falsificável
   - Verifique se endereça lacuna ou contradição na literatura
   - Confirme viabilidade (recursos, ética, tempo)
   - Defina variáveis operacionalmente

2. **Seleção de Desenho**
   - Corresponda desenho à questão (causal → experimental; associacional → observacional)
   - Considere viabilidade e restrições éticas
   - Escolha entre desenhos de entre-sujeitos, dentro-sujeitos ou mistos
   - Planeje desenhos fatoriais se testando múltiplos fatores

3. **Estratégia de Minimização de Viés**
   - Implemente randomização quando possível
   - Planeje cegamento em todos os níveis viáveis (participantes, provedores, avaliadores)
   - Identifique e planeje para controlar confundidores (randomização, pareamento, estratificação, ajuste estatístico)
   - Padronize todos os procedimentos
   - Planeje minimizar atrito

4. **Planejamento de Amostra**
   - Conduza análise de poder a priori (especifique efeito esperado, poder desejado, alpha)
   - Considere atrito no tamanho de amostra
   - Defina critérios claros de inclusão/exclusão
   - Considere estratégia de recrutamento e viabilidade
   - Planeje para representatividade de amostra

5. **Estratégia de Medição**
   - Selecione instrumentos validados e confiáveis
   - Use medidas objetivas quando possível
   - Planeje múltiplas medidas de construtos-chave (triangulação)
   - Garanta que medidas sejam sensíveis a mudanças esperadas
   - Estabeleça procedimentos de confiabilidade entre avaliadores

6. **Planejamento de Análise**
   - Pré-especifique todas as hipóteses e análises
   - Designe desfecho primário claramente
   - Planeje testes estatísticos com verificação de suposições
   - Especifique como dados faltantes serão tratados
   - Planeje relatar tamanhos de efeito e intervalos de confiança
   - Considere correções para comparações múltiplas

7. **Transparência e Rigor**
   - Pré-registre estudo e plano de análise
   - Use diretrizes de relatório (CONSORT, STROBE, PRISMA)
   - Planeje relatar todos os desfechos, não apenas significativos
   - Distinga achados confirmatórios de exploratórios
   - Comprometa-se com compartilhamento de dados/código

**Referência:** Veja `references/experimental_design.md` para checklist de desenho abrangente cobrindo todos os estágios de questão para disseminação.

### 7. Avaliação de Afirmação

Avalie sistematicamente afirmações científicas quanto à validade e apoio.

**Aplique quando:**
- Avaliar conclusões em artigos
- Avaliar relatórios de mídia sobre pesquisa
- Revisar afirmações de resumo ou introdução
- Verificar se dados sustentam conclusões

**Processo de avaliação de afirmação:**

1. **Identifique a Afirmação**
   - Exatamente o quê está sendo afirmado?
   - É uma afirmação causal, associacional ou descritiva?
   - Qual a força da afirmação (comprovado, provável, sugerido, possível)?

2. **Avalie a Evidência**
   - Que evidência é fornecida?
   - A evidência é direta ou indireta?
   - A evidência é suficiente para a força da afirmação?
   - Explicações alternativas são descartadas?

3. **Verifique Conexão Lógica**
   - Conclusões seguem dos dados?
   - Existem saltos lógicos?
   - Dados correlacionais são usados para sustentar afirmações causais?
   - Limitações são reconhecidas?

4. **Avalie Proporcionalidade**
   - A confiança é proporcional à força da evidência?
   - Palavras de ressalva são usadas apropriadamente?
   - Limitações são subestimadas?
   - Especulação é claramente rotulada?

5. **Verifique Sobregeneralização**
   - Afirmações se estendem além da amostra estudada?
   - Restrições de população são reconhecidas?
   - Dependência de contexto é reconhecida?
   - Ressalvas sobre generalização são incluídas?

6. **Sinais de Alerta**
   - Linguagem causal de estudos correlacionais
   - "Prova" ou certeza absoluta
   - Citações selecionadas
   - Ignorar evidência contraditória
   - Descartar limitações
   - Extrapolação além dos dados

**Forneça feedback específico:**
- Cite a afirmação problemática
- Explique que evidência seria necessária para sustentá-la
- Sugira linguagem apropriada de ressalva se garantido
- Distinga entre dados (o que foi encontrado) e interpretação (o que significa)

## Diretrizes de Aplicação

### Abordagem Geral

1. **Seja Construtivo**
   - Identifique pontos fortes bem como fraquezas
   - Sugira melhorias ao invés de apenas criticar
   - Distinga entre falhas fatais e limitações menores
   - Reconheça que toda pesquisa tem limitações

2. **Seja Específico**
   - Aponte instâncias específicas (ex.: "Tabela 2 mostra..." ou "Na seção de Métodos...")
   - Cite declarações problemáticas
   - Forneça exemplos concretos de questões
   - Referencie princípios específicos ou padrões violados

3. **Seja Proporcional**
   - Corresponda severidade de crítica à importância do assunto
   - Distinga entre ameaças principais à validade e preocupações menores
   - Considere se problemas afetam conclusões primárias
   - Reconheça incerteza em suas próprias avaliações

4. **Aplique Padrões Consistentes**
   - Use mesmos critérios em todos os estudos
   - Não aplique padrões mais rigorosos a achados que você desgosta
   - Reconheça seus próprios vieses potenciais
   - Base julgamentos em metodologia, não resultados

5. **Considere Contexto**
   - Reconheça restrições práticas e éticas
   - Considere normas específicas do campo para tamanhos de efeito e métodos
   - Reconheça contextos exploratórios vs. confirmatórios
   - Considere limitações de recurso na avaliação de estudos

### Ao Fornecer Crítica

**Estruture feedback como:**

1. **Resumo:** Visão geral breve do que foi avaliado
2. **Pontos Fortes:** O que foi bem feito (importante para credibilidade e aprendizado)
3. **Preocupações:** Questões organizadas por severidade
   - Questões críticas (ameaçam validade de conclusões principais)
   - Questões importantes (afetam interpretação mas não fatalmente)
   - Questões menores (vale notar mas não mudam conclusões)
4. **Recomendações Específicas:** Sugestões acionáveis para melhoria
5. **Avaliação Geral:** Conclusão equilibrada sobre qualidade de evidência e o que pode ser concluído

**Use terminologia precisa:**
- Nomeie vieses, falácias e questões metodológicas específicas
- Referencie padrões e diretrizes estabelecidas
- Cite princípios de metodologia científica
- Use termos técnicos com precisão

### Quando Incerto

- **Reconheça incerteza:** "Isso poderia ser X ou Y; informação adicional necessária é Z"
- **Faça perguntas esclarecedoras:** "Foi feito [detalhe metodológico]? Isso afeta interpretação."
- **Forneça avaliações condicionais:** "Se X foi feito, então Y segue; se não, então Z é questão"
- **Note qual informação adicional resolveria incerteza**

## Materiais de Referência

Esta habilidade inclui materiais de referência abrangentes que fornecem frameworks detalhados para avaliação crítica:

- **`references/scientific_method.md`** - Princípios centrais da metodologia científica, o processo científico, critérios de avaliação crítica, sinais de alerta em afirmações científicas, padrões de inferência causal, revisão por pares e princípios de ciência aberta

- **`references/common_biases.md`** - Taxonomia abrangente de vieses cognitivos, experimentais, metodológicos, estatísticos e de análise com estratégias de detecção e mitigação

- **`references/statistical_pitfalls.md`** - Erros estatísticos comuns e má-interpretações incluindo compreensões incorretas de valor-p, problemas de comparações múltiplas, problemas de tamanho de amostra, erros de tamanho de efeito, confusão correlação/causalidade, armadilhas de regressão e problemas de meta-análise

- **`references/evidence_hierarchy.md`** - Hierarquia tradicional de evidência, sistema GRADE, critérios de avaliação de qualidade de estudo, considerações específicas de domínio, princípios de síntese de evidência e frameworks de decisão prática

- **`references/logical_fallacies.md`** - Falácias lógicas comuns em discurso científico organizadas por tipo (causalidade, generalização, autoridade, relevância, estrutura, estatística) com exemplos e estratégias de detecção

- **`references/experimental_design.md`** - Checklist de desenho experimental abrangente cobrindo questões de pesquisa, hipóteses, seleção de desenho de estudo, variáveis, amostragem, cegamento, randomização, grupos controle, procedimentos, medição, minimização de viés, gerenciamento de dados, planejamento estatístico, considerações éticas, ameaças à validade e padrões de relatório

**Quando consultar referências:**
- Carregue referências no contexto quando frameworks detalhados são necessários
- Use grep para buscar referências por tópico específico: `grep -r "padrão" references/`
- Referências fornecem profundidade; SKILL.md fornece orientação procedural
- Consulte referências para listas abrangentes, critérios detalhados e exemplos específicos

## Lembre-se

**O pensamento crítico científico é sobre:**
- Avaliação sistemática usando princípios estabelecidos
- Crítica construtiva que melhora a ciência
- Confiança proporcional à força da evidência
- Transparência sobre incerteza e limitações
- Aplicação consistente de padrões
- Reconhecimento de que toda pesquisa tem limitações
- Equilíbrio entre ceticismo e abertura para evidência

**Sempre distinja entre:**
- Dados (o que foi observado) e interpretação (o que significa)
- Correlação e causalidade
- Significância estatística e importância prática
- Achados exploratórios e confirmatórios
- O que é conhecido e o que é incerto
- Evidência contra uma afirmação e evidência para o nulo

**Objetivos do pensamento crítico:**
1. Identificar pontos fortes e fraquezas com precisão
2. Determinar que conclusões são sustentadas
3. Reconhecer limitações e incertezas
4. Sugerir melhorias para trabalho futuro
5. Avançar compreensão