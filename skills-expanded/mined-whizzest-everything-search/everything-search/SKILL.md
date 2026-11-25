---
name: "everything-search"
description: "Provides comprehensive guidance for using ES (Everything Search) command-line tool. Invoke when user asks about file searching, needs help with es commands, or wants to search files efficiently using Everything."
---

# Everything Search Command Helper

This skill provides comprehensive guidance for using the ES (Everything Search) command-line interface tool.

## IMPORTANT: Always Use -help First

**CRITICAL**: Before attempting any ES command, always run `es -help` to get the most up-to-date information. The ES tool is actively maintained and options may change. Using `-help` ensures you have the latest syntax and available options.

```bash
es -help
```

## What is ES?

ES is a command-line interface to Everything, a powerful file search utility for Windows. It provides fast, efficient file searching with advanced filtering and sorting capabilities.

## Installation

### Check if Everything and ES are Installed

```bash
# Check Everything version
es -get-everything-version

# Check ES version
es -version

# Check if es command is available
es -help
```

If these commands fail, you need to install Everything and ES.

### Install Everything and ES using winget

winget is available on Windows 10/11 by default.

#### Search for Everything and ES:
```bash
winget search Everything
```

Expected results:
- `voidtools.Everything` - Everything (main application)
- `voidtools.Everything.Cli` - ES (Everything CLI)

#### Install Everything:
```bash
winget install voidtools.Everything
```

#### Install ES (Everything CLI):
```bash
winget install voidtools.Everything.Cli
```

#### Verify installation:
```bash
es -version
es -get-everything-version
```

### Post-Installation Setup

After installation:

1. **Start Everything**: Launch Everything from Start menu
2. **Configure Everything**: Let Everything index your files (usually quick)
3. **Verify ES connection**:
   ```bash
   es -help
   ```

### Troubleshooting Installation

#### ES command not found:
- Restart your terminal
- Verify ES is in your PATH: `where es`
- Reinstall: `winget install voidtools.Everything.Cli --force`

#### Everything not running:
- Start Everything from Start menu
- Check if Everything is running in Task Manager

#### ES cannot connect to Everything:
- Ensure Everything is running
- Restart Everything

## Basic Usage

### Simple Search
```bash
es <search-term>
```

### Limit Results
```bash
es -n 10 *.js
es -count 5 package.json
```

### Search by Extension
```bash
es ext:exe;ini
es *.txt
es *.js
```

## Search Options

### Pattern Matching
- `-r <pattern>` or `-regex <pattern>`: Use regular expressions
- `-i` or `-case`: Match case (case-sensitive)
- `-w` or `-whole-word`: Match whole words only
- `-p` or `-match-path`: Match full path
- `-prefix`: Match start of words
- `-suffix`: Match end of words

### Path Filtering
- `-path <path>`: Search in specific path
- `-parent-path <path>`: Search in parent of path
- `-parent <path>`: Search files with specific parent path

### File Type Filtering
- `/ad`: Folders only
- `/a-d`: Files only
- `/a[RHSDAVNTPLCOIEUPM]`: DIR style attributes search (see `es -help` for details)

## Sorting Options

### Sort by Property
```bash
es -sort name <search-term>
es -sort size <search-term>
es -sort date-modified <search-term>
es -sort extension <search-term>
```

### Sort Order
```bash
es -sort name-ascending <search-term>
es -sort size-descending <search-term>
```

## Display Options

### Show Specific Columns
```bash
es -name -size -extension *.js
es -path-column -date-modified -size *.log
es -full-path-and-name *.txt
```

### Available Columns
- `-name`: File name
- `-path-column`: Path
- `-full-path-and-name`: Full path and name
- `-extension` or `-ext`: File extension
- `-size`: File size
- `-date-created` or `-dc`: Creation date
- `-date-modified` or `-dm`: Modification date
- `-date-accessed` or `-da`: Last access date
- Use `es -help` for all available columns

### Output Formats
```bash
es -csv *.js
es -json *.txt
es -tsv *.log
es -txt *.ini
```

### Date Format (IMPORTANT for JSON/CSV exports)

