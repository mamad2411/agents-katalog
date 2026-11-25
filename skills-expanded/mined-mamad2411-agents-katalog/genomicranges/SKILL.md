---
name: GenomicRanges
description: R GenomicRanges package for genomic intervals. Use for representing and manipulating genomic coordinates.
---

# GenomicRanges Package

Representation and manipulation of genomic intervals.

## GRanges Object

```r
library(GenomicRanges)

# Create GRanges
gr <- GRanges(
  seqnames = c("chr1", "chr1", "chr2"),
  ranges = IRanges(start = c(100, 200, 150), end = c(150, 250, 200)),
  strand = c("+", "-", "+"),
  score = c(1.5, 2.0, 3.0)
)

# From data frame
gr <- makeGRangesFromDataFrame(df,
  seqnames.field = "chr",
  start.field = "start",
  end.field = "end"
)
```

## Accessors

```r
seqnames(gr)
start(gr)
end(gr)
width(gr)
strand(gr)
ranges(gr)
mcols(gr)  # Metadata columns
gr$score   # Access metadata
```

## Subsetting

```r
gr[1:5]
gr[seqnames(gr) == "chr1"]
gr[strand(gr) == "+"]
gr[gr$score > 2]
```

## Operations

```r
# Shift
shift(gr, 100)

# Resize
resize(gr, width = 500, fix = "start")

# Flank
flank(gr, width = 100, start = TRUE)

# Promoters
promoters(gr, upstream = 2000, downstream = 200)

# Reduce (merge overlapping)
reduce(gr)

# Disjoin
disjoin(gr)
```

## Overlaps

```r
# Find overlaps
hits <- findOverlaps(query, subject)

# Subset by overlap
subsetByOverlaps(gr1, gr2)

# Count overlaps
countOverlaps(gr1, gr2)

# Overlap operations
intersect(gr1, gr2)
union(gr1, gr2)
setdiff(gr1, gr2)
```

## GRangesList

```r
grl <- GRangesList(gene1 = gr1, gene2 = gr2)
grl[[1]]
unlist(grl)
```

## Import/Export

```r
library(rtracklayer)
gr <- import("file.bed")
export(gr, "output.bed")
```
