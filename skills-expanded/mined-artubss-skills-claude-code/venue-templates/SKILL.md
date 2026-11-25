---
name: venue-templates
description: Acesse modelos LaTeX abrangentes, requisitos de formatação e diretrizes de submissão para os principais veículos de publicação científica (Nature, Science, PLOS, IEEE, ACM), conferências acadêmicas (NeurIPS, ICML, CVPR, CHI), pôsteres de pesquisa e propostas de financiamento (NSF, NIH, DOE, DARPA). Esta skill deve ser usada ao preparar manuscritos para submissão em periódicos, artigos de conferência, pôsteres de pesquisa ou propostas de financiamento quando você precisa de requisitos de formatação específicos do veículo e modelos.
allowed-tools: [Read, Write, Edit, Bash]
---

# Modelos de Venue

## Visão Geral

Acesse modelos LaTeX abrangentes, requisitos de formatação e diretrizes de submissão para os principais veículos de publicação científica, conferências acadêmicas, pôsteres de pesquisa e propostas de financiamento. Esta skill fornece modelos prontos para usar e especificações detalhadas para submissões acadêmicas bem-sucedidas em várias disciplinas.

Use esta skill ao preparar um manuscrito para submissão em um periódico específico, artigo de conferência, pôster de pesquisa ou proposta de financiamento quando você precisar de requisitos de formatação específicos do veículo e modelos.

## Quando Usar Esta Skill

Esta skill deve ser usada quando:
- Preparar um manuscrito para submissão em um periódico específico (Nature, Science, PLOS, IEEE, etc.)
- Escrever um artigo de conferência com requisitos de formatação específicos (NeurIPS, ICML, CHI, etc.)
- Criar um pôster acadêmico de pesquisa para conferências
- Rascunhar propostas de financiamento para agências federais (NSF, NIH, DOE, DARPA) ou fundações privadas
- Verificar requisitos de formatação e limites de página para veículos-alvo
- Personalizar modelos com informações de autores e detalhes do projeto
- Verificar conformidade do documento com especificações do veículo

## Aprimoramento Visual com Esquemas Científicos

**Ao criar documentos com esta skill, sempre considere adicionar diagramas científicos e esquemas para aprimorar a comunicação visual.**

Se seu documento ainda não contiver esquemas ou diagramas:
- Use a skill **scientific-schematics** para gerar diagramas de qualidade para publicação com IA
- Simplesmente descreva seu diagrama desejado em linguagem natural
- O Nano Banana Pro gerará, revisará e refinará automaticamente o esquema

**Para novos documentos:** esquemas científicos devem ser gerados por padrão para representar visualmente conceitos-chave, workflows, arquiteturas ou relacionamentos descritos no texto.

**Como gerar esquemas:**
```bash
python scripts/generate_schematic.py "sua descrição de diagrama" -o figures/output.png
```

A IA gerará automaticamente:
- Imagens de qualidade para publicação com formatação apropriada
- Revisão e refinamento através de múltiplas iterações
- Garantia de acessibilidade (amigável para daltônico, alto contraste)
- Saída salva no diretório figures/

**Quando adicionar esquemas:**
- Fluxogramas de metodologia para artigos
- Diagramas de estrutura conceitual
- Ilustrações de arquitetura de sistema
- Diagramas de fluxo de dados
- Visualizações de design experimental
- Diagramas de fluxo de trabalho de pesquisa
- Qualquer conceito complexo que se beneficie de visualização

Para orientação detalhada sobre criação de esquemas, consulte a documentação da skill scientific-schematics.

---

## Capacidades Principais

### 1. Modelos de Artigos em Periódicos

Acesse modelos LaTeX e diretrizes de formatação para 50+ periódicos científicos importantes em várias disciplinas:

**Nature Portfolio**:
- Nature, Nature Methods, Nature Biotechnology, Nature Machine Intelligence
- Nature Communications, Nature Protocols
- Scientific Reports

**Família Science**:
- Science, Science Advances, Science Translational Medicine
- Science Immunology, Science Robotics

