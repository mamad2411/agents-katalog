---
name: analyze-csv
description: Loads a CSV, profiles every column and its quality problems, and summarizes the data with a few plots saved to disk.
disable-model-invocation: true
---

Analyze the CSV at: $ARGUMENTS

1. Confirm the file exists and print its size and first 5 lines raw, so delimiter, encoding and header problems show up. Never modify the source file.
2. Load it with pandas (`pd.read_csv`, pass `sep`, `encoding` and `dtype` as needed). Report rows, columns, memory use.
3. Profile each column: inferred type, null count and percent, distinct count, min, max, mean and top values. Flag mixed types, dates stored as text, numbers with currency symbols, and IDs that are not unique.
4. Check quality: exact duplicate rows, impossible values (negative ages, future birthdates), outliers beyond 3 standard deviations, inconsistent casing or trailing spaces.
5. Write 3 to 5 plots with matplotlib into `./csv-analysis/`: missingness bar, the main numeric distributions, one category count, and one relationship worth seeing.

Finish with a short summary: what each row represents, the three biggest problems, and suggested cleaning steps. Do not clean anything until asked.
