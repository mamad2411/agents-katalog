---
name: clinvar-database
description: "Consultar NCBI ClinVar para significância clínica de variantes. Pesquisar por gene/posição, interpretar classificações de patogenicidade, acessar via API E-utilities ou FTP, anotar VCFs, para medicina genômica."
---

# Base de Dados ClinVar

## Visão Geral

ClinVar é o arquivo livremente acessível do NCBI com relatórios sobre relações entre variantes genéticas humanas e fenótipos, com evidências de suporte. A base de dados agrega informações sobre variação genômica e sua relação com a saúde humana, fornecendo classificações de variantes padronizadas usadas em genética clínica e pesquisa.

## Quando Usar Esta Habilidade

Esta habilidade deve ser usada quando:

- Pesquisar variantes por gene, condição ou significância clínica
- Interpretar classificações de significância clínica (patogênica, benigna, VUS)
- Acessar dados de ClinVar programaticamente via API E-utilities
- Baixar e processar dados em massa do FTP
- Compreender status de revisão e classificações por estrelas
- Resolver interpretações conflitantes de variantes
- Anotar conjuntos de chamadas de variantes com significância clínica

## Capacidades Principais

### 1. Pesquisar e Consultar ClinVar

#### Consultas via Interface Web

Pesquise ClinVar usando a interface web em https://www.ncbi.nlm.nih.gov/clinvar/

**Padrões de pesquisa comuns:**
- Por gene: `BRCA1[gene]`
- Por significância clínica: `pathogenic[CLNSIG]`
- Por condição: `breast cancer[disorder]`
- Por variante: `NM_000059.3:c.1310_1313del[variant name]`
- Por cromossomo: `13[chr]`
- Combinada: `BRCA1[gene] AND pathogenic[CLNSIG]`

#### Acesso Programático via E-utilities

Acesse ClinVar programaticamente usando a API E-utilities do NCBI. Consulte `references/api_reference.md` para documentação abrangente da API incluindo:
- **esearch** - Pesquisar variantes que correspondem aos critérios
- **esummary** - Recuperar resumos de variantes
- **efetch** - Baixar registros XML completos
- **elink** - Encontrar registros relacionados em outras bases de dados NCBI

**Exemplo rápido usando curl:**
```bash
# Pesquisar por variantes patogênicas BRCA1
curl "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=clinvar&term=BRCA1[gene]+AND+pathogenic[CLNSIG]&retmode=json"
```

**Práticas recomendadas:**
- Teste as consultas na interface web antes de automatizar
- Use chaves de API para aumentar limites de taxa de 3 para 10 requisições/segundo
- Implemente backoff exponencial para erros de limite de taxa
- Defina `Entrez.email` ao usar Biopython

### 2. Interpretar Significância Clínica

#### Entendendo as Classificações

ClinVar usa terminologia padronizada para classificações de variantes. Consulte `references/clinical_significance.md` para diretrizes detalhadas de interpretação.

**Principais termos de classificação germinativa (ACMG/AMP):**
- **Pathogenic (P)** - Variante causa doença (~99% de probabilidade)
- **Likely Pathogenic (LP)** - Variante provavelmente causa doença (~90% de probabilidade)
- **Uncertain Significance (VUS)** - Evidência insuficiente para classificar
- **Likely Benign (LB)** - Variante provavelmente não causa doença
- **Benign (B)** - Variante não causa doença

**Status de revisão (classificações por estrelas):**
- ★★★★ Diretriz de prática clínica - Confiança mais alta
- ★★★ Revisão por painel de especialistas (ex: ClinGen) - Confiança alta
- ★★ Múltiplos submissores, sem conflitos - Confiança moderada
- ★ Único submissor com critérios - Peso padrão
- ☆ Nenhum critério de afirmação - Confiança baixa

**Considerações críticas:**
- Sempre verifique o status de revisão - prefira classificações ★★★ ou ★★★★
- Interpretações conflitantes requerem avaliação manual
- Classificações podem mudar conforme novas evidências emergem
- Variantes VUS (significância incerta) carecem de evidência suficiente para uso clínico

### 3. Baixar Dados em Massa do FTP

#### Acessar o Site FTP do ClinVar

Baixe conjuntos de dados completos de `ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/`

Consulte `references/data_formats.md` para documentação abrangente sobre formatos de arquivo e processamento.

**Cronograma de atualização:**
- Lançamentos mensais: Primeiro quinta-feira de cada mês (conjunto de dados completo, arquivado)
- Atualizações semanais: Toda segunda-feira (atualizações incrementais)

#### Formatos Disponíveis

**Arquivos XML** (mais abrangentes):
- Arquivos VCV (Variação): `xml/clinvar_variation/` - Agregação centrada em variante
- Arquivos RCV (Registro): `xml/RCV/` - Pares variante-condição
- Incluem detalhes completos de submissão, evidência e metadados

**Arquivos VCF** (para pipelines genômicos):
- GRCh37: `vcf_GRCh37/clinvar.vcf.gz`
- GRCh38: `vcf_GRCh38/clinvar.vcf.gz`
- Limitações: Exclui variantes >10kb e variantes estruturais complexas

