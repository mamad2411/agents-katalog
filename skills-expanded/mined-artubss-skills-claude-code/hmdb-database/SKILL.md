---
name: hmdb-database
description: "Acesse o Banco de Dados do Metaboloma Humano (220K+ metabólitos). Pesquise por nome/ID/estrutura, recupere propriedades químicas, dados de biomarcadores, espectros de RMN/MS, vias metabólicas, para metabolômica e identificação."
---

# Banco de Dados HMDB

## Visão Geral

O Banco de Dados do Metaboloma Humano (HMDB) é um recurso abrangente e gratuito contendo informações detalhadas sobre metabólitos de pequenas moléculas encontrados no corpo humano.

## Quando Usar Esta Skill

Esta skill deve ser usada ao realizar pesquisa em metabolômica, química clínica, descoberta de biomarcadores ou tarefas de identificação de metabólitos.

## Conteúdo da Base de Dados

HMDB versão 5.0 (atual em 2025) contém:

- **220.945 entradas de metabólitos** abrangendo compostos hidrossolúveis e lipossolúveis
- **8.610 sequências de proteínas** para enzimas e transportadores envolvidos no metabolismo
- **130+ campos de dados por metabólito** incluindo:
  - Propriedades químicas (estrutura, fórmula, peso molecular, InChI, SMILES)
  - Dados clínicos (associações de biomarcadores, doenças, concentrações normais/anormais)
  - Informações biológicas (vias metabólicas, reações, localizações)
  - Dados espectroscópicos (espectros de RMN, MS, MS-MS)
  - Links para bancos de dados externos (KEGG, PubChem, MetaCyc, ChEBI, PDB, UniProt, GenBank)

## Capacidades Principais

### 1. Buscas de Metabólitos Baseadas na Web

Acesse HMDB através da interface web em https://www.hmdb.ca/ para:

**Buscas por Texto:**
- Pesquise por nome do metabólito, sinônimo ou identificador (ID HMDB)
- IDs HMDB exemplares: HMDB0000001, HMDB0001234
- Pesquise por associações com doenças ou envolvimento em vias metabólicas
- Faça consultas por tipo de espécime biológico (urina, soro, LCR, saliva, fezes, suor)

**Buscas Baseadas em Estrutura:**
- Use ChemQuery para buscas de estrutura e subestrutura
- Pesquise por peso molecular ou intervalo de peso molecular
- Use strings SMILES ou InChI para encontrar compostos

**Buscas Espectrais:**
- Correspondência de espectros LC-MS
- Correspondência de espectros GC-MS
- Buscas de espectros RMN para identificação de metabólitos

**Buscas Avançadas:**
- Combine múltiplos critérios (nome, propriedades, intervalos de concentração)
- Filtre por localizações biológicas ou tipos de espécime
- Pesquise por associações com proteínas/enzimas

### 2. Acessando Informações de Metabólitos

Ao recuperar dados de metabólitos, HMDB fornece:

**Informações Químicas:**
- Nome sistemático, nomes tradicionais e sinônimos
- Fórmula química e peso molecular
- Representações de estrutura (2D/3D, SMILES, InChI, arquivo MOL)
- Taxonomia química e classificação

**Contexto Biológico:**
- Vias metabólicas e reações
- Enzimas e transportadores associados
- Localizações subcelulares
- Papéis e funções biológicas

**Relevância Clínica:**
- Intervalos normais de concentração em fluidos biológicos
- Associações de biomarcadores com doenças
- Significância clínica
- Informações de toxicidade quando aplicável

**Dados Analíticos:**
- Espectros RMN experimentais e preditos
- Espectros MS e MS-MS
- Tempos de retenção e dados cromatográficos
- Picos de referência para identificação

### 3. Conjuntos de Dados Disponíveis para Download

HMDB oferece downloads de dados em massa em https://www.hmdb.ca/downloads em múltiplos formatos:

**Formatos Disponíveis:**
- **XML**: Dados completos de metabólitos, proteínas e espectros
- **SDF**: Arquivos de estrutura de metabólitos para quimioinformática
- **FASTA**: Sequências de proteínas e genes
- **TXT**: Listas de picos de espectras brutas
- **CSV/TSV**: Exportações de dados tabulares

**Categorias de Conjuntos de Dados:**
- Todos os metabólitos ou filtrados por tipo de espécime
- Sequências de proteína/enzima
- Espectros experimentais e preditos (RMN, GC-MS, MS-MS)
- Informações de vias metabólicas

