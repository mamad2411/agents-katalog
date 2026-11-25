---
name: chart-plotter
description: Draws a bar chart from a column of numbers and saves it as a PNG beside the data. Use when a table of figures needs a picture, when the user asks for a chart of a column, or when a report is missing its illustration.
---

# Chart plotter

1. Read the column the user named and drop any row that is not a number.
2. Choose the axis range from the data rather than from zero, unless the user says
   otherwise.
3. Hand the numbers to [`scripts/plot.py`](scripts/plot.py), which saves the PNG
   beside the data file.
4. Print the path of the PNG.
