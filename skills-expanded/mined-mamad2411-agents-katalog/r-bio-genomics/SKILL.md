---
name: r-bio-genomics
description: R genomics with GenomicRanges, Biostrings. Use for genomic intervals, sequences, and annotations.
---

# R Genomics

Genomic data structures and operations.

## GenomicRanges

```r
library(GenomicRanges)

# Create GRanges
gr <- GRanges(
  seqnames = c("chr1", "chr1", "chr2"),
  ranges = IRanges(start = c(100, 200, 150), width = 50),
  strand = c("+", "-", "+"),
  score = c(1.5, 2.0, 3.0)
)

# Accessors
seqnames(gr); start(gr); end(gr); width(gr); strand(gr)
mcols(gr)  # Metadata columns

# Operations
shift(gr, 10)
resize(gr, width = 100)
flank(gr, width = 50)
reduce(gr)  # Merge overlapping

# Overlaps
findOverlaps(gr1, gr2)
subsetByOverlaps(gr1, gr2)
countOverlaps(gr1, gr2)

# Set operations
union(gr1, gr2)
intersect(gr1, gr2)
setdiff(gr1, gr2)
```

## Biostrings

```r
library(Biostrings)

# DNA sequences
dna <- DNAStringSet(c("ATCGATCG", "GCTAGCTA"))
reverseComplement(dna)
translate(dna)

# Pattern matching
matchPattern("ATG", dna[[1]])
vmatchPattern("ATG", dna)
countPattern("ATG", dna)

# Alignment
pairwiseAlignment(pattern, subject, type = "global")
```

## Annotation

```r
library(org.Hs.eg.db)

# Map IDs
mapIds(org.Hs.eg.db, keys = genes, column = "SYMBOL", keytype = "ENSEMBL")

# Select
select(org.Hs.eg.db, keys = genes, columns = c("SYMBOL", "GENENAME"), keytype = "ENSEMBL")

# TxDb for transcripts
library(TxDb.Hsapiens.UCSC.hg38.knownGene)
txdb <- TxDb.Hsapiens.UCSC.hg38.knownGene
genes(txdb)
transcripts(txdb)
exons(txdb)
```