**PLOS (Public Library of Science)**:
- PLOS ONE, PLOS Biology, PLOS Computational Biology
- PLOS Medicine, PLOS Genetics

**Cell Press**:
- Cell, Neuron, Immunity, Cell Reports
- Molecular Cell, Developmental Cell

**Publicações IEEE**:
- IEEE Transactions (várias disciplinas)
- IEEE Access, modelos IEEE Journal

**Publicações ACM**:
- ACM Transactions, Communications of the ACM
- Anais de conferências ACM

**Outros Grandes Editores**:
- Periódicos Springer (várias disciplinas)
- Periódicos Elsevier (modelos customizados)
- Periódicos Wiley
- Periódicos BMC
- Periódicos Frontiers

### 2. Modelos de Artigos de Conferência

Modelos específicos de conferência com formatação apropriada para as principais conferências acadêmicas:

**Machine Learning e IA**:
- NeurIPS (Neural Information Processing Systems)
- ICML (International Conference on Machine Learning)
- ICLR (International Conference on Learning Representations)
- CVPR (Computer Vision and Pattern Recognition)
- AAAI (Association for the Advancement of Artificial Intelligence)

**Ciência da Computação**:
- ACM CHI (Human-Computer Interaction)
- SIGKDD (Knowledge Discovery and Data Mining)
- EMNLP (Empirical Methods in Natural Language Processing)
- SIGIR (Information Retrieval)
- Conferências USENIX

**Biologia e Bioinformática**:
- ISMB (Intelligent Systems for Molecular Biology)
- RECOMB (Research in Computational Molecular Biology)
- PSB (Pacific Symposium on Biocomputing)

**Engenharia**:
- Modelos de conferência IEEE (várias disciplinas)
- Conferências ASME, AIAA

### 3. Modelos de Pôsteres de Pesquisa

Modelos de pôsteres acadêmicos para apresentações em conferências:

**Formatos Padrão**:
- A0 (841 × 1189 mm / 33,1 × 46,8 polegadas)
- A1 (594 × 841 mm / 23,4 × 33,1 polegadas)
- 36" × 48" (914 × 1219 mm) - Tamanho comum nos EUA
- 42" × 56" (1067 × 1422 mm)
- 48" × 36" (orientação paisagem)

**Pacotes de Modelos**:
- **beamerposter**: Modelo clássico de pôster acadêmico
- **tikzposter**: Design de pôster moderno e colorido
- **baposter**: Layout estruturado multicolunas

**Características de Design**:
- Tamanhos de fonte ideais para legibilidade à distância
- Esquemas de cores (paletas seguras para daltônicos)
- Layouts em grid e estruturas de colunas
- Integração de código QR para materiais complementares

### 4. Modelos de Propostas de Financiamento

Modelos e requisitos de formatação para agências de financiamento principais:

**NSF (Fundação Nacional de Ciência)**:
- Modelo de proposta completa (descrição de projeto de 15 páginas)
- Resumo do Projeto (1 página: Overview, Intellectual Merit, Broader Impacts)
- Orçamento e justificativa de orçamento
- Currículo (limite de 3 páginas)
- Instalações, Equipamentos e Outros Recursos
- Plano de Gerenciamento de Dados

**NIH (Institutos Nacionais de Saúde)**:
- Subsídio de Pesquisa R01 (multi-ano)
- Subsídio Exploratório/Desenvolvimentista R21
- Prêmios K (Desenvolvimento de Carreira)
- Página de Objetivos Específicos (1 página, componente mais crítico)
- Estratégia de Pesquisa (Significância, Inovação, Abordagem)
- Currículos (limite de 5 páginas)

**DOE (Departamento de Energia)**:
- Propostas do Office of Science
- Modelos ARPA-E
- Descrições de Technology Readiness Level (TRL)
- Seções de comercialização e impacto

**DARPA (Agência de Projetos de Pesquisa Avançada de Defesa)**:
- Respostas BAA (Broad Agency Announcement)
- Framework do Catecismo de Heilmeier
- Abordagem técnica e marcos
- Planejamento de transição

