# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based Excel data processing system designed for analyzing industrial safety and emergency response data, specifically for high-tech industries and firefighting organizations in Taiwan. The system processes Excel files from various sources, aggregates data, and generates consolidated reports organized by regions and categories.

## Architecture

The system follows a modular architecture with separation between data reading, pattern processing, domain analysis, and output operations.

### Core Components

- **`Read_excels_as_one.py`**: Main orchestration module with workflow functions and shared utilities
- **`utils/read_data.py`**: Core `read_data` class for Excel file reading with pattern support
- **`utils/patterns.py`**: Pattern-based extraction logic for domain-specific data parsing
- **`utils/output_excel.py`**: Excel output handler for multi-sheet workbook generation
- **`utils/data_cleaners.py`**: Data type standardization for chemical and equipment data
- **`utils/industry_analysis.py`**: Industrial data aggregation and grouping analysis
- **`utils/firefighter_analysis.py`**: Firefighter survey aggregation with training percentages

### Key Classes

- **`read_data`**: Generator-based Excel processor supporting multiple extraction patterns
  - **Patterns**: `default`, `苗栗縣`, `top_ten_operating_chemicals`, `sort_by_location`, `industry_rescue_equipment`, `firefighter_rescue_survey`
  - **Returns**: Generator yielding `(filename, (keys, values))` tuples
  - **Config**: Parameter dict with `path_data`, `pattern`, `path_output`, `file_name`, `folder_path`, `read_all_sheets`

### Data Processing Patterns

Pattern-specific extraction logic for diverse Excel formats:

1. **`top_ten_operating_chemicals`**: Extracts chemical storage data with 17-column schema (name, container, state, quantities)
2. **`industry_rescue_equipment`**: Parses rescue equipment from multi-section sheets (info, certifications, training, equipment)
3. **`firefighter_rescue_survey`**: Processes capability surveys with personnel and training data
   - Extracts personnel structure from "基本資料" sheets (ordered by rank hierarchy)
   - Aggregates certifications from "證書" sheets across four training levels
   - Calculates training percentages against total personnel composition
4. **`sort_by_location`**: Categorizes data by Taiwan regions (北部園區/中部園區/南部園區/其他)

### Main Processing Workflows

Each workflow follows a three-stage pipeline: folder processing → location sorting → analysis output.

1. **`high_tech_industry_chems_main()`**: Chemical storage processing
   - Groups by chemical name, container material, and storage state
2. **`high_tech_industry_rescue_equipment_main()`**: Equipment inventory analysis
   - Groups by certification, training, and equipment types
3. **`firefighter_training_survey_main()`**: Firefighter capability survey processing
   - Aggregates by city/division with training percentage calculations

## Common Development Commands

### Running the Application

```bash
# Run main processing (modify the main() function or workflow functions as needed)
python Read_excels_as_one.py

# The main entry point allows switching between different workflows by uncommenting the desired function
```

### Testing and Development

```bash
# Use Jupyter notebook for interactive development and testing
jupyter notebook Test.ipynb

# The Test.ipynb notebook contains experimental code and testing scenarios
```

## Key Configuration

### Data Paths
- Default input path: `../Data/科技廠救災能量` or `../Data/消防機關救災能量`
- Default output path: `/Output` (relative to input path)
- Excluded files: `("Output", "Distribution_by_city")` and various output file names

### Processing Parameters
The `read_data` class accepts a parameters dictionary with keys:
- `path_data`: Input data directory
- `pattern`: Processing pattern to use
- `path_output`: Output directory
- `file_name`: Output filename
- `folder_path`: Specific folder to process
- `read_all_sheets`: Whether to read all Excel sheets (default: True)

## Data Processing Flow

1. **Folder Tree Processing**: `process_folder_tree()` walks through subdirectories and processes Excel files
2. **Location Sorting**: `sort_by_location()` aggregates data by Taiwan regions
3. **Analysis**: `analyze_grouped()` performs groupby operations and generates summary reports

## Utility Functions

### Shared Utilities (Read_excels_as_one.py)

- **`process_folder_tree()`**: Walks subdirectories, reads Excel files by pattern, outputs consolidated files
- **`sort_by_location()`**: Aggregates processed files by Taiwan industrial park regions
- **`concat_list_dict()`**: Combines lists of DataFrames into single DataFrames
- **`list_subfolders()`**: Lists subdirectories excluding specified folder names
- **`ensure_dir()`**: Creates directories with parent path handling

### Data Cleaning (utils/data_cleaners.py)

- **`extract_first_number()`**: Extracts numeric values from mixed text/number cells using regex
- **`clean_chems()`**: Standardizes chemical data types (strings for names, floats for quantities)
- **`clean_equipment()`**: Standardizes equipment data types (strings for names, floats for counts)

### Pattern Processing (utils/patterns.py)

- **`merge_sheets_by_group()`**: Merges firefighter survey sheets using groupby operations
- **`process_basic_data_sheet()`**: Extracts personnel structure from basic info sheets
- **`drop_cells_with_string()`**: Removes example/template data from DataFrames

### Domain Analysis (utils/industry_analysis.py, utils/firefighter_analysis.py)

- **`analyze_grouped()`**: Groups industrial data by specified columns, applies cleaner, outputs sorted results
- **`analyze_ff_survey_files()`**: Aggregates firefighter training data across divisions with percentage calculations

## File Structure Expectations

The system expects Excel files in a hierarchical folder structure:
```
Data/
├── 科技廠救災能量/          # High-tech industry data
│   ├── [Company folders]/
│   └── *.xlsx files
├── 消防機關救災能量/        # Firefighter data
│   ├── [City folders]/
│   │   ├── [Division folders]/
│   │   └── *.xlsx files
└── Output/                  # Generated output files
```

## Dependencies

The project uses standard Python scientific computing libraries:
- pandas: Data manipulation and analysis
- numpy: Numerical operations
- openpyxl: Excel file writing
- pathlib: Path operations
- logging: Application logging

## Recent Changes

### PR #1: Firefighter Training Survey Analysis Module (Merged: Oct 1, 2025)

**Commits**: 7003a19, cbacec2, d7953a2, 1ab1e8c

**Summary**: Major refactoring implementing modular architecture for firefighter training survey analysis with automated aggregation and percentage calculations.

**New Modules Created**:
- `utils/firefighter_analysis.py`: Aggregates training certifications and personnel data with percentage calculations
- `utils/industry_analysis.py`: Processes industrial chemical storage and rescue equipment data
- `utils/data_cleaners.py`: Standardizes data types for chemical and equipment columns

**Key Improvements**:
- Extracted domain-specific logic into focused utility modules (44% reduction in main file size: 573→319 lines)
- Added `firefighter_training_survey_main()` workflow function with three-stage processing pipeline
- Enhanced `utils/patterns.py` with `firefighter_rescue_survey` pattern support
- Fixed potential `pd.concat()` error with empty data validation
- Added comprehensive docstrings and type hints

**Architecture Impact**: Transformed monolithic main file into modular system with clear separation between data reading (read_data), pattern extraction (patterns), domain analysis (industry_analysis, firefighter_analysis), data cleaning (data_cleaners), and output (output_excel).