---
name: literature-review
description: Conduzir análises críticas de literatura abrangentes e sistemáticas usando múltiplos bancos de dados acadêmicos (PubMed, arXiv, bioRxiv, Semantic Scholar, etc.). Esta competência deve ser usada ao realizar revisões sistemáticas de literatura, meta-análises, síntese de pesquisa ou buscas bibliográficas abrangentes em domínios biomédicos, científicos e técnicos. Cria documentos markdown e PDFs com formatação profissional e citações verificadas em múltiplos estilos (APA, Nature, Vancouver, etc.).
allowed-tools: [Read, Write, Edit, Bash]
---

# Análise de Literatura

## Visão Geral

Conduza análises críticas sistemáticas e abrangentes de literatura seguindo metodologia acadêmica rigorosa. Busque em múltiplos bancos de dados bibliográficos, sintetize achados tematicamente, verifique todas as citações quanto à precisão e gere documentos de saída profissionais em formatos markdown e PDF.

Esta competência se integra com múltiplas competências científicas para acesso a bancos de dados (gget, bioservices, datacommons-client) e fornece ferramentas especializadas para verificação de citações, agregação de resultados e geração de documentos.

## Quando Usar Esta Competência

Use esta competência quando:
- Conduzir uma análise crítica sistemática de literatura para pesquisa ou publicação
- Sintetizar conhecimento atual sobre um tópico específico entre múltiplas fontes
- Realizar meta-análise ou revisões de escopo
- Escrever a seção de análise de literatura de um artigo de pesquisa ou tese
- Investigar o estado da arte em um domínio de pesquisa
- Identificar lacunas de pesquisa e direções futuras
- Exigir citações verificadas e formatação profissional

## Aprimoramento Visual com Esquemas Científicos

**⚠️ OBRIGATÓRIO: Toda análise de literatura DEVE incluir pelo menos 1-2 figuras geradas por IA usando a competência scientific-schematics.**

Isto não é opcional. Análises de literatura sem elementos visuais estão incompletas. Antes de finalizar qualquer documento:
1. Gere no mínimo UM esquema ou diagrama (p. ex., diagrama de fluxo PRISMA para revisões sistemáticas)
2. Prefira 2-3 figuras para revisões abrangentes (fluxograma de estratégia de busca, diagrama de síntese temática, marco conceitual)

**Como gerar figuras:**
- Use a competência **scientific-schematics** para gerar diagramas de qualidade para publicação com IA
- Simplesmente descreva o diagrama desejado em linguagem natural
- Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "descrição do diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltônicos, alto contraste)
- Salvamento de saídas no diretório figures/

**Quando adicionar esquemas:**
- Diagramas de fluxo PRISMA para revisões sistemáticas
- Fluxogramas de estratégia de busca bibliográfica
- Diagramas de síntese temática
- Mapas de visualização de lacunas de pesquisa
- Diagramas de redes de citações
- Ilustrações de marcos conceituais
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da competência scientific-schematics.

---

## Fluxo de Trabalho Principal

As análises de literatura seguem um fluxo de trabalho estruturado e multifásico:

### Fase 1: Planejamento e Delimitação de Escopo

1. **Defina a Pergunta de Pesquisa**: Use framework PICO (População, Intervenção, Comparação, Outcome) para revisões clínicas/biomédicas
   - Exemplo: "Qual é a eficácia do CRISPR-Cas9 (I) para tratar doença falciforme (P) em comparação com cuidados padrão (C)?"

2. **Estabeleça Escopo e Objetivos**:
   - Defina perguntas de pesquisa claras e específicas
   - Determine tipo de revisão (narrativa, sistemática, escopo, meta-análise)
   - Estabeleça limites (período de tempo, escopo geográfico, tipos de estudo)

3. **Desenvolva Estratégia de Busca**:
   - Identifique 2-4 conceitos principais da pergunta de pesquisa
   - Liste sinônimos, abreviaturas e termos relacionados para cada conceito
   - Planeje operadores booleanos (AND, OR, NOT) para combinar termos
   - Selecione no mínimo 3 bancos de dados complementares

