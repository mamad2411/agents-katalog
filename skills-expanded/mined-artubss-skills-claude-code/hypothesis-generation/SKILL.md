---
name: hypothesis-generation
description: "Gere hipóteses testáveis. Formule a partir de observações, projete experimentos, explore explicações concorrentes, desenvolva previsões, proponha mecanismos para investigação científica em diversos domínios."
allowed-tools: [Read, Write, Edit, Bash]
---

# Geração Científica de Hipóteses

## Visão Geral

Geração de hipóteses é um processo sistemático para desenvolver explicações testáveis. Formule hipóteses baseadas em evidências a partir de observações, projete experimentos, explore explicações concorrentes e desenvolva previsões. Aplique essa habilidade para investigação científica em diversos domínios.

## Quando Usar Essa Habilidade

Essa habilidade deve ser usada quando:
- Desenvolver hipóteses a partir de observações ou dados preliminares
- Projetar experimentos para testar questões científicas
- Explorar explicações concorrentes para fenômenos
- Formular previsões testáveis para pesquisa
- Conduzir geração de hipóteses baseada em literatura
- Planejar estudos mecanísticos em domínios científicos variados

## Aprimoramento Visual com Esquemáticos Científicos

**⚠️ OBRIGATÓRIO: Todo relatório de geração de hipóteses DEVE incluir pelo menos 1-2 figuras geradas por IA usando a habilidade scientific-schematics.**

Isso não é opcional. Relatórios de hipóteses sem elementos visuais estão incompletos. Antes de finalizar qualquer documento:
1. Gere no mínimo UM esquemático ou diagrama (ex.: marco de hipóteses mostrando explicações concorrentes)
2. Prefira 2-3 figuras para relatórios abrangentes (via mecanística, fluxograma de design experimental, árvore de decisão de previsões)

**Como gerar figuras:**
- Use a habilidade **scientific-schematics** para gerar diagramas com qualidade de publicação alimentados por IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará o esquemático automaticamente

