---
name: ape
description: R ape package for phylogenetic analysis. Use for reading, writing, and analyzing phylogenetic trees.
---

# ape

Analyses of Phylogenetics and Evolution.

## Reading Trees

```r
library(ape)

# Read Newick format
tree <- read.tree("tree.nwk")
tree <- read.tree(text = "((A:0.1,B:0.2):0.3,C:0.4);")

# Read Nexus format
tree <- read.nexus("tree.nex")

# Multiple trees
trees <- read.tree("trees.nwk")
```

## Tree Structure

```r
# Tree components
tree$tip.label      # Tip names
tree$edge           # Edge matrix
tree$edge.length    # Branch lengths
tree$Nnode          # Number of internal nodes

# Number of tips
Ntip(tree)

# Number of nodes
Nnode(tree)
```

## Plotting Trees

```r
# Basic plot
plot(tree)

# Phylogram
plot(tree, type = "phylogram")

# Cladogram
plot(tree, type = "cladogram")

# Fan/radial
plot(tree, type = "fan")

# Unrooted
plot(tree, type = "unrooted")

# With options
plot(tree,
     show.tip.label = TRUE,
     tip.color = "blue",
     edge.color = "gray",
     edge.width = 2,
     cex = 0.8
)

# Add scale bar
add.scale.bar()
```

## Tree Manipulation

```r
# Root tree
rooted <- root(tree, outgroup = "A")
rooted <- root(tree, node = 5)

# Unroot tree
unrooted <- unroot(tree)

# Drop tips
pruned <- drop.tip(tree, c("A", "B"))

# Keep tips
kept <- keep.tip(tree, c("C", "D", "E"))

# Rotate nodes
rotated <- rotate(tree, node = 5)

# Ladderize
ladderized <- ladderize(tree)
```

## Distance Matrices

```r
# Compute pairwise distances
dist_matrix <- cophenetic(tree)

# From sequences
library(ape)
dna <- read.dna("sequences.fasta", format = "fasta")
dist_matrix <- dist.dna(dna, model = "K80")
```

## Tree Building

```r
# Neighbor-joining
nj_tree <- nj(dist_matrix)

# UPGMA
upgma_tree <- hclust(as.dist(dist_matrix), method = "average")
upgma_tree <- as.phylo(upgma_tree)

# Minimum evolution
me_tree <- fastme.bal(dist_matrix)
```

## Bootstrap

```r
# Bootstrap analysis
boot_trees <- boot.phylo(tree, dna, function(x) nj(dist.dna(x)),
                         B = 100, trees = TRUE)

# Plot with bootstrap values
plot(tree)
nodelabels(boot_trees$BP, cex = 0.7)
```

## Comparative Methods

```r
# Phylogenetic independent contrasts
pic_result <- pic(trait, tree)

# Ancestral state reconstruction
anc <- ace(trait, tree, type = "continuous")
anc <- ace(trait, tree, type = "discrete")

# Plot ancestral states
plot(tree)
nodelabels(pie = anc$lik.anc, cex = 0.5)
```

## Writing Trees

```r
# Write Newick
write.tree(tree, file = "output.nwk")

# Write Nexus
write.nexus(tree, file = "output.nex")

# As text
write.tree(tree)
```

## Tree Comparison

```r
# Robinson-Foulds distance
RF.dist(tree1, tree2)

# Cophenetic correlation
cor(cophenetic(tree1), cophenetic(tree2))
```

## Sequence Data

```r
# Read sequences
dna <- read.dna("sequences.fasta", format = "fasta")
dna <- read.dna("sequences.phy", format = "sequential")

# Write sequences
write.dna(dna, file = "output.fasta", format = "fasta")

# Sequence statistics
base.freq(dna)
GC.content(dna)
```