**CRITICAL**: When using `-json`, `-csv`, or other export formats, dates are displayed as FILETIME integers by default, which are not human-readable. Use `-date-format` to convert to readable format.

```bash
# Default (FILETIME - not readable)
es -n 2 -json *.ts
# Output: "date_modified":133564093868587796

# ISO-8601 (local time) - RECOMMENDED
es -n 2 -json -date-format 1 *.ts
# Output: "date_modified":"2024-04-01T09:43:06"

# ISO-8601 (UTC) - for timezone-aware applications
es -n 2 -json -date-format 3 *.ts
# Output: "date_modified":"2024-04-01T01:43:06Z"

# ISO-8601 with full resolution (milliseconds)
es -n 2 -json -date-format 5 *.ts
# Output: "date_modified":"2024-04-01T09:43:06.8587796"
```

**Available date formats:**
- `0` - auto (automatic selection)
- `1` - ISO-8601 (local time) - **RECOMMENDED**
- `2` - FILETIME (default, not readable)
- `3` - ISO-8601 (UTC) - for timezone-aware applications
- `4` - User Locale (system-specific format)
- `5` - ISO-8601 with full resolution (milliseconds)
- `6` - ISO-8601 (UTC) with full resolution

**Best practice**: Always use `-date-format 1` or `-date-format 3` when exporting to JSON or CSV for human-readable dates.

## Export Options

### Export to File
```bash
es -export-csv results.csv *.js
es -export-json results.json *.txt
es -export-txt results.txt *.log
es -export-tsv results.tsv *.ini
```
Use `es -help` for additional export options.

## Statistics and Information

### Get Result Count
```bash
es -get-result-count *.js
```

### Get Total Size
```bash
es -get-total-size *.log
```

### Get Folder Size
```bash
es -get-folder-size "C:\path\to\folder"
```

### Version Information
```bash
es -version
es -get-everything-version
```

## Advanced Examples

### Search and Sort
```bash
es -n 20 -sort size -size -name *.log
```

### Search in Specific Path with Custom Columns
```bash
es -n 10 -path "C:\Users" -name -size -date-modified *.pdf
```

### Case-Sensitive Whole Word Search
```bash
es -i -w "MyFile"
```

### Regex Search
```bash
es -r "test_\d+\.txt"
```

### Export Large Results
```bash
es -export-json all_files.json *
```

### Search for Folders Only
```bash
es /ad -n 20
```

### Search for Hidden Files
```bash
es /aH -n 10
```

## Everything Control

### Database Operations
```bash
es -save-db
es -reindex
```

### Exit Everything
```bash
es -exit
```

## Best Practices

1. **Always check `-help` first** - ES options may change
2. **Use `-n` to limit results** - Prevent overwhelming output
3. **Specify columns explicitly** - Get only the information you need
4. **Use appropriate output format** - CSV/JSON for programmatic use, default for human reading
5. **Combine filters** - Use path, extension, and attributes together for precise searches
6. **Export for large result sets** - Use `-export-*` options instead of printing to console

## Common Use Cases

### Find recently modified files
```bash
es -n 50 -sort date-modified-descending *
```

### Export file list for backup
```bash
es -export-csv backup_list.csv -path "C:\important\files" *
```

## Troubleshooting

### No Results Found
- Check if Everything is running
- Verify the search pattern is correct
- Try a broader search term
- Use `-get-result-count` to verify search is working

### Command Not Found
- Ensure ES is installed and in PATH
- Check Everything is installed on your system

### Slow Performance
- Use `-n` to limit results
- Add path filters to narrow search scope
- Consider using `-export-*` for large result sets

## Notes

- Internal `-`'s in options can be omitted: `-nodigitgrouping`
- Switches can start with `/` instead of `-`
- Use double quotes to escape spaces and switches
- Switches can be disabled by prefixing with `no-`: `-no-size`
- Use `^` prefix or wrap with double quotes to escape special characters

## When to Use This Skill

Invoke this skill when:
- User asks about file searching on Windows
- User needs help with es command syntax
- User wants to search files efficiently
- User asks about Everything search tool
- User needs to export file lists
- User wants to find files by specific criteria (size, date, type, etc.)
- User mentions es command or Everything search
