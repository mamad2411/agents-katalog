---
name: file-system-data-aggregation
description: Aggregates numerical data extracted from multiple files within a file system directory, potentially recursively, filtered by content and metadata.
---
## Overview
This skill processes multiple files within a specified directory, potentially recursively. It involves navigating the file system, identifying relevant files based on path, name, and content, extracting specific numerical information from those files using robust and progressive parsing techniques, and then performing an aggregation (like summing or averaging) on the extracted data. The process emphasizes multi-stage filtering, robust error handling, and careful data cleaning to ensure accurate results.

## When to Apply
- When asked to process files in a directory, including subdirectories.
- When filtering files based on keywords in content or path/filename patterns.
- When filtering files based on date/time metadata or content.
- When extracting specific numeric values from file content.
- When calculating a sum, average, or other aggregate from extracted numeric data spread across multiple files.
- When processing a collection of documents to derive a single aggregate metric.

## Procedure
1. List entries in a specified directory, potentially recursively, to gather all potential files.
2. Apply initial filtering to the list of entries based on path or filename patterns.
3. For each filtered entry, retrieve its content and relevant metadata (e.g., creation date, path).
4. Apply content-based filtering criteria (e.g., keyword presence, specific text patterns, temporal or categorical criteria) to determine if the item is relevant. This may involve multiple sequential conditions.
5. If an item is relevant, extract the required numeric data from its content using robust and progressive parsing techniques, such as regular expressions (e.g., specific patterns, then more general ones, then fallback to metadata).
6. Clean the extracted numeric data by removing non-numeric characters (e.g., currency symbols, commas) and convert it to the appropriate numerical type.
7. Initialize an accumulator variable (e.g., a sum) to zero.
8. Add the cleaned numeric data to the accumulator.
9. After processing all items, return the final aggregated value, ensuring a default (e.g., zero) if no relevant data is found, formatted as a structured output including the value, a summary, and a description.

## Key Patterns
- **Robust API Call Handling:** When calling an API that returns a collection of items, always check if the result is an error dictionary before attempting to iterate. Similarly, when processing items in a loop, check for individual item API call failures and skip to the next item. Implement checks for API call success, expected return types (e.g., `isinstance(result, dict)`), and the presence of critical keys (e.g., `'content' in result`) to gracefully handle partial or erroneous responses.
- **Iterative File Processing & Content Access:** Process files one by one, first filtering by path/metadata, then by content, to isolate relevant data. Accessing a collection of items (e.g., file paths) and then, for each item, making a subsequent API call to retrieve its detailed content (e.g., file content).
- **Multi-stage/Multi-Criteria Filtering:** Apply filtering criteria sequentially: first on file metadata (path/name), then on file content, to narrow down the set of relevant items. This involves applying a sequence of independent conditional checks (e.g., keyword presence, date range, specific identifier) to an item's content, where all conditions must be met for the item to be considered valid for further processing.
- **Progressive Data Extraction & Regex-based Cleaning:** When extracting specific data (e.g., dates, amounts) from unstructured text, employ multiple parsing strategies (e.g., specific regex patterns, then more general ones, then fallback to metadata) to maximize extraction success across varied formats. Use regular expressions for precise content parsing, followed by necessary cleaning (e.g., removing commas, currency symbols) and type conversion (e.g., string to float).
- **Content and Metadata Filtering:** Combine checks on both item content (e.g., keywords, specific text patterns) and item metadata (e.g., path, creation/modification dates) to accurately identify and filter relevant items.
- **Text Normalization for Matching:** Convert text to a consistent case (e.g., lowercase) before performing keyword searches or comparisons to ensure case-insensitive matching.
- **Numeric Data Cleaning:** Before converting extracted numeric strings to floats or integers, remove non-numeric characters like currency symbols, commas, or other delimiters that might interfere with conversion.
- **Accumulation and Aggregation:** Maintaining a running total or collection by iteratively adding or appending extracted values from qualifying items, culminating in a single aggregated result. The final aggregation step directly consumes the structured output of the preceding extraction and cleaning step, avoiding redundant API calls.

## Common Pitfalls
- Failing to handle API errors or empty results gracefully, leading to crashes or incorrect processing.
- Not handling empty directory listings or cases where API calls fail or return unexpected types.
- Using a single, rigid parsing pattern for dates or amounts, which fails on variations in text format.
- Not normalizing text (e.g., case-insensitivity) before keyword matching, leading to missed relevant items.
- Ignoring potential non-numeric characters in extracted amounts before type conversion, leading to parsing errors.
- Not providing a default or zero value when no matching items are found, leading to an undefined result.
- Overlooking recursive directory traversal when needed, resulting in incomplete data processing.
- Not properly converting extracted strings to numerical types before aggregation.
- Incorrectly parsing dates or numerical amounts from text, especially when multiple formats, currency symbols, or thousands separators are present.
- Not accounting for cases where the required data (e.g., amount, date) is entirely missing from an item's content.
- Applying filtering conditions in an inefficient order or with incorrect logical operators (e.g., using OR instead of AND for sequential criteria).
- Forgetting to initialize the accumulator variable or incorrectly updating it within the loop.