4. **Estabeleça Critérios de Inclusão/Exclusão**:
   - Intervalo de datas (p. ex., últimos 10 anos: 2015-2024)
   - Idioma (tipicamente inglês, ou especifique multilíngue)
   - Tipos de publicação (revisados por pares, preprints, revisões)
   - Desenhos de estudo (RCTs, observacionais, in vitro, etc.)
   - Documente todos os critérios claramente

### Fase 2: Busca Sistemática de Literatura

1. **Busca em Múltiplos Bancos de Dados**:

   Selecione bancos de dados apropriados para o domínio:

   **Biomédica & Ciências da Vida:**
   - Use competência `gget`: `gget search pubmed "termos de busca"` para PubMed/PMC
   - Use competência `gget`: `gget search biorxiv "termos de busca"` para preprints
   - Use competência `bioservices` para ChEMBL, KEGG, UniProt, etc.

   **Literatura Científica Geral:**
   - Busque arXiv via API direta (preprints em física, matemática, CS, q-bio)
   - Busque Semantic Scholar via API (200M+ artigos, multidisciplinar)
   - Use Google Scholar para cobertura abrangente (manual ou scraping cuidadoso)

   **Bancos de Dados Especializados:**
   - Use `gget alphafold` para estruturas de proteínas
   - Use `gget cosmic` para genômica do câncer
   - Use `datacommons-client` para dados demográficos/estatísticos
   - Use bancos de dados especializados conforme apropriado para o domínio

2. **Documente Parâmetros de Busca**:
   ```markdown
   ## Estratégia de Busca

   ### Banco de Dados: PubMed
   - **Data pesquisada**: 2024-10-25
   - **Intervalo de datas**: 2015-01-01 a 2024-10-25
   - **String de busca**:
     ```
     ("CRISPR"[Title] OR "Cas9"[Title])
     AND ("sickle cell"[MeSH] OR "SCD"[Title/Abstract])
     AND 2015:2024[Publication Date]
     ```
   - **Resultados**: 247 artigos
   ```

   Repita para cada banco de dados pesquisado.

3. **Exporte e Agregue Resultados**:
   - Exporte resultados em formato JSON de cada banco de dados
   - Combine todos os resultados em um único arquivo
   - Use `scripts/search_databases.py` para pós-processamento:
     ```bash
     python search_databases.py combined_results.json \
       --deduplicate \
       --format markdown \
       --output aggregated_results.md
     ```

### Fase 3: Triagem e Seleção

1. **Deduplicação**:
   ```bash
   python search_databases.py results.json --deduplicate --output unique_results.json
   ```
   - Remove duplicatas por DOI (primário) ou título (fallback)
   - Documente número de duplicatas removidas

2. **Triagem de Títulos**:
   - Revise todos os títulos contra critérios de inclusão/exclusão
   - Exclua estudos obviamente irrelevantes
   - Documente número excluído nesta fase

3. **Triagem de Resumos**:
   - Leia resumos dos estudos restantes
   - Aplique critérios de inclusão/exclusão rigorosamente
   - Documente razões de exclusão

4. **Triagem de Texto Completo**:
   - Obtenha textos completos dos estudos restantes
   - Conduza revisão detalhada contra todos os critérios
   - Documente razões específicas de exclusão
   - Registre número final de estudos incluídos

5. **Crie Diagrama de Fluxo PRISMA**:
   ```
   Busca inicial: n = X
   ├─ Após deduplicação: n = Y
   ├─ Após triagem de títulos: n = Z
   ├─ Após triagem de resumos: n = A
   └─ Incluído na revisão: n = B
   ```

### Fase 4: Extração de Dados e Avaliação de Qualidade

1. **Extraia Dados Principais** de cada estudo incluído:
   - Metadados do estudo (autores, ano, periódico, DOI)
   - Desenho e métodos do estudo
   - Tamanho da amostra e características populacionais
   - Achados principais e resultados
   - Limitações observadas pelos autores
   - Fontes de financiamento e conflitos de interesse

