---
name: biopython
description: "Kit de ferramentas Python principal para biologia molecular. Preferido para consultas Python-based no PubMed/NCBI (Bio.Entrez), manipulação de sequências, análise de arquivos (FASTA, GenBank, FASTQ, PDB), workflows avançados de BLAST, estruturas, filogenética. Para BLAST rápido, use gget. Para REST API direto, use pubmed-database."
---

# Biopython: Biologia Molecular Computacional em Python

## Visão Geral

Biopython é um conjunto abrangente de ferramentas Python gratuitas para computação biológica. Oferece funcionalidades para manipulação de sequências, entrada/saída de arquivos, acesso a bancos de dados, bioinformática estrutural, filogenética e muitas outras tarefas de bioinformática. A versão atual é **Biopython 1.85** (lançada em janeiro de 2025), que suporta Python 3 e requer NumPy.

## Quando Usar Esta Skill

Use esta skill quando:

- Trabalhar com sequências biológicas (DNA, RNA ou proteína)
- Ler, escrever ou converter formatos de arquivos biológicos (FASTA, GenBank, FASTQ, PDB, mmCIF, etc.)
- Acessar bancos de dados NCBI (GenBank, PubMed, Protein, Gene, etc.) via Entrez
- Executar buscas BLAST ou analisar resultados de BLAST
- Realizar alinhamentos de sequências (pairwise ou alinhamentos de múltiplas sequências)
- Analisar estruturas de proteínas em arquivos PDB
- Criar, manipular ou visualizar árvores filogenéticas
- Encontrar motivos em sequências ou analisar padrões de motivos
- Calcular estatísticas de sequências (conteúdo GC, peso molecular, temperatura de desnaturação, etc.)
- Realizar tarefas de bioinformática estrutural
- Trabalhar com dados de genética de populações
- Qualquer outra tarefa de biologia molecular computacional

## Capacidades Centrais

Biopython está organizado em sub-pacotes modulares, cada um abordando domínios específicos de bioinformática:

1. **Manipulação de Sequências** - Bio.Seq e Bio.SeqIO para manipulação e entrada/saída de sequências
2. **Análise de Alinhamentos** - Bio.Align e Bio.AlignIO para alinhamentos pairwise e de múltiplas sequências
3. **Acesso a Bancos de Dados** - Bio.Entrez para acesso programático a bancos de dados NCBI
4. **Operações BLAST** - Bio.Blast para executar e analisar buscas BLAST
5. **Bioinformática Estrutural** - Bio.PDB para trabalhar com estruturas de proteínas 3D
6. **Filogenética** - Bio.Phylo para manipulação e visualização de árvores filogenéticas
7. **Recursos Avançados** - Motivos, genética de populações, utilitários de sequência e mais

## Instalação e Configuração

Instale Biopython usando pip (requer Python 3 e NumPy):

```python
uv pip install biopython
```

Para acesso a bancos de dados NCBI, sempre defina seu endereço de email (obrigatório pelo NCBI):

```python
from Bio import Entrez
Entrez.email = "seu.email@example.com"

# Opcional: Chave de API para limites de taxa mais altos (10 req/s em vez de 3 req/s)
Entrez.api_key = "sua_chave_api_aqui"
```

## Usando Esta Skill

Esta skill oferece documentação abrangente organizada por área de funcionalidade. Ao trabalhar em uma tarefa, consulte a documentação de referência relevante:

### 1. Manipulação de Sequências (Bio.Seq & Bio.SeqIO)

**Referência:** `references/sequence_io.md`

Use para:
- Criar e manipular sequências biológicas
- Ler e escrever arquivos de sequências (FASTA, GenBank, FASTQ, etc.)
- Converter entre formatos de arquivo
- Extrair sequências de arquivos grandes
- Tradução, transcrição e complemento reverso de sequências
- Trabalhar com objetos SeqRecord

**Exemplo rápido:**
```python
from Bio import SeqIO

# Ler sequências de arquivo FASTA
for record in SeqIO.parse("sequences.fasta", "fasta"):
    print(f"{record.id}: {len(record.seq)} bp")

# Converter GenBank para FASTA
SeqIO.convert("input.gb", "genbank", "output.fasta", "fasta")
```

