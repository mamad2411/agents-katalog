---
name: pheatmap
description: R pheatmap package for heatmaps. Use for creating publication-quality heatmaps with clustering.
---

# pheatmap

Pretty heatmaps with clustering.

## Basic Heatmap

```r
library(pheatmap)

# From matrix
mat <- matrix(rnorm(100), nrow = 10)
rownames(mat) <- paste0("Gene", 1:10)
colnames(mat) <- paste0("Sample", 1:10)

pheatmap(mat)
```

## Clustering

```r
# With clustering (default)
pheatmap(mat, cluster_rows = TRUE, cluster_cols = TRUE)

# Without clustering
pheatmap(mat, cluster_rows = FALSE, cluster_cols = FALSE)

# Clustering method
pheatmap(mat, clustering_method = "complete")  # complete, average, ward.D2

# Clustering distance
pheatmap(mat, clustering_distance_rows = "euclidean")
pheatmap(mat, clustering_distance_cols = "correlation")
```

## Colors

```r
# Color palette
pheatmap(mat, color = colorRampPalette(c("blue", "white", "red"))(100))

# Breaks
pheatmap(mat, breaks = seq(-3, 3, length.out = 101))

# Color for NA
pheatmap(mat, na_col = "grey")
```

## Annotations

```r
# Row annotations
row_annotation <- data.frame(
  Group = c(rep("A", 5), rep("B", 5)),
  row.names = rownames(mat)
)

pheatmap(mat, annotation_row = row_annotation)

# Column annotations
col_annotation <- data.frame(
  Treatment = c(rep("Control", 5), rep("Treated", 5)),
  row.names = colnames(mat)
)

pheatmap(mat, annotation_col = col_annotation)

# Both
pheatmap(mat,
         annotation_row = row_annotation,
         annotation_col = col_annotation)
```

## Annotation Colors

```r
# Custom annotation colors
ann_colors <- list(
  Group = c(A = "red", B = "blue"),
  Treatment = c(Control = "white", Treated = "black")
)

pheatmap(mat,
         annotation_row = row_annotation,
         annotation_col = col_annotation,
         annotation_colors = ann_colors)
```

## Display Options

```r
pheatmap(mat,
  # Cell labels
  display_numbers = TRUE,
  number_format = "%.2f",
  number_color = "black",
  fontsize_number = 8,

  # Cell size
  cellwidth = 20,
  cellheight = 20,

  # Font sizes
  fontsize = 10,
  fontsize_row = 8,
  fontsize_col = 8,

  # Borders
  border_color = "grey60",

  # Legend
  legend = TRUE,
  legend_breaks = c(-2, 0, 2),
  legend_labels = c("Low", "Mid", "High")
)
```

## Gaps

```r
# Add gaps between groups
pheatmap(mat,
         gaps_row = c(5),      # Gap after row 5
         gaps_col = c(3, 7),   # Gaps after cols 3 and 7
         cutree_rows = 2,      # Cut dendrogram into 2 clusters
         cutree_cols = 3)
```

## Scaling

```r
# Scale by row (z-score)
pheatmap(mat, scale = "row")

# Scale by column
pheatmap(mat, scale = "column")

# No scaling (default)
pheatmap(mat, scale = "none")
```

## Dendrogram

```r
# Show/hide dendrograms
pheatmap(mat,
         treeheight_row = 50,
         treeheight_col = 50)

# Hide dendrogram but keep clustering
pheatmap(mat, treeheight_row = 0, treeheight_col = 0)
```

## Labels

```r
# Custom labels
pheatmap(mat,
         labels_row = paste0("G", 1:10),
         labels_col = paste0("S", 1:10))

# Hide labels
pheatmap(mat, show_rownames = FALSE, show_colnames = FALSE)

# Rotate column labels
pheatmap(mat, angle_col = 45)
```

## Saving

```r
# Save to file
pheatmap(mat, filename = "heatmap.pdf", width = 8, height = 10)
pheatmap(mat, filename = "heatmap.png", width = 800, height = 1000)

# Get plot object
p <- pheatmap(mat)

# Access clustering results
p$tree_row
p$tree_col
```

## Custom Clustering

```r
# Pre-computed clustering
row_clust <- hclust(dist(mat))
col_clust <- hclust(dist(t(mat)))

pheatmap(mat,
         cluster_rows = row_clust,
         cluster_cols = col_clust)
```