**Melhores Práticas:**
- Baixe formato XML para dados abrangentes incluindo todos os campos
- Use formato SDF para análise baseada em estrutura e workflows de quimioinformática
- Parse formatos CSV/TSV para integração com pipelines de análise de dados
- Verifique datas de versão para garantir dados atualizados (atual: v5.0, 2023-07-01)

**Requisitos de Uso:**
- Gratuito para pesquisa acadêmica e não comercial
- Uso comercial requer permissão explícita (contate samackay@ualberta.ca)
- Cite a publicação HMDB ao usar os dados

### 4. Acesso via API Programática

**Disponibilidade de API:**
HMDB não oferece API REST pública. O acesso programático requer contato com a equipe de desenvolvimento:

- **Grupos acadêmicos/pesquisa:** Contate eponine@ualberta.ca (Eponine) ou samackay@ualberta.ca (Scott)
- **Organizações comerciais:** Contate samackay@ualberta.ca (Scott) para acesso customizado via API

**Acesso Programático Alternativo:**
- **R/Bioconductor**: Use o pacote `hmdbQuery` para consultas baseadas em R
  - Instale: `BiocManager::install("hmdbQuery")`
  - Fornece funções de consulta baseadas em HTTP
- **Conjuntos de dados baixados**: Parse arquivos XML ou CSV localmente para análise programática
- **Web scraping**: Não recomendado; contate a equipe para acesso apropriado via API

### 5. Workflows de Pesquisa Comuns

**Identificação de Metabólitos em Metabolômica Não-Dirigida:**
1. Obtenha espectros MS ou RMN experimentais de amostras
2. Use ferramentas de busca espectral do HMDB para comparar com espectros de referência
3. Verifique candidatos verificando peso molecular, tempo de retenção e fragmentação MS-MS
4. Revise a plausibilidade biológica (esperado no tipo de espécime, vias metabólicas conhecidas)

**Descoberta de Biomarcadores:**
1. Pesquise HMDB por metabólitos associados à doença de interesse
2. Revise intervalos de concentração em estados normais versus doença
3. Identifique metabólitos com forte abundância diferencial
4. Examine contexto de vias metabólicas e mecanismos biológicos
5. Consulte referências cruzadas com literatura via links PubMed

**Análise de Vias Metabólicas:**
1. Identifique metabólitos de interesse a partir de dados experimentais
2. Procure entradas HMDB para cada metabólito
3. Extraia associações de vias metabólicas e reações enzimáticas
4. Use SMPDB vinculado (Small Molecule Pathway Database) para diagramas de vias
5. Identifique enriquecimento de vias metabólicas para interpretação biológica

**Integração de Base de Dados:**
1. Baixe dados HMDB em formato XML ou CSV
2. Parse e extraia campos relevantes para banco de dados local
3. Vincule com IDs externos (KEGG, PubChem, ChEBI) para consultas entre bancos de dados
4. Construa ferramentas locais ou pipelines incorporando dados de referência HMDB

## Recursos HMDB Relacionados

O ecossistema HMDB inclui bancos de dados relacionados:

- **DrugBank**: ~2.832 compostos farmacêuticos com informações farmacêuticas
- **T3DB (Toxin and Toxin Target Database)**: ~3.670 compostos tóxicos
- **SMPDB (Small Molecule Pathway Database)**: Diagramas e mapas de vias metabólicas
- **FooDB**: ~70.000 compostos de componentes alimentares

Estes bancos de dados compartilham estrutura similar e identificadores, habilitando consultas integradas através do metaboloma humano, drogas, toxinas e bancos de dados alimentares.

## Melhores Práticas

**Qualidade de Dados:**
- Verifique identificações de metabólitos com múltiplos tipos de evidência (espectros, estrutura, propriedades)
- Verifique indicadores de qualidade de dados experimentais versus preditos
- Revise citações e evidências para associações de biomarcadores

**Rastreamento de Versão:**
- Anote a versão HMDB usada na pesquisa (atual: v5.0)
- Bancos de dados são atualizados periodicamente com novas entradas e correções
- Re-consulte para atualizações ao publicar para garantir informações atuais

**Citação:**
- Sempre cite HMDB em publicações usando o banco de dados
- Referencie IDs HMDB específicos ao discutir metabólitos
- Reconheça fontes de dados para conjuntos de dados baixados

**Desempenho:**
- Para análise em larga escala, baixe conjuntos de dados completos em vez de consultas web repetidas
- Use formatos apropriados (XML para dados abrangentes, CSV para análise tabular)
- Considere cache local de informações de metabólitos acessadas frequentemente

## Documentação de Referência

Veja `references/hmdb_data_fields.md` para informações detalhadas sobre campos de dados disponíveis e seus significados.