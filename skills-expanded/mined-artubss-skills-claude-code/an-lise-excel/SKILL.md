---
name: Análise Excel
description: Analise planilhas Excel, crie tabelas dinâmicas, gere gráficos e realize análise de dados. Use ao analisar arquivos Excel, planilhas, dados tabulares ou arquivos .xlsx.
---

# Análise Excel

## Início rápido

Leia arquivos Excel com pandas:

```python
import pandas as pd

# Read Excel file
df = pd.read_excel("data.xlsx", sheet_name="Sheet1")

# Display first few rows
print(df.head())

# Basic statistics
print(df.describe())
```

## Lendo múltiplas abas

Processe todas as abas em uma pasta de trabalho:

```python
import pandas as pd

# Read all sheets
excel_file = pd.ExcelFile("workbook.xlsx")

for sheet_name in excel_file.sheet_names:
    df = pd.read_excel(excel_file, sheet_name=sheet_name)
    print(f"\n{sheet_name}:")
    print(df.head())
```

## Análise de dados

Realize tarefas comuns de análise:

```python
import pandas as pd

df = pd.read_excel("sales.xlsx")

# Group by and aggregate
sales_by_region = df.groupby("region")["sales"].sum()
print(sales_by_region)

# Filter data
high_sales = df[df["sales"] > 10000]

# Calculate metrics
df["profit_margin"] = (df["revenue"] - df["cost"]) / df["revenue"]

# Sort by column
df_sorted = df.sort_values("sales", ascending=False)
```

## Criando arquivos Excel

Escreva dados em Excel com formatação:

```python
import pandas as pd

df = pd.DataFrame({
    "Product": ["A", "B", "C"],
    "Sales": [100, 200, 150],
    "Profit": [20, 40, 30]
})

# Write to Excel
writer = pd.ExcelWriter("output.xlsx", engine="openpyxl")
df.to_excel(writer, sheet_name="Sales", index=False)

# Get worksheet for formatting
worksheet = writer.sheets["Sales"]

# Auto-adjust column widths
for column in worksheet.columns:
    max_length = 0
    column_letter = column[0].column_letter
    for cell in column:
        if len(str(cell.value)) > max_length:
            max_length = len(str(cell.value))
    worksheet.column_dimensions[column_letter].width = max_length + 2

writer.close()
```

## Tabelas dinâmicas

Crie tabelas dinâmicas programaticamente:

```python
import pandas as pd

df = pd.read_excel("sales_data.xlsx")

# Create pivot table
pivot = pd.pivot_table(
    df,
    values="sales",
    index="region",
    columns="product",
    aggfunc="sum",
    fill_value=0
)

print(pivot)

# Save pivot table
pivot.to_excel("pivot_report.xlsx")
```

## Gráficos e visualização

Gere gráficos a partir de dados Excel:

```python
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_excel("data.xlsx")

# Create bar chart
df.plot(x="category", y="value", kind="bar")
plt.title("Sales by Category")
plt.xlabel("Category")
plt.ylabel("Sales")
plt.tight_layout()
plt.savefig("chart.png")

# Create pie chart
df.set_index("category")["value"].plot(kind="pie", autopct="%1.1f%%")
plt.title("Market Share")
plt.ylabel("")
plt.savefig("pie_chart.png")
```

## Limpeza de dados

Limpe e prepare dados Excel:

```python
import pandas as pd

df = pd.read_excel("messy_data.xlsx")

# Remove duplicates
df = df.drop_duplicates()

# Handle missing values
df = df.fillna(0)  # or df.dropna()

# Remove whitespace
df["name"] = df["name"].str.strip()

# Convert data types
df["date"] = pd.to_datetime(df["date"])
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Save cleaned data
df.to_excel("cleaned_data.xlsx", index=False)
```

## Mesclar e unir

Combine múltiplos arquivos Excel:

```python
import pandas as pd

# Read multiple files
df1 = pd.read_excel("sales_q1.xlsx")
df2 = pd.read_excel("sales_q2.xlsx")

# Concatenate vertically
combined = pd.concat([df1, df2], ignore_index=True)

# Merge on common column
customers = pd.read_excel("customers.xlsx")
sales = pd.read_excel("sales.xlsx")

merged = pd.merge(sales, customers, on="customer_id", how="left")

merged.to_excel("merged_data.xlsx", index=False)
```

## Formatação avançada

Aplique formatação condicional e estilos:

```python
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill, Font

# Create Excel file
df = pd.DataFrame({
    "Product": ["A", "B", "C"],
    "Sales": [100, 200, 150]
})

df.to_excel("formatted.xlsx", index=False)

# Load workbook for formatting
wb = load_workbook("formatted.xlsx")
ws = wb.active

# Apply conditional formatting
red_fill = PatternFill(start_color="FF0000", end_color="FF0000", fill_type="solid")
green_fill = PatternFill(start_color="00FF00", end_color="00FF00", fill_type="solid")

for row in range(2, len(df) + 2):
    cell = ws[f"B{row}"]
    if cell.value < 150:
        cell.fill = red_fill
    else:
        cell.fill = green_fill

# Bold headers
for cell in ws[1]:
    cell.font = Font(bold=True)

wb.save("formatted.xlsx")
```

## Dicas de desempenho

- Use `read_excel` com `usecols` para ler apenas colunas específicas
- Use `chunksize` para arquivos muito grandes
- Considere usar `engine='openpyxl'` ou `engine='xlrd'` conforme o tipo de arquivo
- Use o parâmetro `dtype` para especificar tipos de coluna para leitura mais rápida

## Pacotes disponíveis

- **pandas** - Análise e manipulação de dados (principal)
- **openpyxl** - Criação e formatação de arquivos Excel
- **xlrd** - Leitura de arquivos .xls antigos
- **xlsxwriter** - Capacidades avançadas de escrita em Excel
- **matplotlib** - Geração de gráficos