**Arquivos delimitados por tabulação** (para análise rápida):
- `tab_delimited/variant_summary.txt.gz` - Resumo de todas as variantes
- `tab_delimited/var_citations.txt.gz` - Citações PubMed
- `tab_delimited/cross_references.txt.gz` - Referências cruzadas de banco de dados

**Exemplo de download:**
```bash
# Baixar último lançamento mensal XML
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_00-latest.xml.gz

# Baixar VCF para GRCh38
wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
```

### 4. Processar e Analisar Dados ClinVar

#### Trabalhando com Arquivos XML

Processe arquivos XML para extrair detalhes de variantes, classificações e evidências.

**Exemplo Python com xml.etree:**
```python
import gzip
import xml.etree.ElementTree as ET

with gzip.open('ClinVarVariationRelease.xml.gz', 'rt') as f:
    for event, elem in ET.iterparse(f, events=('end',)):
        if elem.tag == 'VariationArchive':
            variation_id = elem.attrib.get('VariationID')
            # Extrair significância clínica, status de revisão, etc.
            elem.clear()  # Liberar memória
```

#### Trabalhando com Arquivos VCF

Anote chamadas de variantes ou filtre por significância clínica usando bcftools ou Python.

**Usando bcftools:**
```bash
# Filtrar variantes patogênicas
bcftools view -i 'INFO/CLNSIG~"Pathogenic"' clinvar.vcf.gz

# Extrair genes específicos
bcftools view -i 'INFO/GENEINFO~"BRCA"' clinvar.vcf.gz

# Anotar seu VCF com ClinVar
bcftools annotate -a clinvar.vcf.gz -c INFO your_variants.vcf
```

**Usando PyVCF em Python:**
```python
import vcf

vcf_reader = vcf.Reader(filename='clinvar.vcf.gz')
for record in vcf_reader:
    clnsig = record.INFO.get('CLNSIG', [])
    if 'Pathogenic' in clnsig:
        gene = record.INFO.get('GENEINFO', [''])[0]
        print(f"{record.CHROM}:{record.POS} {gene} - {clnsig}")
```

#### Trabalhando com Arquivos Delimitados por Tabulação

Use pandas ou ferramentas de linha de comando para filtragem e análise rápida.

**Usando pandas:**
```python
import pandas as pd

# Carregar resumo de variantes
df = pd.read_csv('variant_summary.txt.gz', sep='\t', compression='gzip')

# Filtrar variantes patogênicas em gene específico
pathogenic_brca = df[
    (df['GeneSymbol'] == 'BRCA1') &
    (df['ClinicalSignificance'].str.contains('Pathogenic', na=False))
]

# Contar variantes por significância clínica
sig_counts = df['ClinicalSignificance'].value_counts()
```

**Usando ferramentas de linha de comando:**
```bash
# Extrair variantes patogênicas para gene específico
zcat variant_summary.txt.gz | \
  awk -F'\t' '$7=="TP53" && $13~"Pathogenic"' | \
  cut -f1,5,7,13,14
```

### 5. Lidar com Interpretações Conflitantes

Quando múltiplos submissores fornecem classificações diferentes para a mesma variante, ClinVar relata "Conflicting interpretations of pathogenicity".

**Estratégia de resolução:**
1. Verifique o status de revisão (classificação por estrelas) - classificações mais altas têm mais peso
2. Examine evidência e critérios de afirmação de cada submissor
3. Considere datas de submissão - submissões mais recentes podem refletir evidência atualizada
4. Revise dados de frequência populacional (ex: gnomAD) para contexto
5. Consulte classificações de painéis de especialistas (★★★) quando disponíveis
6. Para uso clínico, sempre defira para um profissional de genética

**Consulta de busca para excluir conflitos:**
```
TP53[gene] AND pathogenic[CLNSIG] NOT conflicting[RVSTAT]
```

### 6. Rastrear Atualizações de Classificação

Classificações de variantes podem mudar ao longo do tempo conforme novas evidências emergem.

**Por que as classificações mudam:**
- Novos estudos funcionais ou dados clínicos
- Informações de frequência populacional atualizadas
- Diretrizes ACMG/AMP revisadas
- Dados de segregação de famílias adicionais

**Práticas recomendadas:**
- Documente versão do ClinVar e data de acesso para reprodutibilidade
- Revise classificações periodicamente para variantes críticas
- Inscreva-se na lista de distribuição de ClinVar para grandes atualizações
- Use lançamentos mensais arquivados para conjuntos de dados estáveis

### 7. Enviar Dados para ClinVar

Organizações podem enviar interpretações de variantes para ClinVar.

**Métodos de submissão:**
- Portal de submissão web: https://submit.ncbi.nlm.nih.gov/subs/clinvar/
- Submissão por API (requer conta de serviço): Consulte `references/api_reference.md`
- Submissão em lote via modelos Excel

**Requisitos:**
- Conta organizacional com NCBI
- Critérios de afirmação (preferencialmente diretrizes ACMG/AMP)
- Evidência de suporte para classificação

Contate: clinvar@ncbi.nlm.nih.gov para configuração de conta de submissão.

