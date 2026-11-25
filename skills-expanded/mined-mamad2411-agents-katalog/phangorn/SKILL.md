---
name: phangorn
description: R phangorn package for phylogenetic analysis. Use for phylogenetic reconstruction and analysis.
---

# phangorn

Phylogenetic analysis in R.

## Reading Data

```r
library(phangorn)

# Read alignment
alignment <- read.phyDat("alignment.fasta", format = "fasta")

# Read Nexus
alignment <- read.phyDat("alignment.nex", format = "nexus")

# From ape
library(ape)
dna <- read.dna("alignment.fasta", format = "fasta")
alignment <- as.phyDat(dna)
```

## Distance Methods

```r
# Compute distance matrix
dm <- dist.ml(alignment)

# Different models
dm <- dist.ml(alignment, model = "JC69")
dm <- dist.ml(alignment, model = "K80")
dm <- dist.ml(alignment, model = "F81")
dm <- dist.ml(alignment, model = "GTR")

# Neighbor-joining tree
tree_nj <- NJ(dm)

# UPGMA tree
tree_upgma <- upgma(dm)
```

## Maximum Parsimony

```r
# Parsimony score
parsimony(tree, alignment)

# Parsimony search
tree_mp <- pratchet(alignment)

# With rearrangements
tree_mp <- pratchet(alignment,
  minit = 100,
  maxit = 1000,
  k = 10)
```

## Maximum Likelihood

```r
# Fit model
fit <- pml(tree, alignment)

# Optimize
fit_opt <- optim.pml(fit,
  model = "GTR",
  optInv = TRUE,
  optGamma = TRUE)

# Model test
mt <- modelTest(alignment)
```

## Bootstrap

```r
# Bootstrap analysis
bs <- bootstrap.pml(fit_opt,
  bs = 100,
  optNni = TRUE)

# Plot with bootstrap values
plotBS(tree, bs, type = "phylogram")
```

## Tree Manipulation

```r
# Root tree
tree_rooted <- root(tree, outgroup = "species1")

# Midpoint rooting
tree_mid <- midpoint(tree)

# Consensus tree
consensus_tree <- consensus(trees, p = 0.5)
```

## Ancestral States

```r
# Ancestral state reconstruction
anc <- ancestral.pml(fit_opt, type = "ml")

# Plot
plotAnc(anc, 1)
```

## Model Comparison

```r
# AIC comparison
AIC(fit1, fit2)

# Likelihood ratio test
anova(fit1, fit2)
```