2. **Avalie Qualidade do Estudo**:
   - **Para RCTs**: Use ferramenta Cochrane Risk of Bias
   - **Para estudos observacionais**: Use Newcastle-Ottawa Scale
   - **Para revisões sistemáticas**: Use AMSTAR 2
   - Classifique cada estudo: Qualidade Alta, Moderada, Baixa ou Muito Baixa
   - Considere excluir estudos de qualidade muito baixa

3. **Organize por Temas**:
   - Identifique 3-5 temas principais entre estudos
   - Agrupe estudos por tema (estudos podem aparecer em múltiplos temas)
   - Observe padrões, consenso e controvérsias

### Fase 5: Síntese e Análise

1. **Crie Documento de Revisão** a partir do template:
   ```bash
   cp assets/review_template.md minha_analise_literatura.md
   ```

2. **Escreva Síntese Temática** (NÃO sumários estudo-por-estudo):
   - Organize seção de Resultados por temas ou perguntas de pesquisa
   - Sintetize achados entre múltiplos estudos dentro de cada tema
   - Compare e contraste diferentes abordagens e resultados
   - Identifique áreas de consenso e pontos de controvérsia
   - Destaque a evidência mais forte

   Exemplo de estrutura:
   ```markdown
   #### 3.3.1 Tema: Métodos de Entrega de CRISPR

   Múltiplas abordagens de entrega foram investigadas para edição gênica
   terapêutica. Vetores virais (AAV) foram usados em 15 estudos^1-15^ e
   mostraram alta eficiência de transdução (65-85%), mas levantaram
   preocupações de imunogenicidade^3,7,12^. Em contraste, nanopartículas
   lipídicas demonstraram eficiência menor (40-60%), mas perfis de segurança
   melhorados^16-23^.
   ```

3. **Análise Crítica**:
   - Avalie forças metodológicas e limitações entre estudos
   - Avalie qualidade e consistência de evidência
   - Identifique lacunas de conhecimento e metodológicas
   - Observe áreas que exigem futuras pesquisas

4. **Escreva Discussão**:
   - Interprete achados em contexto mais amplo
   - Discuta implicações clínicas, práticas ou de pesquisa
   - Reconheça limitações da própria revisão
   - Compare com revisões anteriores se aplicável
   - Proponha direções específicas de pesquisa futura

### Fase 6: Verificação de Citações

**CRÍTICO**: Todas as citações devem ser verificadas quanto à precisão antes da submissão final.

1. **Verifique Todos os DOIs**:
   ```bash
   python scripts/verify_citations.py minha_analise_literatura.md
   ```

   Este script:
   - Extrai todos os DOIs do documento
   - Verifica cada DOI se resolve corretamente
   - Recupera metadados de CrossRef
   - Gera relatório de verificação
   - Produz citações devidamente formatadas

2. **Revise Relatório de Verificação**:
   - Verifique DOIs que falharam
   - Valide nomes de autores, títulos e detalhes de publicação correspondem
   - Corrija erros no documento original
   - Re-execute verificação até que todas as citações passem

3. **Formate Citações Consistentemente**:
   - Escolha um estilo de citação e use em todo o documento (consulte `references/citation_styles.md`)
   - Estilos comuns: APA, Nature, Vancouver, Chicago, IEEE
   - Use saída do script de verificação para formatar citações corretamente
   - Garanta que citações no texto correspondem ao formato da lista de referências

### Fase 7: Geração de Documento

1. **Gere PDF**:
   ```bash
   python scripts/generate_pdf.py minha_analise_literatura.md \
     --citation-style apa \
     --output minha_revisao.pdf
   ```

   Opções:
   - `--citation-style`: apa, nature, chicago, vancouver, ieee
   - `--no-toc`: Desabilite sumário
   - `--no-numbers`: Desabilite numeração de seções
   - `--check-deps`: Verifique se pandoc/xelatex estão instalados

2. **Revise Saída Final**:
   - Verifique formatação e layout do PDF
   - Valide que todas as seções estão presentes
   - Garanta que citações renderizam corretamente
   - Verifique que figuras/tabelas aparecem adequadamente
   - Valide que sumário está correto

