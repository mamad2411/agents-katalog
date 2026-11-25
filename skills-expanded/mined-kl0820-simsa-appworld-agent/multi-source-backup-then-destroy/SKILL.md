---
name: multi-source-backup-then-destroy
description: When a task requires aggregating data from multiple sources within an application, backing it up to an external system, and then performing a destructive action in the source application.
---
## Overview
This pattern addresses tasks that involve collecting comprehensive data from various internal locations of a primary application, ensuring its safe transfer to a secondary storage, and then executing a final, irreversible operation on the primary application. It prioritizes data integrity and safety before destructive actions.
## When to Apply
- Instruction mentions backing up data from multiple locations within a single service.
- Instruction specifies writing data to an external file or storage.
- Instruction includes a destructive action on the source service that must occur after the backup.
## Procedure
1. Identify all distinct data sources within the primary application that need to be aggregated.
2. Read and combine data from all identified sources, applying any specified de-duplication or formatting.
3. Write the aggregated and processed data to the specified external target, ensuring all formatting and structural requirements (e.g., headers, separators) are met.
4. Confirm the successful completion of the external write operation.
5. Execute the destructive action on the primary application, contingent on the successful data transfer.
## Key Patterns
- **Multi-Source Aggregation:** When data needs to be collected from several logical containers or endpoints within a single application, read all sources first and then combine/de-duplicate them into a unified dataset.
- **Dependent Destructive Action:** If a destructive action is specified, it must be placed after and made strictly dependent on the successful completion of any preceding backup or data transfer steps.
- **Cross-Application Data Transfer:** Separate the read operation from the source application from the write operation to the target application, ensuring all data processing and formatting occurs before the write.
## Common Pitfalls
- Performing the destructive action before confirming the backup is complete.
- Failing to aggregate data from all specified internal sources.
- Not handling de-duplication or specific formatting requirements during aggregation.
- Incorrectly specifying the output path, headers, or data separators for the external write.
