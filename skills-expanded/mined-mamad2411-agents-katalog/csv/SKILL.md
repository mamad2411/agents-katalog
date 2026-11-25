---
name: csv
description: Analyze and transform CSV data using bash tools
---

# CSV Processing Skill

Process CSV files using standard bash tools (awk, cut, sort, grep).

## Available Scripts

### analyze.sh
Get statistics and summary of a CSV file.
```bash
bash /sandbox/skills/csv/scripts/analyze.sh data.csv
```

### filter.sh
Filter rows where a column matches a value.
```bash
bash /sandbox/skills/csv/scripts/filter.sh data.csv <column_number> <value>
```

### select.sh
Select specific columns from CSV.
```bash
bash /sandbox/skills/csv/scripts/select.sh data.csv <columns>
```

### sort.sh
Sort CSV by a column.
```bash
bash /sandbox/skills/csv/scripts/sort.sh data.csv <column_number> [--numeric] [--reverse]
```

## Examples

```bash
# Show CSV summary
bash /sandbox/skills/csv/scripts/analyze.sh sales.csv

# Filter where column 3 equals "active"
bash /sandbox/skills/csv/scripts/filter.sh users.csv 3 active

# Select columns 1, 2, and 4
bash /sandbox/skills/csv/scripts/select.sh data.csv 1,2,4

# Sort by column 2 numerically in reverse
bash /sandbox/skills/csv/scripts/sort.sh data.csv 2 --numeric --reverse
```