**Como gerar esquemáticos:**
```bash
python scripts/generate_schematic.py "your diagram description" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens com qualidade de publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Acessibilidade garantida (amigável para daltonismo, alto contraste)
- Salvamento de outputs no diretório figures/

**Quando adicionar esquemáticos:**
- Diagramas de marco de hipóteses mostrando explicações concorrentes
- Fluxogramas de design experimental
- Diagramas de via mecanística
- Árvores de decisão de previsões
- Diagramas de relacionamento causal
- Visualizações de modelo teórico
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemáticos, consulte a documentação da habilidade scientific-schematics.

---

## Fluxo de Trabalho

Siga este processo sistemático para gerar hipóteses científicas robustas:

### 1. Compreender o Fenômeno

Comece esclarecendo a observação, questão ou fenômeno que requer explicação:

- Identifique a observação central ou padrão que necessita explicação
- Defina o escopo e limites do fenômeno
- Anote restrições ou contextos específicos
- Esclareça o que já é conhecido versus o que é incerto
- Identifique o(s) domínio(s) científico(s) relevante(s)

### 2. Conduzir Busca Abrangente de Literatura

Pesquise literatura científica existente para fundamentar hipóteses em evidências atuais. Use tanto PubMed (para tópicos biomédicos) quanto busca web geral (para domínios científicos mais amplos):

**Para tópicos biomédicos:**
- Use WebFetch com URLs do PubMed para acessar literatura relevante
- Pesquise por revisões recentes, meta-análises e pesquisas primárias
- Procure por fenômenos semelhantes, mecanismos relacionados ou sistemas análogos

**Para todos os domínios científicos:**
- Use WebSearch para encontrar artigos recentes, pré-impressões e revisões
- Pesquise por teorias estabelecidas, mecanismos ou marcos conceituais
- Identifique lacunas na compreensão atual

**Estratégia de busca:**
- Comece com buscas amplas para entender o panorama
- Restrinja a mecanismos, vias ou teorias específicas
- Procure por descobertas contraditórias ou debates não resolvidos
- Consulte `references/literature_search_strategies.md` para técnicas de busca detalhadas

### 3. Sintetizar Evidências Existentes

Analise e integre achados da busca de literatura:

- Resuma a compreensão atual do fenômeno
- Identifique mecanismos estabelecidos ou teorias que podem se aplicar
- Anote evidências conflitantes ou pontos de vista alternativos
- Reconheça lacunas, limitações ou questões sem resposta
- Identifique analogias de sistemas ou domínios relacionados

### 4. Gerar Hipóteses Concorrentes

Desenvolva 3-5 hipóteses distintas que possam explicar o fenômeno. Cada hipótese deve:

- Fornecer explicação mecanística (não apenas descrição)
- Ser distinguível de outras hipóteses
- Basear-se em evidências da síntese de literatura
- Considerar diferentes níveis de explicação (molecular, celular, sistêmico, populacional, etc.)

**Estratégias para gerar hipóteses:**
- Aplique mecanismos conhecidos de sistemas análogos
- Considere múltiplas vias causativas
- Explore diferentes escalas de explicação
- Questione suposições em explicações existentes
- Combine mecanismos de formas inovadoras

### 5. Avaliar Qualidade da Hipótese

Avalie cada hipótese contra critérios de qualidade estabelecidos de `references/hypothesis_quality_criteria.md`:

**Testabilidade:** A hipótese pode ser testada empiricamente?
**Falsabilidade:** Que observações a desprovariam?
**Parcimônia:** É a explicação mais simples que se ajusta à evidência?
**Poder Explicativo:** Quanto do fenômeno ela explica?
**Escopo:** Que alcance de observações ela cobre?
**Consistência:** Ela se alinha com princípios estabelecidos?
**Novidade:** Oferece novas perspectivas além de explicações existentes?

Anote explicitamente os pontos fortes e fracos de cada hipótese.

### 6. Projetar Testes Experimentais

Para cada hipótese viável, proponha experimentos ou estudos específicos para testá-la. Consulte `references/experimental_design_patterns.md` para abordagens comuns:

**Elementos de design experimental:**
- O que seria medido ou observado?
- Que comparações ou controles são necessários?
- Que métodos ou técnicas seriam usados?
- Que tamanhos de amostra ou abordagens estatísticas são apropriados?
- Quais são possíveis confundidores e como abordá-los?

**Considere múltiplas abordagens:**
- Experimentos de laboratório (in vitro, in vivo, computacionais)
- Estudos observacionais (transversais, longitudinais, caso-controle)
- Ensaios clínicos (se aplicável)
- Experimentos naturais ou designs quasi-experimentais

### 7. Formular Previsões Testáveis

Para cada hipótese, gere previsões específicas e quantitativas:

- Declare o que deve ser observado se a hipótese estiver correta
- Especifique direção e magnitude esperadas de efeitos quando possível
- Identifique condições sob as quais previsões devem se manter
- Distinga previsões entre hipóteses concorrentes
- Anote previsões que falseabilizariam a hipótese

### 8. Apresentar Output Estruturado

Gere documento LaTeX profissional usando o template em `assets/hypothesis_report_template.tex`. O relatório deve ser bem formatado com caixas coloridas para organização visual e dividido em texto principal conciso com apêndices abrangentes.

**Estrutura do Documento:**

**Texto Principal (Máximo 4 páginas):**
1. **Resumo Executivo** - Visão geral breve em caixa de resumo (0,5-1 página)
2. **Hipóteses Concorrentes** - Cada hipótese em sua própria caixa colorida com explicação mecanística breve e evidência-chave (2-2,5 páginas para 3-5 hipóteses)
   - **IMPORTANTE:** Use `\newpage` antes de cada caixa de hipótese para evitar transbordamento de conteúdo
   - Cada caixa deve ter ≤0,6 páginas no máximo
3. **Previsões Testáveis** - Previsões-chave em caixas âmbar (0,5-1 página)
4. **Comparações Críticas** - Caixas de comparação prioritária (0,5-1 página)

Mantenha texto principal altamente conciso - apenas informações essenciais. Todos os detalhes vão para apêndices.

**Estratégia de Quebra de Página:**
- Sempre use `\newpage` antes de caixas de hipótese para garantir que comecem em páginas novas
- Isso evita que o conteúdo transborde dos limites da página
- Caixas LaTeX (tcolorbox) não quebram automaticamente entre páginas

**Apêndices (Abrangentes e Detalhados):**
- **Apêndice A:** Revisão de literatura abrangente com citações extensas
- **Apêndice B:** Designs experimentais detalhados com protocolos completos
- **Apêndice C:** Tabelas de avaliação de qualidade e avaliações detalhadas
- **Apêndice D:** Evidências complementares e sistemas análogos

**Uso de Caixas Coloridas:**

Use os ambientes de caixa personalizados de `hypothesis_generation.sty`:

- `hypothesisbox1` até `hypothesisbox5` - Para cada hipótese concorrente (azul, verde, roxo, azul-petróleo, laranja)
- `predictionbox` - Para previsões testáveis (âmbar)
- `comparisonbox` - Para comparações críticas (cinza aço)
- `evidencebox` - Para destaques de evidência de apoio (azul-claro)
- `summarybox` - Para resumo executivo (azul)

**Cada caixa de hipótese deve conter (mantenha conciso para limite de 4 páginas):**
- **Explicação Mecanística:** 1-2 parágrafos breves (máx. 6-10 sentenças) explicando COMO e POR QUÊ
- **Evidência-Chave de Apoio:** 2-3 tópicos com citações (apenas evidência mais importante)
- **Premissas Centrais:** 1-2 suposições críticas

Todas as explicações detalhadas, evidência adicional e discussões abrangentes pertencem aos apêndices.

**Prevenção Crítica de Transbordamento:**
- Insira `\newpage` antes de cada caixa de hipótese para iniciá-la em uma página nova
- Mantenha cada caixa de hipótese completa em ≤0,6 páginas (aproximadamente 15-20 linhas de conteúdo)
- Se o conteúdo exceder isso, mova detalhes adicionais para Apêndice A
- Nunca deixe caixas transbordarem dos limites de página - isso cria PDFs ilegíveis

**Requisitos de Citação:**

Objetivo: citação extensa para apoiar todas as afirmações:
- **Texto principal:** 10-15 citações-chave apenas para evidência mais importante (mantenha conciso para limite de 4 páginas)
- **Apêndice A:** 40-70+ citações abrangentes cobrindo toda a literatura relevante
- **Total alvo:** 50+ referências em bibliografia

Citações em texto principal devem ser seletivas - cite apenas os artigos mais críticos. Toda citação abrangente e discussão detalhada de literatura pertence aos apêndices. Use `\citep{author2023}` para citações parentéticas.

**Compilação LaTeX:**

O template requer XeLaTeX ou LuaLaTeX para renderização apropriada:

```bash
xelatex hypothesis_report.tex
bibtex hypothesis_report
xelatex hypothesis_report.tex
xelatex hypothesis_report.tex
```

**Pacotes requeridos:** O pacote de estilo `hypothesis_generation.sty` deve estar no mesmo diretório ou no caminho LaTeX. Requer: tcolorbox, xcolor, fontspec, fancyhdr, titlesec, enumitem, booktabs, natbib.

**Prevenção de Transbordamento de Página:**

Para evitar que conteúdo transborde em páginas, siga estas diretrizes críticas:

1. **Monitore Comprimento de Conteúdo da Caixa:** Cada caixa de hipótese deve caber confortavelmente em uma única página. Se o conteúdo exceder ~0,7 páginas, provavelmente transbordará.

2. **Use Quebras de Página Estratégicas:** Insira `\newpage` antes de caixas que contenham conteúdo substancial:
   ```latex
   \newpage
   \begin{hypothesisbox1}[Hipótese 1: Título]
   % Conteúdo longo aqui
   \end{hypothesisbox1}
   ```

3. **Mantenha Caixas de Texto Principal Concisas:** Para o limite de texto principal de 4 páginas:
   - Cada caixa de hipótese: Máximo 0,5-0,6 páginas
   - Explicação mecanística: Apenas 1-2 parágrafos breves (máx. 6-10 sentenças)
   - Evidência-chave: Apenas 2-3 tópicos
   - Premissas centrais: Apenas 1-2 itens
   - Se o conteúdo for mais longo, mova detalhes para apêndices

4. **Quebre Conteúdo Longo:** Se uma hipótese requer explicação extensa, divida entre texto principal e apêndice:
   - Caixa de texto principal: Visão geral breve do mecanismo + 2-3 pontos de evidência-chave
   - Apêndice A: Explicação mecanística detalhada, evidência abrangente, discussão estendida

5. **Teste Limites de Página:** Antes de cada caixa nova, considere se o espaço de página restante é suficiente. Se menos de 0,6 páginas permanecerem, use `\newpage` para iniciar a caixa em uma página nova.

6. **Gerenciamento de Página de Apêndice:** Em apêndices, use `\newpage` entre seções principais para evitar transbordamento em áreas de conteúdo detalhado.

**Referência Rápida:** Veja `assets/FORMATTING_GUIDE.md` para exemplos detalhados de todos os tipos de caixa, esquemas de cor e padrões de formatação comuns.

## Padrões de Qualidade

Garanta que todas as hipóteses geradas atendam a esses padrões:

- **Baseadas em evidência:** Fundamentadas em literatura existente com citações
- **Testáveis:** Incluam previsões específicas e mensuráveis
- **Mecanísticas:** Expliquem como/por quê, não apenas o quê
- **Abrangentes:** Considerem explicações alternativas
- **Rigorosas:** Incluam designs experimentais para testar previsões

## Recursos

### references/

- `hypothesis_quality_criteria.md` - Marco para avaliar qualidade de hipótese (testabilidade, falsabilidade, parcimônia, poder explicativo, escopo, consistência)
- `experimental_design_patterns.md` - Abordagens experimentais comuns em domínios (ECRs, estudos observacionais, experimentos de laboratório, modelos computacionais)
- `literature_search_strategies.md` - Técnicas eficazes de busca para PubMed e fontes científicas gerais

### assets/

- `hypothesis_generation.sty` - Pacote de estilo LaTeX fornecendo caixas coloridas, formatação profissional e ambientes personalizados para relatórios de hipóteses
- `hypothesis_report_template.tex` - Template LaTeX completo com estrutura de texto principal e seções abrangentes de apêndice
- `FORMATTING_GUIDE.md` - Guia de referência rápida com exemplos de todos os tipos de caixa, esquemas de cores, práticas de citação e dicas de solução de problemas