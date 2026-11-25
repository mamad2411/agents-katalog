---
name: r-bio-phylo
description: R phylogenetics with ape, ggtree. Use for phylogenetic trees and evolutionary analysis.
---

# R Phylogenetics

Phylogenetic analysis and visualization.

## ape

```r
library(ape)

# Read tree
tree <- read.tree("tree.nwk")
tree <- read.nexus("tree.nex")

# Plot
plot(tree)
plot(tree, type = "fan")
plot(tree, type = "cladogram")

# Tree manipulation
drop.tip(tree, c("species1", "species2"))
root(tree, outgroup = "outgroup")
ladderize(tree)

# Distance
cophenetic(tree)
dist.nodes(tree)

# Bootstrap
boot.phylo(tree, data, FUN, B = 100)
```

## ggtree

```r
library(ggtree)

# Basic tree
ggtree(tree) + geom_tiplab()

# Circular
ggtree(tree, layout = "circular") + geom_tiplab()

# With data
ggtree(tree) %<+% metadata +
  geom_tippoint(aes(color = group)) +
  geom_tiplab(aes(label = name))

# Heatmap
gheatmap(ggtree(tree), data, width = 0.3)

# Annotations
ggtree(tree) +
  geom_hilight(node = 10, fill = "blue", alpha = 0.3) +
  geom_cladelabel(node = 10, label = "Clade A")
```

## phangorn

```r
library(phangorn)

# Parsimony
pars <- parsimony(tree, data)
tree_pars <- optim.parsimony(tree, data)

# Maximum likelihood
fit <- pml(tree, data)
fit <- optim.pml(fit, model = "GTR")

# Bootstrap
bs <- bootstrap.pml(fit, bs = 100)
plotBS(tree, bs)
```