**Fundações Privadas**:
- Gates Foundation
- Wellcome Trust
- Howard Hughes Medical Institute (HHMI)
- Chan Zuckerberg Initiative (CZI)

## Workflow: Localizando e Usando Modelos

### Passo 1: Identificar o Veículo-Alvo

Determine o veículo de publicação específico, conferência ou agência de financiamento:

```
Exemplos de consultas:
- "Preciso submeter para Nature"
- "Quais são os requisitos para NeurIPS 2025?"
- "Mostre-me a formatação de propostas NSF"
- "Estou criando um pôster para ISMB"
```

### Passo 2: Consultar Modelo e Requisitos

Acesse modelos e diretrizes de formatação específicos do veículo:

**Para Periódicos**:
```bash
# Carregar requisitos de formatação do periódico
Reference: references/journals_formatting.md
Search for: "Nature" ou nome do periódico específico

# Recuperar modelo
Template: assets/journals/nature_article.tex
```

**Para Conferências**:
```bash
# Carregar formatação da conferência
Reference: references/conferences_formatting.md
Search for: "NeurIPS" ou conferência específica

# Recuperar modelo
Template: assets/journals/neurips_article.tex
```

**Para Pôsteres**:
```bash
# Carregar diretrizes de pôster
Reference: references/posters_guidelines.md

# Recuperar modelo
Template: assets/posters/beamerposter_academic.tex
```

**Para Financiamento**:
```bash
# Carregar requisitos de financiamento
Reference: references/grants_requirements.md
Search for: "NSF" ou agência específica

# Recuperar modelo
Template: assets/grants/nsf_proposal_template.tex
```

### Passo 3: Revisar Requisitos de Formatação

Verifique especificações críticas antes de personalizar:

**Requisitos-Chave a Verificar**:
- Limites de página (varia por veículo)
- Tamanho e família de fonte
- Especificações de margem
- Espaçamento de linha
- Estilo de citação (APA, Vancouver, Nature, etc.)
- Requisitos de figura/tabela
- Formato de arquivo (PDF, Word, fonte LaTeX)
- Anonimização (para revisão double-blind)
- Limites de material suplementar

### Passo 4: Personalizar Modelo

Use scripts auxiliares ou personalização manual:

**Opção 1: Script Auxiliar (Recomendado)**:
```bash
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --title "Seu Título de Artigo" \
  --authors "Primeiro Autor, Segundo Autor" \
  --affiliations "Nome da Universidade" \
  --output meu_artigo_nature.tex
```

**Opção 2: Edição Manual**:
- Abra arquivo de modelo
- Substitua texto de placeholder (marcado com comentários)
- Preencha título, autores, afiliações, abstract
- Adicione seu conteúdo a cada seção

### Passo 5: Validar Formato

Verifique conformidade com requisitos do veículo:

```bash
python scripts/validate_format.py \
  --file meu_artigo.pdf \
  --venue "Nature" \
  --check-all
```

**Verificações de Validação**:
- Contagem de página dentro dos limites
- Tamanhos de fonte corretos
- Margens atendem às especificações
- Referências formatadas corretamente
- Figuras atendem aos requisitos de resolução

### Passo 6: Compilar e Revisar

Compile LaTeX e revise a saída:

```bash
# Compilar LaTeX
pdflatex meu_artigo.tex
bibtex meu_artigo
pdflatex meu_artigo.tex
pdflatex meu_artigo.tex

# Ou use latexmk para compilação automatizada
latexmk -pdf meu_artigo.tex
```

Checklist de revisão:
- [ ] Todas as seções presentes e adequadamente formatadas
- [ ] Citações renderizam corretamente
- [ ] Figuras aparecem com legendas apropriadas
- [ ] Contagem de página dentro dos limites
- [ ] Diretrizes de autor seguidas
- [ ] Materiais suplementares preparados (se necessário)

## Integração com Outras Skills

Esta skill funciona perfeitamente com outras skills científicas:

