---
name: databricks-lakeview-dashboard
description: Programmatically create and manage Lakeview dashboards in Databricks
---

# Databricks Lakeview Dashboard Skill

This skill enables programmatic creation of beautiful Lakeview dashboards in Databricks using the Dashboard API.

## MANDATORY VALIDATION WORKFLOW

**You MUST follow this workflow exactly. Skipping validation causes broken dashboards.**

```
STEP 1: Get table schemas (use Databricks CLI or SQL DESCRIBE)
STEP 2: Write SQL queries for each dataset
STEP 3: TEST EVERY QUERY before building the dashboard
        - Run each query against the warehouse
        - If a query fails, FIX IT before proceeding
        - Verify column names match what widgets will reference
        - Verify data types are correct (dates, numbers, strings)
STEP 4: Build dashboard JSON using ONLY verified queries
STEP 5: Deploy via the Lakeview API
```

**WARNING: If you deploy without testing queries, widgets WILL show "Invalid widget definition" errors!**

## Prerequisites

1. Databricks CLI authenticated: `databricks auth login --profile <profile>`
2. SQL warehouse available for dashboard queries
3. Unity Catalog tables/views for data sources

## Choosing the Right Visualization Type

> **Important:** Before creating any visualization, think carefully about what chart type best represents your data. Not everything should be a bar chart! Consider the data pattern, the story you want to tell, and the audience.

### Visualization Selection Guide

| Data Pattern | Best Visualization | When to Use |
|-------------|-------------------|-------------|
| **Trend over time** | Line, Area | Showing how metrics change over days/weeks/months |
| **Comparing categories** | Bar (horizontal for many categories) | Comparing values across distinct groups |
| **Part of a whole** | Pie, Funnel | Showing proportions that sum to 100% |
| **Distribution** | Histogram, Box | Understanding data spread, quartiles, outliers |
| **Relationship between variables** | Scatter, Bubble | Correlation analysis, finding patterns |
| **Geographic data** | Choropleth Map, Point Map | Regional comparisons, location-based insights |
| **Flow/Process stages** | Sankey, Funnel | Conversion tracking, user journeys, data flow |
| **Single KPI** | Counter | Highlighting one important metric |
| **Cumulative changes** | Waterfall | Financial analysis, showing positive/negative contributions |
| **Two metrics on different scales** | Combo (dual-axis) | Comparing revenue vs. count, etc. |
| **Retention/Cohort analysis** | Cohort | User retention over time by signup cohort |
| **Pattern in 2D categories** | Heatmap | Finding hotspots in category intersections |
| **Detailed data exploration** | Table, Pivot | When users need to see raw values |

### Available Visualization Types in Lakeview

1. **Area** - Combines line and bar to show cumulative changes over time across groups
2. **Bar** - Compare values across categories; supports stacked, 100% stacked, or grouped
3. **Box** - Show distribution summaries with quartiles; identify outliers
4. **Bubble** - Scatter with size dimension; visualize 3 variables at once
5. **Choropleth Map** - Color regions (countries, states) by aggregate values
6. **Cohort** - Track user retention and behavior patterns over time
7. **Combo** - Mix line and bar on dual axes for different scales
8. **Counter** - Display a single prominent value (KPI)
9. **Funnel** - Analyze metric changes through sequential stages
10. **Heatmap** - Use color intensity to show values in a grid
11. **Histogram** - Plot frequency distribution of values
12. **Line** - Standard time series and trend analysis
13. **Pie** - Show proportions (avoid for time series or many categories)
14. **Pivot** - Tabular summaries with conditional formatting
15. **Point Map** - Plot data at lat/long coordinates
16. **Sankey** - Visualize flow between stages
17. **Scatter** - Show relationship between two numeric variables
18. **Table** - Raw data display with formatting
19. **Waterfall** - Show cumulative effect of sequential values

### Anti-Patterns to Avoid

- **Pie charts with many slices** - Use bar chart if more than 5-6 categories
- **Bar charts for time series** - Use line chart to show trends over time
- **Line charts for categorical data** - Use bar chart for discrete categories
- **Tables when a visual would be clearer** - Reserve tables for detail views
- **Multiple counters when comparison matters** - Use bar chart to enable comparison

