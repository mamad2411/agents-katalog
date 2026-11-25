---
name: Bioconductor
description: R Bioconductor ecosystem for bioinformatics. Use for genomics, proteomics, and bioinformatics analysis.
---

# Bioconductor

Open source software for bioinformatics.

## Installation

```r
# Install BiocManager
install.packages("BiocManager")

# Install Bioconductor packages
BiocManager::install("GenomicRanges")
BiocManager::install(c("DESeq2", "edgeR"))

# Check version
BiocManager::version()

# Update packages
BiocManager::install()
```

## Core Packages

```r
# Genomic ranges
library(GenomicRanges)
library(IRanges)

# Sequences
library(Biostrings)

# Annotations
library(AnnotationDbi)
library(org.Hs.eg.db)

# RNA-seq
library(DESeq2)
library(edgeR)
```

## GenomicRanges

```r
library(GenomicRanges)

# Create GRanges
gr <- GRanges(
  seqnames = c("chr1", "chr1", "chr2"),
  ranges = IRanges(start = c(1, 100, 200), end = c(50, 150, 250)),
  strand = c("+", "-", "+")
)

# Operations
findOverlaps(gr1, gr2)
subsetByOverlaps(gr1, gr2)
reduce(gr)
```

## Biostrings

```r
library(Biostrings)

# DNA sequences
dna <- DNAString("ATCGATCG")
reverseComplement(dna)
translate(dna)

# Pattern matching
matchPattern("ATG", dna)
vmatchPattern("ATG", dna_set)
```

## Annotation

```r
library(org.Hs.eg.db)

# Map gene IDs
mapIds(org.Hs.eg.db,
  keys = gene_ids,
  column = "SYMBOL",
  keytype = "ENTREZID")

# Available columns
columns(org.Hs.eg.db)
keytypes(org.Hs.eg.db)
```

## SummarizedExperiment

```r
library(SummarizedExperiment)

# Create
se <- SummarizedExperiment(
  assays = list(counts = count_matrix),
  colData = sample_info,
  rowData = gene_info
)

# Access
assay(se)
colData(se)
rowData(se)
```

## Finding Packages

```r
# Search for packages
BiocManager::available("RNA")

# Package info
BiocManager::install("BiocPkgTools")
library(BiocPkgTools)
biocPkgList()
```