### Scientific Writing
- Use a skill **scientific-writing** para orientação de conteúdo (estrutura IMRaD, clareza, precisão)
- Aplique modelos específicos do veículo desta skill para formatação
- Combine para preparação completa de manuscritos

### Literature Review
- Use a skill **literature-review** para busca sistemática de literatura e síntese
- Aplique estilo de citação apropriado dos requisitos do veículo
- Formate referências de acordo com especificações de modelo

### Peer Review
- Use a skill **peer-review** para avaliar qualidade de manuscrito
- Use esta skill para verificar conformidade de formatação
- Garanta aderência a diretrizes de relatório (CONSORT, STROBE, etc.)

### Research Grants
- Referência cruzada com a skill **research-grants** para estratégia de conteúdo
- Use esta skill para modelos e formatação específicos de agência
- Combine para preparação abrangente de proposta de financiamento

### LaTeX Posters
- Esta skill fornece modelos de pôster agnósticos de veículo
- Use para requisitos de pôster específicos de conferência
- Integre com skills de visualização para criação de figura

## Categorias de Modelo

### Por Tipo de Documento

| Categoria | Contagem de Modelos | Veículos Comuns |
|----------|------------------|-----------------|
| **Artigos em Periódicos** | 30+ | Nature, Science, PLOS, IEEE, ACM, Cell Press |
| **Artigos de Conferência** | 20+ | NeurIPS, ICML, CVPR, CHI, ISMB |
| **Pôsteres de Pesquisa** | 10+ | A0, A1, 36×48, vários pacotes |
| **Propostas de Financiamento** | 15+ | NSF, NIH, DOE, DARPA, fundações |

### Por Disciplina

| Disciplina | Veículos Suportados |
|------------|-------------------|
| **Ciências da Vida** | Nature, Cell Press, PLOS, ISMB, RECOMB |
| **Ciências Físicas** | Science, Physical Review, ACS, APS |
| **Engenharia** | IEEE, ASME, AIAA, ACM |
| **Ciência da Computação** | ACM, IEEE, NeurIPS, ICML, ICLR |
| **Medicina** | NEJM, Lancet, JAMA, BMJ |
| **Interdisciplinar** | PNAS, Nature Communications, Science Advances |

## Scripts Auxiliares

### query_template.py

Busque e recupere modelos por nome de veículo, tipo ou palavras-chave:

```bash
# Encontrar modelos para um periódico específico
python scripts/query_template.py --venue "Nature" --type "article"

# Buscar por palavra-chave
python scripts/query_template.py --keyword "machine learning"

# Listar todos os modelos disponíveis
python scripts/query_template.py --list-all

# Obter requisitos para um veículo
python scripts/query_template.py --venue "NeurIPS" --requirements
```

### customize_template.py

Personalize modelos com informações de autor e projeto:

```bash
# Personalização básica
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --output meu_artigo.tex

# Com informações de autores
python scripts/customize_template.py \
  --template assets/journals/nature_article.tex \
  --title "Abordagem Novel para Dobradura de Proteína" \
  --authors "Jane Doe, John Smith, Alice Johnson" \
  --affiliations "MIT, Stanford, Harvard" \
  --email "[email protected]" \
  --output meu_artigo.tex

# Modo interativo
python scripts/customize_template.py --interactive
```

### validate_format.py

Verifique conformidade do documento com requisitos do veículo:

```bash
# Validar um PDF compilado
python scripts/validate_format.py \
  --file meu_artigo.pdf \
  --venue "Nature" \
  --check-all

# Verificar aspectos específicos
python scripts/validate_format.py \
  --file meu_artigo.pdf \
  --venue "NeurIPS" \
  --check page-count,margins,fonts

# Gerar relatório de validação
python scripts/validate_format.py \
  --file meu_artigo.pdf \
  --venue "Science" \
  --report validation_report.txt
```

## Melhores Práticas

