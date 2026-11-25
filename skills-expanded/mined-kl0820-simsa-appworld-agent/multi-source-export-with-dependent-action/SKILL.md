---
name: multi-source-export-with-dependent-action
description: Consolidates data from multiple distinct sources, processes it (including deduplication and formatting), exports it to a single target, and then performs a final, critical action strictly contingent on the export's success.
---
## Overview
This pattern addresses tasks that involve gathering disparate data from multiple distinct sources (potentially across different systems or services), unifying and processing it, and then outputting it to a single destination. A critical component is the execution of a subsequent, often irreversible, action that is strictly contingent on the successful completion of the data export, ensuring data integrity and safety. It emphasizes clear separation of data collection, processing, and output, followed by conditional execution of a final step.

## When to Apply
- Consolidate data from multiple distinct origins, potentially across different systems or services.
- Export processed data to a single file or destination.
- Perform a final, critical action *only after* a preceding data operation (export/processing) is successfully completed.
- Specific output formatting (e.g., custom headers, delimiters, attribute formatting, handling multi-valued attributes) is required.
- Deduplication or uniqueness across the *entire* combined dataset is specified.

## Procedure
1. Identify all distinct data sources from which information needs to be collected.
2. Independently read and extract the necessary attributes from each specified source. (These reads can often be performed in parallel).
3. Aggregate all collected records into a single collection.
4. Deduplicate the aggregated collection based on a defined uniqueness criterion, preserving all required attributes. The agent must determine the appropriate keys for uniqueness from the task instruction.
5. Transform the deduplicated records into the specified output format, applying any required attribute formatting (e.g., joining multi-valued attributes with a delimiter) or header mapping.
6. Write the processed and formatted data to the designated target location in the specified format.
7. Conditionally execute the final, critical, and often destructive, dependent action *only after* successful completion of the data write/export.

## Key Patterns
- **Multi-Source Aggregation and Parallel Reads:** Collect data from several distinct origins (e.g., different libraries, lists, categories, or systems). Multiple independent read operations can be initiated, but subsequent processing (combination, deduplication) must await the completion of all reads.
- **Deduplication Across Sources:** After aggregating data from multiple sources, identify and remove duplicate records based on a defined set of key attributes to ensure a unique final dataset across the *entire* combined dataset. The deduction agent must determine the appropriate keys for uniqueness from the task instruction.
- **Structured Data Transformation and Export:** Convert processed data into a specific structured output format (e.g., CSV, JSON, XML), including defining headers, field order, and applying specific formatting rules to individual attributes (e.g., joining multi-valued attributes with a delimiter). Precise adherence to specified header names and internal data delimiters or separators is often required.
- **Dependent Final Action:** A critical, often destructive, action is strictly contingent upon the successful completion of a preceding step (e.g., data export or write operation). This action must only be attempted if the prior step has been confirmed as successful, ensuring data integrity or safety.

## Common Pitfalls
- Failing to identify all distinct data sources for collection or failing to read all specified sources before attempting consolidation.
- Incorrectly defining the uniqueness criteria for deduplication, leading to either missing unique records or retaining duplicates, especially overlooking uniqueness across *all* combined sources (instead only deduplicating within each source).
- Not handling multi-valued attributes (e.g., lists of items) correctly during transformation, leading to data loss or incorrect formatting.
- Executing the dependent final action prematurely or unconditionally, or attempting it before confirming the successful completion of the preceding critical step, risking data loss or unintended consequences.
- Mismatched output headers, incorrect internal data delimiters (e.g., field separators), or overlooking specific formatting requirements for headers or attribute values in the output, leading to malformed output.
- Not considering system boundaries when planning data transfer or actions.