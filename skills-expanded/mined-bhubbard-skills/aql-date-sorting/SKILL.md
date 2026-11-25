---
name: aql-date-sorting
description: Guidance on dynamic date queries and advanced sorting options. Use when building calendars, event lists, or sorting by engagement metrics.
---

# Advanced Query Loop: Dates & Sorting

## Dynamic Date Queries
Perfect for event lists or "recently updated" sections, you can filter the query loop based on time constraints:
- **Relative Dates**: Show content published only in the last 1, 3, 6, or 12 months.
- **Before/After**: Show posts published before or after a specific calendar date, or relative to the "current date".
- **Custom Ranges**: Define precise start and end boundaries.

## Flexible Sorting Options
The core block only sorts by Date or Title. AQL unlocks powerful sorting alternatives:
- **Meta Values**: Sort alphabetically or numerically by custom field data (e.g., price, event date).
- **Engagement**: Sort by `Comment Count`.
- **Administrative**: Sort by `Last Modified` date, `Author`, `Menu Order`, or `Post ID`.
- **Random**: Shuffle the content (Note: doing so disables the block's caching feature).