Reference: [Databricks Lakeview Visualization Types Documentation](https://docs.databricks.com/en/dashboards/lakeview-visualization-types.html)

## API Endpoints

### Create Dashboard
```bash
databricks api post /api/2.0/lakeview/dashboards --profile <profile> --json '{
  "display_name": "My Dashboard",
  "warehouse_id": "<warehouse_id>",
  "parent_path": "/Users/<email>",
  "serialized_dashboard": "<json_string>"
}'
```

### Update Dashboard
```bash
databricks api patch /api/2.0/lakeview/dashboards/<dashboard_id> --profile <profile> --json '{
  "display_name": "Updated Name",
  "serialized_dashboard": "<json_string>"
}'
```

### Get Dashboard
```bash
databricks api get /api/2.0/lakeview/dashboards/<dashboard_id> --profile <profile>
```

### List Dashboards
```bash
databricks api get /api/2.0/lakeview/dashboards --profile <profile>
```

### Publish Dashboard
```bash
databricks api post /api/2.0/lakeview/dashboards/<dashboard_id>/published --profile <profile>
```

## Serialized Dashboard Schema

The `serialized_dashboard` is a JSON string with this structure:

```json
{
  "datasets": [...],
  "pages": [...],
  "uiSettings": {...}
}
```

### Dataset Architecture (STRICT)

- **One dataset per domain** (e.g., orders, customers, products)
- **Exactly ONE valid SQL query per dataset** (no multiple queries separated by `;`)
- Always use **fully-qualified table names**: `catalog.schema.table_name`
- SELECT must include all dimensions needed by widgets and all derived columns via `AS` aliases
- Put ALL business logic (CASE/WHEN, COALESCE, ratios) into the dataset SELECT with explicit aliases
- **Contract rule**: Every widget `fieldName` must exactly match a dataset column or alias

```json
{
  "datasets": [
    {
      "name": "unique_id_123",
      "displayName": "Sales Data",
      "queryLines": [
        "SELECT * FROM catalog.schema.table"
      ]
    }
  ]
}
```

> **Critical: `queryLines` Array Formatting**
>
> The array elements are concatenated **without any separator**. Each element must end with a space or newline to prevent SQL syntax errors.
>
> **Correct** (single string):
> ```json
> "queryLines": [
>   "SELECT col1, SUM(amount) as total FROM catalog.schema.table GROUP BY col1"
> ]
> ```
>
> **Correct** (multi-line with trailing spaces):
> ```json
> "queryLines": [
>   "SELECT col1, SUM(amount) as total ",
>   "FROM catalog.schema.table ",
>   "GROUP BY col1"
> ]
> ```
>
> **Incorrect** (missing spaces - causes `totalFROM` error):
> ```json
> "queryLines": [
>   "SELECT col1, SUM(amount) as total",
>   "FROM catalog.schema.table",
>   "GROUP BY col1"
> ]
> ```

### Spark SQL Patterns

- Date math: `date_sub(current_date(), N)` for days, `add_months(current_date(), -N)` for months
- Date truncation: `DATE_TRUNC('DAY'|'WEEK'|'MONTH'|'QUARTER'|'YEAR', column)`
- **AVOID** `INTERVAL` syntax - use functions instead

### Pages

Pages contain the layout of widgets:

```json
{
  "pages": [
    {
      "name": "page_id_123",
      "displayName": "Overview",
      "pageType": "PAGE_TYPE_CANVAS",
      "layout": [...]
    }
  ]
}
```

### Layout and Positioning (6-Column Grid, NO GAPS)

Widgets are positioned on a 6-column grid. **Each row must fill width=6 exactly. No gaps allowed.**

```json
{
  "layout": [
    {
      "widget": {...},
      "position": {
        "x": 0,       // Column (0-5)
        "y": 0,       // Row
        "width": 2,   // Columns to span (1-6)
        "height": 3   // Rows to span
      }
    }
  ]
}
```

**Recommended widget sizes:**

| Widget Type | Width | Height | Notes |
|-------------|-------|--------|-------|
| Text header | 6 | 1 | Full width; use SEPARATE widgets for title and subtitle |
| Counter/KPI | 2 | **3-4** | **NEVER height=2** - too cramped! |
| Line/Bar chart | 3 | **5-6** | Pair side-by-side to fill row |
| Pie chart | 3 | **5-6** | Needs space for legend |
| Full-width chart | 6 | 5-7 | For detailed time series |
| Table | 6 | 5-8 | Full width for readability |

**Standard dashboard structure:**
```text
y=0:  Title (w=6, h=1) - Dashboard title (use separate widget!)
y=1:  Subtitle (w=6, h=1) - Description (use separate widget!)
y=2:  KPIs (w=2 each, h=3) - 3 key metrics side-by-side
y=5:  Section header (w=6, h=1) - "Trends" or similar
y=6:  Charts (w=3 each, h=5) - Two charts side-by-side
y=11: Section header (w=6, h=1) - "Details"
y=12: Table (w=6, h=6) - Detailed data
```

### Cardinality and Readability

**Dashboard readability depends on limiting distinct values:**

| Dimension Type | Max Values | Examples |
|----------------|------------|----------|
| Chart color/groups | **3-8** | 4 regions, 5 product lines, 3 tiers |
| Filters | 4-10 | 8 countries, 5 channels |
| High cardinality | **Table only** | customer_id, order_id, SKU |

**Before creating any chart with color/grouping:**
1. Check column cardinality
2. If >10 distinct values, aggregate to higher level OR use TOP-N + "Other" bucket
3. For high-cardinality dimensions, use a table widget instead of a chart

## Widget Field Expressions

> **CRITICAL: Field Name Matching Rule**
> The `name` in `query.fields` MUST exactly match the `fieldName` in `encodings`.
> If they don't match, the widget shows "no selected fields to visualize" error!

**Correct pattern for aggregations:**
```json
// In query.fields:
{"name": "sum(spend)", "expression": "SUM(`spend`)"}

// In encodings (must match!):
{"fieldName": "sum(spend)", "displayName": "Total Spend"}
```

**WRONG - names don't match:**
```json
// In query.fields:
{"name": "spend", "expression": "SUM(`spend`)"}  // name is "spend"

// In encodings:
{"fieldName": "sum(spend)", ...}  // ERROR: "sum(spend)" != "spend"
```

Allowed expressions in widget queries (you CANNOT use CAST or other SQL in expressions):

**For numbers:**
```json
{"name": "sum(revenue)", "expression": "SUM(`revenue`)"}
{"name": "avg(price)", "expression": "AVG(`price`)"}
{"name": "count(orders)", "expression": "COUNT(`order_id`)"}
{"name": "countdistinct(customers)", "expression": "COUNT(DISTINCT `customer_id`)"}
{"name": "min(date)", "expression": "MIN(`order_date`)"}
{"name": "max(date)", "expression": "MAX(`order_date`)"}
```

**For dates** (use daily for timeseries, weekly/monthly for grouped comparisons):
```json
{"name": "daily(date)", "expression": "DATE_TRUNC(\"DAY\", `date`)"}
{"name": "weekly(date)", "expression": "DATE_TRUNC(\"WEEK\", `date`)"}
{"name": "monthly(date)", "expression": "DATE_TRUNC(\"MONTH\", `date`)"}
```

**Simple field reference** (for pre-aggregated data):
```json
{"name": "category", "expression": "`category`"}
```

If you need conditional logic or multi-field formulas, compute a derived column in the dataset SQL first.

## Widget Specifications

**Widget Naming Convention:**
- `widget.name`: alphanumeric + hyphens + underscores ONLY (no spaces, parentheses, colons)
- `frame.title`: human-readable name (any characters allowed)
- `widget.queries[0].name`: always use `"main_query"`

**Version Requirements:**

| Widget Type | Version |
|-------------|---------|
| counter | 2 |
| table | 2 |
| filter-multi-select | 2 |
| filter-single-select | 2 |
| filter-date-range-picker | 2 |
| bar | 3 |
| line | 3 |
| area | 3 |
| pie | 3 |
| scatter | 3 |
| histogram | 3 |
| text | N/A (no spec block) |

---

### Text (Headers/Descriptions)

- **Text widgets do NOT use a spec block!**
- Use `multilineTextboxSpec` directly on the widget
- Supports markdown: `#`, `##`, `###`, `**bold**`, `*italic*`
- **Multiple items in the `lines` array are concatenated on a single line, NOT displayed as separate lines!**
- For title + subtitle, use **separate text widgets** at different y positions

```json
// CORRECT: Separate widgets for title and subtitle
{
  "widget": {
    "name": "title",
    "multilineTextboxSpec": {
      "lines": ["## Dashboard Title"]
    }
  },
  "position": {"x": 0, "y": 0, "width": 6, "height": 1}
},
{
  "widget": {
    "name": "subtitle",
    "multilineTextboxSpec": {
      "lines": ["Description text here"]
    }
  },
  "position": {"x": 0, "y": 1, "width": 6, "height": 1}
}

// WRONG: Multiple lines concatenate into one line!
{
  "widget": {
    "name": "title-widget",
    "multilineTextboxSpec": {
      "lines": ["## Dashboard Title", "Description text here"]
    }
  },
  "position": {"x": 0, "y": 0, "width": 6, "height": 2}
}
```

---

### Counter (KPI)

- `version`: **2** (NOT 3!)
- `widgetType`: "counter"
- **Percent values must be 0-1** in the data (not 0-100)

**Two patterns for counters:**

**Pattern 1: Pre-aggregated dataset (1 row, no filters)**
- Dataset returns exactly 1 row
- Use `"disaggregated": true` and simple field reference
- Field `name` matches dataset column directly

```json
{
  "widget": {
    "name": "total-revenue",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "summary_ds",
        "fields": [{"name": "revenue", "expression": "`revenue`"}],
        "disaggregated": true
      }
    }],
    "spec": {
      "version": 2,
      "widgetType": "counter",
      "encodings": {
        "value": {"fieldName": "revenue", "displayName": "Total Revenue"}
      },
      "frame": {"showTitle": true, "title": "Total Revenue"}
    }
  },
  "position": {"x": 0, "y": 0, "width": 2, "height": 3}
}
```

**Pattern 2: Aggregating widget (multi-row dataset, supports filters)**
- Dataset returns multiple rows (e.g., grouped by a filter dimension)
- Use `"disaggregated": false` and aggregation expression
- **Field `name` MUST match `fieldName` exactly** (e.g., `"sum(spend)"`)

```json
{
  "widget": {
    "name": "total-spend",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "by_category",
        "fields": [{"name": "sum(spend)", "expression": "SUM(`spend`)"}],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 2,
      "widgetType": "counter",
      "encodings": {
        "value": {"fieldName": "sum(spend)", "displayName": "Total Spend"}
      },
      "frame": {"showTitle": true, "title": "Total Spend"}
    }
  },
  "position": {"x": 0, "y": 0, "width": 2, "height": 3}
}
```

---

### Bar Chart

- `version`: **3**
- `widgetType`: "bar"
- **Stacked** (default): No `mark` field - bars stack on top of each other
- **Grouped**: Add `"mark": {"layout": "group"}` - bars side-by-side for comparison

```json
{
  "widget": {
    "name": "widget-id",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "dataset_id",
        "fields": [
          {"name": "category", "expression": "`category`"},
          {"name": "sum(amount)", "expression": "SUM(`amount`)"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "bar",
      "encodings": {
        "x": {
          "fieldName": "category",
          "scale": {"type": "categorical"},
          "displayName": "Category"
        },
        "y": {
          "fieldName": "sum(amount)",
          "scale": {"type": "quantitative"},
          "displayName": "Total Amount"
        },
        "label": {"show": true}
      },
      "frame": {
        "showTitle": true,
        "title": "Sales by Category"
      },
      "mark": {
        "colors": ["#FFAB00", "#00A972", "#FF3621"]
      }
    }
  }
}
```

**Multiple Lines on Bar/Line - Two Approaches:**

1. **Multi-Y Fields** (different metrics on same chart):
```json
"y": {
  "scale": {"type": "quantitative"},
  "fields": [
    {"fieldName": "sum(orders)", "displayName": "Orders"},
    {"fieldName": "sum(returns)", "displayName": "Returns"}
  ]
}
```

2. **Color Grouping** (same metric split by dimension):
```json
"y": {"fieldName": "sum(revenue)", "scale": {"type": "quantitative"}},
"color": {"fieldName": "region", "scale": {"type": "categorical"}, "displayName": "Region"}
```

---

### Line Chart

```json
{
  "widget": {
    "name": "widget-id",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "dataset_id",
        "fields": [
          {"name": "date", "expression": "DATE_TRUNC(\"MONTH\", `sale_date`)"},
          {"name": "series", "expression": "`category`"},
          {"name": "value", "expression": "SUM(`amount`)"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "line",
      "encodings": {
        "x": {
          "fieldName": "date",
          "scale": {"type": "temporal"},
          "displayName": "Date"
        },
        "y": {
          "fieldName": "value",
          "scale": {"type": "quantitative"},
          "displayName": "Amount"
        },
        "color": {
          "fieldName": "series",
          "scale": {"type": "categorical"},
          "displayName": "Category"
        }
      }
    }
  }
}
```

---

### Pie Chart

- `version`: **3**
- Limit to 3-8 categories for readability

```json
{
  "widget": {
    "name": "widget-id",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "dataset_id",
        "fields": [
          {"name": "count(*)", "expression": "COUNT(`*`)"},
          {"name": "category", "expression": "`category`"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "pie",
      "encodings": {
        "angle": {
          "fieldName": "count(*)",
          "scale": {"type": "quantitative"},
          "displayName": "Count"
        },
        "color": {
          "fieldName": "category",
          "scale": {"type": "categorical"},
          "displayName": "Category"
        }
      },
      "frame": {
        "showTitle": true,
        "title": "Distribution by Category"
      }
    }
  }
}
```

---

### Scatter Plot

```json
{
  "widget": {
    "name": "widget-id",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "dataset_id",
        "fields": [
          {"name": "x_val", "expression": "`price`"},
          {"name": "y_val", "expression": "`quantity`"},
          {"name": "group", "expression": "`category`"}
        ],
        "disaggregated": true
      }
    }],
    "spec": {
      "version": 3,
      "widgetType": "scatter",
      "encodings": {
        "x": {
          "fieldName": "x_val",
          "scale": {"type": "quantitative"},
          "displayName": "Price"
        },
        "y": {
          "fieldName": "y_val",
          "scale": {"type": "quantitative"},
          "displayName": "Quantity"
        },
        "color": {
          "fieldName": "group",
          "scale": {"type": "categorical"},
          "displayName": "Category"
        }
      }
    }
  }
}
```

---

### Area Chart

```json
{
  "spec": {
    "version": 3,
    "widgetType": "area",
    "encodings": {
      "x": {"fieldName": "date", "scale": {"type": "temporal"}},
      "y": {"fieldName": "value", "scale": {"type": "quantitative"}},
      "color": {"fieldName": "series", "scale": {"type": "categorical"}}
    }
  }
}
```

---

### Histogram

```json
{
  "spec": {
    "version": 3,
    "widgetType": "histogram",
    "encodings": {
      "x": {
        "fieldName": "bin_field",
        "scale": {"type": "categorical", "sort": {"by": "natural-order"}}
      },
      "y": {
        "fieldName": "count",
        "scale": {"type": "quantitative"}
      },
      "color": {
        "fieldName": "category",
        "scale": {
          "type": "categorical",
          "mappings": [
            {"value": "good", "color": "#00A972"},
            {"value": "bad", "color": "#FF3621"}
          ]
        }
      }
    }
  }
}
```

---

### Table

- `version`: **2** (NOT 1 or 3!)
- **Columns only need `fieldName` and `displayName`** - no other properties needed
- Use `"disaggregated": true` for raw rows

```json
{
  "widget": {
    "name": "details-table",
    "queries": [{
      "name": "main_query",
      "query": {
        "datasetName": "dataset_id",
        "fields": [
          {"name": "col1", "expression": "`column1`"},
          {"name": "col2", "expression": "`column2`"}
        ],
        "disaggregated": true
      }
    }],
    "spec": {
      "version": 2,
      "widgetType": "table",
      "encodings": {
        "columns": [
          {"fieldName": "col1", "displayName": "Column 1"},
          {"fieldName": "col2", "displayName": "Column 2"}
        ]
      },
      "frame": {"showTitle": true, "title": "Details"}
    }
  }
}
```

## Filter Widgets

> **Filter widgets use DIFFERENT widget types than charts!**
> - Valid types: `filter-multi-select`, `filter-single-select`, `filter-date-range-picker`
> - **DO NOT** use `widgetType: "filter"` - this does not exist and will cause errors
> - Filters use `spec.version: 2`
> - **ALWAYS include `frame` with `showTitle: true`** for filter widgets

### Global Filters vs Page-Level Filters

| Type | Placement | Scope | Use Case |
|------|-----------|-------|----------|
| **Global Filter** | Dedicated page with `"pageType": "PAGE_TYPE_GLOBAL_FILTERS"` | Affects ALL pages that have datasets with the filter field | Cross-dashboard filtering (e.g., date range, campaign) |
| **Page-Level Filter** | Regular page with `"pageType": "PAGE_TYPE_CANVAS"` | Affects ONLY widgets on that same page | Page-specific filtering (e.g., platform filter on breakdown page only) |

**Key Insight**: A filter only affects datasets that contain the filter field. To have a filter affect only specific pages:
1. Include the filter dimension in datasets for pages that should be filtered
2. Exclude the filter dimension from datasets for pages that should NOT be filtered

### Filter Widget Structure

> **Do NOT use `associative_filter_predicate_group`** - it causes SQL errors!
> Use a simple field expression instead.

```json
{
  "widget": {
    "name": "filter-region",
    "queries": [{
      "name": "ds_data_region",
      "query": {
        "datasetName": "ds_data",
        "fields": [
          {"name": "region", "expression": "`region`"}
        ],
        "disaggregated": false
      }
    }],
    "spec": {
      "version": 2,
      "widgetType": "filter-multi-select",
      "encodings": {
        "fields": [{
          "fieldName": "region",
          "displayName": "Region",
          "queryName": "ds_data_region"
        }]
      },
      "frame": {"showTitle": true, "title": "Region"}
    }
  },
  "position": {"x": 0, "y": 0, "width": 2, "height": 2}
}
```

### Date Range Picker

```json
{
  "spec": {
    "version": 2,
    "widgetType": "filter-date-range-picker",
    "encodings": {
      "fields": [{
        "fieldName": "date_field",
        "displayName": "Date",
        "queryName": "filter_query_name"
      }]
    },
    "frame": {"showTitle": true, "title": "Select Date Range"}
  }
}
```

### Single Select Dropdown

```json
{
  "spec": {
    "version": 2,
    "widgetType": "filter-single-select",
    "encodings": {
      "fields": [{
        "fieldName": "category",
        "displayName": "Category",
        "queryName": "filter_query_name"
      }]
    },
    "frame": {"showTitle": true, "title": "Select Category"}
  }
}
```

### Text Entry Filter

```json
{
  "spec": {
    "version": 2,
    "widgetType": "filter-text-entry",
    "encodings": {
      "fields": [{
        "fieldName": "search_field",
        "displayName": "Search",
        "queryName": "filter_query_name"
      }]
    }
  }
}
```

### Global Filter Example

Place on a dedicated filter page:

```json
{
  "name": "filters",
  "displayName": "Filters",
  "pageType": "PAGE_TYPE_GLOBAL_FILTERS",
  "layout": [
    {
      "widget": {
        "name": "filter-campaign",
        "queries": [{
          "name": "ds_campaign",
          "query": {
            "datasetName": "overview",
            "fields": [{"name": "campaign_name", "expression": "`campaign_name`"}],
            "disaggregated": false
          }
        }],
        "spec": {
          "version": 2,
          "widgetType": "filter-multi-select",
          "encodings": {
            "fields": [{
              "fieldName": "campaign_name",
              "displayName": "Campaign",
              "queryName": "ds_campaign"
            }]
          },
          "frame": {"showTitle": true, "title": "Campaign"}
        }
      },
      "position": {"x": 0, "y": 0, "width": 2, "height": 2}
    }
  ]
}
```

### Filter Layout Guidelines

- Global filters: Position on dedicated filter page, stack vertically at `x=0`
- Page-level filters: Position in header area of page (e.g., top-right corner)
- Typical sizing: `width: 2, height: 2`

## Scale Types

- `categorical` - For discrete categories
- `quantitative` - For numeric values
- `temporal` - For date/time values

## Sorting Charts (Top K / Most X Visualizations)

**Important:** When a chart is visualizing "top K" or "most X" data (e.g., "Top 10 Users", "Most Active Accounts", "Highest Revenue Categories"), the chart should automatically sort by the y-axis value in **descending order** so the largest values appear first.

To show largest values first (left-to-right), add a `sort` configuration to the x-axis scale with `"by": "y-reversed"`:

```json
{
  "x": {
    "fieldName": "user_name",
    "scale": {
      "type": "categorical",
      "sort": {
        "by": "y-reversed"
      }
    },
    "displayName": "User"
  }
}
```

### Sort Options

- `"by": "y"` - Sort by y-axis value, smallest first (ascending)
- `"by": "y-reversed"` - Sort by y-axis value, largest first (descending)
- `"by": "x"` - Sort by x-axis value alphabetically (A-Z)
- `"by": "x-reversed"` - Sort by x-axis value reverse alphabetically (Z-A)
- `"by": "natural-order"` - Preserve the order from the query

**Best Practice:** Use `"by": "y-reversed"` when the chart title contains words like "Top", "Most", "Highest", "Largest", or similar superlatives indicating a ranking - this places the highest values first (left-to-right).

> **Common Mistake:** Do NOT use `"direction": "descending"` or `"direction": "ascending"` syntax - this does not work in Lakeview. The correct syntax uses the `-reversed` suffix on the sort key (e.g., `"by": "y-reversed"` not `"by": "y", "direction": "descending"`).

## Color Palettes

Default Databricks colors:
```json
["#FFAB00", "#00A972", "#FF3621", "#8BCAE7", "#AB4057", "#99DDB4", "#FCA4A1", "#919191", "#BF7080"]
```

Custom color mappings:
```json
{
  "scale": {
    "type": "categorical",
    "mappings": [
      {"value": "Success", "color": "#00A972"},
      {"value": "Warning", "color": "#FFAB00"},
      {"value": "Error", "color": "#FF3621"}
    ]
  }
}
```

## UI Settings

```json
{
  "uiSettings": {
    "theme": {
      "widgetHeaderAlignment": "ALIGNMENT_UNSPECIFIED"
    },
    "applyModeEnabled": false
  }
}
```

## Complete Example

See `resources/example_dashboard.json` for a complete working example.

## Python Helper

Use `resources/lakeview_builder.py` for a Python class that simplifies dashboard creation:

```python
from lakeview_builder import LakeviewDashboard

dashboard = LakeviewDashboard("My Sales Dashboard")

# Add dataset
dashboard.add_dataset(
    "sales",
    "Sales Data",
    "SELECT * FROM catalog.schema.sales"
)

# Add bar chart
dashboard.add_bar_chart(
    dataset_name="sales",
    x_field="category",
    y_field="amount",
    y_agg="SUM",
    title="Sales by Category",
    position={"x": 0, "y": 0, "width": 3, "height": 4}
)

# Add counter
dashboard.add_counter(
    dataset_name="sales",
    value_field="amount",
    value_agg="SUM",
    title="Total Sales",
    position={"x": 3, "y": 0, "width": 1, "height": 2}
)

# Get JSON for API
json_payload = dashboard.to_json()
```

## Quality Checklist

Before deploying, verify:
1. All widget names use only alphanumeric + hyphens + underscores
2. All rows sum to width=6 with no gaps
3. KPIs use height 3-4, charts use height 5-6
4. Chart dimensions have 8 or fewer distinct values
5. All widget fieldNames match dataset columns exactly
6. **Field `name` in query.fields matches `fieldName` in encodings exactly** (e.g., both `"sum(spend)"`)
7. Counter datasets: use `disaggregated: true` for 1-row datasets, `disaggregated: false` with aggregation for multi-row
8. Percent values are 0-1 (not 0-100)
9. SQL uses Spark syntax (date_sub, not INTERVAL)
10. **All SQL queries tested and return expected data**

## Tips

1. **Widget IDs**: Generate unique 8-character hex IDs for widget and dataset names
2. **Grid Layout**: Dashboard uses a 6-column grid. Plan layout before building.
3. **Dataset Reuse**: Multiple widgets can share the same dataset
4. **Disaggregated**: Set to `true` for raw data (tables), `false` for aggregations

## Troubleshooting

### Widget shows "no selected fields to visualize"

**This is a field name mismatch error.** The `name` in `query.fields` must exactly match the `fieldName` in `encodings`.

**Fix:** Ensure names match exactly:
```json
// WRONG - names don't match
"fields": [{"name": "spend", "expression": "SUM(`spend`)"}]
"encodings": {"value": {"fieldName": "sum(spend)", ...}}  // ERROR!

// CORRECT - names match
"fields": [{"name": "sum(spend)", "expression": "SUM(`spend`)"}]
"encodings": {"value": {"fieldName": "sum(spend)", ...}}  // OK!
```

### Widget shows "Invalid widget definition"

**Check version numbers:**
- Counters: `version: 2`
- Tables: `version: 2`
- Filters: `version: 2`
- Bar/Line/Pie/Area/Scatter charts: `version: 3`

**Text widget errors:**
- Text widgets must NOT have a `spec` block
- Use `multilineTextboxSpec` directly on the widget object
- Do NOT use `widgetType: "text"` - this is invalid

**Table widget errors:**
- Use `version: 2` (NOT 1 or 3)
- Column objects only need `fieldName` and `displayName`
- Do NOT add `type`, `displayAs`, `numberFormat`, or other column properties

**Counter widget errors:**
- Use `version: 2` (NOT 3)

### Dashboard shows empty widgets

- Run the dataset SQL query directly to check data exists
- Verify column aliases match widget field expressions
- Check `disaggregated` flag (should be `true` for pre-aggregated data)

### Layout has gaps

- Ensure each row sums to width=6
- Check that y positions don't skip values unnecessarily

### Filter shows "Invalid widget definition"

- Check `widgetType` is one of: `filter-multi-select`, `filter-single-select`, `filter-date-range-picker`
- **DO NOT** use `widgetType: "filter"` - this is invalid
- Verify `spec.version` is `2`
- Ensure `queryName` in encodings matches the query `name`
- Confirm `disaggregated: false` in filter queries
- Ensure `frame` with `showTitle: true` is included

### Filter not affecting expected pages

- **Global filters** (on `PAGE_TYPE_GLOBAL_FILTERS` page) affect all datasets containing the filter field
- **Page-level filters** (on `PAGE_TYPE_CANVAS` page) only affect widgets on that same page
- A filter only works on datasets that include the filter dimension column

### Filter shows "UNRESOLVED_COLUMN" error

- **DO NOT** use `associative_filter_predicate_group` in filter queries
- This internal expression causes SQL errors when the dashboard executes queries
- Use a simple field expression instead: `{"name": "field", "expression": "\`field\`"}`

### Text widget shows title and description on same line

- Multiple items in the `lines` array are **concatenated**, not displayed on separate lines
- Use **separate text widgets** for title and subtitle at different y positions
- Example: title at y=0 with height=1, subtitle at y=1 with height=1

### Dashboard not rendering

- Check serialized_dashboard is valid JSON string (escaped)

### Filters not working

- Ensure filter query names follow the pattern
- Verify the filter field exists in the dataset(s) you want filtered