3. **Checklist de Qualidade**:
   - [ ] Todos os DOIs verificados com verify_citations.py
   - [ ] Citações formatadas consistentemente
   - [ ] Diagrama de fluxo PRISMA incluído (para revisões sistemáticas)
   - [ ] Metodologia de busca totalmente documentada
   - [ ] Critérios de inclusão/exclusão claramente declarados
   - [ ] Resultados organizados tematicamente (não estudo-por-estudo)
   - [ ] Avaliação de qualidade concluída
   - [ ] Limitações reconhecidas
   - [ ] Referências completas e precisas
   - [ ] PDF gerado sem erros

## Orientação Específica por Banco de Dados

### PubMed / PubMed Central

Acesse via competência `gget`:
```bash
# Busque PubMed
gget search pubmed "CRISPR gene editing" -l 100

# Busque com filtros
# Use PubMed Advanced Search Builder para construir consultas complexas
# Depois execute via gget ou API Entrez direta
```

**Dicas de busca**:
- Use termos MeSH: `"sickle cell disease"[MeSH]`
- Tags de campo: `[Title]`, `[Title/Abstract]`, `[Author]`
- Filtros de data: `2020:2024[Publication Date]`
- Operadores booleanos: AND, OR, NOT
- Consulte navegador MeSH: https://meshb.nlm.nih.gov/search

### bioRxiv / medRxiv

Acesse via competência `gget`:
```bash
gget search biorxiv "CRISPR sickle cell" -l 50
```

**Considerações importantes**:
- Preprints não são revisados por pares
- Valide achados com cautela
- Verifique se preprint foi publicado (CrossRef)
- Observe versão e data do preprint

### arXiv

Acesse via API direta ou WebFetch:
```python
# Exemplo categorias de busca:
# q-bio.QM (Métodos Quantitativos)
# q-bio.GN (Genômica)
# q-bio.MN (Redes Moleculares)
# cs.LG (Machine Learning)
# stat.ML (Estatística Machine Learning)

# Formato de busca: categoria AND termos
search_query = "cat:q-bio.QM AND ti:\"single cell sequencing\""
```

### Semantic Scholar

Acesse via API direta (requer chave API, ou use tier gratuito):
- 200M+ artigos em todos os campos
- Excelente para buscas multidisciplinares
- Fornece grafos de citações e recomendações de artigos
- Use para encontrar artigos altamente influentes

### Bancos de Dados Biomédicos Especializados

Use competências apropriadas:
- **ChEMBL**: Competência `bioservices` para bioatividade química
- **UniProt**: Competência `gget` ou `bioservices` para informações de proteínas
- **KEGG**: Competência `bioservices` para vias e genes
- **COSMIC**: Competência `gget` para mutações em câncer
- **AlphaFold**: `gget alphafold` para estruturas de proteínas
- **PDB**: `gget` ou API direta para estruturas experimentais

### Encadeamento de Citações

Expanda busca via redes de citações:

1. **Citações diretas** (artigos que citam artigos principais):
   - Use Google Scholar "Citado por"
   - Use APIs Semantic Scholar ou OpenAlex
   - Identifica pesquisa mais nova construindo sobre trabalho seminal

2. **Citações reversas** (referências de artigos principais):
   - Extraia referências de artigos incluídos
   - Identifique trabalho fundacional altamente citado
   - Encontre artigos citados por múltiplos estudos incluídos

## Guia de Estilo de Citação

Orientação detalhada de formatação está em `references/citation_styles.md`. Referência rápida:

### APA (7ª Edição)
- No texto: (Smith et al., 2023)
- Referência: Smith, J. D., Johnson, M. L., & Williams, K. R. (2023). Título. *Periódico*, *22*(4), 301-318. https://doi.org/10.xxx/yyy

### Nature
- No texto: Números sobrescritos^1,2^
- Referência: Smith, J. D., Johnson, M. L. & Williams, K. R. Título. *Nat. Rev. Drug Discov.* **22**, 301-318 (2023).

### Vancouver
- No texto: Números sobrescritos^1,2^
- Referência: Smith JD, Johnson ML, Williams KR. Título. Nat Rev Drug Discov. 2023;22(4):301-18.

