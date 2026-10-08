---
name: r-analytics
description: R language data analysis and visualization skill. Use when user asks to (1) run R scripts or code, (2) install/update R packages, (3) perform data analysis with R, (4) create visualizations with ggplot2/plotly, (5) statistical analysis, (6) data manipulation with tidyverse/dplyr/data.table. Triggers on keywords like "R语言", "R脚本", "ggplot", "tidyverse", "数据分析", "可视化".
---

# R Analytics

R language data analysis and visualization toolkit.

## Quick Reference

### Run R Code

```bash
# Run inline code
Rscript -e 'print("Hello R")'

# Run script file
Rscript script.R

# Run with arguments
Rscript script.R arg1 arg2
```

### Package Management

```bash
# Update all packages
Rscript -e 'options(repos = c(CRAN = "https://cloud.r-project.org")); update.packages(ask = FALSE, checkBuilt = TRUE)'

# Install package
Rscript -e 'install.packages("tidyverse", repos = "https://cloud.r-project.org")'

# Install multiple packages
Rscript -e 'install.packages(c("ggplot2", "dplyr", "tidyr"), repos = "https://cloud.r-project.org")'
```

## Data Analysis Workflow

### 1. Load Data

```r
# CSV
df <- read.csv("data.csv")
df <- readr::read_csv("data.csv")  # faster, tibble output

# Excel
df <- readxl::read_excel("data.xlsx", sheet = 1)

# JSON
df <- jsonlite::fromJSON("data.json")
```

### 2. Data Manipulation (dplyr)

```r
library(dplyr)

df %>%
  filter(column > 10) %>%           # filter rows
  select(col1, col2) %>%            # select columns
  mutate(new_col = col1 * 2) %>%    # create column
  group_by(category) %>%            # group
  summarise(mean_val = mean(value)) # aggregate
```

### 3. Visualization (ggplot2)

```r
library(ggplot2)

# Scatter plot
ggplot(df, aes(x = x_col, y = y_col)) +
  geom_point() +
  labs(title = "Title", x = "X Label", y = "Y Label") +
  theme_minimal()

# Bar chart
ggplot(df, aes(x = category, y = value, fill = category)) +
  geom_bar(stat = "identity") +
  theme_minimal()

# Line chart
ggplot(df, aes(x = date, y = value, color = group)) +
  geom_line() +
  theme_minimal()

# Save plot
ggsave("plot.png", width = 10, height = 6, dpi = 300)
ggsave("plot.pdf", width = 10, height = 6)
```

### 4. Statistical Analysis

```r
# Summary statistics
summary(df)

# Correlation
cor(df$x, df$y)
cor.test(df$x, df$y)

# Linear regression
model <- lm(y ~ x1 + x2, data = df)
summary(model)

# T-test
t.test(group1, group2)

# ANOVA
aov_result <- aov(value ~ group, data = df)
summary(aov_result)
```

## Common Packages

| Package | Purpose |
|---------|---------|
| tidyverse | Meta-package: ggplot2, dplyr, tidyr, readr, etc. |
| ggplot2 | Visualization |
| dplyr | Data manipulation |
| tidyr | Data tidying |
| readr | Fast CSV reading |
| readxl | Excel files |
| data.table | Fast data manipulation |
| plotly | Interactive plots |
| shiny | Web apps |
| rmarkdown | Reports |

## Output Formats

```r
# Save data
write.csv(df, "output.csv", row.names = FALSE)
readr::write_csv(df, "output.csv")

# Save R object
saveRDS(obj, "data.rds")
obj <- readRDS("data.rds")
```

## Resources

### Scripts
- **scripts/update_packages.R** - Update all installed packages

### References

**Quick Reference:**
- **references/packages.md** - Common packages quick reference
- **references/awesome-packages.md** - Curated packages by domain (ML, viz, web, finance, etc.)
- **references/resources-index.md** - URLs, cheat sheets, community resources

**R for Data Science (2e)** - Tidyverse workflow:
| File | Topics |
|------|--------|
| **references/r4ds-1-visualize.md** | ggplot2: geoms, aesthetics, facets, scales, themes |
| **references/r4ds-2-transform.md** | dplyr: filter, select, mutate, summarize, group_by |
| **references/r4ds-3-wrangle.md** | tidyr (pivot), stringr, forcats, lubridate |
| **references/r4ds-4-import.md** | readr, readxl, joins, binding |
| **references/r4ds-5-program.md** | Functions, across(), map(), iteration |

**Advanced R (2e)** - Deep R programming:
| File | Topics |
|------|--------|
| **references/advr-1-foundations.md** | Names/values, vectors, subsetting, control flow, functions, environments, conditions |
| **references/advr-2-functional.md** | Functionals (map/reduce), function factories, function operators |
| **references/advr-3-oop.md** | S3, R6, S4 object-oriented programming |
| **references/advr-4-metaprogramming.md** | Expressions, quasiquotation, evaluation, code translation |
| **references/advr-5-techniques.md** | Debugging, profiling, performance optimization, Rcpp |

**R Graphics Cookbook** - Visualization recipes:
- **references/graphics-cookbook.md** - Bar graphs, line graphs, scatter plots, distributions, annotations, colors

**Ecosystems:**
- **references/tidyverse-ecosystem.md** - Core packages, import tools, modeling, patterns
- **references/bioconductor.md** - Installation, GenomicRanges, RNA-seq, annotation

### Sub-Skills (Domain-Specific)

| Sub-Skill | Description |
|-----------|-------------|
| **sub-skills/r-data/** | Data manipulation, formats, databases (dplyr, data.table, DBI) |
| **sub-skills/r-viz/** | Visualization (ggplot2, plotly, leaflet, HTML widgets) |
| **sub-skills/r-ml/** | Machine learning (tidymodels, xgboost, caret, deep learning) |
| **sub-skills/r-nlp/** | Natural language processing (tidytext, quanteda, tm) |
| **sub-skills/r-web/** | Web technologies & reproducible research (Shiny, rmarkdown) |
| **sub-skills/r-stats/** | Bayesian analysis, optimization, finance (Stan, quantmod) |
| **sub-skills/r-bio/** | Bioinformatics (Bioconductor, DESeq2, GenomicRanges) |
| **sub-skills/r-network/** | Network analysis (igraph, tidygraph, visNetwork) |
| **sub-skills/r-spatial/** | Spatial analysis (sf, terra, leaflet, tmap) |
| **sub-skills/r-dev/** | R development (devtools, testthat, roxygen2, Rcpp) |
| **sub-skills/r-parallel/** | Parallel computing & performance (future, Rcpp, Spark) |
| **sub-skills/r-resources/** | Learning resources (books, courses, cheat sheets) |