### 2. Análise de Alinhamentos (Bio.Align & Bio.AlignIO)

**Referência:** `references/alignment.md`

Use para:
- Alinhamento de sequências pairwise (global e local)
- Ler e escrever alinhamentos de múltiplas sequências
- Usar matrizes de substituição (BLOSUM, PAM)
- Calcular estatísticas de alinhamento
- Personalizar parâmetros de alinhamento

**Exemplo rápido:**
```python
from Bio import Align

# Alinhamento pairwise
aligner = Align.PairwiseAligner()
aligner.mode = 'global'
alignments = aligner.align("ACCGGT", "ACGGT")
print(alignments[0])
```

### 3. Acesso a Bancos de Dados (Bio.Entrez)

**Referência:** `references/databases.md`

Use para:
- Buscar em bancos de dados NCBI (PubMed, GenBank, Protein, Gene, etc.)
- Baixar sequências e registros
- Obter informações de publicações
- Encontrar registros relacionados entre bancos de dados
- Download em lote com limitação de taxa apropriada

**Exemplo rápido:**
```python
from Bio import Entrez
Entrez.email = "seu.email@example.com"

# Buscar no PubMed
handle = Entrez.esearch(db="pubmed", term="biopython", retmax=10)
results = Entrez.read(handle)
handle.close()
print(f"Encontrados {results['Count']} resultados")
```

### 4. Operações BLAST (Bio.Blast)

**Referência:** `references/blast.md`

Use para:
- Executar buscas BLAST via serviços web NCBI
- Executar buscas BLAST locais
- Analisar saída XML de BLAST
- Filtrar resultados por E-value ou identidade
- Extrair sequências de hits

**Exemplo rápido:**
```python
from Bio.Blast import NCBIWWW, NCBIXML

# Executar busca BLAST
result_handle = NCBIWWW.qblast("blastn", "nt", "ATCGATCGATCG")
blast_record = NCBIXML.read(result_handle)

# Exibir top hits
for alignment in blast_record.alignments[:5]:
    print(f"{alignment.title}: E-value={alignment.hsps[0].expect}")
```

### 5. Bioinformática Estrutural (Bio.PDB)

**Referência:** `references/structure.md`

Use para:
- Analisar arquivos de estrutura PDB e mmCIF
- Navegar na hierarquia de estrutura de proteína (SMCRA: Structure/Model/Chain/Residue/Atom)
- Calcular distâncias, ângulos e dihedros
- Atribuição de estrutura secundária (DSSP)
- Superimposição de estrutura e cálculo de RMSD
- Extrair sequências de estruturas

**Exemplo rápido:**
```python
from Bio.PDB import PDBParser

# Analisar estrutura
parser = PDBParser(QUIET=True)
structure = parser.get_structure("1crn", "1crn.pdb")

# Calcular distância entre carbonos alfa
chain = structure[0]["A"]
distance = chain[10]["CA"] - chain[20]["CA"]
print(f"Distância: {distance:.2f} Å")
```

### 6. Filogenética (Bio.Phylo)

**Referência:** `references/phylogenetics.md`

Use para:
- Ler e escrever árvores filogenéticas (Newick, NEXUS, phyloXML)
- Construir árvores a partir de matrizes de distância ou alinhamentos
- Manipulação de árvore (poda, re-enraizamento, ladderização)
- Calcular distâncias filogenéticas
- Criar árvores de consenso
- Visualizar árvores

**Exemplo rápido:**
```python
from Bio import Phylo

# Ler e visualizar árvore
tree = Phylo.read("tree.nwk", "newick")
Phylo.draw_ascii(tree)

# Calcular distância
distance = tree.distance("Species_A", "Species_B")
print(f"Distância: {distance:.3f}")
```

### 7. Recursos Avançados

**Referência:** `references/advanced.md`