**Sempre verifique citações** com verify_citations.py antes de finalizar.

## Melhores Práticas

### Estratégia de Busca
1. **Use múltiplos bancos de dados** (mínimo 3): Garante cobertura abrangente
2. **Inclua servidores de preprints**: Captura achados mais recentes não publicados
3. **Documente tudo**: Strings de busca, datas, contagens de resultados para reprodutibilidade
4. **Teste e refine**: Execute buscas piloto, revise resultados, ajuste termos

### Triagem e Seleção
1. **Use critérios claros**: Documente critérios de inclusão/exclusão antes da triagem
2. **Triagem sistemática**: Título → Resumo → Texto completo
3. **Documente exclusões**: Registre razões para excluir estudos
4. **Considere triagem dupla**: Para revisões sistemáticas, dois revisores triagem independentemente

### Síntese
1. **Organize tematicamente**: Agrupe por temas, NÃO por estudos individuais
2. **Sintetize entre estudos**: Compare, contraste, identifique padrões
3. **Seja crítico**: Avalie qualidade e consistência de evidência
4. **Identifique lacunas**: Observe o que está faltando ou pouco estudado

### Qualidade e Reprodutibilidade
1. **Avalie qualidade do estudo**: Use ferramentas apropriadas de avaliação de qualidade
2. **Verifique todas as citações**: Execute script verify_citations.py
3. **Documente metodologia**: Forneça detalhe suficiente para outros reproduzirem
4. **Siga diretrizes**: Use PRISMA para revisões sistemáticas

### Escrita
1. **Seja objetivo**: Apresente evidência justamente, reconheça limitações
2. **Seja sistemático**: Siga template estruturado
3. **Seja específico**: Inclua números, estatísticas, tamanhos de efeito quando disponível
4. **Seja claro**: Use headings claros, fluxo lógico, organização temática

## Armadilhas Comuns a Evitar

1. **Busca em banco de dados único**: Perde artigos relevantes; sempre busque em múltiplos
2. **Sem documentação de busca**: Torna revisão irreproduível; documente todas as buscas
3. **Sumário estudo-por-estudo**: Falta síntese; organize tematicamente em vez disso
4. **Citações não verificadas**: Leva a erros; sempre execute verify_citations.py
5. **Busca muito ampla**: Produz milhares de resultados irrelevantes; refine com termos específicos
6. **Busca muito restrita**: Perde artigos relevantes; inclua sinônimos e termos relacionados
7. **Ignora preprints**: Perde achados mais recentes; inclua bioRxiv, medRxiv, arXiv
8. **Sem avaliação de qualidade**: Trata toda evidência igualmente; avalie e reporte qualidade
9. **Viés de publicação**: Apenas resultados positivos publicados; observe viés potencial
10. **Busca desatualizada**: Campo evolui rapidamente; declare claramente data da busca

## Exemplo de Fluxo de Trabalho

Fluxo de trabalho completo para análise de literatura biomédica:

```bash
# 1. Crie documento de revisão a partir do template
cp assets/review_template.md analise_crispr_celula_falciforme.md

# 2. Busque em múltiplos bancos de dados usando competências apropriadas
# - Use competência gget para PubMed, bioRxiv
# - Use acesso API direto para arXiv, Semantic Scholar
# - Exporte resultados em formato JSON

# 3. Agregue e processe resultados
python scripts/search_databases.py combined_results.json \
  --deduplicate \
  --rank citations \
  --year-start 2015 \
  --year-end 2024 \
  --format markdown \
  --output search_results.md \
  --summary

# 4. Triagem de resultados e extração de dados
# - Triagem manual de títulos, resumos, textos completos
# - Extração de dados principais para o documento de revisão
# - Organização por temas

# 5. Escreva a revisão seguindo estrutura do template
# - Introdução com objetivos claros
# - Seção de metodologia detalhada
# - Resultados organizados tematicamente
# - Discussão crítica
# - Conclusões claras

# 6. Verifique todas as citações
python scripts/verify_citations.py analise_crispr_celula_falciforme.md

# Revise o relatório de citações
cat analise_crispr_celula_falciforme_citation_report.json

# Corrija citações que falharam e re-verifique
python scripts/verify_citations.py analise_crispr_celula_falciforme.md

# 7. Gere PDF profissional
python scripts/generate_pdf.py analise_crispr_celula_falciforme.md \
  --citation-style nature \
  --output analise_crispr_celula_falciforme.pdf

# 8. Revise saídas finais de markdown e PDF
```