### Seleção de Modelo
1. **Verificar atualidade**: Verifique data do modelo e compare com as diretrizes de autor mais recentes
2. **Verificar fontes oficiais**: Muitos periódicos fornecem classes LaTeX oficiais
3. **Testar compilação**: Compile modelo antes de adicionar conteúdo
4. **Ler comentários**: Modelos incluem comentários inline úteis

### Personalização
1. **Preservar estrutura**: Não remova seções ou pacotes obrigatórios
2. **Seguir placeholders**: Substitua texto de placeholder marcado sistematicamente
3. **Manter formatação**: Não sobrescreva formatação específica do veículo
4. **Manter backups**: Salve modelo original antes de personalização

### Conformidade
1. **Verificar limites de página**: Verifique antes da submissão final
2. **Validar citações**: Use estilo de citação correto para veículo
3. **Testar figuras**: Garanta que figuras atendam aos requisitos de resolução
4. **Revisar anonimização**: Remova informações de identificação se obrigatório

### Submissão
1. **Seguir instruções**: Leia diretrizes de autor completas
2. **Incluir todos arquivos**: Fonte LaTeX, figuras, bibliografia
3. **Gerar apropriadamente**: Use método de compilação recomendado
4. **Verificar saída**: Verifique que PDF corresponde às expectativas

## Requisitos de Formatação Comuns

### Limites de Página (Típicos)

| Tipo de Veículo | Limite Típico | Notas |
|---------------|--------------|-------|
| **Artigo Nature** | 5 páginas | ~3000 palavras excluindo refs |
| **Relatório Science** | 5 páginas | Figuras contam para limite |
| **PLOS ONE** | Sem limite | Comprimento ilimitado |
| **NeurIPS** | 8 páginas | + refs/apêndice ilimitado |
| **ICML** | 8 páginas | + refs/apêndice ilimitado |
| **Proposta NSF** | 15 páginas | Somente descrição de projeto |
| **NIH R01** | 12 páginas | Estratégia de pesquisa |

### Estilos de Citação por Veículo

| Veículo | Estilo de Citação | Formato |
|--------|------------------|--------|
| **Nature** | Numerado (sobrescrito) | Estilo Nature |
| **Science** | Numerado (sobrescrito) | Estilo Science |
| **PLOS** | Numerado (colchetes) | Vancouver |
| **Cell Press** | Autor-ano | Estilo Cell |
| **ACM** | Numerado | Estilo ACM |
| **IEEE** | Numerado (colchetes) | Estilo IEEE |
| **Periódicos APA** | Autor-ano | APA 7ª edição |

### Requisitos de Figura

| Veículo | Resolução | Formato | Cor |
|--------|-----------|--------|-----|
| **Nature** | 300+ dpi | TIFF, EPS, PDF | RGB ou CMYK |
| **Science** | 300+ dpi | TIFF, PDF | RGB |
| **PLOS** | 300-600 dpi | TIFF, EPS | RGB |
| **IEEE** | 300+ dpi | EPS, PDF | RGB ou Escala de Cinza |

## Recursos

### Recursos Incluídos

**Referências** (em `references/`):
- `journals_formatting.md`: Requisitos abrangentes de formatação de periódicos
- `conferences_formatting.md`: Especificações de artigos de conferência
- `posters_guidelines.md`: Design de pôster de pesquisa e dimensionamento
- `grants_requirements.md`: Requisitos de proposta de financiamento por agência

**Modelos** (em `assets/`):
- `journals/`: Modelos LaTeX de artigos de periódicos
- `posters/`: Modelos de pôsteres de pesquisa
- `grants/`: Modelos de propostas de financiamento

**Scripts** (em `scripts/`):
- `query_template.py`: Buscar e recuperar modelos
- `customize_template.py`: Personalizar com informações de autor
- `validate_format.py`: Verificar conformidade com requisitos

### Recursos Externos

**Diretrizes de Autor de Periódicos**:
- Nature: https://www.nature.com/nature/for-authors
- Science: https://www.science.org/content/page/instructions-authors
- PLOS: https://plos.org/resources/for-authors/
- Cell Press: https://www.cell.com/author-guidelines