Use para:
- **Motivos de sequência** (Bio.motifs) - Encontrar e analisar padrões de motivos
- **Genética de populações** (Bio.PopGen) - Arquivos GenePop, cálculos de Fst, testes de Hardy-Weinberg
- **Utilitários de sequência** (Bio.SeqUtils) - Conteúdo GC, temperatura de desnaturação, peso molecular, análise de proteína
- **Análise de restrição** (Bio.Restriction) - Encontrar sítios de enzimas de restrição
- **Clustering** (Bio.Cluster) - Clustering K-means e hierárquico
- **Diagramas de genoma** (GenomeDiagram) - Visualizar características genômicas

**Exemplo rápido:**
```python
from Bio.SeqUtils import gc_fraction, molecular_weight
from Bio.Seq import Seq

seq = Seq("ATCGATCGATCG")
print(f"Conteúdo GC: {gc_fraction(seq):.2%}")
print(f"Peso molecular: {molecular_weight(seq, seq_type='DNA'):.2f} g/mol")
```

## Diretrizes Gerais de Workflow

### Lendo Documentação

Quando um usuário pergunta sobre uma tarefa específica do Biopython:

1. **Identifique o módulo relevante** baseado na descrição da tarefa
2. **Leia o arquivo de referência apropriado** usando a ferramenta Read
3. **Extraia padrões de código relevantes** e adapte-os às necessidades específicas do usuário
4. **Combine múltiplos módulos** quando a tarefa exigir

Padrões de busca de exemplo para arquivos de referência:
```bash
# Encontrar informações sobre funções específicas
grep -n "SeqIO.parse" references/sequence_io.md

# Encontrar exemplos de tarefas específicas
grep -n "BLAST" references/blast.md

# Encontrar todas as ocorrências de um módulo
grep -n "Bio.Seq" references/*.md
```

### Escrevendo Código Biopython

Siga estes princípios ao escrever código Biopython:

1. **Importe módulos explicitamente**
   ```python
   from Bio import SeqIO, Entrez
   from Bio.Seq import Seq
   ```

2. **Defina email do Entrez** ao usar bancos de dados NCBI
   ```python
   Entrez.email = "seu.email@example.com"
   ```

3. **Use formatos de arquivo apropriados** - Verifique qual formato melhor se adequa à tarefa
   ```python
   # Formatos comuns: "fasta", "genbank", "fastq", "clustal", "phylip"
   ```

4. **Manipule arquivos apropriadamente** - Feche handles após o uso ou use context managers
   ```python
   with open("file.fasta") as handle:
       records = SeqIO.parse(handle, "fasta")
   ```

5. **Use iteradores para arquivos grandes** - Evite carregar tudo na memória
   ```python
   for record in SeqIO.parse("large_file.fasta", "fasta"):
       # Processe um registro por vez
   ```

6. **Trate erros apropriadamente** - Operações de rede e análise de arquivo podem falhar
   ```python
   try:
       handle = Entrez.efetch(db="nucleotide", id=accession)
   except HTTPError as e:
       print(f"Erro: {e}")
   ```

## Padrões Comuns

### Padrão 1: Buscar Sequência do GenBank

```python
from Bio import Entrez, SeqIO

Entrez.email = "seu.email@example.com"

# Buscar sequência
handle = Entrez.efetch(db="nucleotide", id="EU490707", rettype="gb", retmode="text")
record = SeqIO.read(handle, "genbank")
handle.close()

print(f"Descrição: {record.description}")
print(f"Comprimento da sequência: {len(record.seq)}")
```

### Padrão 2: Pipeline de Análise de Sequência

```python
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

for record in SeqIO.parse("sequences.fasta", "fasta"):
    # Calcular estatísticas
    gc = gc_fraction(record.seq)
    length = len(record.seq)

    # Encontrar ORFs, traduzir, etc.
    protein = record.seq.translate()

    print(f"{record.id}: {length} bp, GC={gc:.2%}")
```

### Padrão 3: BLAST e Buscar Top Hits

