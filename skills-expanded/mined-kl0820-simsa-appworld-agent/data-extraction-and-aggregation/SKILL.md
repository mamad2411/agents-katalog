---
name: data-extraction-and-aggregation
description: When the task requires extracting specific data points from multiple sources and then performing an aggregation or computation on that extracted data.
---
## Overview
This skill addresses tasks that involve iterating through a collection of items (e.g., files, records), extracting specific information from each item's content based on certain criteria, structuring this information, and finally performing a summary operation (like summing or counting) on the collected data. It emphasizes creating a robust intermediate data structure to facilitate subsequent processing.
## When to Apply
- Read the contents of a directory or collection of records.
- Identify items based on content or metadata patterns.
- Extract specific values from multiple sources.
- Calculate a total, sum, or count based on extracted data.
- Process a collection of documents or records to derive a summary.
## Procedure
1. List all potential source items from a given location (e.g., files in a directory, records from a database).
2. Filter these items based on initial, easily verifiable criteria (e.g., filename patterns, metadata).
3. For each filtered item, retrieve its full content.
4. Parse the content to extract relevant data points and apply detailed filtering criteria based on the extracted data.
5. Construct an intermediate structured data representation (e.g., a list of dictionaries) where each entry contains the extracted, processed, and normalized data, along with any necessary identifiers, to be consumed by subsequent steps.
6. Retrieve the structured data from the previous step.
7. Iterate through the structured data and perform the required aggregation or computation on the relevant fields.
8. Format and output the final computed result.
## Key Patterns
- **Intermediate Structured Data:** Creating a well-defined, structured data representation (e.g., a list of dictionaries) from raw content is crucial. This structure should encapsulate extracted, processed, and normalized data, preserving context and enabling flexible filtering, aggregation, and robustness for future operations, rather than passing raw content or minimal values.
- **Content-Based Filtering:** Filtering items often requires not just checking metadata or initial identifiers, but also retrieving and parsing the actual content of each item to apply more detailed, business-logic-driven criteria.
- **Aggregation from Structured Data:** Final computations or aggregations should be performed on the pre-processed, structured data generated in an earlier step, rather than re-accessing or re-parsing raw content.
## Common Pitfalls
- Not creating a structured intermediate representation, leading to re-parsing of raw content or loss of context in subsequent steps.
- Overlooking edge cases in content parsing, such as missing values, inconsistent formats, or unexpected data types.
- Not handling empty results or collections gracefully, which can lead to errors or incorrect outputs.
- Attempting to re-fetch or re-parse data in later steps when it was already processed and structured in an earlier step, leading to inefficiency.