**Formatação de Conferência**:
- NeurIPS: https://neurips.cc/Conferences/2024/CallForPapers
- ICML: https://icml.cc/Conferences/2024/StyleAuthorInstructions
- CVPR: https://cvpr.thecvf.com/Conferences/2024/AuthorGuidelines

**Recursos de Financiamento**:
- NSF PAPPG: https://www.nsf.gov/publications/pub_summ.jsp?ods_key=pappg
- NIH Forms: https://grants.nih.gov/grants/how-to-apply-application-guide.html
- DOE Funding: https://science.osti.gov/grants

## Uso de Exemplo

### Exemplo 1: Submissão de Artigo para Nature

```markdown
Usuário: "Preciso preparar um manuscrito para Nature"

Resposta:
1. Carregar requisitos de formatação para Nature (references/journals_formatting.md)
2. Recuperar modelo Nature (assets/journals/nature_article.tex)
3. Requisitos-chave:
   - Comprimento: ~3000 palavras, ~5 páginas
   - Formato: Coluna única, fonte 12pt
   - Citações: Numerado sobrescrito (estilo Nature)
   - Figuras: 300+ dpi, cor RGB
4. Personalizar modelo com seu título, autores, afiliações
5. Compilar e validar contra requisitos
```

### Exemplo 2: Artigo de Conferência NeurIPS

```markdown
Usuário: "Quais são os requisitos de formatação para NeurIPS?"

Resposta:
De references/conferences_formatting.md:
- Limite de página: 8 páginas texto principal + referências/apêndice ilimitado
- Formato: Duas colunas, fonte 10pt
- Modelo: neurips_2024.sty (arquivo de estilo oficial)
- Anonimização: Obrigatória para submissão inicial
- Citações: Numerado (colchetes)
- Figuras: Alta resolução, seguro para daltônicos recomendado
```

### Exemplo 3: Proposta NSF

```markdown
Usuário: "Ajude-me a formatar uma proposta NSF"

Resposta:
Requisitos NSF (de references/grants_requirements.md):
- Descrição do Projeto: máximo 15 páginas
- Resumo do Projeto: 1 página (Overview, Intellectual Merit, Broader Impacts)
- Justificativa de Orçamento: 3-5 páginas
- Currículo: 3 páginas por pesquisador sênior
- Fonte: Mínimo 10pt, Times Roman ou similar
- Margens: 1 polegada em todos os lados
Modelo: assets/grants/nsf_proposal_template.tex
```

### Exemplo 4: Pôster de Conferência

```markdown
Usuário: "Preciso criar um pôster para ISMB"

Resposta:
Especificações de pôster ISMB:
- Tamanho: Tipicamente A0 retrato (33,1 × 46,8 polegadas)
- Modelo recomendado: beamerposter ou tikzposter
- Tamanhos de fonte: Título 60-85pt, Headers 36-48pt, Corpo 24-32pt
- Incluir: Código QR para artigo/materiais complementares
Modelos disponíveis:
- assets/posters/beamerposter_academic.tex
- assets/posters/tikzposter_research.tex
```

## Atualizações e Manutenção

**Atualidade de Modelos**:
- Modelos atualizados anualmente ou quando veículos lançam novas diretrizes
- Última atualização: 2024
- Verifique sites de veículos oficiais para requisitos mais atuais

**Reportar Problemas**:
- Erros de compilação de modelo
- Requisitos de formatação desatualizados
- Modelos de veículo ausentes
- Especificações incorretas

## Resumo

A skill venue-templates fornece acesso abrangente a:

1. **Modelos de 50+ veículos de publicação** em várias disciplinas
2. **Requisitos detalhados de formatação** para periódicos, conferências, pôsteres, financiamento
3. **Scripts auxiliares** para descoberta de modelo, personalização e validação
4. **Integração** com outras skills de redação científica
5. **Melhores práticas** para submissões acadêmicas bem-sucedidas

Use esta skill sempre que precisar de orientação sobre formatação específica do veículo ou modelos para publicação acadêmica.