```python
from Bio.Blast import NCBIWWW, NCBIXML
from Bio import Entrez, SeqIO

Entrez.email = "seu.email@example.com"

# Executar BLAST
result_handle = NCBIWWW.qblast("blastn", "nt", sequence)
blast_record = NCBIXML.read(result_handle)

# Obter acessões de top hit
accessions = [aln.accession for aln in blast_record.alignments[:5]]

# Buscar sequências
for acc in accessions:
    handle = Entrez.efetch(db="nucleotide", id=acc, rettype="fasta", retmode="text")
    record = SeqIO.read(handle, "fasta")
    handle.close()
    print(f">{record.description}")
```

### Padrão 4: Construir Árvore Filogenética a partir de Sequências

```python
from Bio import AlignIO, Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

# Ler alinhamento
alignment = AlignIO.read("alignment.fasta", "fasta")

# Calcular distâncias
calculator = DistanceCalculator("identity")
dm = calculator.get_distance(alignment)

# Construir árvore
constructor = DistanceTreeConstructor()
tree = constructor.nj(dm)

# Visualizar
Phylo.draw_ascii(tree)
```

## Melhores Práticas

1. **Sempre leia a documentação de referência relevante** antes de escrever código
2. **Use grep para buscar em arquivos de referência** funções específicas ou exemplos
3. **Valide formatos de arquivo** antes de analisar
4. **Trate dados faltantes apropriadamente** - Nem todos os registros têm todos os campos
5. **Cache dados baixados** - Não baixe repetidamente as mesmas sequências
6. **Respeite limites de taxa NCBI** - Use chaves de API e atrasos apropriados
7. **Teste com pequenos conjuntos de dados** antes de processar arquivos grandes
8. **Mantenha Biopython atualizado** para obter novos recursos e correções de bugs
9. **Use tabelas de código genético apropriadas** para tradução
10. **Documente parâmetros de análise** para reprodutibilidade

## Solução de Problemas de Problemas Comuns

### Problema: "No handlers could be found for logger 'Bio.Entrez'"
**Solução:** É apenas um aviso. Defina Entrez.email para suprimi-lo.

### Problema: "HTTP Error 400" do NCBI
**Solução:** Verifique se os IDs/acessões são válidos e formatados corretamente.

### Problema: "ValueError: EOF" ao analisar arquivos
**Solução:** Verifique se o formato do arquivo corresponde à string de formato especificada.

### Problema: Falha no alinhamento com "sequences are not the same length"
**Solução:** Certifique-se de que as sequências estão alinhadas antes de usar AlignIO ou MultipleSeqAlignment.

### Problema: Buscas BLAST lentas
**Solução:** Use BLAST local para buscas em larga escala ou cache de resultados.

### Problema: Avisos do analisador PDB
**Solução:** Use `PDBParser(QUIET=True)` para suprimir avisos ou investigue a qualidade da estrutura.

## Recursos Adicionais

- **Documentação Oficial**: https://biopython.org/docs/latest/
- **Tutorial**: https://biopython.org/docs/latest/Tutorial/
- **Cookbook**: https://biopython.org/docs/latest/Tutorial/ (exemplos avançados)
- **GitHub**: https://github.com/biopython/biopython
- **Lista de Discussão**: biopython@biopython.org

## Referência Rápida

Para localizar informações em arquivos de referência, use estes padrões de busca:

```bash
# Buscar funções específicas
grep -n "function_name" references/*.md

# Encontrar exemplos de tarefas específicas
grep -n "example" references/sequence_io.md

# Encontrar todas as ocorrências de um módulo
grep -n "Bio.Seq" references/*.md
```

## Resumo

Biopython oferece ferramentas abrangentes para biologia molecular computacional. Ao usar esta skill:

1. **Identifique o domínio da tarefa** (sequências, alinhamentos, bancos de dados, BLAST, estruturas, filogenética ou avançado)
2. **Consulte o arquivo de referência apropriado** no diretório `references/`
3. **Adapte exemplos de código** ao caso de uso específico
4. **Combine múltiplos módulos** quando necessário para workflows complexos
5. **Siga as melhores práticas** para manipulação de arquivo, verificação de erro e gerenciamento de dados

A documentação de referência modular garante informações detalhadas e pesquisáveis para todas as principais capacidades do Biopython.