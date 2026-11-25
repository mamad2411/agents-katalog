---
name: Biostrings
description: R Biostrings package for biological sequences. Use for DNA, RNA, and protein sequence manipulation.
---

# Biostrings Package

Efficient manipulation of biological sequences.

## Create Sequences

```r
library(Biostrings)

# DNA
dna <- DNAString("ATGCGATCGATCG")
dna_set <- DNAStringSet(c("ATGC", "GCTA", "TTAA"))

# RNA
rna <- RNAString("AUGCGAUCGAUCG")

# Amino acids
aa <- AAString("MKTAYIAKQRQISFVKSHFSRQLEERLGLIEVQAPILSRVGDGTQDNLSGAEKAVQVKVKALPDAQFEVVHSLAKWKRQQIAAALEHHHHHH")
```

## Read FASTA

```r
# Read
seqs <- readDNAStringSet("sequences.fasta")
seqs <- readAAStringSet("proteins.fasta")

# Write
writeXStringSet(seqs, "output.fasta")
```

## Basic Operations

```r
# Length
length(dna)
width(dna_set)

# Subset
subseq(dna, start = 1, end = 10)
dna[1:10]

# Reverse complement
reverseComplement(dna)

# Translate
translate(dna)
```

## Pattern Matching

```r
# Find pattern
matchPattern("ATG", dna)

# Count
countPattern("ATG", dna)

# Multiple patterns
vmatchPattern("ATG", dna_set)

# With mismatches
matchPattern("ATG", dna, max.mismatch = 1)
```

## Alignment

```r
# Pairwise alignment
pairwiseAlignment(pattern, subject,
  type = "global",
  substitutionMatrix = "BLOSUM62"
)

# Score
score(alignment)

# Aligned sequences
aligned(alignment)
```

## Sequence Statistics

```r
# Letter frequency
letterFrequency(dna, letters = c("A", "T", "G", "C"))

# Dinucleotide frequency
dinucleotideFrequency(dna)

# GC content
letterFrequency(dna, "GC", as.prob = TRUE)

# Oligonucleotide frequency
oligonucleotideFrequency(dna, width = 3)
```

## Consensus

```r
# Consensus matrix
consensusMatrix(dna_set)

# Consensus string
consensusString(dna_set)
```
