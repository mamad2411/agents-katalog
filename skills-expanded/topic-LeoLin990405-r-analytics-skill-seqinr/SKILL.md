---
name: seqinr
description: R seqinr package for biological sequence analysis. Use for reading, writing, and analyzing biological sequences.
---

# seqinr

Biological sequences retrieval and analysis.

## Reading Sequences

```r
library(seqinr)

# Read FASTA
seqs <- read.fasta("sequences.fasta")

# Get sequence
seq1 <- seqs[[1]]
getSequence(seq1)

# Get annotation
getAnnot(seq1)
getName(seq1)
```

## Writing Sequences

```r
# Write FASTA
write.fasta(sequences, names, file = "output.fasta")

# Multiple sequences
write.fasta(
  sequences = list(seq1, seq2),
  names = c("seq1", "seq2"),
  file.out = "output.fasta"
)
```

## Sequence Properties

```r
# GC content
GC(seq)

# Sequence length
length(seq)

# Count nucleotides
count(seq, wordsize = 1)

# Count codons
count(seq, wordsize = 3)
```

## Codon Usage

```r
# Codon usage table
uco(seq)

# Codon adaptation index
cai(seq, w = codon_weights)

# Effective number of codons
eff.nc(seq)
```

## Translation

```r
# Translate DNA to protein
translate(seq)

# With specific genetic code
translate(seq, numcode = 2)  # Vertebrate mitochondrial
```

## Sequence Manipulation

```r
# Reverse complement
comp(seq)
rev(comp(seq))

# Subsequence
seq[10:50]

# Convert to string
c2s(seq)

# Convert string to vector
s2c("ATCGATCG")
```

## Dotplot

```r
# Sequence comparison
dotPlot(seq1, seq2)

# With window
dotPlot(seq1, seq2, wsize = 10, wstep = 1)
```

## Database Access

```r
# Query GenBank
choosebank("genbank")
query <- query("myquery", "SP=Homo sapiens AND K=insulin")
seqs <- getSequence(query)
closebank()
```

## Amino Acid Properties

```r
# Amino acid composition
AAstat(protein_seq)

# Molecular weight
pmw(protein_seq)

# Isoelectric point
computePI(protein_seq)
```