## Integração com Outras Competências

Esta competência trabalha de forma integrada com outras competências científicas:

### Competências de Acesso a Bancos de Dados
- **gget**: PubMed, bioRxiv, COSMIC, AlphaFold, Ensembl, UniProt
- **bioservices**: ChEMBL, KEGG, Reactome, UniProt, PubChem
- **datacommons-client**: Dados demográficos, econômicos, estatísticas de saúde

### Competências de Análise
- **pydeseq2**: RNA-seq expressão diferencial (para seções de métodos)
- **scanpy**: Análise single-cell (para seções de métodos)
- **anndata**: Dados single-cell (para seções de métodos)
- **biopython**: Análise de sequências (para seções de fundo)

### Competências de Visualização
- **matplotlib**: Gere figuras e gráficos para revisão
- **seaborn**: Visualizações estatísticas

### Competências de Escrita
- **brand-guidelines**: Aplique branding institucional ao PDF
- **internal-comms**: Adapte revisão para diferentes audiências

## Recursos

### Recursos Inclusos

**Scripts:**
- `scripts/verify_citations.py`: Verifique DOIs e gere citações formatadas
- `scripts/generate_pdf.py`: Converta markdown em PDF profissional
- `scripts/search_databases.py`: Processe, deduplicar e formate resultados de busca

**Referências:**
- `references/citation_styles.md`: Guia detalhado de formatação de citações (APA, Nature, Vancouver, Chicago, IEEE)
- `references/database_strategies.md`: Estratégias abrangentes de busca em banco de dados

**Assets:**
- `assets/review_template.md`: Template de análise de literatura completo com todas as seções

### Recursos Externos

**Diretrizes:**
- PRISMA (Revisões Sistemáticas): http://www.prisma-statement.org/
- Manual Cochrane: https://training.cochrane.org/handbook
- AMSTAR 2 (Qualidade de Revisão): https://amstar.ca/

**Ferramentas:**
- Navegador MeSH: https://meshb.nlm.nih.gov/search
- PubMed Advanced Search: https://pubmed.ncbi.nlm.nih.gov/advanced/
- Guia Boolean Search: https://www.ncbi.nlm.nih.gov/books/NBK3827/

**Estilos de Citação:**
- APA Style: https://apastyle.apa.org/
- Nature Portfolio: https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards
- NLM/Vancouver: https://www.nlm.nih.gov/bsd/uniform_requirements.html

## Dependências

### Pacotes Python Obrigatórios
```bash
pip install requests  # Para verificação de citações
```

### Ferramentas de Sistema Obrigatórias
```bash
# Para geração de PDF
brew install pandoc  # macOS
apt-get install pandoc  # Linux

# Para LaTeX (geração PDF)
brew install --cask mactex  # macOS
apt-get install texlive-xetex  # Linux
```

Verifique dependências:
```bash
python scripts/generate_pdf.py --check-deps
```

## Resumo

Esta competência de análise de literatura fornece:

1. **Metodologia sistemática** seguindo melhores práticas acadêmicas
2. **Integração multi-banco de dados** via competências científicas existentes
3. **Verificação de citações** garantindo acurácia e credibilidade
4. **Saída profissional** em formatos markdown e PDF
5. **Orientação abrangente** cobrindo todo processo de revisão
6. **Garantia de qualidade** com ferramentas de verificação e validação
7. **Reprodutibilidade** através de requisitos de documentação detalhada

Conduza análises de literatura rigorosas e minuciosas que atendam padrões acadêmicos e forneçam síntese abrangente do conhecimento atual em qualquer domínio.