## Exemplos de Workflow

### Exemplo 1: Identificar Variantes Patogênicas de Alta Confiança em um Gene

**Objetivo:** Encontrar variantes patogênicas no gene CFTR com revisão de painel de especialistas.

**Passos:**
1. Pesquise usando a interface web ou E-utilities:
   ```
   CFTR[gene] AND pathogenic[CLNSIG] AND (reviewed by expert panel[RVSTAT] OR practice guideline[RVSTAT])
   ```
2. Revise resultados, anotando status de revisão (deve ser ★★★ ou ★★★★)
3. Exporte lista de variantes ou recupere registros completos via efetch
4. Referência cruzada com apresentação clínica se aplicável

### Exemplo 2: Anotar VCF com Classificações ClinVar

**Objetivo:** Adicionar anotações de significância clínica a chamadas de variantes.

**Passos:**
1. Baixe o VCF do ClinVar apropriado (combine a construção do genoma: GRCh37 ou GRCh38):
   ```bash
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/vcf_GRCh38/clinvar.vcf.gz.tbi
   ```
2. Anote usando bcftools:
   ```bash
   bcftools annotate -a clinvar.vcf.gz \
     -c INFO/CLNSIG,INFO/CLNDN,INFO/CLNREVSTAT \
     -o annotated_variants.vcf \
     your_variants.vcf
   ```
3. Filtre o VCF anotado por variantes patogênicas:
   ```bash
   bcftools view -i 'INFO/CLNSIG~"Pathogenic"' annotated_variants.vcf
   ```

### Exemplo 3: Analisar Variantes para uma Doença Específica

**Objetivo:** Estudar todas as variantes associadas ao câncer de mama hereditário.

**Passos:**
1. Pesquise por condição:
   ```
   hereditary breast cancer[disorder] OR "Breast-ovarian cancer, familial"[disorder]
   ```
2. Baixe resultados como CSV ou recupere via E-utilities
3. Filtre por status de revisão para priorizar variantes de alta confiança
4. Analise distribuição entre genes (BRCA1, BRCA2, PALB2, etc.)
5. Examine variantes com interpretações conflitantes separadamente

### Exemplo 4: Download em Massa e Construção de Base de Dados

**Objetivo:** Construir uma base de dados ClinVar local para pipeline de análise.

**Passos:**
1. Baixe lançamento mensal para reprodutibilidade:
   ```bash
   wget ftp://ftp.ncbi.nlm.nih.gov/pub/clinvar/xml/clinvar_variation/ClinVarVariationRelease_YYYY-MM.xml.gz
   ```
2. Analise XML e carregue em base de dados (PostgreSQL, MySQL, MongoDB)
3. Indexe por gene, posição, significância clínica, status de revisão
4. Implemente rastreamento de versão para atualizações
5. Agende atualizações mensais do site FTP

## Limitações e Considerações Importantes

### Qualidade de Dados
- **Nem todas as submissões têm peso igual** - Verifique status de revisão (classificações por estrelas)
- **Interpretações conflitantes existem** - Requerem avaliação manual
- **Submissões históricas podem estar desatualizadas** - Dados mais recentes podem ser mais precisos
- **Classificação VUS não é um diagnóstico clínico** - Significa evidência insuficiente

### Limitações de Escopo
- **Não para diagnóstico clínico direto** - Sempre envolva profissional de genética
- **Específico de população** - Frequências de variante variam por ancestralidade
- **Cobertura incompleta** - Nem todos os genes ou variantes são bem estudados
- **Dependências de versão** - Coordene construção do genoma (GRCh37/GRCh38) entre análises

### Limitações Técnicas
- **Arquivos VCF excluem variantes grandes** - Variantes >10kb não estão em formato VCF
- **Limites de taxa na API** - 3 req/sec sem chave, 10 req/sec com chave API
- **Tamanhos de arquivo** - Lançamentos XML completos são arquivos multi-GB comprimidos
- **Sem atualizações em tempo real** - Site web atualizado semanalmente, FTP mensal/semanal

## Recursos

### Documentação de Referência

Esta habilidade inclui documentação de referência abrangente:

- **`references/api_reference.md`** - Documentação completa da API E-utilities com exemplos para esearch, esummary, efetch e elink; inclui limites de taxa, autenticação e amostras de código Python/Biopython

- **`references/clinical_significance.md`** - Guia detalhado para interpretar classificações de significância clínica, classificações por estrelas de status de revisão, resolução de conflitos e práticas recomendadas para interpretação de variantes

- **`references/data_formats.md`** - Documentação para formatos XML, VCF e delimitados por tabulação; estrutura de diretório FTP, exemplos de processamento e orientação de seleção de formato

### Recursos Externos

- Página inicial ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/
- Documentação ClinVar: https://www.ncbi.nlm.nih.gov/clinvar/docs/
- Documentação E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- Diretrizes de interpretação de variantes ACMG: Richards et al., 2015 (PMID: 25741868)
- Painéis de especialistas ClinGen: https://clinicalgenome.org/

### Contato

Para dúvidas sobre ClinVar ou submissão de dados: clinvar@ncbi.nlm.nih.gov