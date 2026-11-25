---
name: work-log-processing
description: Industrial protocol for transforming rough work log files (*_rough.txt) into formatted work log files (*.txt) with standardized date format, day of week, and caller notation.
category: Data-Processing
---

# Work Log Processing Skill

This skill transforms rough work log entries into professionally formatted work log files following the standardized work log format.

***

## 1. Preparation: Context Assembly

The agent MUST:

1. **Source Discovery**: Identify the rough work log file from the user's input (e.g., `*_rough.txt`)
2. **Reference Format**: Read an existing properly formatted work log file for format reference (e.g., `jan2026.txt`)
3. **Output Path**: Determine the output file path by removing `_rough` suffix (e.g., `feb2026_rough.txt` → `feb2026.txt`)
4. **Month Identification**: Identify the month being processed from the filename

### 1.1 Reference Format Analysis

The properly formatted work log file uses this structure:

```
DD/MM/YYYY DayName HH:MM:SS HH:MM:SS "Activity Description"
```

Key characteristics:

- Date format: `DD/MM/YYYY DayName` (e.g., `02/01/2026 Friday`)
- Time range: `StartTime EndTime` (e.g., `15:08:00 15:09:30`)
- Activity in double quotes: `"Activity Description"`
- Caller format: `(Name)` for voice/calls
- No header/comment lines

***

## 2. Operational Transformation Logic

The agent MUST apply these transformations:

### 2.1 Removal Transformations

1. **Header Lines**: Remove lines starting with `#`
2. **Separator Lines**: Remove lines with `---` or `====`
3. **Blank Lines**: Remove consecutive blank lines

### 2.2 Date Format Transformations

1. **Add Day of Week**: If day of week is missing, add it based on the date
2. **Standardize Date Format**: Convert `Mar 1 2026` → `01/03/2026 Monday`
3. **Standardize Date Format**: Convert `march 4 2026` → `04/03/2026 Wednesday`
4. **Standardize Date Format**: Convert `15 April 2026` → `15/04/2026 Wednesday`

### 2.3 Content Transformations

1. **Braces to Quotes**: Convert `{...}` to `"..."`
2. **Caller Format**: Convert `Voice Call to <colleague>` → `Voice Call (<colleague>)`
3. **Caller Format**: Convert `Phone Call by <colleague>` → `Phone Call (<colleague>)`
4. **Caller Format**: Convert `Team Call to <colleague>` → `Team Call (<colleague>)`
5. **Caller Format**: Convert `Team Meet by <colleague>` → `Team Meet (<colleague>)`
6. **Caller Format**: Convert `Call with <colleague>` → `Call (<colleague>)`
7. **Remove By/To Prefixes**: Remove `by` and `to` prefixes in descriptions
8. **Fix Incomplete Times**: Convert `XX:XX:XX` to valid time range (e.g., `22:01:00 23:59:59`)

### 2.4 Rough Note Processing

For rough notes that span multiple lines or contain numbered items:

1. Break into individual time entries
2. Estimate time ranges where information is implicit
3. Consolidate multi-item descriptions into separate entries
4. Process date-based sections into chronological entries

***

## 3. Output Generation

### 3.1 File Creation

1. Create the output file at the same directory with `_rough` removed from filename
2. Write all transformed entries in chronological order
3. Maintain the format: `DD/MM/YYYY DayName StartTime EndTime "Description"`

### 3.2 Entry Ordering

- Sort all entries by date first, then by start time
- Ensure no entries are lost during transformation

***

## 4. Verification

The agent MUST verify:

1. All date entries have day of week
2. All entries are in `"..."` format
3. No header lines remain
4. All time ranges are valid (start < end)
5. Output file is created successfully

***

## 5. Environment & Dependencies

No external tools required. This skill uses:

- File system access (Read/Write tools)
- Date calculation for day of week determination

***

## 6. Related Skills

| Skill | Relationship |
|-------|-------------|
| [`time-entry-markdown-presentation`](../time-entry-markdown-presentation/SKILL.md) | Downstream presentation layer — pipes the formatted TXT entries through this skill for markdown table rendering with duration calculation and summary rows. |

***

## 7. Related Conversations & Traceability

This skill was created from a work log processing workflow demonstrated in an earlier session. Refer to the source conversation for operational context and examples.
